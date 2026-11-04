---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, shell or web access is available. Answer by writing what was asked for, or by explaining exactly what you would do.)

Rename the `users.email` column to `users.primary_email` in our Postgres database. A Rails app with three replicas reads and writes it. Give me the migration.
