---
type: llm
weight: 1
---

Pass if this holds for the response: The plan recognises that once v2 tokens have been issued, rolling auth-service back to a build that cannot read v2 would invalidate those sessions (logging users out), and so keeps v2 validation in place on rollback — rolling back by turning off v2 issuance rather than removing v2 support — and keeps v1 validation until outstanding v1 tokens have expired (up to the 30-day refresh lifetime).
