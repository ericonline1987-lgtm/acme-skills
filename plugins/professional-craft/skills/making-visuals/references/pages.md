# Pages and interfaces

Read this when building or reworking an HTML page, a dashboard, an app screen or a
document meant to be read on screen.

## Hierarchy first

- Decide the one thing the page must get across, and make it the first thing the eye
  lands on: the largest type, the top-left of the content area, with space around it.
- Three or four levels of type at most (page title, section, body, caption), on a
  consistent scale (for example 32, 22, 16, 13 px). More sizes than that read as noise.
- Group by proximity: items that belong together sit closer to each other than to
  anything else. Borders and boxes are a last resort; space does the work first.
- Align everything to a grid. Ragged left edges and items a few pixels off read as
  careless even when nobody can say why.

## Spacing and density

- Use a spacing scale (4, 8, 12, 16, 24, 32, 48 px) and nothing between its steps.
- Body text 16 px or larger, line length 50 to 75 characters, line height about 1.5.
- Dense dashboards are fine for experts who use them daily; keep the density consistent
  and let the most important number be visibly larger, not just bolder.
- Whitespace is not wasted. A page that fills every pixel has no hierarchy.

## Colour and contrast

- A neutral base, one accent for actions and the current state, semantic colours (red,
  amber, green) only for status, each paired with an icon or word.
- Body text at least 4.5:1 against its background; large text, icons and chart marks at
  least 3:1. Check brand colours; they often fail.
- Define colours as variables and support dark mode deliberately, checking every element
  in both themes, not by inverting.

## States a real screen has

Design and check each one, not only the happy path with sample data:

| State | What the page shows |
|---|---|
| Empty | What goes here and how to add the first item |
| Loading | A skeleton or placeholder at the final size, so nothing jumps |
| Partial or slow | What's ready, with the rest clearly pending |
| Error | What went wrong in plain words, and what the person can do |
| Too much | Long names, many items, big numbers: truncation with full text on hover or focus |
| No permission | Why, and who to ask |

For example, a table that looks finished with three demo rows can push the page into
horizontal scroll with a real customer's 400 rows and 60-character names. Test with
real or worst-case data.

## Interaction

- Every control reachable and usable by keyboard, with visible focus, in a sensible
  order; Escape closes overlays.
- Touch and click targets about 24 px or larger, more on touch screens, with space
  between them.
- Feedback within a tenth of a second for any action; a progress indicator for anything
  longer than a second.
- Motion short and purposeful (showing where something went), and off when the reader
  asks the system for reduced motion.
- Opening a detail and coming back keeps filters, scroll position and focus.

## Responsive behaviour

- Design at the narrow width first (320 px), then let the layout widen. No horizontal
  scrolling at 320 px; text readable at 200% zoom.
- Tables on narrow screens: let the table scroll inside its own container, or stack
  each row as a card; never shrink the type.
- Fixed-size frames (slides, cards, canvases) checked at their real size for overflow.

## Packaging

State where the page will run and whether it must work offline before building. A page
sent as a file carries everything it loads; open the exported copy from a clean folder
with the network off before calling it done.
