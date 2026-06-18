from utils import base_parser, has_no_adjacent_same_letter_words


def main():
    @base_parser(wait_for_sentence=True)
    def filter_sentences(current_sentence: str, **_):
        if not current_sentence:
            print(current_sentence)
            return True

        if not has_no_adjacent_same_letter_words(current_sentence):
            return True

        if current_sentence.count(" ") >= 5:
            print(current_sentence)

        return True

    _ = filter_sentences


if __name__ == "__main__":
    main()
