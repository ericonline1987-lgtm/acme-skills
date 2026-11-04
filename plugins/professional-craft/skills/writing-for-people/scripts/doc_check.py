#!/usr/bin/env python3
"""Count reader-level defects in a Markdown document before it goes out.

Checks, each reported with line numbers:

  over budget        main-path words (everything before an "Appendix" heading) above --budget
  slow opening       the first prose sentence talks about the document instead of the point
                     ("This document...", "The purpose of...", "Background")
  meta-commentary    phrases that narrate the text ("as mentioned above", "it is worth noting")
  long sentences     more than --max-sentence words
  label headings     headings that name a bucket instead of summarising ("Overview", "Details")
  heavy hedging      more than 2 hedge words ("might", "perhaps", "somewhat") per 100 words
  bold overuse       more than 1 bold span per 60 words
  open placeholders  TODO, TBD, <placeholder>, [fill in] left in the text

Code blocks, front matter and tables are excluded from sentence checks.

What this cannot see: whether the document answers its reader's question, is true, or
is well organised. Zero defects means none of these mechanical problems, nothing more.
A person or a fresh agent reading for the reader's job is still the real test.

Usage:
  doc_check.py FILE.md [--budget 500] [--max-sentence 35] [--json] [--warn-only]

Exit status: 0 no defects (or --warn-only), 1 defects found, 2 unreadable.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FENCE = re.compile(r"^\s*(```|~~~)")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
APPENDIX = re.compile(r"^#{1,6}\s+(appendix|annex)\b", re.I)
SLOW_OPENING = re.compile(
    r"^(this (document|report|memo|page|doc|proposal|update)|the purpose of|in this (document|report|memo)|"
    r"background\b|introduction\b|overview\b|i am writing|we are writing|as requested)", re.I)
META = re.compile(
    r"\b(as (mentioned|noted|stated|discussed) (above|below|earlier|previously)|it is worth noting|"
    r"it should be noted|needless to say|in this section|the following section|in conclusion|"
    r"to summari[sz]e|as you can see|it goes without saying|let'?s dive in)\b", re.I)
LABEL_HEADINGS = {"overview", "background", "introduction", "details", "miscellaneous", "misc",
                  "other", "notes", "summary", "discussion", "general", "context"}
HEDGES = re.compile(r"\b(might|perhaps|possibly|somewhat|fairly|quite|relatively|arguably|"
                    r"seemingly|potentially|kind of|sort of)\b", re.I)
BOLD = re.compile(r"\*\*[^*\n]+\*\*|__[^_\n]+__")
INLINE_CODE = re.compile(r"`[^`\n]*`")
PLACEHOLDER = re.compile(r"\bTODO\b|\bTBD\b|\[fill in[^\]]*\]|<(?!/?(?:a|b|i|br|em|strong|code|kbd|sub|sup|span|div|p|img|details|summary|table|tr|td|th|ul|ol|li)\b)[a-z][^<>\n]{3,}>", re.I)
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=\S)")  # over-splitting only shortens sentences
WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’-]*")


def prose_lines(text: str):
    """Yield (line_number, line, kind) where kind is heading, table or prose."""
    in_fence = in_front = False
    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.rstrip()
        if number == 1 and line.strip() == "---":
            in_front = True
            continue
        if in_front:
            in_front = line.strip() != "---"
            continue
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence or not line.strip():
            continue
        if HEADING.match(line):
            yield number, line, "heading"
        elif line.lstrip().startswith("|"):
            yield number, line, "table"
        else:
            yield number, re.sub(r"^\s*([-*+]|\d+[.)]|>)\s+", "", line), "prose"


def check(text: str, budget: int, max_sentence: int) -> dict:
    defects: list[dict] = []
    main_words = 0
    in_appendix = False
    first_prose_seen = False
    prose_words = 0
    hedges = bolds = 0

    def add(kind, line, detail):
        defects.append({"kind": kind, "line": line, "detail": detail})

    for number, line, kind in prose_lines(text):
        if kind == "heading":
            if APPENDIX.match(line):
                in_appendix = True
            title = HEADING.match(line).group(2).strip().strip("#").strip().lower().rstrip(":")
            if title in LABEL_HEADINGS:
                add("label heading", number, f"'{title}' names a bucket; say what the section concludes")
            continue
        words = WORD.findall(line)
        if not in_appendix:
            main_words += len(words)
        if kind == "table":
            continue
        prose_words += len(words)
        if not first_prose_seen:
            first_prose_seen = True
            if SLOW_OPENING.match(re.sub(r"^[*_]+", "", line.strip())):
                add("slow opening", number, "open with the point, not with what the document is")
        for match in META.finditer(line):
            add("meta-commentary", number, match.group(0))
        for sentence in SENTENCE_SPLIT.split(line):
            count = len(WORD.findall(sentence))
            if count > max_sentence:
                add("long sentence", number, f"{count} words")
        hedges += len(HEDGES.findall(line))
        bolds += len(BOLD.findall(line))
        # Inline code shows syntax (`git log -S "<value>"`), not an unfilled gap.
        for match in PLACEHOLDER.finditer(INLINE_CODE.sub("", line)):
            add("open placeholder", number, match.group(0))

    if main_words > budget:
        add("over budget", 0, f"{main_words} main-path words; budget {budget}")
    if prose_words and hedges / prose_words * 100 > 2:
        add("heavy hedging", 0, f"{hedges} hedges in {prose_words} words")
    if prose_words and bolds > max(1, prose_words / 60):
        add("bold overuse", 0, f"{bolds} bold spans in {prose_words} words")
    return {"main_path_words": main_words, "budget": budget, "defects": defects}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file", type=Path)
    parser.add_argument("--budget", type=int, default=500, help="main-path word budget (default 500, about one page)")
    parser.add_argument("--max-sentence", type=int, default=35)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--warn-only", action="store_true")
    args = parser.parse_args(argv)
    try:
        text = args.file.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    report = check(text, args.budget, args.max_sentence)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for d in report["defects"]:
            where = f"line {d['line']}" if d["line"] else "document"
            print(f"{where}: {d['kind']}: {d['detail']}")
        print(f"\n{len(report['defects'])} defect(s); {report['main_path_words']} main-path words "
              f"(budget {report['budget']}). Mechanical checks only; still run the fresh-reader test.")
    return 0 if (args.warn_only or not report["defects"]) else 1


if __name__ == "__main__":
    sys.exit(main())
