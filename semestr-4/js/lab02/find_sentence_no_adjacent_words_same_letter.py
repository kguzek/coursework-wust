from utils import base_parser, has_no_adjacent_same_letter_words


def main():
    longest_sentence: str = ""

    @base_parser(wait_for_sentence=True, skip_preamble=False)
    def find_sentence_no_adjacent_same_letter(current_sentence: str, **_):
        nonlocal longest_sentence
        if has_no_adjacent_same_letter_words(current_sentence):
            if len(current_sentence) > len(longest_sentence):
                longest_sentence = current_sentence
        return True

    _ = find_sentence_no_adjacent_same_letter

    print(longest_sentence)


if __name__ == "__main__":
    main()
