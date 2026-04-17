# Audit Dimensions

Two tracks: frontend and backend. Most full-stack features need both. Each dimension lists probes (how to surface the finding) and an example finding to calibrate phrasing.

## Frontend track

### F1. State coverage

**Probe**
- For every async data fetch, list the states the UI can be in: idle, loading, success-empty, success-populated, success-stale, error-recoverable, error-fatal.
- For each state, render the page in that state (use dev tools network throttling, mock responses, or seeded test data) and inspect.

**Common gaps**
- Loading state is a blank page (use a skeleton or spinner)
- Empty state is also a blank page (use illustration + helper text + CTA)
- Error state shows a stack trace or generic "Something went wrong" with no recovery action

**Example finding (Major):** "Order list shows skeleton during fetch ✓, populated state ✓. Empty state (zero orders) renders as blank white area — should show 'No orders yet' message with CTA to start shopping. Error state on 500 response shows raw `Error: Network request failed` — should show user-friendly message with retry button."

### F2. Accessibility

**Probe**
- Tab through every interactive element — does focus visibly move and never get trapped?
- Activate VoiceOver / NVDA — is each element announced with meaningful label and role?
- Run the page through an automated checker (axe, Lighthouse a11y) for contrast and semantic issues
- Verify each form input has an associated label (visible or `aria-label`)

**Example finding (Blocker):** "Modal dialog has no focus trap. Tabbing past the last element returns focus to the page below the modal, which is supposed to be inert. Keyboard users cannot complete the dialog action without losing context."

### F3. Responsive behavior

**Probe**
- Test at every breakpoint the design covers (typically 375 / 768 / 1024 / 1440)
- For each breakpoint, verify content reflows without truncation, horizontal scroll, or hidden interactive elements
- Test with browser zoom at 200% (WCAG requirement) — content must remain usable

**Example finding (Major):** "Settings page navigation collapses to dropdown at 768px ✓. At 375px, the dropdown options overflow viewport horizontally — last 3 menu items unreachable without zooming out."

### F4. Input validation and error messaging

**Probe**
- For each form field, attempt: empty submit, max length + 1, special characters, paste from clipboard with formatting, browser autofill
- Verify error messages are specific (not "Invalid input") and tell the user how to fix
- Errors should appear inline near the field, not just as a top-of-form summary

**Example finding (Major):** "Phone field accepts any string, posts to backend, backend returns 400 with `{ error: 'invalid_phone' }`. Frontend shows generic 'Failed to save'. Add client-side phone format validation with country-specific examples in the error message."

### F5. Internationalization

**Probe**
- Search the source for hardcoded user-visible strings (`grep -rn '"[A-Za-z][^"]*"' src/`)
- For each, verify it goes through the i18n layer
- Check date, number, currency formats use locale-aware formatters
- If RTL support is in scope, test with `dir="rtl"` applied at root

**Example finding (Polish):** "Button copy 'Save changes' is hardcoded in `SettingsForm.tsx:142`. Move to translation file. Three other strings in the same file have the same issue."

### F6. Performance perception

**Probe**
- Throttle network to "Slow 3G" and interact with the feature
- Note any interaction that produces no feedback within 100ms (button presses, form submits, navigation)
- For lists, verify pagination or virtualization beyond ~100 items

**Example finding (Major):** "Submit button on the form provides no loading state — clicking it during a slow network request shows nothing for 4-6 seconds, leading users to click again and submit twice. Add disabled+spinner state on submit."

## Backend track

### B1. Input validation

**Probe**
- For each endpoint, attempt: empty body, oversized body, wrong content-type, malformed JSON, SQL/NoSQL injection patterns in string fields, integer overflow in numeric fields
- Verify validation happens at the API layer before reaching business logic
- Check that validation errors return 400 with structured error details, not 500 with stack trace

**Example finding (Blocker):** "POST /api/orders accepts `quantity` field as raw number. No upper bound. Sending `quantity: 999999999` triggers a downstream calculation that overflows and returns negative price. Add max bound matching business reality."

### B2. Authorization

**Probe**
- For every endpoint, identify which user roles should access it
- Verify the authorization check is explicit, not implicit (e.g., 'user must own the resource')
- Test with an authenticated user from a different tenant — does the endpoint leak data?
- Distinguish authentication (who you are) from authorization (what you can do) — both are required

**Example finding (Blocker):** "GET /api/credits/:id requires authentication ✓. Does not verify the requesting user owns or has access to the credit record. User A can read credits belonging to User B by guessing IDs."

### B3. Concurrency

**Probe**
- For each write endpoint, ask: what happens if two concurrent requests modify the same record?
- For multi-step operations (read-then-write), is there a race window?
- For external side effects (email, payment, queue publish), is the operation idempotent — can the same request be retried safely?

**Example finding (Major):** "POST /api/credits/transfer reads source balance, deducts amount, writes back. Two concurrent transfers from the same source can both pass the balance check before either deduction lands, allowing overdraft. Use atomic decrement or row-level lock."

### B4. Error handling

**Probe**
- For each external call (DB, HTTP, queue, cache), verify timeout is set explicitly
- Verify retry policy: which errors retry, with what backoff, with what maximum
- Verify failure mode: when the external call ultimately fails, does the user see a meaningful response and does the system remain consistent?

**Example finding (Major):** "Email send via SES has no timeout configured (defaults to client default ~120s). A slow SES response blocks the request handler thread. Set explicit 5s timeout, treat timeout as failure, queue for retry rather than failing the whole request."

### B5. Observability

**Probe**
- For each significant operation, list the logs/metrics/traces it should emit
- Verify error paths log with sufficient context (user ID, request ID, relevant entity IDs)
- Verify high-cardinality metrics aren't being emitted (which blow out cost)
- Verify there's at least one trace per request to enable end-to-end debugging

**Example finding (Major):** "Credit transfer endpoint logs only on the happy path. Error path catches and returns 500 with no log. When this endpoint fails in production, no signal exists in observability beyond a generic '500 rate increased' alarm. Add structured error logging with operation, user ID, source/dest IDs."

### B6. Operational hooks

**Probe**
- Can an admin/operator override or undo a record without writing a migration?
- Is there an audit trail for sensitive operations (financial, permissions, deletions)?
- Can the data be exported for a deletion request (regulatory or user)?
- Does the system have a kill switch for the feature in case of incident?

**Example finding (Major):** "Refund endpoint records the refund but no audit trail captures the operator who initiated it. For financial operations, audit trail is typically a compliance requirement. Add `actor_id`, `actor_type`, `reason` fields to the refund record."
