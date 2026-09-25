# Preserve Binding Requirements — Implementation Plan

**Goal:** prepare a reduced documentation candidate for requirement-preserving handoff
and explicit review scope, without claiming complete defect discovery.

**Source base:** `b4de2efbcf00c20d530602e9a631998b2ee46423`.
**Preserved prior candidate:** `a54186b632b8a6558f61a6015da6180807612c0e`.
**Plan identity:** `REQUIREMENTS-PRESERVATION-v2-reduced`; bind PLAN review to this
file's SHA-256 and source base. On 2026-09-25 the owner approved stopping experiments
and narrowing the existing package to outcomes 01–02. This supersedes the original
three-outcome execution protocol; it does not accept the original package or authorize
publication. Preserve earlier commits and local evidence without rewriting history.

**Architecture:** compact clarification of existing canonical delivery/review references,
role prompts, and template fields. No new process, gate, role, registry, mandatory
separate coverage matrix, checker, or runtime mechanism.
**Stack:** existing Markdown instructions, Git, existing Python contract checks.
**Binding sources:** [SPEC](../SPEC.md), [AGENTS](../../../AGENTS.md), the active skill,
and the latest owner decision recorded here. Older plans and generic skill workflows
do not override the owner's explicit stop on further wording/behavioral trials.

## Accepted scope and ownership

One Work Item owns the reduced documentation change:

1. Preserve mandatory requirement and binding source → owning WI → observable acceptance
   in the existing plan/package. Compare each child brief with its approved WI block
   and normative sources before dispatch. Nearest result/non-goals cannot override
   binding requirements. Unauthorized narrowing or an unowned obligation blocks only
   the dependent handoff; authorized exclusions/deferrals retain their authority and
   conditions.
2. Assess source requirements, implementation, existing evidence, and closure of old
   findings separately. Derive applicable review scope from original normative sources,
   not only child wording, prior findings, or an old coverage table. Name unchecked areas
   and partial closure; these do not support a full PASS. Continue independent safe
   checks after a blocker and state the inspected scope and limitations. Do not promise
   discovery of every unknown defect or require the last probe's separate coverage map.

Outcome 03 is deferred: remove only this package's experimental critical-check
sufficiency protocol, property → concrete failing violation requirement, added
completion wording, and corresponding template fields/role-prompt demands. Where a
line combines outcomes 02 and 03, keep the minimal outcome-02 text. Preserve all
testing, privacy, evidence, and shared-async-state guarantees already in the source base,
including the accepted async guidance. Acceptance of the whole original package remains
deferred; removing experimental instructions does not turn failed evidence into PASS.

## Files and non-goals

Modify only this existing plan and these existing active-skill files:

- `references/agentic-development.md`: retain requirement ownership and child-brief
  reconciliation; keep routing to source-derived review scope, remove routing to the
  experimental critical-check protocol.
- `references/quality-gates.md`: retain the compact review-coverage clarification;
  remove only the added Critical check sufficiency section.
- `assets/work-item-and-review-templates.md`: retain compact ownership, reconciliation,
  review-scope, and separate assessment slots; remove the added Critical checks field.
- `assets/role-prompts.md`: retain bounded responsibilities for outcomes 01–02; remove
  the experimental critical-check sufficiency demand without duplicating canonical rules.

Keep SKILL.md routing, independent roles, native identity boundaries, exact-head review,
manual merge, and all source-base guarantees unchanged. No new repository document,
application change, installed skill/settings change, dependencies, scripts/tests/harness,
mandatory matrix, process redesign, or further behavioral/wording experiments. No push,
PR, merge, release, or installation is authorized. Keep private evidence outside Git.

## Execution and verification

1. Confirm the clean existing worktree, source base and preserved candidate; fetch and
   record current main without changing the checkout. Independently review this exact
   revised plan/base for the authorized narrowing before active-skill edits. No new
   research or owner reconfirmation is needed for this accepted boundary.
2. One independent Implementation agent uses skill-creator and applicable implementation
   guidance to edit the four bounded files. Compare against the full source-base diff,
   removing only outcome-03 additions and preserving outcomes 01–02 and base guarantees.
3. Run the existing `python3 -B -m unittest discover -s tests -v`,
   `shasum -a 256 -c BASELINE.sha256`, and `git diff --check`. Attempt existing
   quick_validate only if its dependency is available; do not install dependencies.
   Save fresh output and identity outside Git. No new tests or cold behavioral trials.
4. Commit locally without rewriting prior commits. Give independent Change Review the
   exact base/new head, this plan, original accepted boundaries, complete base-to-head
   diff, and fresh check evidence with clean bounded context. Review removal of 03,
   preservation of base guarantees, scope, and truthful claims. Any changed head requires
   current review; earlier source-text PASS does not transfer. Resolve concrete required
   corrections through the existing implementation/review process without new experiments.
5. Report only readiness of the reduced documentation candidate for owner consideration,
   with exact identities, changed paths, checks, review evidence, and limitations in the
   local evidence record. FINAL remains a distinct post-manual-merge role, not a claim
   available from this pre-merge documentation review.

PLAN and Change Review use native `gpt-5.6-sol/high`; Implementation uses native
`gpt-5.6-sol/medium`. Record requested/accepted assignment separately from independently
known runtime. Use distinct bounded internal sessions, one writer, and no new user task.

## Evidence limits and exit

Earlier experiments were mixed or unsuccessful. Historical replay was not a controlled
A/B comparison and did not establish complete review coverage. The synthetic R FAIL and
the missed edits-during-save scenario remain open in preserved local evidence. The
coverage-format probe did not demonstrate sufficient benefit to require its format.

The reduced candidate is deliberately not behaviorally retested: the owner stopped
further runs. Fresh structural checks and independent review can establish conformity of
the reduced text with this scope and preservation of base instructions; they cannot
establish behavioral reliability, close outcome 03 or the prior failures, accept all
three original outcomes, or authorize integration/publication. Exit is a locally committed,
exact-head-reviewed reduced documentation candidate with these limitations stated.
