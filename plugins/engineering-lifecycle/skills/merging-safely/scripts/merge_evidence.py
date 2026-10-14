#!/usr/bin/env python3
"""Collect read-only git facts for a merge and flag changes the merge may have dropped.

Before a merge (default): models the diff between the target (default HEAD) and the
source ref: merge base, commits only on each side, incoming commits, files each side
changed, and hotspots (files both sides changed, where silent logic conflicts live).

After a merge (--pre-merge-ref = the target as it was before, e.g. HEAD^1): also proves
completeness and looks for dropped changes:

  - contained:     the source tip is an ancestor of the target
  - not contained: commits on the source whose patch is not in the target (git cherry)
  - dropped?:      files only the source changed since the base must, after a plain merge,
                   be identical to the source tip. If one differs, the merge (or a later
                   commit) lost or altered the source's change. Hotspots are listed for
                   manual review instead, because there a difference is expected.

It never writes to the repository. It cannot judge whether a hotspot's resolution is
semantically right, and a "dropped?" file may be a later deliberate change on the
target; each flag is a place to look, not a verdict.

Usage:
  merge_evidence.py --repo PATH --source-ref REF [--target-ref REF]
                    [--pre-merge-ref REF] [--max-list N] [--json]

Exit status: 0 no flags, 1 flags raised (dirty worktree, not contained, dropped?),
2 git error or bad refs.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


class GitError(RuntimeError):
    pass


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, timeout=60)
    if check and result.returncode != 0:
        raise GitError(f"git {' '.join(args)}: {result.stderr.strip() or result.returncode}")
    return result.stdout.strip()


def lines(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.strip()]


def changed(repo: Path, a: str, b: str) -> set[str]:
    return set(lines(git(repo, "diff", "--name-only", a, b)))


def collect(repo: Path, source: str, target: str, pre_merge: str | None, max_list: int) -> dict:
    target_sha = git(repo, "rev-parse", "--verify", f"{target}^{{commit}}")
    source_sha = git(repo, "rev-parse", "--verify", f"{source}^{{commit}}")
    model_target = git(repo, "rev-parse", "--verify", f"{pre_merge}^{{commit}}") if pre_merge else target_sha
    base = git(repo, "merge-base", model_target, source_sha)
    left, right = git(repo, "rev-list", "--left-right", "--count", f"{model_target}...{source_sha}").split()
    incoming = lines(git(repo, "log", "--oneline", "--no-decorate", f"{base}..{source_sha}"))
    source_files = changed(repo, base, source_sha)
    target_files = changed(repo, base, model_target)
    hotspots = sorted(source_files & target_files)

    facts = {
        "repo": str(repo),
        "target": f"{target} ({target_sha[:12]})",
        "source_ref": f"{source} ({source_sha[:12]})",
        "model_target": model_target[:12] + (" (pre-merge)" if pre_merge else ""),
        "merge_base": base[:12],
        "left_right_counts": {"only_on_target": int(left), "only_on_source": int(right)},
        "incoming_commits": incoming[:max_list],
        "incoming_truncated": max(0, len(incoming) - max_list),
        "source_changed_files": sorted(source_files),
        "hotspots": hotspots,
        "worktree_dirty": lines(git(repo, "status", "--porcelain")),
        "flags": [],
    }

    contained = subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", source_sha, target_sha]).returncode == 0
    facts["source_contained_by_ancestry"] = contained
    if pre_merge:
        not_in_target = [l[2:] for l in lines(git(repo, "cherry", target_sha, source_sha)) if l.startswith("+")]
        facts["source_commits_not_in_target_by_patch"] = not_in_target
        facts["landed_files"] = sorted(changed(repo, model_target, target_sha))
        dropped = [
            path for path in sorted(source_files - target_files)
            if git(repo, "diff", "--name-only", source_sha, target_sha, "--", path)
        ]
        facts["dropped_suspects"] = dropped
        if not contained and not_in_target:
            facts["flags"].append(f"source not contained: {len(not_in_target)} commit(s) by patch")
        if dropped:
            facts["flags"].append(f"possible dropped changes in {len(dropped)} file(s) only the source changed")
        facts["hotspots_to_review"] = hotspots
    if facts["worktree_dirty"]:
        facts["flags"].append("worktree has uncommitted changes")
    return facts


def render(f: dict) -> str:
    out = [
        "Merge evidence",
        f"repo:                {f['repo']}",
        f"target:              {f['target']}",
        f"source ref:          {f['source_ref']}",
        f"modelled against:    {f['model_target']}",
        f"merge base:          {f['merge_base']}",
        f"left/right counts:   target-only {f['left_right_counts']['only_on_target']}, "
        f"source-only {f['left_right_counts']['only_on_source']}",
        "incoming commits:",
        *[f"  {c}" for c in f["incoming_commits"]],
    ]
    if f["incoming_truncated"]:
        out.append(f"  ... {f['incoming_truncated']} more not shown (residual risk: review them)")
    out.append("hotspots (both sides changed): " + (", ".join(f["hotspots"]) or "none"))
    out.append("worktree: " + ("dirty: " + ", ".join(f["worktree_dirty"]) if f["worktree_dirty"] else "clean"))
    out.append(f"contained by ancestry: {'yes' if f['source_contained_by_ancestry'] else 'no'}")
    if "landed_files" in f:
        out.append("landed files: " + (", ".join(f["landed_files"]) or "none"))
        out.append("not in target by patch: " + (", ".join(f["source_commits_not_in_target_by_patch"]) or "none"))
        out.append("DROPPED? (source-only files that differ from the source tip): "
                   + (", ".join(f["dropped_suspects"]) or "none"))
    out += [
        "",
        "Fill in by hand:",
        "  merge strategy and why:          <already contained | fast-forward | no-ff | squash>",
        "  conflicts and reasoning:          <file: why no needed behaviour from either side was lost>",
        "  semantic review of hotspots:      <per hotspot>",
        "  completeness proof method:        <ancestry | patch-equivalence | tree comparison>",
        "  tests run and real result:        <command -> result>",
        "  push status:                      <not pushed | pushed at user's request>",
        "  residual risks:                   <anything skipped or unverified>",
        "",
        "flags: " + ("; ".join(f["flags"]) if f["flags"] else "none"),
    ]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--source-ref", required=True)
    parser.add_argument("--target-ref", default="HEAD")
    parser.add_argument("--pre-merge-ref", help="the target before the merge (post-merge audit)")
    parser.add_argument("--max-list", type=int, default=30)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        facts = collect(args.repo, args.source_ref, args.target_ref, args.pre_merge_ref, args.max_list)
    except (GitError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(facts, indent=2) if args.json else render(facts))
    return 1 if facts["flags"] else 0


if __name__ == "__main__":
    sys.exit(main())
