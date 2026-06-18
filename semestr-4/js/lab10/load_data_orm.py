import sys

from orm_loader import load_gtfs_orm


def main() -> None:
    if len(sys.argv) not in {2, 3}:
        raise SystemExit("usage: python load_data_orm.py GTFS_SOURCE [DATABASE_OR_URL]")
    database = sys.argv[2] if len(sys.argv) == 3 else None
    load_gtfs_orm(sys.argv[1], database)


if __name__ == "__main__":
    main()
