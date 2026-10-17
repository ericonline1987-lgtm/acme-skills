#!/usr/bin/env python3
"""Copy shared source files into the skills that use them, or check the copies match.

Skills must be self-contained: Codex and Antigravity install each skill folder on its
own (and `agy plugin install` drops non-skill folders), so a skill can never reference
`../../shared`. The single source of truth lives in `shared/`; `shared/manifest.json`
maps each source file to the skill-relative copies. Edit the source, then run this.

Usage:
  tools/sync_shared.py          write the copies
  tools/sync_shared.py --check  exit 1 if any copy is missing or differs (CI)

Exit status: 0 in sync (or written), 1 drift found with --check, 2 bad manifest.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def pairs() -> list[tuple[Path, Path]]:
    manifest = json.loads((ROOT / "shared" / "manifest.json").read_text(encoding="utf-8"))
    out = []
    for source, targets in manifest["copies"].items():
        src = ROOT / "shared" / source
        if not src.is_file():
            raise FileNotFoundError(f"shared/{source} is listed but missing")
        for target in targets:
            plugin, skill, *rest = target.split("/")
            out.append((src, ROOT / "plugins" / plugin / "skills" / skill / Path(*rest)))
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        items = pairs()
    except (OSError, KeyError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    drift = []
    for src, dst in items:
        same = dst.is_file() and dst.read_bytes() == src.read_bytes()
        if args.check:
            if not same:
                drift.append(dst)
        elif not same:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            if src.suffix == ".py":
                dst.chmod(0o755)
            print(f"wrote {dst.relative_to(ROOT)}")
    if drift:
        for dst in drift:
            print(f"out of sync: {dst.relative_to(ROOT)} (run tools/sync_shared.py)")
        return 1
    print(f"{len(items)} copies in sync")
    return 0


if __name__ == "__main__":
    sys.exit(main())
