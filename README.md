# ssep — Super Software Engineering Power

[![License: MIT](https://img.shields.io/github/license/pacho-h/ssep?color=blue)](./LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-orange)](./CHANGELOG.md)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-7C3AED?logo=anthropic&logoColor=white)](https://docs.claude.com/en/docs/claude-code/plugins)
[![Lint](https://github.com/pacho-h/ssep/actions/workflows/lint.yml/badge.svg)](https://github.com/pacho-h/ssep/actions/workflows/lint.yml)

A Claude Code plugin that adds specialized software engineering skills focused on the parts of the workflow that need **structured judgment** — spec review, design fidelity verification, production-readiness audits, and multi-layer testing.

ssep is designed to **complement** the [`superpowers`](https://github.com/obra/superpowers) plugin by [Jesse Vincent](https://github.com/obra), not replace it. Use `superpowers` for the universal disciplines (TDD, debugging, code review, planning); use ssep for the specialized review and verification work that superpowers doesn't cover. See [Acknowledgments](#acknowledgments) for more.

## Skills included

| Skill | What it does | Triggers on |
|---|---|---|
| `reviewing-spec-and-policy` | Audits PRDs, RFCs, requirement docs, policies — from text or Figma sources — for completeness, consistency, edge cases, policy compliance. | "review this spec", "audit this PRD", "check requirements", Figma planning URLs |
| `reviewing-design-fidelity` | Compares implemented UI to Figma source via Playwright + Figma MCP. Reports drift in spacing, color, typography, state coverage, responsive behavior, accessibility. | "design QA", "compare with figma", "pixel comparison", "publishing review" |
| `improving-feature-completeness` | Production-readiness audit. Surfaces the gap between "happy path passes" and "ready to ship" — edge cases, loading/empty/error states, a11y, i18n, observability, ops hooks. | "production ready check", "polish this feature", "edge case review", "ship readiness" |
| `running-integration-tests` | Authors and runs unit/integration/end-to-end tests with Playwright MCP. Includes the meta-decision of which test level fits which scenario. | "integration test", "e2e test", "verify with playwright", "browser test" |

> Skill descriptions also include localized trigger phrases (currently English + Korean) so bilingual teams can trigger skills in either language.

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

- [Claude Code](https://docs.claude.com/en/docs/claude-code) installed (plugin system requires v2.x or later — run `claude --version` to check)
- (Recommended) [`superpowers`](https://github.com/obra/superpowers) plugin installed for the complementary universal skills
- (For full functionality) [Figma MCP](https://help.figma.com/hc/en-us/articles/32132100833559) and [Playwright MCP](https://github.com/microsoft/playwright-mcp) configured

### Install (pick one of three methods)

#### Method 1 — Interactive `/plugin` UI (recommended)

The fastest path. Inside any Claude Code session:

1. Run `/plugin` to open the plugin manager
2. Open the **Marketplaces** tab → **Add marketplace** → choose **GitHub** → enter `pacho-h/ssep`
3. Switch to the **Discover** tab → click **Install** on `ssep`
4. Skills are immediately available; no restart required

#### Method 2 — CLI

If you prefer the terminal:

```bash
claude plugin marketplace add github:pacho-h/ssep
claude plugin install ssep@ssep
```

#### Method 3 — Manual `~/.claude/settings.json` edit

If you manage your Claude Code config as code, merge the following into `~/.claude/settings.json` (preserve any existing keys):

```json
{
  "extraKnownMarketplaces": {
    "ssep": {
      "source": { "source": "github", "repo": "pacho-h/ssep" },
      "autoUpdate": true
    }
  },
  "enabledPlugins": {
    "ssep@ssep": true
  }
}
```

Then run `/reload-plugins` inside Claude Code (required after manual settings edits).

### Verify installation

In Claude Code, run `/plugin list` (or open the **Installed** tab in `/plugin`). You should see `ssep@ssep` listed and the four skills available as slash commands:

- `/reviewing-spec-and-policy`
- `/reviewing-design-fidelity`
- `/improving-feature-completeness`
- `/running-integration-tests`

You can also trigger them with natural language: "review this PRD for me", "do a publishing review on the staging URL", "check production readiness", "write integration tests for this endpoint".

## Updating and uninstalling

| Action | Command / setting |
|---|---|
| Auto-update on session start | Set `autoUpdate: true` in the marketplace config (Method 3 includes this; Methods 1/2 default to false for non-official marketplaces) |
| Manual update | `/plugin marketplace update ssep` or `claude plugin marketplace update ssep` |
| Disable temporarily (keep installed) | `/plugin disable ssep@ssep` |
| Uninstall | `/plugin uninstall ssep@ssep`, or remove the entries from `settings.json` and run `/reload-plugins` |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `/plugin` command not recognized | Older Claude Code version | `claude --version` and update to a recent build (plugin system requires v2.x+) |
| Marketplace fails to load | Network access or invalid manifest | Verify GitHub access; this repo's CI validates `marketplace.json` on every push, so the upstream copy is always schema-valid |
| Skills don't appear after install | Cached marketplace state | Run `/reload-plugins`; if that fails, `rm -rf ~/.claude/plugins/cache` and reinstall |
| Slash commands missing only in one project | Project settings overriding user settings | Check `.claude/settings.local.json` for a conflicting `enabledPlugins` entry |
| Figma / Playwright skills error out | MCP server not configured | Confirm the relevant MCP server is installed; the skills fall back to manual workflows when MCPs are missing but lose their primary capture-and-compare value |
| Auto-update not happening | `autoUpdate: false` (default for non-official marketplaces) | Set `autoUpdate: true` in `extraKnownMarketplaces.ssep.autoUpdate`, or update manually with `/plugin marketplace update ssep` |

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

## Acknowledgments

ssep is built on the shoulders of [`superpowers`](https://github.com/obra/superpowers) by [Jesse Vincent](https://github.com/obra), shipped through the [official Anthropic Claude Code marketplace](https://github.com/anthropics/claude-plugins-official) (`superpowers@claude-plugins-official`).

Several things in ssep wouldn't exist without superpowers:

- **The discipline-first philosophy.** superpowers established that skills work best when they encode hard-won engineering disciplines (TDD, systematic debugging, verification before completion) as rigid workflows rather than loose suggestions. ssep extends the same model to spec review, fidelity review, completeness audit, and test-level decision-making.
- **The composition model.** Each ssep skill explicitly cross-references the `superpowers:*` skill at its boundary (e.g., `improving-feature-completeness` defers to `superpowers:test-driven-development` once a fix is identified). The `When NOT to use` section in every ssep skill points users back to the right superpowers skill when their task crosses the boundary.
- **The skill anatomy.** ssep follows the same `SKILL.md` + `references/` + `evals/` directory structure that superpowers popularized, with the official Claude Code skill guidelines layered on top.

If you only install one Claude Code plugin, install superpowers first. ssep adds the most value when it's complementing — not competing with — that foundation.

## Roadmap

- **v0.2** — optimize each skill's `description` via `skill-creator`'s `run_loop.py` against the included trigger eval sets (currently shipped at `skills/*/evals/trigger-eval.json`)
- **v0.3** — run output-quality evals (cases at `skills/*/evals/evals.json`) and refine SKILL.md content based on real-world results
- **v0.4** — add specialized subagents (e.g., dedicated `spec-reviewer` agent that wraps the spec-review skill in a constrained context window)

## Contributing

Issues, [Discussions](https://github.com/pacho-h/ssep/discussions), and pull requests welcome. Please:

1. Read the [skill authoring conventions in `CLAUDE.md`](./CLAUDE.md) before editing any `SKILL.md`
2. Keep `SKILL.md` files under ~150 lines (hard limit ~500); push deep content to `references/`
3. Preserve the `When NOT to use` section — it's how the plugin stays scoped
4. Add a CHANGELOG entry for every user-visible change
5. CI runs schema validation on `marketplace.json`, `plugin.json`, and every `SKILL.md` frontmatter — make sure your changes pass before opening a PR

## License

[MIT](./LICENSE)
