#!/usr/bin/env python3
"""Generate the Codex and Antigravity packaging from the Claude Code manifests.

One set of skill folders serves three runtimes. The source of truth is each plugin's
`.claude-plugin/plugin.json` plus the display text in `tools/skill_ui.json`. From those
this writes:

  plugins/<p>/.codex-plugin/plugin.json     Codex plugin manifest
  plugins/<p>/plugin.json                    Antigravity plugin manifest (name, description only:
                                             its schema forbids other keys)
  plugins/<p>/skills/<s>/agents/openai.yaml  Codex UI metadata per skill
  .agents/plugins/marketplace.json           Codex marketplace (skill plugins only; rules
                                             reach Codex through AGENTS.md, see tools/install.py)

Usage:
  tools/build_manifests.py          write the files
  tools/build_manifests.py --check  exit 1 if any generated file is missing or stale (CI)

Exit status: 0 written or in sync, 1 stale with --check, 2 bad input.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO_URL = "https://github.com/ericonline1987-lgtm/acme-skills"
AGY_SCHEMA = "https://antigravity.google/schemas/v1/plugin.json"


def dump(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def plan() -> dict[Path, str]:
    ui = json.loads((ROOT / "tools" / "skill_ui.json").read_text(encoding="utf-8"))
    claude_market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    files: dict[Path, str] = {}
    market_entries = []

    for entry in claude_market["plugins"]:
        name = entry["name"]
        pdir = ROOT / "plugins" / name
        manifest = json.loads((pdir / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        pui = ui["plugins"][name]
        has_skills = (pdir / "skills").is_dir()

        files[pdir / "plugin.json"] = dump({
            "$schema": AGY_SCHEMA,
            "name": name,
            "description": manifest["description"],
        })

        if not has_skills:
            continue  # rules-only plugin: Codex reads rules from AGENTS.md instead

        codex = {
            "name": name,
            "version": manifest["version"],
            "description": manifest["description"],
            "author": {"name": manifest["author"]["name"], "url": f"https://github.com/{manifest['author']['name']}"},
            "homepage": REPO_URL,
            "repository": REPO_URL,
            "license": "MIT",
            "keywords": manifest.get("keywords", []),
            "skills": "./skills/",
            "interface": {
                "displayName": pui["displayName"],
                "shortDescription": pui["shortDescription"],
                "longDescription": manifest["description"],
                "developerName": manifest["author"]["name"],
                "category": pui["category"],
                "capabilities": ["Interactive", "Read", "Write"],
                "defaultPrompt": pui["defaultPrompt"],
                "websiteURL": REPO_URL,
            },
        }
        files[pdir / ".codex-plugin" / "plugin.json"] = dump(codex)
        market_entries.append({
            "name": name,
            "source": {"source": "local", "path": f"./plugins/{name}"},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": pui["category"],
        })

        for skill_dir in sorted(p for p in (pdir / "skills").iterdir() if (p / "SKILL.md").is_file()):
            display, short, prompt = ui["skills"][skill_dir.name]
            if not 25 <= len(short) <= 64:
                raise ValueError(f"{skill_dir.name}: short_description must be 25-64 chars, is {len(short)}")
            if f"${skill_dir.name}" not in prompt:
                raise ValueError(f"{skill_dir.name}: default_prompt must mention ${skill_dir.name}")
            files[skill_dir / "agents" / "openai.yaml"] = (
                "interface:\n"
                f"  display_name: {yaml_quote(display)}\n"
                f"  short_description: {yaml_quote(short)}\n"
                f"  default_prompt: {yaml_quote(prompt)}\n"
            )

    files[ROOT / ".agents" / "plugins" / "marketplace.json"] = dump({
        "name": claude_market["name"],
        "interface": {"displayName": "acme-skills"},
        "plugins": market_entries,
    })
    return files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        files = plan()
    except (OSError, KeyError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    stale = [p for p, text in files.items() if not p.is_file() or p.read_text(encoding="utf-8") != text]
    if args.check:
        for p in stale:
            print(f"stale: {p.relative_to(ROOT)} (run tools/build_manifests.py)")
        if not stale:
            print(f"{len(files)} generated files in sync")
        return 1 if stale else 0
    for p in stale:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(files[p], encoding="utf-8")
    print(f"wrote {len(stale)} of {len(files)} generated files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
