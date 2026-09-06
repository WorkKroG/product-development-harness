# Product Development Harness First Working Version Implementation Plan

> **For agentic workers:** REQUIRED EXECUTION PROTOCOL: use the repository-specific user-owned task topology in this plan. A Task coordinator dispatches one separate Implementation task and one separate Change Review task per Work Item, then obtains module FINAL after manual merge. Subagents and inline execution must not replace these roles. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a repository-local, reviewable `product-development-cycle` harness candidate that can start or resume one synthetic Codex product, select the correct stage-aware next gate, and coordinate one module through independent review without manual result relay.

**Architecture:** Keep the existing skill as the entry point and add focused Markdown references and assets around it; Codex remains the runtime and Git remains the evidence layer. A small dependency-free Python checker validates structural contracts, while rubric-driven fixtures and the QuietFollow rehearsal validate behavior that static checks cannot prove.

**Tech Stack:** Codex skill Markdown/YAML, Python 3 standard library (`unittest`, `pathlib`, `json`, `hashlib`), Git, and Codex native task/message/wait capabilities during the authorized synthetic rehearsal.

**Spec:** `SPEC.md` (`FWP-PLAN-v1`, approved 2026-09-06)

## Global Constraints

- Develop the existing `product-development-cycle`; do not create a competing entry-point skill.
- `baseline/product-development-cycle/` and `BASELINE.sha256` remain byte-for-byte unchanged.
- Codex desktop is the only supported runtime for the FWP.
- The active order is Positioning → light Gate 3.5 → Journey; Gate 8 refines the same economics for the next investment.
- Preserve five maturity stages and separate architectural vision, current implementation, and transition plan.
- The prototype may be replaced completely; reuse is evidence-driven and real user data may not be discarded silently.
- Product decisions flow through the main Product coordinator; routine implementation details remain inside approved scope.
- Every implementation change has a separate Implementation task and Change Review task; every module has independent PLAN and FINAL review against exact content/head identity.
- Merge remains manual. No GitHub mutation, public push, global skill installation, paid action, or production release is authorized by this plan.
- Use native model/reasoning fields and never silently substitute an unavailable model.
- `gh` is the only GitHub service client when later authorized; FWP GitHub states are fixtures, not live mutations.
- Do not copy private `.local-handoff/` content, machine paths, credentials, historical task IDs, or Recipes-specific requirements into active files.
- Invoke `skill-creator` before editing the active skill and use `superpowers:test-driven-development` for every implementation Work Item.

---

## File Map

### Distribution

- `skills/product-development-cycle/SKILL.md` — short entry point, routing, invariant rules, and next-gate response contract.
- `skills/product-development-cycle/agents/openai.yaml` — existing display metadata and invocation prompt.
- `skills/product-development-cycle/references/lifecycle.md` — canonical gate map, Gate 3.5/8 boundary, five maturity stages, and transition evidence.
- `skills/product-development-cycle/references/financial-model.md` — one-page Gate 3.5 rubric plus investment-proportionate Gate 8.
- `skills/product-development-cycle/references/quality-gates.md` — applicability, evidence states, scenario matrix, and release constraints.
- `skills/product-development-cycle/references/agentic-development.md` — coordinator topology, task protocol, review identity, recovery, and manual merge.
- `skills/product-development-cycle/references/codex-runtime.md` — capability checks, task IDs, native handoff/wait semantics, platform denials, and GitHub boundary.
- `skills/product-development-cycle/references/dependencies.md` — specialist capability matrix, allowed fallback, and blocking conditions.
- `skills/product-development-cycle/assets/AGENTS.template.md` — project-local operating guide template.
- `skills/product-development-cycle/assets/project-profile.template.md` — version, stage, evidence, runtime, model, economics, and load profile.
- `skills/product-development-cycle/assets/PROJECT_STATUS.template.md` — current gate, evidence, decisions, risks, and next action.
- `skills/product-development-cycle/assets/role-prompts.md` — Product/Task/Implementation/Review/FINAL prompt contracts.
- `skills/product-development-cycle/assets/work-item-and-review-templates.md` — Work Item, decision package, manifest, PLAN, Change Review, and FINAL records.

### Verification

