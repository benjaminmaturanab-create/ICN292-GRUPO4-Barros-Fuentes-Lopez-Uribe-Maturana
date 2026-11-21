# Declaración de uso de Inteligencia Artificial

**Proyecto:** SIG de inventario Eliko — ICN-292, Entrega 2, Paralelo 100
**Herramienta:** Claude (Anthropic)

> **Revisar antes de entregar:** cada integrante debe confirmar que esta lista refleja lo que realmente se hizo con IA. Agregar o quitar filas según corresponda.

## Usos

| Área | Uso de la IA | Trabajo del equipo |
|---|---|---|
| Datos | Conversión del CSV del inventario a sentencias `INSERT`, aplicando las reglas de limpieza del README | El inventario se levantó en terreno por el equipo. **La IA no inventó datos**: todos los valores de `seed.sql` provienen de `Inventario_Bodega_Eliko_14_10_2026.csv`, salvo las reglas de limpieza documentadas (nombres faltantes como "Producto {SKU}" y categorías inferidas del prefijo del SKU) |
| Esquema SQL y consultas | Apoyo en la escritura de `CREATE TABLE`, de las 5 consultas de negocio y del script `separar_sql.py` | El modelo ER y la normalización fueron diseñados por el equipo; las consultas se ejecutaron sobre la base real |
| Dashboard | Apoyo en la escritura del código Python/Streamlit y depuración de la autoinicialización de la base | El equipo ejecutó, probó y desplegó la aplicación |
| Automatización | Diseño del flujo n8n y del script `alertas_stock.py` | El equipo importó el flujo, configuró la credencial y lo ejecutó |
| Informe y documentación | Apoyo en redacción, formato LaTeX, archivos `.md` y revisión de coherencia entre informe y repositorio | El equipo revisó el contenido y confirmó los datos y decisiones |

## Lo que no se hizo con IA
- Levantamiento del inventario en terreno y comunicación con la PYME.
- Decisiones de alcance y de diseño.
- Ejecución del código y de las consultas SQL: todos los resultados del informe provienen de la base.

## Compromiso
Todos los integrantes comprenden el código y los documentos entregados y pueden explicarlos en la defensa. El uso de IA se declara según la política del curso (enunciado E2, §5).
