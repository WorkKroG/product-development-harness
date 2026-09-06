---
name: product-development-cycle
description: Guide a digital product from discovery and user research through PRD, UX, architecture, implementation, QA, security, release, and iteration. Use when starting or resuming a product, turning a prototype or MVP into a working application, deciding the next product-development step, auditing skipped stages, preparing a feature for implementation, or checking whether user journeys, edge cases, acceptance criteria, and release gates are complete.
---

# Product Development Cycle

Run a gated, evidence-based product workflow. Preserve useful existing work and continue from the first incomplete gate.

## Start

1. Inspect the repository, product documents, backlog, designs, tests, and current implementation.
2. Identify which lifecycle gates have concrete evidence and which remain assumptions.
3. Report the current stage, missing gates, and recommended next action.
4. Ask only questions that cannot be answered from existing artifacts.
5. Never restart discovery merely because documents use different filenames.

When the user requests a full audit, read [references/lifecycle.md](references/lifecycle.md) and [references/quality-gates.md](references/quality-gates.md). When the product has a commercial model, meaningful operating costs, paid acquisition, subscriptions, transactions, advertising, partnerships, or a scaling decision, also read [references/financial-model.md](references/financial-model.md). For a single feature, run the same gates at feature scale.

When starting a new project, establishing an agentic delivery model, or coordinating multiple specialist roles, read [references/agentic-development.md](references/agentic-development.md). If the repository has no `AGENTS.md`, adapt [assets/AGENTS.template.md](assets/AGENTS.template.md) to the project instead of copying it blindly. Do not overwrite existing repository guidance.

## Invocation

- Explicit invocation is recommended at the start of every new project: `$product-development-cycle <objective>`.
- The skill may activate implicitly for lifecycle questions, but an explicit invocation signals that the complete gated workflow is required.
- Keep one coordinating conversation as the product source of truth. Delegate only bounded, independent work; do not create user-owned tasks unless the user asks.
- Re-run the skill when resuming a project, beginning a major feature, preparing a release, or auditing skipped stages.

## Global source of truth

This skill and its bundled references are the canonical product pipeline for every project. Do not create a full repository-local `PRODUCT_DEVELOPMENT_CYCLE.md` copy unless the user explicitly requests a project-specific fork.

Projects store only:

- `AGENTS.md` with local commands, sources of truth, and explicit exceptions;
- `docs/PROJECT_STATUS.md` or an existing equivalent with the current gate and evidence;
- product, design, risk, finance, architecture, plan, and release artifacts.

When a repository already contains its own lifecycle document, compare it with this skill. Move generally useful improvements into the global skill, keep genuine project exceptions in `AGENTS.md` or project status, and never silently let a local copy override mandatory gates.

## Operating rules

- Do not mark a gate complete without an artifact or verifiable evidence.
- Do not silently skip a gate. Record the skip, reason, risk, and revisit condition.
- Separate facts, validated learning, assumptions, open questions, and decisions.
- Use one source of truth per artifact; update an existing document instead of duplicating it.
- Keep MVP scope explicit, including non-goals and deferred scenarios.
- Cover happy paths, alternate paths, failures, recovery, permissions, and data lifecycle.
- End every stage with: outputs, unresolved risks, decision log, and next gate.
- Use installed skills when available. If a named skill is unavailable, perform the objective directly and note the missing specialization.

## Mandatory skill sequence

- **Hypothesis through approved PRD:** use the installed Product Manager Skills for problem framing, users/JTBD, positioning, journey, story map, PRD, stories, splitting, and prioritization. Do not replace this set with a generic planning pass.
- **Early viability:** begin the preliminary market, reachability, acquisition, and economics review once Gate 1 has a working segment; complete Gate 4.5 before Gate 5 scope approval. Every project must record a viability decision. Commercial products must test market volume, channel capacity, CAC, unit economics, and a meaningful Month-24 profit target; non-commercial products must record why commercial metrics are not applicable and use an explicit cost/value constraint instead.
- **Immediately after PRD:** run `$grill-me` against the current PRD, scope, permissions, evidence, assumptions, and open decisions. The financial gate and UX are blocked by unresolved critical questions unless each has an owner, validation plan, or explicitly accepted residual risk.
- **Before UX:** complete the detailed financial gate using the approved PRD. Proceed only when the economics support the scope, a cheaper validation experiment is explicitly chosen, or the owner accepts a documented investment risk.
- **After the financial decision:** run Impeccable in order: `shape`, `critique`, `harden`, then `adapt`. Record the UX/design artifact and gate result.
- **Before architecture:** complete the threat/privacy review. Re-check financial deltas when UX or risk work changes scope, operating cost, monetization, or acquisition assumptions.
- **Architecture and detailed delivery plan:** use Superpowers `$brainstorming` to compare approaches and obtain written design approval, then Superpowers `$writing-plans`. Do not implement before both gates pass.
- **Financial gate:** use `$product-financial-model` when installed; otherwise follow [references/financial-model.md](references/financial-model.md), current market research, and the Spreadsheet skill. Never silently skip the gate for a commercial product.

