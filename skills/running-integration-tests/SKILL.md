---
name: running-integration-tests
description: Authors and executes tests across all levels of the test pyramid — unit, frontend-backend integration, and end-to-end browser scenarios — using Playwright MCP and standard test runners (jest, vitest, mocha). Use when verifying multi-layer behavior or when user requests "e2e 테스트", "integration 테스트", "통합 테스트", "playwright로 검증", "브라우저에서 직접 확인", "백엔드-프론트 연동 테스트", "API 통합 테스트", "staging에서 확인", "staging 검증", "배포 후 검증", "실제 화면에서 확인", "smoke test", or when a feature crosses service boundaries (API + UI + DB). Also triggers when user asks to verify a deployed feature or when a PR test plan has unchecked browser/API verification items. Triggers even when only one boundary is crossed in the change and a manual Playwright click was already performed; manual verification proves the path works once but does not produce a codified regression test, and integration-tier surprises cluster at exactly the boundary that "looked fine" during manual checks. Helps decide which test level fits, sets up infrastructure, writes tests, runs them, reports failures with diagnostic context. Distinct from superpowers:test-driven-development (unit-level TDD); this handles integration and e2e tiers.
allowed-tools: Read, Grep, Glob, Edit, Bash, mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_click, mcp__plugin_playwright_playwright__browser_type, mcp__plugin_playwright_playwright__browser_fill_form, mcp__plugin_playwright_playwright__browser_select_option, mcp__plugin_playwright_playwright__browser_press_key, mcp__plugin_playwright_playwright__browser_hover, mcp__plugin_playwright_playwright__browser_snapshot, mcp__plugin_playwright_playwright__browser_take_screenshot, mcp__plugin_playwright_playwright__browser_evaluate, mcp__plugin_playwright_playwright__browser_console_messages, mcp__plugin_playwright_playwright__browser_network_requests, mcp__plugin_playwright_playwright__browser_wait_for, mcp__plugin_playwright_playwright__browser_resize, mcp__plugin_playwright_playwright__browser_navigate_back, mcp__plugin_playwright_playwright__browser_handle_dialog, mcp__plugin_playwright_playwright__browser_close
---

# Running Integration Tests

## Purpose

A passing unit test proves a function returns the expected value. It does not prove the API endpoint that calls the function works, that the database returns the expected schema, that the frontend renders the response correctly, or that the user can complete the flow end-to-end. Each of those is a different test level, and skipping the right one is how features ship "with full test coverage" and immediately break in production.

This skill handles the test levels above the unit tier — integration tests that exercise real HTTP/DB/queue boundaries, and end-to-end tests that drive a real browser through complete user flows. It also handles the meta-decision of which level fits which scenario, since the wrong level is worse than no test (slow, brittle, and gives false confidence).

## When to use this skill

- A feature crosses layer boundaries (frontend ↔ API, API ↔ DB, service ↔ queue, multi-service)
- User requests "e2e 테스트", "integration 테스트", "통합 테스트", "playwright로 확인", "브라우저에서 직접 검증", "API 통합 테스트", "프론트백 연동 확인"
- Unit tests pass but production behavior is broken — the gap lives in the integration tier
- A user flow needs to be verified through actual UI, not unit-level abstractions

## When NOT to use

- Pure function or class behavior with no I/O → use `superpowers:test-driven-development` (unit TDD)
- Visual regression / pixel comparison → use `reviewing-design-fidelity` (which uses Playwright too, but for visual diff rather than behavioral assertion)
- Manual exploratory smoke check that doesn't need to be re-run → just run it; not every check needs to be a test

## The decision: which test level

A test should live at the lowest level where it can express the behavior it needs to verify. Higher levels are slower, more brittle, and harder to debug.

| Level | Speed | Verifies | Use when |
|---|---|---|---|
| Unit | <100ms | Pure logic, single function/class | Behavior is fully expressible in inputs/outputs without I/O |
| Integration | 100ms – 5s | Real HTTP/DB/queue boundaries, real schemas | Boundary contract is what's being tested (route returns expected JSON, query returns expected rows) |
| End-to-end | 5s – 60s | Full user flow through real UI | Multi-step user behavior that crosses many boundaries |

Common mistakes:
- Writing an e2e test for behavior that's actually a unit-level concern (e.g., date formatting) — wastes minutes per CI run
- Writing a unit test for behavior that requires real DB constraints (e.g., uniqueness, foreign keys) — gives false confidence
- Writing integration tests with mocked DB — tests the mock, not the system

See `references/test-level-decision.md` for the decision tree and worked examples.

## Workflow

### 1. Identify the behavior being verified

Write a single sentence: "When the user does X, the system should Y." This is the test's reason for existence; if you can't write it, the test isn't ready to be written.

### 2. Choose the level

Apply the decision tree from `references/test-level-decision.md`. If multiple levels could express the behavior, choose the lowest. Document the choice briefly in the test (a one-line comment) so future readers know it was deliberate.

### 3. Set up the level's infrastructure

Each level has its own setup pattern. See:

- `references/integration-test-patterns.md` for HTTP+DB integration tests — test database setup, fixtures, transactional rollback, request helpers
- `references/playwright-patterns.md` for end-to-end browser tests via Playwright MCP — selector strategy, waiting, network mocking, capturing diagnostics on failure

### 4. Write the test, then run it red

Per TDD discipline: write the test, run it, see it fail with the expected failure mode (not a setup error masquerading as a test failure). Only then is the test ready to be paired with implementation. If implementation already exists and the test is being added retroactively, still run it red first by intentionally breaking the implementation in one place — confirms the test would catch the regression it claims to.

### 5. Run the test green

Make the test pass. For new features, this is the implementation work. For retroactive tests, this is just verifying the test passes against current code.

### 6. Capture diagnostics on failure

When an integration or e2e test fails, the cause is rarely visible from the assertion message alone. Required diagnostics by level:

- **Integration:** the actual HTTP response (status, headers, body), the actual DB state at the point of failure, recent logs from the system under test
- **End-to-end (Playwright MCP):** screenshot at point of failure, accessibility snapshot, console messages, network request log

See `references/playwright-patterns.md` § "Failure diagnostics" for the standard capture sequence to run when a Playwright test fails.

### 7. Commit the test alongside the change

A test that lives only on a developer's machine doesn't catch regressions. Commit the test and run it in CI. If CI doesn't yet run integration / e2e tests, that's its own finding to surface (CI gap → blocker for feature completeness).

## Principles

- **Lowest level that expresses the behavior.** Higher levels are debt.
- **Real I/O at integration level.** Mocked DB tests prove the mock works.
- **One user flow per e2e test.** Multi-flow e2e tests fail in compound ways and become impossible to triage.
- **Selector stability over selector convenience.** Prefer `data-testid` or accessible roles over CSS classes that change with refactors.
- **Capture diagnostics automatically on failure.** A flaky e2e failure with no diagnostics is wasted CI time.
- **Test the contract, not the implementation.** An integration test that asserts on internal log lines breaks every refactor; one that asserts on the response body and DB state survives refactors.

## Detailed references

- `references/test-level-decision.md` — decision tree and worked examples for choosing unit vs integration vs e2e
- `references/integration-test-patterns.md` — HTTP+DB integration patterns: test DB setup, transactional fixtures, request helpers, common pitfalls
- `references/playwright-patterns.md` — end-to-end browser test patterns using Playwright MCP: selector strategy, waiting, network mocking, failure diagnostics
