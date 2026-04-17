# Changelog

All notable changes to ssep are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Installation guide expanded: three install methods (`/plugin` UI, CLI, manual `settings.json`), explicit Update/Uninstall section, Troubleshooting table for common gotchas (cache, version, project overrides, MCP availability, autoUpdate)
- README badges (license, version, Claude Code plugin, lint status)
- Strengthened `Acknowledgments` section explicitly crediting `superpowers` (Jesse Vincent / claude-plugins-official) for design philosophy and skill anatomy
- GitHub Actions `lint.yml` workflow validating `marketplace.json`, `plugin.json`, all `SKILL.md` frontmatter (name regex, description length, body line limits, references existence), and all eval JSON files on every push and PR
- GitHub Discussions enabled for user feedback

### Changed
- README now fully English (Korean trigger phrases moved to skill descriptions only)

## [0.1.0] — 2026-04-17

Initial release.

### Added
- `reviewing-spec-and-policy` — spec/PRD/policy review from text and Figma sources
- `reviewing-design-fidelity` — implemented UI vs Figma design comparison via Playwright + Figma MCP
- `improving-feature-completeness` — production-readiness audit (states, a11y, observability, ops hooks)
- `running-integration-tests` — multi-layer test authoring with Playwright MCP
- Trigger eval sets per skill (20 queries each, 50/50 should/should-not split) for future description optimization
- Output quality eval cases per skill (`evals/evals.json`)

### Design choices vs `superpowers`
- 3rd-person skill descriptions
- `allowed-tools` declared per skill (minimum-privilege tool surface)
- Progressive disclosure: each `SKILL.md` ≤ 110 lines, deep content in `references/`
- Explicit `When NOT to use` section in every skill to define boundaries with adjacent skills (notably `superpowers:*`)

### Not yet done
- Description optimization via `skill-creator`'s `run_loop.py` — trigger eval sets are prepared; running the loop requires an Anthropic API key
- Real-world output quality validation against the eval cases
