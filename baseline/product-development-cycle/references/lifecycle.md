# Product Development Lifecycle

## Contents

1. Context and discovery
2. Product definition
3. Design and risk
4. Economics and planning
5. Implementation
6. Verification and release
7. Learning loop

## 0. Context inventory

Inspect existing research, product specifications, design files, backlog, architecture, API, database, tests, analytics, and release state. Build a short artifact map and identify the first incomplete gate.

Exit criteria:

- current product state is stated;
- existing sources of truth are identified;
- contradictions and stale decisions are listed;
- the next gate is selected.

## 1. Problem discovery

Use `$problem-framing-canvas` to define the affected user, problem, evidence, impact, current alternatives, assumptions, and desired outcome.

Exit criteria:

- problem is phrased independently of a proposed feature;
- evidence is separated from assumptions;
- success and guardrail signals are named;
- discovery gaps are assigned a validation method.

## 2. Users and jobs

Use `$proto-persona` for provisional personas and `$jobs-to-be-done` for situations, motivations, expected progress, and competing alternatives. Avoid demographic detail that does not affect product behavior.

Exit criteria:

- primary and secondary actors are distinct;
- each actor has goals, constraints, and relevant permissions;
- the core job and switching forces are clear.

## 3. Positioning

Use `$positioning-workshop` when audience, category, alternative, or value proposition remains unclear. Positioning is required for launch-facing products and optional for internal tools.

Exit criteria:

- target segment and main alternative are explicit;
- differentiated value is credible;
- claims do not exceed available evidence.

## 4. Customer journey

Use `$customer-journey-mapping-workshop`. Map entry, activation, core task, collaboration, return usage, support, and exit. Include emotions and pain points only where they inform decisions.

For every phase cover:

- trigger and user goal;
- action and system response;
- required data and permission;
- failure and recovery;
- interruption and resume behavior;
- opportunity and measurable signal.

Exit criteria:

- happy and alternate paths reach a clear outcome;
- failure recovery is possible or intentionally blocked;
- cross-account and cross-device behavior is known;
- unresolved journey gaps are visible.

## 4.5. Early market and economic viability

Begin this review after Gate 1 has a working segment and complete it before Gate 5 scope approval. It is an early decision checkpoint, not a substitute for the detailed Gate 10 financial model.

For every project, state whether the intended outcome is commercial. If it is not commercial, record why market, acquisition, and profit metrics are not applicable and define the equivalent budget, adoption, capacity, or value constraint.

For a commercial product, test:

- target-market volume in the same atomic unit used for revenue;
- serviceable and reachable demand rather than category totals alone;
- named acquisition mechanisms, funnel stages, CAC unit, attribution, and plausible channel capacity;
- price, net revenue, variable cost, contribution, fixed cost, break-even, and major sensitivities;
- a monthly path to a meaningful Month-24 profit target;
- peak burn, cash need, and the evidence needed to replace benchmarks;
- product-value guardrails such as successful outcomes, refunds, repeat use, and referrals.

When the owner has not set a different meaningful target or currency, use **RUB 1 million sustainable monthly operating profit by Month 24** as the default commercial test. Define sustainable as a trailing-three-month average, not a single seasonal or promotional peak, and include acquisition and recurring operating costs. Keep tax treatment explicit.

Exit criteria:

- market volume, reachable volume, payers, and transactions are not conflated;
- at least one acquisition route has a testable funnel, cost basis, and capacity hypothesis;
- conservative, base, and optimistic economics identify the break points;
- the Month-24 target has required volume, growth, channel capacity, and cash estimates;
- facts, observations, benchmarks, hypotheses, and unknowns are separated;
- the result is classified as supported, conditional, mathematically possible only, or not plausible;
- the owner records proceed, run a cheaper experiment, change segment/price/channel/cost, or stop.

## 5. Story map and MVP slice

Use `$user-story-mapping-workshop` to create the activity backbone, user tasks, stories, and release slices. The first slice must deliver a complete user outcome, not merely backend or frontend layers.

Exit criteria:

- activities follow user behavior rather than architecture;
- the MVP slice works end to end;
- later slices and non-goals are explicit;
- dependencies and sequencing are understood.

## 6. PRD and acceptance criteria

Use `$prd-development`, then `$user-story` and `$user-story-splitting` for implementation-sized work.

The PRD must include:

- problem, users, evidence, and strategic context;
- solution overview and journey reference;
- functional and non-functional requirements;
- acceptance criteria and error handling;
- data, permissions, privacy, and retention;
- success and guardrail metrics;
- dependencies, risks, non-goals, and open questions.

Exit criteria:

- every requirement is observable or testable;
- stories describe user value and acceptance criteria;
- large stories are split vertically;
- conflicts with existing behavior are resolved.

## 7. Adversarial PRD clarification

Run `$grill-me` after the PRD and story map are coherent and before the detailed financial gate or UX work starts. Resolve one decision at a time and update the authoritative product artifacts.

Exit criteria:

- no critical ambiguity remains in problem, scope, data, permissions, recovery, or metrics;
- rejected alternatives and tradeoffs are recorded;
- open questions have owners, validation plans, or explicitly accepted residual risks.

