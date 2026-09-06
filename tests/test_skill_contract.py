from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ROOT / "skills/product-development-cycle"


class SkillContractTest(unittest.TestCase):
    def read_active(self, relative_path):
        return (ACTIVE / relative_path).read_text(encoding="utf-8")

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

    def test_active_skill_is_codex_only_and_routes_to_task_one_references(self):
        skill = self.read_active("SKILL.md")
        self.assertIn("Codex-only", skill)
        links = re.findall(r"\[[^]]+\]\(([^)]+\.md)\)", skill)
        self.assertEqual(
            {"references/financial-model.md", "references/lifecycle.md"},
            set(links),
        )
        for target in links:
            with self.subTest(target=target):
                self.assertTrue((ACTIVE / target).is_file())

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
