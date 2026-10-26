#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["Markdown==3.10.2", "weasyprint==68.1"]
# ///
"""Run: uv run render_pdf.py LAB (for example, 2 renders lab02/notes.pdf)."""

import argparse
import html
import os
import sys
from pathlib import Path

# Homebrew libraries required by WeasyPrint on macOS.
if sys.platform == "darwin":
    _ = os.environ.setdefault(
        "DYLD_FALLBACK_LIBRARY_PATH", "/opt/homebrew/lib:/usr/local/lib"
    )

import markdown
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent
CSS = """
@page {
    size: A4 landscape;
    margin: 16mm;
    @bottom-center { content: counter(page) " / " counter(pages); font-size: 8pt; }
}
body { font-family: sans-serif; font-size: 9pt; line-height: 1.4; color: #222; }
h1 { font-size: 20pt; }
h2 { font-size: 14pt; margin-top: 20pt; }
h3 { font-size: 11pt; margin-top: 14pt; }
h1, h2, h3, h4 { break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 10pt 0; font-size: 8pt; }
th, td { border: 0.5pt solid #bbb; padding: 5pt; vertical-align: top; overflow-wrap: anywhere; }
th { background: #eee; text-align: left; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
code { font-family: monospace; font-size: 0.9em; overflow-wrap: anywhere; }
pre { white-space: pre-wrap; background: #f5f5f5; padding: 8pt; }
img { max-width: 100%; max-height: 160mm; object-fit: contain; }
a { color: inherit; }
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("lab", type=int, help="lab number (for example, 2 or 02)")
    args = parser.parse_args()
    if args.lab < 1:
        parser.error("lab number must be positive")
    source = ROOT / f"lab{args.lab:02d}" / "notes.md"
    if not source.is_file():
        parser.error(f"notes file not found: {source}")
    destination = source.with_suffix(".pdf")
    body = markdown.markdown(
        source.read_text(encoding="utf8"), extensions=["tables", "fenced_code"]
    )
    document = (
        f'<!doctype html><html lang="pl"><meta charset="utf-8"><title>{html.escape(source.stem)}</title>'
        f"<style>{CSS}</style><body>{body}</body></html>"
    )
    HTML(string=document, base_url=source.parent.as_uri() + "/").write_pdf(destination)
    print(destination)


if __name__ == "__main__":
    main()
