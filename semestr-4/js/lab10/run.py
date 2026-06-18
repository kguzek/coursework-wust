"""Production entrypoint: initialise DB, load GTFS, run uvicorn."""
import logging
import time
from pathlib import Path

import psycopg
import uvicorn
from uvicorn.middleware.wsgi import WSGIMiddleware

from db import connect
from loader import create_database, load_gtfs


def wait_for_db() -> None:
    for _ in range(60):
        try:
            with connect() as conn:
                conn.execute("SELECT 1")
            return
        except psycopg.OperationalError:
            time.sleep(1)
    raise RuntimeError("Could not connect to database after 60 seconds")


def main() -> None:
    wait_for_db()
    create_database()
    gtfs_zip = Path(__file__).with_name("OtwartyWroclaw_rozklad_jazdy_GTFS_28052026.zip")
    if gtfs_zip.exists():
        load_gtfs(gtfs_zip)
    else:
        logging.warning("GTFS zip not found at %s — skipping data load", gtfs_zip)
    from web import create_app  # pylint: disable=import-outside-toplevel
    uvicorn.run(WSGIMiddleware(create_app()), host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
