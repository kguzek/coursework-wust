from utils import base_parser


def main(min_clause_count: int):
    @base_parser(wait_for_sentence=True)
    def find_first_compound_sentence(current_sentence: str, **_):
        if current_sentence.count(",") >= min_clause_count:
            print(current_sentence)
            return False
        return True

    _ = find_first_compound_sentence


if __name__ == "__main__":
    main(2)