- `scripts/check_harness.py` — deterministic structural and identity checks with machine-readable JSON output.
- `tests/test_check_harness.py` — checker unit tests, including deliberately invalid fixture states.
- `tests/test_skill_contract.py` — active skill contract checks such as ordering, version identity, and forbidden leakage.
- `tests/fixtures/quietfollow/` — synthetic product profile and lifecycle artifacts.
- `tests/fixtures/quietfollow/product/quietfollow.py` — disposable JSON-backed prototype used only by the pilot.
- `tests/fixtures/quietfollow/product/test_quietfollow.py` — executable acceptance tests for the complete pilot path and recovery.
- `tests/fixtures/resume-legacy-4-5/` — existing-project migration evidence for E02/E41.
- `tests/fixtures/review-state/` — immutable SHA, queued task, model absence, denial, and drift events.
- `tests/scenarios.md` — FWP case procedure and reviewer rubric.
- `docs/validation.md` — actual run evidence, limitations, findings, and reruns; FINAL itself remains immutable native task evidence.
- `docs/PROJECT_STATUS.md` — actual harness state, candidate identity, evidence pointer, limitations, and next gate.
- `CHANGELOG.md` — user-visible FWP changes; no release claim.
- `README.md` — repository-local use, boundaries, verification commands, and later installation status.

---

## Delivery Protocol

For each task below:

1. Product coordinator records owner authorization, approved scope, and exact plan identity.
2. A user-owned Task coordinator task produces the task-local PLAN package.
3. A separate user-owned PLAN reviewer task returns `PLAN_PASS` or concrete changes.
4. After owner approval of the module plan, a user-owned Implementation task works in one isolated `codex/` branch/worktree.
5. A separate user-owned Change Review task reads binding sources and the full current diff.
6. Prompts and evidence record distinct coordinator, implementation, reviewer, and report-to task IDs plus requested/accepted native model fields.
7. A new commit invalidates the prior review verdict.
8. Manual merge is rehearsed only in a disposable synthetic repository during the FWP.
9. A separate user-owned FINAL task evaluates the exact resulting SHA/content identity.

There is no inline or subagent execution alternative for Implementation, Change Review, or FINAL in this repository.

---

### Task 1: Create the active skill and correct the lifecycle/economics contract

**Files:**

- Create: `skills/product-development-cycle/SKILL.md`
- Create: `skills/product-development-cycle/agents/openai.yaml`
- Create: `skills/product-development-cycle/references/lifecycle.md`
- Create: `skills/product-development-cycle/references/financial-model.md`
- Create: `tests/test_skill_contract.py`
- Create: `CHANGELOG.md`
- Modify: `README.md`

**Interfaces:**

- Consumes: immutable `baseline/product-development-cycle/*`, `SPEC.md` §§1–5.5, A14–A17/A20/A23/A24, E01–E06/E29/E31–E41.
- Produces: canonical gate labels `0`, `1`, `2`, `3`, `3.5`, `4`…`16`; maturity labels `working-prototype`, `mvp`, `scale-1`, `scale-2`, `mature`; entry response fields `Current gate`, `Evidence found`, `Missing or assumed`, `Risks`, `Recommended next action`, `Exit criteria`, `Next gate`.

- [ ] **Step 1: Write failing lifecycle contract tests**

```python
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ROOT / "skills/product-development-cycle"


class SkillContractTest(unittest.TestCase):
    def test_light_viability_precedes_journey(self):
        lifecycle = (ACTIVE / "references/lifecycle.md").read_text()
        self.assertLess(lifecycle.index("## 3.5."), lifecycle.index("## 4."))
        self.assertNotIn("## 4.5.", lifecycle)

    def test_gate_8_is_the_investment_finance_gate(self):
        lifecycle = (ACTIVE / "references/lifecycle.md").read_text()
        self.assertIn("## 8. Finance", lifecycle)
        self.assertIn("reuses Gate 3.5 evidence", lifecycle)

    def test_entry_point_names_all_five_maturity_stages(self):
        skill = (ACTIVE / "SKILL.md").read_text()
        for stage in ("working prototype", "MVP", "scale 1", "scale 2", "mature operation"):
            self.assertIn(stage, skill)
```

- [ ] **Step 2: Run the tests and verify the missing active skill fails**

Run: `python3 -m unittest tests.test_skill_contract -v`

Expected: FAIL because `skills/product-development-cycle/` does not exist.

- [ ] **Step 3: Create the active skill from the baseline and apply the approved semantic changes**

The active files must preserve the recognizable entry point while implementing these exact rules:

```markdown
## Start
1. Determine whether the request is start, resume, audit, module, or release.
2. Read existing artifacts and recognize their current names.
3. Determine current and target maturity stage.
4. Select the first missing or invalidated gate within that stage's scope.
5. Return one next action; ask only for a decision that existing evidence cannot answer.

## Maturity
Track working prototype, MVP, scale 1, scale 2, and mature operation separately.
For architecture, distinguish vision, current implementation, and transition plan.
Account-count labels never prove capacity without a measurable load profile.
```

