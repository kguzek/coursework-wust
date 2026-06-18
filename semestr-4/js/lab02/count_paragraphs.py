from utils import base_parser


def main():
    count = 0

    @base_parser()
    def count_paragraphs(current_line: str, previous_line: str | None, **_):
        nonlocal count
        if current_line and not previous_line:
            count += 1
        return True

    _ = count_paragraphs
    print(count)


if __name__ == "__main__":
    main()
