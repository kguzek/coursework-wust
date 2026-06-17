from collections.abc import Iterator
from contextlib import contextmanager
import os
from pathlib import Path

import psycopg
from psycopg import Connection


DEFAULT_DATABASE_URL = "postgresql://lab10:lab10@localhost:55432/lab10"


def database_url(value: str | None = None) -> str:
    if value and value.startswith(("postgresql://", "postgresql+psycopg://")):
        return value.replace("postgresql+psycopg://", "postgresql://", 1)
    if value:
        return f"postgresql://lab10:lab10@localhost:55432/{value}"
    return os.environ.get("LAB10_DATABASE_URL", DEFAULT_DATABASE_URL)


@contextmanager
def connect(value: str | None = None) -> Iterator[Connection[tuple[object, ...]]]:
    with psycopg.connect(database_url(value)) as connection:
        yield connection


def execute_schema(connection: Connection[tuple[object, ...]]) -> None:
    schema_path = Path(__file__).with_name("schema.sql")
    connection.execute(schema_path.read_text(encoding="utf-8"))
    connection.commit()
