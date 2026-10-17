#!/usr/bin/env python3
"""Install acme-skills into Claude Code, Codex or Antigravity without a plugin marketplace.

Copies skill folders (each one is self-contained) into the runtime's documented skill
directory, and optionally installs the core rules into the runtime's rules file between
marker lines, so re-running replaces the block instead of duplicating it.

Targets (user scope / project scope):

  claude       ~/.claude/skills            .claude/skills          rules: ~/.claude/CLAUDE.md | CLAUDE.md
  codex        ~/.agents/skills            .agents/skills          rules: $CODEX_HOME/AGENTS.md | AGENTS.md
               (--codex-legacy: $CODEX_HOME/skills, default ~/.codex/skills)
  antigravity  ~/.gemini/config/skills     .agents/skills          rules: ~/.gemini/GEMINI.md | .agents/rules/acme-core-rules.md

Codex and Antigravity share the project folder `.agents/skills`, so one project install
serves both. The Antigravity rules locations come from a third-party guide, not Google's
own docs; check them against your version.

Safety: it never deletes anything. A skill folder that exists but was not installed by
this tool (no `.acme-skills` marker inside) is skipped unless --force. Use --dry-run to
see every action first.

Usage:
  tools/install.py --runtime codex [--scope user|project] [--project DIR]
                   [--plugins foundations engineering-lifecycle ...] [--rules]
                   [--codex-legacy] [--force] [--dry-run]
  tools/install.py --runtime all --scope project --project ~/code/myapp --rules

Exit status: 0 success, 1 something skipped, 2 bad arguments.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ["foundations", "engineering-lifecycle", "professional-craft"]
MARKER_FILE = ".acme-skills"
BEGIN = "<!-- acme-skills core-rules: begin (managed by tools/install.py) -->"
END = "<!-- acme-skills core-rules: end -->"


def targets(runtime: str, scope: str, project: Path, codex_legacy: bool) -> tuple[Path, Path]:
    """Return (skills_dir, rules_file) for a runtime and scope."""
    home = Path.home()
    codex_home = Path(os.environ.get("CODEX_HOME", home / ".codex"))
    table = {
        ("claude", "user"): (home / ".claude" / "skills", home / ".claude" / "CLAUDE.md"),
        ("claude", "project"): (project / ".claude" / "skills", project / "CLAUDE.md"),
        ("codex", "user"): ((codex_home / "skills") if codex_legacy else (home / ".agents" / "skills"),
                            codex_home / "AGENTS.md"),
        ("codex", "project"): (project / ".agents" / "skills", project / "AGENTS.md"),
        ("antigravity", "user"): (home / ".gemini" / "config" / "skills", home / ".gemini" / "GEMINI.md"),
        ("antigravity", "project"): (project / ".agents" / "skills",
                                     project / ".agents" / "rules" / "acme-core-rules.md"),
    }
    return table[(runtime, scope)]


def skill_sources(plugins: list[str]) -> list[Path]:
    out = []
    for plugin in plugins:
        base = ROOT / "plugins" / plugin / "skills"
        if not base.is_dir():
            raise ValueError(f"unknown plugin with no skills: {plugin}")
        out += sorted(p for p in base.iterdir() if (p / "SKILL.md").is_file())
    return out


def install_skills(sources: list[Path], dest: Path, force: bool, dry: bool, log: list[str]) -> int:
    skipped = 0
    for src in sources:
        target = dest / src.name
        ours = (target / MARKER_FILE).is_file()
        if target.exists() and not ours and not force:
            log.append(f"SKIP   {target} exists and was not installed by acme-skills (use --force)")
            skipped += 1
            continue
        log.append(f"{'UPDATE' if target.exists() else 'ADD'}    {target}")
        if not dry:
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(src, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            (target / MARKER_FILE).write_text("installed by acme-skills tools/install.py\n")
    return skipped


def install_rules(rules_file: Path, dry: bool, log: list[str]) -> None:
    body = (ROOT / "plugins" / "core-rules" / "rules" / "core.md").read_text(encoding="utf-8").strip()
    block = f"{BEGIN}\n{body}\n{END}\n"
    existing = rules_file.read_text(encoding="utf-8") if rules_file.is_file() else ""
    if BEGIN in existing and END in existing:
        start, rest = existing.split(BEGIN, 1)
        _, after = rest.split(END, 1)
        new = start + block + after.lstrip("\n")
        action = "UPDATE"
    else:
        new = existing + ("\n" if existing and not existing.endswith("\n") else "") + ("\n" if existing else "") + block
        action = "ADD"
    if new == existing:
        log.append(f"OK     {rules_file} rules already current")
        return
    log.append(f"{action}    {rules_file} (core rules block)")
    if not dry:
        rules_file.parent.mkdir(parents=True, exist_ok=True)
        rules_file.write_text(new, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--runtime", required=True, choices=["claude", "codex", "antigravity", "all"])
    parser.add_argument("--scope", choices=["user", "project"], default="user")
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="project root for --scope project")
    parser.add_argument("--plugins", nargs="+", default=PLUGINS, choices=PLUGINS)
    parser.add_argument("--rules", action="store_true", help="also install the core rules")
    parser.add_argument("--codex-legacy", action="store_true", help="Codex: use $CODEX_HOME/skills")
    parser.add_argument("--force", action="store_true", help="replace same-named skills not installed by this tool")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    runtimes = ["claude", "codex", "antigravity"] if args.runtime == "all" else [args.runtime]
    try:
        sources = skill_sources(args.plugins)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    log: list[str] = []
    skipped = 0
    done_dirs: set[Path] = set()
    done_rules: set[Path] = set()
    for runtime in runtimes:
        skills_dir, rules_file = targets(runtime, args.scope, args.project.resolve(), args.codex_legacy)
        log.append(f"== {runtime} ({args.scope})")
        if skills_dir in done_dirs:
            log.append(f"OK     {skills_dir} already handled (shared with another runtime)")
        else:
            skipped += install_skills(sources, skills_dir, args.force, args.dry_run, log)
            done_dirs.add(skills_dir)
        if args.rules and rules_file not in done_rules:
            install_rules(rules_file, args.dry_run, log)
            done_rules.add(rules_file)
    print("\n".join(log))
    print(f"\n{'Dry run: nothing written. ' if args.dry_run else ''}{len(sources)} skills; "
          f"{skipped} skipped. Restart the agent session so it picks up new skills.")
    return 1 if skipped else 0


if __name__ == "__main__":
    sys.exit(main())
