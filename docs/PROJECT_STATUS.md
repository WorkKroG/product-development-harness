# Project status

Date: 2026-09-08. Product: Product Development Workflow.
Repository: `WorkKroG/product-development-harness` (repository slug unchanged).

## Current stage

Module 3 is integrated at base `f008c78980113f67f5bc73c7e93adcf8ad003423`.
The Module 4 candidate adds a standard-library structural checker and synthetic offline
review-state fixtures for C01–C12. This evidence is local structural evidence only; it does
not install, publish, merge, or release the workflow and is not a mirror of live PR/CI state.

## Accepted decisions

- Evolve the existing product-development-cycle; Codex-only initial scope.
- Five maturity stages, early architectural vision, staged implementation and reconsideration
  before scaling. Prototype code may be discarded; rewriting is not mandatory.
- Light Gate 3.5 between Positioning and Journey replaces the heavy early 4.5. Later Finance
  refines the same economics for the investment at hand.
- Product Development Workflow is the product name; product-development-workflow is the
  renamed active skill. Baseline, installed global copy and GitHub repo slug are unchanged.
- One Product coordinator and one user-owned Task coordinator per large module. The owner
  works and agrees local scope/plan/acceptance in the Task coordinator directly.
- PLAN, Implementation, Change Review and FINAL use distinct internal subagents with bounded
  context and independent review. Existing WIP must survive the change in topology.
- Only main state transitions travel upward. Project scope/architecture/contracts and material
  cost/risk/schedule changes are escalated. Product can commission an authorized architecture
  task, record a versioned decision and send revised boundaries to affected tasks.
- Native model assignments, sole `gh` service access and manual merge remain required.
- Start with a small usable process, validate on a small synthetic product, then extend coverage.
- Bootstrap baseline and specification separately before implementation.

## Next action for the main coordinator

Perform independent Change Review of the exact Module 4 candidate against
[MODULE4-PLAN-v1](superpowers/plans/2026-09-07-module-4-deterministic-structural-checker.md).
Any new head invalidates that review. Integration remains a separate manually authorized step.

## Evidence and limits

SPEC.md §§6–8 is the accepted coordination design. README.md and AGENTS.md provide current
navigation. The Module 4 checker command and its synthetic inputs are documented in README;
fresh verification output and the exact candidate SHA belong to the implementation/review
evidence. A01–A24 and E01–E41 remain audit findings and proposed scenarios, not passed runtime
tests. Pilot, installation and release evidence remain pending.
The private original transfer package is available locally under `.local-handoff/`, ignored by Git.

Structural checks do not prove behavioral correctness.
