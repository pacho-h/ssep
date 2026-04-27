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

## Embedding evidence in PRs

When a fidelity review leads to an actual PR (the fix), the captured screenshots are the strongest review artifact. Reviewers should not have to re-run the skill to see what was wrong vs what was fixed.

Treat the captures as PR-grade artifacts:

- Save under a known, non-temporary path (e.g. the project's `.playwright-mcp/` output directory or a dedicated `docs/fidelity/<YYYY-MM-DD>/` folder).
- Embed each major finding's before/after pair directly in the PR body:

  ```markdown
  ### Before (Figma) vs After (impl)
  | Figma | Implementation |
  |---|---|
  | ![figma](path/figma-frame.png) | ![impl](path/impl-screenshot.png) |
  ```

- If the host (e.g. GitHub) requires uploaded asset URLs, drag-drop the PNGs into the PR description editor — GitHub auto-uploads to its asset CDN and stable URLs replace the local paths.
- For repos with an established screenshot-upload workflow (e.g. a `fix-pr` or `commit-and-pr` skill that handles upload), use that — duplicate paths between the fidelity report and the PR body without re-uploading.

Anti-pattern: linking to local `/tmp/...` paths in the PR body. The reviewer cannot read those, and the files vanish on machine reboot.

## Anti-patterns

❌ Findings without artifact references — "the spacing looks off" is not a finding.

❌ Mixing impl drift with design preferences — "I'd prefer more contrast" goes in a separate suggestions doc, not the fidelity report.

❌ Reporting raw pixel measurements without comparing to the design token — "padding is 14px" is meaningless without "design specifies `space-md` = 16px".

❌ Reviewing only the desktop viewport — most production users are mobile.

❌ Producing a fidelity report and a PR but never linking captures into the PR body — reviewers re-do the work or rubber-stamp it.
