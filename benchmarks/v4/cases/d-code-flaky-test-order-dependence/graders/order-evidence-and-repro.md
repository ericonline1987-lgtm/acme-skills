---
type: llm
weight: 1
---

Pass if this holds for the response: The response ties the failures to test order using the logs (test_tax.py ran before test_invoice.py in both failing runs and after it in the passing run) and gives a deterministic way to reproduce, such as re-running with `-p randomly --randomly-seed=2841907731` or running test_tax.py before test_invoice.py in one session.
