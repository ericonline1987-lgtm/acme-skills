---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, browser or environment are available; everything you need is in this message.)

Need a rollout + rollback plan I can paste into the change ticket for Thursday's auth-service release. The release contains:

a) new session token format: v2 switches from HS256 JWTs to PASETO v4.local tokens. New tokens are issued on login and on refresh (access token 15 min, refresh token 30 days).
b) a new rate limiter on POST /login (sliding window, 10 attempts / 5 min per IP+username)
c) Postgres driver bump (pgx 5.5 → 5.7)

Setup: auth-service runs 40 pods behind the gateway, ~25M active sessions. Tokens are validated by auth-service and also by api-gateway, billing-service and notifications-service, which use our shared `authtoken` library (each service pins its own version of it). We have a feature-flag system and can canary by pod.
