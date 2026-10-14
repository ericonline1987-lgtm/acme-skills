# Rendered-surface checks

Pick the rows that apply. Each says what to check and one way to check it.

| Check | Pass when | How (Playwright snippet or manual) |
|---|---|---|
| Loads cleanly | No console errors or failed requests | `page.on('console', m => m.type()==='error' && errors.push(m.text()))`; `page.on('requestfailed', ...)` |
| Small screens | No horizontal scroll at 320px | `setViewportSize({width: 320, height: 800})`, then `document.documentElement.scrollWidth <= clientWidth` |
| Zoom | Text readable, nothing clipped at 200% | Browser zoom to 200%, or `document.body.style.zoom = '2'` as an approximation; look at it |
| Contrast | 4.5:1 body text; 3:1 large text, icons and chart marks | An accessibility checker (axe, Lighthouse) plus a spot check on brand colours |
| Keyboard | Every control reachable by Tab, visible focus, no trap, Escape closes dialogs | Tab through; `expect(locator).toBeFocused()` |
| Hit areas | Controls about 24×24 CSS px or larger | `boundingBox()` on buttons and links |
| Fixed frames | No overflow in slides, cards or canvases at real size | For each frame, `el.scrollHeight <= el.clientHeight && el.scrollWidth <= el.clientWidth` |
| Projection | No leftover margins or overflow at true full screen in the venue's aspect ratio | OS-level full screen at 16:9 (or the venue's ratio), step through every page |
| Dark rooms | No glaring full-white slides when projecting in the dark | Look at it at full brightness |
| Master-detail views | Opening a detail and returning keeps filters, scroll and focus | Inspect, return, inspect again |
| Media in overlays | Clicking player controls doesn't close the overlay; closing pauses playback | Click the controls; close and listen |
| Global keys | Navigation keys don't fire while a player or embedded frame has focus, and clicking content doesn't navigate | Focus the media, press the keys |
| Animation settled | Captures show the final state | `page.emulateMedia({ reducedMotion: 'reduce' })` or wait for animations; `await img.decode()` for images |
| Offline or packaged | Works where the reader will open it (no network, file URL) | Open the exported copy from a clean folder with the network off |

After a check fails, fix it, then re-run that row and its neighbours.
