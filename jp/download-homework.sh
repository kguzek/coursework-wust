#!/bin/bash
# Copyright © 2025 by Konrad Guzek
# Script for automatically downloading homework assignments
# Japanese A1 (Toyotaka Ota, PhD)
# Department of Foreign Languages
# Wrocław University of Science and Technology

set -e

FILE_URL='https://www.dropbox.com/scl/fi/fyorx8qh7cp9e0svv6gdw/Homework_A1_60b.txt?rlkey=wvhyxk587glavvvgrvjx9fxzh'

for lesson in ./lesson-*; do
  pushd "$lesson" >/dev/null
  if [ ! -f "homework.txt" ]; then
    echo -n "⬇️  Downloading homework for $(basename "$lesson")... "
    curl -fsSLo homework.txt "$FILE_URL" && echo "Done!" && exit 0
  fi
  popd >/dev/null
done

echo "❌ No lesson directories found to download homework into."
exit 1
