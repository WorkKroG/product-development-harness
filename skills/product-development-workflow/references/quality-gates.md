# Quality Gates and Evidence States

Use this reference to classify evidence for the current product scope and maturity stage. A gate closes through decision-grade evidence, not through the presence of a document or specialist.

Keep common lifecycle and quality rules in the distributed skill. Keep product-specific configuration and decisions in the project's profile, guidance, and status pointer. Keep live Issue, PR, CI, and merge state in GitHub. Keep transient executable paths, access-check observations, and current task identities in runtime handoffs rather than shared templates.

## Guarantees and mechanisms

Preservation of raw results, independent review, version freshness, safety, and privacy are
guarantees. Markdown or JSON, custom validators, and dedicated recorder roles are possible
mechanisms, not guarantees themselves. A reviewer identifies the violated guarantee and
observable harm. It may assess candidate corrections, but it cannot impose a new
architecture as the only correction without the decision required for material scope.

Safety and privacy remain non-negotiable when applicable. Simplifying a mechanism,
stopping an unproductive correction cycle, or lacking a preferred tool never converts a
missing safety or privacy guarantee into PASS; block only the transition that depends on it
and name the evidence or correction needed.

## Review coverage

Derive applicable obligations from the original normative binding sources, then map the
implementation and evidence to them. A copied child brief, previous coverage table, or old
finding list is input to verify, not the source of the obligation set. Assess four questions
separately: whether source requirements are covered, whether the implementation conforms,
whether the evidence is fit for the claimed behavior, and whether each prior finding is
actually closed. Name unchecked areas and partial closure; neither supports a full PASS.

A blocker stops only its dependent transition. Continue independent safe checks so the
review reports the bounded state of the candidate rather than only the first failure. State
the scope inspected and its limits; review evidence does not promise discovery of every
unknown defect.

## Critical check sufficiency

For each critical check, name the required property and one concrete violation that must
make the check fail. Evidence that only excludes a forbidden effect does not prove a
required positive effect. Mocks and assertions must represent the relevant real contract,
including lifecycle and completion semantics; otherwise record the limitation or missing
evidence. Use mutation or fault injection when it is a proportionate way to demonstrate
the violation, not as a universal requirement for every test.

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
