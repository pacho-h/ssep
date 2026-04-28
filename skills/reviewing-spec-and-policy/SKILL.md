---
name: reviewing-spec-and-policy
description: Reviews product specs, requirements docs, RFCs, PRDs, and policy documents from text, markdown, or Figma. Use for completeness, consistency, edge-case coverage, ambiguity, policy conflicts, or compliance gaps. Triggers on "이 기획서 검토해줘", "스펙 리뷰", "정책 검토", "review this PRD", "is this complete?", "이 기획대로 구현하면 빠진게 뭐가 있을까", "스펙 갭", "요구사항 누락", or whenever a Figma URL is shared in a planning context. Triggers even when the requirement reads as a single concise sentence (e.g. "X should default to inactive and be activatable from detail"); concise requirements hide unstated questions about default values for existing data, role/permission interactions, and state-transition edges that a structured audit surfaces in minutes. Reads sources, runs a multi-dimensional review, returns a prioritized gap report. Distinct from brainstorming (generates new designs) and reviewing-design-fidelity (compares impl vs design); this audits an existing artifact.
allowed-tools: Read, Grep, Glob, WebFetch, mcp__plugin_figma_figma__get_design_context, mcp__plugin_figma_figma__get_screenshot, mcp__plugin_figma_figma__get_metadata, mcp__plugin_figma_figma__get_variable_defs
---

# Reviewing Specifications and Policies

## Purpose

Specs ship bugs before code does. A missing edge case in a PRD becomes a hotfix in production; an unstated assumption in a policy becomes a compliance incident. This skill performs a structured review of specification artifacts so gaps are surfaced **before** implementation begins, when changes cost minutes instead of weeks.

The skill applies to product requirement docs, RFCs, technical design docs, internal policies, regulatory checklists, and Figma planning files. Output is a prioritized gap report — not a rewrite. Authors keep ownership; reviewers surface what's missing or contradictory.

## When to use this skill

- A user shares a spec/PRD/RFC and asks for review, audit, or "is this ready?"
- A Figma URL appears in planning context (not pure design context — those go to `reviewing-design-fidelity`)
- A user asks to verify a doc against a known policy ("does this comply with our refund policy?", "check against GDPR section X")
- A user mentions terms like 기획서, 요구사항, 정책 검토, spec review, requirements audit, PRD review

## When NOT to use

- Generating a new spec from scratch → use `superpowers:brainstorming`
- Reviewing implemented code against a spec → use `superpowers:requesting-code-review`
- Comparing built UI to a Figma file → use `reviewing-design-fidelity`

## Workflow

### 1. Gather sources

Identify and read every input artifact before analysis. Sources may include:

- Markdown/text files (read directly via `Read`)
- External URLs (use `WebFetch` for public docs; ask user to paste content for internal-only links)
- Figma URLs — use `mcp__plugin_figma_figma__get_design_context` for the structured content and `mcp__plugin_figma_figma__get_screenshot` for the visual context. Frames in Figma planning files often contain user flows, copy decks, and acceptance criteria that don't appear in any text doc. See `references/figma-spec-extraction.md` for extraction patterns.
- Reference policies the spec must comply with — read these first so review dimensions align with constraints

If sources are incomplete (e.g., user mentions "the auth policy" without sharing it), pause and ask before proceeding. A review against assumed policy is worse than no review.

### 2. Build the review matrix

Apply the eight review dimensions described in `references/review-dimensions.md`:

1. **Completeness** — every described behavior has acceptance criteria
2. **Consistency** — no contradictions between sections, glossary terms used uniformly
3. **Edge cases** — boundary, null, concurrency, failure modes considered
4. **Policy compliance** — every applicable policy is acknowledged and satisfied
5. **Testability** — each requirement has an unambiguous pass/fail definition
6. **Stakeholder coverage** — admin, end-user, system, operator perspectives all addressed
7. **State and lifecycle** — initial, intermediate, terminal, recovery states defined
8. **Ambiguity** — vague quantifiers ("fast", "reasonable", "many") flagged

Each dimension produces zero or more findings. A finding is a concrete, quotable gap — not a vibe.

### 3. Prioritize findings

Categorize each finding by impact:

- **Blocker** — implementation cannot proceed safely without resolution (missing critical behavior, policy violation, contradictory requirements)
- **Major** — implementation can proceed but will likely produce defects or rework (vague acceptance criteria, missing edge case, untested state)
- **Minor** — clarity/quality improvement, no implementation risk (terminology, formatting, redundancy)

Skip "Nit" / "Style" — those drown out signal. Authors will polish on their own pass.

### 4. Produce the report

Use the report template in `references/report-template.md`. Brief excerpt of the structure:

```
# Spec Review: <doc title>

## Summary
- Sources reviewed: <list>
- Blockers: N | Major: N | Minor: N
- Top 3 risks if shipped as-is: ...

## Blockers
### [B-1] <short title>
Quote: "<exact text from spec>"
Gap: <what's missing or wrong>
Suggestion: <minimal change to resolve>

## Major
### [M-1] ...

## Minor
### [N-1] ...

## Out of scope (flagged for separate review)
- ...
```

Quotes matter. A reviewer who cannot point to the exact phrase being critiqued is critiquing their own interpretation, not the spec.

## Principles

- **Audit, don't rewrite.** Surface gaps; let the author decide the fix.
- **Cite the source.** Every finding references the exact text or Figma frame ID being critiqued.
- **Prioritize ruthlessly.** A 50-finding report goes ignored. A 5-blocker report gets fixed.
- **Distinguish observation from opinion.** "Section 3 contradicts Section 7" is observation. "Section 3 is poorly written" is opinion — skip it unless ambiguity is the actual finding.
- **Acknowledge what's good.** A short "Strengths" note in the summary signals the reviewer engaged with the substance, not just the gaps.

## Detailed references

Load these only when working through the relevant phase:

- `references/figma-spec-extraction.md` — extracting structured content from Figma planning files (frame conventions, comment threads, decision pins)
- `references/review-dimensions.md` — full descriptions and example findings for the eight review dimensions
- `references/report-template.md` — annotated template with example findings showing good vs weak phrasing
