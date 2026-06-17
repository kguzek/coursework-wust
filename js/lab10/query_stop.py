import sys

from cli import main as cli_main


def main() -> None:
    database = sys.argv[1] if len(sys.argv) > 1 else None
    arguments = ["query"] if database is None else ["query", database]
    raise SystemExit(cli_main(arguments))


if __name__ == "__main__":
    main()
