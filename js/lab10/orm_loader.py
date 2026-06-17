from collections.abc import Iterator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from db import database_url
from gtfs import COPY_COLUMNS, LOAD_ORDER, batch, normalized_rows
from orm_models import MODEL_BY_TABLE, Base


def create_database_orm(database: str | None = None) -> None:
    engine = orm_engine(database)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def load_gtfs_orm(source: str | Path, database: str | None = None, batch_size: int = 10_000) -> None:
    engine = orm_engine(database)
    source_path = Path(source)
    with Session(engine) as session:
        for table in LOAD_ORDER:
            mappings = mapping_batches(source_path, table, batch_size)
            for table_batch in mappings:
                session.bulk_insert_mappings(MODEL_BY_TABLE[table], table_batch)
                session.commit()


def orm_engine(database: str | None = None) -> Engine:
    url = database_url(database).replace("postgresql://", "postgresql+psycopg://", 1)
    return create_engine(url)


def mapping_batches(source: Path, table: str, batch_size: int) -> Iterator[list[dict[str, object]]]:
    columns = COPY_COLUMNS[table]
    for rows in batch(normalized_rows(source, table), batch_size):
        yield [dict(zip(columns, row, strict=True)) for row in rows]
