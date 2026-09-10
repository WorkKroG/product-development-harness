from __future__ import annotations

import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures"
QUIETFOLLOW = FIXTURES / "quietfollow"
LEGACY = FIXTURES / "resume-legacy-4-5"
EVENTS = FIXTURES / "review-state/events.json"
SCENARIOS = ROOT / "tests/scenarios.md"

QUIETFOLLOW_INPUTS = (
    "AGENTS.md",
    "PROJECT_STATUS.md",
    "product-profile.md",
    "positioning.md",
)
LEGACY_INPUTS = ("PROJECT_STATUS.md", "legacy-viability.md")
EVENT_IDS = {
    "queued-creation",
    "sha-mismatch",
    "unavailable-requested-model",
    "platform-denial",
    "old-prompt-drift",
    "unchanged-quiet-wait",
    "release-rehearsal-manual-evidence-pending",
}
SELECTED_CASES = {
    "E02", "E08", "E10", "E11", "E12", "E13", "E14", "E17",
    "E20", "E21", "E22", "E25", "E27", "E28", "E31", "E33",
    "E34", "E37", "E38", "E39", "E41",
}
RUBRIC_FIELDS = (
    "Input fixture",
    "Allowed side effects",
    "Observable PASS",
    "Observable FAIL",
    "BLOCKED rule",
    "Dependent action or gate state",
    "Required transcript/tool evidence",
    "Execution environment",
    "Harness revision",
    "Requested and accepted model/reasoning",
    "Independently verified runtime fact",
    "Actual outcome and verdict",
    "Findings and rerun",
)
EVALUATOR_ONLY_KEYS = {
    "expected",
    "expected_outcome",
    "actual_outcome",
    "observable_pass",
    "observable_fail",
    "blocked_rule",
    "dependent_action_state",
    "allowed_side_effects",
    "evaluator_notes",
    "verdict",
}


def all_json_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from all_json_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from all_json_keys(child)


def scenario_sections(markdown):
    matches = list(re.finditer(r"(?m)^### (E\d{2}) — .+$", markdown))
    sections = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        sections[match.group(1)] = markdown[match.end():end]
    return sections


class BehavioralFixtureContractTest(unittest.TestCase):
    def test_required_input_files_exist_without_module_6_dependencies(self):
        for directory, relative_paths in (
            (QUIETFOLLOW, QUIETFOLLOW_INPUTS),
            (LEGACY, LEGACY_INPUTS),
        ):
            for relative_path in relative_paths:
                with self.subTest(path=f"{directory.name}/{relative_path}"):
                    path = directory / relative_path
                    self.assertTrue(path.is_file())
                    self.assertFalse(path.is_symlink())
        self.assertTrue(EVENTS.is_file())
        self.assertFalse(EVENTS.is_symlink())

    def test_review_events_are_complete_input_only_observations(self):
        payload = json.loads(EVENTS.read_text(encoding="utf-8"))
        self.assertIsInstance(payload, dict)
        self.assertEqual({"schema_version", "fixture_kind", "events"}, set(payload))
        self.assertEqual(1, payload["schema_version"])
        self.assertEqual("input-only", payload["fixture_kind"])
        self.assertIsInstance(payload["events"], list)
        self.assertEqual(EVENT_IDS, {event["id"] for event in payload["events"]})
        self.assertEqual(len(EVENT_IDS), len(payload["events"]))
        for event in payload["events"]:
            self.assertEqual(
                {"id", "observed_state", "available_evidence", "unknowns"},
                set(event),
            )
            self.assertIsInstance(event["id"], str)
            self.assertIsInstance(event["observed_state"], dict)
            self.assertIsInstance(event["available_evidence"], list)
            self.assertIsInstance(event["unknowns"], list)
        self.assertTrue(EVALUATOR_ONLY_KEYS.isdisjoint(all_json_keys(payload)))

    def test_executor_inputs_do_not_contain_reviewer_rubric_fields(self):
        forbidden_labels = tuple(f"- {field}:" for field in RUBRIC_FIELDS)
        for directory, relative_paths in (
            (QUIETFOLLOW, QUIETFOLLOW_INPUTS),
            (LEGACY, LEGACY_INPUTS),
        ):
            for relative_path in relative_paths:
                text = (directory / relative_path).read_text(encoding="utf-8")
                with self.subTest(path=f"{directory.name}/{relative_path}"):
                    for forbidden in forbidden_labels:
                        self.assertNotIn(forbidden, text)

    def test_reviewer_rubric_covers_exact_selected_cases_and_fields(self):
        markdown = SCENARIOS.read_text(encoding="utf-8")
        self.assertIn("Reviewer only", markdown)
        self.assertIn("must not be copied into an executor bundle", markdown)
        case_ids = re.findall(r"(?m)^### (E\d{2}) — .+$", markdown)
        self.assertEqual(len(SELECTED_CASES), len(case_ids))
        self.assertEqual(SELECTED_CASES, set(case_ids))
        sections = scenario_sections(markdown)
        for case_id, section in sections.items():
            with self.subTest(case_id=case_id):
                for field in RUBRIC_FIELDS:
                    self.assertEqual(1, section.count(f"- {field}:"), field)

    def test_evaluation_links_prepared_coverage_without_execution_claim(self):
        evaluation = (ROOT / "EVALUATION.md").read_text(encoding="utf-8")
        self.assertIn("[Module 5 reviewer rubric](tests/scenarios.md)", evaluation)
        self.assertIn("prepared coverage, not executed evidence", evaluation)
        self.assertNotIn("Module 5 cases passed", evaluation)
