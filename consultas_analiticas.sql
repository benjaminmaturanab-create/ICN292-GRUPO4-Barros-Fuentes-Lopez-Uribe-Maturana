-- =============================================================
-- CONSULTAS ANALÍTICAS — Sistema de Inventario Eliko Bodega
-- ICN-292 Sistemas de Información para la Gestión
-- Universidad Técnica Federico Santa María, Campus Vitacura
-- Segundo Semestre 2026
-- =============================================================


-- -------------------------------------------------------------
-- CONSULTA 1: KPI — Total de productos, unidades y categorías
-- Propósito: Obtener los indicadores macro del inventario.
-- Esta query alimenta directamente los KPIs del dashboard.
-- COUNT(DISTINCT id_categoria) evita contar categorías duplicadas.
-- Resultado esperado: 767 productos | 8964 unidades | 17 categorías
-- -------------------------------------------------------------
SELECT
    COUNT(*)                      AS total_productos,
    SUM(stock_actual)             AS total_unidades,
    COUNT(DISTINCT id_categoria)  AS total_categorias
FROM producto;


-- -------------------------------------------------------------
-- CONSULTA 2: Alertas de reposición activas
-- Propósito: Identificar productos bajo umbral mínimo de stock.
-- La columna "deficit" cuantifica unidades faltantes para normalizar.
-- ORDER BY deficit DESC presenta primero los casos más críticos.
-- -------------------------------------------------------------
SELECT
    p.codigo,
    p.nombre,
    p.stock_actual,
    p.stock_minimo,
    (p.stock_minimo - p.stock_actual) AS deficit
FROM producto p
WHERE p.stock_actual < p.stock_minimo
ORDER BY deficit DESC;


-- -------------------------------------------------------------
-- CONSULTA 3: Resumen de stock por categoría
-- Propósito: Análisis consolidado por categoría para decisiones
-- de abastecimiento. LEFT JOIN garantiza que aparezcan categorías
-- sin productos. AVG/MIN/MAX detectan desequilibrios internos.
-- -------------------------------------------------------------
SELECT
    c.nombre                        AS categoria,
    COUNT(p.id_producto)            AS cantidad_productos,
    SUM(p.stock_actual)             AS total_unidades,
    ROUND(AVG(p.stock_actual), 1)   AS promedio_stock,
    MIN(p.stock_actual)             AS stock_minimo_registrado,
    MAX(p.stock_actual)             AS stock_maximo_registrado
FROM categoria c
LEFT JOIN producto p ON c.id_categoria = p.id_categoria
GROUP BY c.id_categoria, c.nombre
ORDER BY total_unidades DESC;


-- -------------------------------------------------------------
-- CONSULTA 4: Productos sin movimiento registrado
-- Propósito: Detectar productos sin actividad en el sistema.
-- Candidatos a revisión: descontinuados, mal codificados o
-- de demanda nula. ORDER BY stock_actual DESC prioriza productos
-- inmovilizados con mayor capital invertido.
-- -------------------------------------------------------------
SELECT
    p.codigo,
    p.nombre,
    c.nombre        AS categoria,
    p.stock_actual
FROM producto p
JOIN categoria c ON p.id_categoria = c.id_categoria
WHERE p.id_producto NOT IN (
    SELECT DISTINCT id_producto
    FROM movimiento_stock
)
ORDER BY p.stock_actual DESC;


-- -------------------------------------------------------------
-- CONSULTA 5: Valor del inventario y margen potencial por categoría
-- Propósito: Business intelligence estratégico. Responde cuánto
-- capital está invertido por categoría y cuál es el margen potencial.
-- Transforma datos operativos en información para toma de decisiones.
-- -------------------------------------------------------------
SELECT
    c.nombre                                                AS categoria,
    COUNT(p.id_producto)                                    AS productos,
    SUM(p.stock_actual * p.precio_costo)                    AS valor_inventario_costo,
    SUM(p.stock_actual * p.precio_venta)                    AS valor_inventario_venta,
    SUM(p.stock_actual * (p.precio_venta - p.precio_costo)) AS margen_potencial
FROM categoria c
JOIN producto p ON c.id_categoria = p.id_categoria
GROUP BY c.id_categoria, c.nombre
ORDER BY valor_inventario_venta DESC;
