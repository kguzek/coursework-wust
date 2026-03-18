from utils import base_parser


def main():

    @base_parser(skip_preamble=True, wait_for_sentence=True)
    def parse_book(current_sentence: str, **_):
        print(current_sentence)
        return True

    _ = parse_book


if __name__ == "__main__":
    main()