The light viability contract must require approximate accessible market, meaningful competitors/substitutes, payer/value and broad income/cost ranges, strongest unknown, and one bounded next experiment. It must explicitly reject mandatory workbook, exact CAC/LTV, universal Month-24 target, and fabricated numbers at Gate 3.5. Gate 8 must reuse unchanged evidence and increase depth only for the named investment.

- [ ] **Step 4: Add version and change identity without claiming a release**

```markdown
## Unreleased
- Add the repository-local FWP candidate.
- Replace the heavy early Gate 4.5 with light Gate 3.5 before Journey.
- Add stage-aware architecture planning and evidence-driven transition review.
```

README must label the active tree an unreleased candidate and link to the verification command and known limitations.

- [ ] **Step 5: Run the lifecycle tests and baseline checksum**

Run: `python3 -m unittest tests.test_skill_contract -v`

Expected: PASS.

Run: `shasum -a 256 -c BASELINE.sha256`

Expected: all seven baseline paths report `OK`.

- [ ] **Step 6: Commit the reviewed Work Item**

```bash
git add README.md CHANGELOG.md skills/product-development-cycle tests/test_skill_contract.py
git commit -m "feat: add stage-aware lifecycle core"
```

---

### Task 2: Add product profile, evidence states, runtime, and dependency boundaries

**Files:**

- Create: `skills/product-development-cycle/references/quality-gates.md`
- Create: `skills/product-development-cycle/references/codex-runtime.md`
- Create: `skills/product-development-cycle/references/dependencies.md`
- Create: `skills/product-development-cycle/assets/AGENTS.template.md`
- Create: `skills/product-development-cycle/assets/project-profile.template.md`
- Create: `skills/product-development-cycle/assets/PROJECT_STATUS.template.md`
- Modify: `tests/test_skill_contract.py`

**Interfaces:**

- Consumes: Task 1 gate/stage labels; SPEC §§3–5 and §§7–10; A10–A22; E17–E30/E34–E35.
- Produces: Markdown profile headings `Process identity`, `Product`, `Maturity`, `Architecture`, `Load profile`, `Sources of truth`, `Runtime`, `Models`, `Economics`, `Applicability`; evidence states `applicable-covered`, `applicable-missing`, `not-applicable`, `deferred-with-trigger`.

- [ ] **Step 1: Extend the contract tests for the profile and dependency matrix**

```python
    def test_profile_has_decision_bearing_fields(self):
        profile = (ACTIVE / "assets/project-profile.template.md").read_text()
        for heading in (
            "## Process identity", "## Maturity", "## Architecture",
            "## Load profile", "## Runtime", "## Models", "## Economics",
        ):
            self.assertIn(heading, profile)

    def test_dependency_matrix_distinguishes_fallback_from_blocked(self):
        dependencies = (ACTIVE / "references/dependencies.md").read_text()
        self.assertIn("Allowed fallback", dependencies)
        self.assertIn("Block the gate when", dependencies)
        self.assertIn("Do not install dependencies silently", dependencies)
```

- [ ] **Step 2: Run the new tests and verify they fail**

Run: `python3 -m unittest tests.test_skill_contract -v`

Expected: FAIL on missing profile and dependency files.

- [ ] **Step 3: Implement the Markdown profile and status templates**

Use explicit `Unknown` values and links rather than machine-specific values. The architecture section must contain:

```markdown
## Architecture
- Vision identity:
- Current implementation identity:
- Current limits:
- Next transition trigger:
- Transition evidence required:
- Data preservation or lifecycle rule:
- Rollback/replacement path:
```

The load profile must name user unit, active period, peak concurrent work, heavy operation, data volume, latency objective, cost ceiling, evidence source, and next measurement.

- [ ] **Step 4: Implement runtime and dependency contracts**

`codex-runtime.md` must require usable thread IDs rather than queued client IDs, one bounded capability check per dependent stage, quiet waits, fresh-state recovery, and precise platform-denial reporting. `dependencies.md` must define purpose, detection, allowed fallback, and blocking condition for PM, challenge, finance, UX, security, planning, review, and verification capabilities.

- [ ] **Step 5: Run the contract tests**

Run: `python3 -m unittest tests.test_skill_contract -v`

Expected: PASS.

- [ ] **Step 6: Commit the reviewed Work Item**

```bash
git add skills/product-development-cycle/references skills/product-development-cycle/assets tests/test_skill_contract.py
git commit -m "feat: add project profile and runtime boundaries"
```

---

### Task 3: Implement delivery roles, handoffs, review identity, and recovery

