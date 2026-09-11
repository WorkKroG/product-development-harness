# Product Profile

## Process identity

- Selected release: `product-development-workflow`.
- Selected commit/content identity: Provided by the future runner.
- Actually loaded identity: Unknown.
- Identity state (`matched`, `unknown`, `ambiguous`, or `mismatched`): `unknown`.

## Product

- Product mode and objective: commercial product experiment for a local personal follow-up tracker.
- Target user and outcome: one solo consultant remembers and records promised follow-ups.
- Communication language: Unknown.
- Decision owner/coordinator: owner in the synthetic Task.
- Current scope and non-goals: one synthetic offline loop; no email sending, payment,
  analytics, public deployment, team workflow, real customer data, or CRM import.

## Maturity

- Current stage (`working-prototype`, `mvp`, `scale-1`, `scale-2`, or `mature`): `working-prototype`.
- Target stage: `working-prototype`.
- Stage outcome and exit need: the full core path is useful in a bounded synthetic rehearsal.

## Architecture

- Vision identity: a replaceable personal follow-up service that could later support multiple users.
- Current implementation identity: None — input-only fixture.
- Current limits: no product code, persistence, external integration, or measured load.
- Next transition trigger: the full core path is useful in a bounded synthetic rehearsal.
- Transition evidence required: a versioned record of the bounded synthetic rehearsal and its limits.
- Data preservation or lifecycle rule: no real user data is permitted.
- Rollback/replacement path: delete the disposable local fixture copy.

## Load profile

- User unit: one solo consultant.
- Active period: Unknown.
- Peak concurrent work or peak operation rate: Unknown.
- Heavy operation: Unknown.
- Data volume: Unknown.
- Latency/reliability objective: Unknown.
- Cost ceiling: no paid services or permanent infrastructure.
- Evidence source: Unknown.
- Next measurement: Unknown.

## Sources of truth

- Product/requirements identity: `product-profile.md`.
- Journey/design identity: Unknown.
- Architecture/decision identity: `product-profile.md` architecture section.
- Risk/release identity: Unknown.
- GitHub host/repository: Not applicable for this offline fixture.

## Runtime

- Runtime environment: Codex desktop target.
- Allowed parallelism: one future isolated writer; independent review after a stable candidate.
- Actual dependencies: Unknown.
- Transient runtime handoff location: Unknown.

## Models

| Role/stage | Requested model/reasoning | Accepted native assignment | Independently verified runtime fact |
|---|---|---|---|
| Product | `gpt-5.6-sol/high` | Unknown | Unknown |
| Task | `gpt-5.6-sol/high` | Unknown | Unknown |
| PLAN | `gpt-5.6-sol/high` | Unknown | Unknown |
| Implementation | `gpt-5.6-sol/medium` | Unknown | Unknown |
| Change Review | `gpt-5.6-sol/high` | Unknown | Unknown |
| FINAL | `gpt-6-astra/high` | Unknown | Unknown |

## Economics

- Mode (`commercial`, `internal`, or `non-commercial`): `commercial`.
- Commercial assumptions and targets: hypothesis that a focused local loop can reduce
  missed promised follow-ups for a solo consultant.
- Non-commercial budget/value constraint: zero authorized spend.
- Current decision and investment boundary: Gate 3.5 is the decision boundary; no spend
  or external action is authorized.
- Recalculation trigger: a recorded Gate 3.5 decision or a material change to scope or cost.

## Applicability

| Gate/check | State | Current scope/stage | Evidence source and identity/date | Rationale | Owner/decision authority | Missing evidence or accepted limitation | Revisit trigger | Dependent transition |
|---|---|---|---|---|---|---|---|---|
| Positioning | applicable-covered | working-prototype | `positioning.md`, synthetic fixture | Segment, alternatives, and differentiated value are recorded | Owner in synthetic Task | Synthetic evidence only | Positioning facts change | Gate 3.5 |
| Gate 3.5 Light viability | applicable-missing | working-prototype | Unknown | The next bounded investment decision is required | Owner in synthetic Task | Accessible market, broad economics, strongest unknown, and bounded experiment decision | Decision-grade inputs are recorded | Journey |
| Product gates 4–13 | deferred-with-trigger | working-prototype | `PROJECT_STATUS.md`, synthetic fixture | Later product and implementation work is outside this input package | Owner in synthetic Task | No product, journey, requirements, implementation, or runtime evidence | Gate 3.5 selects the bounded experiment | Future experiment |
| Risk gate 10 | deferred-with-trigger | working-prototype | `PROJECT_STATUS.md`, synthetic fixture | Actual exposure is limited to disposable synthetic local files | Owner in synthetic Task | No future implementation or data exposure is defined | Scope introduces code, external integration, or non-synthetic data | Future experiment or release |
| Verification gate 14 | deferred-with-trigger | working-prototype | `PROJECT_STATUS.md`, synthetic fixture | There is no product candidate to verify | Owner in synthetic Task | No executed checks or manual evidence | A product candidate exists | Product transition |
| Release gate 15 | deferred-with-trigger | working-prototype | `PROJECT_STATUS.md`, synthetic fixture | Public or production release is outside this fixture | Owner in synthetic Task | No release, recovery, or authorization evidence | A specific release is proposed | Release |
