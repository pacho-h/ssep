# Fidelity Report Template

```markdown
# Design Fidelity Review: <feature name>

**Reviewed:** <YYYY-MM-DD>
**Design source:** <Figma URL>
**Implementation source:** <live URL or build path>
**Viewports captured:** <list>
**States captured per viewport:** <list>

## Summary

- Critical: N | Major: N | Minor: N
- Coverage: <X> of <Y> Figma frames reviewed
- Top 3 user-visible issues:
  1. ...

## Critical findings

### [C-1] <short title>

**Frame:** Figma node `<fileKey>:<nodeId>` (link)
**Implementation:** <URL> @ <viewport>, state: <state>
**Dimension:** <Layout / Typography / Color / Iconography / State / Responsive / A11y>

**Evidence:**
- Figma screenshot: <path>
- Implementation screenshot: <path>
- Computed values: <quoted output from browser_evaluate, if relevant>
- Console messages: <quoted, if relevant>

**Drift:** <concrete description of difference, with measurements>

**Suggested fix:** <token name, CSS property change, or component prop change — minimal change to close the gap>

---

(repeat for each critical finding)

## Major findings

(same structure, prefix [M-N])

## Minor findings

(same structure, prefix [N-N])

## Design-side issues (separate from implementation)

Items where implementation revealed a problem with the design itself:
- <issue> — <description, why it's a design issue not an impl issue>

## Coverage gaps

Frames or states not reviewed and why:
- <frame> — <reason (e.g., "no implementation yet", "out of scope per user")>
```

## Anti-patterns

❌ Findings without artifact references — "the spacing looks off" is not a finding.

❌ Mixing impl drift with design preferences — "I'd prefer more contrast" goes in a separate suggestions doc, not the fidelity report.

❌ Reporting raw pixel measurements without comparing to the design token — "padding is 14px" is meaningless without "design specifies `space-md` = 16px".

❌ Reviewing only the desktop viewport — most production users are mobile.
