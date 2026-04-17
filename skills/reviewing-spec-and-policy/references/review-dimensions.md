# Review Dimensions

Each dimension below names a class of gap, gives heuristics for finding it, and shows example findings phrased well vs poorly.

## Table of contents

1. [Completeness](#1-completeness)
2. [Consistency](#2-consistency)
3. [Edge cases](#3-edge-cases)
4. [Policy compliance](#4-policy-compliance)
5. [Testability](#5-testability)
6. [Stakeholder coverage](#6-stakeholder-coverage)
7. [State and lifecycle](#7-state-and-lifecycle)
8. [Ambiguity](#8-ambiguity)

---

## 1. Completeness

Every described capability has acceptance criteria, and every acceptance criterion has a clear "done" definition.

**Heuristics**
- For each user-facing action, can a tester write a test that would fail before implementation and pass after?
- For each external integration mentioned (auth, payment, notification), is the contract specified?
- Are non-functional requirements (latency, throughput, retention) quantified?

**Good finding:** "Section 4.2 describes a 'reset password' flow but does not specify token expiry, single-use vs multi-use, or rate limiting. Three implementation paths are equally valid; pick one."

**Weak finding:** "The reset password section needs more detail." → unactionable; the author already knows it's brief.

## 2. Consistency

Same concept named the same way throughout. No two sections contradict each other.

**Heuristics**
- Glossary check: pick three nouns (e.g., "user", "account", "session") — are they used identically across sections?
- Numeric check: every limit/threshold/timeout mentioned twice should agree.
- Behavioral check: a rule stated in section 2 ("admins can delete any record") should not be contradicted in section 7 ("only the record owner may delete").

**Good finding:** "Section 2.1 says session timeout is 30 minutes; Section 6.4 says 1 hour. Pick one and update the other."

## 3. Edge cases

Boundary, null, concurrency, and failure modes that the spec assumes but does not address.

**Standard probe set** — for each operation, ask:
- Empty input (zero items, empty string, null user)
- Maximum input (N+1 items where N is the spec limit)
- Concurrent operations (two users editing the same record)
- Network failure mid-operation
- Authorization revoked mid-session
- Time zone / DST transitions for time-sensitive logic
- Deletion of a referenced entity (foreign-key style cascading)

**Good finding:** "Section 3.5 describes credit transfer between two RFID cards. Behavior when the source card is deactivated mid-transfer is unspecified. Three reasonable resolutions exist (rollback, complete-then-deactivate, queue-and-retry); pick one."

## 4. Policy compliance

Every policy that applies must be acknowledged in the spec, and the spec must satisfy it.

**Heuristics**
- List policies the user named or that the document type implies (privacy/GDPR for any PII handling, PCI for payment, internal data retention for storage).
- For each, find the section of the spec that addresses it. If absent → blocker.
- If present, verify the rule cited matches the policy's actual text (quote both).

**Good finding:** "Section 5 stores user phone numbers indefinitely. Internal Data Retention Policy v3 §2.1 requires PII deletion after account closure plus 90 days. No retention rule is specified."

## 5. Testability

Each requirement can be verified by an unambiguous pass/fail test.

**Heuristics**
- Search for "fast", "quickly", "many", "appropriate", "intuitive", "user-friendly" — each is a finding unless quantified.
- For each acceptance criterion, draft the test in your head: input → expected output. If you can't, the requirement is untestable.

**Good finding:** "Section 7.2 requires charging sessions to start 'quickly'. Replace with a numeric SLA (e.g., p95 < 3s from authorize to status=Charging)."

## 6. Stakeholder coverage

Specs often default to the happy-path end user. Other stakeholders (admins, operators, integrators, system itself) need their own behaviors defined.

**Standard stakeholder probe**
- End user: described?
- Admin / back-office operator: how do they audit, override, undo?
- System / scheduled job: what runs autonomously, with what permissions?
- Integration partner: what's the API contract and error envelope?
- Support: how does support diagnose a stuck record?

**Good finding:** "Spec describes the user-facing refund flow in detail. No mention of how a back-office operator initiates or audits a manual refund — likely a Day-1 support need."

## 7. State and lifecycle

Each entity has a defined initial state, set of intermediate states, terminal state(s), and recovery paths from error states.

**Heuristics**
- Draw the implied state diagram from the prose. Are all transitions covered? Are dead-ends acknowledged?
- For each terminal state, is the path to that state from any other state defined?
- Is there a recovery path from each error state, or is "stuck" the actual final state?

**Good finding:** "Charging session has states {Idle, Authorized, Charging, Completed, Faulted}. The transition from Faulted is unspecified — does it auto-retry, require operator intervention, or terminate?"

## 8. Ambiguity

Words and phrases with multiple reasonable interpretations.

**Standard probe list** (search for these terms; each hit is a candidate finding)
- "etc.", "and so on" — incomplete enumeration
- "should", "may", "ideally" — non-binding requirements
- "various", "multiple", "several" — uncountable quantities
- "typically", "usually", "normally" — undefined exception cases
- Pronouns with unclear antecedent ("it", "they", "this") — especially across paragraphs

**Good finding:** "Section 4.1: 'Send notification when usage is high.' 'High' is undefined; pick a threshold (e.g., 80% of monthly quota)."
