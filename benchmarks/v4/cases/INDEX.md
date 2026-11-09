# Pool D — index

24 cases. Each case directory holds `prompt.md`, `graders/*.md` (3–5 single-criterion LLM graders), `rubric.md` (pairwise-judge description) and `SOURCE.md` (public sources, per-grader basis, why a general model may miss it). All case material (code, logs, numbers, notes, people, companies) is synthetic.

| Case | Area | Specialist point targeted |
|------|------|---------------------------|
| d-writing-decline-key-account | writing | Saying no to a top customer up front and without false hope ("we'll revisit"), while turning the reply toward real alternatives for her Q2 rollout; no stock filler or invented concessions |
| d-writing-rewrite-ai-announcement | writing | De-AI-ing an announcement means restructuring (deadline and actions first), not swapping synonyms; keep every fact, add none |
| d-writing-outage-customer-email | writing | Translate engineer notes for salon owners: local time not UTC, no jargon, and surface the consequence they care about (their clients may have missed appointments; we can't tell which) |
| d-writing-exec-summary-cfo | writing | BLUF for a CFO, and flagging that the headline BigQuery saving rests on stale volumes (+40% since) rather than reporting it as fact |
| d-writing-launch-post-offline-mode | writing | A launch post that "pops" through specifics, not hype; keeps limitations and the last-sync-wins conflict rule; no invented quotes or stats |
| d-writing-reply-upset-colleague | writing | Owning both specific mistakes plainly, repairing them (public credit; correcting the date with the VP himself) without therapy-speak or pushing the overworked team |
| d-visuals-chart-truncated-bars | visuals | Rejecting truncated bar axes in favour of dot/slope charts; spotting the tiny-denominator warehouse that distorts the comparison |
| d-visuals-board-update-storyline | visuals | Answer-first board storyline with action titles, bad news early, and asks tied to the churn-by-segment evidence |
| d-visuals-oncall-dashboard-spec | visuals | SLO symptoms first, percentiles not averages, multi-window burn rate, drill-down to causes with deploy markers, and pruning the 46 panels |
| d-visuals-signup-page-a11y-review | visuals | Quantified contrast failures incl. white-on-brand-green button, zoom-blocking viewport/reflow, div-as-button, colour-only error, content-box input overflow |
| d-visuals-refund-flow-diagram | visuals | Diagram that shows the async 202 boundary, all three provider outcomes, the conditional webhook reconciliation, and specific edge labels |
| d-design-rename-column-live-table | design | Rename vs rolling deploy (expand/contract), NOT NULL via NOT VALID check, concurrent unique index, case-duplicate failure leaving INVALID index, lock_timeout and the lock queue |
| d-design-api-enum-old-mobile-clients | design | A new enum value breaks strict Codable/Moshi decoders on never-updated apps; gate by version; keep `total`; CAD amounts shown as dollars on old apps |
| d-design-webhook-credit-idempotency | design | DB-enforced dedupe atomic with the credit, racy `+=`, partial/out-of-order refunds, async ack, and repairing the 37 affected balances |
| d-design-price-cache-flash-sales | design | Key dimensions, display-only cache with authoritative checkout, pre-loading scheduled sale prices, stampede at 12:00:00, cold/failed cache vs a backend that can't take the load |
| d-design-token-format-rollout | design | Validators before issuers for a new token format; rollback = flag off, not redeploy; unbundled changes; numeric abort criteria; rate limiter in shadow mode |
| d-design-llm-support-reply-eval | design | Stratify rare high-risk categories, calibrate the LLM judge against humans, specific failure-mode criteria not similarity to agent reply, non-averaging ship gate, online agent-edit signal |
| d-code-review-keyset-pagination | code | Cursor on non-unique created_at skips rows — certain here because batch inserts share one now() per transaction; compound (created_at, id) cursor and matching index; API contract break |
| d-code-review-retry-charge | code | Retrying a non-idempotent charge double-charges; idempotency key must be stable across attempts; only retry transient errors; retry budget exceeds the LB timeout |
| d-code-flaky-test-order-dependence | code | Order-dependent failure via lru_cache surviving monkeypatch; reproduce with the seed; refuse reruns; fix isolation |
| d-code-fix-hides-cached-failure | code | The None-guard patch hides a memoised failure (lru_cache caching None for hours per pod) and converts money at 1:1; successful rates never expire either |
| d-code-merge-conflict-both-intents | code | Keep both sides' rules, cap the discount in the same currency, and fix the semantic conflicts in files git merged cleanly |
| d-code-merge-dropped-fix-audit | code | A fix "in history" but dropped by conflict resolution; why log/--contains and `git show` of a merge mislead; first-parent diff and --remerge-diff to audit; port to refactored code |
| d-code-revert-of-revert-remerge | code | Re-merging after reverting a merge brings only new commits; revert the revert (keeping the fixes on conflict), no force-push on shared main |

## Counts

- writing: 6
- visuals: 5
- design: 6
- code: 7
