# ICN-292 — Propuesta de SIG: Electroliko / LapicaOnline ("Eliko")

**Universidad Técnica Federico Santa María — Campus Vitacura — Paralelo 100**

## ¿Qué PYME y qué problema?

Eliko es el nombre comercial de un negocio de e-commerce que opera bajo dos razones sociales: Comercial Electroliko SpA y La PicaOnline SpA. Venden productos importados a través de Mercado Libre (2 cuentas), Falabella y su página web propia, acumulando cerca de 1.400 publicaciones activas y 800 ventas mensuales.

El problema central es que **no tienen inventario**. El stock se controla visualmente en bodega y se actualiza manualmente en cada plataforma cuando quedan menos de 5 unidades. Esto genera entre 3 y 4 cancelaciones mensuales por quiebre de stock, con pérdidas de $100.000 a $300.000 por evento, además de penalizaciones automáticas en Mercado Libre.

## Integrantes

| Nombre | RUT |
|---|---|
| Rodrigo Barros | 202360546-8 |
| Iovanni Fuentes | 202360570-0 |
| Benjamín Maturana | 202304540-3 |
| Alonso López | 202360535-2 |
| Maximiliano Uribe | 202360533-6 |

## Cómo se relaciona con la Entrega 2

La Entrega 1 dejó el **diagnóstico y el diseño** del SIG; la Entrega 2 consiste en **construir y levantar en localhost** esa misma propuesta, manteniendo el mismo caso PYME y el mismo equipo. La relación concreta entre ambas entregas es:

| En la Entrega 1 definimos... | En la Entrega 2 se convierte en... |
|---|---|
| Requisitos funcionales (RF01–RF09, Sección C) | Consultas de negocio y pantallas de la interfaz que implementan cada RF |
| BPMN to-be (Sección D), con el carril "Sistema de gestión SIG" | Automatización de proceso (n8n u homóloga) conectada al flujo real |
| Modelo entidad-relación preliminar (Sección E) | Modelo normalizado a 3FN, materializado en `db/schema.sql` y poblado con `db/seed.sql` |
| Arquitectura lógica y stack tentativo (Sección F) | Implementación reproducible en localhost (contenedores o entorno documentado) |
| Plan de hitos H1–H8 (Sección G) | Cronograma real de desarrollo hacia la Entrega 2 |
| Riesgo de datos personales (Ley 21.719) | Medidas de gobernanza de datos aplicadas y documentadas en `docs/07-etica-ley-21719.md` |

En síntesis, la Entrega 2 debe demostrar —de forma auditable y reproducible por el docente clonando este repositorio— que la propuesta de la Entrega 1 funciona con datos reales: base de datos consultable, al menos 3 consultas de negocio, un tablero de KPI alineado al problema de Eliko, y la automatización del proceso to-be.
