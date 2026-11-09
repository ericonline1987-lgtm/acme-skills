---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, browser or environment are available; everything you need is in this message.)

Write me a spec for the on-call dashboard for checkout-service — the one the page links to. Current one has 46 panels and nobody uses it during incidents.

What we have in Prometheus:
- http_requests_total{route, method, code}
- http_request_duration_seconds (histogram) {route, method}
- payment_provider_requests_total{provider, outcome}   # provider = adyen | stripe | paypal
- payment_provider_latency_seconds (histogram) {provider}
- db_pool_in_use, db_pool_max
- kafka_consumer_lag{topic}   # order-events
- node_cpu_seconds_total, node_memory_*, kube_pod_container_status_restarts_total
- deploy events are in Grafana annotations already

SLOs (30-day window):
- 99.9% of POST /checkout requests succeed (non-5xx)
- p99 latency of POST /checkout < 1.5s

Pages currently fire on "5xx rate > 1% for 5 min" and "CPU > 80%".
