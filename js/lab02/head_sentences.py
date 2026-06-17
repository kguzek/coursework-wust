from utils import base_parser


def main(max_sentence_count: int):
    @base_parser(wait_for_sentence=True)
    def head_sentences(current_sentence: str, sentence_counter: int, **_):
        if sentence_counter > max_sentence_count:
            return False
        print(current_sentence)
        return True

    _ = head_sentences


if __name__ == "__main__":
    main(20)
