from utils import base_parser


def main(sentence_length: int):
    @base_parser(wait_for_sentence=True)
    def filter_long_sentences(current_sentence: str, **_):
        if not current_sentence:
            print(current_sentence)
            return True
        if current_sentence.count(" ") >= sentence_length:
            print(current_sentence)
        return True

    _ = filter_long_sentences


if __name__ == "__main__":
    main(4)
