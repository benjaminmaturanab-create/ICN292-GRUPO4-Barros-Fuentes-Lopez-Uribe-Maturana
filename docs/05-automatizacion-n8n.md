# 05 — Automatización con n8n

## Qué se automatiza y por qué

En el BPMN to-be de la E2 (ver [`02-bpmn.md`](02-bpmn.md)), después de cada movimiento el sistema evalúa el gateway **"¿Stock bajo mínimo?"**. Si la respuesta es **Sí**, se ejecuta la tarea **"Generar alerta"**.

En el dashboard, la alerta solo se ve si alguien lo abre. El flujo n8n hace que la alerta **llegue sola**: todos los días a las 09:00 revisa la base y, si hay productos bajo su mínimo, envía un correo a Alejandro con la lista ordenada por urgencia.

En la Entrega 1 esta tarea estaba planificada como un proceso `node-cron` dentro del backend. En la E2 se implementa con n8n, la herramienta del curso, porque el flujo queda visible, se puede modificar sin programar y se traza directamente al BPMN.

## Flujo

```
[Todos los días 09:00] ─┐
                        ├─> [Consultar stock bajo mínimo] ─> [Armar mensaje] ─> <¿Stock bajo mínimo?> ─Sí─> [Enviar alerta (Gmail)]
[Ejecución manual] ─────┘                                                                            └─No─> [Sin alertas: fin]
```

Archivo exportado: [`../n8n/flujo_alerta_stock.json`](../n8n/flujo_alerta_stock.json)

## Traza nodo n8n ↔ BPMN

| Nodo n8n | Tipo | Elemento BPMN | Qué hace |
|---|---|---|---|
| Todos los días 09:00 | Schedule Trigger | — | Inicia la revisión cada mañana, antes de preparar pedidos |
| Ejecución manual | Manual Trigger | — | Permite ejecutarlo a pedido (por ejemplo, en la defensa) |
| Consultar stock bajo mínimo (SQLite) | Execute Command | Carril *Sistema de Inventario* | Ejecuta `scripts/alertas_stock.py`, que lee `eliko.db` con la consulta de alertas (§6.2 del informe) y devuelve un JSON |
| Armar mensaje de alerta | Code | — | Convierte el JSON en un correo HTML con código, producto, categoría, stock, mínimo y déficit |
| ¿Stock bajo mínimo? | IF | **Gateway XOR "¿Stock bajo mínimo?"** | Continúa solo si `total_alertas > 0` |
| Enviar alerta por correo (Gmail) | Gmail | **Tarea "Generar alerta"** | Envía el correo a Alejandro |
| Sin alertas: fin | No Operation | Evento de fin | No envía nada si todo está sobre el mínimo |

## Por qué un script de Python

n8n no trae un nodo nativo para SQLite. El script `scripts/alertas_stock.py`:

- usa solo la biblioteca estándar de Python (`sqlite3`), que ya se necesita para el dashboard;
- funciona igual en Windows, macOS y Linux;
- usa la **misma consulta** de alertas que el dashboard y que la Consulta 2 de `consultas_analiticas.sql`, así el correo y el dashboard muestran lo mismo;
- si `eliko.db` no existe, la crea desde `schema.sql` + `seed.sql`.

Se puede probar sin n8n (debe imprimir un JSON):

```bash
python scripts/alertas_stock.py
```

Salida real con la base del repositorio (formateada):

```json
{"fecha_consulta": "2026-11-20 22:18", "total_alertas": 1, "deficit_total": 50,
 "productos": [{"codigo": "HOG001",
                "nombre": "Rascador Extensible Acero Inoxidable H2 Negro Manito Colgable 57cm",
                "categoria": "Hogar y jard\u00edn", "stock_actual": 0, "stock_minimo": 50, "deficit": 50}]}
```

Hoy solo 2 productos tienen stock mínimo definido, por lo que el correo incluirá 1 producto. A medida que se definan más umbrales, el flujo los incluirá sin cambios.

## Cómo ejecutarlo

1. Iniciar n8n en el mismo computador donde está clonado el repositorio. Desde n8n 2.0 el nodo **Execute Command** viene deshabilitado por seguridad, así que hay que habilitarlo al iniciar (probado con n8n 2.35.7):

   Windows (PowerShell):
   ```powershell
   $env:NODES_EXCLUDE='[]'; npx n8n
   ```
   macOS / Linux:
   ```bash
   NODES_EXCLUDE='[]' npx n8n
   ```
2. Abrir `http://localhost:5678` → **Create workflow** → menú `⋯` → **Import from File** → `n8n/flujo_alerta_stock.json`.
3. Nodo **Consultar stock bajo mínimo (SQLite)**: cambiar `C:/RUTA/AL/REPO/ICN292-GRUPO4-Barros-Fuentes-Lopez-Uribe-Maturana` por la ruta real. En macOS/Linux puede ser necesario usar `python3` en vez de `python`.
4. Nodo **Enviar alerta por correo (Gmail)**: crear o elegir la credencial de Gmail y escribir el correo de destino.
5. Presionar **Execute workflow** y revisar que el correo llegue.
6. Para que corra solo cada día, activar el workflow (interruptor **Active**). El computador debe estar encendido y n8n abierto a la hora programada.

## Problemas frecuentes

| Problema | Solución |
|---|---|
| `Unrecognized node type: n8n-nodes-base.executeCommand` o el nodo aparece con signo de pregunta | n8n se inició sin habilitar Execute Command. Cerrarlo y volver a iniciarlo con `NODES_EXCLUDE='[]'` (paso 1). |
| `python: command not found` | Usar `python3` o la ruta completa al ejecutable de Python. |
| El nodo Code falla con `Unexpected token` | El script imprimió un error en vez de JSON: ejecutar `python scripts/alertas_stock.py` en la terminal para ver el mensaje. |
| No llega el correo | Revisar la credencial de Gmail en n8n y la carpeta de spam. |

## Prueba realizada

El flujo se importó y ejecutó en n8n 2.35.7 con la base real del repositorio: los nodos *Ejecución manual*, *Consultar stock bajo mínimo*, *Armar mensaje de alerta* e *¿Stock bajo mínimo?* terminaron sin errores, el IF envió los datos a la rama **Sí** y el mensaje armado fue "[Eliko] 1 producto(s) bajo stock mínimo". El nodo de Gmail requiere la credencial de la cuenta que enviará el correo.

## Evidencia de ejecución

> **Pendiente (equipo):** agregar aquí las capturas del flujo ejecutado en n8n y del correo recibido.

<!-- ![Flujo ejecutado](../informe/img/n8n_ejecucion.png) -->
<!-- ![Correo recibido](../informe/img/n8n_correo.png) -->
