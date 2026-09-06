# Project status

Date: 2026-09-06. Repository: `WorkKroG/product-development-harness`.

## Current stage

The owner authorized a separate project and supplied the repository. The prepared transfer
package has been adapted for this project. The source skill is preserved under `baseline/`;
the target harness is not implemented or installed. Bootstrap is local; no public push is implied.

The next stage is to prepare and approve the first working-version plan (Technical/Delivery
planning, with an evidence-based check of any material missing requirements). Do not repeat
discovery or all workshops merely because this is a new repository.

## Accepted decisions

- Evolve the existing product-development-cycle; Codex-only initial scope.
- Five maturity stages, early architectural vision, staged implementation and reconsideration
  before scaling. Prototype code may be discarded; rewriting is not mandatory.
- Light Gate 3.5 between Positioning and Journey replaces the heavy early 4.5. Later Finance
  refines the same economics for the investment at hand.
- Main coordinator for owner decisions; automatic result handoff, independent plan/change/module
  review, agreed native model matrix, sole `gh` service access, manual merge.
- Start with a small usable process, validate on a small synthetic product, then extend coverage.
- Bootstrap baseline and specification separately before implementation.

## Next action for the main coordinator

Read AGENTS.md, README.md, SPEC.md, AUDIT.md, SOURCES.md, HANDOFF.md and EVALUATION.md.
Check baseline hashes. Propose a compact first-working-version plan: user outcome, scope,
existing mechanisms to reuse, bounded modules/dependencies, model assignment, meaningful checks,
pilot and completion criteria. Separate later installation/release and broader lifecycle testing.
Bring remaining consequential choices and this plan to the owner in this task. Do not ask again
for accepted principles, and do not start implementation or create child tasks before its mandate.

## Evidence and limits

SPEC.md and README.md contain the transferred requirements/decisions. VERIFICATION.md records
package checks. A01–A24 and E01–E41 are audit findings and proposed scenarios, not passed runtime
tests. Independent specification review, pilot, installation and release are still pending.
The private original transfer package is available locally under `.local-handoff/`, ignored by Git.

Remaining choices: details of the first-version plan and consequential unresolved SPEC proposals;
pilot; license/provenance and publication scope before public push. Repository name, local location
and public visibility are now known, and no longer open questions.
