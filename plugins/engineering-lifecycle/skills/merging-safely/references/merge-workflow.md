# Merge workflow, command by command

Read this for any non-trivial merge, a readiness check, or an audit of a merge already
done. `SKILL.md` gives the order; this gives the commands and the decisions at each step.

**Contents:** 1. Scope and a clean tree · 2. Pin the refs · 3. Model the diff · 4. Hotspots · 5. Choose the strategy · 6. Resolve conflicts · 7. Prove completeness · 8. Verify and gate the push · 9. Undoing a merge

## 1. Scope and a clean tree

```bash
git rev-parse --show-toplevel      # really a repository, and which one
git status --short --branch
git worktree list
git remote -v
```

| Working tree | Do |
|---|---|
| Clean | Continue |
| Dirty, and the changes touch files the merge touches | Stop; agree an isolation plan with the person (a separate worktree, or they commit first) |
| Dirty, apparently unrelated | Say so, then decide with them; still prefer a separate worktree |
| Changes you didn't make | They're the person's. Never stash, reset or check out over them silently |

`git diff --stat` and `git diff --cached --stat` show what the dirty changes are.

## 2. Pin the refs

```bash
git fetch origin <source-branch>
git rev-parse HEAD
git rev-parse origin/<source-branch>
```

Merge `origin/<branch>` after a fetch, not a local branch of the same name that may be
weeks old. Record both commit ids in the report; "the latest main" is not a ref.

## 3. Model the diff

```bash
BASE=$(git merge-base HEAD <source>)
git rev-list --left-right --count HEAD...<source>     # commits only on each side
git log --oneline HEAD..<source>                      # what's incoming
git log --oneline --left-right --cherry-pick --no-merges HEAD...<source>   # patches already on both sides
```

- **Rebased or squashed history**: commit ids differ even when content matches. Compare
  patches with `git range-diff "$BASE"..HEAD "$BASE"..<source>` before concluding that
  anything is missing.
- **Parallel release lines**: the same fix often lands on each line as a different
  commit under a different ticket, and the lines may share no merge base. Decide "does
  this line have the fix?" by content, never by commit id:
  `git show <branch>:<path> | grep -n '<distinctive line of the fix>'`, or
  `git diff <branch> <known-fixed-ref> -- <path>`. To port it, check the target has the
  same file and structure before any `cherry-pick`.

`python3 scripts/merge_evidence.py --repo . --source-ref <source> [--target-ref <target>]`
collects all of this in one read-only run.

## 4. Hotspots

Files changed on both sides since the base are where silent logic conflicts live, even
when git merges them cleanly:

```bash
comm -12 <(git diff --name-only "$BASE" HEAD | sort) <(git diff --name-only "$BASE" <source> | sort)
```

Rank them, highest risk first: configuration and defaults; schemas and migrations;
dependency manifests and lockfiles; initialisation and wiring (startup, dependency
injection, routing tables); authorisation; shared constants and enums; tests whose
assertions changed. For each, read both sides' changes since the base and walk
`post-merge-patterns.md`.

## 5. Choose the strategy

| Situation | Check | Do |
|---|---|---|
| Source already contained | `git merge-base --is-ancestor <source> HEAD` succeeds | Nothing to merge. Report "already contained", with the check |
| Fast-forward possible | `git merge-base --is-ancestor HEAD <source>` succeeds | Review incoming first, then `git merge --ff-only <source>`, or `--no-ff --no-commit` if the project keeps merge commits |
| Real merge | Neither | `git merge --no-ff --no-commit <source>`, inspect the staged result, then commit |
| Readiness check or merge-request review | Any | Trial merge in a disposable worktree (below); the answer is a verdict, not a merge |

```bash
trial=$(mktemp -d)
git worktree add --detach "$trial/wt" <target>
git -C "$trial/wt" merge --no-ff --no-commit <source>
git -C "$trial/wt" diff --name-only --diff-filter=U      # conflicts
git -C "$trial/wt" diff --cached --stat                  # what would land
git worktree remove --force "$trial/wt" && rmdir "$trial" && git worktree list
```

