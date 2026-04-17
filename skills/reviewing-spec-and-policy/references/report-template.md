# Report Template

Annotated template. Replace bracketed sections; preserve heading structure so authors can navigate consistently.

```markdown
# Spec Review: <doc title>

**Reviewed:** <YYYY-MM-DD>
**Sources:**
- <path or URL #1>
- <path or URL #2>
**Reference policies considered:** <list, or "none specified">

## Summary

- Blockers: N | Major: N | Minor: N
- Top 3 risks if shipped as-is:
  1. <risk + section reference>
  2. ...
- Strengths: <1-2 things the spec does well — keeps the report from feeling adversarial>

## Blockers

### [B-1] <short title — what is missing or wrong>

**Quote (Section X.Y):**
> "exact text from the spec"

**Gap:** <what's wrong or missing — concrete, not vibes>

**Suggested resolution:** <minimal change that closes the gap; offer alternatives if multiple paths are valid>

---

(repeat for each blocker)

## Major

(same structure, prefix [M-N])

## Minor

(same structure, prefix [N-N])

## Out of scope

Items deferred from this review with reasoning:
- <item> — <why deferred (e.g., "covered by separate security review", "not yet in scope per PRD §1.3")>
```

## Anti-patterns to avoid

❌ "Section 3 is unclear." → not actionable. Quote the unclear sentence and propose what would clarify it.

❌ "Consider using GraphQL instead of REST." → not a spec gap; that's a design opinion. Skip unless the spec explicitly underspecifies the API style and that gap is the finding.

❌ Listing 30 minor findings in equal weight with 2 blockers. → readers fatigue and ignore everything. Cap minor findings at 5 per review; consolidate the rest into a single "additional polish" bullet.

❌ Making suggestions without quotes. → the author cannot tell what was actually being critiqued.
