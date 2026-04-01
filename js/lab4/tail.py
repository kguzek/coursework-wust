import argparse
import os
import sys
import time
from typing import List, Optional

TAIL_REVERSE_ENV_VAR = "TAIL_REVERSE"
TAIL_MODE_ENV_VAR = "TAIL_MODE"


def read_lines_from_stdin() -> List[str]:
    lines: List[str] = []
    for line in sys.stdin:
        lines.append(line)
    return lines


def read_lines_from_file(filepath: str) -> List[str]:
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        return f.readlines()


def tail_generic[T](content: T, n: int, reverse: bool, default: T) -> T:
    if n <= 0:
        return default
    if len(content) <= n:
        return content
    return content[-1 : -n - 1 : -1] if reverse else content[-n:]


def tail_content(
    lines: List[str], n: int, reverse: bool, line_mode: bool
) -> List[str] | str:
    (content, default) = (lines, []) if line_mode else ("\n".join(lines), "")
    result = tail_generic(content, n, reverse, default)
    return result if line_mode else [result]


def tail_chars(chars: str, n: int, reverse: bool) -> str:
    return tail_generic(chars, n, reverse, "")


def follow_file(filepath: str) -> None:
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if line:
                sys.stdout.write(line)
                sys.stdout.flush()
            else:
                time.sleep(0.1)


def parse_reverse_var() -> bool:
    tail_reverse_var = os.environ.get(TAIL_REVERSE_ENV_VAR, None)
    if tail_reverse_var is not None:
        if tail_reverse_var == "1":
            return True
        print(
            f"Unknown value for {TAIL_REVERSE_ENV_VAR}: '{tail_reverse_var}'",
            file=sys.stderr,
        )
    return False


def parse_line_mode_var() -> bool:
    parse_mode_var = os.environ.get(TAIL_MODE_ENV_VAR, None)
    if parse_mode_var == "chars":
        return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Display last lines of a file")
    parser.add_argument("file", nargs="?", help="File to read")
    parser.add_argument("--lines", "-n", type=int, default=10, help="Number of lines")
    parser.add_argument(
        "--follow", "-f", action="store_true", help="Follow file updates"
    )
    args = parser.parse_args()

    file_arg: Optional = args.file
    lines_count: int = args.lines
    follow: bool = args.follow
    reverse: bool = parse_reverse_var()
    line_mode: bool = parse_line_mode_var()

    if file_arg:
        lines = read_lines_from_file(file_arg)
        result = tail_content(lines, lines_count, reverse, line_mode)
        for line in result:
            sys.stdout.write(line)
        if follow:
            follow_file(file_arg)
    else:
        lines = read_lines_from_stdin()
        result = tail_content(lines, lines_count, reverse, line_mode)
        for line in result:
            sys.stdout.write(line)


if __name__ == "__main__":
    main()
