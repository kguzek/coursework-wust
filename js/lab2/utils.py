import sys
from typing import Protocol


class ParserCallback(Protocol):
    def __call__(
        self, *, current_line: str, previous_line: str | None, row_counter: int
    ) -> bool: ...


def base_parser(delimiter: str = "\n"):
    """Implements reading from stdin and can be used as a decorator."""

    def inner(callback: ParserCallback):
        """Calls the callback whenever the parser encounters `delimiter`."""

        current_line = ""
        current_char = sys.stdin.read(1)

        row_counter = 0
        previous_line: str | None = None

        while current_char:
            current_line += current_char

            stripped = current_line.strip()

            if current_char == delimiter:
                row_counter += 1

                should_continue = callback(
                    current_line=stripped,
                    previous_line=previous_line,
                    row_counter=row_counter,
                )
                if not should_continue:
                    break

                current_line = ""
                previous_line = stripped

            current_char = sys.stdin.read(1)

    return inner
