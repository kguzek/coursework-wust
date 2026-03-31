import os
import sys
from typing import List


def get_path_dirs() -> List[str]:
    path_var = os.environ.get("PATH", "")
    return path_var.split(os.pathsep) if path_var else []


def list_path_dirs() -> None:
    dirs = get_path_dirs()
    for directory in dirs:
        print(directory)


def is_executable(filepath: str) -> bool:
    if not os.path.isfile(filepath):
        return False
    if sys.platform == "win32":
        return filepath.lower().endswith((".exe", ".bat", ".cmd"))
    return os.access(filepath, os.X_OK)


def list_path_executables() -> None:
    dirs = get_path_dirs()
    for directory in dirs:
        print(f"\n{directory}:")
        if not os.path.isdir(directory):
            print("  [directory does not exist]")
            continue
        try:
            entries = sorted(os.listdir(directory))
            executables = [
                e for e in entries if is_executable(os.path.join(directory, e))
            ]
            for exe in executables:
                print(f"  {exe}")
        except PermissionError:
            print("  [permission denied]")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: path_browser.py <command>", file=sys.stderr)
        print("Commands: dirs, executables", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    if command == "dirs":
        list_path_dirs()
    elif command == "executables":
        list_path_executables()
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
