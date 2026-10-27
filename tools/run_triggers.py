#!/usr/bin/env python3
"""Measure skill triggering with Claude Code: which skill (if any) each query makes the agent load.

Reads every plugins/*/evals/triggers/<skill>.json ({query, should_trigger}), sends each
query to a fresh `claude -p` session with all skill plugins loaded (so skills compete as
they do in real use), and records the skills the agent invoked. Reports per skill:

  recall     should-trigger queries that loaded this skill
  precision  near-miss queries that correctly did NOT load it
  confusion  the skill loaded instead, when a different one fired

Every run is a real session on your Claude credential and costs money; --max-cost-usd
stops launching new queries once the running total passes the ceiling. Results go to
--out as JSON so a report never needs re-running.

Codex and Antigravity: the same JSON files work with their non-interactive modes, but
this runner only drives Claude Code. See docs/RUNTIMES.md.

Usage:
  tools/run_triggers.py [--model sonnet] [--max-turns 6] [--skills a b] [-j 6] [--max-cost-usd 8] [--with-rules] [--out FILE]

Exit status: 0 completed, 2 claude CLI missing or bad input, 3 stopped at the cost ceiling.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import shutil
import subprocess
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_PLUGINS = ["foundations", "engineering-lifecycle", "professional-craft"]


def load_queries(only: set[str] | None) -> list[dict]:
    rows = []
    for plugin in SKILL_PLUGINS:
        for path in sorted((ROOT / "plugins" / plugin / "evals" / "triggers").glob("*.json")):
            if only and path.stem not in only:
                continue
            for row in json.loads(path.read_text(encoding="utf-8")):
                rows.append({"skill": path.stem, **row})
    return rows


def invoked_skills(stream: str) -> tuple[list[str], float, bool]:
    """Skill names invoked, session cost, and whether the session hit a usage limit.

    The limit is read from the session's own result event, never from the answer text,
    which may legitimately mention limits (a rate-limiter question, for example)."""
    skills, cost, limited = [], 0.0, False
    for line in stream.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "assistant":
            for block in event.get("message", {}).get("content", []):
                if block.get("type") == "tool_use" and block.get("name") == "Skill":
                    raw = str(block.get("input", {}).get("skill", ""))
                    skills.append(raw.split(":")[-1])
        elif event.get("type") == "result":
            cost = float(event.get("total_cost_usd") or 0.0)
            if event.get("is_error") and "limit" in str(event.get("result", "")).lower():
                limited = True
    return skills, cost, limited


def run_one(row: dict, model: str, max_turns: int, with_rules: bool = False) -> dict:
    cmd = ["claude", "-p", row["query"], "--output-format", "stream-json", "--verbose",
           "--max-turns", str(max_turns), "--model", model,
           "--disallowedTools", "Bash,Write,Edit,NotebookEdit,WebFetch,WebSearch"]
    for plugin in SKILL_PLUGINS + (["core-rules"] if with_rules else []):
        cmd += ["--plugin-dir", str(ROOT / "plugins" / plugin)]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=180, stdin=subprocess.DEVNULL).stdout
    except subprocess.TimeoutExpired:
        out = ""
    skills, cost, limited = invoked_skills(out)
    return {**row, "invoked": skills, "cost": cost, "error": "usage limit" if limited else (None if out else "no output")}


def summarise(results: list[dict]) -> dict:
    per: dict[str, dict] = {}
    for r in results:
        s = per.setdefault(r["skill"], {"pos": 0, "hit": 0, "neg": 0, "clean": 0, "instead": {}})
        fired = r["skill"] in r["invoked"]
        if r["should_trigger"]:
            s["pos"] += 1
            s["hit"] += fired
            for other in r["invoked"]:
                if other != r["skill"]:
                    s["instead"][other] = s["instead"].get(other, 0) + 1
        else:
            s["neg"] += 1
            s["clean"] += not fired
    return per


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--model", default="sonnet")
    parser.add_argument("--max-turns", type=int, default=6,
                        help="agents often explore first and load a skill later; too few turns undercounts")
    parser.add_argument("--skills", nargs="+")
    parser.add_argument("-j", "--concurrency", type=int, default=6)
    parser.add_argument("--max-cost-usd", type=float, default=8.0)
    parser.add_argument("--with-rules", action="store_true",
                        help="also load the optional core-rules plugin, to measure its effect on triggering")
    parser.add_argument("--out", type=Path, default=Path("trigger-results.json"))
    args = parser.parse_args(argv)
    if not shutil.which("claude"):
        print("error: claude CLI not found", file=sys.stderr)
        return 2
    rows = load_queries(set(args.skills) if args.skills else None)
    if not rows:
        print("error: no trigger queries found", file=sys.stderr)
        return 2

    results, spent, stopped = [], 0.0, False
    lock = threading.Lock()
    with cf.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        pending = {}
        queue = list(rows)
        while queue or pending:
            while queue and len(pending) < args.concurrency and not stopped:
                row = queue.pop(0)
                pending[pool.submit(run_one, row, args.model, args.max_turns, args.with_rules)] = row
            if not pending:
                break
            done, _ = cf.wait(pending, return_when=cf.FIRST_COMPLETED)
            for fut in done:
                pending.pop(fut)
                res = fut.result()
                with lock:
                    results.append(res)
                    spent += res["cost"]
                    if res["error"] == "usage limit" or spent >= args.max_cost_usd:
                        stopped = True
            if stopped:
                queue.clear()

    per = summarise(results)
    args.out.write_text(json.dumps({"model": args.model, "with_rules": args.with_rules, "spent_usd": round(spent, 2),
                                    "stopped_early": stopped, "results": results, "summary": per}, indent=2))
    print(f"{'skill':24} recall  precision  loaded instead")
    tot = {"pos": 0, "hit": 0, "neg": 0, "clean": 0}
    for skill, s in sorted(per.items()):
        for k in tot:
            tot[k] += s[k]
        instead = ", ".join(f"{k}×{v}" for k, v in sorted(s["instead"].items())) or "-"
        print(f"{skill:24} {s['hit']}/{s['pos']:<5} {s['clean']}/{s['neg']:<8} {instead}")
    print(f"\nall: recall {tot['hit']}/{tot['pos']}, precision {tot['clean']}/{tot['neg']}, "
          f"model {args.model}, spent ${spent:.2f}{' (stopped early)' if stopped else ''}")
    print(f"details: {args.out}")
    return 3 if stopped else 0


if __name__ == "__main__":
    sys.exit(main())
