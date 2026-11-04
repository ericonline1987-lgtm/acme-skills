#!/usr/bin/env python3
"""Check an SVG file for the structural problems that break it where it will be shown.

Errors (exit 1):
  - not well-formed XML, or the root is not <svg>
  - missing viewBox, or a viewBox that is not four numbers with positive width and height
  - duplicate id values
  - internal references (href="#x", xlink:href="#x", url(#x)) to ids that don't exist
  - <script> elements or on* event attributes (unsafe or blocked in most viewers)
Warnings:
  - external dependencies (http/https/file/relative hrefs, @import) that break offline
  - no width/height attributes (the host must size it)
  - no <title> (screen readers have nothing to announce)

What this cannot check: layout, overlaps, legibility at the viewing size, colour
contrast, or whether the picture is correct. Look at the rendered result as well.

Usage:
  validate_svg.py FILE.svg [--json]

Exit status: 0 no errors, 1 errors found, 2 unreadable.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

XLINK = "{http://www.w3.org/1999/xlink}href"
URL_REF = re.compile(r"url\(\s*['\"]?#([^'\")\s]+)['\"]?\s*\)")
IMPORT = re.compile(r"@import\s+(url\()?['\"]?([^'\");]+)")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def check(text: str) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        return {"errors": [f"not well-formed XML: {exc}"], "warnings": []}
    if local_name(root.tag) != "svg":
        return {"errors": [f"root element is <{local_name(root.tag)}>, not <svg>"], "warnings": []}

    view_box = root.get("viewBox")
    if view_box is None:
        errors.append("missing viewBox (the drawing will not scale)")
    else:
        parts = re.split(r"[\s,]+", view_box.strip())
        try:
            numbers = [float(p) for p in parts]
            if len(numbers) != 4 or numbers[2] <= 0 or numbers[3] <= 0:
                raise ValueError
        except ValueError:
            errors.append(f"invalid viewBox {view_box!r} (need: min-x min-y width height, width and height > 0)")
    if root.get("width") is None or root.get("height") is None:
        warnings.append("no width/height on <svg>; the host page must size it")

    ids: dict[str, int] = {}
    refs: set[str] = set()
    has_title = False
    for element in root.iter():
        name = local_name(element.tag)
        if name == "title":
            has_title = True
        if name == "script":
            errors.append("contains <script>")
        element_id = element.get("id")
        if element_id:
            ids[element_id] = ids.get(element_id, 0) + 1
        for attr, value in element.attrib.items():
            attr_name = local_name(attr)
            if attr_name.lower().startswith("on"):
                errors.append(f"event attribute {attr_name} on <{name}>")
            if attr in (XLINK, "href") or attr_name == "href":
                if value.startswith("#"):
                    refs.add(value[1:])
                elif value and not value.startswith("data:"):
                    warnings.append(f"external dependency on <{name}>: {value}")
            refs.update(URL_REF.findall(value))
        if name == "style" and element.text:
            refs.update(URL_REF.findall(element.text))
            for match in IMPORT.finditer(element.text):
                warnings.append(f"external stylesheet import: {match.group(2)}")

    for element_id, count in sorted(ids.items()):
        if count > 1:
            errors.append(f"duplicate id {element_id!r} ({count} times)")
    for ref in sorted(refs - set(ids)):
        errors.append(f"reference to missing id #{ref}")
    if not has_title:
        warnings.append("no <title>; add one so assistive technology can name the image")
    return {"errors": errors, "warnings": warnings}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        text = args.file.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    report = check(text)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for message in report["errors"]:
            print(f"ERROR  {message}")
        for message in report["warnings"]:
            print(f"WARN   {message}")
        print(f"\n{len(report['errors'])} error(s), {len(report['warnings'])} warning(s). "
              "Layout, legibility and correctness are not checked; look at the render.")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
