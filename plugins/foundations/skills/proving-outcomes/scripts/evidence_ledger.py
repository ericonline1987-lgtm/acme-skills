#!/usr/bin/env python3
"""Compute the highest rung a claim of "done" has actually reached, and flag overclaims.

A ledger is a JSON file (see shared/templates/evidence-ledger.example.json):

  claim          what is being called done
  claimed_rung   1-5, the rung the report is about to claim
  evidence       list of {rung, check, result, source} or {rung, na: "<reason>"}
  follow_up      {due: YYYY-MM-DD, check, owner} or {none: "<reason>"}

Rungs:
  1 Checked              automated checks or tests pass, real result read
  2 Delivered            the work reached its destination (merged, deployed, sent, published)
  3 Working in real use  exercised with real inputs in the real environment
  4 Accepted             the consumer confirmed it through their own path
  5 Outcome achieved     the intended change in the world was observed

Rules:
  - A rung counts only if it and every rung below it has valid evidence (or is
    marked not applicable with a reason). Evidence is valid when check, result
    and source are all non-empty and the result does not report failures.
  - claimed_rung above the supported rung is an overclaim (exit 1).
  - Below rung 5, a follow-up is required: a dated check with an owner, or an
    explicit "none" with a reason. Without it the outcome is never checked.
  - A follow-up whose due date has passed is reported as overdue.

What this cannot see: whether the evidence is true or was really observed.
It checks that claims and recorded evidence agree.

Usage:
  evidence_ledger.py LEDGER.json [--today YYYY-MM-DD] [--json]

Exit status: 0 consistent, 1 overclaim or missing follow-up or invalid ledger, 2 unreadable.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

RUNGS = {
    1: "Checked",
    2: "Delivered",
    3: "Working in real use",
    4: "Accepted",
    5: "Outcome achieved",
}
# "3 failed", "2 errors", "1 failure" (non-zero counts) or plain failure words.
FAILING_COUNT = re.compile(r"\b([1-9]\d*)\s+(failed|failures?|errors?)\b", re.I)
FAILING_WORD = re.compile(r"\b(FAILED|FAILURE|ERROR|timed out|not found)\b")


def evidence_problem(item: dict) -> str | None:
    """Return why an evidence item does not count, or None if it counts."""
    if not isinstance(item, dict):
        return "not an object"
    if item.get("na"):
        return None
    for field in ("check", "result", "source"):
        if not str(item.get(field, "")).strip():
            return f"missing {field}"
    result = str(item["result"])
    if FAILING_COUNT.search(result) or FAILING_WORD.search(result):
        return f"result reports a failure: {result!r}"
    return None


def evaluate(ledger: dict, today: dt.date) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    claimed = ledger.get("claimed_rung")
    if not isinstance(claimed, int) or claimed not in RUNGS:
        errors.append("claimed_rung must be an integer from 1 to 5")
        claimed = 0
    if not str(ledger.get("claim", "")).strip():
        errors.append("claim is empty")

    by_rung: dict[int, list[dict]] = {r: [] for r in RUNGS}
    for index, item in enumerate(ledger.get("evidence") or []):
        rung = item.get("rung") if isinstance(item, dict) else None
        if rung not in RUNGS:
            errors.append(f"evidence[{index}] has invalid rung {rung!r}")
            continue
        problem = evidence_problem(item)
        if problem:
            warnings.append(f"evidence[{index}] (rung {rung}) does not count: {problem}")
        else:
            by_rung[rung].append(item)

    supported = 0
    for rung in sorted(RUNGS):
        if by_rung[rung]:
            supported = rung
        else:
            break

    if claimed > supported:
        errors.append(
            f"overclaim: claims rung {claimed} ({RUNGS[claimed]}) but evidence supports "
            f"rung {supported}" + (f" ({RUNGS[supported]})" if supported else " (nothing)")
        )

    follow = ledger.get("follow_up")
    overdue = False
    if supported < 5:
        if not isinstance(follow, dict):
            errors.append("no follow_up: below rung 5 the outcome must get a dated check or an explicit none")
        elif follow.get("none"):
            warnings.append(f"no outcome check planned: {follow['none']}")
        else:
            missing = [f for f in ("due", "check", "owner") if not str(follow.get(f, "")).strip()]
            if missing:
                errors.append(f"follow_up missing {', '.join(missing)}")
            else:
                try:
                    due = dt.date.fromisoformat(str(follow["due"]))
                    if due < today:
                        overdue = True
                        warnings.append(f"follow-up overdue since {due.isoformat()}: {follow['check']}")
                except ValueError:
                    errors.append(f"follow_up.due is not YYYY-MM-DD: {follow['due']!r}")

    next_rung = supported + 1 if supported < 5 else None
    return {
        "claim": ledger.get("claim", ""),
        "claimed_rung": claimed,
        "supported_rung": supported,
        "supported_name": RUNGS.get(supported, "nothing"),
        "next_rung": next_rung,
        "next_name": RUNGS.get(next_rung) if next_rung else None,
        "follow_up_overdue": overdue,
        "errors": errors,
        "warnings": warnings,
        "consistent": not errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--today", type=dt.date.fromisoformat, default=dt.date.today())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: cannot read ledger: {exc}", file=sys.stderr)
        return 2
    if not isinstance(ledger, dict):
        print("error: ledger must be a JSON object", file=sys.stderr)
        return 2

    report = evaluate(ledger, args.today)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"claim:          {report['claim']}")
        print(f"claimed rung:   {report['claimed_rung']}")
        print(f"supported rung: {report['supported_rung']} ({report['supported_name']})")
        if report["next_rung"]:
            print(f"next rung:      {report['next_rung']} ({report['next_name']})")
        for message in report["errors"]:
            print(f"ERROR  {message}")
        for message in report["warnings"]:
            print(f"WARN   {message}")
        print("\nconsistent" if report["consistent"] else "\nNOT consistent: report the supported rung, not the claimed one")
    return 0 if report["consistent"] else 1


if __name__ == "__main__":
    sys.exit(main())
