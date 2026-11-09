---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, browser or environment are available; everything you need is in this message.)

Need a customer email for this incident. It goes to every affected account — mostly small business owners in the US (salons, physios, dog groomers) who use us for appointment booking and reminders. Support lead wants it sent today. Eng notes from Priya below.

```
INC-2291 — reminder send-time skew + dup sends
- 2026-11-04 14:12 UTC deploy booking-api v4.18, incl. migration changing tz handling on reminders table
- bug: scheduler read scheduled_at as naive UTC for accounts w/ non-UTC tz -> SMS/email reminders fired at wrong
  times, off by the account's UTC offset (US accounts: 5-8h early or late)
- also ~3% of reminders double-sent: retry worker re-enqueued jobs that timed out at the SMS gateway but had
  actually been delivered
- detected 2026-11-05 02:40 UTC from support tickets (no alert on send-time skew, oops)
- rolled back 03:25 UTC; fixed forward with v4.18.1 at 09:10 UTC
- impact: 1,842 accounts, ~61k reminders between 11/04 14:12 and 11/05 03:25 UTC
- bookings themselves NOT affected, calendar times correct throughout, no data lost
- SMS credits burned by dup sends: auto-refund, will show as a credit on the December invoice
- some end customers probably missed appointments because the reminder came hours late / early. we can't tell which.
- follow-ups: alert on send-time skew, idempotency key on SMS gateway calls, tz test coverage
```