## Lifecycle routing

| Gate | Objective | Preferred skill |
|---|---|---|
| 0. Context | Inventory current evidence and constraints | This skill |
| 1. Problem | Define the problem, evidence, and assumptions | `$problem-framing-canvas` |
| 2. Users | Define personas, motivations, and jobs | `$proto-persona`, `$jobs-to-be-done` |
| 3. Positioning | Clarify audience, alternative, and value | `$positioning-workshop` |
| 4. Journey | Map end-to-end user behavior and failure points | `$customer-journey-mapping-workshop` |
| 4.5. Early viability | Test preliminary market volume, reachability, acquisition, unit economics, and the Month-24 outcome before scope freeze | Market research; [financial-model.md](references/financial-model.md); Spreadsheet skill when a workbook is useful |
| 5. Scope | Map activities, stories, and MVP release slice | `$user-story-mapping-workshop` |
| 6. Requirements | Produce PRD, stories, acceptance criteria, and non-goals | `$prd-development`, `$user-story`, `$user-story-splitting` |
| 7. PRD challenge | Expose unresolved decisions and weak assumptions before financial commitment and UX | `$grill-me` |
| 8. Financial model | Validate revenue, costs, CAC/LTV, cash flow, scenarios, break-even, and the investment decision before UX | `$product-financial-model` when installed; otherwise Spreadsheet skill and market research |
| 9. UX | Design flows, states, responsive behavior, and accessibility after the economic decision | `$impeccable shape`, `$impeccable critique`, `$impeccable harden`, `$impeccable adapt` |
| 10. Risk | Model security, privacy, abuse, and recovery; re-check financial deltas when risk controls change cost or scope | `$threat-model`, `$attack-path-analysis` |
| 11. Technical plan | Define architecture, data, API, migrations, observability, and cost constraints | Superpowers `$brainstorming`, `$writing-plans` |
| 12. Delivery plan | Prioritize and create roadmap/backlog | `$prioritization-advisor`, `$roadmap-planning` |
| 13. Implementation | Build incrementally with tests and isolated changes | Superpowers `$test-driven-development`, `$executing-plans` |
| 14. Verification | Review behavior, UI, security, and regressions | `$requesting-code-review`, `$verification-before-completion`, `$security-diff-scan`, `$impeccable audit` |
| 15. Release | Prepare rollout, rollback, monitoring, and support | `$finishing-a-development-branch` plus release checklist |
| 16. Learn | Measure outcomes, collect feedback, refresh the financial model, and update priorities | Return to gates 1, 4, 5, 8, or 12 |

Use workshop skills with `$workshop-facilitation` when the user wants a guided one-question-at-a-time session.

## Gate response format

For lifecycle audits and transitions, respond with:

1. **Current gate**
2. **Evidence found**
3. **Missing or assumed**
4. **Risks of proceeding**
5. **Recommended skill and prompt**
6. **Exit criteria**
7. **Next gate**

## Completion rule

A product or feature is ready to release only when:

- the target user and problem are evidenced;
- the early viability checkpoint has a recorded proceed, experiment, change, or stop decision;
- the end-to-end journey and failure recovery are documented;
- MVP scope and non-goals are explicit;
- requirements and acceptance criteria are testable;
- design includes all relevant states and devices;
- authorization, privacy, and abuse cases are reviewed;
- for a commercial product, unit economics, cash needs, break-even, and the conditions for paid acquisition or permanent cost commitments are explicit;
- implementation and migrations are verified;
- automated and manual checks pass;
- rollout, rollback, monitoring, and ownership are defined;
- success and guardrail metrics can be measured.

Otherwise report the first unmet gate rather than declaring completion.
