#!/usr/bin/env python3
"""Check that a filled-in Markdown document has every required section, filled.

Required sections come from a template (its "## " headings) or from --require.
A section fails when it is missing, empty, or still holds a template placeholder
(<like this>) or a TODO. "TBD" is allowed but reported, because an open item is
honest; an unfilled placeholder is not.

What this cannot see: whether the content is true, specific, or useful. A pass
means the shape is complete, nothing more.

Usage:
  check_sections.py FILE --template TEMPLATE.md
  check_sections.py FILE --require "Outcome" "Follow-up check"
  check_sections.py FILE --template T.md --json

Exit status: 0 when every section passes, 1 when any fails, 2 on usage errors.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HEADING = re.compile(r"^##\s+(.+?)\s*$")
PLACEHOLDER = re.compile(r"<[^<>\n]{3,}>")
HTML_TAG = re.compile(
    r"</?(a|b|i|br|em|strong|code|kbd|sub|sup|span|div|p|img|details|summary|table|tr|td|th|ul|ol|li)"
    r"(\s+[a-z-]+(=(\"[^\"]*\"|'[^']*'|[^\s>]+))?)*\s*/?>",
    re.I,
)
TODO = re.compile(r"\bTODO\b")
TBD = re.compile(r"\bTBD\b")
FENCE = re.compile(r"^\s*(```|~~~)")


def normalise(title: str) -> str:
    return re.sub(r"\s+", " ", title).strip().lower()


def split_sections(text: str) -> dict[str, str]:
    """Map each '## ' heading (normalised) to its body, ignoring fenced code."""
    sections: dict[str, list[str]] = {}
    current: str | None = None
    in_fence = False
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
        if not in_fence:
            match = HEADING.match(line)
            if match:
                current = normalise(match.group(1))
                sections.setdefault(current, [])
                continue
        if current is not None:
            sections[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def required_from_template(path: Path) -> list[str]:
    titles = []
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        match = HEADING.match(line)
        if match and not in_fence:
            titles.append(match.group(1).strip())
    return titles


def has_placeholder(body: str) -> bool:
    for match in PLACEHOLDER.finditer(body):
        if not HTML_TAG.fullmatch(match.group(0)):
            return True
    return False


def check(text: str, required: list[str]) -> list[dict]:
    sections = split_sections(text)
    results = []
    for title in required:
        body = sections.get(normalise(title))
        if body is None:
            status, detail = "fail", "missing"
        elif not body:
            status, detail = "fail", "empty"
        elif has_placeholder(body):
            status, detail = "fail", "unfilled placeholder"
        elif TODO.search(body):
            status, detail = "fail", "contains TODO"
        elif TBD.search(body):
            status, detail = "warn", "contains TBD (open item; make sure it has an owner)"
        else:
            status, detail = "pass", ""
        results.append({"section": title, "status": status, "detail": detail})
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file", type=Path)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--template", type=Path, help="template whose ## headings are required")
    source.add_argument("--require", nargs="+", metavar="HEADING", help="required headings")
    parser.add_argument("--json", action="store_true", help="print results as JSON")
    args = parser.parse_args(argv)

    try:
        text = args.file.read_text(encoding="utf-8")
        required = required_from_template(args.template) if args.template else args.require
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if not required:
        print("error: no required sections found", file=sys.stderr)
        return 2

    results = check(text, required)
    failed = [r for r in results if r["status"] == "fail"]
    if args.json:
        print(json.dumps({"file": str(args.file), "results": results, "passed": not failed}, indent=2))
    else:
        for r in results:
            line = f"{r['status'].upper():4}  {r['section']}"
            print(line + (f"  ({r['detail']})" if r["detail"] else ""))
        print(f"\n{len(results) - len(failed)}/{len(results)} sections complete."
              " Content quality is not checked.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
