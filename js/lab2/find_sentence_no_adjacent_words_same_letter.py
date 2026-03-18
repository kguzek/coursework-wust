from utils import base_parser


def has_no_adjacent_same_letter_words(sentence: str) -> bool:
    """
    Check if no two adjacent words in the sentence start with the same letter.

    Uses only string operations - no lists, tuples, or dicts.
    Words are compared case-insensitively, and only alphabetic starting
    characters are considered.
    """
    if not sentence:
        return False

    in_word = False
    prev_first_char = ""
    current_word_first_char = ""

    for char in sentence:
        if char.isalpha():
            if not in_word:
                # Start of a new word
                current_word_first_char = char.lower()
                if prev_first_char and current_word_first_char == prev_first_char:
                    return False
                prev_first_char = current_word_first_char
                in_word = True
        else:
            # Non-alphabetic character - end of word
            in_word = False

    return True


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
