import sys

from loader import create_database


def main() -> None:
    database = sys.argv[1] if len(sys.argv) > 1 else None
    create_database(database)


if __name__ == "__main__":
    main()