**Files:**

- Create: `skills/product-development-cycle/references/agentic-development.md`
- Create: `skills/product-development-cycle/assets/role-prompts.md`
- Create: `skills/product-development-cycle/assets/work-item-and-review-templates.md`
- Modify: `tests/test_skill_contract.py`

**Interfaces:**

- Consumes: Task 1 gate/stage identity and Task 2 profile/runtime fields; SPEC §§6–9; A01–A13/A18/A19; E08–E25.
- Produces: decision package fields `Package identity`, `Outcome`, `Why`, `Scope`, `Non-goals`, `Options`, `Recommendation`, `Risks`, `Reviewer verdict`; handoff fields `Role`, `Parent`, `Report to`, `Plan identity`, `Process identity`, `Maturity`, `Architecture identity`, `Base`, `Head`, `Sources`, `Checks`, `Constraints`, `Next action`.

- [ ] **Step 1: Add failing role and review-identity tests**

```python
    def test_handoff_template_has_recovery_identity(self):
        templates = (ACTIVE / "assets/work-item-and-review-templates.md").read_text()
        for field in (
            "Plan identity", "Process identity", "Architecture identity",
            "Base SHA", "Head SHA", "Report to", "Next action",
        ):
            self.assertIn(field, templates)

    def test_review_contract_invalidates_stale_pass(self):
        agentic = (ACTIVE / "references/agentic-development.md").read_text()
        self.assertIn("A new head invalidates Change Review PASS", agentic)
        self.assertIn("Main drift invalidates FINAL", agentic)
        self.assertIn("Manual merge", agentic)

    def test_delivery_uses_distinct_authorized_tasks(self):
        templates = (ACTIVE / "assets/work-item-and-review-templates.md").read_text()
        for field in (
            "Owner authorization identity", "Task coordinator task ID",
            "Implementation task ID", "Change Review task ID", "FINAL task ID",
            "Requested model", "Accepted model",
        ):
            self.assertIn(field, templates)
        self.assertIn("must be distinct", templates)
```

- [ ] **Step 2: Run the tests and verify they fail**

Run: `python3 -m unittest tests.test_skill_contract -v`

Expected: FAIL on missing delivery files.

- [ ] **Step 3: Implement role topology and decision routing**

The reference must encode this single path:

```text
owner ↔ Product coordinator
Product coordinator → Task coordinator → Implementation ↔ Change Review
Task coordinator → PLAN review / FINAL review
all owner decisions return through Product coordinator
```

Task coordinator may resolve ordinary technical details inside approved scope. Significant scope, cost, risk, architecture impact, and release decisions return as a versioned package. Product approval does not override platform permissions.

- [ ] **Step 4: Implement review and recovery invariants**

Require full-diff Change Review, exact head, no duplicate accepted Work Items, same implementation/review pair for pre-merge correction, new corrective Work Item for post-merge defect, FINAL on current main identity, fresh-state reconciliation after resume, and no transport/model/credential switching to bypass denial.

- [ ] **Step 5: Encode the approved model matrix in role prompts**

```markdown
| Product/Task coordination and PLAN | gpt-5.6-sol | high |
| Ordinary implementation | gpt-5.6-sol | medium |
| Small obvious low-risk change | gpt-5.6-terra | medium |
| Change Review | gpt-5.6-sol | high |
| Architecture, security, FINAL, second opinion | gpt-6-astra | high |
| Early PM, finance, UX | gpt-5.6-sol | high |
```

Prompts must require availability verification and prohibit silent substitution or unsupported claims about the actual executing model.

- [ ] **Step 6: Run the contract tests**

Run: `python3 -m unittest tests.test_skill_contract -v`

Expected: PASS.

- [ ] **Step 7: Commit the reviewed Work Item**

```bash
git add skills/product-development-cycle/references/agentic-development.md skills/product-development-cycle/assets tests/test_skill_contract.py
git commit -m "feat: add reviewed delivery coordination"
```

---

### Task 4: Add a deterministic structural checker

**Files:**

- Create: `scripts/check_harness.py`
- Create: `tests/test_check_harness.py`
- Create: `tests/fixtures/review-state/valid.json`
- Create: `tests/fixtures/invalid/stale-final.json`
- Create: `tests/fixtures/invalid/leaked-binding.txt`
- Modify: `README.md`

**Interfaces:**

- Consumes: active skill files and templates from Tasks 1–3 plus `BASELINE.sha256`.
- Produces: exit code `0` only when every structural check passes; JSON object `{revision, passed, failed, checks}` where every check has `id`, `status`, and `evidence`; optional `--review-state PATH` selects the exact state checked by C10.

