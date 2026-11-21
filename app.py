"""
app.py — Dashboard KPI · Eliko Bodega
ICN-292 PIP2 · UTFSM 2026-2

Uso:
    streamlit run app.py

Requiere eliko.db en el mismo directorio, o ajusta DB_PATH.
"""

import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# Configuración
# ─────────────────────────────────────────────────────────────
_repo_root = Path(__file__).parent.parent

# Busca eliko.db en db/ relativo al repo, o en el directorio actual
DB_PATH = _repo_root / "db" / "eliko.db"
if not DB_PATH.exists():
    DB_PATH = Path("eliko.db")

# Busca el SQL seed en db/ o en el directorio actual
SQL_SEED = _repo_root / "db" / "eliko_db.sql"
if not SQL_SEED.exists():
    SQL_SEED = Path("eliko_db.sql")

def _init_db():
    """Inicializa la BD desde el SQL seed si no existe."""
    if DB_PATH.exists():
        return
    if not SQL_SEED.exists():
        return
    db_dir = DB_PATH.parent
    db_dir.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(DB_PATH))
    con.executescript(SQL_SEED.read_text(encoding="utf-8"))
    con.commit()
    con.close()

_init_db()

st.set_page_config(
    page_title="Eliko Bodega — Dashboard",
    page_icon="📦",
    layout="wide",
)

# ─────────────────────────────────────────────────────────────
# Conexión a la base de datos
# ─────────────────────────────────────────────────────────────
@st.cache_resource
def get_connection():
    if not DB_PATH.exists():
        st.error(f"Base de datos no encontrada en: {DB_PATH}")
        st.stop()
    return sqlite3.connect(str(DB_PATH), check_same_thread=False)

@st.cache_data(ttl=30)
def query(_con, sql):
    return pd.read_sql_query(sql, _con)

con = get_connection()

# ─────────────────────────────────────────────────────────────
# Queries
# ─────────────────────────────────────────────────────────────
SQL_ALERTAS = """
SELECT p.sku, p.nombre_producto, c.nombre_categoria,
       i.stock_actual, i.stock_minimo,
       (i.stock_minimo - i.stock_actual) AS unidades_a_reponer
FROM inventario i
JOIN producto  p ON p.sku = i.sku
JOIN categoria c ON c.id_categoria = p.id_categoria
WHERE i.stock_minimo IS NOT NULL AND i.stock_actual < i.stock_minimo
ORDER BY unidades_a_reponer DESC
"""

SQL_POR_CATEGORIA = """
SELECT c.nombre_categoria,
       COUNT(p.sku)                  AS total_productos,
       SUM(i.stock_actual)           AS total_unidades,
       ROUND(AVG(i.stock_actual), 1) AS promedio_unidades
FROM categoria c
JOIN producto  p ON p.id_categoria = c.id_categoria
JOIN inventario i ON i.sku = p.sku
GROUP BY c.nombre_categoria
ORDER BY total_unidades DESC
"""

SQL_SIN_MOVIMIENTO = """
SELECT p.sku, p.nombre_producto, c.nombre_categoria,
       i.stock_actual, i.fecha_actualizacion AS ultima_actualizacion
FROM producto  p
JOIN inventario i ON i.sku = p.sku
JOIN categoria  c ON c.id_categoria = p.id_categoria
WHERE p.sku NOT IN (
    SELECT DISTINCT sku FROM movimiento_stock
    WHERE fecha_movimiento >= datetime('now', '-28 days')
)
  AND i.stock_actual > 0
ORDER BY i.stock_actual DESC
"""

SQL_TOP_STOCK = """
SELECT p.sku, p.nombre_producto, c.nombre_categoria, i.stock_actual
FROM inventario i
JOIN producto  p ON p.sku = i.sku
JOIN categoria c ON c.id_categoria = p.id_categoria
ORDER BY i.stock_actual DESC
LIMIT 10
"""

SQL_RESUMEN = """
SELECT
    (SELECT COUNT(*) FROM producto)   AS total_productos,
    (SELECT COUNT(*) FROM categoria)  AS total_categorias,
    (SELECT SUM(stock_actual) FROM inventario)        AS total_unidades,
    (SELECT COUNT(*) FROM inventario WHERE stock_minimo IS NOT NULL
         AND stock_actual < stock_minimo)             AS alertas_activas,
    (SELECT COUNT(*) FROM movimiento_stock)           AS total_movimientos
"""

# ─────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────
st.title("📦 Eliko Bodega — Dashboard de Inventario")
st.caption("ICN-292 · UTFSM 2026-2 · Datos al 14/10/2026")

# ─────────────────────────────────────────────────────────────
# KPI tiles
# ─────────────────────────────────────────────────────────────
resumen = query(con, SQL_RESUMEN).iloc[0]

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Productos",   f"{resumen['total_productos']:,}")
col2.metric("Categorías",  f"{resumen['total_categorias']:,}")
col3.metric("Unidades totales", f"{int(resumen['total_unidades']):,}")
col4.metric("⚠️ Alertas reposición", f"{resumen['alertas_activas']:,}")
col5.metric("Movimientos registrados", f"{resumen['total_movimientos']:,}")

