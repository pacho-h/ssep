# Changelog

All notable changes to ssep are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `reviewing-design-fidelity/references/skill-handoff.md` — explicit hand-off matrix from fidelity review to `improving-feature-completeness` (state/coverage gaps), `running-integration-tests` (BE contract drift / route bugs), and `reviewing-spec-and-policy` (design-side defects). Lists chain anti-patterns and `superpowers` composition paths.
- State coverage checklist in `reviewing-design-fidelity/references/playwright-capture.md` — explicit table covering default / empty / loading / error / hover / focus / active / disabled / long-content states with triggers and rationale; warns against synthetic-event clicks that don't update React state.
- Embedding-evidence-in-PRs section in `reviewing-design-fidelity/references/fidelity-report-template.md` — guidance on saving captures to non-temporary paths, embedding before/after pairs in the PR body, and integrating with screenshot-upload workflows. Adds a new anti-pattern entry.
- Route-matching integration-test pattern in `running-integration-tests/references/integration-test-patterns.md` — supertest example for the static-vs-dynamic-route collision case (e.g. NestJS `:itemIdx` swallowing `scope-catalog`), with the rationale that handler-unit tests cannot catch this class of bug.

### Changed
- `reviewing-design-fidelity/SKILL.md` workflow gains a Step 7 ("Hand off to the next skill") and Step 6 now links to the PR-embed guidance.

## [0.1.3] — 2026-04-17

### Changed
- Skill descriptions expanded with additional Korean trigger phrases and proactive activation hints to improve matcher recall:
  - `reviewing-design-fidelity`: added "피그마 비교해서 차이점 찾아줘", "figma vs 현재 화면", "구현이 디자인과 맞는지", "피그마대로 되어있나", "현황과 비교", "figma url 과 현재 화면 대조"
  - `reviewing-spec-and-policy`: added "이 기획대로 구현하면 빠진게 뭐가 있을까", "스펙 갭", "요구사항 누락", "기획서 애매한 부분"; clarified distinction vs `reviewing-design-fidelity`
  - `improving-feature-completeness`: added "엣지 케이스 다 챙겼나", "PR 전 점검", "빠진 상태 없나", "ship 전 검토"; added proactive trigger note for pre-PR moments on non-trivial feature branches
  - `running-integration-tests`: added "staging에서 확인", "staging 검증", "배포 후 검증", "실제 화면에서 확인", "smoke test"; added proactive trigger for deployed-feature verification and unchecked PR test-plan items

## [0.1.2] — 2026-04-17

### Fixed
- README version badge returned 404 (shields.io static badge missing color segment); replaced with dynamic GitHub tag badge that auto-syncs with released tags

### Changed
- Full name: `Super Software Engineering Power` → `Super Software Engineering Powers` across README title, `plugin.json` description, and `marketplace.json` metadata/plugin descriptions

## [0.1.1] — 2026-04-17

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
