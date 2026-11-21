# 04 — SQL: schema, seed y consultas de negocio

Motor: **SQLite 3**

| Archivo | Contenido |
|---|---|
| [`../schema.sql`](../schema.sql) | Crea las 4 tablas con PK, FK, CHECK e índices |
| [`../seed.sql`](../seed.sql) | Inserta 17 categorías, 767 productos y sus 767 registros de inventario |
| [`../eliko_db.sql`](../eliko_db.sql) | `schema.sql` + `seed.sql` en un archivo; lo usa `app.py` al iniciar |
| [`../consultas_analiticas.sql`](../consultas_analiticas.sql) | Las 5 consultas de negocio |

Todos los resultados de este documento se obtuvieron ejecutando, en una base recién creada:

```bash
sqlite3 eliko.db < schema.sql
sqlite3 eliko.db < seed.sql
sqlite3 -header -column eliko.db < consultas_analiticas.sql
```

## Consulta 1 — KPIs generales del inventario

```sql
SELECT
    (SELECT COUNT(*)          FROM producto)                              AS total_productos,
    (SELECT COUNT(*)          FROM categoria)                             AS total_categorias,
    (SELECT SUM(stock_actual) FROM inventario)                            AS total_unidades,
    (SELECT COUNT(*)          FROM inventario WHERE stock_actual = 0)     AS productos_agotados,
    (SELECT COUNT(*)          FROM inventario WHERE stock_minimo IS NOT NULL) AS productos_con_umbral,
    (SELECT COUNT(*)          FROM movimiento_stock)                      AS total_movimientos;
```

**Resultado:**

```
total_productos  total_categorias  total_unidades  productos_agotados  productos_con_umbral  total_movimientos
---------------  ----------------  --------------  ------------------  --------------------  -----------------
767              17                8964            308                 2                     0
```

**Interpretación:** La bodega tiene 8.964 unidades, pero **308 de los 767 productos (40%) están en cero**: son publicaciones que no deberían estar activas o que hay que reponer, la situación que causa cancelaciones de venta. Solo 2 productos tienen stock mínimo definido, por lo que el sistema de alertas hoy cubre una parte muy pequeña del catálogo.

## Consulta 2 — Alertas de reposición

```sql
SELECT
    p.sku,
    p.nombre_producto,
    c.nombre_categoria,
    i.stock_actual,
    i.stock_minimo,
    (i.stock_minimo - i.stock_actual) AS unidades_a_reponer
FROM inventario i
JOIN producto  p ON p.sku = i.sku
JOIN categoria c ON c.id_categoria = p.id_categoria
WHERE i.stock_minimo IS NOT NULL
  AND i.stock_actual < i.stock_minimo
ORDER BY unidades_a_reponer DESC;
```

**Resultado:**

```
sku     nombre_producto                                                     nombre_categoria  stock_actual  stock_minimo  unidades_a_reponer
------  ------------------------------------------------------------------  ----------------  ------------  ------------  ------------------
HOG001  Rascador Extensible Acero Inoxidable H2 Negro Manito Colgable 57cm  Hogar y jardín    0             50            50
```

**Interpretación:** De los 2 productos con umbral, uno está bajo su mínimo: HOG001 está agotado y faltan 50 unidades. CAB001 tiene 52 unidades frente a un mínimo de 12, así que no genera alerta. Esta es la consulta que ejecuta el flujo n8n.

## Consulta 3 — Stock y quiebres por categoría

```sql
SELECT
    c.nombre_categoria,
    COUNT(p.sku)                                          AS productos,
    SUM(i.stock_actual)                                   AS unidades,
    ROUND(AVG(i.stock_actual), 1)                         AS promedio_unidades,
    SUM(CASE WHEN i.stock_actual = 0 THEN 1 ELSE 0 END)   AS agotados,
    ROUND(100.0 * SUM(CASE WHEN i.stock_actual = 0 THEN 1 ELSE 0 END)
          / COUNT(p.sku), 1)                              AS pct_agotados
FROM categoria c
JOIN producto   p ON p.id_categoria = c.id_categoria
JOIN inventario i ON i.sku = p.sku
GROUP BY c.id_categoria, c.nombre_categoria
ORDER BY unidades DESC;
```

**Resultado:**

```
nombre_categoria      productos  unidades  promedio_unidades  agotados  pct_agotados
--------------------  ---------  --------  -----------------  --------  ------------
Hogar y jardín        194        2569      13.2               132       68.0
Cables y cargadores   100        1659      16.6               44        44.0
Accesorios celular    48         770       16.0               4         8.3
Deportes y fitness    64         742       11.6               18        28.1
Controles remotos     28         506       18.1               15        53.6
Audífonos             34         394       11.6               0         0.0
Colección y juguetes  29         382       13.2               5         17.2
Mascotas              38         368       9.7                5         13.2
Herramientas          25         348       13.9               13        52.0
Carcasas y fundas     95         306       3.2                28        29.5
Memorias y almacen.   51         266       5.2                35        68.6
Belleza               15         186       12.4               0         0.0
Relojes               22         151       6.9                3         13.6
Equipos satelitales   10         111       11.1               2         20.0
Salud                 4          109       27.3               0         0.0
Computación           8          97        12.1               2         25.0
Intercomunicadores    2          0         0.0                2         100.0
```

