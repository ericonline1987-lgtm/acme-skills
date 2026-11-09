# Sources

- Git documentation, git-show (diff formatting for merges: --cc dense-combined, --remerge-diff, first-parent) — https://git-scm.com/docs/git-show
- Git documentation, How to revert a faulty merge (merges affect history separately from data) — https://github.com/git/git/blob/HEAD/Documentation/howto/revert-a-faulty-merge.adoc

## Grader basis

- diagnosis: git merge semantics — a merge's tree is whatever the resolver committed; ancestry is recorded regardless (revert-a-faulty-merge on history vs data).
- why-git-misleads: git-show docs (dense-combined omits hunks where the merge result picks one parent's version unchanged; first-parent diff shows what the merge introduced to the mainline).
- port-to-new-structure: practice of fixing shared history with new commits rather than rewriting a pushed merge (revert-a-faulty-merge's approach of adding commits); code moved by the PRJ-1190 refactor (from the supplied stat).
- audit-other-changes: git-show docs (--remerge-diff re-runs the merge and diffs it against the recorded result).

## Why a capable general model might miss it

"The commit is in history but the change is missing" is counter-intuitive, and models usually jump to cherry-pick without explaining evil/lossy merge resolution or giving a way to audit the rest of the merge.

The repository history and output are synthetic.
