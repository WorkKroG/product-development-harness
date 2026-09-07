# Product Development Lifecycle

Use this as the canonical active gate map. Gate numbers and maturity stages are different coordinates: apply only the depth needed for the current stage, decision, data, and risk. Preserve still-valid evidence when moving between stages.

## 0. Context

Inventory repository guidance, research, requirements, designs, architecture, backlog, implementation, tests, analytics, delivery state, and contradictions. Identify the current and target maturity stages and the first missing or invalidated gate in scope.

Exit when sources of truth, facts, assumptions, constraints, contradictions, current stage, and one next gate are explicit.

## 1. Problem

Define the affected user, problem independent of a preferred solution, available evidence, current alternatives, intended outcome, assumptions, success signals, and guardrails.

Exit when the problem and validation method are decision-ready for the current stage.

## 2. Users

Define primary and secondary actors, situations, jobs, motivations, constraints, permissions, and switching forces. Avoid demographic detail that does not change product behavior.

Exit when actors, core jobs, and access boundaries are clear enough for positioning.

## 3. Positioning

Clarify the target segment, category or context, meaningful alternatives, differentiated value, and claims supported by evidence. For an internal product, record a concise value and alternative statement or why public-market positioning is not applicable.

Exit when audience, alternative, and value are explicit.

## 3.5. Light viability

Make one short, approximate decision: proceed, run a bounded experiment, change the idea, or stop. Reuse Positioning evidence and assess the accessible market, meaningful competitors and substitutes, payer or value, broad income and cost ranges, strongest unknown, and one bounded experiment. For external facts, record source and date; keep estimates and unknowns visible.

This gate does not prove demand or profitability. It does not require a workbook, exact CAC/LTV, a universal Month-24 target, or fabricated numbers. For internal or non-commercial products, compare expected value with acceptable cost instead of inventing revenue.

Map still-valid historical Gate 4.5 evidence and decisions into Gate 3.5. Ask only for missing or stale inputs. Preserve the historical baseline and recorded decisions rather than rewriting them to current terminology. This mapping keeps exactly one active early checkpoint: Gate 3.5.

Exit when the decision, reasoning, strongest uncertainty, experiment boundary, success/revisit signal, and allowed resources are explicit.

## 4. Journey

Map entry, activation, core task, return, support, and exit for the direction selected at Gate 3.5. For each meaningful phase cover user goal, action, system response, required data and permission, failure, recovery, interruption, resume, and measurable signal. Carry Gate 3.5 constraints forward without repeating its market or finance work.

Exit when main, alternate, failure, and recovery paths produce a clear outcome or an explicit blocker.

## 5. Scope

Choose a vertical slice that delivers a complete outcome at the current maturity stage. Record in-scope behavior, non-goals, dependencies, deferred work, and revisit triggers.

Exit when the owner has accepted the decision package appropriate to the investment.

## 6. Requirements

Connect the problem, users, journey, and scope to observable functional and non-functional requirements, acceptance criteria, permissions, data lifecycle, failure behavior, success measures, risks, and open questions.

Exit when each requirement is testable and implementation-sized work can be derived without inventing product decisions.

## 7. Challenge

Independently challenge the PRD, scope, permissions, evidence, assumptions, recovery, metrics, and unresolved decisions. Use an available specialist or an explicit rubric; do not treat a generic summary as independent evidence.

Exit when critical questions are resolved, assigned a validation plan, or retained as explicit accepted residual risk by the appropriate decision-maker.

## 8. Finance

Gate 8 reuses Gate 3.5 evidence. Refresh only facts and assumptions changed by scope, pricing, monetization, acquisition, risk controls, architecture, or time. Deepen the model only enough for the named investment, such as a prototype budget, paid pilot, permanent commitment, or acquisition scaling.

Exit when the named decision, relevant costs and value or revenue, material sensitivities, cash or budget boundary, evidence quality, and recalculation trigger support proceed, experiment, change, or stop.

## 9. UX

Design the journey's applicable flows and states, including loading, empty, partial, success, error, destructive confirmation, lost access, supported viewports, keyboard, screen reader, contrast, zoom, and reduced motion.

Exit when system responses map to acceptance criteria and unresolved experience risks are visible.

## 10. Risk

Review identity, authorization, tenant boundaries, sensitive data, privacy, input, secrets, abuse, auditability, retention, deletion, backup, migration, and recovery in proportion to actual exposure. Revisit scope or Gate 8 when mitigations materially change cost or value.

Exit when applicable threats, mitigations, verification, owners, and residual risks are explicit.

## 11. Technical plan

Separate architecture vision, current implementation, and transition plan. Define the current boundaries, data, APIs, invariants, concurrency, migrations, rollback, observability, operating assumptions, and cost constraints. Future components remain hypotheses until evidence triggers them.

Exit when the current design is testable, transition risks are understood, and an independent review covers both premature complexity and unsafe future constraints.

## 12. Delivery plan

Prioritize outcome-oriented modules and small independently verifiable work items. Make dependencies, stable shared contracts, review boundaries, non-goals, checks, and manual merge explicit.

Exit when the next module has approved scope and immutable plan identity.

## 13. Implementation

Implement small work items with tests in isolated branches or worktrees. Preserve unrelated work and keep implementation and independent Change Review distinct.

Exit when the exact candidate passes fresh relevant checks and matches its approved scope.

## 14. Verification

Verify integrated behavior, regressions, permissions, data handling, failures, recovery, accessibility, security, performance, installation where supported, and operational readiness. Automated checks do not replace required manual evidence.

Exit when critical findings are resolved, limitations are recorded, and evidence identifies the exact candidate.

## 15. Release

Prepare configuration, migrations, backup, rollback, staged rollout, monitoring, alerts, support, analytics, and ownership. A rehearsal is not a production release; merge and release remain separately authorized actions.

Exit when recovery is executable, responsible owners are known, evidence is retained, and the specific release is authorized.

## 16. Learn

Compare outcomes with success and guardrail measures. Collect product behavior, feedback, failures, operating cost, and support evidence. Update affected assumptions and return to the earliest invalidated gate without replaying the entire lifecycle.

Exit when new evidence, decisions, and the next learning or delivery action are recorded.

## Maturity stages and transition evidence

### working-prototype

Prove one core hypothesis through a manually testable scenario. Keep implementation minimal, state stubs and experiment boundaries, and carry an architecture vision without building future infrastructure automatically.

### mvp

Deliver the core outcome to limited real users and collect feedback. Current implementation needs suitable data change, access, recovery, update, and measurement behavior. The transition plan names the next constraints to validate.

### scale-1

Meet the product-defined first growth profile. Do not infer readiness from registrations: use a measurable load profile with active-user window, peak operations, data volume, heavy paths, latency and reliability targets, evidence, and cost.

### scale-2

Meet the revised larger load and operating profile. Reconsider early architecture assumptions from observed behavior and migrate components or data only when evidence supports the change.

### mature

Meet explicit reliability, recovery, support, change-safety, and cost goals for mature operation. Requirements may apply earlier when actual data or risk demands them.

Before every stage transition, compare the architecture vision with the current implementation and measured evidence. Produce a versioned transition plan covering what stays, what changes, why, expected effect, validation, data migration, rollback, and cost. Prototype code may be replaced, partially reused, or retained according to evidence and transition cost. Real user data must not be silently discarded; preserve, migrate, or delete it only through an explicit authorized lifecycle.
