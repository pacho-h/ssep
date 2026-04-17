---
name: reviewing-design-fidelity
description: Reviews implemented UI against design source-of-truth (Figma frames, mockup images, design system tokens) to verify visual fidelity — spacing, typography, color, responsive behavior, interaction states, and accessibility. Use when comparing built pages to design specs, when a Figma URL is shared alongside a running URL or screenshot, or when user says "디자인 검수", "퍼블리싱 검토", "compare with figma", "check design fidelity", "픽셀 비교", "design QA". Skill captures both sides (Figma extraction + Playwright snapshot of live impl), runs a structured visual diff, and reports gaps prioritized by user-visible impact. Distinct from reviewing-spec-and-policy (which audits docs) and from code review (which audits code structure).
allowed-tools: Read, Glob, Grep, Bash, mcp__plugin_figma_figma__get_design_context, mcp__plugin_figma_figma__get_screenshot, mcp__plugin_figma_figma__get_metadata, mcp__plugin_figma_figma__get_variable_defs, mcp__plugin_figma_figma__get_code_connect_map, mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_snapshot, mcp__plugin_playwright_playwright__browser_take_screenshot, mcp__plugin_playwright_playwright__browser_resize, mcp__plugin_playwright_playwright__browser_evaluate, mcp__plugin_playwright_playwright__browser_console_messages, mcp__plugin_playwright_playwright__browser_hover, mcp__plugin_playwright_playwright__browser_click
---

# Reviewing Design Fidelity

## Purpose

Implementation drifts from design — silently, in small increments, every sprint. Padding shrinks by 2px to fit a label, a hex code gets approximated, a state variant is forgotten. Each drift is invisible alone; together they erode the brand and the design system. This skill performs side-by-side capture and structured comparison so drift is surfaced concretely, with evidence, before it accumulates further.

The skill produces an annotated gap report — not a redesign. It assumes the design is the source of truth and the implementation should match it; if that assumption is wrong (e.g., implementation revealed a design problem), surface that as a separate finding rather than rewriting the design.

## When to use this skill

- A Figma URL is shared together with a live URL or built page screenshot
- User asks to "verify design", "compare with Figma", "check publishing", "디자인 검수", "퍼블리싱 검토", "design QA pass"
- After a frontend feature is implemented and before sign-off
- When the design system maintainer reports drift across a release

## When NOT to use

- Reviewing the design itself (no implementation yet) → use `reviewing-spec-and-policy`
- Reviewing code structure / component APIs → use `superpowers:requesting-code-review`
- Generating new design from code → that's the figma-generate-design skill, not this one

## Workflow

### 1. Identify both sides

Before capturing anything, confirm:
- **Design side:** Figma file URL + specific frame node IDs to review (one frame per screen state, including hover/focus/error/empty if applicable)
- **Implementation side:** live URL OR a path to deployed screenshots OR a local dev server URL

If either side is missing, pause and ask. A one-sided "review" is just an opinion.

### 2. Extract the design context

For each frame:

1. `mcp__plugin_figma_figma__get_metadata` → confirm frame structure and identify variant set
2. `mcp__plugin_figma_figma__get_variable_defs` → pull design tokens (color/spacing/typography) referenced by the frame. These are the canonical values; any drift in implementation should be measured against tokens, not against rendered pixel values, when tokens exist.
3. `mcp__plugin_figma_figma__get_design_context` → structured component data + Code Connect mappings if present
4. `mcp__plugin_figma_figma__get_screenshot` → reference image for the frame

See `references/figma-extraction.md` for tactics on multi-variant frames and Code Connect interpretation.

### 3. Capture the implementation

Use Playwright MCP to capture the live page in matched viewport sizes:

1. `browser_resize` to the design's intended viewport (mobile 375, tablet 768, desktop 1440 — or match the Figma frame width)
2. `browser_navigate` to the page URL
3. `browser_snapshot` for the accessibility tree (text content, ARIA roles, heading structure)
4. `browser_take_screenshot` for visual comparison
5. For interaction states, use `browser_hover` / `browser_click` then re-snapshot to capture hover/active/focus visuals
6. `browser_console_messages` once per page — console errors during rendering are themselves fidelity findings (broken images, missing fonts)

See `references/playwright-capture.md` for state coverage and viewport-matrix patterns.

### 4. Compare across the fidelity matrix

Apply the seven dimensions from `references/fidelity-matrix.md`:

1. **Layout & spacing** — padding, margin, gap match design tokens
2. **Typography** — font family, weight, size, line-height, letter-spacing
3. **Color** — fills, strokes, text — match tokens (not just visually similar)
4. **Iconography & imagery** — correct asset, correct size, correct positioning
5. **State coverage** — hover, focus, active, disabled, loading, empty, error all implemented
6. **Responsive behavior** — design intent preserved at each breakpoint, not just "doesn't crash"
7. **Accessibility** — contrast ratio, focus visibility, semantic structure, alt text, keyboard reachability

Each dimension produces zero or more findings.

### 5. Prioritize by user impact

- **Critical** — broken or unusable (missing state, content overflow that hides info, accessibility blocker)
- **Major** — visibly wrong (color/spacing off enough that a designer would call it out, missing variant)
- **Minor** — token drift not visually detectable but breaks design-system contract (e.g., 14px instead of token `text-sm`/15px)

Skip subjective preference findings ("I'd prefer more whitespace"); only flag drift from the documented design.

### 6. Produce the report

Use the structure in `references/fidelity-report-template.md`. Each finding includes:
- Frame reference (Figma node ID)
- Implementation reference (URL + viewport)
- Side-by-side evidence (screenshot paths or quoted token values)
- Dimension category
- Priority
- Concrete fix suggestion (token name, CSS property, or component prop change)

## Principles

- **Tokens first, pixels second.** A 14px font-size when the design token is `text-sm` (15px) is a finding even if visually indistinguishable — the design system contract is what gets re-rendered when tokens change.
- **Capture all states, not just the default.** Most drift hides in hover/focus/error/empty states because those rarely appear in a happy-path design review.
- **Match viewports.** A "looks fine on my laptop" review misses the 70% of users on other viewports. Capture each breakpoint in the design.
- **Evidence is required.** Every finding must reference a captured artifact (screenshot, snapshot tree, console log, computed style). "It looks off" without artifact = not a finding.
- **Distinguish drift from design conflict.** If implementation reveals a design problem (e.g., text actually overflows in real content), that's a separate finding flagging the design — don't try to silently "fix it" in implementation.

## Detailed references

- `references/figma-extraction.md` — tactics for multi-variant frames, Code Connect mappings, and choosing which frames to review
- `references/playwright-capture.md` — viewport matrix, state-capture sequence, console-error interpretation
- `references/fidelity-matrix.md` — full descriptions and example findings for the seven dimensions
- `references/fidelity-report-template.md` — annotated template with example findings showing artifact references
