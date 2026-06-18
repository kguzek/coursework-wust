from pathlib import Path

from psycopg import Connection, sql

from db import connect, execute_schema
from gtfs import COPY_COLUMNS, LOAD_ORDER, normalized_rows


def create_database(database: str | None = None) -> None:
    with connect(database) as connection:
        execute_schema(connection)


def load_gtfs(source: str | Path, database: str | None = None) -> None:
    source_path = Path(source)
    with connect(database) as connection:
        truncate_loaded_tables(connection)
        for table in LOAD_ORDER:
            copy_table(connection, source_path, table)
        connection.commit()


def truncate_loaded_tables(connection: Connection[tuple[object, ...]]) -> None:
    connection.execute("TRUNCATE agency, route_types, vehicle_types, calendar, stops, routes, trips, stop_times RESTART IDENTITY CASCADE")


def copy_table(connection: Connection[tuple[object, ...]], source: Path, table: str) -> None:
    columns = sql.SQL(", ").join(sql.Identifier(column) for column in COPY_COLUMNS[table])
    statement = sql.SQL("COPY {} ({}) FROM STDIN").format(sql.Identifier(table), columns)
    with connection.cursor() as cursor:
        with cursor.copy(statement) as copy:
            for row in normalized_rows(source, table):
                copy.write_row(row)
