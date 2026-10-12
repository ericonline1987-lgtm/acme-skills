---
name: writing-tests
description: Write unit and integration tests for existing or new code, matching the project's test framework and conventions. Use when someone asks to add tests, improve coverage, or write a test for a bug.
---

# Writing tests

## Process
1. **Detect the framework and conventions** from the repo (pytest, Jest, Go testing, etc.), including file naming, fixtures, and mocking style. Follow them.
2. **List behaviors before writing code:** happy path, boundaries, invalid input, error paths, and any reported bug.
3. **Write one test per behavior,** named for what it checks (`test_rejects_expired_token`, not `test_token_2`).
4. **Use Arrange / Act / Assert** structure. Keep each test independent.
5. **Mock only at boundaries** (network, clock, filesystem). Don't mock the unit under test.
6. **Run the tests.** Confirm new tests pass, and for a bug fix, confirm the test fails without the fix.

## Quality bar
- Assertions check outcomes, not implementation details.
- No sleeps or real network calls in unit tests.
- Test data is minimal and readable.
