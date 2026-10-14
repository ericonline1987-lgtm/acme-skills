# Playwright practice

## Locators

- Prefer what a user perceives: `getByRole('button', { name: 'Pay now' })`,
  `getByLabel('Email')`, `getByText('Order placed')`. Use `getByTestId` when the UI has
  no stable accessible name. Avoid CSS chains and XPath tied to layout.
- Scope inside a region (`page.getByRole('dialog').getByRole('button', ...)`) instead of
  using `nth()`.

## Assertions and waiting

- Use web-first assertions that retry: `await expect(locator).toBeVisible()`,
  `toHaveText`, `toHaveURL`, `toHaveCount`. Never `waitForTimeout` as a wait for state.
- Assert the outcome the user sees (a confirmation, a total, a disabled button), not
  internal calls.

## Authentication

- Log in once in a setup project and save `storageState`; reuse it per role. Never log in
  through the UI in every test.
- Keep stored auth files out of the repository and outside shared folders.

## Mocking

- Mock at the network boundary (`page.route`) for third parties and failure cases you
  can't trigger (payment declined, a 500, a slow response). Don't mock your own backend
  in end-to-end tests, or the test proves only the mock.

## Isolation

- Each test gets its own browser context; tests don't depend on order or shared data.
  Create the data a test needs through an API in setup and clean it up after.
- Page objects are worth it when a page is used by many tests; follow the project's
  existing pattern otherwise.

## Flaky tests

- Turn on `trace: 'on-first-retry'` and read the trace before changing anything.
- Reproduce with `--repeat-each=20`. Common causes: a missing web-first assertion, shared
  state between tests, animations, time and time zones, and test data collisions.
- A retry that hides a real race is a bug report, not a fix.

## Toolchain failures (not UI evidence)

- A browser folder existing doesn't mean the browser installed; look for the completed
  install marker or run the browser's `--version`.
- Downloads can be silent for minutes. Don't kill an install mid-write; a truncated
  binary is worse than a missing one.
- Before switching download mirrors, check whether Playwright already fell back. If the
  bundled browser can't be installed, use an installed one: `channel: 'chrome'` (and
  `video: 'off'` if the media helper is missing).
- Report any of these as a tool failure with the exact error, then decide on a fallback.
