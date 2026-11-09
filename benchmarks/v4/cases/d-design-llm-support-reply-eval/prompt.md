---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, browser or environment are available; everything you need is in this message.)

We're shipping an LLM feature that drafts replies to customer support tickets; agents review and edit before sending. PM wants an eval we run before launch and on every prompt/model change.

What I have: 6 months of tickets (~220k) with the reply the agent actually sent, CSAT on ~15% of them, and tags (billing 41%, how-to 33%, bug 17%, account access 6%, cancellation 2.5%, abuse/harassment 0.5%).

My plan: sample 200 tickets at random, generate drafts, have GPT-4o score each draft 1–10 for "quality" compared with the agent's actual reply, ship if the mean is ≥ 7. Poke holes and give me a better design.
