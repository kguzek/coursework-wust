from utils import base_parser


def main():
    @base_parser()
    def echo(current_line: str, **_):
        print(current_line)
        return True

    _ = echo


if __name__ == "__main__":
    main()
