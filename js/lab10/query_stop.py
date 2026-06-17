import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lab10.cli import main as cli_main  # pylint: disable=wrong-import-position


def main() -> None:
    database = sys.argv[1] if len(sys.argv) > 1 else None
    arguments = ["query"] if database is None else ["query", database]
    raise SystemExit(cli_main(arguments))


if __name__ == "__main__":
    main()
