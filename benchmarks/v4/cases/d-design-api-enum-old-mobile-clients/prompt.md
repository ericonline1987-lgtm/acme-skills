---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, browser or environment are available; everything you need is in this message.)

Two API changes we want in the next sprint for our mobile order API (`GET /orders`, `GET /orders/{id}`):

1. Add `partially_refunded` to `Order.status`. Current values: `pending, paid, shipped, delivered, refunded, cancelled`.
2. We're launching in Canada in January, so replace `total` (float, dollars) with `total_amount: { "value": 1999, "currency": "USD" }` (integer minor units).

Clients: Android decodes `status` into a Kotlin enum with Moshi; iOS decodes into a Swift `enum Status: String, Codable`. About 18% of mobile traffic comes from app versions more than a year old, and a chunk of those users will never update. Every app request sends an `X-App-Version` header.

Plan was to ship both as part of the next API release. How would you do it?
