# Choosing the Test Level

## Decision tree

```
Does the behavior involve actual I/O (DB, HTTP, queue, browser)?
├─ No → unit test (jest/vitest, no test DB, no test server)
└─ Yes → does the behavior require multiple user-visible steps?
   ├─ No → integration test (real HTTP/DB, no browser, single boundary)
   └─ Yes → end-to-end test (real browser via Playwright MCP, full flow)
```

## Worked examples

### Example 1: Date formatting in user's locale
- "Format a Date as 'YYYY-MM-DD' in user's locale"
- No I/O, single function → **unit test**
- Anti-pattern: writing an e2e test that loads the page and reads the displayed date — adds 30 seconds per CI run for behavior that's expressible in <100ms

### Example 2: API endpoint returns user's orders
- "GET /api/orders returns the requesting user's orders, ordered by date desc, with pagination"
- Real HTTP boundary, real DB query, real auth — single boundary → **integration test**
- Anti-pattern: mocking the DB. The test then proves the mock returns what you told it to, not that the query actually works

### Example 3: User completes checkout
- "User adds item to cart, navigates to checkout, fills payment, sees confirmation"
- Multi-step user flow crossing UI → API → payment service → DB → email queue → **end-to-end test**
- Anti-pattern: trying to express this as a series of integration tests. The e2e nature *is* the behavior being tested

### Example 4: SQL constraint enforces uniqueness
- "Cannot insert two users with the same email"
- The behavior is the DB constraint itself — must run against real DB → **integration test**
- Anti-pattern: a unit test that asserts the application code calls `INSERT` correctly. That doesn't prove the constraint exists or works

### Example 5: Charging session state machine
- "Session transitions: Idle → Authorized → Charging → Completed"
- If transitions are pure logic in code → **unit test** for the state machine
- If transitions involve DB writes and external service calls between states → **integration test**
- Choose based on where the behavior actually lives, not where it conceptually belongs

## When in doubt, write at the lowest level you can

A unit test runs in milliseconds and survives refactors. An e2e test runs in tens of seconds and breaks with every UI change. The cost-of-test compounds across thousands of CI runs.

A team-level rule of thumb:
- Unit tests: thousands per service, run on every save
- Integration tests: tens to low hundreds per service, run in CI
- E2e tests: low tens per major feature, run nightly or on release branch

If you're considering writing the 100th e2e test in a service, that's the signal to push behavior down to integration / unit tiers, not to tolerate slower CI.
