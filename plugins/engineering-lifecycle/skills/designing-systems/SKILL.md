---
name: designing-systems
description: Produce a technical design for a feature, service, migration or architecture change by collecting constraints, comparing real options, attacking the favourite, and recording the decision with rollout and rollback. Use when someone asks for a design doc, RFC, architecture proposal, migration plan, or "how should we build X".
---

# Designing systems

A design is a set of constraints, a target that satisfies all of them, and a safe path
from here to there. Every claim in it carries its evidence.

## Process

1. **Collect constraints into one table**: constraint, source (person, code, policy,
   data), what it rules out. Include scale, latency, cost, team skills, deadlines, and
   the deployment model (independent deploys, bundled releases, single replica, shared
   hosts), because arguments that hold in one model fail in another.
2. **Inventory what exists** for any change to a running system: each capability,
   interface, job and data set marked live, dead or unknown, with evidence. Zero usage
   counts only with a baseline showing the probe would have caught use. When the design
   **replaces a mechanism** (a renderer, script, pipeline, service), list every effect the
   old one has, by walking its code rather than from the examples at hand: each branch,
   default and fallback, and each channel it writes (files, environment, arguments,
   databases, DNS, caches). Mark each effect as failing **loudly** or **silently** if lost.
   Where two live implementations exist, diff them before choosing either as the baseline.
3. **Compare at least two options** on the same fields (see `exploring-options` if
   installed): what each achieves, cost, risk, how it's undone, evidence. Spike the
   riskiest part when argument alone can't settle it.
4. **Recommend one, tied to the constraints**, and attack it: the strongest case for the
   runner-up, the likeliest failure once built, and what evidence would overturn it.
5. **Detail the recommendation**: components, data model, APIs and contracts, failure
   modes (what happens when each dependency is slow or down), observability (logs,
   metrics, alerts), security and privacy.
6. **Walk the blast radius**: entry routes, per-environment config, storage and shared
   volumes, scheduled jobs and monitoring, multi-replica consistency, upgrade and
   rollback unit, other teams' actions, external callers. Mark each affected, not
   affected, or unknown with who can answer.
7. **Plan rollout and rollback**: flags, migration order, the smallest first step that
   proves the direction, and how to back out at each stage.
8. **Record the decision** so the next engineer knows why: context, options considered,
   decision and who made it, why (with evidence grades), consequences, and the signal
   that should reopen it. Keep it beside the code (for example `docs/decisions/`).

## Completeness check

Before calling the design complete, confirm: every constraint has a source; every
inventory item has evidence and every "dead" has a baseline; replaced effects are listed
and marked loud or silent; every blast-radius row is marked; every load-bearing claim is
graded; the recommendation was attacked and each objection ruled on; each mitigation
says when it fires, what it checks and what happens on failure; open decisions have
owners; the first step is named. A design missing a row is reported incomplete, not
padded. A "no gaps" verdict says what was enumerated and how, because a search for
missing topics cannot find a class no one listed.

## Quality bar

- Every choice traces to a constraint; every load-bearing claim is graded observed,
  inferred or unverified.
- Failure modes are named, not hand-waved.
- Decisions that belong to people (scope, cost, cross-team asks) are listed with owners.

## Output

Sections: Context and constraints, Goals and non-goals, Options, Recommendation and
challenge, Detailed design, Blast radius, Rollout and rollback, Decision, Open questions.
