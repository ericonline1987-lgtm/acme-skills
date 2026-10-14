#!/usr/bin/env python3
"""Score the outcome log: did real work achieve its outcome, and was anything overclaimed?

Reads a CSV with these columns (see outcomes.csv):

  date             YYYY-MM-DD the task was handed off
  task             short description
  area             engineering | writing | other (free text)
  setup            what the agent ran with, e.g. "skills-v1.0" or "none" (the comparison arm)
  claimed_rung     1-5, the rung the hand-off claimed
  supported_rung   1-5, the rung a reviewer found the evidence actually supports
  outcome_due      YYYY-MM-DD the outcome check is due, or blank if none was planned
  outcome_achieved yes | no | blank (not checked yet)
  corrections      how many times a person had to correct or redo part of the work
  notes            free text

Per setup it reports, each rate with a 95% Wilson interval:
  - overclaim rate      claimed_rung > supported_rung
  - follow-up planned   outcome_due filled in
  - outcome achieved    among tasks whose outcome was checked
  - overdue checks      outcome_due passed and outcome_achieved still blank
  - mean corrections

Rows whose task starts with "EXAMPLE" are skipped, so the shipped examples never
pollute real numbers.

Usage:
  score_outcomes.py outcomes.csv [--today YYYY-MM-DD] [--json]

Exit status: 0 on success, 2 on unreadable input or malformed rows.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

REQUIRED = ["date", "task", "setup", "claimed_rung", "supported_rung",
            "outcome_due", "outcome_achieved", "corrections"]


def wilson(successes: int, n: int, z: float = 1.96) -> tuple[float, float] | None:
    """95% Wilson score interval for a proportion; None when n is 0."""
    if n == 0:
        return None
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def rate(successes: int, n: int) -> dict:
    interval = wilson(successes, n)
    return {
        "k": successes,
        "n": n,
        "rate": successes / n if n else None,
        "ci95": [round(interval[0], 3), round(interval[1], 3)] if interval else None,
    }


def parse_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"missing columns: {', '.join(missing)}")
        rows = []
        for line, row in enumerate(reader, start=2):
            if row["task"].strip().upper().startswith("EXAMPLE"):
                continue
            try:
                row["claimed_rung"] = int(row["claimed_rung"])
                row["supported_rung"] = int(row["supported_rung"])
                row["corrections"] = int(row["corrections"] or 0)
                row["outcome_due"] = (dt.date.fromisoformat(row["outcome_due"])
                                      if row["outcome_due"].strip() else None)
            except ValueError as exc:
                raise ValueError(f"line {line}: {exc}") from exc
            achieved = row["outcome_achieved"].strip().lower()
            if achieved not in ("", "yes", "no"):
                raise ValueError(f"line {line}: outcome_achieved must be yes, no or blank")
            row["outcome_achieved"] = achieved or None
            rows.append(row)
        return rows


def score(rows: list[dict], today: dt.date) -> dict:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[row["setup"].strip() or "unlabelled"].append(row)
    report = {}
    for setup, items in sorted(groups.items()):
        n = len(items)
        checked = [r for r in items if r["outcome_achieved"] is not None]
        report[setup] = {
            "tasks": n,
            "overclaim": rate(sum(r["claimed_rung"] > r["supported_rung"] for r in items), n),
            "follow_up_planned": rate(sum(r["outcome_due"] is not None for r in items), n),
            "outcome_achieved": rate(sum(r["outcome_achieved"] == "yes" for r in checked), len(checked)),
            "overdue_checks": sum(1 for r in items if r["outcome_due"] and r["outcome_due"] < today
                                  and r["outcome_achieved"] is None),
            "mean_corrections": round(sum(r["corrections"] for r in items) / n, 2) if n else None,
        }
    return report


def fmt(r: dict) -> str:
    if not r["n"]:
        return "n/a (none yet)"
    lo, hi = r["ci95"]
    return f"{r['rate']:.0%} ({r['k']}/{r['n']}, 95% CI {lo:.0%}-{hi:.0%})"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("csv", type=Path)
    parser.add_argument("--today", type=dt.date.fromisoformat, default=dt.date.today())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        rows = parse_rows(args.csv)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    report = score(rows, args.today)
    if args.json:
        print(json.dumps(report, indent=2))
        return 0
    if not report:
        print("No real tasks logged yet (EXAMPLE rows are skipped).")
        return 0
    for setup, s in report.items():
        print(f"== {setup}: {s['tasks']} task(s)")
        print(f"  overclaim rate     {fmt(s['overclaim'])}")
        print(f"  follow-up planned  {fmt(s['follow_up_planned'])}")
        print(f"  outcome achieved   {fmt(s['outcome_achieved'])}")
        print(f"  overdue checks     {s['overdue_checks']}")
        print(f"  mean corrections   {s['mean_corrections']}")
    print("\nIntervals overlap? Then the difference between setups is not yet established.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
