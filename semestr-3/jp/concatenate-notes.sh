#!/bin/sh
# Copyright © 2026 by Konrad Guzek
# Script for concatenating lesson notes text files
# Japanese A1 (Toyotaka Ota, PhD)
# Department of Foreign Languages
# Wrocław University of Science and Technology

set -e

output_directory='concatenated'

if [ -d "$output_directory" ]; then
  if [ "$(ls -A $output_directory)" ]; then
    echo "Directory $output_directory already exists and is not empty, exiting." >&2
    exit 1
  fi
else
  mkdir -p "$output_directory"
fi

for lesson in lesson-*; do 
  output_file="$output_directory/$lesson.md"

  if [ -f "$lesson/notes.md" ]
  then
    cat $lesson/notes.md > $output_file
    echo '\n-----\n' >> $output_file
  fi
  cat $lesson/homework.txt >> $output_file
  echo '\n-----\n\nSolution\n' >> $output_file
  cat $lesson/solution.txt >> $output_file
done

