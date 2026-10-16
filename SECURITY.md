# Security

These plugins contain instructions for an AI agent and Python scripts that run on your machine. The scripts use only the standard library, make no network calls, and only read from git repositories (none of them writes to a repository).

## Reporting a problem

If you find a skill that could lead an agent to leak data, follow instructions hidden in untrusted content, or take an irreversible action without asking, or a script that does something its docstring doesn't say, report it privately through this repository's **Security → Report a vulnerability** page rather than in a public issue.

Please include the skill or script, the prompt or input that triggers the problem, and what happened.

## Before installing any skill set

Read the SKILL.md files and scripts first, as you would any code you run. `claude plugin eval` runs a plugin's eval suite on your machine as you; only run suites you trust.
