# Project status

Date: 2026-09-07. Product: Product Development Workflow.
Repository: `WorkKroG/product-development-harness` (repository slug unchanged).

## Current stage

Coordination design and naming amendment accepted by the owner. Module 3 needs a revised
plan before delivery implementation resumes. The active repository skill is being renamed
to `product-development-workflow`; this does not install or release it.

The fetched main at this checkpoint is `4ed8c87960bfd04e528cd98303c54e053228c7ce`,
containing the merged lifecycle core and profile/runtime modules. This is immutable context,
not a mirror of live PR/CI state; obtain fresh state from Git/GitHub before dependent work.

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

Complete independent review of the naming/coordination amendment and the revised
[Module 3 plan](superpowers/plans/2026-09-07-module-3-workflow-coordination.md).
Then hand the reviewed package to the existing Module 3 Task coordinator for task-local
plan acceptance and WIP reconciliation. The previous MODULE3-PLAN-v2 verdict does not cover
the new topology or skill path; do not resume from its old execution instructions.
No global install, automatic merge, repository rename, pilot or release is included here.

## Evidence and limits

SPEC.md §§6–8 is the accepted coordination design. README.md and AGENTS.md provide current
navigation. The older FWP plan is historical where superseded. A01–A24 and E01–E41 are audit
findings and proposed scenarios, not passed runtime tests. The 20 Python contract checks
passed on the fetched base before this amendment. The revised delivery reference/templates
and behavioral evaluation remain Module 3+ work; pilot, installation and release are pending.
The private original transfer package is available locally under `.local-handoff/`, ignored by Git.

The FWP choices, Module 1 and synthetic QuietFollow pilot are approved in `FWP-PLAN-v1` and the
reviewed implementation plan. Remaining choices are later module plans, license/provenance and
publication scope before public push, and the MVP installation/live-GitHub scope. Repository name,
local location and public visibility are known and are no longer open questions.
