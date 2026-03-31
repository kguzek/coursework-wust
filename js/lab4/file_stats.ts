import { readFileSync } from "node:fs";

interface FileStats {
  path: string;
  chars: number;
  words: number;
  lines: number;
  most_common_char: string;
  most_common_word: string;
}

function analyzeFile(filePath: string): FileStats {
  const content: string = readFileSync(filePath, "utf-8");
  const chars = content.length;
  const lines = content.split("\n");
  const lineCount = lines.length;

  const words: string[] = [];
  for (const line of lines) {
    words.push(...line.split(/\s+/).filter((w) => w.length > 0));
  }
  const wordCount = words.length;

  const charCounts = new Map<string, number>();
  for (const char of content) {
    if (!/\s/.test(char)) {
      charCounts.set(char, (charCounts.get(char) ?? 0) + 1);
    }
  }
  let mostCommonChar = "";
  let maxCharCount = 0;
  for (const [char, count] of charCounts) {
    if (count > maxCharCount) {
      maxCharCount = count;
      mostCommonChar = char;
    }
  }

  const wordCounts = new Map<string, number>();
  for (const word of words) {
    const lower = word.toLowerCase();
    wordCounts.set(lower, (wordCounts.get(lower) ?? 0) + 1);
  }
  let mostCommonWord = "";
  let maxWordCount = 0;
  for (const [word, count] of wordCounts) {
    if (count > maxWordCount) {
      maxWordCount = count;
      mostCommonWord = word;
    }
  }

  return {
    path: filePath,
    chars,
    words: wordCount,
    lines: lineCount,
    most_common_char: mostCommonChar,
    most_common_word: mostCommonWord,
  };
}

function formatOutput(stats: FileStats, formatType: string): string {
  if (formatType === "json") {
    return JSON.stringify(stats);
  }

  const keys = Object.keys(stats);
  const values = Object.values(stats);

  if (formatType === "csv") {
    return `${keys.join(",")}\n${values.join(",")}`;
  }

  if (formatType === "tsv") {
    return `${keys.join("\t")}\n${values.join("\t")}`;
  }

  return JSON.stringify(stats);
}

function main(): void {
  const args = process.argv.slice(2);
  let formatType = "json";
  const filePaths: string[] = [];

  for (const arg of args) {
    if (arg.startsWith("--format=")) {
      formatType = arg.split("=")[1];
    } else if (!arg.startsWith("--")) {
      filePaths.push(arg);
    }
  }

  if (filePaths.length === 0) {
    const filePath = readFileSync(0, "utf-8").trim();
    const stats = analyzeFile(filePath);
    console.log(formatOutput(stats, formatType));
  } else {
    for (const filePath of filePaths) {
      const stats = analyzeFile(filePath);
      console.log(formatOutput(stats, formatType));
    }
  }
}

main();

