# ssep plugin

This directory is a Claude Code plugin providing four specialized SE skills (spec review, design fidelity, feature completeness, integration testing).

## When working in this directory

- All four skills follow the same structural conventions: `SKILL.md` ≤120 lines + `references/*.md` for deep content. Preserve this when editing.
- Frontmatter must include `allowed-tools` listing only the tools each skill actually invokes — keeps permission surface minimal.
- Descriptions are 3rd-person ("Reviews ...", "Authors ...") not 2nd-person ("You MUST ..."), matching official Claude Code skill guidelines.
- Each skill explicitly cross-references `superpowers` for adjacent responsibilities so the two plugins compose without overlap.

## Trigger discipline

These skills are most often *skipped* not because the trigger keywords are unclear but because the task looks small in the moment. The descriptions in v0.3.0+ explicitly push back against this rationalization, but contributors editing descriptions or references should preserve and extend the pattern.

Real-session skip rationalizations and the right move:

| Rationalization observed in real sessions | The right move |
|---|---|
| "It's a single-line CSS swap, fidelity check is overkill" | Invoke `reviewing-design-fidelity`. The skill chooses scope; let it decide, not the agent. |
| "The requirement is one sentence, no spec to audit" | Invoke `reviewing-spec-and-policy`. Concise requirements hide unstated edge cases (default values for existing data, role differences, state-transition gaps). |
| "Happy path passed in Playwright, ship it" | Invoke `improving-feature-completeness`. State coverage (empty/loading/error/disabled) and i18n/a11y are not checked by happy-path e2e. |
| "I already clicked through it manually, no integration test needed" | Invoke `running-integration-tests`. Manual click ≠ codified regression. |

Each skill's `## When NOT to use` section defines the *only* legitimate skip cases. If the situation isn't there, invoke the skill — the skill itself decides scope (full audit vs quick check) faster than the caller can rationalize a skip.

When editing skill descriptions, keep one explicit "Triggers even when ..." clause per description that names the dominant rationalization. That clause is what makes the skill harder to skip in agentic sessions where the model is biased toward "looks fast, just do it."

## Verifying changes

After editing any `SKILL.md`:

1. Confirm frontmatter parses (no missing `---`, no tab characters, valid YAML)
2. Run `wc -l skills/*/SKILL.md` and confirm all are under ~150 lines (hard limit ~500)
3. Confirm every `references/*.md` linked from the SKILL.md actually exists

## Roadmap

- v0.2: optimize each skill's description via `skill-creator`'s trigger-eval loop (run_loop.py)
- v0.3: add evals/ directory per skill with realistic test prompts
- v0.4: add an `agents/` directory for specialized subagents (e.g., spec-reviewer agent that wraps the spec-review skill in a constrained context window)
