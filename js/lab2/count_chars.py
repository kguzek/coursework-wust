from utils import base_parser


def main():
    count = 0

    @base_parser(delimiters="\n ")
    def count_chars(current_line: str, **_):
        nonlocal count
        count += len(current_line)
        return True

    _ = count_chars
    print(count)


if __name__ == "__main__":
    main()
