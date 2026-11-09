#!/usr/bin/env python3
"""Blind pairwise judging of the v4 arms (see docs/PLAN-v4.md).

For every case and run index, each pair of arms is judged twice, once in each order, by each
judge model. Skill names are redacted from both answers first. Judgments are appended to a
JSONL file, and existing judgments are skipped, so an interrupted run resumes where it stopped.

Usage:
  pairwise.py --arm base=BASE.json --arm acme=ACME.json --arm ref=REF.json \
      --cases CASES --names skill_names.json --judge opus --judge sonnet --out pairs.jsonl

BASE.json etc. are `claude plugin eval --json` results run with --keep-temp, so each run's
trace (and so its final answer) is still on disk.

Exit status: 0 done, 3 stopped at a usage limit (rerun later to resume), 2 bad input.
"""
from __future__ import annotations

import argparse
import itertools
import json
import re
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PAIRS = [("acme", "ref"), ("acme", "base"), ("ref", "base")]
EXTRA_REDACT = ["acme-skills", "acme", "ly87ing", "agent-skills"]
JUDGE_CWD = Path(__file__).resolve().parent / ".judge-cwd"

PROMPT = """You are a senior specialist judging two responses to the same request.

<request>
{request}
</request>

<what_a_senior_specialist_does>
{rubric}
</what_a_senior_specialist_does>

<checks_from_the_case_author>
{checks}
</checks_from_the_case_author>

<response_1>
{one}
</response_1>

<response_2>
{two}
</response_2>

Decide which response a senior specialist would rather send or ship as it is. Judge substance:
correctness, the specialist points above, and fitness for the reader. Do not prefer a response
for being longer, for its formatting, or for describing its own process. "[a skill]" marks a
redacted name; ignore it. If they are equally good or equally flawed, answer tie.

Reply with one JSON object only: {{"winner": "1" or "2" or "tie", "reason": "<one sentence>"}}"""


def body(md: str) -> str:
    """Strip YAML frontmatter."""
    if md.startswith("---"):
        parts = md.split("---", 2)
        if len(parts) == 3:
            return parts[2].strip()
    return md.strip()


def final_answer(trace: str | None) -> tuple[str | None, list[str]]:
    """Return (final answer, skills loaded) from a run trace, or (None, []) if unusable."""
    if not trace or not Path(trace).is_file():
        return None, []
    answer, skills = None, []
    for line in Path(trace).read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "result":
            answer = None if ev.get("is_error") else ev.get("result")
        for block in (ev.get("message") or {}).get("content") or []:
            if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Skill":
                skills.append(str((block.get("input") or {}).get("skill", "")))
    return answer, skills


def load_arm(path: Path) -> dict[str, list[dict]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for case in data["cases"]:
        runs = []
        for run in case["arms"].get("with", []):
            answer, skills = final_answer(run.get("tracePath"))
            runs.append({"answer": answer if not run.get("error") else None, "skills": skills,
                         "score": run.get("score"), "cost": run.get("costUsd"),
                         "error": run.get("error")})
        out[case["name"]] = runs
    return out


def redactor(names: list[str]):
    words = sorted(set(names) | set(EXTRA_REDACT), key=len, reverse=True)
    pattern = re.compile(r"(?<![\w-])(" + "|".join(re.escape(w) for w in words) + r")(?![\w-])", re.I)
    return lambda text: pattern.sub("[a skill]", text)


def judge_once(model: str, prompt: str) -> tuple[str | None, str, float, bool]:
    """Return (winner '1'/'2'/'tie' or None, reason, cost, hit_limit)."""
    JUDGE_CWD.mkdir(exist_ok=True)
    proc = subprocess.run(
        ["claude", "-p", "--model", model, "--tools", "", "--disable-slash-commands",
         "--strict-mcp-config", "--no-session-persistence", "--output-format", "json"],
        input=prompt, capture_output=True, text=True, cwd=JUDGE_CWD, timeout=600)
    try:
        res = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None, f"unparseable judge output: {proc.stderr[-200:]}", 0.0, False
    cost = float(res.get("total_cost_usd") or 0)
    if res.get("is_error"):
        limit = res.get("api_error") == "usage_limit_reached" or res.get("api_error_status") == 429
        return None, f"judge error: {res.get('api_error') or res.get('subtype')}", cost, limit
    text = res.get("result") or ""
    match = re.search(r"\{[^{}]*\"winner\"[^{}]*\}", text, re.S)
    if not match:
        return None, "no verdict in judge output", cost, False
    try:
        verdict = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None, "bad verdict JSON", cost, False
    winner = str(verdict.get("winner", "")).strip().lower()
    if winner not in ("1", "2", "tie"):
        return None, f"bad winner {winner!r}", cost, False
    return winner, str(verdict.get("reason", ""))[:400], cost, False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--arm", action="append", required=True, help="label=results.json")
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--names", type=Path, required=True)
    parser.add_argument("--judge", action="append", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("-j", type=int, default=6)
    parser.add_argument("--case", default="", help="only cases whose name starts with this")
    args = parser.parse_args(argv)

    arms = {}
    for spec in args.arm:
        label, _, path = spec.partition("=")
        arms[label] = load_arm(Path(path))
    redact = redactor(json.loads(args.names.read_text()))
    done = set()
    if args.out.exists():
        for line in args.out.read_text().splitlines():
            r = json.loads(line)
            done.add((r["case"], r["run"], r["x"], r["y"], r["order"], r["judge"]))

    jobs = []
    for case in sorted(next(iter(arms.values()))):
        if not case.startswith(args.case):
            continue
        cdir = args.cases / case
        request = body((cdir / "prompt.md").read_text())
        rubric = (cdir / "rubric.md").read_text().strip() if (cdir / "rubric.md").is_file() else "(none)"
        checks = "\n".join("- " + body(g.read_text()).replace("Pass if this holds for the response: ", "")
                           for g in sorted((cdir / "graders").glob("*.md")))
        for x, y in PAIRS:
            if x not in arms or y not in arms:
                continue
            for run, (rx, ry) in enumerate(zip(arms[x][case], arms[y][case])):
                if not rx["answer"] or not ry["answer"]:
                    continue
                for order, judge in itertools.product(("xy", "yx"), args.judge):
                    if (case, run, x, y, order, judge) in done:
                        continue
                    a, b = (rx, ry) if order == "xy" else (ry, rx)
                    prompt = PROMPT.format(request=request, rubric=rubric, checks=checks,
                                           one=redact(a["answer"]), two=redact(b["answer"]))
                    jobs.append((case, run, x, y, order, judge, prompt))
    print(f"{len(jobs)} judgments to make", file=sys.stderr)

    lock, stop = threading.Lock(), threading.Event()

    def work(job):
        if stop.is_set():
            return
        case, run, x, y, order, judge, prompt = job
        winner, reason, cost, limit = judge_once(judge, prompt)
        if limit:
            stop.set()
            return
        if winner is None:
            print(f"skip {case} run{run} {x}-{y} {order} {judge}: {reason}", file=sys.stderr)
            return
        first, second = (x, y) if order == "xy" else (y, x)
        arm_winner = {"1": first, "2": second, "tie": "tie"}[winner]
        rec = {"case": case, "run": run, "x": x, "y": y, "order": order, "judge": judge,
               "winner": arm_winner, "reason": reason, "cost": cost}
        with lock, args.out.open("a") as fh:
            fh.write(json.dumps(rec) + "\n")

    with ThreadPoolExecutor(max_workers=args.j) as pool:
        list(pool.map(work, jobs))
    if stop.is_set():
        print("stopped at a usage limit; rerun the same command to resume", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
