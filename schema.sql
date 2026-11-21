-- schema.sql — Estructura de la base de datos Eliko (SQLite 3)

CREATE TABLE IF NOT EXISTS categoria (
    id_categoria     INTEGER      PRIMARY KEY AUTOINCREMENT,
    nombre_categoria VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS producto (
    sku             VARCHAR(20)  PRIMARY KEY,
    nombre_producto VARCHAR(255) NOT NULL,
    id_categoria    INTEGER      NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria)
);

CREATE TABLE IF NOT EXISTS inventario (
    id_registro         INTEGER      PRIMARY KEY AUTOINCREMENT,
    sku                 VARCHAR(20)  NOT NULL UNIQUE,
    stock_actual        INTEGER      NOT NULL DEFAULT 0,
    stock_minimo        INTEGER      DEFAULT NULL,
    fecha_actualizacion DATETIME     DEFAULT CURRENT_TIMESTAMP,
    comentario          TEXT         DEFAULT NULL,
    FOREIGN KEY (sku) REFERENCES producto(sku)
);

CREATE TABLE IF NOT EXISTS movimiento_stock (
    id_movimiento    INTEGER     PRIMARY KEY AUTOINCREMENT,
    sku              VARCHAR(20) NOT NULL,
    tipo_movimiento  VARCHAR(10) NOT NULL CHECK (tipo_movimiento IN ('ENTRADA','SALIDA','AJUSTE')),
    cantidad         INTEGER     NOT NULL CHECK (cantidad > 0),
    fecha_movimiento DATETIME    DEFAULT CURRENT_TIMESTAMP,
    motivo           TEXT        DEFAULT NULL,
    FOREIGN KEY (sku) REFERENCES producto(sku)
);

CREATE INDEX IF NOT EXISTS idx_producto_categoria ON producto(id_categoria);

CREATE INDEX IF NOT EXISTS idx_movimiento_sku     ON movimiento_stock(sku);

CREATE INDEX IF NOT EXISTS idx_movimiento_fecha   ON movimiento_stock(fecha_movimiento);
