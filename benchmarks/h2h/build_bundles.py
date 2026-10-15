#!/usr/bin/env python3
"""Build the two comparison bundles for a head-to-head eval run.

Creates, under OUT:
  acme-all/  every skill from this repo's plugins (plus their shared/ folders) as one plugin
  ref-all/   every skill from another skill set's skills/ folder as one plugin
and copies benchmarks/h2h/cases into each bundle's evals/, so both run identical cases.

The bundles exist only for measurement; they are never published.

Usage:
  build_bundles.py --ref-skills PATH_TO_OTHER_REPO/skills --out DIR

Then, for example:
  claude plugin eval DIR/acme-all --runs 1 -j 4 --judge-model sonnet
  claude plugin eval DIR/ref-all  --runs 1 -j 4 --judge-model sonnet --ablation none

Exit status: 0 built, 2 bad paths or existing output.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SKILL_PLUGINS = ["foundations", "engineering-lifecycle", "professional-craft"]


def bundle(out: Path, name: str, description: str) -> Path:
    root = out / name
    (root / ".claude-plugin").mkdir(parents=True)
    (root / "skills").mkdir()
    (root / ".claude-plugin" / "plugin.json").write_text(
        json.dumps({"name": name, "version": "0.0.1", "description": description}, indent=2))
    return root


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ref-skills", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    if not args.ref_skills.is_dir():
        print(f"error: {args.ref_skills} is not a directory", file=sys.stderr)
        return 2
    if args.out.exists() and any(args.out.iterdir()):
        print(f"error: {args.out} is not empty", file=sys.stderr)
        return 2
    args.out.mkdir(parents=True, exist_ok=True)

    ours = bundle(args.out, "acme-all", "All acme-skills skills, bundled for comparison only")
    for plugin in SKILL_PLUGINS:
        for skill in (REPO / "plugins" / plugin / "skills").iterdir():
            shutil.copytree(skill, ours / "skills" / skill.name)
        shared = REPO / "plugins" / plugin / "shared"
        if shared.is_dir():
            shutil.copytree(shared, ours / "shared", dirs_exist_ok=True)

    ref = bundle(args.out, "ref-all", "Reference skill set, bundled for comparison only")
    for skill in args.ref_skills.iterdir():
        if (skill / "SKILL.md").is_file():
            shutil.copytree(skill, ref / "skills" / skill.name,
                            ignore=shutil.ignore_patterns("evals", "tests", "agents"))

    cases = REPO / "benchmarks" / "h2h" / "cases"
    for root in (ours, ref):
        shutil.copytree(cases, root / "evals")
    print(f"built {ours} ({len(list((ours / 'skills').iterdir()))} skills) and "
          f"{ref} ({len(list((ref / 'skills').iterdir()))} skills) with "
          f"{len(list(cases.iterdir()))} shared cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
