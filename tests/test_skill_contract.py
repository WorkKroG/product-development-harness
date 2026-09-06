from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ROOT / "skills/product-development-cycle"


class SkillContractTest(unittest.TestCase):
    def read_active(self, relative_path):
        path = ACTIVE / relative_path
        self.assertTrue(path.is_file(), f"missing active skill file: {relative_path}")
        return path.read_text(encoding="utf-8")

    def test_light_viability_precedes_journey(self):
        lifecycle = self.read_active("references/lifecycle.md")
        self.assertLess(lifecycle.index("## 3.5."), lifecycle.index("## 4."))
        self.assertNotIn("## 4.5.", lifecycle)

    def test_gate_8_is_the_investment_finance_gate(self):
        lifecycle = self.read_active("references/lifecycle.md")
        self.assertIn("## 8. Finance", lifecycle)
        self.assertIn("reuses Gate 3.5 evidence", lifecycle)

    def test_entry_point_names_all_five_maturity_stages(self):
        skill = self.read_active("SKILL.md")
        for stage in (
            "working prototype",
            "MVP",
            "scale 1",
            "scale 2",
            "mature operation",
        ):
            with self.subTest(stage=stage):
                self.assertIn(stage, skill)

    def test_entry_response_contract_is_complete(self):
        skill = self.read_active("SKILL.md")
        for field in (
            "Current gate",
            "Evidence found",
            "Missing or assumed",
            "Risks",
            "Recommended next action",
            "Exit criteria",
            "Next gate",
        ):
            with self.subTest(field=field):
                self.assertIn(field, skill)

    def test_entry_point_surfaces_process_identity_drift(self):
        skill = self.read_active("SKILL.md")
        start = skill[skill.index("## Start") : skill.index("## Operating rules")]
        for requirement in (
            "selected release, commit, or content identity",
            "actually loaded identity",
            "unknown, ambiguous, or mismatched",
            "Do not mix two active versions",
            "Never silently replace a shared or globally installed copy",
            "Pause only transitions that depend on the unresolved version selection",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, start)

    def test_active_skill_is_codex_only_and_routes_to_required_references(self):
        skill = self.read_active("SKILL.md")
        self.assertIn("Codex-only", skill)
        links = re.findall(r"\[[^]]+\]\(([^)]+\.md)\)", skill)
        self.assertTrue(
            {
                "references/financial-model.md",
                "references/lifecycle.md",
                "references/quality-gates.md",
                "references/codex-runtime.md",
                "references/dependencies.md",
                "assets/AGENTS.template.md",
                "assets/project-profile.template.md",
                "assets/PROJECT_STATUS.template.md",
            }.issubset(set(links)),
            f"missing required routes from SKILL.md; found: {sorted(set(links))}",
        )
        for target in links:
            with self.subTest(target=target):
                self.assertTrue((ACTIVE / target).is_file())

    def test_profile_has_decision_bearing_fields_and_unknown_defaults(self):
        profile = self.read_active("assets/project-profile.template.md")
        for heading in (
            "## Process identity",
            "## Product",
            "## Maturity",
            "## Architecture",
            "## Load profile",
            "## Sources of truth",
            "## Runtime",
            "## Models",
            "## Economics",
            "## Applicability",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, profile)
        self.assertIn("Unknown", profile)
        for field in (
            "Vision identity",
            "Current implementation identity",
            "Current limits",
            "Next transition trigger",
            "Transition evidence required",
            "Data preservation or lifecycle rule",
            "Rollback/replacement path",
            "User unit",
            "Active period",
            "Peak concurrent work or peak operation rate",
            "Heavy operation",
            "Data volume",
            "Latency/reliability objective",
            "Cost ceiling",
            "Evidence source",
            "Next measurement",
            "Requested model/reasoning",
            "Accepted native assignment",
            "Allowed parallelism",
            "Actual dependencies",
        ):
            with self.subTest(field=field):
                self.assertIn(field, profile)

    def test_evidence_states_are_consistent_across_active_artifacts(self):
        states = (
            "applicable-covered",
            "applicable-missing",
            "not-applicable",
            "deferred-with-trigger",
        )
        for relative_path in (
            "references/quality-gates.md",
            "assets/project-profile.template.md",
            "assets/PROJECT_STATUS.template.md",
        ):
            content = self.read_active(relative_path)
            for state in states:
                with self.subTest(relative_path=relative_path, state=state):
                    self.assertIn(state, content)

    def test_quality_gates_define_evidence_records_and_readiness_boundaries(self):
        quality = self.read_active("references/quality-gates.md")
        for field in (
            "Gate/check",
            "State",
            "Current scope/stage",
            "Evidence source",
            "Identity/date",
            "Rationale",
            "Owner/decision authority",
            "Missing evidence or accepted limitation",
            "Revisit trigger",
            "Dependent transition",
        ):
            with self.subTest(field=field):
                self.assertIn(field, quality)
        for dimension in (
            "Identity and permission",
            "Data state and lifecycle",
            "Failure and recovery",
            "Concurrency and duplication",
            "Accessibility and device",
            "Security and privacy",
            "Operations and rollback",
        ):
            with self.subTest(dimension=dimension):
                self.assertIn(dimension, quality)
        self.assertIn("never equal PASS", quality)
        self.assertIn("block only the dependent transition", quality)
        self.assertIn("green CI", quality)
        self.assertIn("release rehearsal is not a production launch", quality)

    def test_status_is_a_fresh_evidence_pointer_with_one_next_action(self):
        status = self.read_active("assets/PROJECT_STATUS.template.md")
        for field in (
            "Current stage",
            "Target stage",
            "Current gate",
            "Profile identity",
            "Process identity",
            "Architecture identity",
            "Decisions and accepted risks",
            "Blockers and limitations",
            "Fresh-state timestamp/source",
            "## Recommended next action",
            "Next gate",
        ):
            with self.subTest(field=field):
                self.assertIn(field, status)
        self.assertEqual(1, status.count("## Recommended next action"))
        self.assertIn("Fresh GitHub, native task, and Git evidence overrides this pointer", status)
        self.assertIn("Do not duplicate live Issue, PR, CI, merge, or task state", status)

    def test_runtime_contract_covers_native_identity_wait_recovery_and_authority(self):
        runtime = self.read_active("references/codex-runtime.md")
        for requirement in (
            "at most one bounded capability check",
            "current stage or action actually depends",
            "queued client ID",
            "never a usable task/thread ID",
            "do not create a duplicate",
            "one compact bounded wait",
            "Unchanged in-progress state is silent",
            "Update the existing task or monitor",
            "preserve work in progress",
            "record acknowledgement",
            "Preserve work in progress",
            "Requested model/reasoning",
            "Accepted native assignment",
            "No prompt text proves the executing model",
            "Never bypass",
            "Product mandate, account access, and platform permission",
            "gh-only",
            "bounded authenticated read check",
            "No browser or UI",
            "untrusted data",
            "cannot expand scope",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, runtime)

    def test_dependency_matrix_distinguishes_fallback_from_blocked(self):
        dependencies = self.read_active("references/dependencies.md")
        for heading in (
            "Purpose",
            "Needed when",
            "Detection",
            "Allowed fallback",
            "Block the gate when",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, dependencies)
        for capability in (
            "PM",
            "Challenge",
            "Finance",
            "UX",
            "Security",
            "Planning",
            "Review",
            "Verification",
        ):
            with self.subTest(capability=capability):
                self.assertRegex(dependencies, rf"\|\s*{capability}\s*\|")
        for rule in (
            "Do not install dependencies silently",
            "BLOCKED is not PASS",
            "catalog or README claim is not availability proof",
            "Gate 3.5",
            "Gate 8",
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, dependencies)

    def test_agents_template_preserves_local_authority_and_review_boundaries(self):
        agents = self.read_active("assets/AGENTS.template.md")
        for requirement in (
            "Adapt this template",
            "Product profile",
            "Project status",
            "Sources of truth",
            "Commands",
            "Authority",
            "Exceptions",
            "Unknown",
            "Product approval",
            "platform permission",
            "scoped branch",
            "manual merge",
            "independent review",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, agents)

    def test_templates_are_portable_and_free_of_transient_bindings(self):
        combined = "\n".join(
            self.read_active(relative_path)
            for relative_path in (
                "assets/AGENTS.template.md",
                "assets/project-profile.template.md",
                "assets/PROJECT_STATUS.template.md",
            )
        )
        for forbidden in (
            ".local-handoff",
            "/Users/",
            "WorkKroG/product-development-harness",
            "github.com/WorkKroG",
            "client-new-thread:",
            "ghp_",
            "github_pat_",
            "npm run",
            "go test",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, combined)

    def test_stage_aware_architecture_and_data_transition_are_explicit(self):
        combined = "\n".join(
            (self.read_active("SKILL.md"), self.read_active("references/lifecycle.md"))
        )
        for concept in (
            "architecture vision",
            "current implementation",
            "transition plan",
            "measurable load profile",
            "Prototype code may be replaced",
            "Real user data must not be silently discarded",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, combined)

    def test_gate_3_5_is_lightweight_and_does_not_mandate_precision(self):
        finance = self.read_active("references/financial-model.md")
        for requirement in (
            "accessible market",
            "competitors and substitutes",
            "payer or value",
            "broad income and cost ranges",
            "strongest unknown",
            "one bounded experiment",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, finance)
        for rejected_requirement in (
            "workbook is not required",
            "exact CAC/LTV is not required",
            "universal Month-24 target is not required",
            "Never fabricate numbers",
        ):
            with self.subTest(rejected_requirement=rejected_requirement):
                self.assertIn(rejected_requirement, finance)

    def test_gate_8_deepens_only_for_the_named_investment(self):
        finance = self.read_active("references/financial-model.md")
        self.assertIn("Reuse unchanged Gate 3.5 evidence", finance)
        self.assertIn("only enough for the named investment", finance)

    def test_gate_3_5_reuses_valid_legacy_gate_4_5_evidence(self):
        lifecycle = self.read_active("references/lifecycle.md")
        gate = lifecycle[lifecycle.index("## 3.5.") : lifecycle.index("## 4.")]
        for requirement in (
            "Map still-valid historical Gate 4.5 evidence and decisions into Gate 3.5",
            "Ask only for missing or stale inputs",
            "Preserve the historical baseline and recorded decisions",
            "exactly one active early checkpoint",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, gate)

    def test_candidate_docs_do_not_claim_release_or_installation_support(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("Unreleased candidate", readme)
        self.assertIn("python3 -m unittest tests.test_skill_contract -v", readme)
        self.assertIn("Known limitations", readme)
        self.assertIn("## Unreleased", changelog)
        self.assertNotIn("Installation is supported", readme)
        self.assertNotIn("Released", changelog)

    def test_openai_metadata_keeps_the_existing_identity(self):
        metadata = self.read_active("agents/openai.yaml")
        self.assertIn('display_name: "Product Development Cycle"', metadata)
        self.assertIn("$product-development-cycle", metadata)


if __name__ == "__main__":
    unittest.main()
