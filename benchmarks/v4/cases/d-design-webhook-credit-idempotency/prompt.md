---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, browser or environment are available; everything you need is in this message.)

We sell prepaid credits. Finance found 37 users last month with more credits than they paid for, and a handful with negative balances. Here's the webhook handler (Flask + SQLAlchemy, 4 gunicorn workers × 3 pods):

```python
@app.post("/webhooks/stripe")
def stripe_webhook():
    event = stripe.Webhook.construct_event(
        request.data, request.headers["Stripe-Signature"], WH_SECRET
    )

    if event.type == "payment_intent.succeeded":
        pi = event.data.object
        user = User.query.get(pi.metadata["user_id"])
        user.credits += int(pi.metadata["credits"])
        db.session.commit()
        send_receipt_email(user, pi)          # calls SendGrid, ~300-900ms

    elif event.type == "charge.refunded":
        ch = event.data.object
        user = User.query.get(ch.metadata["user_id"])
        user.credits -= int(ch.metadata["credits"])
        db.session.commit()

    return "", 200
```

How should this be redesigned?
