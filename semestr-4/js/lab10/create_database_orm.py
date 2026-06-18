import sys

from orm_loader import create_database_orm


def main() -> None:
    database = sys.argv[1] if len(sys.argv) > 1 else None
    create_database_orm(database)


if __name__ == "__main__":
    main()
