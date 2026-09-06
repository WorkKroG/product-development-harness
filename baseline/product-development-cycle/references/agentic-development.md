# Agentic Development Model

Use this model to coordinate product work without relying on one agent to define, implement, and approve its own output.

## Topology

1. Keep one coordinating conversation as the product orchestrator.
2. Store decisions and evidence in repository artifacts, not only in chat history.
3. Assign specialist roles only for the current gate or bounded task.
4. Give implementation work a small scope, explicit acceptance criteria, and an isolated branch or worktree.
5. Have a reviewer independent from the implementation pass whenever practical.
6. Require human approval at product, architecture, risk, and release gates.

Skills provide procedures; agents or delegated tasks execute roles. Do not invoke every skill at once. Route work according to the active lifecycle gate.

## Roles

| Role | Responsibility | Preferred capabilities |
|---|---|---|
| Product orchestrator | Determine the current gate, evidence, risks, and next action | `$product-development-cycle` |
| Research facilitator | Frame the problem, users, jobs, and positioning | PM workshop skills |
| Product manager | Produce journey, story map, PRD, stories, and backlog | Journey, PRD, story, and prioritization skills |
| Challenger | Expose weak assumptions and unresolved decisions | `$grill-me` |
| UX/UI specialist | Cover flows, states, responsive behavior, accessibility, and design quality | `$impeccable` and Figma capabilities |
| Technical lead | Define architecture, contracts, migrations, observability, and delivery plan | Superpowers planning skills |
| Builder | Implement one ready story incrementally with tests | Superpowers implementation and TDD skills |
| Reviewer | Check specification compliance, regressions, code quality, and test evidence | Review and verification skills |
| Security reviewer | Review threats, permissions, secrets, abuse cases, and sensitive diffs | Security skills and tools |
| Release owner | Verify rollout, rollback, monitoring, support, and ownership | Release checklist and branch-finishing skills |

Do not create permanent agents for every role. Instantiate a role only when its gate requires work.

## Repository Sources of Truth

Prefer existing filenames and avoid duplicate documents. A new project normally needs:

- `AGENTS.md`: durable operating rules, commands, branch policy, and quality gates;
- `docs/PROJECT_STATUS.md`: current gate, evidence, assumptions, decisions, risks, and next action;
- product specification or PRD;
- customer journey and story map;
- design brief or design links;
- architecture and decision log;
- prioritized backlog;
- risk and security record;
- metrics and release checklist.

Each subject must have one authoritative artifact. Update it after material decisions.

## New Project Sequence

1. Inventory the repository and initialize version control if required.
2. Create or adapt `AGENTS.md` and identify commands for install, development, tests, lint, types, build, and migrations.
3. Create `docs/PROJECT_STATUS.md` with the current gate and evidence map.
4. Run lifecycle gates 1 through 11 before broad implementation. Record any intentional skips.
5. Complete the Product Manager Skills sequence through an approved PRD.
6. Run `$grill-me` immediately after PRD; resolve or explicitly disposition every critical question.
7. Complete the financial gate and record whether the economics authorize the scope, a cheaper experiment, or no further investment.
8. Run Impeccable `shape`, `critique`, `harden`, and `adapt`, then review security and privacy risks.
9. Re-check the financial decision when UX or risk work changes material scope or cost.
10. Use Superpowers `$brainstorming` for architecture approval, followed by `$writing-plans`.
11. Convert the approved scope into small, independently verifiable backlog items.
12. Implement each ready item through the task protocol below.
13. Run release gates and obtain human approval before production rollout.
14. Measure outcomes and return to the earliest gate changed by new evidence.

## Task Protocol

For every implementation item:

1. Confirm the user outcome, scope, non-goals, dependencies, and acceptance criteria.
2. Confirm affected permissions, data lifecycle, failure states, and recovery.
3. Create a small technical plan and identify required tests.
4. Work in an isolated branch or worktree using the repository naming policy.
5. Implement the smallest coherent increment; keep unrelated edits out.
6. Run fresh tests, type checks, lint, build, and migrations relevant to the change.
7. Perform independent specification and code review.
8. Add security review for auth, permissions, secrets, input, data exposure, dependencies, and infrastructure changes.
9. Add UX and accessibility review for user-facing changes.
10. Merge only when acceptance criteria and repository gates pass.

The author must not be the sole source of approval for high-risk work.

## Parallelism

Parallelize only work that is independent and has clear ownership:

- read-only research and audits;
- separate UI screens or components with stable contracts;
- tests and documentation for already stable behavior;
- unrelated backlog items with disjoint files.

Keep these sequential or centrally coordinated:

- product scope and source-of-truth documents;
- authentication and authorization;
- database schema and migrations;
- shared API contracts and cross-cutting infrastructure;
- final integration and release decisions.

## Human Approval Gates

Require explicit product-owner approval before:

- accepting the problem, target user, and success criteria;
- freezing MVP scope and non-goals;
- approving PRD after challenge;
- approving the end-to-end design;
- accepting architecture and residual security risks;
- releasing a candidate to production.

Agents may recommend a decision and present evidence, but must not silently make irreversible product or risk decisions.

## Standard Start Prompt

```text
$product-development-cycle Initialize this project using the agentic development model.
Inventory existing evidence, create or update the project status and AGENTS.md,
identify the first incomplete gate, and guide me through it. Do not skip gates.
Separate facts from assumptions, keep one source of truth per artifact, and require
my approval at product, architecture, risk, and release checkpoints. Do not start
broad implementation until journeys, failure states, acceptance criteria, design,
architecture, security risks, and the delivery plan are ready.
```
