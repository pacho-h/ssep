# Playwright Patterns (via Playwright MCP)

The Playwright MCP server exposes browser control as tools (`browser_navigate`, `browser_click`, `browser_snapshot`, etc.). This skill uses those directly during a Claude session, and the same patterns translate to authored Playwright test files for CI.

## Selector strategy

In order of preference:

1. **Accessible role + name:** `getByRole('button', { name: 'Submit' })` — matches what screen readers see, survives styling refactors
2. **Test ID:** `getByTestId('submit-btn')` — explicit contract between test and code
3. **Text content:** `getByText('Submit')` — works but fragile to copy changes (and bad for i18n tests)
4. **CSS selector:** `[data-component="submit"]` — last resort

Avoid: brittle selectors like `.btn.btn-primary > span:nth-child(2)`. They break with every CSS refactor.

When using `browser_snapshot`, the returned tree shows accessible roles and names — use those as your selector basis for `browser_click` etc.

## Waiting, not sleeping

Playwright's auto-waiting handles most cases. When manual waits are needed:

- **Wait for element:** `browser_wait_for(text: "Order confirmed")` — waits for visible text
- **Wait for network:** Inspect `browser_network_requests()` for the expected response
- **Wait for state:** `browser_evaluate(() => window.appReady === true)` — for app-specific readiness

Never use a fixed `sleep(N)` — either it's longer than needed (slow CI) or shorter than needed (flake).

## Network mocking

When a flow depends on a third-party service that shouldn't be hit in tests (payment provider, email service):

- Stub the network response at the route level (use `page.route()` in authored tests, or run the system under test against a sandbox endpoint)
- Verify the call was made and parameters are correct via `browser_network_requests()`

For internal services, prefer real calls — the integration is part of what's being tested.

## Failure diagnostics

When a Playwright assertion fails, capture before exiting the test:

```
1. browser_take_screenshot()        → visual state at failure
2. browser_snapshot()                → accessibility tree (often shows missing/extra elements)
3. browser_console_messages()        → runtime errors that may have caused the failure
4. browser_network_requests()        → failed XHR / fetch calls
5. (if logs accessible) tail server logs at the timestamp of failure
```

Save these as artifacts (CI usually has a `test-results/` directory). A flaky failure with no artifacts is wasted CI cycles.

## Common pitfalls

- **Testing the third party.** A test asserting the email arrived in the user's inbox tests Gmail, not your code. Assert that your service queued the email; trust the email service to deliver.
- **Selectors coupled to layout.** `nav > ul > li:first-child` breaks when nav restructures. Use roles or test IDs.
- **One mega-test for the whole flow.** When it fails, you have no idea where. Split into focused tests for each meaningful sub-flow.
- **Skipping the "see it fail" step.** A green test you've never seen red doesn't actually prove anything. Break the implementation to confirm the test catches it before pairing them.

## Skeleton (Playwright Test, adapt for project)

```typescript
import { test, expect } from '@playwright/test';

test('user completes checkout for cart with one item', async ({ page }) => {
  await loginAs(page, 'test-user@example.com');
  await page.goto('/products/sku-123');
  await page.getByRole('button', { name: 'Add to cart' }).click();
  await page.getByRole('link', { name: 'Cart' }).click();
  await page.getByRole('button', { name: 'Checkout' }).click();
  await page.getByLabel('Card number').fill('4242424242424242');
  await page.getByLabel('Expiry').fill('12/30');
  await page.getByLabel('CVC').fill('123');
  await page.getByRole('button', { name: 'Place order' }).click();
  await expect(page.getByRole('heading', { name: 'Order confirmed' })).toBeVisible();
  await expect(page).toHaveURL(/\/orders\/[a-z0-9-]+$/);
});
```

## Live-session usage (Playwright MCP, not authored test file)

When using this skill in-session for ad-hoc verification (rather than authoring a CI test), the same primitives apply but the workflow is interactive:

1. `browser_navigate` to the page
2. `browser_snapshot` to see the current accessibility tree
3. Take action (`browser_click`, `browser_type`, etc.) using refs from the snapshot
4. Verify state (snapshot again, or `browser_evaluate` for specific values)
5. Capture screenshots at decision points so the user has visual evidence in the conversation

Live-session checks are *exploration*, not regression tests. If the behavior should be re-verified later, author a Playwright Test file from the same steps.
