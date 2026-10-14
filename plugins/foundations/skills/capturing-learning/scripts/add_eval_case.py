#!/usr/bin/env python3
"""Turn a lesson into an eval case that `claude plugin eval` runs on every release.

Creates <plugin>/evals/<name>/prompt.md and graders/*.md:

  - one outcome grader (type: llm) per --criteria, so failures are diagnosable
  - for --skill: a display-only trigger check (tool_used: Skill)
  - for --skill with --should-not-fire: a scored check that the skill was NOT used

A SOURCE.md beside them records where the lesson came from, so a later reader
knows why the case exists. Existing cases are never overwritten.

Usage:
  add_eval_case.py --plugin-dir plugins/foundations --name overclaim-deploy \
      --prompt "..." --criteria "..." --criteria "..." [--skill proving-outcomes] \
      [--should-not-fire] [--source "incident 2026-10-02: ..."] [--max-turns 10]

Exit status: 0 created, 1 refused (exists or invalid), 2 usage error.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

NAME = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}$")


def frontmatter(fields: dict) -> str:
    lines = ["---"]
    for key, value in fields.items():
        if isinstance(value, list):
            lines.append(f"{key}: [{', '.join(value)}]")
        elif isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines)


def build_case(args: argparse.Namespace) -> dict[str, str]:
    """Return {relative path: content} for the case."""
    files: dict[str, str] = {}
    files["prompt.md"] = (
        frontmatter({"max_turns": args.max_turns, "allowed_tools": ["Read", "Glob", "Grep", "Skill"]})
        + "\n\n" + args.prompt.strip() + "\n"
    )
    # One grader per criterion: a failed run then shows which criterion failed,
    # and a case earns partial credit instead of all-or-nothing.
    for index, criterion in enumerate(args.criteria, start=1):
        words = re.findall(r"[a-z0-9]+", criterion.lower())[:5]
        slug = "-".join(words) or "criterion"
        files[f"graders/c{index}-{slug}.md"] = (
            frontmatter({"type": "llm", "weight": 1})
            + "\n\nPass if this holds for the response: " + criterion.strip() + "\n"
        )
    if args.skill and args.should_not_fire:
        files["graders/skill-not-used.md"] = frontmatter({
            "type": "tool_used", "tool": "Skill", "input_match": args.skill,
            "min": 0, "max": 0, "arm": "both",
        }) + "\n"
    elif args.skill:
        files["graders/skill-fired.md"] = frontmatter({
            "type": "tool_used", "tool": "Skill", "input_match": args.skill,
        }) + "\n"
    files["SOURCE.md"] = (
        f"# Why this case exists\n\n{(args.source or 'Not recorded.').strip()}\n"
    )
    return files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--plugin-dir", type=Path, required=True)
    parser.add_argument("--name", required=True, help="lowercase-hyphenated case name")
    parser.add_argument("--prompt", required=True, help="the task, written as a user would ask it")
    parser.add_argument("--criteria", required=True, action="append",
                        help="one observable thing a successful answer does; repeat for each criterion")
    parser.add_argument("--skill", help="skill this case exercises")
    parser.add_argument("--should-not-fire", action="store_true", help="the skill must not be used")
    parser.add_argument("--source", help="where the lesson came from")
    parser.add_argument("--max-turns", type=int, default=10)
    args = parser.parse_args(argv)

    if not NAME.match(args.name):
        print("error: --name must be lowercase letters, digits and hyphens", file=sys.stderr)
        return 1
    if args.should_not_fire and not args.skill:
        print("error: --should-not-fire needs --skill", file=sys.stderr)
        return 1
    if not (args.plugin_dir / ".claude-plugin" / "plugin.json").is_file():
        print(f"error: {args.plugin_dir} is not a plugin (no .claude-plugin/plugin.json)", file=sys.stderr)
        return 1
    if args.skill and not (args.plugin_dir / "skills" / args.skill / "SKILL.md").is_file():
        print(f"note: skill {args.skill!r} is not in this plugin; the case still checks for it by name")

    case_dir = args.plugin_dir / "evals" / args.name
    if case_dir.exists():
        print(f"error: {case_dir} already exists; choose another name", file=sys.stderr)
        return 1

    for relative, content in build_case(args).items():
        path = case_dir / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"wrote {path}")
    print(f"\nRun it: claude plugin eval {args.plugin_dir} --case {args.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
