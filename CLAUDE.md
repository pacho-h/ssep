# ssep plugin

This directory is a Claude Code plugin providing four specialized SE skills (spec review, design fidelity, feature completeness, integration testing).

## When working in this directory

- All four skills follow the same structural conventions: `SKILL.md` ≤120 lines + `references/*.md` for deep content. Preserve this when editing.
- Frontmatter must include `allowed-tools` listing only the tools each skill actually invokes — keeps permission surface minimal.
- Descriptions are 3rd-person ("Reviews ...", "Authors ...") not 2nd-person ("You MUST ..."), matching official Claude Code skill guidelines.
- Each skill explicitly cross-references `superpowers` for adjacent responsibilities so the two plugins compose without overlap.

## Verifying changes

After editing any `SKILL.md`:

1. Confirm frontmatter parses (no missing `---`, no tab characters, valid YAML)
2. Run `wc -l skills/*/SKILL.md` and confirm all are under ~150 lines (hard limit ~500)
3. Confirm every `references/*.md` linked from the SKILL.md actually exists

## Roadmap

- v0.2: optimize each skill's description via `skill-creator`'s trigger-eval loop (run_loop.py)
- v0.3: add evals/ directory per skill with realistic test prompts
- v0.4: add an `agents/` directory for specialized subagents (e.g., spec-reviewer agent that wraps the spec-review skill in a constrained context window)
