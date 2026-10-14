---
name: merging-safely
description: Merge a branch, or judge whether one is ready to merge, and prove the result is complete and correct rather than merely conflict-free — model the diff, review files both sides changed, resolve conflicts from three-way evidence, and gate the push. Use when merging branches, resolving conflicts, auditing a past merge, or checking a fix landed on a release line.
---

# Merging safely

"Git merged it" and "the merge is right" are different claims. Prove the second.

## 1. Stabilise

- `git status --short --branch`, `git rev-parse --abbrev-ref HEAD`, `git worktree list`.
  Confirm you are on the branch the person named; don't trust a prompt or status line.
- A dirty worktree is not merged into by default: state the risk and ask.
- Pin the source ref and remote exactly. If unclear, ask; never guess "the latest".
- Given a merge-request or pull-request link, resolve it first: read its source branch,
  target branch and current head commit (`gh pr view <n> --json headRefName,baseRefName,headRefOid`,
  or `glab mr view`). Review that head commit, not the title; the request may have been
  retargeted or force-pushed since it was opened.

## 2. Model the diff

Fetch the source, then run the read-only evidence script:

```
python3 scripts/merge_evidence.py --repo <path> --source-ref <ref> [--target-ref <ref>]
```

It reports the merge base, commits only on each side, incoming commits, and hotspots
(files both sides changed, where silent logic conflicts live). If history was rebased
or squashed, also compare patches (`git cherry`, `git range-diff`) rather than ids.

## 3. Review hotspots before merging

For each hotspot, read both sides' changes since the base and walk the patterns in
`references/post-merge-patterns.md`: half-generalised branches, new options without
defaults, incomplete initialisation, code merged without its configuration, missing
companion changes, weakened tests, one side winning wholesale, renames under the other
side.

## 4. Merge reviewably

- For a readiness check, trial-merge in a disposable worktree
  (`git worktree add <tmp> HEAD && git -C <tmp> merge --no-commit <source>`), never in
  the person's tree, then remove it.
- For a real merge of anything non-trivial: `git merge --no-ff --no-commit <source>`,
  inspect the staged result, then commit.
- Resolve each conflict from base, ours and theirs (`git show :1:f :2:f :3:f`), and note
  why no needed behaviour from either side was lost.

## 5. Prove completeness

- Re-run the script with `--pre-merge-ref <target before the merge>` (`HEAD^1` for a
  merge commit). It proves containment by ancestry and by patch, lists the landed files,
  and flags **dropped?** files: files only the source changed that no longer match the
  source tip. Ancestry checks pass in that case, so this is the check that catches a
  conflict resolved by taking one side wholesale.
- For squash merges, ancestry doesn't apply: compare the tree diff or patch equivalence
  and say which method you used.
- On parallel release lines, the same fix may land under a different commit id; judge by
  content, not ids.
- Run the tests that cover the hotspots and the post-merge pipeline step that could fail.

## 6. Gate the push

Push only when asked. If the merge references something published elsewhere (a package,
submodule pin, skill), confirm it exists on the exact ref that will be resolved.

## Several repositories

When corresponding branches must be merged across a set of repositories, run every step
per repository, merge in dependency order (libraries before their consumers), and report
per repository. Never summarise a set as "all merged fine"; one repository that lacks a
source ref, context or a test command stops the set until resolved.

## Report

repo · target · source ref · merge base · left/right counts · hotspots · conflicts and
reasoning · completeness proof and method · tests run · push status · residual risks.
A readiness check ends **green / yellow / red** with "merge as is", "merge after named
fixes", or "do not merge".
