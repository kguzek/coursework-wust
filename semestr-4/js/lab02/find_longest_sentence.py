from utils import base_parser


def main():
    longest_sentence: str = ""

    @base_parser(wait_for_sentence=True)
    def find_longest_sentence(current_sentence: str, **_):
        nonlocal longest_sentence
        if len(current_sentence) > len(longest_sentence):
            longest_sentence = current_sentence

        return True

    _ = find_longest_sentence

    print(longest_sentence)


if __name__ == "__main__":
    main()
