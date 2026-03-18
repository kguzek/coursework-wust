import sys
from typing import Protocol


class ParserCallback(Protocol):
    def __call__(
        self, *, current_line: str, previous_line: str | None, row_counter: int
    ) -> bool: ...


def base_parser(delimiters: str = ".!?"):
    """Implements reading from stdin and can be used as a decorator."""

    def inner(callback: ParserCallback):
        """Calls the callback whenever the parser encounters any character in `delimiters`."""

        current_line: str = ""
        stripped: str = ""

        row_counter: int = 0
        previous_line: str | None = None
        previous_char: str = ""
        should_continue: bool = True

        while should_continue:
            current_char: str = sys.stdin.read(1)
            if not current_char:
                if stripped:
                    row_counter += 1
                    should_continue = callback(
                        current_line=current_line,
                        previous_line=previous_line,
                        row_counter=row_counter,
                    )
                break

            is_new_paragraph = current_char == "\n" and previous_char == "\n"
            is_duplicate_space = current_char == " " and current_line.endswith(" ")

            if not (is_new_paragraph or is_duplicate_space):
                current_line += current_char

            stripped = current_line.strip()

            if (is_new_paragraph and stripped) or current_char in delimiters:
                row_counter += 1

                should_continue = callback(
                    current_line=current_line,
                    previous_line=previous_line,
                    row_counter=row_counter,
                )

                previous_line = stripped
                current_line = ""

            if is_new_paragraph:
                row_counter += 1
                should_continue = should_continue and callback(
                    current_line="",
                    previous_line=stripped,
                    row_counter=row_counter,
                )
                previous_line = current_char
                current_line = ""

            previous_char = current_char

    return inner
