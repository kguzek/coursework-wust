from utils import base_parser


def contains_proper_noun(sentence: str) -> bool:
    """
    Check if the sentence contains at least one proper noun.
    A proper noun is defined as a word starting with a capital letter,
    not being the first word in the sentence.
    Uses only string operations.
    """
    if not sentence:
        return False

    is_first_word = True
    in_word = False
    found_proper_noun = False

    for char in sentence:
        if char.isalpha():
            if not in_word:
                # Start of a new word
                if not is_first_word and char.isupper():
                    found_proper_noun = True
                is_first_word = False
                in_word = True
        else:
            # Non-alphabetic character - end of word
            in_word = False

    return found_proper_noun


def main():
    total_sentences = 0
    sentences_with_proper_noun = 0

    @base_parser(wait_for_sentence=True, skip_preamble=False)
    def calculate_percentage(current_sentence: str, **_):
        nonlocal total_sentences, sentences_with_proper_noun
        if current_sentence:
            total_sentences += 1
            if contains_proper_noun(current_sentence):
                sentences_with_proper_noun += 1
        return True

    _ = calculate_percentage

    if total_sentences > 0:
        percentage = (sentences_with_proper_noun / total_sentences) * 100
        print(f"{percentage:.2f}%")
    else:
        print("0.00%")


if __name__ == "__main__":
    main()
