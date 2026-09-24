# Preserve Binding Requirements — Implementation Plan

**Goal:** preserve approved mandatory behavior through work-item handoff, independent
review, and critical test evidence using the existing workflow records.

**Source base:** `b4de2efbcf00c20d530602e9a631998b2ee46423`.
**Plan identity:** `REQUIREMENTS-PRESERVATION-v1`; bind PLAN review to this file's
SHA-256 and the source base. The owner has approved the bounded behavior and local
implementation below; ordinary technical choices do not reopen that approval.

**Architecture:** one cohesive instruction change, with dispatch rules in the delivery
reference, evidence/review rules in quality gates, and short fields/pointers in existing
templates and role prompts. No new gate, role, registry, checker, or runtime mechanism.
**Stack:** existing Markdown instructions, Git, existing Python contract checks.
**Binding sources:** [SPEC](../SPEC.md), [AGENTS](../../../AGENTS.md), the active skill,
and the accepted requirements recorded here. Older documentation-only direction and
historical plans do not replace the owner's current bounded mandate.

## Accepted scope and ownership

One Work Item owns these three connected outcomes:

1. Preserve mandatory requirement and binding source → owning WI → observable acceptance
   in the existing plan/package. Compare each child brief with its approved WI block
   before dispatch. Nearest result/non-goals cannot override binding requirements.
   Unauthorized narrowing or an unowned obligation blocks only the dependent handoff;
   authorized exclusions/deferrals retain their authority and conditions.
2. Assess source requirements, implementation, evidence fitness, and closure of old
   findings separately. Derive applicable obligation coverage from original normative
   sources, not a copied child brief or prior coverage table. Name unchecked areas;
   partial closure is not full PASS. Continue independent safe checks after a blocker.
   Do not promise discovery of every unknown defect.
3. For critical checks, name the property and a concrete violation that would fail the
   check. Absence of a forbidden effect does not prove a required positive effect.
   Mocks, lifecycle, and completion must match the real contract. No mandatory mutation
   testing of every test.

## Files and non-goals

Modify only these existing active-skill files:

- `references/agentic-development.md`: requirement ownership, dispatch reconciliation,
  and routing to the existing review/evidence rules.
- `references/quality-gates.md`: source-derived coverage and critical-check sufficiency.
- `assets/work-item-and-review-templates.md`: compact work-package/review slots for the
  above relationships, reusing existing evidence states without a second registry.
- `assets/role-prompts.md`: concise responsibilities/pointers for Task, PLAN,
  Implementation, Change Review, and FINAL, without repeating the canonical paragraphs.

The technical plan itself is the only new repository document. Keep SKILL.md routing,
independent roles, native identity boundaries, exact-head review, human merge, safety,
privacy, and the existing shared-async-state paragraph unchanged. No application,
installed skill, settings, decomposition/breaker redesign, async matrix, skill-composition
policy, platform integration, new tests/programs, or other feedback direction is included.
No public push/PR, merge, release, or installation is authorized for this package.

## Execution and verification

- [ ] Independently review this exact plan/base before active-skill changes. The reviewer
  checks all accepted obligations, allowed paths, proportionality, and the bounded
  before/after protocol. A changed plan/base requires a fresh PLAN recommendation.
- [ ] Before editing, freeze evaluator criteria separately from executor inputs. Use one
  small equipment-inspection packet with source requirements, approved parent WI,
  narrowed child brief, candidate/tests, and a prior coverage/closure claim. A Task
  agent decides the next handoff; a separate Change Review agent evaluates the supplied
  candidate independently. Include revision selection lost in the child brief, dirty
  navigation, a required audit event, and a privacy-only check that passes without it.
  Include accurate coverage/closed findings and an authorized deferral to detect false
  findings, plus a separately authorized safe task that must not freeze.
- [ ] Run one baseline pass for each role and one simple static-label counterexample,
  with fresh agents, the current skill, realistic raw inputs, and no expected answers,
  author context, feedback, or evaluator criteria. Store only compact local artifacts
  outside the repository. Do not implement an application or test harness.
- [ ] One Implementation agent edits the four bounded files using skill-creator and
  writing-skills. Add only operationally useful guidance for the three accepted outcomes;
  keep existing records and use cross-references to avoid duplicating rules.
- [ ] Repeat the same three inputs once with the candidate and fresh agents. Compare
  actual artifacts to the frozen criteria, including false findings and process overhead.
  Mark ambiguous behavior as inconclusive. If baseline passes, retain that result;
  historical failure is separate evidence, not a synthetic RED or causal-gain claim.
- [ ] Run `python3 -B -m unittest discover -s tests -v`,
  `shasum -a 256 -c BASELINE.sha256`, and `git diff --check`. Existing quick_validate may
  be attempted if its dependency is available; do not install dependencies for this edit.
  Do not add wording-matching tests that merely restate the instructions.
- [ ] Commit locally and give independent Change Review the exact base/head, this plan,
  original requirements, complete diff, checks, and bounded raw evaluation artifacts,
  without the author's conversation. Resolve required findings using the existing
  correction process. No FINAL claim before a separately authorized manual merge.

## Roles, limits, and exit

PLAN/Task probes/Change Review use native `gpt-5.6-sol/high`; ordinary Implementation
uses `gpt-5.6-sol/medium`; the simple counterexample uses `gpt-5.6-terra/medium`.
Record requested/accepted assignment separately from independently known runtime.
Use distinct internal sessions; one writer. No new user-owned task.

Exit: the scoped candidate satisfies all three accepted instruction outcomes, preserves
existing guarantees and the simple counterexample, has current relevant checks and an
independent exact-head review, and reports before/after findings and limitations.
Single synthetic responses do not prove statistical reliability, application correctness,
model/runtime behavior, or causal attribution to the skill. The next real task remains
the practical validation. Escalate only material scope/risk/cost or shared-contract changes.
