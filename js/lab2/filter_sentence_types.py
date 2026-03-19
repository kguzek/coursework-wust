from utils import base_parser


def main(sentence_types: str):
    @base_parser(wait_for_sentence=True)
    def filter_sentence_types(current_sentence: str, **_):
        if not current_sentence:
            print(current_sentence)
            return True
        if current_sentence[-1] in sentence_types:
            print(current_sentence)
        return True

    _ = filter_sentence_types


if __name__ == "__main__":
    main("?!")
