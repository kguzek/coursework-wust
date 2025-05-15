#!/bin/bash
# Copyright © 2025 by Konrad Guzek
# Script for automatic testing of laboratory exercises
# Algorithms and Data Structures (Dariusz Konieczny, PhD)
# Department of Applied Informatics
# Faculty of Information and Communication Technology
# Wrocław University of Science and Technology

if [ "$1" = "clean" ]; then
  if rm -r ./samples-L*/*.*.result 2>/dev/null; then
    echo "🧹 Removed all saved result files"
    exit 0
  else
    echo "⭕  No files were removed"
    exit 1
  fi
fi

EXERCISE=$1;
OUTPUT_DIR="out/production"
SAVE_OUTPUT_ARG='--save-output'

if [ -z "$EXERCISE" ]; then
  read -rp "❓  Exercise number: " EXERCISE
fi

if [ -z "$EXERCISE" ] || ! [[ "$EXERCISE" =~ ^[0-9]+$ ]]; then
    echo "Usage: $0 [exercise number] [-q/--quiet] [-s/$SAVE_OUTPUT_ARG] or $0 clean";
    exit 1;
fi
ZERO_PADDED=$(printf "%02d" "${EXERCISE#0}")
EXERCISE_DIR="dsaa.lab$ZERO_PADDED"

if [ ! -d "$EXERCISE_DIR" ]; then
  echo "Invalid exercise $ZERO_PADDED"
  exit 1;
fi

SAMPLES_DIR="samples-L$ZERO_PADDED"

if [ ! -d "$SAMPLES_DIR" ]; then
  echo "❌  Tests directory $SAMPLES_DIR is missing"
  exit 1
fi

echo "📜 Testing Lab $ZERO_PADDED..."

mkdir -p "$OUTPUT_DIR"
rm -rf "${OUTPUT_DIR:?}/${EXERCISE_DIR:?}"
if ! javac -d "$OUTPUT_DIR" "$EXERCISE_DIR"/*.java; then
  echo "❌  Failed to compile source code"
  exit 1
fi

declare -i FAILED_TESTS=0

TEST_FILES=("./$SAMPLES_DIR"/*.in)
TOTAL_TESTS=${#TEST_FILES[@]}
QUIET_MODE=false
OUTPUT_ON_ERROR=false
for arg in "$@"; do
    if [ "$arg" = "-q" ] || [ "$arg" = "--quiet" ]; then
        QUIET_MODE=true
    fi
    if [ "$arg" = "-s" ] || [ "$arg" = "$SAVE_OUTPUT_ARG" ]; then
        OUTPUT_ON_ERROR=true
    fi
done


VIM_DIFF_AVAILABLE=$(vimdiff --version >/dev/null 2>&1 && echo true || echo false)

for input_file in "${TEST_FILES[@]}"; do
    FILE_WITHOUT_EXTENSION="${input_file%.in}"
    TEST_NUMBER=${FILE_WITHOUT_EXTENSION#./*/}
    echo -n "⌛  Running test $TEST_NUMBER/$TOTAL_TESTS... "
    output=$(java -cp "$OUTPUT_DIR" "$EXERCISE_DIR.Main" < "$input_file" 2>&1)
    APP_EXIT_CODE=$?
    if [ $APP_EXIT_CODE -ne 0 ]; then
      echo "❌  program finished with exit code $APP_EXIT_CODE"
      echo "🐞 Application execution stopped at:"
      echo "$output"
      FAILED_TESTS+=1
      continue
    fi
    EXPECTED_OUTPUT_FILE="$FILE_WITHOUT_EXTENSION.ans"
    if diff --strip-trailing-cr -qy "$EXPECTED_OUTPUT_FILE" <(echo -n "$output") >/dev/null; then
      echo "✔️"
      continue
    fi
    FAILED_TESTS+=1
    MESSAGE="❌  program output"
    if [ -z "$output" ]; then
        echo "$MESSAGE was empty"
        continue
    fi
    if [ $QUIET_MODE = false ]; then
      if $VIM_DIFF_AVAILABLE; then
        vimdiff --not-a-term "$EXPECTED_OUTPUT_FILE" <(echo -n "$output")
      else
        git diff --word-diff --no-index "$EXPECTED_OUTPUT_FILE" <(echo -n "$output")
      fi
    fi
    if [ $OUTPUT_ON_ERROR = false ]; then
      echo "$MESSAGE hidden (use -s/$SAVE_OUTPUT_ARG to save on error)"
      continue
    fi
    OUTPUT_FILE="$FILE_WITHOUT_EXTENSION.$(date '+%Y%m%d%H%M%S%3N').result"
    echo -n "$output" > "$OUTPUT_FILE"
    echo "$MESSAGE written to $OUTPUT_FILE"
done

pluralise() {
  if [ "$1" = "1" ]; then
    echo "$1 $2"
  else
    echo "$1 $2s"
  fi
}

if [ $FAILED_TESTS -eq 0 ]; then
  echo "✔️ All tests passed"
else
  echo "❌  $FAILED_TESTS/$(pluralise "$TOTAL_TESTS" "test") failed"
  exit 1
fi