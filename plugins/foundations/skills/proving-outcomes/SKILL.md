---
name: proving-outcomes
description: Use this skill whenever someone wants to say work is done, fixed, live, shipped or resolved — status updates, Slack messages, release notes — or asks to verify a change works, even when CI and the deploy are green. It reports only the rung of evidence actually reached (checked, delivered, working in real use, accepted, outcome achieved) and schedules the outcome check.
---

# Proving outcomes

"Tests pass" is not "it works", "it works" is not "they accepted it", and "they accepted
it" is not "it mattered". Name the rung you reached; never borrow a higher one.

## The ladder

| Rung | Means | Proven by | Not proven by |
|---|---|---|---|
| 1 Checked | Automated checks pass | The narrowest check that exercises the change, its real output read | A piped exit code; "all passed" while old failures remain |
| 2 Delivered | It reached its destination | Read-back from the destination: commit on the remote, version running, email in Sent, doc published | A push or send command returning 0 |
| 3 Working in real use | It does the job with real inputs where it lives | Real inputs through the user's real path, compared with the old behaviour | Synthetic samples only; internal checks only |
| 4 Accepted | The consumer confirmed it | Their confirmation through their own path | Your own screenshot; a worker's report |
| 5 Outcome achieved | The intended change in the world happened | The evidence named in the outcome contract, at the follow-up | Any lower rung |

## Process

1. **Fetch the outcome contract** (see `defining-done`). If there is none, write the
   one-line version now: the outcome and how you'd know.
2. **Lock the target.** Name the exact version, environment and address being checked.
   If the one that matters can't be reached, report that; never substitute a convenient
   look-alike and count it.
3. **Collect evidence rung by rung**, starting at 1. Read real outputs. For rung 3, take
   inputs from real use (logs, recent requests, actual documents) and include the case
   that should fail or be rejected.
4. **Record a ledger** for anything beyond a small task, in the format of
   `assets/evidence-ledger.example.json`, and run
   `python3 scripts/evidence_ledger.py <ledger.json>`. It reports the highest supported
   rung and fails on an overclaim or a missing follow-up.
5. **Schedule the outcome check.** Below rung 5, write the follow-up date, check and
   owner into the hand-off. Offer to set a reminder or scheduled task if the platform
   supports it.
6. **Hand off** with `assets/handoff-report.md`: result, rung reached
   and the next one, evidence, decisions for the person, what was not checked,
   follow-up, what was learned.

## Rules

- Report the supported rung in the first sentence of the hand-off.
- "Not checked" is never empty by omission: name what the evidence does not cover.
- Keep evidence the consumer will look at (a test upload, a probe file) until they
  confirm (see `handling-artifacts`).
- When a later rung contradicts an earlier one, the later rung wins; report the
  regression, don't explain it away.