## 8. Financial model

Use `$product-financial-model` when installed. Otherwise read [financial-model.md](financial-model.md) and combine current market research with the Spreadsheet skill.

Complete this gate before detailed UX investment. The model depth should match the decision: an order-of-magnitude model can authorize a cheap validation experiment, while a full monthly model is required before paid launch, permanent commitments, or acquisition scaling.

Exit criteria:

- the decision, model horizon, currency, tax treatment, and unit of economics are explicit;
- revenue is driver-based and separated by stream;
- variable, fixed, step, and one-time costs are visible;
- CAC, contribution LTV, allowable CAC, payback, break-even, burn, and runway are calculated where applicable;
- conservative, base, and optimistic scenarios use editable inputs rather than hardcoded outputs;
- material inputs are classified as fact, observed data, benchmark, hypothesis, or unknown and have a source or validation plan;
- sensitivity identifies the drivers and thresholds that can break the model;
- formula and logic checks pass;
- the result explicitly authorizes the current scope, chooses a cheaper experiment, changes the model/scope, or stops investment;
- the next recalculation date or trigger is recorded.

## 9. UX and interface design

Use `$impeccable shape` before implementation, then `critique`, `harden`, and `adapt` as appropriate. Use Figma when the project requires visual collaboration or prototype testing.

Required states:

- default, loading, empty, partial, success, error, disabled, and destructive confirmation;
- signed-out, expired-session, insufficient-permission, and removed-access states;
- desktop and mobile layouts where supported;
- keyboard, screen-reader, focus, contrast, and reduced-motion behavior.

Exit criteria:

- all journey steps have a designed system response;
- destructive and irreversible actions are explicit;
- content and controls fit supported viewports;
- designs map to acceptance criteria.

## 10. Security, privacy, and abuse

Run `$threat-model` before architecture is frozen and `$attack-path-analysis` for sensitive flows. Cover identity, sessions, authorization, tenant boundaries, input, secrets, data exposure, abuse, auditability, and recovery.

Exit criteria:

- assets, actors, boundaries, threats, and mitigations are documented;
- authorization is checked server-side for every protected object;
- sensitive data and secrets have explicit handling rules;
- high-risk findings block implementation or release.

If required controls materially change scope, fixed cost, variable cost, conversion, or acquisition assumptions, refresh the Gate 8 financial decision before technical design.

## 11. Technical design

Use Superpowers `$brainstorming` and `$writing-plans`. Define architecture, data model, API contracts, ownership boundaries, consistency rules, concurrency, migrations, compatibility, caching, observability, and deployment assumptions.

Exit criteria:

- design follows the repository's existing patterns where suitable;
- migrations and rollback are safe;
- API and data invariants are testable;
- operational failure modes are addressed.

## 12. Prioritization and roadmap

Use `$prioritization-advisor` to compare value, evidence, risk, effort, and dependency. Use `$roadmap-planning` for outcome-oriented sequencing. Convert the chosen slice into a backlog with acceptance criteria and verification steps.

Exit criteria:

- priorities have explicit rationale;
- dependencies and critical path are visible;
- each backlog item is independently verifiable;
- deferred work has a revisit trigger.

## 13. Implementation

Use Superpowers `$test-driven-development` and `$executing-plans`. Work in an isolated branch or worktree. Keep changes scoped, integrate continuously, and update decisions when implementation reveals new constraints.

Exit criteria:

- tests demonstrate intended behavior and meaningful failures;
- migrations and seed data work from a clean state;
- no unrelated refactoring is mixed into the change;
- documentation and contracts match implementation.

## 14. Verification

Use `$requesting-code-review`, `$verification-before-completion`, `$security-diff-scan`, and `$impeccable audit`.

Verify:

- unit, integration, API, authorization, and end-to-end behavior;
- loading, error, recovery, concurrency, and destructive flows;
- responsive UI, accessibility, and browser/device support;
- dependency, secret, and security findings;
- performance budgets and observability signals;
- clean installation and reproducible startup.

Exit criteria:

- required checks have fresh evidence;
- critical and high findings are resolved;
- accepted residual risks are recorded;
- release candidate matches the reviewed commit.

## 15. Release

Use `$finishing-a-development-branch` after the release checklist passes.

Prepare:

- environment configuration and secret provisioning;
- database backup, migration, and rollback;
- staged rollout or feature flag where warranted;
- monitoring, alerts, dashboards, and log access;
- support notes, release notes, and ownership;
- analytics events and baseline metrics.

Exit criteria:

- rollback can be executed;
- responsible owner and incident path are known;
- metrics and alerts are live;
- release evidence is retained.

## 16. Learn and iterate

Compare outcomes with success and guardrail metrics. Collect qualitative feedback, support issues, failures, and drop-off points. Replace financial benchmarks and hypotheses with observed acquisition, retention, payment, churn, refund, variable-cost, and support data. Update assumptions, journey, story map, PRD, financial model, and roadmap. Return to the earliest gate invalidated by new evidence.
