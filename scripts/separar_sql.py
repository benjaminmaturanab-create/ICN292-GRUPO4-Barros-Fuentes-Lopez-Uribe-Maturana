
import argparse
import sqlite3
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# Sentencias que definen estructura 
PREFIJOS_SCHEMA = (
    "CREATE TABLE", "CREATE INDEX", "CREATE UNIQUE INDEX", "CREATE VIEW",
    "CREATE TRIGGER", "DROP TABLE", "DROP INDEX", "DROP VIEW", "DROP TRIGGER",
    "PRAGMA",
)


def sentencias(texto: str):
    """Separa el script en sentencias completas, respetando ';' dentro de textos."""
    actual = ""
    for linea in texto.splitlines(keepends=True):
        if not actual.strip() and (not linea.strip() or linea.strip().startswith("--")):
            actual = ""
            continue  # línea en blanco o comentario entre sentencias
        actual += linea
        if sqlite3.complete_statement(actual):
            yield actual.strip()
            actual = ""
    if actual.strip():
        yield actual.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--entrada", default=str(RAIZ / "eliko_db.sql"))
    args = parser.parse_args()

    texto = Path(args.entrada).read_text(encoding="utf-8")
    schema, seed, omitidas = [], [], 0
    for s in sentencias(texto):
        cabeza = " ".join(s.upper().split())
        if cabeza.startswith(("SELECT", "WITH")):
            omitidas += 1  # consultas: van en consultas_analiticas.sql, no en el seed
            continue
        (schema if cabeza.startswith(PREFIJOS_SCHEMA) else seed).append(s)

    # Ordenar los INSERT según dependencias de FK (padres antes que hijos),
    # para que el seed también cargue con PRAGMA foreign_keys = ON.
    orden = ["categoria", "producto", "inventario", "movimiento_stock"]
    def prioridad(sentencia: str) -> int:
        cabeza = " ".join(sentencia.split()).lower().replace('"', "")
        for i, tabla in enumerate(orden):
            if cabeza.startswith(f"insert into {tabla} ") or cabeza.startswith(f"insert into {tabla}("):
                return i
        return len(orden)
    seed.sort(key=prioridad)  # sort es estable: conserva el orden dentro de cada tabla

    encabezado_schema = "-- schema.sql — Estructura de la base de datos Eliko (SQLite 3)\n\n"
    encabezado_seed = "-- seed.sql — Datos del inventario levantado en terreno (14/10/2026)\n\n"
    (RAIZ / "schema.sql").write_text(encabezado_schema + "\n\n".join(schema) + "\n", encoding="utf-8")
    (RAIZ / "seed.sql").write_text(encabezado_seed + "\n".join(seed) + "\n", encoding="utf-8")
    print(f"schema.sql: {len(schema)} sentencias | seed.sql: {len(seed)} sentencias | consultas omitidas: {omitidas}")


if __name__ == "__main__":
    main()
