#!/usr/bin/env python3
"""Build the three arms of the v4 comparison (see docs/PLAN-v4.md).

Creates, under OUT:
  base/   decoy skills only (the baseline: a realistic workspace without either set)
  acme/   this repo's skills plus the same decoys
  ref/    another skill set's skills plus the same decoys
Each arm is one plugin with the same cases copied into evals/. No arm gets a session-start
routing line or always-on rules, so the arms differ only in skill content and descriptions.
Also writes OUT/skill_names.json (every skill name in any arm), which pairwise.py redacts
from answers before judging so the judge cannot tell the arms apart by name.

The arms exist only for measurement; they are never published (the decoys keep their own
licences and are not copied into this repo).

Usage:
  build_arms.py --ref-skills REF/skills --decoys ANTHROPIC_SKILLS/skills --cases CASES --out DIR

Exit status: 0 built, 2 bad paths, missing decoys or existing output.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SKILL_PLUGINS = ["engineering-lifecycle", "professional-craft"]
# Four near competitors (writing, documents, UI design, browser testing) and three unrelated
# skills, so routing is tested in a crowded workspace rather than an empty one.
DECOYS = ["doc-coauthoring", "internal-comms", "frontend-design", "webapp-testing",
          "mcp-builder", "slack-gif-creator", "algorithmic-art"]
IGNORE = shutil.ignore_patterns("evals", "tests", "agents", "__pycache__")


def arm(out: Path, name: str, description: str) -> Path:
    root = out / name
    (root / ".claude-plugin").mkdir(parents=True)
    (root / "skills").mkdir()
    (root / ".claude-plugin" / "plugin.json").write_text(
        json.dumps({"name": f"v4-{name}", "version": "0.0.1", "description": description}, indent=2))
    return root


def add_decoys(root: Path, decoys: Path) -> None:
    for name in DECOYS:
        shutil.copytree(decoys / name, root / "skills" / name, ignore=IGNORE)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ref-skills", type=Path, required=True)
    parser.add_argument("--decoys", type=Path, required=True)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    for path in (args.ref_skills, args.decoys, args.cases):
        if not path.is_dir():
            print(f"error: {path} is not a directory", file=sys.stderr)
            return 2
    missing = [d for d in DECOYS if not (args.decoys / d / "SKILL.md").is_file()]
    if missing:
        print(f"error: decoys not found: {', '.join(missing)}", file=sys.stderr)
        return 2
    if args.out.exists() and any(args.out.iterdir()):
        print(f"error: {args.out} is not empty", file=sys.stderr)
        return 2
    args.out.mkdir(parents=True, exist_ok=True)

    base = arm(args.out, "base", "Decoy skills only, for comparison")
    add_decoys(base, args.decoys)

    acme = arm(args.out, "acme", "acme-skills plus decoys, for comparison")
    for plugin in SKILL_PLUGINS:
        for skill in sorted((REPO / "plugins" / plugin / "skills").iterdir()):
            shutil.copytree(skill, acme / "skills" / skill.name, ignore=IGNORE)
    add_decoys(acme, args.decoys)

    ref = arm(args.out, "ref", "Reference skill set plus decoys, for comparison")
    for skill in sorted(args.ref_skills.iterdir()):
        if (skill / "SKILL.md").is_file():
            shutil.copytree(skill, ref / "skills" / skill.name, ignore=IGNORE)
    add_decoys(ref, args.decoys)

    names = sorted({p.name for root in (base, acme, ref) for p in (root / "skills").iterdir()})
    (args.out / "skill_names.json").write_text(json.dumps(names, indent=2))
    for root in (base, acme, ref):
        shutil.copytree(args.cases, root / "evals")
    counts = {r.name: len(list((r / "skills").iterdir())) for r in (base, acme, ref)}
    print(f"built arms {counts} with {len(list(args.cases.iterdir()))} cases in {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
