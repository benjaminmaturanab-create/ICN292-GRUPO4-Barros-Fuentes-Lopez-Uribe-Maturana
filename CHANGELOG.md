# CHANGELOG — Cambios desde la Entrega 1

Formato: qué se mantuvo, qué cambió y por qué. Detalle completo en el informe E2, §2.

## [v1.0-e2] — Noviembre 2026 (Entrega 2)

### Se mantiene
- Misma PYME (Eliko: Comercial Electroliko SpA / La PicaOnline SpA) y mismo problema de fondo: falta de inventario centralizado y quiebres de stock.
- Mismo equipo (P100, 5 integrantes) y mismo repositorio.
- Objetivo de reproducibilidad: cualquiera puede clonar el repo y levantar la base.

### Agregado
- Base de datos SQLite en 3FN: `schema.sql`, `seed.sql` y `eliko_db.sql`.
- Datos reales: inventario físico levantado en terreno (767 productos, 17 categorías, 8.964 unidades), con reglas de limpieza documentadas en el README.
- Dashboard Streamlit (`app.py`) con 5 KPIs, stock por categoría, alertas, top 10, productos sin movimiento y búsqueda por SKU.
- 5 consultas SQL de negocio (`consultas_analiticas.sql`) con resultados reales en `docs/04-sql-consultas.md`.
- Automatización n8n de la tarea BPMN "Generar alerta" (`n8n/flujo_alerta_stock.json`, `scripts/alertas_stock.py`).
- BPMN to-be final con el gateway "¿Existe en sistema?" (`assets/BPMN-TO-BE-E2.png`, `assets/bpmn_inventario_eliko.drawio`).
- ER final (`assets/ER-E2.png`) y documentación `docs/03`, `docs/04`, `docs/05`.
- `DECLARACION_IA.md`, este `CHANGELOG.md`, `ENLACE_GITHUB.txt`, informe E2 en `informe/E2/`.

### Cambiado
- **Alcance:** de inventario multicanal (4 canales) a inventario consolidado de bodega. Motivo: sin una base de stock confiable, el descuento automático por venta se aplicaría sobre datos incorrectos. En la E1 ya estaba prevista la mitigación de partir con un conteo físico, y la integración vía API estaba marcada como *Won't* (RF10).
- **Modelo de datos:** de 10 entidades preliminares a 4 tablas en 3FN.
  - Producto + Variante → `producto` (cada variante tiene su propio SKU)
  - stock de Variante → `inventario` (tabla nueva, 1:1 con producto)
  - categoría (atributo) → `categoria` (entidad propia)
  - IngresoStock + DetalleVenta → `movimiento_stock` (ENTRADA / SALIDA / AJUSTE)
  - AlertaStock → consulta calculada
- **BPMN:** de proceso de venta-despacho con 5+ actores a proceso de bodega con 2 carriles.
- **Stack:** React + Node/Express + PostgreSQL + Docker → Streamlit + Python + SQLite + Streamlit Community Cloud.
- **Automatización:** tarea `node-cron` planificada → flujo n8n.
- `docs/02-bpmn.md`: se quitaron marcas `[cite: …]` que habían quedado del borrador.

### Diferido (siguiente etapa)
- Formulario de registro de entradas y salidas en el dashboard.
- Definir el stock mínimo de los productos (hoy solo 2 de 767 lo tienen).
- Entidades Canal, Publicación, Venta, Cancelación y Proveedor.
- RF06 (asociación multicanal), RF08 (motivo de cancelación), RF10 (integración API).
- Autenticación y roles.