- [ ] **Step 1: Write failing checker unit tests**

```python
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HarnessCheckerTest(unittest.TestCase):
    def run_checker(self, root: Path, review_state: str = "tests/fixtures/review-state/valid.json"):
        return subprocess.run(
            [
                "python3", str(ROOT / "scripts/check_harness.py"),
                "--root", str(root), "--review-state", review_state, "--json",
            ],
            text=True, capture_output=True, check=False,
        )

    def test_repository_passes_structural_checks(self):
        result = self.run_checker(ROOT)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual([], json.loads(result.stdout)["failed"])

    def test_private_binding_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", ".local-handoff"))
            skill = root / "skills/product-development-cycle/SKILL.md"
            leak = (root / "tests/fixtures/invalid/leaked-binding.txt").read_text()
            skill.write_text(skill.read_text() + "\n" + leak)
            result = self.run_checker(root)
            self.assertNotEqual(0, result.returncode)
            self.assertEqual(["C11"], json.loads(result.stdout)["failed"])

    def test_stale_final_is_rejected_for_c10_only(self):
        result = self.run_checker(ROOT, "tests/fixtures/invalid/stale-final.json")
        self.assertNotEqual(0, result.returncode)
        self.assertEqual(["C10"], json.loads(result.stdout)["failed"])
```

- [ ] **Step 2: Run the checker tests and verify they fail**

Run: `python3 -m unittest tests.test_check_harness -v`

Expected: FAIL because the checker does not exist.

- [ ] **Step 3: Implement explicit checks**

Implement check IDs:

```text
C01 baseline-hashes
C02 required-active-files
C03 relative-links
C04 metadata
C05 gate-order
C06 single-light-viability
C07 five-maturity-stages
C08 required-profile-fields
C09 required-handoff-fields
C10 review-identity-consistency
C11 forbidden-private-bindings
C12 no-placeholder-markers
```

The checker may prove only these mechanical properties. C11 scans exactly these paths:

```text
skills/product-development-cycle/**/*.md
skills/product-development-cycle/**/*.yaml
README.md
CHANGELOG.md
docs/PROJECT_STATUS.md
docs/validation.md (when present)
```

It does not scan `baseline/`, `.local-handoff/`, `tests/`, `SPEC.md`, `AUDIT.md`,
`EVALUATION.md`, `HANDOFF.md`, `SOURCES.md`, `VERIFICATION.md`, or this implementation plan.
Its final output must state `Structural checks do not prove behavioral correctness.`

- [ ] **Step 4: Add invalid-state fixtures**

`valid.json` must contain equal `reviewed_main_sha` and `current_main_sha`. `stale-final.json`
must differ only in those two fields. `leaked-binding.txt` supplies the exact synthetic text
appended to an otherwise valid copied tree. Tests must assert the complete repository passes,
then the single mutations fail with exactly C10 and C11 respectively.

- [ ] **Step 5: Run checker and unit tests**

Run: `python3 -m unittest discover -s tests -p 'test_*.py' -v`

Expected: PASS.

Run: `python3 scripts/check_harness.py --root . --review-state tests/fixtures/review-state/valid.json --json`

Expected: exit `0`, empty `failed`, and twelve passed check IDs.

- [ ] **Step 6: Commit the reviewed Work Item**

```bash
git add README.md scripts/check_harness.py tests/test_check_harness.py tests/fixtures/invalid tests/fixtures/review-state/valid.json
git commit -m "test: add deterministic harness checks"
```

---

### Task 5: Add FWP behavioral fixtures and reviewer rubric

**Files:**

- Create: `tests/fixtures/quietfollow/AGENTS.md`
- Create: `tests/fixtures/quietfollow/PROJECT_STATUS.md`
- Create: `tests/fixtures/quietfollow/product-profile.md`
- Create: `tests/fixtures/quietfollow/positioning.md`
- Create: `tests/fixtures/resume-legacy-4-5/PROJECT_STATUS.md`
- Create: `tests/fixtures/resume-legacy-4-5/legacy-viability.md`
- Create: `tests/fixtures/review-state/events.json`
- Create: `tests/scenarios.md`
- Modify: `EVALUATION.md`

**Interfaces:**

- Consumes: E02, E08, E10–E14, E17, E20–E22, E25, E27–E28, E31, E33–E34, E37–E39, E41 and active contracts from Tasks 1–4.
- Produces: fixture input packages without expected answers; reviewer-only rubric with observable PASS/FAIL/BLOCKED criteria and evidence fields.

