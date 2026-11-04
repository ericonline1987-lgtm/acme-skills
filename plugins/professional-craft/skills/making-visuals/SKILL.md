---
name: making-visuals
description: Always use this skill when making or fixing something people look at — slides or a deck, a chart, a diagram or figure, a dashboard, an HTML page or app screen — or when checking, testing or screenshotting one ("make sure it works", "does it look right on a phone"), even a quick one. It designs from the one point to land, encodes data honestly, and checks the rendered result at its real size.
---

# Making visuals

A visual works when the viewer's eye lands on the point first and nothing on the page
contradicts or distracts from it. Source code, DOM text and a description of a chart
are leads; what a person sees at real size is the evidence.

## 1. Name the point and the medium

Write the one thing the viewer should take away, and where they'll see it: projected in
a room, read alone on a laptop, on a phone, in print, in a Markdown file on a code host.
The medium decides what's possible: motion needs a static fallback, print has no
hover, a code host strips most HTML.

## 2. Pick the form

- **Slides**: `references/decks.md`. Storyline as headlines first; one claim per slide;
  the last headline is the ask, written out.
- **Charts and diagrams**: `references/charts-and-diagrams.md`. Form from the question,
  bars from zero, direct labels, one accent colour on what the title names.
- **Pages, dashboards, app screens**: `references/pages.md`. Hierarchy, spacing scale,
  every real state (empty, loading, error, too much), keyboard and narrow screens.

If one sentence carries the point, write the sentence instead (see
`writing-for-people`).

## 3. Use real material, honestly

- Show the real thing: the actual screenshot, number or output, cropped but not redrawn.
- Nothing invented to fill a gap: a missing figure or capture is marked
  `[Q3 figure from finance]` and resolved before it ships.
- A before-and-after pair differs only in the thing claimed.
- Every number on a visual carries its basis (source, period, n).
- A chart that should "pop" gets a sharper title and an accent, never a truncated axis.

## 4. Build for the reader's conditions

Readable at the distance and size it will be seen (24 pt or more on projected slides,
16 px body on screen); 4.5:1 contrast for text, 3:1 for large text and marks; colour
never the only carrier of meaning; motion pausable and off under reduced-motion
settings.

## 5. Check the rendered result

1. **Lock the target.** Name the build, environment, address, account and screen sizes,
   and where each came from. If that environment can't be reached, or not in the right
   login state, say so and stop: results from a look-alike are discarded. Confirm the
   change is in what you're looking at (version, hash, a hard reload with cache off).
2. **Pick the tool by intent.** Repeatable assertions and regression coverage: Playwright
   (`references/playwright.md`). A one-off look at layout or network: browser developer
   tools. Acting as the logged-in person: their browser session. Search the project for
   an existing test harness first. If a browser tool can't start, report that as a tool
   failure, not as evidence about the page.
3. **Run the checks that apply** from `references/rendered-checks.md`. The minimum for
   anything handed to others: loads with no console errors, key interactions work, no
   horizontal scroll at 320 px, readable at 200% zoom, contrast, keyboard use with
   visible focus, every fixed frame (slide, card) without overflow at real size.
4. **Capture honestly.** Let animations finish and images decode before a screenshot;
   a mid-animation capture is false evidence. Judge what a viewer sees from pixels, not
   the DOM. For SVG, run `python3 scripts/validate_svg.py <file>` and then look at it.
5. **Keep the record straight.** A blank or error page is a load failure, not a result.
   If a submit was interrupted, look the record up before repeating it. Keep checks
   read-only on an environment someone is using, or ask.

A durable, user-visible bug gets a small regression test, not only a manual look.

## Report

```
point: <the takeaway>   medium: <where it's seen>
checked: <build> on <environment> at <address>, sizes <list>, themes <list>
evidence: <check -> result>, one line each, screenshots named
not covered: <states, sizes, browsers, roles not exercised; anything unrendered>
```

A screenshot proves one state at one size; say so when it's offered as proof.

## Not this skill

The words on a slide or page follow `writing-for-people`. Unit and integration tests for
the code behind a page belong to `changing-code`.
