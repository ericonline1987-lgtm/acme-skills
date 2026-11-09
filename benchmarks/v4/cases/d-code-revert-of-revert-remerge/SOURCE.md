# Sources

- Git documentation, How to revert a faulty merge (Linus Torvalds / Junio Hamano) — https://github.com/git/git/blob/HEAD/Documentation/howto/revert-a-faulty-merge.adoc
- Git documentation, git-show — https://git-scm.com/docs/git-show

## Grader basis

- explains-history-vs-content: revert-a-faulty-merge (reverting a merge "does absolutely nothing to the effects on history"; future merges see that merge as the last shared state).
- revert-the-revert: revert-a-faulty-merge (when fixes were added on top of the side branch, you "need to do it by reverting the revert").
- no-history-rewrite: standard practice for published branches; the how-to's remedies all add commits rather than rewrite history.
- keep-fixes-in-conflicts: revert-a-faulty-merge (warns that reverting the revert is likely to conflict and must not be done blindly); the supplied conflict note shows parser.ts/upload.ts already carry the fixes.
- verify-feature-present: reading the merges' diff stats (git-show/diff); the feature's tests were part of the reverted change.

## Why a capable general model might miss it

The revert-then-remerge trap is a known but rarely encountered git behaviour; models often recommend re-merging, cherry-picking or reset-and-force-push instead of the revert of the revert.

The repository history and output are synthetic.
