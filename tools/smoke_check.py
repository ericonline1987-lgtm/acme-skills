#!/usr/bin/env python3
"""Check that a runtime actually sees every skill: install, ask the agent, compare.

Installs the skills into a fresh project folder with tools/install.py, runs the
runtime's non-interactive command there with a prompt asking for the skills it can
see, and reports any skill missing from the answer. Run it on a machine where the
runtime is installed and signed in; it costs one agent session per run.

  tools/smoke_check.py --runtime codex --command 'codex exec {prompt}'
  tools/smoke_check.py --runtime antigravity --command '<your agy non-interactive command> {prompt}'

{prompt} is replaced by the shell-quoted prompt. Exit status: 0 every skill seen,
1 some missing, 2 bad input or the command failed.
"""
from __future__ import annotations

import argparse
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPT = ("List the name of every agent skill available to you in this session, one per "
          "line, exactly as named, and nothing else.")


def expected_skills() -> list[str]:
    return sorted(p.parent.name for p in ROOT.glob("plugins/*/skills/*/SKILL.md"))


def missing_from(answer: str, skills: list[str]) -> list[str]:
    """Skills whose exact name doesn't appear as a whole word in the answer."""
    return [s for s in skills if not re.search(rf"(?<![\w-]){re.escape(s)}(?![\w-])", answer)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--runtime", required=True, choices=["claude", "codex", "antigravity"])
    parser.add_argument("--command", required=True, help="non-interactive command; {prompt} is substituted")
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args(argv)
    if "{prompt}" not in args.command:
        print("error: --command must contain {prompt}", file=sys.stderr)
        return 2
    skills = expected_skills()
    with tempfile.TemporaryDirectory() as project:
        install = subprocess.run([sys.executable, str(ROOT / "tools" / "install.py"), "--runtime", args.runtime,
                                  "--scope", "project", "--project", project], capture_output=True, text=True)
        if install.returncode != 0:
            print(install.stdout + install.stderr, file=sys.stderr)
            return 2
        command = args.command.replace("{prompt}", shlex.quote(PROMPT))
        try:
            run = subprocess.run(command, shell=True, cwd=project, capture_output=True, text=True,
                                 timeout=args.timeout, stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            print(f"error: command timed out after {args.timeout}s", file=sys.stderr)
            return 2
        if run.returncode != 0 and not run.stdout.strip():
            print(f"error: command failed ({run.returncode}): {run.stderr.strip()[:500]}", file=sys.stderr)
            return 2
    missing = missing_from(run.stdout, skills)
    print(f"{args.runtime}: {len(skills) - len(missing)} of {len(skills)} skills seen")
    for name in missing:
        print(f"  missing: {name}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
