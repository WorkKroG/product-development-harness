---
name: product-development-workflow
description: Guide a digital product through evidence-based discovery, staged implementation, verification, release, and learning in Codex. Use when starting, resuming, auditing, or preparing a product, module, or release while preserving existing evidence and selecting the next incomplete gate.
---

# Product Development Workflow

Run a gated, evidence-based product workflow in Codex. Preserve useful existing work, match depth to the product's maturity and current decision, and continue from the first incomplete or invalidated gate.

This first working version is Codex-only. Discover available capabilities before relying on them. Skill discovery does not authorize repository changes, external actions, installation, publication, spending, merge, or release.

## Start

1. Determine whether the request is to start, resume, audit, work on a module, or prepare a release.
2. Read existing repository guidance and artifacts; recognize their current names instead of creating duplicates.
3. When known, establish the selected release, commit, or content identity and compare it with the actually loaded identity.
4. Surface the version state as matched, unknown, ambiguous, or mismatched.
5. Determine the current and target maturity stage.
6. Select the first missing or invalidated gate within that stage's scope.
7. Return one recommended next action; ask only for a decision that existing evidence cannot answer.

Do not mix two active versions. Never silently replace a shared or globally installed copy. Pause only transitions that depend on the unresolved version selection; continue independent authorized work.

For the canonical gates and maturity transitions, read [the lifecycle reference](references/lifecycle.md). For Gate 3.5 or Gate 8, read [the financial model reference](references/financial-model.md).

Read [quality gates](references/quality-gates.md) when classifying applicability or evidence, auditing readiness, or preparing verification or release. Before relying on user-owned tasks, native messages or waits, model assignment, recovery, GitHub service access, or a platform denial, read [Codex runtime boundaries](references/codex-runtime.md). Before a stage depends on a specialist capability, model, tool, or fallback, read [dependency boundaries](references/dependencies.md).

When an approved module needs planning, implementation, review, integration, escalation,
or recovery, read [agentic delivery coordination](references/agentic-development.md). Adapt
the bounded [delivery role prompts](assets/role-prompts.md) and the applicable
[work item and review templates](assets/work-item-and-review-templates.md); do not turn
them into a second live status system.

If project-local guidance, a product profile, or a status and evidence pointer is missing, adapt the corresponding [AGENTS template](assets/AGENTS.template.md), [product profile template](assets/project-profile.template.md), or [project status template](assets/PROJECT_STATUS.template.md). Do not copy templates blindly, overwrite an existing source of truth, assume capability availability, or expand authority.

## Operating rules

- A gate is complete only when its decision has relevant evidence, not because a document exists.
- Separate facts, observations, assumptions, unknowns, decisions, and accepted risks.
- Preserve valid evidence and reopen only gates affected by new facts, scope, cost, risk, or maturity.
- Record intentional non-applicability with its reason. Do not turn an unperformed check into a pass.
- Use one source of truth per subject and update existing artifacts where possible.
- Keep scope, non-goals, permissions, data lifecycle, failure, recovery, and measurable outcomes explicit.
- Do not fabricate interviews, measurements, sources, market figures, financial values, or readiness evidence.
- Stop only the transition that depends on missing evidence or capability; continue unrelated authorized work.
- Keep module planning, local requirements and UX decisions, feedback, corrections, and
  acceptance in its user-owned Task coordinator within delegated scope; do not request
  unchanged decisions again through Product.
- Route shared architecture/contracts, project scope, cross-task dependencies or order,
  and material cost, risk, or schedule changes to the Product coordinator. Substantive
  owner choices and manual merge/release remain human.
- Use distinct internal agent sessions for PLAN, Implementation, Change Review, and FINAL.
  Preserve typed native identities and give each role only bounded context.

## Lifecycle routing

Use this active order: Context → Problem → Users → Positioning → light Gate 3.5 → Journey → Scope → Requirements → Challenge → Finance → UX → Risk → Technical plan → Delivery plan → Implementation → Verification → Release → Learn.

Gate 3.5 is one short, approximate viability decision before Journey. Gate 8 reuses unchanged Gate 3.5 evidence and deepens the economics only enough for the named investment. There is no active early Gate 4.5.

Use installed specialist skills only when the current gate requires them. If a specialist is unavailable, state the limitation, use a documented fallback only when it can produce decision-grade evidence, and otherwise leave the gate open.

## Maturity

Track these five stages separately:

- working prototype
- MVP
- scale 1
- scale 2
- mature operation

For architecture, distinguish architecture vision, current implementation, and transition plan. Describe the nearest stage in detail and later stages as hypotheses, constraints, and revisit triggers. Account counts never prove capacity without a measurable load profile that names active users or operations, peak rate, data volume, latency or reliability target, measurement evidence, and cost boundary.

Prototype code may be replaced when evidence and transition cost support replacement; reuse is not mandatory. Real user data must not be silently discarded when code is replaced: preservation, migration, deletion, and rollback require an explicit authorized lifecycle.

Do not require production-scale infrastructure, a complete PRD, or a detailed financial model before a bounded prototype experiment unless the experiment's actual risk requires it. As real users, sensitive data, spending, or operational consequences appear, apply the relevant protections regardless of the stage label.

## Entry response contract

For lifecycle entry, audit, and gate transitions, return:

1. **Current gate**
2. **Evidence found**
3. **Missing or assumed**
4. **Risks**
5. **Recommended next action**
6. **Exit criteria**
7. **Next gate**

Keep the recommendation to one next action unless independent preparation can safely proceed in parallel. Local module decisions stay in Task within delegated scope. Route only shared or project-wide architecture and contracts, project scope, cross-task dependencies or order, and decisions with material cost, risk, or schedule impact through Product. Substantive human decisions stay with the owner in their applicable coordinator task. Routine technical choices stay within the approved scope.

## Completion

Do not claim release readiness from a stage label, a green CI result, or a completed artifact alone. Report the first unmet applicable gate, the evidence needed to close it, and the next decision. Release requires fresh implementation and migration checks, applicable manual checks, accepted residual risks, rollout and rollback evidence, monitoring, support ownership, and explicit authorization for the particular release.
