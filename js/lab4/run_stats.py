import os
import sys
import subprocess
import json
from collections import Counter
from typing import List, Any


def run_file_stats(directory: str, format_type: str = "json") -> List[dict[str, Any]]:
    results: List[dict[str, Any]] = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ts_script = os.path.join(script_dir, "file_stats.ts")
    for entry in os.scandir(directory):
        if entry.is_file():
            try:
                result = subprocess.run(
                    ["node", ts_script, "--format=" + format_type, entry.path],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                stats = json.loads(result.stdout.strip())
                results.append(stats)
            except (subprocess.CalledProcessError, json.JSONDecodeError):
                continue
    return results


def aggregate_stats(results: List[dict[str, Any]]) -> dict[str, Any]:
    if not results:
        return {}

    total_files = len(results)
    total_chars = sum(r["chars"] for r in results)
    total_words = sum(r["words"] for r in results)
    total_lines = sum(r["lines"] for r in results)

    char_counter = Counter(
        r["most_common_char"] for r in results if r["most_common_char"]
    )
    word_counter = Counter(
        r["most_common_word"] for r in results if r["most_common_word"]
    )

    most_common_char = char_counter.most_common(1)[0][0] if char_counter else ""
    most_common_word = word_counter.most_common(1)[0][0] if word_counter else ""

    return {
        "files_count": total_files,
        "total_chars": total_chars,
        "total_words": total_words,
        "total_lines": total_lines,
        "most_common_char": most_common_char,
        "most_common_word": most_common_word,
    }


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: run_stats.py <directory>", file=sys.stderr)
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Not a directory: {directory}", file=sys.stderr)
        sys.exit(1)

    results = run_file_stats(directory)
    aggregated = aggregate_stats(results)
    print(json.dumps(aggregated, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
