-- =============================================================
-- CONSULTAS ANALÍTICAS — Sistema de Inventario Eliko
-- ICN-292 Sistemas de Información para la Gestión — Entrega 2
-- Universidad Técnica Federico Santa María, Campus Vitacura
-- Motor: SQLite 3
--
-- Ejecutar (después de cargar schema.sql y seed.sql):
--   sqlite3 -header -column eliko.db < consultas_analiticas.sql
-- =============================================================


-- -------------------------------------------------------------
-- CONSULTA 1: KPIs generales del inventario
-- Pregunta: ¿cuál es el estado general de la bodega?
-- Alimenta los indicadores del dashboard.
-- -------------------------------------------------------------
SELECT
    (SELECT COUNT(*)          FROM producto)                              AS total_productos,
    (SELECT COUNT(*)          FROM categoria)                             AS total_categorias,
    (SELECT SUM(stock_actual) FROM inventario)                            AS total_unidades,
    (SELECT COUNT(*)          FROM inventario WHERE stock_actual = 0)     AS productos_agotados,
    (SELECT COUNT(*)          FROM inventario WHERE stock_minimo IS NOT NULL) AS productos_con_umbral,
    (SELECT COUNT(*)          FROM movimiento_stock)                      AS total_movimientos;


-- -------------------------------------------------------------
-- CONSULTA 2: Alertas de reposición
-- Pregunta: ¿qué productos están bajo su stock mínimo y cuántas
-- unidades faltan? Ordenada por urgencia (mayor déficit primero).
-- Es la misma consulta que usa el flujo n8n (scripts/alertas_stock.py).
-- -------------------------------------------------------------
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


-- -------------------------------------------------------------
-- CONSULTA 3: Stock y quiebres por categoría
-- Pregunta: ¿qué categorías concentran el inventario y en cuáles
-- hay más productos agotados?
-- -------------------------------------------------------------
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


-- -------------------------------------------------------------
-- CONSULTA 4: Top 10 productos con mayor stock
-- Pregunta: ¿dónde se concentran las unidades en bodega?
-- Útil para no volver a comprar lo que ya sobra.
-- -------------------------------------------------------------
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


-- -------------------------------------------------------------
-- CONSULTA 5: Productos en stock crítico sin umbral configurado
-- Pregunta: ¿a qué productos conviene definirles primero un stock
-- mínimo? Son los que tienen 1 o 2 unidades y que hoy el sistema
-- no puede alertar porque stock_minimo está vacío.
-- -------------------------------------------------------------
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
