import sys


def main():
    current_line = ""
    current_char = sys.stdin.read(1)

    line_counter = 0
    preamble_consumed = False
    last_was_newline = False

    while current_char:
        current_line += current_char

        stripped = current_line.strip()

        if stripped == "-----":
            break

        if current_char == "\n":
            line_counter += 1
            is_newline = stripped == ""
            current_line = ""
            if last_was_newline and is_newline:
                preamble_consumed = True
            else:
                if preamble_consumed:
                    print(stripped)
                elif line_counter >= 10:
                    preamble_consumed = True
            last_was_newline = is_newline

        current_char = sys.stdin.read(1)


if __name__ == "__main__":
    main()
