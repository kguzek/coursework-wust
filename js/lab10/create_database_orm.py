import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lab10.orm_loader import create_database_orm  # pylint: disable=wrong-import-position


def main() -> None:
    database = sys.argv[1] if len(sys.argv) > 1 else None
    create_database_orm(database)


if __name__ == "__main__":
    main()