- [ ] **Step 1: Add a failing fixture-completeness test**

Append to `tests/test_skill_contract.py`:

```python
    def test_fwp_fixture_set_is_complete(self):
        fixtures = ROOT / "tests/fixtures"
        required = (
            "quietfollow/product-profile.md",
            "quietfollow/positioning.md",
            "quietfollow/product/test_quietfollow.py",
            "resume-legacy-4-5/legacy-viability.md",
            "review-state/events.json",
        )
        for relative in required:
            self.assertTrue((fixtures / relative).is_file(), relative)
```

- [ ] **Step 2: Run the test and verify it fails**

Run: `python3 -m unittest tests.test_skill_contract.SkillContractTest.test_fwp_fixture_set_is_complete -v`

Expected: FAIL on the first missing fixture.

- [ ] **Step 3: Write the QuietFollow input fixture**

The synthetic product is a local follow-up tracker for a solo consultant. The main path is create contact → schedule follow-up → see due item → record outcome. Its Positioning compares a spreadsheet, generic task app, and CRM. All names/data are synthetic; email sending, payment, analytics, and public deployment are out of scope.

- [ ] **Step 4: Write migration and review-state fixtures**

The legacy fixture contains useful market/competitor/cost evidence under a historical Gate 4.5 label plus one stale acquisition assumption. The event fixture contains queued task creation, reviewed SHA/current SHA mismatch, unavailable requested model, platform denial, old prompt drift, unchanged wait state, and release rehearsal with pending manual evidence.

- [ ] **Step 5: Write the reviewer-only scenario rubric**

For each selected E-case, record:

```markdown
### E12 — stale Change Review
- Input fixture:
- Allowed side effects: none
- Observable PASS:
- Observable FAIL:
- BLOCKED rule:
- Required transcript/tool evidence:
- Harness revision:
- Model/reasoning requested and accepted:
- Findings and rerun:
```

Do not place expected answers in the executor's input fixture. Update `EVALUATION.md` only with a link to actual FWP coverage; do not mark any scenario passed yet.

- [ ] **Step 6: Run all structural tests**

Run: `python3 -m unittest discover -s tests -p 'test_*.py' -v`

Expected: PASS.

- [ ] **Step 7: Commit the reviewed Work Item**

```bash
git add EVALUATION.md tests/fixtures tests/scenarios.md tests/test_skill_contract.py
git commit -m "test: add first working version scenarios"
```

---

### Task 6: Run the QuietFollow synthetic coordination rehearsal

**Files:**

- Create: `tests/fixtures/quietfollow/product/quietfollow.py`
- Create: `tests/fixtures/quietfollow/product/test_quietfollow.py`
- Modify: `tests/fixtures/quietfollow/PROJECT_STATUS.md`
- Create: `tests/fixtures/quietfollow/evidence/manifest.md`
- Create: `tests/fixtures/quietfollow/evidence/gate-3-5.md`
- Create: `tests/fixtures/quietfollow/evidence/journey.md`
- Create: `tests/fixtures/quietfollow/evidence/mvp-decision.md`
- Create: `tests/fixtures/quietfollow/evidence/requirements-and-risk.md`
- Create: `tests/fixtures/quietfollow/evidence/module-plan.md`
- Create: `tests/fixtures/quietfollow/evidence/review-record.md`
- Create: `tests/fixtures/quietfollow/evidence/scaling-review.md`
- Create: `tests/fixtures/quietfollow/evidence/release-rehearsal.md`
- Create: `docs/validation.md`
- Modify: `docs/PROJECT_STATUS.md`

**Interfaces:**

- Consumes: exact active harness revision from Tasks 1–5 and QuietFollow inputs.
- Produces: one executable JSON-backed local prototype, a complete five-part synthetic pilot evidence chain with no live GitHub mutations, and measured counts for manual relay, duplicate prompts/tasks, invalid PASS, and incorrect transitions.

- [ ] **Step 1: Build an input-only executor bundle and record its identity**

Create a disposable local directory containing only the active skill and copies of
`tests/fixtures/quietfollow/AGENTS.md`, `PROJECT_STATUS.md`, `product-profile.md`, and
`positioning.md`. Do not copy `tests/scenarios.md`, `EVALUATION.md`, or expected outcomes into
the executor bundle. The evaluator remains in a separate read-only task and receives the rubric
only after the executor has returned its artifacts/transcript.

The manifest must record the resolved disposable path, hashes of every copied input, active
harness commit/content identity, requested and accepted model/reasoning, allowed local/Codex-task
side effects, explicit forbidden side effects, and distinct Product/Task/Implementation/Review IDs.
Record as a limitation that filesystem isolation is procedural if the runtime can read outside
the assigned working directory.

