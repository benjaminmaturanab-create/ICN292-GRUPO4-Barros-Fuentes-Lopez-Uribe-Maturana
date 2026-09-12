# ICN-292 — Propuesta de SIG: Electroliko | LapicaOnline ("Eliko")

**Universidad Técnica Federico Santa María | Campus Vitacura | Paralelo 100**

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

## Estructura del repositorio

```
assets/          # Diagramas exportados (BPMN as-is, to-be, ER)
docs/            # Documentación del proyecto en markdown
  00-caso-pyme.md
  01-requerimientos.md
  02-bpmn.md
  03-er-preliminar.md
informe/         # Informe completo en PDF y LaTeX
README.md        # Este archivo
```

## Relación con la Entrega 2

La Entrega 1 es el diagnóstico y diseño del sistema. La Entrega 2 es 
construirlo y dejarlo funcionando en localhost, con el mismo caso y el 
mismo equipo.

Lo que diseñamos acá se convierte en esto para la E2: los requisitos 
funcionales pasan a ser pantallas reales y consultas SQL; el BPMN to-be 
se conecta a una automatización de procesos; el modelo ER preliminar se 
normaliza y se materializa en una base de datos con datos reales de Eliko; 
y la arquitectura tentativa se implementa para que cualquiera pueda 
levantar el sistema localmente.

El docente debe poder clonar este repositorio, seguir el README y ver 
el sistema funcionando: base de datos consultable, al menos 3 consultas 
de negocio, un tablero KPI alineado al problema de inventario de Eliko, 
y la automatización del proceso to-be documentada.
