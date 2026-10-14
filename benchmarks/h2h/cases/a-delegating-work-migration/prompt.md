---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

I'm going to hand three parts of a data migration to three AI agents running in parallel: (1) export data from our old MySQL database, (2) transform it to the new schema, (3) load it into the new Postgres database. Write the instructions you'd give each agent, and tell me how you'll know their work is actually right.