A clean trial merge proves git can merge it, nothing more; the hotspot review decides
the verdict. `git merge --no-edit` as the default path is how changes get lost
unreviewed.

## 6. Resolve conflicts

```bash
git config merge.conflictStyle zdiff3   # shows the base inside each conflict
git diff --name-only --diff-filter=U
git show :1:<file>   # base
git show :2:<file>   # ours
git show :3:<file>   # theirs
```

- For each conflict, write down what the base had, what each side changed, and why the
  result keeps, combines or drops each change. "Took ours" is a decision that needs a
  reason, and it usually drops the other side's work.
- **Lockfiles and generated files**: don't hand-merge. Take one side, then regenerate
  (`npm install`, `poetry lock --no-update`, the code generator) from the merged
  manifest, and review the regenerated diff.
- **Migrations**: two branches that each added migration number 0042 conflict at run
  time, not in git. Renumber one, and check the order still makes sense.
- **Renames**: a file renamed on one side and edited on the other can come through as a
  delete plus an untouched copy. Check `git diff --cached -M --stat` for the rename and
  confirm the edits landed in the new path.
- **Submodules and pinned versions**: a conflict in a pointer means two different
  versions; pick one deliberately and confirm that commit exists on the remote.
- After resolving: `git diff --check` for leftover markers and whitespace, and a grep
  for `<<<<<<<` in files git didn't flag (generated files, docs).
- `git rerere` remembers resolutions for repeated merges of the same branches; turn it
  on for long-running integration work.

## 7. Prove completeness

For a merge commit:

```bash
git merge-base --is-ancestor <source> HEAD && echo contained
git log --oneline HEAD..<source>           # must be empty
git diff --stat HEAD^1 HEAD                # what landed
python3 scripts/merge_evidence.py --repo . --source-ref <source> --pre-merge-ref HEAD^1
```

The script's **dropped?** list is the check ancestry can't do: files only the source
changed that no longer match the source tip, which is what a conflict resolved by
taking one side wholesale leaves behind.

For a fast-forward or a squash, save the pre-merge head first
(`PRE=$(git rev-parse HEAD)`), because `HEAD^1` is not the old target.

**Squash merges** aren't ancestors, so ancestry proves nothing. Use one of these and name
it in the report:

1. **File state over every path the source changed** (the default):
   `git diff -z --name-only "$BASE" <source> | xargs -0 -r git diff --name-status HEAD <source> --`.
   Any path listed must be explained by a target-side change; `A` means a file the
   source added is missing, `D` a file it deleted is still there, `M` content that
   didn't land.
2. **Whole-range patch id**: `git show <squash> | git patch-id --stable` against
   `git diff "$BASE" <source> | git patch-id --stable`. Equal proves an exact squash;
   unequal is inconclusive (conflict resolutions differ legitimately), so fall back to 1.
3. **Cherry-pick no-op**, in a disposable worktree only: cherry-pick the source commits
   onto HEAD with `--no-commit`; if both `git diff --cached --quiet` and
   `git diff --quiet` pass, nothing was missing. A conflict here is inconclusive.

## 8. Verify and gate the push

Run the build and the tests that cover the hotspots, and the post-merge pipeline step
most likely to fail (migrations, config validation, startup). Then
`git status --short --branch` once more. Push only when the source is contained and
complete, the hotspot review passed, the checks passed, and the person asked for the
push.

## 9. Undoing a merge

- Reverting a merge commit (`git revert -m 1 <merge>`) undoes its content but leaves
  the source's commits in history. Merging the same branch again later brings in only
  commits made after the revert; the reverted work stays out until you revert the
  revert. Say this whenever you revert a merge.
- On a shared branch, revert rather than reset; resetting rewrites history others have.
- `git cherry-pick -x` records where a ported commit came from; use it on release lines
  so the next audit can trace it.