st.divider()

# ─────────────────────────────────────────────────────────────
# Fila 1: Stock por categoría
# ─────────────────────────────────────────────────────────────
st.subheader("Stock por categoría")

df_cat = query(con, SQL_POR_CATEGORIA)

col_chart, col_table = st.columns([2, 1])

with col_chart:
    fig = px.bar(
        df_cat,
        x="total_unidades",
        y="nombre_categoria",
        orientation="h",
        color="total_unidades",
        color_continuous_scale="Blues",
        labels={"total_unidades": "Unidades", "nombre_categoria": "Categoría"},
        height=420,
    )
    fig.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=10, b=0),
        yaxis=dict(autorange="reversed"),
    )
    st.plotly_chart(fig, use_container_width=True)

with col_table:
    st.dataframe(
        df_cat.rename(columns={
            "nombre_categoria": "Categoría",
            "total_productos": "Productos",
            "total_unidades": "Unidades",
            "promedio_unidades": "Prom/producto",
        }),
        hide_index=True,
        use_container_width=True,
        height=420,
    )

st.divider()

# ─────────────────────────────────────────────────────────────
# Fila 2: Alertas de reposición + Top 10
# ─────────────────────────────────────────────────────────────
col_alertas, col_top = st.columns(2)

with col_alertas:
    st.subheader("⚠️ Alertas de reposición")
    df_alertas = query(con, SQL_ALERTAS)
    if df_alertas.empty:
        st.success("No hay productos bajo el stock mínimo.")
    else:
        st.dataframe(
            df_alertas.rename(columns={
                "sku": "SKU",
                "nombre_producto": "Producto",
                "nombre_categoria": "Categoría",
                "stock_actual": "Stock actual",
                "stock_minimo": "Mínimo",
                "unidades_a_reponer": "A reponer",
            }),
            hide_index=True,
            use_container_width=True,
            height=300,
        )
        st.caption(f"{len(df_alertas)} producto(s) requieren reposición")

with col_top:
    st.subheader("📊 Top 10 mayor stock")
    df_top = query(con, SQL_TOP_STOCK)
    fig2 = px.bar(
        df_top,
        x="sku",
        y="stock_actual",
        color="nombre_categoria",
        labels={"stock_actual": "Unidades", "sku": "SKU", "nombre_categoria": "Categoría"},
        height=320,
    )
    fig2.update_layout(margin=dict(l=0, r=0, t=10, b=0), showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────────────────────
# Fila 3: Productos sin movimiento
# ─────────────────────────────────────────────────────────────
st.subheader("🕐 Productos sin movimiento (últimas 4 semanas)")
df_sin_mov = query(con, SQL_SIN_MOVIMIENTO)

if df_sin_mov.empty:
    st.info("Todos los productos han tenido movimiento reciente.")
else:
    st.dataframe(
        df_sin_mov.rename(columns={
            "sku": "SKU",
            "nombre_producto": "Producto",
            "nombre_categoria": "Categoría",
            "stock_actual": "Stock",
            "ultima_actualizacion": "Última actualización",
        }),
        hide_index=True,
        use_container_width=True,
        height=300,
    )
    st.caption(
        f"⚠️ {len(df_sin_mov)} productos con stock > 0 sin movimiento registrado. "
        "Nota: la tabla movimiento_stock se alimenta con el uso del sistema; "
        "al iniciar, todos aparecen aquí hasta que se registren operaciones."
    )

st.divider()

# ─────────────────────────────────────────────────────────────
# Búsqueda por SKU
# ─────────────────────────────────────────────────────────────
st.subheader("🔍 Buscar producto")
sku_input = st.text_input("Ingresa un SKU (ej: ACC001, CAB040K)").strip().upper()

if sku_input:
    df_prod = query(con, f"""
        SELECT p.sku, p.nombre_producto, c.nombre_categoria,
               i.stock_actual, i.stock_minimo,
               i.fecha_actualizacion, i.comentario
        FROM producto p
        JOIN categoria c ON c.id_categoria = p.id_categoria
        JOIN inventario i ON i.sku = p.sku
        WHERE p.sku = '{sku_input}'
    """)
    if df_prod.empty:
        st.warning(f"SKU '{sku_input}' no encontrado.")
    else:
        st.dataframe(df_prod, hide_index=True, use_container_width=True)

        df_mov = query(con, f"""
            SELECT fecha_movimiento, tipo_movimiento, cantidad, motivo
            FROM movimiento_stock WHERE sku = '{sku_input}'
            ORDER BY fecha_movimiento DESC
        """)
        if df_mov.empty:
            st.caption("Sin movimientos registrados para este SKU.")
        else:
            st.caption(f"Historial de movimientos ({len(df_mov)} registros)")
            st.dataframe(df_mov, hide_index=True, use_container_width=True)
