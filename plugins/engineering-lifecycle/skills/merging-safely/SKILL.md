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

## 2. Model the diff

```
git fetch <remote> <branch>
base=$(git merge-base HEAD <source>)
git rev-list --left-right --count HEAD...<source>     # commits only on each side
git log --oneline $base..<source>                      # incoming commits
comm -12 <(git diff --name-only $base HEAD | sort) <(git diff --name-only $base <source> | sort)   # hotspots
```

Hotspots (files both sides changed) are where silent logic conflicts live. If history
was rebased or squashed, compare patches (`git cherry`, `git range-diff`) rather than ids.

## 3. Review hotspots before merging

For each hotspot, read both sides' changes since the base and ask: does either side
rely on something the other removed, renamed, reordered or re-defaulted? Pay most
attention to initialisation order, config defaults, shared interfaces and schemas.

## 4. Merge reviewably

- For a readiness check, trial-merge in a disposable worktree
  (`git worktree add <tmp> HEAD && git -C <tmp> merge --no-commit <source>`), never in
  the person's tree, then remove it.
- For a real merge of anything non-trivial: `git merge --no-ff --no-commit <source>`,
  inspect the staged result, then commit.
- Resolve each conflict from base, ours and theirs (`git show :1:f :2:f :3:f`), and note
  why no needed behaviour from either side was lost.

## 5. Prove completeness

- `git merge-base --is-ancestor <source> HEAD` and `git log HEAD..<source>` is empty.
- For squash merges, ancestry doesn't apply: compare the tree diff or patch equivalence
  and say which method you used.
- On parallel release lines, the same fix may land under a different commit id; judge by
  content, not ids.
- Run the tests that cover the hotspots and the post-merge pipeline step that could fail.

## 6. Gate the push

Push only when asked. If the merge references something published elsewhere (a package,
submodule pin, skill), confirm it exists on the exact ref that will be resolved.

## Report

repo · target · source ref · merge base · left/right counts · hotspots · conflicts and
reasoning · completeness proof and method · tests run · push status · residual risks.
A readiness check ends **green / yellow / red** with "merge as is", "merge after named
fixes", or "do not merge".
