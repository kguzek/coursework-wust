from utils import base_parser


def main(min_connector_count: int):
    @base_parser(wait_for_sentence=True)
    def filter_compound_sentences(current_sentence: str, **_):
        i_count = current_sentence.count(" i ")
        oraz_count = current_sentence.count(" oraz ")
        ale_count = current_sentence.count(" ale ")
        ze_count = current_sentence.count(" że ")
        lub_count = current_sentence.count(" lub ")

        connector_count = i_count + oraz_count + ale_count + ze_count + lub_count

        if connector_count >= min_connector_count:
            print(current_sentence)

        return True

    _ = filter_compound_sentences


if __name__ == "__main__":
    main(2)
