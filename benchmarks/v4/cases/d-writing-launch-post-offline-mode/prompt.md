---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, browser or environment are available; everything you need is in this message.)

Need the launch post for our blog + in-app changelog, ~300 words. Readers are inspection managers and field techs (utilities, facilities, construction). Marketing wants it to pop. Facts from the PM:

- Feature: Offline mode for the Fieldwise mobile app (iOS + Android). Ships Nov 18.
- Techs can open assigned inspections, fill in forms, take photos and capture signatures with no signal. Everything syncs automatically when the device is back online.
- Before going offline, the app caches up to 500 inspections per device (most recent assigned first).
- If two people edit the same inspection while offline, each field takes the value from whoever synced last. The overwritten value is kept in the inspection's History panel and can be restored.
- Map layers over 200 MB aren't available offline.
- Not on the web app.
- Needs app version 7.4 or later. Team plan and above (not Starter).
- Beta: 14 customers since August. Brightwater Utilities told us their crews working in tunnels and basements used to fill in paper forms and retype them back at the depot; they've stopped doing that.
- Help article: fieldwise.com/help/offline
