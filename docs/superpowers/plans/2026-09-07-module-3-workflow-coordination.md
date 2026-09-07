# Product Development Workflow — Module 3 Implementation Plan

> **For agentic workers:** Use the owner-approved Product/Task coordinator topology and
> internal implementation/review subagents from SPEC.md §§6–8. Apply
> `superpowers:subagent-driven-development` with those project-specific authority and
> independent-review boundaries; do not substitute its generic owner-routing defaults.

**Identity:** MODULE3-PLAN-v3. Design approved by the owner on 2026-09-07; this replacement
implementation plan requires independent PLAN review and task-local acceptance before execution.
Its exact file hash plus containing commit identify the reviewed content. v2 PASS is historical.

**Goal:** Make the renamed skill guide an autonomous module whose owner works in its Task
coordinator, with bounded internal workers and compact project-level events/escalations.

**Architecture:** Product coordinates project-wide decisions; Task coordinates local planning,
implementation, review and acceptance. Codex provides sessions/messages; the skill defines
decision and evidence contracts, not a scheduler, runtime service or status database.

**Tech Stack:** Skill Markdown/YAML, Python standard-library contract checks, Git, native
Codex task/subagent capabilities where available. No new dependency or installation.

**Spec:** `SPEC.md` §§6–9; accepted naming and coordination amendment dated 2026-09-07.

## Global constraints

- Active entry: `skills/product-development-workflow/SKILL.md`; invocation `$product-development-workflow`.
- Product name: Product Development Workflow. GitHub slug stays `WorkKroG/product-development-harness`.
- Preserve `baseline/product-development-cycle/`, `BASELINE.sha256`, global installed copy,
  historical evidence and unrelated WIP. Completed Modules 1–2 are not recreated.
- Local product decisions and module plan/acceptance belong in Task, with no repeated Product approval.
- Material shared architecture/contracts, project scope/dependencies/task order, cost/risk/schedule
  changes go to Product; substantive owner choices remain human. Manual merge and release remain human.
- Model matrix: Product/Task/PLAN `gpt-5.6-sol/high`; ordinary Implementation `gpt-5.6-sol/medium`;
  Change Review `gpt-5.6-sol/high`; FINAL/architecture/security/second opinion `gpt-6-astra/high`.
  Native assignments and availability are recorded separately from requested/verified runtime facts.
- Existing platform denials remain binding. Moving work to a subagent does not authorize a denied action.
- No GitHub mutation, push, repository rename, global installation, paid action, pilot or release is
  authorized by this local implementation plan. These need their applicable existing/new authority.

## Base, dependencies and migration

Planning baseline: fetched `origin/main` at `4ed8c87960bfd04e528cd98303c54e053228c7ce`.
This plan depends on the reviewed naming/coordination amendment that contains this file. Before
execution, Task records the exact amendment commit and refreshed main/merge-base. If the amendment
has not been integrated, keep implementation pending unless a stacked branch is explicitly in scope.
If relevant sources/base drift, reconcile and re-review the affected plan before writing.

MODULE3-PLAN-v2 was built around five old-path files and user-owned worker tasks. Its WIP is
potentially reusable input, not authority or a tested candidate. Task must inspect the existing
held sessions and worktree, record actual changed paths and checks, map old active paths to the
new skill name and preserve originals. Do not delete/archive/restart old tasks automatically.
Obtain acknowledgement of the new process before any worker resumes. Any transfer of WIP must
be deliberate and reviewed; if copying would require additional filesystem authority, stop that
operation and report the concrete blocker rather than changing executor to bypass it.

## One Work Item: delivery coordination contract

One cohesive Work Item owns the delivery reference, role packages, runtime distinction and tests.
Parallel implementation is not useful here because these files define one shared contract.

**Files:**

- Create `skills/product-development-workflow/references/agentic-development.md` — delivery,
  local decision authority, event filtering, escalation/replanning, exact review and recovery rules.
