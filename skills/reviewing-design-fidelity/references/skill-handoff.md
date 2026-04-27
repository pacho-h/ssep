# Skill Hand-off Matrix

A fidelity review almost always uncovers issues that aren't fidelity issues. They show up as side observations during capture — the API errored, the empty state wasn't designed, the BE behaviour suggests a route/contract bug, the spec itself was ambiguous.

Resolving those silently inside this skill makes the work invisible and untraceable. Instead, route each side-finding to the skill that's actually responsible for it. The user (and any reviewer reading later) then sees a clear chain: design fidelity → completeness audit → integration coverage → spec correction.

## Trigger matrix

When you observe one of these signals during a fidelity review, hand off to the listed skill rather than fixing in place.

| Signal observed during fidelity review | Hand-off skill | Reason |
|---|---|---|
| Empty / loading / error state never implemented (not just visually wrong — missing entirely) | `improving-feature-completeness` | Production-readiness audit covers state coverage holistically; one missing state is usually a symptom of more |
| Implementation handles happy path but throws on edge inputs (long strings, NaN dates, null fields) | `improving-feature-completeness` | Same skill audits realistic-worst-case input handling |
| Console / network shows the BE returned an unexpected status, body shape, or path mismatch | `running-integration-tests` | Add a contract / integration test asserting on the boundary, so the regression is caught next time without re-running the visual review |
| Discovery: a backend route / controller change is needed to make the page work | `running-integration-tests` | Backend behavioural change demands a real-boundary test; unit-level mocks cannot prove route matching, request shape, or DB state |
| Design itself is incomplete or contradictory (no empty-state spec, conflicting tokens, missing variant) | `reviewing-spec-and-policy` | The defect is upstream of implementation — file it against the spec, not the code |
| The fix requires net-new design (e.g. spec only had desktop, mobile is needed) | back to the designer + `reviewing-spec-and-policy` for the new spec | Don't invent design inside a fidelity review |
| Drift is a one-line CSS token swap and nothing else surfaces | (no hand-off) | Just fix it — the chain is overhead when there's no chain to extend |

## Hand-off form

When you do hand off, do it explicitly so the chain is recorded:

1. Finish the fidelity report with the side-findings listed under "Coverage gaps" or a dedicated "Out of scope" subsection.
2. Reference the next skill by name in that subsection: "→ delegated to `improving-feature-completeness`" / "→ requires `running-integration-tests` regression test".
3. Invoke that skill in the same session if the user wants the chain executed now, or note it as a follow-up if the user wants a smaller PR.

## Chain anti-patterns

❌ Fixing a missing empty state inside a fidelity-review patch without invoking `improving-feature-completeness`. The fix may be correct in isolation but the underlying coverage gap (likely many missing states) goes unaudited.

❌ Quietly editing a backend controller to make the page render, with no integration test added. The next migration / refactor reintroduces the bug because nothing pins the contract.

❌ Treating the fidelity skill as a catch-all "make the page right". This skill is a *visual-diff auditor*. Behavioural correctness, completeness, and contract pinning are deliberate adjacent skills.

## Composition with `superpowers`

The chain above stays within ssep. Composition with `superpowers` is also possible — examples:

- After `running-integration-tests` writes a failing integration test, `superpowers:test-driven-development` drives the implementation.
- After `improving-feature-completeness` enumerates gaps, `superpowers:writing-plans` turns the gap list into an implementation plan if the work spans a session.
- Before any of the above, if the user wants a structured PR review of the fix bundle, `superpowers:requesting-code-review` runs against the full diff once each ssep step is complete.

These compositions are deliberate — the two plugins do not duplicate, and chaining them only adds friction when the user already knows the path. If unsure, propose the chain and let the user accept or skip.
