#!/bin/bash
# Copyright © 2025 by Konrad Guzek
# Script for automatic testing of laboratory exercises
# Algorithms and Data Structures (Dariusz Konieczny, PhD)
# Department of Applied Informatics
# Faculty of Information and Communication Technology
# Wrocław University of Science and Technology

EXERCISE=$1;
OUTPUT_DIR="out/production"

if [ -z "$EXERCISE" ] || ! [[ "$EXERCISE" =~ ^[0-9]+$ ]]; then
    echo "Usage: $0 <exercise number>";
    exit 1;
fi
ZERO_PADDED=$(printf "%02d" "$EXERCISE")
EXERCISE_DIR="dsaa.lab$ZERO_PADDED"

if [ ! -d "$EXERCISE_DIR" ]; then
  echo "Invalid exercise $ZERO_PADDED"
  exit 1;
fi

SAMPLES_DIR="samples-L$ZERO_PADDED"

if [ ! -d "$SAMPLES_DIR" ]; then
  echo "Tests directory $SAMPLES_DIR is missing"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"
rm -rf "${OUTPUT_DIR:?}/${EXERCISE_DIR:?}"
javac -d "$OUTPUT_DIR" "$EXERCISE_DIR"/*.java

declare -i FAILED_TESTS=0

TEST_FILES=("./$SAMPLES_DIR"/*.in)
TOTAL_TESTS=${#TEST_FILES[@]}


VIM_DIFF_AVAILABLE=$(vimdiff --version >/dev/null 2>&1 && echo true || echo false)

for input_file in "${TEST_FILES[@]}"; do
    FILE_WITHOUT_EXTENSION="${input_file%.in}"
    TEST_NUMBER=${FILE_WITHOUT_EXTENSION#./*/}
    echo "Running test $TEST_NUMBER/$TOTAL_TESTS..."
    output=$(java -cp "$OUTPUT_DIR" "$EXERCISE_DIR.Main" < "$input_file")
    APP_EXIT_CODE=$?
    if [ $APP_EXIT_CODE -ne 0 ]; then
      echo "🐞  Application execution stopped at:"
      echo "$output"
      echo "❌  Test $TEST_NUMBER failed; program finished with exit code $APP_EXIT_CODE"
      FAILED_TESTS+=1
      continue
    fi
    EXPECTED_OUTPUT_FILE="$FILE_WITHOUT_EXTENSION.ans"
    if diff --strip-trailing-cr -qy "$EXPECTED_OUTPUT_FILE" <(echo "$output") >/dev/null; then
      echo "✔️ Test $TEST_NUMBER passed"
      continue
    fi
    MESSAGE="❌  Test $TEST_NUMBER failed; program output"
    if [ -z "$output" ]; then
        echo "$MESSAGE was empty"
    else
      OUTPUT_FILE="$FILE_WITHOUT_EXTENSION.$(date '+%Y%m%d%H%M%S%3N').result"
      echo "$output" > "$OUTPUT_FILE"
      echo "$MESSAGE written to $OUTPUT_FILE"
      if $VIM_DIFF_AVAILABLE; then
        vimdiff --not-a-term -c "set diffopt+=iwhite" "$EXPECTED_OUTPUT_FILE" "$OUTPUT_FILE"
      else
        git diff --word-diff --no-index "$EXPECTED_OUTPUT_FILE" "$OUTPUT_FILE"
      fi
    fi
    FAILED_TESTS+=1
done

pluralise() {
  if [ "$1" == "1" ]; then
    echo "$1$2"
  else
    echo "$1$2s"
  fi
}

if [ $FAILED_TESTS -eq 0 ]; then
  echo "✔️ All tests passed"
else
  echo "❌  $(pluralise $FAILED_TESTS "/$TOTAL_TESTS test") failed"
  exit 1
fi