- Create `skills/product-development-workflow/assets/role-prompts.md` — Product, Task, PLAN,
  Implementation, Change Review, FINAL and temporary Architecture role prompts and model assignments.
- Create `skills/product-development-workflow/assets/work-item-and-review-templates.md` — bounded
  work/review packages, decisions, native identities, compact events, escalation and resumption records.
- Modify `skills/product-development-workflow/SKILL.md` — narrow delivery routing and local/project
  decision boundary; preserve stage, finance and existing dependency routes.
- Modify `skills/product-development-workflow/references/codex-runtime.md` — distinguish user-owned
  coordinator tasks from internal agent sessions, correct tool family/ID use and recovery semantics.
- Modify `skills/product-development-workflow/assets/AGENTS.template.md` — local/task versus project
  authority and pointers to the delivery contract, without copying the complete protocol.
- Modify `tests/test_skill_contract.py` — stable package/identity/routing regressions.

No other active path is implicitly included. A discovered conflict in another file must be included
explicitly in the reviewed scope before editing. Navigation/evidence for this Work Item lives in
the Task's native record; later repository navigation changes belong to a reviewed change.

**Interfaces consumed:** current lifecycle/stage/process identity, profile/runtime boundaries,
SPEC §§6–9, E08–E25 (including the revised E10/E14 subcases), current repository authority.

**Interfaces produced:**

- Work package: Work Item/module identity, outcome/why, scope/non-goals, binding sources,
  dependencies, maturity/architecture/process/plan identities, exact base/head, allowed paths,
  permissions/data/recovery, acceptance criteria, checks, role, executor kind and native ID.
- Review record: phase, independent reviewer kind/ID, reviewed plan hash or base/head/main,
  binding sources, checks, findings, verdict and invalidation condition. New head invalidates
  Change Review PASS; main drift invalidates FINAL; plan changes invalidate PLAN_PASS.
- Local decision: package identity, decision authority and location, options/recommendation,
  consequences, owner decision, approved boundaries and next authorized action.
- Project event: task identity, event, short reason/result, evidence pointer, requested decision
  only when applicable. Types: ACTIVE, ESCALATION_REQUIRED, READY_FOR_INTEGRATION, DONE, CANCELLED.
- Escalation: evidence/problem, boundary exceeded, affected tasks/contracts, options/recommendation,
  required authority/decision, paused scope and independent work allowed to continue.
- Architecture return: accepted decision/architecture version, revised tasks/dependencies,
  preserved work, affected plans/reviews, continuation conditions and next authorized action.
- Recovery: old/new process identity, actual repository/session/WIP state, preserved evidence,
  superseded verdicts, acknowledged instruction update and next unresolved transition.

## Execution steps

- [ ] **1. Reconcile the dependency and held WIP.** Perform the checks above before writing.
  Record the exact executable base and owner-accepted plan hash in the Task. Reuse valid evidence;
  prior RED on old-path requirements is not proof of RED for this revised contract.
- [ ] **2. Read `skill-creator` and applicable implementation/review guidance.** Dispatch one bounded
  Implementation subagent. Pass only approved scope, source paths, current identities and WIP
  inventory; no full-history fork. Confirm it is the sole writer in the shared worktree.
- [ ] **3. Extend the existing contract tests for stable interfaces.** Add checks that each new route
  resolves, role/work/review packages carry executor kind and native ID, and decision/event/recovery
  fields are present. Preserve existing lifecycle/runtime/model/leakage regressions. Test names:
  `test_delivery_routes_resolve`, `test_worker_and_coordinator_identities_are_typed`,
  `test_delivery_packages_include_review_and_decision_identity`,
  `test_project_event_and_escalation_packages_are_bounded`.
  These are document contract checks, not simulated proof of agent behavior.
- [ ] **4. Run the focused tests before implementation.** Missing delivery routes/files/fields are the
  expected failure. Import/syntax errors or failures caused only by a stale rename are invalid RED.
  Use `python3 -B -m unittest discover -s tests -v`; record the actual relevant failures.
