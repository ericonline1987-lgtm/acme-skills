#!/usr/bin/env python3
"""Find load-bearing claims in a Markdown document that carry no source or evidence grade.

A sentence (or table row) is a load-bearing claim when it states a figure
(a percentage, money, a multiplier, a large or decimal number, a count with a
unit such as "17 timeouts" or "300 ms"), an absolute ("always", "never",
"guaranteed", "proven", "zero") or a superlative ("fastest", "best").
Bare small numbers and years are not flagged. It is traced when the same
sentence has any of:

  - a Markdown link or bare URL
  - a footnote or numbered reference: [1], [^note]
  - a source note: (source: ...), (via ...), "according to ..."
  - an evidence grade: [observed], [inferred], [unverified]
  - a marker saying it is not a claim about the world: [target], [goal],
    [estimate], [example]

Code blocks, headings, table header rows, link reference definitions and front
matter are skipped.

What this cannot see: whether a cited source says what the sentence claims,
or claims made without numbers or absolutes. It finds the claims most likely
to be repeated, then leaves judgment to a reader.

Usage:
  claim_check.py FILE.md [--json] [--warn-only]

Exit status: 0 when every flagged claim is traced (or --warn-only), 1 otherwise, 2 unreadable.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FIGURE = re.compile(
    r"(\d+(\.\d+)?\s?%"                    # 12%, 3.5 %
    r"|[$€£¥]\s?\d"                         # $40, € 3
    r"|\b\d+(\.\d+)?\s?(x|×)\b"            # 3x, 2.5×
    r"|\b\d{1,3}(,\d{3})+\b"                # 13,000
    r"|(?<![\d.])\b\d+\.\d+\b(?!\.\d)"      # 70.6 (not v1.0, nor any part of 1.2.3)
    r"|\b\d+\s?(ms|sec|seconds|minutes|hours|k|bn|gb|mb|tb|users|customers|requests|"
    r"times|timeouts|errors|incidents|tickets|orders)\b)",
    re.I,
)
# Words that make a sentence absolute or comparative. Everyday quantifiers
# ("all", "every", "only") are left out on purpose: they are mostly not claims,
# and a checker that flags every plan line gets ignored.
ABSOLUTE = re.compile(
    r"\b(always|never|guaranteed|proven|impossible|zero|"
    r"fastest|slowest|cheapest|best|worst|largest|smallest|leading|unique|"
    r"industry[- ]standard|state[- ]of[- ]the[- ]art)\b",
    re.I,
)
TRACE = re.compile(
    r"(\[[^\]]+\]\([^)]+\)"                         # [text](url)
    r"|https?://\S+"                                 # bare url
    r"|\[\^?[\w-]+\]"                                # [1], [^note], [observed]
    r"|\((source|sources|via|from|per)\s*:?[^)]*\)"  # (source: x)
    r"|\baccording to\b"
    r"|\b(observed|inferred|unverified)\b"
    r"|\[(target|goal|estimate|example)\])",
    re.I,
)
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(\[*])")
LIST_MARKER = re.compile(r"^\s*([-*+]|\d+[.)])\s+")
REF_DEFINITION = re.compile(r"^\s*\[[^\]]+\]:\s+\S+")
FENCE = re.compile(r"^\s*(```|~~~)")


def candidate_units(text: str):
    """Yield (line_number, unit_text) for prose sentences and table rows."""
    in_fence = False
    in_front_matter = False
    lines = text.splitlines()
    separator = re.compile(r"\|?[\s:|-]+\|?")
    for number, raw in enumerate(lines, start=1):
        line = raw.rstrip()
        if number == 1 and line.strip() == "---":
            in_front_matter = True
            continue
        if in_front_matter:
            if line.strip() == "---":
                in_front_matter = False
            continue
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence or not line.strip():
            continue
        stripped = line.strip()
        if stripped.startswith("#") or REF_DEFINITION.match(stripped):
            continue
        if stripped.startswith("|"):
            if separator.fullmatch(stripped):
                continue  # table separator row
            following = lines[number].strip() if number < len(lines) else ""
            if separator.fullmatch(following) and "-" in following:
                continue  # header row: names columns, makes no claim
            yield number, stripped
            continue
        body = LIST_MARKER.sub("", stripped).lstrip("> ").strip()
        for sentence in SENTENCE_END.split(body):
            if sentence.strip():
                yield number, sentence.strip()


def find_untraced(text: str) -> list[dict]:
    findings = []
    for line, unit in candidate_units(text):
        reasons = []
        figure = FIGURE.search(unit)
        if figure:
            reasons.append(f"figure {figure.group(0).strip()!r}")
        absolute = ABSOLUTE.search(unit)
        if absolute:
            reasons.append(f"absolute {absolute.group(0)!r}")
        if reasons and not TRACE.search(unit):
            findings.append({"line": line, "text": unit, "why": ", ".join(reasons)})
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--warn-only", action="store_true", help="always exit 0")
    args = parser.parse_args(argv)

    try:
        text = args.file.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    findings = find_untraced(text)
    if args.json:
        print(json.dumps({"file": str(args.file), "untraced": findings}, indent=2))
    else:
        for f in findings:
            snippet = f["text"] if len(f["text"]) <= 120 else f["text"][:117] + "..."
            print(f"line {f['line']}: {f['why']}\n    {snippet}")
        print(f"\n{len(findings)} untraced load-bearing claim(s). "
              "Add a source or mark it [observed], [inferred] or [unverified]. "
              "Claims without figures or absolutes are not checked.")
    return 0 if (args.warn_only or not findings) else 1


if __name__ == "__main__":
    sys.exit(main())
