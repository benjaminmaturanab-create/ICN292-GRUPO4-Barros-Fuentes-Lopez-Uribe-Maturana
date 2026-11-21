# 05 — Automatización con n8n

## Qué se automatiza y por qué

En el BPMN to-be de la E2 (ver [`02-bpmn.md`](02-bpmn.md)), después de cada movimiento el sistema evalúa el gateway **"¿Stock bajo mínimo?"**. Si la respuesta es **Sí**, se ejecuta la tarea **"Generar alerta"**.

En el dashboard, la alerta solo se ve si alguien lo abre. El flujo n8n hace que la alerta **llegue sola**: todos los días a las 09:00 revisa el inventario y, si hay productos bajo su mínimo, envía un correo a Alejandro con la lista ordenada por urgencia.

En la Entrega 1 esta tarea estaba planificada como un proceso `node-cron` dentro del backend. En la E2 se implementa con n8n, la herramienta del curso, porque el flujo queda visible, se puede modificar sin programar y se traza directamente al BPMN.

## Versión principal: n8n Cloud

Archivo: [`../n8n/flujo_alerta_stock_cloud.json`](../n8n/flujo_alerta_stock_cloud.json)

```
[Todos los días 09:00] ─┐
                        ├─> [Leer base de datos (seed.sql en GitHub)] ─> [Calcular alertas y armar mensaje] ─> <¿Stock bajo mínimo?> ─Sí─> [Enviar alerta (Gmail)]
[Ejecución manual] ─────┘                                                                                                         └─No─> [Sin alertas: fin]
```

n8n Cloud no puede ejecutar comandos ni leer archivos de un computador, así que el flujo lee la base desde el repositorio público:

`https://raw.githubusercontent.com/benjaminmaturanab-create/ICN292-GRUPO4-Barros-Fuentes-Lopez-Uribe-Maturana/main/seed.sql`

| Nodo n8n | Tipo | Elemento BPMN | Qué hace |
|---|---|---|---|
| Todos los días 09:00 | Schedule Trigger | — | Inicia la revisión cada mañana, antes de preparar pedidos |
| Ejecución manual | Manual Trigger | — | Permite ejecutarlo a pedido (por ejemplo, en la defensa) |
| Leer base de datos (seed.sql en GitHub) | HTTP Request | Carril *Sistema de Inventario* | Descarga `seed.sql` del repositorio |
| Calcular alertas y armar mensaje | Code (JavaScript) | Gateway "¿Stock bajo mínimo?" (evaluación) | Lee las tablas `categoria`, `producto` e `inventario` del seed y aplica la misma regla que la Consulta 2 de `consultas_analiticas.sql`: `stock_minimo IS NOT NULL AND stock_actual < stock_minimo`, ordenando por déficit. Arma el correo HTML |
| ¿Stock bajo mínimo? | IF | **Gateway XOR "¿Stock bajo mínimo?"** | Continúa solo si `total_alertas > 0` |
| Enviar alerta por correo (Gmail) | Gmail | **Tarea "Generar alerta"** | Envía el correo a Alejandro |
| Sin alertas: fin | No Operation | Evento de fin | No envía nada si todo está sobre el mínimo |

### Verificación

El nodo de código se comparó con la base SQLite: con el `seed.sql` del repositorio entrega **767 productos, 17 categorías, 1 alerta (HOG001, déficit 50), 308 agotados y 72 productos críticos sin umbral**, los mismos valores de las Consultas 1, 2 y 5 (ver [`04-sql-consultas.md`](04-sql-consultas.md)). El flujo completo se ejecutó en n8n 2.35.7 leyendo el archivo real desde GitHub: todos los nodos terminaron sin errores hasta el envío del correo, que requiere la credencial de Gmail.

### Cómo ejecutarlo en n8n Cloud

1. Entrar a [n8n.io](https://n8n.io) e iniciar sesión.
2. **Create workflow** → menú `⋯` → **Import from File** → `n8n/flujo_alerta_stock_cloud.json`.
3. Abrir el nodo **Enviar alerta por correo (Gmail)** → **Credential → Create new → Sign in with Google** y autorizar la cuenta. En **To**, escribir el correo de destino.
4. Presionar **Execute workflow**. Debe llegar un correo con el asunto "[Eliko] 1 producto(s) bajo stock mínimo".
5. Para que corra solo cada día, activar el workflow (**Active**).

### Limitación

El flujo lee el inventario cargado en el repositorio (`seed.sql`). Si en el futuro se registran movimientos en una base alojada en un servidor, el nodo HTTP Request se reemplaza por una consulta a esa base y el resto del flujo no cambia.

## Versión alternativa: n8n local

Para ejecutar n8n en el propio computador, con la base `eliko.db` local:

- [`../n8n/flujo_alerta_stock.json`](../n8n/flujo_alerta_stock.json): consulta la base con `scripts/alertas_stock.py` y envía por Gmail.
- [`../n8n/flujo_alerta_stock_smtp.json`](../n8n/flujo_alerta_stock_smtp.json): igual, pero envía por SMTP con una contraseña de aplicación de Google (Host `smtp.gmail.com`, Port `465`, SSL activado).

Ambos usan el nodo **Execute Command**, que desde n8n 2.0 hay que habilitar al iniciar:

```powershell
$env:NODES_EXCLUDE='[]'; npx n8n
```

En el nodo **Consultar stock bajo mínimo (SQLite)** hay que reemplazar `C:/RUTA/AL/REPO/` por la ruta real del repositorio. El script se puede probar sin n8n con `python scripts/alertas_stock.py`.

## Evidencia de ejecución

El flujo se ejecutó en la instancia de n8n Cloud del equipo el 20/11/2026. Todos los nodos de la rama "true" terminaron con éxito y el correo de alerta llegó correctamente.

![Flujo ejecutado en n8n Cloud](../assets/n8n-ejecucion.png)

<img src="../assets/n8n-correo.png" alt="Correo de alerta recibido" width="380">