- [ ] **5. Write the seven scoped files' changes.** Encode the interfaces above and SPEC §§6–8.
  Keep detailed procedure in references/assets; the entrypoint and AGENTS template route to it.
  Roles get their own bounded context. Review starts after the candidate is stable, read-only and
  without implementation reasoning. Task forwards findings internally, preserving the Work Item
  and branch; a replacement agent session is explicitly recorded if the original is unavailable.
- [ ] **6. Check event and escalation semantics against the cases below.** Correct contradictions
  before running the full suite. Event filtering uses transitions, never every local agreement.
  READY_FOR_INTEGRATION requires current review/PR readiness; DONE requires module FINAL after
  manual merges. A meaningful failure beyond Task authority triggers ESCALATION_REQUIRED once.
- [ ] **7. Verify and create a local candidate.** Run full unittest discovery, baseline checksum,
  skill quick validation if available, diff and allowed-path checks. Record limitations if the
  existing environment cannot run the quick validator; do not install dependencies silently.
  Commit only the seven scoped paths with subject `feat: add autonomous task coordination`.
- [ ] **8. Run independent Change Review.** A fresh subagent gets the spec, accepted plan, exact
  base/head and complete diff, not the implementation chat. It independently checks evidence.
  Correct concrete findings inside the Work Item, re-run affected checks and review each new head.
  After two unsuccessful cycles on the same finding, use an independent second opinion.
- [ ] **9. Integrate only under the applicable authority.** Ready candidate is not permission to
  publish/push/merge. After authorized PR and manual merge, independent FINAL checks the actual
  current main and all planned/corrective changes. Send DONE only after unchanged-main FINAL_PASS.

## Review cases and acceptance

These are required review cases for this module and inputs to later behavioral evaluation.
Reading the cases or passing text checks is not a live coordination pilot.

| Case | Expected contract |
|---|---|
| Owner accepts local module plan/UX refinement in Task | Decision stays there; no Product approval or full report |
| Implementation needs a shared API change affecting a second module | Pause dependent work; one evidence-backed escalation to Product |
| Product commissions authorized architecture task | Separate visible coordinator with bounded subagents and independent review |
| Owner accepts revised architecture | Versioned decision/task changes returned once; affected plans re-reviewed; preserve valid WIP |
| Repeated CI progress and local review corrections | No repeated upward status or full transcripts |
| PR merged but FINAL still pending | Module not DONE |
| Candidate/main/plan changes after PASS | Relevant verdict invalidated; unrelated valid evidence retained |
| Internal agent ID passed to user-owned task API | Reject ID mismatch; use proper runtime family; no duplicate task |
| Old worker unavailable after interruption | Reconcile WIP and evidence; new bounded session explicitly replaces it |
| Platform denied push in old task | New topology does not bypass denial; independent work may continue |

Acceptance requires all seven paths within scope; valid existing routes; local/project decision
authority consistent across active files; five compact event types; bounded typed worker context;
independent PLAN/Change Review/FINAL evidence; safe drift/WIP recovery; no installation/release claims.

## Verification evidence and handoff

Commands from the candidate worktree:

```sh
python3 -B -m unittest discover -s tests -v
shasum -a 256 -c BASELINE.sha256
git diff --check
git status --short
git rev-parse HEAD
```

Additionally inspect `git diff <recorded-base>..<candidate-head>` and its changed-path set;
use the actual recorded full SHAs, not invented placeholder refs. The independent reviewer reruns
checks on that exact candidate. Structural PASS does not execute E08–E25; fixtures/rehearsal and
remaining FWP tasks are still separate work. No unresolved correctness finding may be called PASS.

Task coordinator presents this plan for acceptance locally after PLAN_PASS, without repeating the
owner's already accepted naming/topology decision. Product receives only the next meaningful event.
