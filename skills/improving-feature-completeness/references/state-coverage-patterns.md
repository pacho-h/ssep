# UI State Coverage Patterns

A taxonomy of states a UI surface can be in, with implementation hints per state.

## The full state set

For any view that fetches or mutates data:

- `idle` — before any fetch/mutation has been initiated
- `loading-initial` — first fetch in progress, no prior data
- `loading-refresh` — fetch in progress with prior data shown stale
- `loading-paginated` — fetch in progress for next page, prior pages shown
- `success-empty` — fetch succeeded, response was empty (zero records)
- `success-populated` — fetch succeeded, response had data
- `success-partial` — fetch succeeded, but some sub-resource failed (e.g., main list loaded, related counts failed)
- `error-recoverable` — fetch failed, retry might work (network error, 5xx, timeout)
- `error-fatal` — fetch failed, retry won't help (404, 403, malformed data)
- `error-stale` — fetch failed, but cached/prior data is still being shown
- `optimistic` — write in progress, UI showing the predicted post-write state
- `optimistic-rollback` — write failed, UI reverting to pre-write state with error message

A naive implementation handles `loading-initial`, `success-populated`, and `error-recoverable`. The other 8 states are where polish lives.

## Per-state implementation hints

### Loading states
- `loading-initial`: use skeleton matching the eventual layout, not a generic spinner — preserves perceived stability
- `loading-refresh`: keep prior data visible, show a subtle in-place indicator (top progress bar, fade) — don't blank the screen
- `loading-paginated`: append a smaller spinner at the load-more boundary, don't reset scroll position

### Empty states
- `success-empty` first encounter: illustration + heading + helper text + primary CTA (e.g., "Create your first order")
- `success-empty` after filter: same layout but with "No results match your filter" + secondary CTA "Clear filter"
- Distinguish "no data because new account" from "no data because filter excludes everything"

### Error states
- `error-recoverable`: retry button + brief explanation ("Connection issue, please try again")
- `error-fatal`: explanation of what cannot be done + path forward ("This page no longer exists. Go to home.")
- `error-stale`: keep prior data visible with a non-blocking banner ("Showing data from 5 minutes ago — refresh failed")

### Optimistic states
- `optimistic`: show the user's expected outcome immediately, with a subtle indicator that it's pending
- `optimistic-rollback`: revert UI to pre-write state, show toast/inline error explaining what happened — don't silently roll back

## Quick audit script

For each view in the audit scope, complete this matrix:

| State | Implemented? | If yes, link to design / screenshot | If no, finding ID |
|---|---|---|---|
| loading-initial | ? | ? | ? |
| success-empty | ? | ? | ? |
| ... | ... | ... | ... |
