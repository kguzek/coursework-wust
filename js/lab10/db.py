import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import psycopg
from psycopg import Connection


def database_url(value: str | None = None) -> str:
    if value is not None:
        return value.replace("postgresql+psycopg://", "postgresql://", 1)
    env = os.environ.get("LAB10_DATABASE_URL")
    if env is None:
        raise RuntimeError("LAB10_DATABASE_URL environment variable is required")
    return env


@contextmanager
def connect(value: str | None = None) -> Iterator[Connection[tuple[object, ...]]]:
    with psycopg.connect(database_url(value)) as connection:
        yield connection


def execute_schema(connection: Connection[tuple[object, ...]]) -> None:
    schema_path = Path(__file__).with_name("schema.sql")
    connection.execute(schema_path.read_text(encoding="utf-8"))
    connection.commit()
