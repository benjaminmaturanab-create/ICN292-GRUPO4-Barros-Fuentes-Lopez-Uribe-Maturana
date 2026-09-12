# 2. Modelos de Procesos de Negocio (BPMN)

## 2.1 Modelo AS-IS (Proceso Actual)
![Diagrama AS-IS](../assets/AS-IS.png)

## 2.2 Modelo TO-BE (Proceso Propuesto con SIG)
![Diagrama TO-BE](../assets/TO-BE.png)

## 2.3 Explicación de Mejoras

Con la implementación del nuevo sistema (SIG), el flujo operativo de Electroliko pasa de ser reactivo a uno preventivo. Estas son las mejoras principales:

### Qué se automatiza
El descuento del stock. Ahora el sistema actualiza el inventario de forma automática cada vez que entra una venta de los canales integrados[cite: 1]. Esto ocurre en paralelo a la preparación del pedido, lo que evita que vendamos productos cuando queda solo una unidad y nos ahorra tener que actualizar las plataformas manualmente[cite: 1].

### Qué se controla
Los quiebres de inventario. Eliminamos la revisión visual en la bodega[cite: 3]. Ahora el sistema controla los niveles en tiempo real y lanza alertas automáticas cuando un producto cae bajo el umbral mínimo configurado[cite: 1]. Así, Alejandro puede priorizar la reposición antes de quedarse sin stock[cite: 1]. Para las ventas de canales sin integración, dejamos un punto de registro manual en el sistema para mantener el control[cite: 1].

### Qué se mide
La rotación de los productos y el impacto de las cancelaciones[cite: 1]. A través de un módulo automático, el sistema genera reportes semanales que entregan información clara para decidir qué productos comprar primero a los proveedores y medir las pérdidas por falta de stock[cite: 1].