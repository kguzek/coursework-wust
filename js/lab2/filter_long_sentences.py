from utils import base_parser


def main(sentence_length: int):
    @base_parser(wait_for_sentence=True)
    def filter_long_sentences(current_sentence: str, **_):
        if len(current_sentence.split(" ")) > sentence_length:
            print(current_sentence)
        return True

    _ = filter_long_sentences


if __name__ == "__main__":
    main(4)
