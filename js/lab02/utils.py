# pylint: disable=too-many-arguments, too-many-branches, too-many-statements
import sys
from typing import Protocol

PREAMBLE_MAX_LINE_COUNT: int = 10


class ParserCallback(Protocol):
    def __call__(
        self,
        *,
        current_line: str,
        previous_line: str | None,
        current_sentence: str,
        previous_sentence: str | None,
        line_counter: int,
        sentence_counter: int,
    ) -> bool: ...


def base_parser(
    delimiters: str = ".!?",
    wait_for_sentence: bool = False,
    skip_preamble: bool = True,
    skip_footer: bool = True,
):
    """Implements reading from stdin and can be used as a decorator."""

    def inner(callback: ParserCallback):
        """Calls the callback whenever the parser encounters any character in `delimiters`."""

        previous_line: str | None = None
        current_line: str = ""
        current_line_stripped: str = ""
        line_counter: int = 0

        previous_sentence: str | None = None
        current_sentence: str = ""
        current_sentence_stripped: str = ""
        sentence_counter: int = 0

        consecutive_newline_counter: int = 0

        should_continue: bool = True
        preamble_consumed = False

        while should_continue:
            try:
                current_char: str = sys.stdin.read(1)
            except KeyboardInterrupt:
                break

            if current_char == "\r":
                continue

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
                        line_counter=line_counter,
                        sentence_counter=sentence_counter,
                    )
                break

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
                        line_counter=line_counter,
                        sentence_counter=sentence_counter,
                    )
                previous_line = current_line_stripped
                current_line = ""
                if line_counter > PREAMBLE_MAX_LINE_COUNT:
                    preamble_consumed = True
            else:
                consecutive_newline_counter = 0

            is_sentence_end = current_char in delimiters

            if consecutive_newline_counter >= 2:
                is_sentence_end = True

                if consecutive_newline_counter == 3 and not preamble_consumed:
                    preamble_consumed = True
                    if skip_preamble:
                        sentence_counter = 0
                        is_sentence_end = False

            if is_sentence_end:
                if current_sentence_stripped:
                    sentence_counter += 1
                if wait_for_sentence and not (skip_preamble and not preamble_consumed):
                    should_continue = callback(
                        current_line=current_line_stripped,
                        previous_line=previous_line,
                        current_sentence=current_sentence_stripped,
                        previous_sentence=previous_sentence,
                        line_counter=line_counter,
                        sentence_counter=sentence_counter,
                    )

                previous_sentence = current_sentence_stripped
                current_sentence = ""

    return inner


def has_no_adjacent_same_letter_words(sentence: str) -> bool:
    if not sentence:
        return False

    in_word = False
    prev_first_char = ""
    current_word_first_char = ""

    for char in sentence:
        if char.isalpha():
            if not in_word:
                current_word_first_char = char.lower()
                if prev_first_char and current_word_first_char == prev_first_char:
                    return False
                prev_first_char = current_word_first_char
                in_word = True
        else:
            in_word = False

    return True
