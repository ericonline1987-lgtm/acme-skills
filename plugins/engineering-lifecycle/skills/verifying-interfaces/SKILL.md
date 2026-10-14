---
name: verifying-interfaces
description: Prove a web page, dashboard, deck or UI change works as people will see and use it — the right environment and login, the right browser tool for the job, settled screenshots, zoom, contrast, small screens, overflow and keyboard checks. Use whenever someone asks to check, test, screenshot, smoke-test or confirm a page, HTML file, UI flow or browser behaviour.
---

# Verifying interfaces

A UI claim is proven by what a person would see and be able to do, in the environment
that matters. Code, DOM text and logs are leads; the rendered surface is the evidence.

## 1. Lock the target

- Name the build, environment, address, account or role, and screen sizes being checked,
  and where each came from (the bug report, the person, the deploy record).
- If the named environment can't be reached, or not in the right login state, report that
  and stop. A reachable look-alike is not a substitute; results from it are discarded.
- Confirm the change is actually in the build you are looking at (version, commit, file
  hash). After editing a local file, hard-reload with the cache disabled.
- If someone is using the environment right now, keep checks read-only or ask first.

## 2. Pick the tool by intent

| Intent | Tool |
|---|---|
| Repeatable assertions, regression coverage, CI | Playwright (see `references/playwright.md`) |
| One-off look at layout, performance, network, Core Web Vitals | Browser developer tools |
| Navigating as a logged-in user, forms, an existing session | A session-aware browser using the person's profile |

- Search the project for an existing login or test harness before writing one.
- A durable, user-visible bug needs a small regression test, not only a manual look.
- If a browser tool can't start, connect or install, report that tool failure as such; it
  is not evidence about the UI (see the toolchain section of `references/playwright.md`).

## 3. Keep the session and the record straight

- Don't assume a fresh browser has the person's cookies or permissions. To recover a lost
  session, open a new tab in the same profile; ask before anything that could log out.
- A blank or error page is a load failure, not a result. Never infer whether an earlier
  action succeeded from it; check an independent record.
- If a submit or other change was interrupted, look the record up (order, ticket, case)
  and continue from its id rather than repeating the flow and creating a duplicate.
- When the person unblocks you (logs in, grants access), carry the real interaction
  through and capture it; don't substitute a description.

## 4. Check the rendered surface

Run the checks in `references/rendered-checks.md` that apply. The minimum for any page
handed to others:

- Loads with no console errors; key elements and interactions work.
- Readable at 200% zoom; no horizontal scrolling at 320px wide; text contrast at least
  4.5:1 (3:1 for large text and chart marks); usable by keyboard with visible focus.
- Every fixed-size frame (slide, card, canvas) checked at its real size for overflow.

## 5. Capture honest evidence

- Let animations finish and images decode before capturing; a mid-animation screenshot
  is false evidence. If a defect appears only in an early capture, re-capture before
  "fixing" it.
- Judge what a viewer sees from pixels, not from the DOM or logs.
- For SVG files (or inline SVG saved to a file), run `python3 scripts/validate_svg.py <file>`.
  It catches malformed XML, a bad viewBox, duplicate ids, broken internal references,
  external dependencies and scripts. It can't judge layout or legibility; look at it too.

## Report

```
claim: <what works>   rung: <checked | delivered | working in real use | accepted>
target: <build> on <environment> at <address> as <role>; sizes: <list>
evidence: <check -> result>, one line each, screenshots named
not covered: <states, sizes, browsers, roles, flows not exercised>
```

A screenshot proves one state at one size; a recording of a passing run is not a
regression test. Say so under "not covered" when either is offered as proof.
