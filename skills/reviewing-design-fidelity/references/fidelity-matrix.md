# Fidelity Matrix — Seven Dimensions

## Table of contents

1. [Layout & spacing](#1-layout--spacing)
2. [Typography](#2-typography)
3. [Color](#3-color)
4. [Iconography & imagery](#4-iconography--imagery)
5. [State coverage](#5-state-coverage)
6. [Responsive behavior](#6-responsive-behavior)
7. [Accessibility](#7-accessibility)

---

## 1. Layout & spacing

Padding, margin, gap, border radius, alignment.

**How to check**
- Read computed styles with `browser_evaluate` for key elements
- Compare to Figma tokens from `get_variable_defs`
- For spacing tokens (e.g., `space-4` = 16px), verify the implementation uses the token, not a hardcoded value

**Example finding (Major):** "Card padding implements `padding: 14px` (computed). Figma frame `123:456` uses token `space-md` which resolves to 16px. 2px drift."

## 2. Typography

Font family, weight, size, line-height, letter-spacing, text-transform.

**How to check**
- Computed `font-family`, `font-size`, `font-weight`, `line-height`, `letter-spacing`
- Verify font has actually loaded (`document.fonts.check()` via `browser_evaluate`)
- Console errors for missing font files

**Example finding (Critical):** "Heading uses `font-family: -apple-system, sans-serif` (computed). Design specifies `Pretendard`. Console shows 'Failed to load font: Pretendard.woff2 (404)'. Users see system fallback."

## 3. Color

Fills, strokes, text color, background color, gradients, opacity.

**How to check**
- Computed `color`, `background-color`, `border-color`, `box-shadow`
- Token resolution comparison
- Contrast ratio for text-on-background pairs (covered also under Accessibility)

**Example finding (Minor):** "Button uses `background-color: rgb(37, 99, 235)`. Figma token `color-primary-500` resolves to the same value. Implementation hardcodes the hex; should reference the token for theme support."

## 4. Iconography & imagery

Correct asset, correct size, correct positioning, correct color (for monochrome icons).

**How to check**
- Inspect `src` attributes for `<img>`, `<source>`, `<svg>` content
- Verify icon component prop matches Figma component name
- Check responsive image variants (`srcset`)

**Example finding (Major):** "Avatar placeholder uses `<svg>` of an outlined person. Figma frame uses `Icon/User/Filled`. Different visual weight changes the perceived hierarchy of the row."

## 5. State coverage

Hover, focus, active, disabled, loading, empty, error.

**How to check**
- Drive each state via Playwright (hover, tab, click, network mock)
- For each state Figma defines a variant for, confirm implementation produces the same visual

**Example finding (Critical):** "List shows correct rendering for populated state. Empty state (zero items) renders as a blank white area. Figma frame `123:789` defines an empty-state illustration with helper text and CTA. Empty state implementation missing."

## 6. Responsive behavior

Design intent preserved across breakpoints.

**How to check**
- Capture at every viewport the design covers
- For each breakpoint, compare implementation vs Figma frame at that width

**Example finding (Major):** "At 375px viewport, navigation collapses to hamburger menu (matches design). At 768px viewport, design shows tabs visible inline; implementation keeps the hamburger until 1024px. Tablet users get mobile UI."

## 7. Accessibility

Contrast ratio, focus visibility, semantic structure, alt text, keyboard reachability.

**How to check**
- WCAG 2.1 AA contrast minimums: 4.5:1 for normal text, 3:1 for large text and UI elements
- `browser_snapshot` returns the accessibility tree — verify roles, labels, headings present
- Tab through the page (`browser_press_key("Tab")`) — every interactive element should receive a visible focus indicator
- Verify `alt` attribute presence and meaningfulness on images

**Example finding (Critical):** "Buy button uses `color: #ffffff` on `background-color: #fbbf24`. Contrast ratio is 1.95:1 — fails WCAG AA (requires 4.5:1). Either darken background or use a darker foreground."

**Example finding (Major):** "Snapshot shows three `<div role='button'>` elements with no accessible name. Keyboard users cannot identify the button's purpose. Add `aria-label` or use a `<button>` element with text content."
