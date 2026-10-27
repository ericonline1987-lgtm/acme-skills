# Shrinking a repository grown heavy with binaries

Classify media by role: keep maintained, reviewable assets under the project's policy
(for example Git LFS); keep generated, sensitive or oversized files out of history.
Deleting a file today doesn't shrink history. To reclaim space, in this order:

1. Diagnose: `python3 scripts/repo_weight.py --repo <path>` (paths are relative to the
   skill folder) lists the largest objects in all history and whether each is still in
   the current tree. Old deleted binaries are usually the real weight.
2. Back up outside the repo: `git bundle create <path> --all` and `git bundle verify <path>`.
3. Show the person exactly which paths will be removed; wait for an explicit yes.
4. Rewrite with `git filter-repo`, naming only the diagnosed paths.
5. Re-run step 1 and confirm the weight is gone and nothing else was.
6. Agree the force-push with everyone who uses the repository; every clone must re-clone,
   and an old clone pushed back restores what was removed.

The same procedure removes a committed secret from history, but rewriting is not enough
on its own: revoke and replace the secret first, because any existing clone, fork or
cache still has it.
