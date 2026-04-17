# Playwright Capture Patterns

## Viewport matrix

Match each captured viewport to a Figma frame width. Common matrix:

| Device class | Width | Typical Figma frame width |
|---|---|---|
| Mobile small | 375 | 375 |
| Mobile large | 414 | 414 |
| Tablet | 768 | 768 |
| Desktop | 1440 | 1440 |
| Wide | 1920 | 1920 |

Skip viewports the design doesn't explicitly cover — a "wide" capture without a wide design frame produces noise, not findings.

## State capture sequence

For a single page at one viewport, the standard capture sequence is:

```
1. browser_navigate(url)
2. browser_take_screenshot()        → default
3. browser_snapshot()               → a11y tree default
4. browser_console_messages()       → capture rendering errors
5. For each interactive element being reviewed:
   a. browser_hover(ref)            → hover state
   b. browser_take_screenshot()
   c. browser_click(ref)            → active/clicked state
   d. browser_take_screenshot()
   e. (if focusable) browser_press_key("Tab") → focus visibility
   f. browser_take_screenshot()
```

For loading/empty/error states, drive the page into that state first (e.g., navigate with a query param, intercept the network response, or seed the test data) before snapshotting.

## Console errors as findings

Every console error captured during page load is a fidelity finding even if visually invisible. Common high-impact cases:
- `Failed to load resource: 404` for an image → broken asset
- `font-family ... was not found` → font fallback in use, typography fidelity broken
- React/framework warnings about missing keys or accessibility attributes → state coverage / a11y findings

Quote the exact console message in the finding.

## Computed style verification

When a visual difference is suspected but unclear, use `browser_evaluate` to read the computed style:

```js
() => {
  const el = document.querySelector('selector');
  const cs = getComputedStyle(el);
  return {
    color: cs.color,
    backgroundColor: cs.backgroundColor,
    fontSize: cs.fontSize,
    fontFamily: cs.fontFamily,
    padding: cs.padding,
  };
}
```

Compare against the Figma token values from `get_variable_defs`. This converts "looks slightly off" into "is `#3b82f6` but token `color-primary-500` resolves to `#2563eb`".
