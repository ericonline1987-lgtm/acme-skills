---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, browser or environment are available; everything you need is in this message.)

Product pages are slow — p99 ~900ms, mostly waiting on pricing-service. Pricing computes price per SKU × region × customer tier (6 regions, 4 tiers, ~120k SKUs). pricing-service p50 is 40ms but the tail is bad, and it falls over above ~3k rps.

Traffic: ~8k rps on product pages, very skewed — top ~2k SKUs get 70% of views. Merchandising changes a few hundred prices a day. We also run flash sales where ~3k SKUs change price at an exact time (e.g. 12:00:00 ET), announced a week ahead, and traffic jumps ~5x right at the start.

Team's proposal: Redis in front of pricing-service, key = `price:{sku}`, TTL 10 minutes. Thoughts? What would you do instead/in addition?
