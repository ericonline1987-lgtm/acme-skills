---
name: designing-systems
description: Produce a technical design doc for a feature or service, covering architecture, data model, APIs, and trade-offs. Use when someone asks for a design doc, architecture proposal, RFC, or "how should we build X".
---

# Designing systems

## Process
1. **Restate requirements and constraints** (scale, latency, budget, team skills, deadlines). Ask for any that are missing and matter.
2. **Propose at least two options.** For each: a short description, a diagram (Mermaid is fine), and pros/cons.
3. **Recommend one** and say why, tied back to the constraints.
4. **Detail the recommended option:** components, data model, API surface, failure modes, and how it's observed (logs, metrics, alerts).
5. **Plan the rollout:** migration steps, feature flags, rollback path.
6. **List risks and open questions** with owners.

## Quality bar
- Every choice links to a requirement or constraint.
- Failure modes are named, not hand-waved ("what happens when the queue is down?").
- Security and data privacy are addressed explicitly, even if briefly.

## Output
Sections: Context, Goals / non-goals, Options, Recommendation, Detailed design, Rollout, Risks, Open questions.
