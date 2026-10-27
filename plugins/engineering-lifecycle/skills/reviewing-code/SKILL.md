---
name: reviewing-code
description: Always use this skill when someone shares code, a diff, a patch or a pull request and wants any opinion on it — "review this", "is this OK", "anything wrong", "look over my changes" — even a few lines that look fine at a glance. It confirms each finding before reporting it, checks callers, history, project rules and tests, and ends with grouped findings and a merge recommendation.
---

# Reviewing code

A review answers one question: what could go wrong if this goes in, and has anything
checked for it? Report only what you can show. A false finding costs the author time and
costs every later finding its credibility.

## 1. Frame the review

- **Intent.** Read the description and linked issue, and restate the change's outcome
  in one sentence. If you can't, ask before reviewing.
- **Risk tier**, decided by what the change touches, not by who wrote it:

  | Tier | Touches | Depth | Human approval |
  |---|---|---|---|
  | Low | Docs, copy, tests only, additive code behind an off-by-default flag | One pass | Not required |
  | Medium | Normal product code, caching, config | All passes below | One person |
  | High | Auth, billing and money, data deletion or migration, security controls, CI/CD and release workflows, auto-updaters, shared code many others copy | All passes, plus history on every changed line | Two people, or a named owner |

- **Project rules.** Find the rules files for the changed paths (CLAUDE.md, AGENTS.md,
  REVIEW.md, CONTRIBUTING.md) in the root and each changed file's directories. A rule
  applies only to files under its directory.
- **Round.** First review or re-review? See section 4.

## 2. Find: separate passes, each with one job

Run each pass on its own: with helper agents, give each to a fresh one with the title,
description and diff; otherwise do them in turn without letting one steer the next.

1. Bugs in the diff. Code that won't compile or parse, unresolved names, and logic
   that is wrong for any input.
2. Problems the change introduces. Wrong behaviour on edge cases (empty, null, huge,
   concurrent, repeated), broken error handling, security (validation, injection,
   authorisation, secrets in code or logs, unsafe deserialisation, new dependencies).
3. What it touches. Grep callers of every changed signature, config key or contract;
   run `git log -L` on changed lines to catch a past fix being undone (high tier: every
   changed line).
4. Project rules. Each violation quotes the exact rule and names its file.
5. Tests. Would a test fail if the change were reverted? New behaviour with no test at
   all is a finding; a missing edge case in otherwise tested code is a should-fix.

## 3. Confirm before you report

Every candidate finding gets a separate check before it reaches the author: re-read the
code it cites, follow the path, run it where you can. With helper agents, give each
finding to one that didn't find it, with only the claim and the code, and ask whether
it is real. Drop anything not confirmed.

Never report these:

- Problems that were already there before this change. Mention one in a single line
  under "Noticed, out of scope" only if it is serious.
- Style, naming and formatting preferences, and anything a linter or type checker
  already enforces.
- Pedantic points a senior engineer wouldn't raise.
- Generic advice ("consider adding tests", "think about security") with no specific
  failure behind it, unless a project rule requires it.
- Issues the code deliberately silences (a lint-ignore with a reason).
- Things that look wrong but are correct. If you can't tell, read more context or say
  you couldn't verify it. Don't report a guess as a finding.

## 4. Keep re-reviews converging

- From the second round on, review only what changed since the last round, plus
  anything those changes affect.
- Never repeat a finding. If one is still open, say "still open" with a link to the
  first comment.
- Name the bug class, not just the instance ("every handler builds SQL with string
  formatting"), so the author fixes all of them at once.
- Round three is the limit. If confirmed blocking findings are still appearing,
  stop line-editing: say the approach may be wrong, and suggest what to rethink.
- A fix that changes a name, an order, an identity or a concurrency property is a new
  design decision. Review it as one.

## 5. Report

Group confirmed findings by severity, each with file and line:

- **Blocking**: confirmed bugs, security issues, new behaviour with no test at all,
  undone past fixes, quoted rule violations.
- **Should fix**: confirmed problems that will cost time later.

Each finding says what's wrong, why it matters, and a fix. Include a ready-to-apply
suggestion only when applying it fixes the problem completely. Otherwise describe the
fix. One comment per issue. Comment on the code, not the author.

Keep two short sections apart from the findings: Suggestions (optional improvements,
only if the person asked for a thorough review) and Noticed, out of scope. If nothing
was confirmed, say so plainly: "No confirmed issues. Checked: bugs, introduced risks,
callers and history, project rules, tests."

## 6. Recommendation, not approval

End with **merge**, **merge after fixes**, or **don't merge yet**, the risk tier, and
what you verified yourself (ran tests, ran the code, read only) versus didn't check.
This is a recommendation: an agent's review never replaces the human approval the tier
requires, and the person who asked for the change owns the outcome.

## After the review

When a bug escapes review, add it as an eval case (see `capturing-learning`), so every
later change to this skill is checked against it.
