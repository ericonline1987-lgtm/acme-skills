---
name: writing-tests
description: Write tests that would catch real regressions — match the project's framework, one behaviour per test with descriptive names, edge and invalid cases, shown to fail without the fix, real results reported. Use whenever someone asks for tests, unit tests, pytest or Jest cases, more coverage, or a test that reproduces a bug.
---

# Writing tests

A test earns its place if it would fail when the behaviour it guards breaks. Coverage
numbers are a side effect.

## Process

1. **Follow the project.** Detect the framework, file layout, naming, fixtures and
   mocking style from existing tests, and match them.
2. **List behaviours before writing code**: the main path, boundaries, invalid input,
   error paths, concurrency or ordering if relevant, and the reported bug if there is one.
   Prioritise by what would hurt users most if broken.
3. **One behaviour per test**, named for what it checks (`rejects_expired_token`, not
   `test_token_2`). Arrange, act, assert.
4. **Use realistic inputs.** Take shapes from real data, logs or fixtures where possible;
   invented inputs miss what production sends.
5. **Mock only at boundaries** (network, clock, filesystem, third-party services). Never
   mock the unit under test.
6. **Prove each test can fail.** For a bug fix, run it without the fix and see it fail,
   then with the fix and see it pass. For new tests on existing code, break the
   behaviour briefly and confirm the test catches it.
7. **Run and read the real result**, not a piped exit code. Compare failures with the
   same tests before your change and report "no new failures" rather than "all pass"
   when old failures exist.

## Quality bar

- No sleeps, real network calls or shared mutable state in unit tests.
- Assertions check outcomes the user would notice, not private details.
- Test data is minimal and readable; each test runs alone.

## Report

Tests added (one line each with the behaviour), the run command and its real output,
which tests were shown to fail without the change, and what remains untested and why.