**Interpretación:** "Hogar y jardín" es la categoría más grande (194 productos, 2.569 unidades) y también la con más quiebres: 132 productos agotados (68%). Le siguen "Memorias y almacenamiento" (68,6%) y "Controles remotos" (53,6%). "Audífonos", "Belleza" y "Salud" no tienen agotados. El problema no es la falta de unidades en general, sino que están concentradas en pocos productos.

## Consulta 4 — Top 10 productos con mayor stock

```sql
SELECT
    p.sku,
    p.nombre_producto,
    c.nombre_categoria,
    i.stock_actual
FROM inventario i
JOIN producto  p ON p.sku = i.sku
JOIN categoria c ON c.id_categoria = p.id_categoria
ORDER BY i.stock_actual DESC
LIMIT 10;
```

**Resultado:**

```
sku      nombre_producto                                                                            nombre_categoria     stock_actual
-------  -----------------------------------------------------------------------------------------  -------------------  ------------
HOG015   2 Soportes pequeños GYM  De Acero Galvanizado Plateado Kit Doble Acero                     Hogar y jardín       296
HOG010   2 Soportes Para Hamaca De Acero Galvanizado Plateado Kit Doble Acero (kit soporte grande)  Hogar y jardín       278
CAB053   Grampas Rg6 Blancas 100 Unid. Para Cable Coaxial                                           Cables y cargadores  197
CAB016   Kit 100 Bridas Precintos Clip Automotriz Fijación Cables Negro                             Cables y cargadores  196
HOG066   Resorte Acero Inoxidable Para Hamacas, Sillas, Columpios Etc                               Hogar y jardín       192
ACC003   Soporte Clip Para Intercomunicador Ejeas V6pro No Para Tipoc                               Accesorios celular   186
HOG132   Bolsa Para Aspiradora Universal De Tela                                                    Hogar y jardín       159
HOG011   Kit De Soporte Para Silla Colgante, Hamacas Columpios Etc Plateado Kit Hamaca              Hogar y jardín       148
HOG025B  Enchufe Corriente Americano A Nacional Calidad 220v Blanco                                 Hogar y jardín       137
CTR007G  Control Remoto Genérico Para Android Consolas Emuelec Gris                                 Controles remotos    129
```

**Interpretación:** Estos 10 productos suman 1.918 unidades: **el 21% del stock está en el 1,3% de los productos**. Seis son de "Hogar y jardín", la misma categoría con más agotados: conviven productos con exceso y productos en cero. Sirve para no recomprar lo que sobra.

## Consulta 5 — Productos en stock crítico sin umbral configurado

```sql
SELECT
    c.nombre_categoria,
    COUNT(*)                                   AS productos_criticos_sin_umbral,
    SUM(CASE WHEN i.stock_actual = 1 THEN 1 ELSE 0 END) AS con_1_unidad,
    SUM(CASE WHEN i.stock_actual = 2 THEN 1 ELSE 0 END) AS con_2_unidades
FROM inventario i
JOIN producto  p ON p.sku = i.sku
JOIN categoria c ON c.id_categoria = p.id_categoria
WHERE i.stock_minimo IS NULL
  AND i.stock_actual BETWEEN 1 AND 2
GROUP BY c.id_categoria, c.nombre_categoria
ORDER BY productos_criticos_sin_umbral DESC;
```

**Resultado:**

```
nombre_categoria      productos_criticos_sin_umbral  con_1_unidad  con_2_unidades
--------------------  -----------------------------  ------------  --------------
Carcasas y fundas     25                             11            14
Accesorios celular    9                              3             6
Mascotas              7                              4             3
Hogar y jardín        6                              2             4
Audífonos             5                              3             2
Deportes y fitness    5                              1             4
Colección y juguetes  4                              2             2
Equipos satelitales   3                              3             0
Belleza               2                              1             1
Cables y cargadores   2                              1             1
Relojes               2                              1             1
Computación           1                              1             0
Memorias y almacen.   1                              0             1
```

**Interpretación:** Hay **72 productos con 1 o 2 unidades que el sistema no puede alertar** porque no tienen umbral (33 con 1 unidad y 39 con 2). Son los quiebres más probables de las próximas semanas, sobre todo en "Carcasas y fundas" (25). La acción para Eliko es definir primero el stock mínimo de estos productos.
