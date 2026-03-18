from utils import base_parser


def main():
    preamble_consumed = False

    @base_parser()
    def parse_book_content(
        current_line: str, previous_line: str | None, row_counter: int
    ) -> bool:
        nonlocal preamble_consumed

        if current_line == "-----":
            return False

        if current_line == "" and previous_line == "":
            preamble_consumed = True
        else:
            if preamble_consumed:
                print(current_line)
            elif row_counter >= 10:
                preamble_consumed = True
        return True

    _ = parse_book_content


if __name__ == "__main__":
    main()
