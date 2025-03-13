#!/bin/bash

EXERCISE=$1;

if [ -z "$EXERCISE" ] || ! [[ "$EXERCISE" =~ ^[0-9]+$ ]]; then
    echo "Usage: $0 <exercise number>";
    exit 1;
fi
ZERO_PADDED=$(printf "%02d" "$EXERCISE")
EXERCISE_DIR="dsaa.lab$ZERO_PADDED"
SAMPLES_DIR="samples-L$ZERO_PADDED"
javac "$EXERCISE_DIR"/*.java

EXIT_CODE=0

TEST_FILES=("./$SAMPLES_DIR"/*.in)
TOTAL_TESTS=${#TEST_FILES[@]}

for input_file in "${TEST_FILES[@]}"; do
    FILE_WITHOUT_EXTENSION="${input_file%.in}"
    TEST_NUMBER=${FILE_WITHOUT_EXTENSION#./*/}
    echo "Running test $TEST_NUMBER/$TOTAL_TESTS"
    output=$(java -cp "$EXERCISE_DIR" Main < "$input_file")
    OUTPUT_FILE="$FILE_WITHOUT_EXTENSION.ans"
    EXPECTED_OUTPUT=$(cat "$OUTPUT_FILE")
    if [ "$output" == "$EXPECTED_OUTPUT" ]; then
      echo "Test $TEST_NUMBER passed"
      continue
    fi
    MESSAGE="Test $TEST_NUMBER failed; program output"
    if [ -z "$output" ]; then
        echo "$MESSAGE was empty"
    else
      OUTPUT_FILE="$FILE_WITHOUT_EXTENSION.$(date '+%Y%m%d%H%M%S%3N').result"
      echo "$output" > "$OUTPUT_FILE"
      echo "$MESSAGE written to $OUTPUT_FILE"
    fi
    EXIT_CODE=1
done

exit $EXIT_CODE
