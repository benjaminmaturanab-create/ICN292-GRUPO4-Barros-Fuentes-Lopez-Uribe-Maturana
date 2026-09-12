# 01 — Requerimientos

Proyecto: sistema de gestión de inventario centralizado para Electroliko y LapicaOnline, negocio de Alejandro Olguín.
El contexto completo del problema está descrito en `00-caso-pyme.md`.

## C.1 Actores y roles

A partir del BPMN as-is levantado por el equipo, identificamos a los actores humanos y a los sistemas externos que participan en el proceso de gestión de inventario y ventas.

| Actor o sistema | Tipo | Rol en el proceso |
|---|---|---|
| Alejandro Olguín | Humano, dueño y operador | Revisa el dashboard de ventas, imprime etiquetas, gestiona el stock, cancela ventas cuando no hay disponibilidad, actualiza el inventario manualmente y contacta a los proveedores. |
| Pareja de Alejandro | Humano, operadora | Apoya en la recolección, el embalaje y la verificación de los productos que se van a despachar. |
| Persona a medio tiempo | Humano, operador de despacho | Apoya en el ordenamiento, embalaje, etiquetado y envío de mercadería a la bodega Full. |
| Mercado Libre, cuenta Electroliko | Sistema externo | Canal de venta; recibe las actualizaciones de stock y pausa las publicaciones que se quedan sin disponibilidad. |
| Mercado Libre, cuenta LapicaOnline | Sistema externo | Segundo canal de venta que opera bajo la misma lógica que el anterior. |
| Falabella | Sistema externo | Canal de venta marketplace. |
| Página web Eliko | Sistema externo | Canal de venta propio del negocio. |
| Bodega Full | Sistema y servicio externo | Recibe, almacena y despacha los productos que se gestionan bajo la modalidad Full. |
| Proveedor | Sistema y actor externo | Es el origen de la mercadería y se contacta cuando corresponde reponer stock. |

## C.2 Alcance in / out

**Dentro del alcance:**
- Registro de los ingresos de mercadería por producto y variante.
- Registro y descuento del stock cada vez que se concreta una venta, en cualquiera de los cuatro canales.
- Vista consolidada del stock disponible por producto y variante, actualizada de forma prácticamente inmediata.
- Alertas automáticas cuando el stock de un producto cae bajo un umbral que se pueda configurar.
- Registro manual de ventas para los canales que todavía no cuentan con integración automática.
- Reportes básicos de rotación de productos y de cancelaciones asociadas a la falta de stock.
- Apoyo a la decisión de reposición, indicando qué producto conviene reponer y con qué prioridad.

**Fuera del alcance de esta entrega dejamos lo siguiente:**
- La integración automática vía API con cada plataforma, que queda planteada como una evolución para la Entrega 2.
- La gestión contable, la facturación electrónica o los temas tributarios del negocio.
- La gestión de relación con clientes y el marketing o la publicación de nuevos productos.
- La logística de última milla que ya está delegada a la bodega Full o al operador de despacho.
- La gestión de recursos humanos del equipo, como turnos o remuneraciones.
- La automatización de la creación de nuevas publicaciones.

## C.3 Requisitos Funcionales

Priorizamos los requisitos con la técnica MoSCoW y los trazamos directamente al problema identificado en la Sección B.

| ID | Requisito funcional | Prioridad | Trazabilidad al problema |
|---|---|---|---|
| RF01 | El sistema debe permitir registrar el ingreso de mercadería, indicando producto, variante, cantidad, fecha y proveedor. | Must | Hoy no existe un inventario centralizado, lo que impide conocer con certeza cuánto stock hay disponible. |
| RF02 | El sistema debe descontar automáticamente el stock disponible cuando se registra una venta en cualquier canal. | Must | Evita que un mismo producto se venda en dos plataformas distintas cuando solo queda una unidad. |
| RF03 | El sistema debe mostrar el stock consolidado por producto y variante, visible para todo el equipo. | Must | Elimina la necesidad de revisar físicamente los estantes de la bodega para saber cuánto queda. |
| RF04 | El sistema debe generar una alerta cuando el stock de un producto caiga bajo un umbral que se pueda configurar. | Must | Reemplaza el control reactivo actual por uno preventivo, anticipándose al quiebre de stock. |
| RF05 | El sistema debe permitir registrar manualmente una venta en los canales que todavía no cuenten con integración automática. | Should | Mantiene el flujo operativo funcionando mientras no exista integración con las cuatro plataformas. |
| RF06 | El sistema debe permitir asociar un mismo producto físico con sus publicaciones equivalentes en Mercado Libre, Falabella y la página web Eliko. | Should | El problema surge precisamente de vender el mismo producto en cuatro canales sin una visión unificada. |
| RF07 | El sistema debe generar reportes de rotación de productos y de cancelaciones de venta por falta de stock. | Should | Permite dimensionar el impacto económico del problema y priorizar las mejoras a implementar. |
| RF08 | El sistema debe registrar el motivo de cada cancelación de venta. | Could | Da trazabilidad al flujo de resolución identificado en el BPMN as-is, cuando el proceso termina con un problema. |
| RF09 | El sistema debe permitir priorizar los productos a reponer según su historial de ventas y su nivel de stock crítico. | Could | Apoya directamente la toma de decisiones de reposición, que es uno de los objetivos del sistema. |
| RF10 | El sistema podría integrarse automáticamente vía API con cada plataforma para sincronizar el stock sin intervención manual. | Won't | Es la solución ideal a largo plazo, pero excede el alcance de esta primera entrega y queda planteada como evolución futura. |

## C.4 Requisitos No Funcionales

| ID | Requisito no funcional | Prioridad | Trazabilidad al problema |
|---|---|---|---|
| RNF01 | El sistema debe estar disponible durante el horario de trabajo del equipo, con un nivel de disponibilidad alto. | Must | El registro de ventas y despacho ocurre a diario, por lo que una caída del sistema reintroduce el riesgo de vender sin conocer el stock real. |
| RNF02 | Registrar un movimiento de stock debe tomar pocos pasos y no requerir capacitación técnica avanzada. | Must | El equipo no tiene un perfil técnico, y la solución debe reemplazar un proceso que hoy es manual y simple. |
| RNF03 | La consulta del stock consolidado debe responder de forma prácticamente inmediata. | Should | El stock se consulta justo en los momentos de mayor operación del negocio. |
| RNF04 | Los datos de clientes y pedidos que maneje el sistema deben protegerse de acuerdo con la Ley 21.719 sobre protección de datos personales. | Must | El sistema procesará información de ventas y pedidos provenientes de los cuatro canales de venta. |
| RNF05 | El sistema debe soportar el volumen actual de publicaciones y su crecimiento, sin que se degrade su rendimiento. | Should | El negocio se encuentra en expansión, y el problema tiende a agravarse si no se anticipa este crecimiento. |
| RNF06 | El sistema debe poder consultarse desde un dispositivo móvil para verificar el stock durante el embalaje en bodega. | Could | La operación ocurre de forma física, en bodega, y no frente a un computador de escritorio de manera permanente. |

---