- [ ] **Step 2: Run pilot part 1 — Positioning → Gate 3.5 → Journey**

The executor receives only the input bundle and active skill. The independent evaluator scores
E38 and the relevant portions of E03/E31. Gate 3.5 must end with one recommendation and one
bounded experiment; it must not produce a 24-month workbook.

- [ ] **Step 3: Run pilot part 2 — MVP decision and proportionate readiness gates**

Record the prototype result and one explicit MVP decision. Prepare testable requirements,
independent challenge, minimal local CLI/behavior states, risk/privacy review, and architecture
with vision/current/transition sections. The approved prototype architecture is one Python module
with a JSON file store; network, authentication, email, payments, analytics, and public deployment
remain non-goals.

- [ ] **Step 4: Work Item 1 RED → GREEN — create, schedule, and see due**

The product interface is:

```python
class Tracker:
    def __init__(self, path: str): ...
    def create_contact(self, name: str) -> str: ...
    def schedule_follow_up(self, contact_id: str, due_on: str) -> str: ...
    def due(self, as_of: str, include_completed: bool = False) -> list[dict[str, str]]: ...
    def record_outcome(self, follow_up_id: str, outcome: str) -> None: ...
```

Create the first failing acceptance test before the product module:

```python
from pathlib import Path
import tempfile
import unittest

from quietfollow import Tracker


class QuietFollowWorkItem1Test(unittest.TestCase):
    def test_create_schedule_and_see_due(self):
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "quietfollow.json")
            tracker = Tracker(path)
            contact_id = tracker.create_contact("Synthetic Client")
            follow_up_id = tracker.schedule_follow_up(contact_id, "2026-09-10")
            self.assertEqual(follow_up_id, tracker.due("2026-09-10")[0]["id"])
```

Run: `python3 -m unittest discover -s tests/fixtures/quietfollow/product -p 'test_*.py' -v`

Expected: FAIL because `quietfollow.py` does not exist. Implement only contact creation,
scheduling, JSON persistence, and due lookup. Run the test green, commit Work Item 1, obtain
Change Review on its exact head, and rehearse its manual merge in the disposable product repo.
Record the merged main SHA. Work Item 2 must start from that merged SHA.

- [ ] **Step 5: Work Item 2 RED → GREEN — record outcome and reload**

From main after the reviewed Work Item 1 merge, add this second failing test:

```python
class QuietFollowWorkItem2Test(unittest.TestCase):
    def test_record_outcome_survives_reload(self):
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "quietfollow.json")
            tracker = Tracker(path)
            contact_id = tracker.create_contact("Synthetic Client")
            follow_up_id = tracker.schedule_follow_up(contact_id, "2026-09-10")
            tracker.record_outcome(follow_up_id, "completed")
            reloaded = Tracker(path)
            item = reloaded.due("2026-09-10", include_completed=True)[0]
            self.assertEqual("completed", item["outcome"])
```

Run: `python3 -m unittest discover -s tests/fixtures/quietfollow/product -p 'test_*.py' -v`

Expected: Work Item 1 test PASS and Work Item 2 test FAIL because outcome recording is absent.
Implement only record/reload behavior, run both tests green, and commit the Work Item 2 candidate.
Use separate authorized Implementation and Change Review task IDs and record base/head identities.
Do not create GitHub objects.

- [ ] **Step 6: Exercise review correction, PASS invalidation, and E12**

The first complete main-path candidate lacks the binding recovery behavior for interrupted outcome
writes. Change Review must report that concrete violation. In the same implementation/reviewer
pair, add a failing `test_interrupted_outcome_write_preserves_previous_state`, replace direct writes
with temp-file plus atomic replace, and rerun the full test. Obtain Change Review PASS for corrected
SHA A; this closes the review-correction part of E14.

Then add a scoped failing `test_empty_outcome_is_rejected`, implement its validation, and create
SHA B in the disposable repository. Demonstrate that PASS(A) is rejected because current head is B,
then run a new full Change Review for B. Evidence must contain `PASS(A)`, `current=B`, explicit stale
verdict rejection, and the verdict for B. This closes E12 with an actual stale PASS rather than a
stale finding.

- [ ] **Step 7: Run pilot part 3 — disposable merge and release rehearsal**

Use a disposable synthetic Git repository for the product module. Rehearse one manual merge after
the corrected Change Review, capture the resulting main SHA, and evaluate rollout/rollback,
observability, and support criteria. Record `release rehearsal`; do not claim production release.

