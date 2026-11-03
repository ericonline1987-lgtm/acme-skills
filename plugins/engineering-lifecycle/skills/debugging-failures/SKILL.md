---
name: debugging-failures
description: Always use this skill when something is broken, failing or behaving oddly and the cause isn't known yet — an error, a crash, a flaky test, a slow page, "it worked yesterday", a production incident — even if a fix seems obvious. It mitigates live harm first, reproduces the failure, proves the cause with evidence before changing code, and for incidents keeps a timeline and writes the follow-up.
---

# Debugging failures

A fix for the wrong cause ships a second bug and hides the first. Find the cause, prove
it, then change the code (see `changing-code`).

## 1. If people are affected now, stop the harm first

- Mitigate before diagnosing: roll back the last change, turn the flag off, fail over,
  or route around. Rolling back the most recent deploy is usually the fastest safe move.
  Anything destructive or outward-facing needs the person's go-ahead
  (see `guarding-agent-actions`).
- Name one person who leads and one who updates affected people, even if both are you.
- Start a timeline now: time with zone, what was seen, what was done, by whom. Written
  as it happens, it is evidence; reconstructed later, it is a story.

## 2. Reproduce

- Get the exact error text, input, version, environment and time. Quote errors; don't
  paraphrase them.
- Reproduce with the smallest case. If you can't, list every difference between where
  it fails and where it works (data, config, versions, load, parallelism, time).
- For intermittent failures, run it many times and record the failure rate. One pass
  proves nothing; a retry that makes it pass hides it.

## 3. Narrow the cause

- Ask what changed: deploys, config, dependencies, data, traffic, other teams, and the
  calendar (expiring certificates, clock changes, month end). Use deploy history,
  `git log --since`, and `git bisect` between a known good and a known bad version.
- Read from the first error forward. Later errors are usually consequences.
- One hypothesis at a time, each with a check that would disprove it. Run the check,
  record the result, change one thing at a time.
- After three disproved hypotheses, stop guessing fixes. Widen the search instead:
  add logging, compare a good and a bad case side by side, or bisect.
- Call something the cause only with two independent lines of evidence, for example a
  reproduction that fails without the fix and passes with it, plus the log line or
  code path that explains why.

## 4. Fix and prevent

- Fix the cause, not the symptom. Write the test that fails first (see `writing-tests`).
- Look for the same cause elsewhere: the same pattern, other callers, other services.
- Say what would have caught it sooner: an alert, a test, a check in review.
- Remove temporary workarounds (retries, disabled checks) once the real fix is in.

## Report

```
symptom: <exact error, where, since when>   impact: <who, how many, how long>
cause: <statement> [observed | inferred], evidence: <the two lines of evidence>
fix: <change>, verified by: <check>; same cause checked in: <places>
not verified: <what remains>   prevention: <alert, test or check, with owner>
```

For an incident, add the review: impact in one line, the timeline, the cause, what
helped, and actions each with one owner and a date. Describe what the system allowed,
not who slipped; blame stops people reporting the next one.
