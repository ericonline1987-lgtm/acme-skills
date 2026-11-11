# Plan v1.1: full coverage of the reference set, then measured

**Bottom line:** v1.0 covers four of the six skills in `ly87ing/agent-skills` (the reference set) [observed: side-by-side reading on 2026-10-13]. It goes beyond them on outcomes, trust and learning. It has two real gaps (browser and UI evidence; file and artifact handling), thinner detail in three places, and no always-on rules. v1.1 closes every gap and keeps the always-on cost flat by putting detail in reference files. It then settles "is it better?" by running both skill sets on the same cases, including cases written by the reference set's own author.

## 1. Parity matrix

| Reference skill | v1.0 coverage | v1.1 work |
|---|---|---|
| verification (browser half) | Gap | New skill `verifying-interfaces` (engineering-lifecycle), with Playwright and rendered-surface references and an SVG validator |
| artifact-hygiene | Gap | New skill `handling-artifacts` (foundations), with a repo-weight script |
| change-discipline facets | Core only | `changing-code/references/boundaries.md` and `style-and-validation.md`, loaded only when the change has that dimension |
| safe-merge-review | Mostly | `merging-safely/scripts/merge_evidence.py`, `references/post-merge-patterns.md`, merge-request resolution, per-repo multi-repo reporting |
| reader-facing-writing | Partial | `writing-documents/references/skeletons.md` (README, release notes, QA hand-off, agent instruction file), `references/figures-and-html.md`, `scripts/doc_check.py` |
| solution-shaping | Mostly | Mechanism inventory (each effect marked loud or silent) and a completeness check in `designing-systems` and `exploring-options` |
| rules/core.md | Gap by design | New optional plugin `core-rules`: a short rules file injected at session start, measured with the same eval harness as the skills |

## 2. Design rules (unchanged from v1.0, restated because they bind this work)

- Detail goes into reference files; SKILL.md bodies stay at or under 900 words and descriptions at or under 400 characters.
- References stay inside their plugin. Cross-plugin mentions use skill names only.
- Every new skill gets a should-fire eval case; every plugin keeps should-not-fire cases.
- Every new script uses only the standard library, documents what it cannot check, and has unit tests.
- Ideas from the reference set are rewritten in our own words and structure; nothing is copied.

## 3. Measurement

**Head-to-head.** Two bundles, built outside the repo for the run only: all our skills in one test plugin, all reference skills in another. Both run the same two case pools:

| Pool | Source | Cases | Why |
|---|---|---|---|
| A | Our should-fire cases | 19 + 2 new | Tests the goals we set |
| B | The reference set's own should-trigger cases, 2 per skill | 12 | Tests the goals they set, so the comparison is not rigged in our favour |

Scoring uses outcome graders only (trigger graders name skills differently in each bundle). Our bundle runs with the no-plugin baseline arm; the reference bundle runs plugin-only, since the baseline is shared.

**Gate for calling v1.1 better:** ours scores at least as high as the reference set on pool B (their ground) and higher on pool A, with no new false triggers. If ours loses on pool B, the losing cases become eval cases and the skill is fixed before release.

## 4. Usage budget

The person has a fixed usage quota and does not plan to raise it, so:

- All offline work first; paid eval runs last, one run per case (indicative), concurrency at most 8.
- [estimate] Head-to-head about $15; new-skill and rules cases about $5.
- If any run reports a usage or rate limit, stop immediately, record where the work stopped, and resume later rather than retry in a loop.
- The release-gate run (3 runs per case) stays the person's call.

## 5. Order of work

1. Deepen existing skills (offline).
2. Add `verifying-interfaces` and `handling-artifacts` (offline).
3. Add `core-rules` (offline), then one cheap run to confirm session-start injection works in the eval harness.
4. Unit tests and eval cases for everything new (offline).
5. Head-to-head runs (paid, quota-aware).
6. Fix any case where ours loses, then document, version to 1.1.0 and deliver.

## 6. Status (2026-10-14)

Done. Every row of the parity matrix is built and tested. The gate passed: ours matched or beat the reference on every one of its own author's cases (5 of 12 against 3 of 12), and scored higher on ours. The one case that exposed a gap led to a fix in `changing-code`. `core-rules` showed +0.12 mean lift from one rule [observed] and stays optional. Details: `benchmarks/RESULTS.md`.

## 7. Decisions that are yours

- Whether to install `core-rules` by default (it adds text to every session).
- Whether to run the release-gate eval after v1.1 is delivered.
