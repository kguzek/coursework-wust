import sys
from typing import Protocol


class ParserCallback(Protocol):
    def __call__(
        self,
        *,
        current_line: str,
        previous_line: str | None,
        current_sentence: str,
        previous_sentence: str | None,
    ) -> bool: ...


def base_parser(
    delimiters: str = ".!?",
    wait_for_sentence: bool = False,
    skip_preamble: bool = False,
    skip_footer: bool = True,
):
    """Implements reading from stdin and can be used as a decorator."""

    def inner(callback: ParserCallback):
        """Calls the callback whenever the parser encounters any character in `delimiters`."""

        previous_line: str | None = None
        current_line: str = ""
        current_line_stripped: str = ""

        previous_sentence: str | None = None
        current_sentence: str = ""
        current_sentence_stripped: str = ""

        line_counter: int = 0
        consecutive_newline_counter: int = 0

        should_continue: bool = True
        preamble_consumed = False

        while should_continue:
            try:
                current_char: str = sys.stdin.read(1)
            except KeyboardInterrupt:
                break

            current_line += current_char
            current_sentence += current_char

            current_line_stripped = current_line.strip()
            current_sentence_stripped = current_sentence.strip()

            if not current_char:
                if (
                    current_sentence_stripped
                    if wait_for_sentence
                    else current_line_stripped
                ):
                    should_continue = callback(
                        current_line=current_line_stripped,
                        previous_line=previous_line,
                        current_sentence=current_sentence_stripped,
                        previous_sentence=previous_sentence,
                    )
                break

            if current_char == "\r":
                continue

            if skip_footer and current_line == "-----":
                break

            if current_char == "\n":
                consecutive_newline_counter += 1
                line_counter += 1
                if not wait_for_sentence:
                    should_continue = callback(
                        current_line=current_line_stripped,
                        previous_line=previous_line,
                        current_sentence=current_sentence_stripped,
                        previous_sentence=previous_sentence,
                    )
                previous_line = current_line_stripped
                current_line = ""
            else:
                consecutive_newline_counter = 0

            is_sentence_end = current_char in delimiters

            if consecutive_newline_counter >= 2:
                is_sentence_end = True

                if consecutive_newline_counter == 3:
                    preamble_consumed = True

            if is_sentence_end:
                if wait_for_sentence and not (skip_preamble and not preamble_consumed):
                    should_continue = callback(
                        current_line=current_line_stripped,
                        previous_line=previous_line,
                        current_sentence=current_sentence_stripped,
                        previous_sentence=previous_sentence,
                    )

                previous_sentence = current_sentence_stripped
                current_sentence = ""

    return inner