- [ ] **Step 8: Run pilot part 4 — resume and harness update with WIP preservation**

Resume from stored product evidence while one synthetic Work Item is in progress. Apply the
legacy Gate 4.5 migration fixture and an old-prompt drift event: reuse valid facts, ask only for
the stale assumption, update active instructions at a safe boundary, obtain ACK, and preserve
the WIP and completed Work Items. Exercise model absence and platform denial without changing
transport, credentials, model, or executor as a workaround.

- [ ] **Step 9: Run pilot part 5 — revise the scaling path from load evidence**

Provide synthetic evidence that the proposed queue/service split is unnecessary at the measured
profile and that the dominant constraint is local file-lock contention. Record the units, peak
operations, data volume, latency/cost limits, decision to defer the queue, safe next experiment,
data transition implications, and rollback. The evaluator scores E33/E34/E37.

- [ ] **Step 10: Write validation evidence and update the real project status**

`docs/validation.md` must list every selected E-case, including E13, as PASS/FAIL/BLOCKED with
direct artifact/transcript evidence, unresolved findings, rerun identity, and limitations. It must
report the four target counts and state that token/time savings are unknown unless measured.

Update `docs/PROJECT_STATUS.md` in this same reviewed scope with the candidate identity field,
evidence links, supported FWP subset, known limitations, and this next-action rule:

```markdown
Consult the independent native FINAL for the recorded current HEAD. If FINAL passes and HEAD has
not changed, the FWP is complete; otherwise correct the finding or rerun FINAL on the new HEAD.
```

Do not duplicate live task/GitHub state in the status document.

- [ ] **Step 11: Run final FWP verification before the candidate commit**

Run: `shasum -a 256 -c BASELINE.sha256`

Expected: all baseline files `OK`.

Run: `python3 -m unittest discover -s tests -p 'test_*.py' -v`

Expected: PASS.

Run: `python3 scripts/check_harness.py --root . --review-state tests/fixtures/review-state/valid.json --json`

Expected: all C01–C12 PASS.

- [ ] **Step 12: Commit every product, evidence, validation, and status change**

```bash
git add docs/PROJECT_STATUS.md docs/validation.md tests/fixtures/quietfollow
git commit -m "test: validate the synthetic coordination pilot"
```

- [ ] **Step 13: Record the immutable candidate SHA and rehearse E13**

Run: `git rev-parse HEAD`

Expected: one full 40-character candidate SHA recorded in the FINAL handoff. In a disposable copy,
advance main and prove that the prior FINAL state becomes stale; restore the candidate identity only
by selecting the unchanged candidate SHA, never by rewriting the real candidate.

- [ ] **Step 14: Obtain independent FINAL after the last commit**

FINAL runs in a separate user-owned task and returns PASS only if all five pilot parts and selected
FWP behavioral cases pass, no critical finding is open, and `reviewed_main_sha == current_main_sha`.
Store the verdict in the native FINAL task and the Product coordinator task record, outside the reviewed tree.
Do not make another repository change after FINAL; any later change requires a new FINAL.

---

## FWP Completion Criteria

- The active skill is recognizable as an evolution of the baseline and the baseline checksum remains valid.
- Gate 3.5 is the only early viability gate; Gate 8 reuses its evidence at investment-appropriate depth.
- Stage, architecture vision, current implementation, transition plan, load profile, and revisit trigger are distinguishable.
- Start/resume selects the first missing or invalidated gate without duplicate discovery or artifacts.
- Product/Task/Implementation/Change Review/FINAL roles use versioned handoffs and the approved model matrix.
- A new candidate SHA invalidates Change Review PASS; main drift invalidates FINAL.
- The selected FWP E-cases have independent actual evidence and no open critical failure.
- QuietFollow records 0 manual relays, 0 duplicate owner prompts, 0 duplicate tasks, and 0 invalid PASS transitions.
- README and validation state the exact supported subset and do not claim installation, live GitHub support, production release, or time/token savings.

## Deferred to MVP and Later Stages

- Complete E01–E41 coverage and all start/resume/audit/module/release modes.
- Clean Codex installation, discovery verification, pinned release/content identity, upgrade, rollback, and old-prompt migration.
- Live GitHub Issue/PR/CI rehearsal after explicit mutation authorization.
- Provenance/licensing decision, public-scope review, first public push, version tag, and release notes.
- Use on one or two real bounded products with WIP-preserving update evidence.
- Define scale evidence for the harness in terms of projects/runs, coordination failure rate, recovery, latency, and operating cost rather than raw account count.
- Revisit architecture before every scale transition; add services or persistent state only when measured constraints justify them.
