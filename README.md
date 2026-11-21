# ICN-292 — SIG de Inventario para Eliko (Electroliko | LapicaOnline)

**Universidad Técnica Federico Santa María · Campus Vitacura · Paralelo 100 · Segundo Semestre 2026**

Eliko es el nombre comercial de un negocio de e-commerce que opera bajo dos razones sociales: Comercial Electroliko SpA y La PicaOnline SpA. Vende productos importados en Mercado Libre (2 cuentas), Falabella y su página web, con cerca de 1.400 publicaciones activas y 800 ventas mensuales.

**Problema:** no tenían inventario centralizado. El stock se controlaba visualmente en bodega y se actualizaba a mano en cada plataforma, lo que generaba 3–4 cancelaciones de venta al mes por quiebre de stock (pérdidas de $100.000 a $300.000 por evento).

**Solución (Entrega 2):** base de datos relacional en 3FN con el inventario real levantado en terreno (767 productos), dashboard web con KPIs y alertas, 5 consultas SQL de negocio y una automatización n8n que avisa por correo cuando un producto queda bajo su stock mínimo.

- **Sistema en línea:** https://eliko-inventario-hcyyqk7oxjlhuwa94pkns2.streamlit.app
- **Motor SQL:** SQLite 3
- **Informe E2:** [`informe/E2/`](informe/E2/) · **Informe E1:** [`informe/`](informe/) · **Presentación:** [`presentacion/`](presentacion/)

## Integrantes

| Nombre | Rol USM | Función en el proyecto |
|---|---|---|
| Rodrigo Barros | 202360546-8 | Desarrollo del sistema y base de datos |
| Iovanni Fuentes | 202360570-0 | Comunicación con la PYME y carga de base de datos |
| Benjamín Maturana | 202304540-3 | Carga de base de datos y organización del inventario |
| Alonso López | 202360535-2 | Carga de base de datos y organización del inventario |
| Maximiliano Uribe | 202360533-6 | Carga de base de datos y organización del inventario |

---

## Guía de uso (entorno limpio)

Requisitos: **Git**, **Python 3.10+** y, opcionalmente, el programa **`sqlite3`**.

### 1. Clonar el repositorio

```bash
git clone https://github.com/benjaminmaturanab-create/ICN292-GRUPO4-Barros-Fuentes-Lopez-Uribe-Maturana
cd ICN292-GRUPO4-Barros-Fuentes-Lopez-Uribe-Maturana
```

### 2. Crear y cargar la base de datos

Con el programa `sqlite3`:

```bash
sqlite3 eliko.db < schema.sql
sqlite3 eliko.db < seed.sql
```

Si el computador no tiene `sqlite3` (por ejemplo, Windows sin instalación adicional), Python trae SQLite incluido:

```bash
python -c "import sqlite3; c=sqlite3.connect('eliko.db'); [c.executescript(open(f, encoding='utf-8').read()) for f in ('schema.sql','seed.sql')]; c.commit()"
```

Comprobar la carga (debe devolver `767`):

```bash
sqlite3 eliko.db "SELECT COUNT(*) FROM producto;"
```

> Para partir de cero, borrar `eliko.db` antes de volver a ejecutar `schema.sql`.

### 3. Ejecutar las consultas de negocio

```bash
sqlite3 -header -column eliko.db < consultas_analiticas.sql
```

Las 5 consultas, su salida real y su interpretación están en [`docs/04-sql-consultas.md`](docs/04-sql-consultas.md).

### 4. Abrir el dashboard

```bash
pip install -r requirements.txt
streamlit run app.py
```

Se abre en el navegador (por defecto `http://localhost:8501`). Si `eliko.db` no existe, `app.py` la crea sola desde `eliko_db.sql`.

### 5. Automatización n8n (alerta de stock bajo mínimo)

El flujo usa el nodo **Execute Command**, que desde n8n 2.0 hay que habilitar al iniciar:

```powershell
# Windows (PowerShell)
$env:NODES_EXCLUDE='[]'; npx n8n
```

```bash
# macOS / Linux
NODES_EXCLUDE='[]' npx n8n
```

1. Abrir `http://localhost:5678`, crear un workflow y elegir **Import from File** → `n8n/flujo_alerta_stock.json`.
2. En el nodo **Consultar stock bajo mínimo (SQLite)**, reemplazar `C:/RUTA/AL/REPO/` por la ruta real de este repositorio.
3. En el nodo **Enviar alerta por correo (Gmail)**, elegir una credencial de Gmail y el correo de destino.
4. Presionar **Execute workflow**.

Detalle y solución de problemas en [`docs/05-automatizacion-n8n.md`](docs/05-automatizacion-n8n.md).

---

## Lógica del repositorio

```
├── README.md                     Este archivo
├── app.py                        Dashboard Streamlit
├── requirements.txt              Dependencias Python
├── schema.sql                    Tablas, PK, FK, CHECK e índices
├── seed.sql                      Datos: 17 categorías y 767 productos
├── eliko_db.sql                  schema + seed en un archivo (lo usa app.py)
├── consultas_analiticas.sql      5 consultas de negocio
├── Inventario_Bodega_Eliko_14_10_2026.csv   Datos originales del conteo en terreno
├── CHANGELOG.md                  Cambios desde la Entrega 1
├── DECLARACION_IA.md             Uso declarado de IA
├── ENLACE_GITHUB.txt             URL y tag de la versión defendida
├── assets/                       Diagramas (BPMN E1 y E2, ER E1 y E2) y capturas del dashboard
├── docs/
│   ├── 00-caso-pyme.md           PYME, problema y alcance E2
│   ├── 01-requerimientos.md      Requisitos E1 y su estado en la E2
│   ├── 02-bpmn.md                BPMN as-is/to-be E1 y to-be final E2
│   ├── parte_4.md                Modelo de datos preliminar (E1)
│   ├── 03-modelo-datos.md        ER en 3FN y diccionario de datos (E2)
│   ├── 04-sql-consultas.md       Consultas, resultados reales e interpretación
│   └── 05-automatizacion-n8n.md  Flujo n8n trazado al BPMN
├── n8n/flujo_alerta_stock.json   Flujo n8n exportado
├── scripts/
│   ├── alertas_stock.py          Consulta de alertas que ejecuta n8n
│   └── separar_sql.py            Genera schema.sql y seed.sql desde eliko_db.sql
├── informe/                      Informe E1 (PDF + LaTeX) y E2 en informe/E2/
└── presentacion/                 Diapositivas de la defensa
```

## Calidad de los datos del CSV original

Reglas aplicadas al cargar `Inventario_Bodega_Eliko_14_10_2026.csv` (768 filas):

- 1 fila sin SKU se omitió, porque sin clave primaria no puede cargarse.
- 73 productos sin nombre se cargaron como `"Producto {SKU}"`, para completarlos después.
- 23 productos sin categoría la recibieron según el prefijo de su SKU (ACC → Accesorios celular, etc.).
- 2 productos tenían un stock mínimo numérico y se cargaron tal cual; otros 2 tenían una nota de texto ("revisar 24 piezas") y quedaron sin umbral.

## Entrega 1

El diagnóstico y diseño de la Entrega 1 se conservan en este repositorio: [`docs/00-caso-pyme.md`](docs/00-caso-pyme.md), [`docs/01-requerimientos.md`](docs/01-requerimientos.md), [`docs/02-bpmn.md`](docs/02-bpmn.md), [`docs/parte_4.md`](docs/parte_4.md), [`assets/`](assets/) e [`informe/`](informe/). Qué se mantuvo y qué cambió está en [`CHANGELOG.md`](CHANGELOG.md).
