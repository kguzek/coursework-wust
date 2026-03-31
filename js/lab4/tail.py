import sys
import time
import argparse
from typing import List, Optional


def read_lines_from_stdin() -> List[str]:
    lines: List[str] = []
    for line in sys.stdin:
        lines.append(line)
    return lines


def read_lines_from_file(filepath: str) -> List[str]:
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        return f.readlines()


def tail_lines(lines: List[str], n: int) -> List[str]:
    if n <= 0:
        return []
    return lines[-n:] if len(lines) > n else lines


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Display last lines of a file")
    parser.add_argument("file", nargs="?", help="File to read")
    parser.add_argument("--lines", "-n", type=int, default=10, help="Number of lines")
    parser.add_argument(
        "--follow", "-f", action="store_true", help="Follow file updates"
    )
    args = parser.parse_args()

    file_arg: Optional[str] = args.file
    lines_count: int = args.lines
    follow: bool = args.follow

    if file_arg:
        lines = read_lines_from_file(file_arg)
        result = tail_lines(lines, lines_count)
        for line in result:
            sys.stdout.write(line)
        if follow:
            follow_file(file_arg)
    else:
        lines = read_lines_from_stdin()
        result = tail_lines(lines, lines_count)
        for line in result:
            sys.stdout.write(line)


if __name__ == "__main__":
    main()
