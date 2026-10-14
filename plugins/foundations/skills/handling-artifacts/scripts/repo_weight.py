#!/usr/bin/env python3
"""List the largest objects in a git repository's entire history, read-only.

For each of the --top largest blobs reachable from any ref, prints its size, the path
it was stored under, and whether that path still exists in HEAD. Files deleted from the
current tree but still in history are usually where repository weight really sits,
and deleting them from the tree today reclaims nothing.

Also prints the on-disk pack size (git count-objects) for before/after comparison.

It never modifies the repository. It reports sizes uncompressed, so a large text file
may weigh less on disk than shown; binaries that don't compress are shown accurately.
Rewriting history to remove objects is destructive; see SKILL.md for the safe order.

Usage:
  repo_weight.py [--repo PATH] [--top N] [--min-kb K] [--json]

Exit status: 0 on success, 2 on git error.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def git(repo: Path, *args: str, stdin: str | None = None) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], input=stdin,
                            capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {result.stderr.strip()}")
    return result.stdout


def largest_blobs(repo: Path, top: int, min_bytes: int) -> list[dict]:
    objects = git(repo, "rev-list", "--objects", "--all")
    paths: dict[str, str] = {}
    for line in objects.splitlines():
        sha, _, path = line.partition(" ")
        if path and sha not in paths:
            paths[sha] = path
    if not paths:
        return []
    batch = git(repo, "cat-file", "--batch-check=%(objecttype) %(objectname) %(objectsize)",
                stdin="\n".join(paths) + "\n")
    blobs = []
    for line in batch.splitlines():
        kind, sha, size = line.split()
        if kind == "blob" and int(size) >= min_bytes:
            blobs.append({"sha": sha[:12], "bytes": int(size), "path": paths[sha]})
    blobs.sort(key=lambda b: b["bytes"], reverse=True)
    blobs = blobs[:top]
    try:
        in_head = set(git(repo, "ls-tree", "-r", "--name-only", "HEAD").splitlines())
    except RuntimeError:
        in_head = set()
    for blob in blobs:
        blob["in_head"] = blob["path"] in in_head
    return blobs


def pack_size(repo: Path) -> dict:
    info = {}
    for line in git(repo, "count-objects", "-v").splitlines():
        key, _, value = line.partition(":")
        info[key.strip()] = value.strip()
    return {"loose_kib": int(info.get("size", 0)), "pack_kib": int(info.get("size-pack", 0))}


def human(n: int) -> str:
    for unit in ("B", "KiB", "MiB", "GiB"):
        if n < 1024 or unit == "GiB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return str(n)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--min-kb", type=int, default=0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        blobs = largest_blobs(args.repo, args.top, args.min_kb * 1024)
        sizes = pack_size(args.repo)
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"on_disk": sizes, "largest": blobs}, indent=2))
        return 0
    print(f"on disk: packs {sizes['pack_kib']} KiB, loose {sizes['loose_kib']} KiB\n")
    print(f"{'size':>10}  {'in HEAD':7}  path")
    for blob in blobs:
        print(f"{human(blob['bytes']):>10}  {'yes' if blob['in_head'] else 'NO':7}  {blob['path']}  ({blob['sha']})")
    gone = [b for b in blobs if not b["in_head"]]
    if gone:
        print(f"\n{len(gone)} of these are not in HEAD: deleted from the tree but still in history.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
