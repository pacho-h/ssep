# Completeness Audit Report Template

```markdown
# Completeness Audit: <feature name>

**Reviewed:** <YYYY-MM-DD>
**Scope (in):** <bounded list of routes/files/services>
**Scope (out):** <explicit exclusions>
**Verification commands run:** <e.g., `pnpm test`, `pnpm typecheck`, `pnpm lint`>

## Summary

- Blockers: N | Major: N | Polish: N
- Top 3 risks if shipped as-is:
  1. ...
- Strengths: <what the implementation already handles well>

## Blockers

### [B-1] <short title>

**Track:** Frontend | Backend
**Dimension:** <F1 / B2 / etc>
**Probe used:** <how the gap was found — e.g., "Tabbed through form with keyboard">

**Observation:** <concrete description of what was observed>

**Why this is a blocker:** <impact on a user/operator class>

**Suggested fix:** <minimal change to close the gap; reference specific file/function if known>

---

(repeat for each blocker)

## Major

(same structure, prefix [M-N])

## Polish

(same structure, prefix [P-N], can be more compact — single-line findings OK if context is clear)

## Out of scope (deferred)

- <item> — <reason>

## Verification status

```
$ pnpm test
... output ...

$ pnpm typecheck
... output ...
```
```

## Anti-patterns

❌ Reporting findings without specifying the probe — readers can't verify or reproduce.

❌ Mixing "would be nice" preferences with actual gaps — bury signal in noise.

❌ Closing fixes without writing regression tests — same gap returns in 6 months.

❌ Audit-and-fix mode landing 20 fixes in one PR — code review becomes impossible; pause and triage with the author first.
