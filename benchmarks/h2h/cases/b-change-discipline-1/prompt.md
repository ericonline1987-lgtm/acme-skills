---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, browser or environment are available in this conversation, and none will be provided. Do not search for them. Answer by explaining exactly how you would carry out the request, step by step, including what you would check and what you would report.)

I want to extract a generic RequestContext abstraction. Right now only the order service uses it, but let me build it first so others can reuse it later.
