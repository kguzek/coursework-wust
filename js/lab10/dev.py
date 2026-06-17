import os

from web import create_app


def main() -> None:
    _ = os.environ.setdefault(
        "LAB10_DATABASE_URL", "postgresql://lab10:lab10@localhost:55432/lab10"
    )
    create_app().run(host="0.0.0.0", port=8000, debug=True)


if __name__ == "__main__":
    main()
