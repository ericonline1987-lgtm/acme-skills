---
type: llm
weight: 1
---

Pass if this holds for the response: The response recognises that refund handling is wrong as written — charge.refunded can fire for partial and multiple refunds, so subtracting the full metadata credit amount each time over-deducts — and/or that events can arrive out of order (a refund before the success event) and proposes handling based on refund IDs/amounts or on the current object state rather than on event arrival order.
