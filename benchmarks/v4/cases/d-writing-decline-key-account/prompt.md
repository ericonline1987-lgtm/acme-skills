---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, browser or environment are available; everything you need is in this message.)

can you draft my reply to Dana? context below.

Halvorsen Logistics is our biggest account (~$410k ARR, renewal in March). Dana Whitcomb is their VP Ops. She wants us to build a custom on-prem connector that pushes shipment data into their legacy AS/400 system every night. Product said no: we don't build customer-specific integrations, and on-prem is off the roadmap completely.

What we can offer:
- our REST API already exposes all the shipment data they'd need
- Tessaline (one of our integration partners) does AS/400 work all the time, usually 4-6 weeks, they quote the customer directly
- the nightly CSV-to-SFTP export that's in beta now goes GA on Dec 8, they could use it from then

I really don't want to lose them.

Her email:

> Hi Marcus — following up on our call Tuesday. As discussed, the nightly AS/400 feed is a must-have for us before we roll out to the remaining 6 depots in Q2. Can you confirm your team will build this and send me a timeline?
>
> Thanks,
> Dana
