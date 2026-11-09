#!/usr/bin/env python3
"""Score the v4 comparison exactly as docs/PLAN-v4.md pre-registers it.

Reads the arms' eval results (criterion scores, traces) and the pairwise judgments, and
prints one JSON summary:
  pairwise   for each pair of arms, the first arm's win rate (both orders, flip or tie = 0.5),
             averaged per case, with a 95% bootstrap interval over cases; overall and by area
  criteria   each arm's mean criterion score, lift over base with a 95% interval, harm cases
  routing    share of runs that loaded one of the arm's own skills (not a decoy)
  judges     position consistency per judge and agreement between judges
  cost       mean answer cost per run and per passing run; mean answer length

Usage:
  stats.py --arm base=BASE.json --arm acme=ACME.json --arm ref=REF.json --pairs pairs.jsonl \
      [--split split.json]

Exit status: 0.
"""
from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_arms import DECOYS  # noqa: E402
from pairwise import load_arm  # noqa: E402

RESAMPLES = 10000


def area(case: str) -> str:
    parts = case.split("-")
    return parts[1] if len(parts) > 2 else "other"


def boot(values: dict[str, float]) -> dict:
    """Mean over cases with a 95% percentile bootstrap interval, resampling cases."""
    cases = sorted(values)
    if not cases:
        return {"mean": None, "lo": None, "hi": None, "n": 0}
    rng = random.Random(0)
    vals = [values[c] for c in cases]
    means = sorted(statistics.fmean(rng.choices(vals, k=len(vals))) for _ in range(RESAMPLES))
    return {"mean": round(statistics.fmean(vals), 3), "lo": round(means[int(0.025 * RESAMPLES)], 3),
            "hi": round(means[int(0.975 * RESAMPLES) - 1], 3), "n": len(cases)}


def pair_scores(pairs: list[dict], x: str, y: str, judges: set[str] | None = None) -> dict[str, float]:
    """Per case: x's win rate against y, combining both orders of each run and judge."""
    grouped = defaultdict(dict)
    for r in pairs:
        if r["x"] == x and r["y"] == y and (judges is None or r["judge"] in judges):
            grouped[(r["case"], r["run"], r["judge"])][r["order"]] = r["winner"]
    per_case = defaultdict(list)
    for (case, _, _), orders in grouped.items():
        if len(orders) < 2:
            continue
        a, b = orders["xy"], orders["yx"]
        per_case[case].append(1.0 if a == b == x else 0.0 if a == b == y else 0.5)
    return {c: statistics.fmean(v) for c, v in per_case.items()}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--arm", action="append", required=True)
    parser.add_argument("--pairs", type=Path)
    parser.add_argument("--split", type=Path, help='{"dev": [...], "test": [...]}')
    args = parser.parse_args(argv)
    arms = {}
    for spec in args.arm:
        label, _, path = spec.partition("=")
        arms[label] = load_arm(Path(path))
    pairs = [json.loads(l) for l in args.pairs.read_text().splitlines()] if args.pairs else []
    splits = json.loads(args.split.read_text()) if args.split else {}
    out: dict = {"cases": len(next(iter(arms.values())))}

    def subsets(values: dict[str, float]) -> dict:
        res = {"all": boot(values)}
        for name, members in splits.items():
            res[name] = boot({c: v for c, v in values.items() if c in members})
        for a in sorted({area(c) for c in values}):
            res[f"area:{a}"] = boot({c: v for c, v in values.items() if area(c) == a})
        return res

    judges = sorted({r["judge"] for r in pairs})
    out["pairwise"] = {}
    for x, y in [("acme", "ref"), ("acme", "base"), ("ref", "base")]:
        if any(r["x"] == x and r["y"] == y for r in pairs):
            out["pairwise"][f"{x}_vs_{y}"] = subsets(pair_scores(pairs, x, y))
            for j in judges:
                out["pairwise"][f"{x}_vs_{y}"][f"judge:{j}"] = boot(pair_scores(pairs, x, y, {j}))

    def case_scores(label: str) -> dict[str, float]:
        res = {}
        for case, runs in arms[label].items():
            scores = [r["score"] for r in runs if r["score"] is not None and not r["error"]]
            if scores:
                res[case] = statistics.fmean(scores)
        return res

    scores = {label: case_scores(label) for label in arms}
    out["criteria"] = {}
    for label in arms:
        entry = {"score": subsets(scores[label])}
        if label != "base" and "base" in scores:
            lift = {c: scores[label][c] - scores["base"][c] for c in scores[label] if c in scores["base"]}
            entry["lift_over_base"] = subsets(lift)
            entry["harm_cases"] = sorted(c for c, v in lift.items() if v < 0)
        out["criteria"][label] = entry

    out["routing"] = {}
    for label, cases in arms.items():
        runs = [r for rs in cases.values() for r in rs if r["answer"]]
        own = sum(any(s.split(":")[-1] not in DECOYS for s in r["skills"]) for r in runs)
        decoy = sum(any(s.split(":")[-1] in DECOYS for s in r["skills"]) for r in runs)
        out["routing"][label] = {"runs": len(runs), "loaded_own": own, "loaded_decoy": decoy}

    out["judges"] = {}
    for j in judges:
        grouped = defaultdict(dict)
        for r in pairs:
            if r["judge"] == j:
                grouped[(r["case"], r["run"], r["x"], r["y"])][r["order"]] = r["winner"]
        both = [o for o in grouped.values() if len(o) == 2]
        out["judges"][j] = {"pairs": len(both),
                            "position_consistent": round(sum(o["xy"] == o["yx"] for o in both) / max(len(both), 1), 3)}
    if len(judges) >= 2:
        verdicts = defaultdict(dict)
        for r in pairs:
            verdicts[(r["case"], r["run"], r["x"], r["y"], r["judge"])][r["order"]] = r["winner"]
        agree = total = 0
        for (case, run, x, y, j), o in verdicts.items():
            if j != judges[0] or len(o) < 2:
                continue
            other = verdicts.get((case, run, x, y, judges[1]), {})
            if len(other) < 2:
                continue
            combine = lambda d: d["xy"] if d["xy"] == d["yx"] else "tie"  # noqa: E731
            total += 1
            agree += combine(o) == combine(other)
        out["judges"]["agreement"] = round(agree / max(total, 1), 3)

    out["cost"] = {}
    for label, cases in arms.items():
        runs = [r for rs in cases.values() for r in rs if r["cost"] is not None and not r["error"]]
        passing = sum(r["score"] for r in runs if r["score"] is not None)
        total = sum(r["cost"] for r in runs)
        lengths = [len(r["answer"].split()) for r in runs if r["answer"]]
        out["cost"][label] = {"mean_run_usd": round(total / max(len(runs), 1), 4),
                              "usd_per_score_point": round(total / passing, 4) if passing else None,
                              "mean_answer_words": round(statistics.fmean(lengths)) if lengths else None}
    out["judge_cost_usd"] = round(sum(r.get("cost", 0) for r in pairs), 2)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
