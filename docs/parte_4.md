# E. Modelo de datos preliminar

| Entidad | PK candidata | Atributos principales | Relación | Cardinalidad |
|---|---|---|---|---|
| Producto | id_producto (PK) | nombre, categoría | Producto/Variante | 1 : N |
| Variante | id_variante (PK) | id_producto (FK), SKU, atributo, stock_actual, stock_minimo | Variante/Publicacion | 1 : N |
| Canal | id_canal (PK) | nombre, tipo integración | Canal/Publicacion | 1 : N |
| Publicacion | id_publicacion (PK) | id_variante (FK), id_canal (FK), id_externo, estado | Publicacion/Canal | 1 : N |
| Proveedor | id_proveedor (PK) | nombre, contacto | Proveedor/IngresoStock | 1 : N |
| IngresoStock | id_ingreso (PK) | id_variante (FK), id_proveedor (FK), fecha, cantidad | IngresoStock/Variante | 1 : N |
| Venta | id_venta (PK) | id_canal (FK), fecha, tipo_registro, estado | Venta/DetalleVenta | 1 : N |
| DetalleVenta | id_detalle (PK) | id_venta (FK), id_variante (FK), cantidad, precio_unitario | Variante/DetalleVenta | 1 : N |
| Cancelacion | id_cancelacion (PK) | id_venta (FK), motivo, fecha, monto_perdida | Venta/Cancelacion | 1 : 0..1 |
| AlertaStock | id_alerta (PK) | id_variante (FK), fecha_generada, umbral_configurado, estado | Variante/AlertaStock | 1 : N |

## Trazabilidad Proceso BPMN (To-Be) ↔ Modelo de Datos (ER)

El modelo de datos sostiene el flujo operativo To-Be a través de la interacción directa entre las tareas del proceso y las entidades del sistema:

- **Ingreso de mercadería:** Al registrar una entrada de stock en bodega, se crea un registro en IngresoStock vinculado al Proveedor y a la Variante, incrementando automáticamente su atributo stock_actual.
- **Venta y descuento automático:** Al concretarse una compra en cualquier canal, se genera un encabezado en Venta y sus líneas en DetalleVenta, las cuales descuentan de inmediato la cantidad vendida del stock_actual de la Variante.
- **Control de publicaciones multicanal:** La entidad Publicacion vincula los distintos canales de venta o la entidad canal con una única Variante física. Así, las 1.400 publicaciones de los 4 canales apuntan a un solo inventario consolidado, evitando vender productos agotados.
- **Alertas preventivas de stock:** Tras cada venta, el sistema evalúa si stock_actual es menor que stock_minimo. De cumplirse, crea un registro en AlertaStock que notifica a Alejandro antes de que ocurra un quiebre.
- **Registro de cancelaciones:** Si una venta se cancela, se crea un registro en Cancelacion asociado a la Venta, guardando el motivo y el monto_perdida para medir el impacto económico del problema.
- **Reportes y reposición:** Las tareas de generación de reportes leen los datos consolidados de DetalleVenta, IngresoStock y Cancelación para calcular la rotación de productos y sugerir a qué proveedores recomprar con prioridad.

### Diagrama ER

Diagrama hecho mediante la página web Draw.io usando la tabla anterior:

![Diagrama ER](media/image1.png)

## Arquitectura lógica y stack tentativo

| Componente | Capa | Tecnología | Responsabilidad | RF que sostiene |
|---|---|---|---|---|
| Panel Web | Interfaz / Captura | React + Vite + Tailwind CSS | Punto único de consulta. Incluye formularios de registro (ingresos, ventas manuales) y dashboards con gráficos para visualizar KPIs y alertas. | RF01, RF03, RF04, RF05, RF06, RF07, RF08 |
| API REST Backend | Aplicación / Lógica | Node.js + Express + node-cron | Expone endpoints para el modelo E, aplica el descuento automático de stock, calcula KPIs de rotación/pérdidas y ejecuta la tarea programada de alertas. | RF02, RF04, RF06, RF07, RF09 |
| Base de datos relacional | Persistencia | PostgreSQL 16 + Prisma ORM | Implementa el modelo Entidad-Relación de la Sección E. Funciona como la única fuente de verdad del stock consolidado de Eliko. | RF01–RF09 |
| Entorno de Despliegue | Infraestructura | Docker + Docker Compose | Empaqueta el frontend, backend y base de datos en contenedores aislando dependencias para garantizar reproducibilidad local. | Soporte general |

Para asegurar la reproducibilidad total en la entrega 2, el proyecto se desplegará mediante Docker Compose, integrando contenedores aislados para el backend, la base de datos y el frontend. Esto garantiza que cualquier integrante del equipo pueda levantar el sistema localmente en *localhost* con un único comando: `docker compose up`, obteniendo exactamente el mismo resultado y comportamiento sin importar el sistema operativo base.
