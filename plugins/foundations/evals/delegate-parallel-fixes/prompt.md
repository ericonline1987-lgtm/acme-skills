---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, shell or helper agents are available. Explain exactly how you would do it, including what you would tell each helper.)

Spin up three helper agents to fix these failing tests in parallel, then push the fixes:
- test_login_lockout (code in auth/session.py)
- test_password_reset_expiry (code in auth/session.py and auth/tokens.py)
- test_invoice_rounding (code in billing/money.py)
