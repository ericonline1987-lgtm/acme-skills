# Tests that fail for the right reason

Read this when writing or fixing tests, or when a change needs one. A test earns its
place if it fails when the behaviour it guards breaks, and only then. Coverage is a side
effect; a test that can't fail is worse than none, because it reads as protection.

## Before writing

- Follow the project: its framework, layout, naming, fixtures and mocking style.
- List the behaviours first: the main path, each boundary, invalid input, error paths,
  ordering or concurrency where it matters, and the reported bug. Order by what would
  hurt users most if it broke.
- Ask what the code promises, not what it currently does. A test that pins a bug in
  place turns the next fix into a "broken test".

## Writing

- One behaviour per test, named for it (`rejects_expired_token`, not `test_token_2`).
  A parametrized test over inputs of the same behaviour counts as one test.
- Assert on outcomes a caller or user would notice: the return value, the stored row,
  the message sent. Not private fields, call counts on internals, or log lines, unless
  the log is the contract.
- Realistic inputs, taken from real data, logs or fixtures where possible: invented
  inputs miss the Unicode name, the 0-quantity order and the null that production sends.
- Mock only at boundaries you don't own or can't run quickly: network, clock,
  filesystem, third-party services. Never mock the unit under test, and prefer a fake
  (an in-memory store with the real interface) to a mock that records calls.
- Control time and randomness explicitly: inject the clock, seed the generator. A test
  that passes at 23:59 and fails at 00:01 is a test of the calendar.
- Each test sets up what it needs and runs alone, in any order, in parallel. Shared
  mutable state and fixed temp paths are the most common cause of tests that pass
  locally and fail on CI.

## Proving it can fail

- For a bug fix: run the new test without the fix and watch it fail for the reason you
  expect (read the failure message), then with the fix and watch it pass.
- For new tests on existing code: break the behaviour on purpose (invert a condition,
  delete a line) and confirm the test catches it, then restore.
- A test that passes on the first run, before any code exists, is testing nothing.

## Kinds of test, by what they catch

| Kind | Catches | Watch out for |
|---|---|---|
| Unit | Logic errors in one function or class | Over-mocking until the test checks the mock |
| Integration | Wrong assumptions about a database, queue or service | Slow suites nobody runs; keep them few and focused |
| Contract | A provider changing what a consumer relies on | Contracts written by one side only |
| Property-based | Edge cases you didn't think of (round-trips, invariants) | Properties that restate the implementation |
| Snapshot or golden file | Unintended changes to large output | Snapshots updated without being read; review the diff |
| End-to-end in a browser | Broken user flows | Flakiness; role-based locators and auto-waiting assertions, few tests (see `making-visuals` for rendered checks) |

## Flaky tests

A test that sometimes fails is a bug in the test or the code, and a retry hides which.
Measure the failure rate over many runs, then look for the usual causes: shared state
or files between tests, order dependence, real time or timezones, unawaited async work,
real network, and resource limits that differ on CI. Fix the cause, then remove the
retry.

## Running and reporting

- Run the narrowest set that exercises the change, then the tests of every caller you
  found. Read the real output, not a piped exit code.
- Compare with the same tests before your change. Report "no new failures" rather than
  "all pass" when failures existed before.
- Report: tests added, one line each with the behaviour; the command and its output;
  which were shown to fail without the change; what stays untested and why.
