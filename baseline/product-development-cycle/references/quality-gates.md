# Quality Gates and Error Matrix

## Contents

1. Universal gate checklist
2. Scenario coverage matrix
3. Financial gate checklist
4. Feature readiness template
5. Skip record

## Universal gate checklist

Complete each gate with:

- **Inputs:** evidence and constraints used.
- **Decisions:** what was chosen and why.
- **Artifact:** the updated source of truth.
- **Assumptions:** unvalidated beliefs.
- **Open questions:** unknowns with a resolution plan.
- **Risks:** probability, impact, mitigation, and trigger.
- **Exit evidence:** what proves the gate is complete.
- **Next gate:** the single recommended next stage.

## Scenario coverage matrix

Apply this matrix to every meaningful user flow. Mark each row as applicable, covered, intentionally excluded, or unresolved.

| Dimension | Cases to consider |
|---|---|
| Entry | First visit, returning user, deep link, expired link, direct URL |
| Identity | Signed out, wrong account, expired session, deleted account, concurrent sessions |
| Permission | Owner, editor, viewer, non-member, removed member, changed ownership |
| Data state | Empty, partial, stale, duplicate, deleted, restored, archived, corrupted |
| Input | Missing, invalid, boundary, very long, Unicode, duplicate, pasted content |
| Network | Offline, timeout, slow response, retry, duplicate submission, partial failure |
| Concurrency | Simultaneous edits, stale version, conflict, reordered operations, idempotency |
| Lifecycle | Create, read, edit, share, revoke, delete, restore, export, import |
| Device | Mobile, desktop, rotation, narrow viewport, touch, keyboard |
| Accessibility | Focus, labels, screen reader, contrast, zoom, reduced motion |
| Security | Enumeration, IDOR, injection, CSRF, rate abuse, leaked secret, token replay |
| Privacy | Data minimization, visibility, retention, deletion, logs, backups |
| Recovery | Retry, resume, undo, restore, support path, audit trail |
| Operations | Logging, metrics, alerts, backup, migration, rollback, incident response |

Do not manufacture scenarios without product relevance. Explain why excluded cases do not apply.

## Financial gate checklist

Use this gate before paid launch, permanent hiring or content commitments, and acquisition scaling. A low-cost prototype may proceed with an order-of-magnitude model if the uncertainty and revisit trigger are explicit.

Before Gate 5 scope approval, also complete the early viability subset: reachable market volume, named acquisition routes, channel capacity, preliminary CAC/contribution, Month-24 outcome, cash requirement, evidence quality, and an explicit proceed/experiment/change/stop decision. For commercial products without another owner-approved target, test RUB 1 million sustainable monthly operating profit by Month 24; for non-commercial products, record the replacement cost/value constraint.

- **Decision:** launch, price, scope, budget, hire, channel, partnership, or scale decision is stated.
- **Driver tree:** traffic → registration → activation → retained user → payer/order → revenue → contribution → operating result → cash.
- **Revenue:** each subscription, transaction, advertising, affiliate, B2B, or other stream has separate drivers.
- **Costs:** variable, fixed, step, and one-time costs include payments, refunds, taxes, free credits, support, infrastructure, team, content, legal, security, and partner shares where applicable.
- **Acquisition:** CAC is calculated for the selected funnel stage and channel, not substituted with CPC or CPI.
- **Unit economics:** net ARPPU, contribution, gross margin, LTV, allowable CAC, LTV/CAC, and payback are visible.
- **Cash:** burn, runway, break-even, collection timing, and launch cash needs are visible.
- **Month-24 outcome:** sustainable profit uses a trailing-three-month average, includes acquisition and recurring costs, and shows required volume, channel capacity, growth, seasonality, and peak cash need.
- **Scenarios:** conservative, base, and optimistic cases change inputs, not outputs.
- **Sensitivity:** price, conversion, retention/churn, CAC, key variable costs, and major fixed costs have break points.
- **Evidence:** every material input is fact, observed, benchmark, hypothesis, or unknown, with a date and source or experiment.
- **Audit:** outputs trace to inputs, formulas have no errors, components tie, and checks pass.
- **Decision record:** recommendation, rejected alternatives, accepted risk, owner, and next recalculation trigger are recorded.

## Feature readiness template

```markdown
## Feature: <name>

### Outcome
<User and measurable result>

### Evidence
- <Research, analytics, support signal, or explicit assumption>

### Scope
- In: ...
- Out: ...

### Actors and permissions
- ...

### Main path
1. ...

### Alternate and failure paths
- ...

### Acceptance criteria
- [ ] ...

### Non-functional requirements
- Security: ...
- Privacy: ...
- Performance: ...
- Accessibility: ...
- Reliability: ...

### Measurement
- Success metric: ...
- Guardrail metric: ...

### Release
- Migration: ...
- Rollback: ...
- Monitoring: ...

### Open questions and decisions
- ...
```

## Skip record

When the user explicitly skips a gate, record:

```markdown
### Skipped gate: <gate>
- Reason:
- Evidence currently available:
- Risk accepted:
- Temporary assumptions:
- Revisit trigger:
- Blocking before release: yes/no
```

A skipped discovery or design gate may be acceptable for a prototype. Security, data integrity, verification, migration safety, and rollback cannot be silently waived for production.
