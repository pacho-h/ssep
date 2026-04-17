# ssep — Super Software Engineering Power

A Claude Code plugin that adds specialized software engineering skills focused on the parts of the workflow that need **structured judgment** — spec review, design fidelity verification, production-readiness audits, and multi-layer testing.

ssep is designed to **complement** the [`superpowers`](https://github.com/obra/superpowers) plugin, not replace it. Use `superpowers` for the universal disciplines (TDD, debugging, code review, planning); use ssep for the specialized review and verification work that superpowers doesn't cover.

## Skills included

| Skill | What it does | Triggers on |
|---|---|---|
| `reviewing-spec-and-policy` | Audits PRDs, RFCs, requirement docs, policies — from text or Figma sources — for completeness, consistency, edge cases, policy compliance. | "review this spec", "기획서 검토", "PRD audit", Figma planning URLs |
| `reviewing-design-fidelity` | Compares implemented UI to Figma source via Playwright + Figma MCP. Reports drift in spacing, color, typography, state coverage, responsive behavior, accessibility. | "퍼블리싱 검토", "design QA", "compare with figma", "픽셀 비교" |
| `improving-feature-completeness` | Production-readiness audit. Surfaces the gap between "happy path passes" and "ready to ship" — edge cases, loading/empty/error states, a11y, i18n, observability, ops hooks. | "완성도 점검", "production ready", "polish this feature", "edge case 검토" |
| `running-integration-tests` | Authors and runs unit/integration/end-to-end tests with Playwright MCP. Includes the meta-decision of which test level fits which scenario. | "통합 테스트", "e2e 테스트", "playwright로 검증", "integration test" |

## Why this exists

The `superpowers` plugin covers the universal SE workflow disciplines (TDD, debugging, code review, planning). It does **not** cover:

1. **Pre-implementation review** — spec/policy/design audits before code is written
2. **Post-implementation polish** — the gap between green tests and a shippable feature
3. **Multi-layer testing decisions** — when to write unit vs integration vs e2e

ssep adds focused skills for those gaps, while delegating everything else to `superpowers`.

## Design principles

ssep applies the [official Claude Code skill authoring guidelines](https://code.claude.com/docs/en/skills) more strictly than most community plugins:

- **`allowed-tools` declared per skill** — minimum-privilege tool surface, no permission-prompt spam
- **Progressive disclosure** — every `SKILL.md` is ≤ 110 lines; deep checklists, templates, and decision trees live in linked `references/*.md` files loaded only when relevant
- **Third-person descriptions** — "Reviews specs..." not "You MUST review..."
- **Explicit boundaries** — every skill includes a `When NOT to use` section pointing at the right alternative (often a `superpowers:*` skill)
- **WHY over MUST** — each skill explains the rationale for its discipline so the model can extend the principle to edge cases

## Installation

### Prerequisites

- [Claude Code](https://docs.claude.com/en/docs/claude-code) installed
- (Recommended) `superpowers` plugin installed for the complementary universal skills
- (For full functionality) [Figma MCP](https://help.figma.com/hc/en-us/articles/32132100833559) and [Playwright MCP](https://github.com/microsoft/playwright-mcp) configured

### Add the marketplace

In your `~/.claude/settings.json`, add to `extraKnownMarketplaces`:

```json
{
  "extraKnownMarketplaces": {
    "ssep": {
      "source": {
        "source": "github",
        "repo": "pacho-h/ssep"
      },
      "autoUpdate": true
    }
  }
}
```

### Enable the plugin

In the same `~/.claude/settings.json`, add to `enabledPlugins`:

```json
{
  "enabledPlugins": {
    "ssep@ssep": true
  }
}
```

Then run `/reload-plugins` in Claude Code (or restart the session).

### Verify installation

The four skills should appear under their slash-command form:
- `/reviewing-spec-and-policy`
- `/reviewing-design-fidelity`
- `/improving-feature-completeness`
- `/running-integration-tests`

You can also trigger them with natural language: "이 PRD 검토해줘", "퍼블리싱 검수 부탁", "완성도 점검", "통합 테스트 짜줘".

## Workflow composition with `superpowers`

A typical full feature lifecycle composes ssep + superpowers skills:

```
┌─────────────────────────────────────────────────────────────────┐
│ ssep:reviewing-spec-and-policy                                  │
│   → audit the PRD before any work starts                        │
└─────────────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────────────┐
│ superpowers:brainstorming → superpowers:writing-plans           │
│   → design the implementation                                   │
└─────────────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────────────┐
│ superpowers:test-driven-development                              │
│   → implement with unit-level discipline                        │
└─────────────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────────────┐
│ ssep:running-integration-tests                                  │
│   → add integration / e2e coverage                              │
└─────────────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────────────┐
│ ssep:reviewing-design-fidelity (if UI work)                     │
│   → verify against Figma source                                 │
└─────────────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────────────┐
│ ssep:improving-feature-completeness                             │
│   → close the works→ships gap                                   │
└─────────────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────────────┐
│ superpowers:requesting-code-review                              │
│   → final review before merge                                   │
└─────────────────────────────────────────────────────────────────┘
```

Each skill knows where its responsibility ends — they don't overlap.

## MCP dependencies

These skills assume the following MCP servers may be available; they fall back to manual workflows when not:

- **`figma`** — required for `reviewing-spec-and-policy` (Figma sources) and `reviewing-design-fidelity` (design extraction)
- **`playwright`** — required for `reviewing-design-fidelity` (impl capture) and `running-integration-tests` (browser automation)

If neither MCP is configured, the skills still produce usable output but lose their primary capture-and-compare value.

## Roadmap

- **v0.2** — optimize each skill's `description` via `skill-creator`'s `run_loop.py` against the included trigger eval sets (currently shipped at `skills/*/evals/trigger-eval.json`)
- **v0.3** — run output-quality evals (cases at `skills/*/evals/evals.json`) and refine SKILL.md content based on real-world results
- **v0.4** — add specialized subagents (e.g., dedicated `spec-reviewer` agent that wraps the spec-review skill in a constrained context window)

## Contributing

Issues and pull requests welcome. Please:

1. Read the [skill authoring conventions in `CLAUDE.md`](./CLAUDE.md) before editing any `SKILL.md`
2. Keep `SKILL.md` files under ~150 lines (hard limit ~500); push deep content to `references/`
3. Preserve the `When NOT to use` section — it's how the plugin stays scoped
4. Add a CHANGELOG entry for every user-visible change

## License

[MIT](./LICENSE)
