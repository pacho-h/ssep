---
name: improving-feature-completeness
description: Audits a working feature implementation for the gap between "happy path passes" and "ready to ship to production" — edge cases, error handling, loading/empty/error states, accessibility, responsive behavior, internationalization, observability, and operational hooks. Use when a feature implementation works but needs polish, when user says "완성도 높여줘", "production ready로 만들어줘", "edge case 검토", "polish this feature", "is this ready to ship?", "출시 가능한지 점검", "엣지 케이스 다 챙겼나", "PR 전 점검", "빠진 상태 없나", "ship 전 검토", or before shipping any non-trivial frontend or backend feature. Also triggers proactively right before PR creation on a non-trivial feature branch, even without explicit user request. Triggers even when the diff is small or the happy path was verified manually; completeness gaps emerge from state interactions (empty/loading/error/disabled, role variants, locale variants), not from line count, and "I already clicked through it in Playwright" does not substitute for the audit. Distinct from brainstorming (which designs the feature), test-driven-development (which implements it), and requesting-code-review (which evaluates code structure) — focuses specifically on raising the bar of an already-working implementation through a structured production-readiness audit.
allowed-tools: Read, Grep, Glob, Edit, Bash
---

# Improving Feature Completeness

## Purpose

A feature that works on the happy path is approximately 50% done. The remaining 50% is what users actually encounter — empty states, slow networks, expired sessions, screen readers, second languages, off-by-one boundaries, and the operator who needs to debug it next Tuesday.

This gap is invisible to standard code review (which looks at structure) and to TDD (which proves the spec'd behavior works). It needs its own audit pass: enumerate the production scenarios, check each one, surface what's missing.

This skill performs that audit. Output is a prioritized gap list and, when scope permits, the actual edits to close gaps.

## When to use this skill

- A feature is implemented and the happy path works
- User says "완성도 점검", "production ready", "edge case 검토", "polish this feature", "is this ready to ship?"
- Before any release that includes new user-facing functionality
- After resolving a production incident that revealed a class of missing handling — to find the same class elsewhere

## When NOT to use

- Designing the feature → `superpowers:brainstorming`
- Initial implementation → `superpowers:test-driven-development`
- Reviewing code quality / structure → `superpowers:requesting-code-review`
- Comparing UI to design → `reviewing-design-fidelity`

## Workflow

### 1. Inventory the feature surface

Identify what is actually in scope before auditing. Read the entry points and trace outward:

- **Frontend feature:** start from the route/page component, list all child components and the data they fetch
- **Backend feature:** start from the route/handler, list all DB tables, external calls, queues, and side effects
- **Full-stack feature:** combine both inventories

Bound the scope explicitly. "Audit the user dashboard" is unbounded; "audit the user dashboard's billing tab" is bounded.

### 2. Run the audit by dimension

Apply the dimensions in `references/audit-dimensions.md`. Each dimension generates zero or more gap findings.

The dimensions are organized in two tracks — frontend (UI surface) and backend (data/operational surface) — because the relevant probes differ. Most full-stack features need both tracks.

**Frontend track:**
1. State coverage (loading, empty, error, partial, stale)
2. Accessibility (keyboard, screen reader, contrast, focus)
3. Responsive behavior (every breakpoint the design covers)
4. Input validation and error messaging
5. Internationalization (text externalization, RTL, date/number formats)
6. Performance perception (skeleton screens, optimistic updates, debouncing)

**Backend track:**
1. Input validation (boundaries, types, encoding)
2. Authorization (every operation has explicit checks; not just authentication)
3. Concurrency (idempotency, race conditions, partial failures)
4. Error handling (every external call has timeout + retry policy + failure mode)
5. Observability (logs, metrics, traces — enough to debug without a re-deploy)
6. Operational hooks (admin override, audit trail, data export, deletion compliance)

See `references/audit-dimensions.md` for full descriptions, probes, and example findings per dimension.

### 3. Prioritize by user/operator impact

- **Blocker** — feature is unsafe or unusable for some user class without resolution (a11y blocker, missing error handling that loses data, missing authorization)
- **Major** — feature works but degrades materially in realistic scenarios (slow network has no feedback, error states leak stack traces, no admin visibility)
- **Polish** — quality bar improvements with no functional impact (skeleton screens, copy refinement, telemetry granularity)

Skip "nice to have" findings; if it's not at least Polish-tier impact, drop it from the report.

### 4. Decide: report or fix

Two modes depending on the user's request:

- **Audit-only mode (default):** produce the gap report. Author or feature owner decides which to fix. Use the template in `references/completeness-report-template.md`.
- **Audit-and-fix mode:** when the user explicitly asks for fixes ("개선까지 해줘", "fix the gaps"), close blocker and major findings in place via Edit, leaving polish findings in the report for follow-up. For each fix, write the test first (per `superpowers:test-driven-development` discipline) so the gap stays closed.

If audit-and-fix mode produces more than ~5 fixes, pause and present the report first — landing 20 fixes in one pass is a code-review nightmare and bypasses the author's input.

### 5. Verify before claiming done

Before reporting completion, run whatever the project's verification commands are (tests, type-check, lint, build). Per `superpowers:verification-before-completion`: evidence before assertions. Don't claim "all gaps closed" without showing the verification output.

## Principles

- **Audit the user's reality, not the developer's setup.** "Works on my machine with seeded data and warm cache" is the starting point, not the finish line.
- **Operators are users too.** A feature with no admin override and no audit log is incomplete for the operator class, even if end-users are happy.
- **Errors are features.** Every error path is a code path users will hit. An unhandled error is a missing feature, not a missing exception block.
- **Each finding cites a probe.** "How did you find this?" should always be answerable. "Tabbed through the form, focus indicator disappeared on the second input" beats "accessibility issue".
- **Closing a gap requires a test.** Once a gap is identified and fixed, write the test that would catch its regression. Otherwise the same gap returns next quarter.

## Detailed references

- `references/audit-dimensions.md` — full descriptions, probes, and example findings per dimension (frontend + backend tracks)
- `references/completeness-report-template.md` — annotated template with example findings
- `references/state-coverage-patterns.md` — UI state taxonomy (loading variants, empty variants, error variants) and per-pattern implementation hints
