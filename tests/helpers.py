"""Shared helpers for the offline test suite (standard library only)."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = ROOT / "plugins"

# Budgets from docs/PLAN.md, section 2.
DESCRIPTION_MAX_CHARS = 400
BODY_MAX_WORDS = 900
NAME_MAX_CHARS = 64


def plugin_dirs() -> list[Path]:
    return sorted(p for p in PLUGINS_DIR.iterdir() if (p / ".claude-plugin" / "plugin.json").is_file())


def skill_dirs(plugin: Path | None = None) -> list[Path]:
    plugins = [plugin] if plugin else plugin_dirs()
    return sorted(s for p in plugins for s in (p / "skills").iterdir() if (s / "SKILL.md").is_file())


def all_skill_names() -> set[str]:
    return {s.name for s in skill_dirs()}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def split_frontmatter(text: str) -> tuple[list[str], str]:
    """Return (frontmatter lines, body). Raises ValueError if absent."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("file does not start with '---'")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index], "\n".join(lines[index + 1:])
    raise ValueError("frontmatter is not closed")


def parse_simple_frontmatter(lines: list[str]) -> dict[str, str]:
    """Parse flat `key: value` frontmatter, the only shape this repo uses.

    Values are kept as raw strings; callers check the rules they care about.
    """
    fields: dict[str, str] = {}
    for line in lines:
        if not line.strip():
            continue
        match = re.match(r"^([A-Za-z_][\w-]*):\s?(.*)$", line)
        if not match:
            raise ValueError(f"not a flat key: value line: {line!r}")
        fields[match.group(1)] = match.group(2)
    return fields


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module
