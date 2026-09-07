# Quality Gates and Evidence States

Use this reference to classify evidence for the current product scope and maturity stage. A gate closes through decision-grade evidence, not through the presence of a document or specialist.

Keep common lifecycle and quality rules in the distributed skill. Keep product-specific configuration and decisions in the project's profile, guidance, and status pointer. Keep live Issue, PR, CI, and merge state in GitHub. Keep transient executable paths, access-check observations, and current task identities in runtime handoffs rather than shared templates.

## Evidence states

- **applicable-covered** — required in the current scope/stage and supported by current identified evidence that meets the gate's exit need.
- **applicable-missing** — required now but absent, stale, contradicted, or insufficient. It must block only the dependent transition and name what would resolve it.
- **not-applicable** — excluded for a stated product or scope reason, with decision authority and a revisit condition. It does not mean the work was performed.
- **deferred-with-trigger** — relevant to a later stage or decision and deliberately not required now, with a reason, trigger, and destination gate. It must be revisited before the triggered transition or release.

`not-applicable` and `deferred-with-trigger` never equal PASS. `applicable-missing` does not freeze unrelated authorized work; it blocks only the dependent transition. Unknown values remain literally `Unknown` until a dependent action requires resolution.

## Evidence record

Record one row per gate or check. Preserve valid evidence and update the state when scope, maturity, facts, risk, or evidence identity changes.

| Field | Record |
|---|---|
| Gate/check | Gate number or named check |
| State | One of the four evidence states |
| Current scope/stage | Product scope and maturity stage to which the judgment applies |
| Evidence source | Authoritative artifact, observation, or external source; `Unknown` when absent |
| Identity/date | Revision, result identity, and observation date when present |
| Rationale | Why the state follows from the evidence and current exit need |
| Owner/decision authority | Required for exclusions, accepted limitations, and substantive decisions |
| Missing evidence or accepted limitation | Concrete gap, or the limitation retained by authority |
| Revisit trigger | Fact, date, scope, risk, or maturity change that reopens the check |
| Dependent transition | The gate, decision, or release transition this record can block |

## Scenario dimensions

Apply only dimensions relevant to the current behavior and risk. Exclusion needs a rationale rather than a fabricated test result.

| Dimension | Consider |
|---|---|
| Identity and permission | Signed-out, wrong account, expired or removed access, role and ownership changes |
| Data state and lifecycle | Empty, partial, stale, duplicate, retention, deletion, migration, restoration |
| Failure and recovery | Timeout, interruption, retry, resume, undo, support path, audit trail |
| Concurrency and duplication | Simultaneous work, stale versions, ordering, idempotency, duplicate requests |
| Accessibility and device | Keyboard, screen reader, contrast, zoom, reduced motion, supported viewports |
| Security and privacy | Authorization, boundaries, input, abuse, secrets, minimization, visibility |
| Operations and rollback | Logs, metrics, alerts, backup, migration, rollback, incident ownership |

Actual exposure controls applicability. Real users, sensitive data, spending, or operational consequences can require protection at any maturity stage; a stage label cannot defer them by itself.

## Readiness boundary

A green CI result, stage label, completed artifact, or available specialist does not establish release readiness. Release requires fresh evidence for every applicable implementation, migration, manual, accessibility, security, recovery, rollout, rollback, monitoring, and ownership check, plus accepted residual risks and authorization for the specific release. Report the first applicable missing check and its dependent transition.

A release rehearsal is not a production launch. Record it as simulated evidence and retain the separate authorization and fresh evidence required for an actual release.

These Markdown contracts and their mechanical tests do not execute the behavioral scenarios E17–E30 or E34–E35. They do not prove runtime behavior, installation, or release readiness; later fixtures and rehearsal must supply that evidence.
