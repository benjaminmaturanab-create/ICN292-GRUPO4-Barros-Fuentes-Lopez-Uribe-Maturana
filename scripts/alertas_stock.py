
import argparse
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

CONSULTA_ALERTAS = """
SELECT
    p.sku                             AS codigo,
    p.nombre_producto                 AS nombre,
    c.nombre_categoria                AS categoria,
    i.stock_actual,
    i.stock_minimo,
    (i.stock_minimo - i.stock_actual) AS deficit
FROM inventario i
JOIN producto  p ON p.sku = i.sku
JOIN categoria c ON c.id_categoria = p.id_categoria
WHERE i.stock_minimo IS NOT NULL
  AND i.stock_actual < i.stock_minimo
ORDER BY deficit DESC;
"""


def crear_bd_si_no_existe(ruta_db: Path) -> None:
    if ruta_db.exists():
        return
    schema, seed, unico = RAIZ / "schema.sql", RAIZ / "seed.sql", RAIZ / "eliko_db.sql"
    if schema.exists() and seed.exists():
        scripts = [schema, seed]
    elif unico.exists():
        scripts = [unico]
    else:
        sys.exit(f"No existe {ruta_db} ni los scripts SQL para crearla en {RAIZ}")
    con = sqlite3.connect(ruta_db)
    try:
        for s in scripts:
            con.executescript(s.read_text(encoding="utf-8"))
        con.commit()
    finally:
        con.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Alertas de reposición Eliko")
    por_defecto = RAIZ / "eliko.db"
    if not por_defecto.exists() and (RAIZ / "db" / "eliko.db").exists():
        por_defecto = RAIZ / "db" / "eliko.db"
    parser.add_argument("--db", default=str(por_defecto), help="Ruta a eliko.db")
    args = parser.parse_args()

    ruta_db = Path(args.db)
    crear_bd_si_no_existe(ruta_db)

    con = sqlite3.connect(ruta_db)
    con.row_factory = sqlite3.Row
    try:
        filas = [dict(f) for f in con.execute(CONSULTA_ALERTAS)]
    finally:
        con.close()

    salida = {
        "fecha_consulta": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_alertas": len(filas),
        "deficit_total": sum(f["deficit"] for f in filas),
        "productos": filas,
    }
    # ensure_ascii=True evita problemas de codificación en la consola de Windows
    print(json.dumps(salida, ensure_ascii=True))


if __name__ == "__main__":
    main()
