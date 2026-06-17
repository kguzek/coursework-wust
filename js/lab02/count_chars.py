from utils import base_parser


def main():
    count = 0

    @base_parser(delimiters="\n ", wait_for_sentence=True)
    def count_chars(current_sentence: str, **_):
        nonlocal count
        count += len(current_sentence)
        return True

    _ = count_chars
    print(count)


if __name__ == "__main__":
    main()
