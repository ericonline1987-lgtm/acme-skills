---
name: authoring-skills
description: Always use this skill when someone writes, improves or debugs an agent skill, plugin, custom command or standing instruction file — a SKILL.md, CLAUDE.md or AGENTS.md — or asks why a skill doesn't trigger or doesn't help. It starts from cases the agent fails without it, writes the description for routing, keeps the body short and specific, and proves the gain against a no-skill baseline.
---

# Authoring skills

A skill earns its place only when it loads at the right moments and an agent with it
does measurably better than one without it. Everything else is weight in the context.

## 1. Start from failures, not from a topic

- Collect three or more real tasks where the agent did worse than it should, and for
  each, what a good answer does. If the agent already does them well, the skill isn't
  needed; say so.
- Write each as an eval case: the prompt as a person would type it, one grader per
  criterion, and nothing the test harness can't provide (files, tools, network).
- Run the no-skill baseline first. Keep the cases it fails; a case the baseline passes
  can't show the skill helps.

## 2. Write the description for routing

- The description alone decides whether the skill loads. Lead with when to use it, in
  the words people use ("Use this skill whenever…", the casual phrasings, the adjacent
  tasks it covers), then one sentence on what it does that a plain answer wouldn't.
- Agents skip skills for tasks they think they can do alone. "Even a quick one" helps;
  an always-on instruction to load the matching skill helps more.
- Write trigger queries: six or more short should-fire prompts and four or more near
  misses that share keywords but need something else. Hold some out, measure recall and
  false loads, and never tune the wording on the held-out set.

## 3. Write the body

- Imperative steps an agent can check ("run X and read its output"), not virtues ("be
  careful"). Each step should change what the agent does.
- Only what the agent wouldn't do on its own; delete lines the baseline already
  follows.
- Short: aim under 500 words. Move rare procedures and long references into files
  loaded only when needed; put deterministic checks in scripts.
- Self-contained: no paths outside the skill folder; refer to other skills by name.
- Follow the format's rules: a lowercase hyphenated name matching the folder, and the
  required frontmatter, checked with the platform's validator.

## 4. Measure every change

- Run each case with and without the skill, three or more times per arm, with a capable
  judge. Check that every output exists, and that no run or judge call hit a usage
  limit, before reading a score (see `building-ai-features` for checking an eval).
- Read failing answers yourself before believing the grader; judges fail correct
  answers on literal words ("ends with", "briefly", "checks" when nothing can run).
- Change one thing at a time. Log each run with its date, result and cost.
- Every failure that escapes becomes a new case (see `capturing-learning`).

## 5. Ship

Bump the version, record the change and its measured effect, and install it in every
runtime you claim to support before saying it works there.

## Report

```
cases: <name — with skill vs without, runs per arm>
triggers: <recall on held-out should-fire queries; false loads on near misses; model>
size: <words in the body, files loaded on demand>
not measured: <runtimes, models, task types>
```
