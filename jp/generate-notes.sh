#!/bin/bash
# Copyright © 2025 by Konrad Guzek
# Script for automatically downloading homework assignments
# Japanese A1 (Toyotaka Ota, PhD)
# Department of Foreign Languages
# Wrocław University of Science and Technology

set -e

# Find highest existing lesson number
last_lesson=$(ls -d lesson-[0-9]* 2>/dev/null | sed 's/lesson-//' | sort -n | tail -1)

if [ -z "$last_lesson" ]; then
    echo "❌ No existing lesson directories found."
    exit 1
else
    next_lesson=$((last_lesson + 1))
fi

folder="lesson-$next_lesson"

echo "✨ Creating folder: $folder"
mkdir -p "$folder"

lesson_date=$(date +%F)

if [ ! -f notes-template.md ]; then
    echo "❌ Notes template file not found."
    exit 1
fi

cp notes-template.md "$folder/notes.md"

sed -i \
    -e "s/{LESSON_NUMBER}/$next_lesson/g" \
    -e "s/{LESSON_DATE}/$lesson_date/g" \
    "$folder/notes.md"

echo "📁 Lesson folder created: $folder"
echo "📝 Notes file generated with:"
echo "   • Lesson number: $next_lesson"
echo "   • Date: $lesson_date"

