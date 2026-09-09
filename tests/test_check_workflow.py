from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check_workflow.py"
FIXTURES = ROOT / "tests/fixtures"


def load_checker_module():
    if not SCRIPT.is_file():
        raise AssertionError(f"production checker is missing: {SCRIPT.relative_to(ROOT)}")
    spec = importlib.util.spec_from_file_location("check_workflow", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run_checker(root: Path, review_state: str | None, *, json_output: bool = True):
    command = [sys.executable, str(SCRIPT), "--root", str(root)]
    if review_state is not None:
        command += ["--review-state", review_state]
    if json_output:
        command.append("--json")
    return subprocess.run(command, text=True, capture_output=True, check=False)


class WorkflowCheckerCoreTest(unittest.TestCase):
    def setUp(self):
        self.checker = load_checker_module()
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name) / "repo"
        self.root.mkdir()

    def write(self, relative_path: str, content: bytes = b"fixture") -> Path:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def populate_revision_inputs(self):
        for relative_path in self.checker.REVISION_PATHS:
            self.write(relative_path, f"content:{relative_path}\n".encode())

    def test_resolve_root_requires_existing_directory(self):
        self.assertEqual(self.root.resolve(), self.checker.resolve_root(self.root))
        with self.assertRaisesRegex(self.checker.InputError, "root must be an existing directory"):
            self.checker.resolve_root(self.root / "missing")

    def test_review_state_must_resolve_inside_root(self):
        inside = self.write("state.json", b"{}")
        self.assertEqual(inside.resolve(), self.checker.resolve_review_state(self.root, Path("state.json")))
        outside = Path(self.tempdir.name) / "outside.json"
        outside.write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(self.checker.InputError, "review-state must be inside root"):
            self.checker.resolve_review_state(self.root, outside)

    def test_revision_uses_the_framed_algorithm(self):
        self.populate_revision_inputs()
        expected = hashlib.sha256()
        expected.update(b"PDW-STRUCTURAL-REVISION-v1\0")
        for relative_path in sorted(self.checker.REVISION_PATHS):
            encoded_path = relative_path.encode("utf-8")
            content = (self.root / relative_path).read_bytes()
            expected.update(struct.pack(">Q", len(encoded_path)))
            expected.update(encoded_path)
            expected.update(b"F")
            expected.update(struct.pack(">Q", len(content)))
            expected.update(content)
        self.assertEqual(f"sha256:{expected.hexdigest()}", self.checker.compute_revision(self.root))

    def test_revision_changes_for_baseline_content_but_not_review_state(self):
        self.populate_revision_inputs()
        before = self.checker.compute_revision(self.root)
        (self.root / "baseline/product-development-cycle/SKILL.md").write_bytes(b"mutated")
        after_baseline = self.checker.compute_revision(self.root)
        self.assertNotEqual(before, after_baseline)
        self.write("review-state.json", b'{"fixture":"one"}')
        before_state = self.checker.compute_revision(self.root)
        (self.root / "review-state.json").write_bytes(b'{"fixture":"two"}')
        self.assertEqual(before_state, self.checker.compute_revision(self.root))

    def test_missing_file_has_a_stable_revision_frame(self):
        first = self.checker.compute_revision(self.root)
        second = self.checker.compute_revision(self.root)
        self.assertEqual(first, second)
        self.assertRegex(first, r"^sha256:[0-9a-f]{64}$")

    def test_revision_frames_leaf_and_ancestor_symlinks_as_nonregular(self):
        outside = Path(self.tempdir.name) / "outside"
        outside.mkdir()
        (outside / "README.md").write_bytes(b"outside")

        leaf = self.root / "README.md"
        leaf.symlink_to(outside / "README.md")
        self.assertEqual((b"O", b""), self.checker._file_frame(self.root, "README.md"))
        leaf.unlink()

        (outside / "skills").mkdir()
        external_skill = outside / "skills/product-development-workflow/SKILL.md"
        external_skill.parent.mkdir(parents=True)
        external_skill.write_bytes(b"outside")
        (self.root / "skills").symlink_to(outside / "skills", target_is_directory=True)
        self.assertEqual(
            (b"O", b""),
            self.checker._file_frame(
                self.root, "skills/product-development-workflow/SKILL.md"
            ),
        )

    def test_dangling_leaf_symlink_revision_is_external_state_invariant(self):
        outside_target = Path(self.tempdir.name) / "outside/README.md"
        (self.root / "README.md").symlink_to(outside_target)

        before = self.checker.compute_revision(self.root)
        self.assertEqual((b"O", b""), self.checker._file_frame(self.root, "README.md"))

        outside_target.parent.mkdir()
        outside_target.write_bytes(b"appeared outside")
        self.assertEqual((b"O", b""), self.checker._file_frame(self.root, "README.md"))
        self.assertEqual(before, self.checker.compute_revision(self.root))

    def test_dangling_ancestor_symlink_revision_is_external_state_invariant(self):
        outside_skills = Path(self.tempdir.name) / "outside-skills"
        (self.root / "skills").symlink_to(outside_skills, target_is_directory=True)
        relative_path = "skills/product-development-workflow/SKILL.md"

        before = self.checker.compute_revision(self.root)
        self.assertEqual(
            (b"O", b""), self.checker._file_frame(self.root, relative_path)
        )

        external_skill = outside_skills / "product-development-workflow/SKILL.md"
        external_skill.parent.mkdir(parents=True)
        external_skill.write_bytes(b"appeared outside")
        self.assertEqual(
            (b"O", b""), self.checker._file_frame(self.root, relative_path)
        )
        self.assertEqual(before, self.checker.compute_revision(self.root))

    def test_optional_validation_through_dangling_ancestor_is_external_state_invariant(self):
        outside_docs = Path(self.tempdir.name) / "outside-docs"
        (self.root / "docs").symlink_to(outside_docs, target_is_directory=True)
        relative_path = "docs/validation.md"

        before = self.checker.compute_revision(self.root)
        self.assertEqual(
            (b"O", b""), self.checker._file_frame(self.root, relative_path)
        )

        outside_docs.mkdir()
        (outside_docs / "validation.md").write_bytes(b"appeared outside")
        self.assertEqual(
            (b"O", b""), self.checker._file_frame(self.root, relative_path)
        )
        self.assertEqual(before, self.checker.compute_revision(self.root))

    def test_c02_reports_only_relative_missing_paths(self):
        for relative_path in self.checker.REQUIRED_ACTIVE_FILES:
            if relative_path != "scripts/check_workflow.py":
                self.write(relative_path)
        check = self.checker.check_c02(self.root)
        self.assertEqual(("C02", "FAIL"), (check.id, check.status))
        self.assertIn("scripts/check_workflow.py", check.evidence)
        self.assertNotIn(str(self.root), check.evidence)
        self.assertEqual(
            self.checker.compute_revision(self.root),
            self.checker.compute_revision(self.root),
        )

    def test_c02_rejects_required_paths_through_a_symlink_ancestor(self):
        for relative_path in self.checker.REQUIRED_ACTIVE_FILES:
            self.write(relative_path)
        outside_skills = Path(self.tempdir.name) / "outside-skills"
        (self.root / "skills").rename(outside_skills)
        (self.root / "skills").symlink_to(outside_skills, target_is_directory=True)

        check = self.checker.check_c02(self.root)

        self.assertEqual(("C02", "FAIL"), (check.id, check.status))
        self.assertIn("skills/product-development-workflow/SKILL.md", check.evidence)
        self.assertNotIn(str(outside_skills), check.evidence)

    def test_renderers_preserve_order_and_four_field_json(self):
        checks = (
            self.checker.Check("C01", "PASS", "baseline manifest: 7/7 matched"),
            self.checker.Check("C02", "FAIL", "missing: scripts/check_workflow.py"),
        )
        payload = self.checker.render_json("sha256:" + "a" * 64, checks)
        self.assertEqual(["revision", "passed", "failed", "checks"], list(payload))
        self.assertEqual(["C01"], payload["passed"])
        self.assertEqual(["C02"], payload["failed"])
        self.assertEqual(["C01", "C02"], [item["id"] for item in payload["checks"]])

        text = self.checker.render_text("sha256:" + "a" * 64, checks)
        self.assertLess(text.index("C01 PASS"), text.index("C02 FAIL"))
        self.assertIn("Structural checks do not prove behavioral correctness.", text.splitlines()[-1])

    def test_error_json_has_empty_core_and_stable_error(self):
        error = self.checker.InputError("invalid-review-state", "review-state is invalid")
        payload = self.checker.render_error_json(error)
        self.assertEqual(None, payload["revision"])
        self.assertEqual([], payload["passed"])
        self.assertEqual([], payload["failed"])
        self.assertEqual([], payload["checks"])
        self.assertEqual(
            {"code": "invalid-review-state", "message": "review-state is invalid"},
            payload["error"],
        )


class WorkflowInlineConstructScannerTest(unittest.TestCase):
    def setUp(self):
        self.checker = load_checker_module()

    def test_m01_m02_emit_named_and_empty_label_links_in_order(self):
        self.assertEqual(
            (
                self.checker.InlineConstruct("link", "references/lifecycle.md"),
                self.checker.InlineConstruct("link", "references/missing.md"),
            ),
            self.checker._scan_inline_constructs(
                "[named](references/lifecycle.md)[](references/missing.md)"
            ),
        )

    def test_m03_m04_emit_every_empty_pathless_and_authority_destination(self):
        self.assertEqual(
            (
                self.checker.InlineConstruct("link", ""),
                self.checker.InlineConstruct("link", ""),
                self.checker.InlineConstruct("link", ""),
                self.checker.InlineConstruct("link", "//host"),
                self.checker.InlineConstruct("link", "//host/path"),
                self.checker.InlineConstruct("link", "?view=1"),
            ),
            self.checker._scan_inline_constructs(
                "[empty]()[](   )[](<>)"
                "[authority](//host)[](//host/path)[query](?view=1)"
            ),
        )

    def test_m05_m06_emit_unsupported_and_exempt_destinations_exactly(self):
        self.assertEqual(
            (
                self.checker.InlineConstruct("link", "ftp:references/lifecycle.md"),
                self.checker.InlineConstruct("link", "file:references/lifecycle.md"),
                self.checker.InlineConstruct("link", "madeup:references/lifecycle.md"),
                self.checker.InlineConstruct("link", "http://example.invalid/path"),
                self.checker.InlineConstruct("link", "HTTPS://example.invalid/path"),
                self.checker.InlineConstruct("link", "mailto:owner@example.invalid"),
                self.checker.InlineConstruct("link", "#"),
                self.checker.InlineConstruct("link", "#section?view=1"),
            ),
            self.checker._scan_inline_constructs(
                "[ftp](ftp:references/lifecycle.md)"
                "[](file:references/lifecycle.md)"
                "[custom](madeup:references/lifecycle.md)"
                "[http](http://example.invalid/path)"
                "[](HTTPS://example.invalid/path)"
                "[mail](mailto:owner@example.invalid)"
                "[top](#)[](#section?view=1)"
            ),
        )

    def test_m07_m08_preserve_destinations_while_consuming_complete_titles(self):
        self.assertEqual(
            (
                self.checker.InlineConstruct("link", "references/lifecycle.md"),
                self.checker.InlineConstruct("link", "references/missing.md"),
                self.checker.InlineConstruct("link", "references/right).md"),
                self.checker.InlineConstruct("link", "references/missing target.md"),
            ),
            self.checker._scan_inline_constructs(
                "[plain](references/lifecycle.md 'single')"
                '[double](references/missing.md "title ) [fake](ignored)")'
                "[angle](<references/right).md> 'single ) title')"
                '[](<references/missing target.md> "fake [inner](missing)")'
            ),
        )

    def test_leading_space_precedence_is_literal(self):
        self.assertEqual(
            (
                self.checker.InlineConstruct("link", "'title'"),
                self.checker.InlineConstruct("link", ""),
            ),
            self.checker._scan_inline_constructs("[x]( 'title')[x]( )"),
        )

    def test_trailing_horizontal_space_without_a_title_is_valid(self):
        self.assertEqual(
            (
                self.checker.InlineConstruct("link", "references/lifecycle.md"),
                self.checker.InlineConstruct("link", "references/lifecycle.md"),
                self.checker.InlineConstruct("image", "image.png"),
            ),
            self.checker._scan_inline_constructs(
                "[plain](references/lifecycle.md )"
                "[angle](<references/lifecycle.md>\t)"
                "![image](image.png )"
            ),
        )

    def test_m09_m10_images_emit_only_image_tokens_and_accept_empty_destination(self):
        self.assertEqual(
            (
                self.checker.InlineConstruct("image", ""),
                self.checker.InlineConstruct("image", "references/missing.md"),
                self.checker.InlineConstruct("image", "https://example.invalid/image.png"),
                self.checker.InlineConstruct("image", "images/fake).png"),
            ),
            self.checker._scan_inline_constructs(
                "![]()![named](references/missing.md)"
                '![remote](https://example.invalid/image.png "fake [inner](missing)")'
                "![angle](<images/fake).png> 'fake [inner](https://example.invalid)')"
            ),
        )

    def test_m11_m12_image_title_is_consumed_before_adjacent_link(self):
        self.assertEqual(
            (
                self.checker.InlineConstruct("image", "https://example.invalid/image.png"),
                self.checker.InlineConstruct("link", "references/missing.md"),
                self.checker.InlineConstruct("image", "references/ignored.md"),
                self.checker.InlineConstruct("link", "references/lifecycle.md"),
            ),
            self.checker._scan_inline_constructs(
                '![image](https://example.invalid/image.png "fake [inner](<https://example.invalid/path")'
                "[](<references/missing.md>)"
                "![next](references/ignored.md 'fake [inner](madeup:path)')"
                "[valid](references/lifecycle.md)"
            ),
        )

    def test_m13_literal_and_odd_escaped_openers_do_not_claim_later_constructs(self):
        self.assertEqual(
            (
                self.checker.InlineConstruct("image", "references/ignored.md"),
                self.checker.InlineConstruct("link", "references/lifecycle.md"),
                self.checker.InlineConstruct("link", "references/even.md"),
                self.checker.InlineConstruct("image", "references/even-image.md"),
            ),
            self.checker._scan_inline_constructs(
                "literal [ ![image](references/ignored.md)[](references/lifecycle.md)\n"
                r"\[odd](references/odd.md)\![odd](references/odd-image.md)"
                "\n"
                r"\\[even](references/even.md)\\![even](references/even-image.md)"
            ),
        )

    def test_m14_emits_every_adjacent_and_repeated_link(self):
        self.assertEqual(
            (
                self.checker.InlineConstruct("link", "references/lifecycle.md"),
                self.checker.InlineConstruct("link", "#section"),
                self.checker.InlineConstruct("link", "references/missing.md"),
            ),
            self.checker._scan_inline_constructs(
                "[](references/lifecycle.md)[two](#section)[](references/missing.md)"
            ),
        )

    def test_m15_m16_emit_invalid_tokens_and_recover_at_first_closing_parenthesis(self):
        invalid = self.checker.InlineConstruct("invalid", None)
        link = self.checker.InlineConstruct("link", "references/lifecycle.md")
        cases = (
            ("[x](p title)", (invalid,)),
            ("[x](p 'mismatch\\\")", (invalid,)),
            ("[x](<p)", (invalid,)),
            (r"[x](p\q)", (invalid,)),
            ("[x](p\x01)", (invalid,)),
            ("[bad](x title)[ok](references/lifecycle.md)", (invalid, link)),
            ("![bad](x title)[](<references/lifecycle.md>)", (invalid, link)),
            (
                '[bad](x "unterminated [maybe](references/lifecycle.md)',
                (invalid,),
            ),
        )
        for markdown, expected in cases:
            with self.subTest(markdown=repr(markdown)):
                self.assertEqual(expected, self.checker._scan_inline_constructs(markdown))

    def test_m17_scans_each_physical_line_without_cross_line_capture(self):
        self.assertEqual(
            (
                self.checker.InlineConstruct("link", "references/lifecycle.md"),
                self.checker.InlineConstruct("link", "references/missing.md"),
            ),
            self.checker._scan_inline_constructs(
                "[line](references/lifecycle.md)\n[](references/missing.md)"
            ),
        )
        self.assertEqual(
            (),
            self.checker._scan_inline_constructs("[not-cross-line]\n(references/missing.md)"),
        )


class WorkflowStructuralChecksTest(unittest.TestCase):
    STRUCTURAL_FUNCTIONS = (
        "check_c01",
        "check_c03",
        "check_c04",
        "check_c05",
        "check_c06",
        "check_c07",
        "check_c08",
        "check_c09",
        "check_c12",
    )

    def setUp(self):
        self.checker = load_checker_module()
        missing = [name for name in self.STRUCTURAL_FUNCTIONS if not hasattr(self.checker, name)]
        if missing:
            self.fail(f"structural check functions are missing: {', '.join(missing)}")
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name) / "repo"
        shutil.copytree(
            ROOT,
            self.root,
            ignore=shutil.ignore_patterns(
                ".git", ".local-handoff", "__pycache__", "*.pyc", ".DS_Store"
            ),
        )

    def mutate(self, relative_path: str, old: str, new: str) -> None:
        path = self.root / relative_path
        content = path.read_text(encoding="utf-8")
        self.assertIn(old, content)
        path.write_text(content.replace(old, new, 1), encoding="utf-8")

    def assert_check(self, check, expected_id, expected_status):
        self.assertEqual(expected_id, check.id)
        self.assertEqual(expected_status, check.status)
        self.assertNotIn(str(self.root), check.evidence)

    def fresh_c03_root(self, case_name: str) -> Path:
        case_root = Path(self.tempdir.name) / case_name
        shutil.copytree(self.root, case_root)
        return case_root

    def test_c01_detects_a_changed_baseline_byte(self):
        self.assert_check(self.checker.check_c01(self.root), "C01", "PASS")
        path = self.root / "baseline/product-development-cycle/SKILL.md"
        path.write_bytes(path.read_bytes() + b"\nmutation")
        self.assert_check(self.checker.check_c01(self.root), "C01", "FAIL")

    def test_c03_accepts_query_and_fragment_then_rejects_missing_local_target(self):
        skill = "skills/product-development-workflow/SKILL.md"
        path = self.root / skill
        with path.open("a", encoding="utf-8") as stream:
            stream.write("\n[local fixture](references/lifecycle.md?view=1#top)\n")
        self.assert_check(self.checker.check_c03(self.root), "C03", "PASS")
        self.mutate(skill, "references/lifecycle.md?view=1#top", "references/missing.md?view=1#top")
        self.assert_check(self.checker.check_c03(self.root), "C03", "FAIL")

    def test_c03_rejects_a_local_link_to_a_symlinked_leaf(self):
        skill = self.root / "skills/product-development-workflow/SKILL.md"
        with skill.open("a", encoding="utf-8") as stream:
            stream.write("\n[linked](references/linked.md)\n")
        linked = self.root / "skills/product-development-workflow/references/linked.md"
        linked.symlink_to(linked.parent / "lifecycle.md")

        self.assert_check(self.checker.check_c03(self.root.resolve()), "C03", "FAIL")

    def test_c03_rejects_a_network_path_destination(self):
        skill = self.root / "skills/product-development-workflow/SKILL.md"
        with skill.open("a", encoding="utf-8") as stream:
            stream.write("\n[http](http://example.invalid)\n")
            stream.write("[https](https://example.invalid)\n")
            stream.write("[mail](mailto:owner@example.invalid)\n")
            stream.write("[section](#fragment)\n")
        self.assert_check(self.checker.check_c03(self.root), "C03", "PASS")
        with skill.open("a", encoding="utf-8") as stream:
            stream.write("\n[external](//example.invalid)\n")

        self.assert_check(self.checker.check_c03(self.root), "C03", "FAIL")

    def test_c03_accepts_an_empty_fragment_reference(self):
        skill = self.root / "skills/product-development-workflow/SKILL.md"
        with skill.open("a", encoding="utf-8") as stream:
            stream.write("\n[top](#)\n")

        self.assert_check(self.checker.check_c03(self.root), "C03", "PASS")

    def test_c03_rejects_an_empty_destination(self):
        skill = self.root / "skills/product-development-workflow/SKILL.md"
        with skill.open("a", encoding="utf-8") as stream:
            stream.write("\n[empty]()\n")

        self.assert_check(self.checker.check_c03(self.root), "C03", "FAIL")

    def test_c03_rejects_unsupported_schemes_even_when_the_path_exists(self):
        skill = self.root / "skills/product-development-workflow/SKILL.md"
        original = skill.read_text(encoding="utf-8")
        cases = (
            "[ftp](ftp:references/lifecycle.md)",
            "[file](FiLe:references/lifecycle.md?view=1#top)",
            "[custom](madeup:references/lifecycle.md#top)",
            '[angled](<FTP:references/lifecycle.md> "title")',
        )
        for markdown in cases:
            with self.subTest(markdown):
                skill.write_text(f"{original}\n{markdown}\n", encoding="utf-8")
                self.assert_check(self.checker.check_c03(self.root), "C03", "FAIL")

    def test_c03_accepts_angle_destinations_with_titles(self):
        skill = self.root / "skills/product-development-workflow/SKILL.md"
        spaced_target = skill.parent / "references/space target.md"
        spaced_target.write_text("fixture\n", encoding="utf-8")
        original = skill.read_text(encoding="utf-8")
        cases = (
            '[local](<references/lifecycle.md> "title")',
            '[fragment](<#> "title")',
            '[spaced](<references/space target.md> "title")',
        )
        for markdown in cases:
            with self.subTest(markdown):
                skill.write_text(f"{original}\n{markdown}\n", encoding="utf-8")
                self.assert_check(self.checker.check_c03(self.root), "C03", "PASS")

    def test_c03_preserves_declared_external_and_fragment_exemptions(self):
        skill = self.root / "skills/product-development-workflow/SKILL.md"
        original = skill.read_text(encoding="utf-8")
        cases = (
            "[http](HTTP://example.invalid/path)",
            "[https](HtTpS://example.invalid/path?view=1#top)",
            "[mail](MAILTO:owner@example.invalid)",
            "[fragment](#section?view=1)",
        )
        for markdown in cases:
            with self.subTest(markdown):
                skill.write_text(f"{original}\n{markdown}\n", encoding="utf-8")
                self.assert_check(self.checker.check_c03(self.root), "C03", "PASS")

    def test_c03_accepts_plain_titled_angle_and_bounded_parent_local_paths(self):
        skill = self.root / "skills/product-development-workflow/SKILL.md"
        original = skill.read_text(encoding="utf-8")
        cases = (
            "[plain](references/lifecycle.md)",
            '[titled](references/lifecycle.md "title")',
            "[angle](<references/lifecycle.md>)",
            "[bounded](references/../references/lifecycle.md)",
        )
        for markdown in cases:
            with self.subTest(markdown):
                skill.write_text(f"{original}\n{markdown}\n", encoding="utf-8")
                self.assert_check(self.checker.check_c03(self.root), "C03", "PASS")

    def test_c03_trailing_horizontal_space_without_title_reaches_classification(self):
        cases = (
            (
                "plain",
                "[x](references/lifecycle.md )",
                "[x](references/missing.md )",
            ),
            (
                "angle-tab",
                "[x](<references/lifecycle.md>\t)",
                "[x](<references/missing.md>\t)",
            ),
            (
                "image-plus-link",
                "![x](image.png )[ok](references/lifecycle.md )",
                "![x](image.png )[bad](references/missing.md )",
            ),
        )
        for case_name, valid, invalid in cases:
            with self.subTest(case_name, state="valid"):
                valid_root = self.fresh_c03_root(f"trailing-{case_name}-valid")
                skill = valid_root / "skills/product-development-workflow/SKILL.md"
                with skill.open("a", encoding="utf-8") as stream:
                    stream.write(f"\n{valid}\n")
                self.assert_check(self.checker.check_c03(valid_root), "C03", "PASS")
            with self.subTest(case_name, state="invalid"):
                invalid_root = self.fresh_c03_root(f"trailing-{case_name}-invalid")
                skill = invalid_root / "skills/product-development-workflow/SKILL.md"
                with skill.open("a", encoding="utf-8") as stream:
                    stream.write(f"\n{invalid}\n")
                self.assert_check(self.checker.check_c03(invalid_root), "C03", "FAIL")

    def test_c03_rejects_pathless_and_non_file_local_destinations(self):
        skill = self.root / "skills/product-development-workflow/SKILL.md"
        outside = self.root / "skills/outside.md"
        outside.write_text("fixture\n", encoding="utf-8")
        original = skill.read_text(encoding="utf-8")
        cases = (
            "[angle-empty](<>)",
            "[query](?view=1)",
            "[authority](//example.invalid/references/lifecycle.md)",
            "[absolute](/references/lifecycle.md)",
            "[escape](../outside.md)",
            "[directory](references)",
        )
        for markdown in cases:
            with self.subTest(markdown):
                skill.write_text(f"{original}\n{markdown}\n", encoding="utf-8")
                self.assert_check(self.checker.check_c03(self.root), "C03", "FAIL")

    def test_c03_rejects_ancestor_and_dangling_symlink_targets(self):
        skill = self.root / "skills/product-development-workflow/SKILL.md"
        references = skill.parent / "references"
        outside = Path(self.tempdir.name) / "outside"
        outside.mkdir()
        (outside / "target.md").write_text("fixture\n", encoding="utf-8")
        (references / "linked").symlink_to(outside, target_is_directory=True)
        (references / "dangling.md").symlink_to(references / "missing.md")
        original = skill.read_text(encoding="utf-8")
        cases = (
            "[ancestor](references/linked/target.md)",
            "[dangling](references/dangling.md)",
        )
        for markdown in cases:
            with self.subTest(markdown):
                skill.write_text(f"{original}\n{markdown}\n", encoding="utf-8")
                self.assert_check(self.checker.check_c03(self.root), "C03", "FAIL")

    def test_c03_empty_labels_validate_each_destination_class(self):
        cases = (
            ("existing", "[](references/lifecycle.md)", "PASS"),
            ("missing", "[](references/missing.md)", "FAIL"),
            ("empty", "[]()", "FAIL"),
            ("whitespace", "[](   )", "FAIL"),
            ("angle-empty", "[](<>)", "FAIL"),
            ("allowed", "[](HTTP://example.invalid/path)", "PASS"),
            ("unsupported", "[](madeup:references/lifecycle.md)", "FAIL"),
            ("fragment", "[](#section)", "PASS"),
            ("query-only", "[](?view=1)", "FAIL"),
            ("authority", "[](//example.invalid/path)", "FAIL"),
            ("malformed", "[](//[)", "FAIL"),
        )
        for case_name, markdown, expected in cases:
            with self.subTest(case_name):
                case_root = self.fresh_c03_root(case_name)
                skill = case_root / "skills/product-development-workflow/SKILL.md"
                with skill.open("a", encoding="utf-8") as stream:
                    stream.write(f"\n{markdown}\n")
                self.assert_check(self.checker.check_c03(case_root), "C03", expected)

    def test_c03_does_not_cross_labels_or_treat_images_as_links(self):
        cases = (
            ("isolated-image", "![image](references/missing.md)", "PASS"),
            ("literal-bracket-image", "literal [ ![image](references/missing.md)", "PASS"),
            (
                "adjacent-image-link",
                "![image](references/missing.md)[](references/missing.md)",
                "FAIL",
            ),
        )
        for case_name, markdown, expected in cases:
            with self.subTest(case_name):
                case_root = self.fresh_c03_root(case_name)
                skill = case_root / "skills/product-development-workflow/SKILL.md"
                with skill.open("a", encoding="utf-8") as stream:
                    stream.write(f"\n{markdown}\n")
                self.assert_check(self.checker.check_c03(case_root), "C03", expected)

    def test_c03_preserves_parentheses_in_angle_destinations_and_titles(self):
        cases = (
            ("title-paren", '[local](<references/lifecycle.md> "title ) stays")'),
            ("destination-paren", '[local](<references/right).md> "title")'),
            ("plain-title-paren", '[local](references/lifecycle.md "title ) stays")'),
        )
        for case_name, markdown in cases:
            with self.subTest(case_name):
                case_root = self.fresh_c03_root(case_name)
                target = case_root / "skills/product-development-workflow/references/right).md"
                target.write_text("fixture\n", encoding="utf-8")
                skill = case_root / "skills/product-development-workflow/SKILL.md"
                with skill.open("a", encoding="utf-8") as stream:
                    stream.write(f"\n{markdown}\n")
                self.assert_check(self.checker.check_c03(case_root), "C03", "PASS")

    def test_c03_malformed_suffixes_and_control_destinations_fail_closed(self):
        cases = (
            ("plain-suffix", "[bad](references/lifecycle.md suffix)"),
            ("plain-title", '[bad](references/lifecycle.md "unterminated)'),
            ("angle-suffix", "[bad](<references/lifecycle.md> suffix)"),
            ("angle-title", '[bad](<references/lifecycle.md> "unterminated)'),
            ("allowed-control", "[bad](http://example.invalid/\x01)"),
        )
        for case_name, markdown in cases:
            with self.subTest(case_name):
                case_root = self.fresh_c03_root(case_name)
                skill = case_root / "skills/product-development-workflow/SKILL.md"
                with skill.open("a", encoding="utf-8") as stream:
                    stream.write(f"\n{markdown}\n")
                self.assert_check(self.checker.check_c03(case_root), "C03", "FAIL")

    def test_c03_empty_label_wrappers_reach_local_classification(self):
        cases = (
            (
                "plain-double-title",
                '[](references/lifecycle.md "title")',
                '[](references/missing.md "title")',
            ),
            (
                "plain-single-title",
                "[](references/lifecycle.md 'title')",
                "[](references/missing.md 'title')",
            ),
            ("angle", "[](<references/lifecycle.md>)", "[](<references/missing.md>)"),
            (
                "angle-double-title",
                '[](<references/lifecycle.md> "title ) stays")',
                '[](<references/missing.md> "title ) stays")',
            ),
            (
                "angle-single-title",
                "[](<references/lifecycle.md> 'title')",
                "[](<references/missing.md> 'title')",
            ),
        )
        for case_name, valid, missing in cases:
            with self.subTest(case_name, state="valid"):
                valid_root = self.fresh_c03_root(f"{case_name}-valid")
                skill = valid_root / "skills/product-development-workflow/SKILL.md"
                with skill.open("a", encoding="utf-8") as stream:
                    stream.write(f"\n{valid}\n")
                self.assert_check(self.checker.check_c03(valid_root), "C03", "PASS")
            with self.subTest(case_name, state="missing"):
                missing_root = self.fresh_c03_root(f"{case_name}-missing")
                skill = missing_root / "skills/product-development-workflow/SKILL.md"
                with skill.open("a", encoding="utf-8") as stream:
                    stream.write(f"\n{missing}\n")
                self.assert_check(self.checker.check_c03(missing_root), "C03", "FAIL")

    def test_c03_empty_label_spaced_angle_target_reaches_classification(self):
        valid_root = self.fresh_c03_root("spaced-valid")
        target = valid_root / "skills/product-development-workflow/references/space target.md"
        target.write_text("fixture\n", encoding="utf-8")
        skill = valid_root / "skills/product-development-workflow/SKILL.md"
        with skill.open("a", encoding="utf-8") as stream:
            stream.write('\n[](<references/space target.md> "title")\n')
        self.assert_check(self.checker.check_c03(valid_root), "C03", "PASS")

        missing_root = self.fresh_c03_root("spaced-missing")
        skill = missing_root / "skills/product-development-workflow/SKILL.md"
        with skill.open("a", encoding="utf-8") as stream:
            stream.write('\n[](<references/missing target.md> "title")\n')
        self.assert_check(self.checker.check_c03(missing_root), "C03", "FAIL")

    def test_c03_adjacent_and_repeated_links_each_reach_classification(self):
        valid_root = self.fresh_c03_root("adjacent-valid")
        skill = valid_root / "skills/product-development-workflow/SKILL.md"
        with skill.open("a", encoding="utf-8") as stream:
            stream.write(
                "\n[](references/lifecycle.md)[named](references/lifecycle.md)"
                '[](references/lifecycle.md "title")\n'
            )
        self.assert_check(self.checker.check_c03(valid_root), "C03", "PASS")

        missing_root = self.fresh_c03_root("adjacent-missing")
        skill = missing_root / "skills/product-development-workflow/SKILL.md"
        with skill.open("a", encoding="utf-8") as stream:
            stream.write(
                "\n[](references/lifecycle.md)[named](references/lifecycle.md)"
                "[](references/missing.md)\n"
            )
        self.assert_check(self.checker.check_c03(missing_root), "C03", "FAIL")

    def test_c03_title_text_is_not_scanned_as_an_adjacent_link(self):
        cases = (
            (
                "named-double-title",
                '[outer](references/lifecycle.md "fake [inner](references/missing.md)")',
                "PASS",
            ),
            (
                "empty-single-title",
                "[](references/lifecycle.md 'fake [inner](references/missing.md)')",
                "PASS",
            ),
            (
                "real-adjacent-missing",
                '[outer](references/lifecycle.md "fake [inner](references/missing.md)")'
                "[](references/missing.md)",
                "FAIL",
            ),
        )
        for case_name, markdown, expected in cases:
            with self.subTest(case_name):
                case_root = self.fresh_c03_root(case_name)
                skill = case_root / "skills/product-development-workflow/SKILL.md"
                with skill.open("a", encoding="utf-8") as stream:
                    stream.write(f"\n{markdown}\n")
                self.assert_check(self.checker.check_c03(case_root), "C03", expected)

    def test_c03_complete_images_cannot_hide_adjacent_link_destinations(self):
        cases = (
            (
                "image-only",
                '![image](references/missing.md "fake [inner](missing)")',
                "PASS",
            ),
            (
                "image-adjacent-existing",
                '![image](https://example.invalid/image.png "fake [inner](<https://example.invalid/path")'
                "[](<references/lifecycle.md>)",
                "PASS",
            ),
            (
                "image-adjacent-missing",
                '![image](https://example.invalid/image.png "fake [inner](<https://example.invalid/path")'
                "[](<references/missing.md>)",
                "FAIL",
            ),
            (
                "image-adjacent-unsupported",
                "![image](references/ignored.md 'fake [inner](https://example.invalid/path)')"
                "[](madeup:references/lifecycle.md)",
                "FAIL",
            ),
        )
        for case_name, markdown, expected in cases:
            with self.subTest(case_name):
                case_root = self.fresh_c03_root(case_name)
                skill = case_root / "skills/product-development-workflow/SKILL.md"
                with skill.open("a", encoding="utf-8") as stream:
                    stream.write(f"\n{markdown}\n")
                self.assert_check(self.checker.check_c03(case_root), "C03", expected)

    def test_c03_escape_parity_literal_precedence_and_line_boundaries(self):
        cases = (
            ("odd-link", r"\[x](references/missing.md)", "PASS"),
            ("odd-image", r"\![x](references/missing.md)", "PASS"),
            ("even-link", r"\\[x](references/missing.md)", "FAIL"),
            (
                "literal-before-independent",
                "literal [ ![image](references/missing.md)[](references/lifecycle.md)",
                "PASS",
            ),
            (
                "separate-lines",
                "[not-cross-line]\n(references/missing.md)",
                "PASS",
            ),
            (
                "next-line-missing",
                "[valid](references/lifecycle.md)\n[](references/missing.md)",
                "FAIL",
            ),
        )
        for case_name, markdown, expected in cases:
            with self.subTest(case_name):
                case_root = self.fresh_c03_root(case_name)
                skill = case_root / "skills/product-development-workflow/SKILL.md"
                with skill.open("a", encoding="utf-8") as stream:
                    stream.write(f"\n{markdown}\n")
                self.assert_check(self.checker.check_c03(case_root), "C03", expected)

    def test_c03_malformed_constructs_fail_and_recover_without_hiding_adjacent_links(self):
        cases = (
            ("plain-suffix", "[x](p title)"),
            ("mismatched-title", "[x](p 'mismatch\\\")"),
            ("unterminated-angle", "[x](<p)"),
            ("backslash", r"[x](p\q)"),
            ("control", "[x](p\x01)"),
            ("recover-link", "[bad](x title)[ok](references/lifecycle.md)"),
            ("recover-image", "![bad](x title)[](<references/lifecycle.md>)"),
            (
                "ambiguous-eol",
                '[bad](x "unterminated [maybe](references/lifecycle.md)',
            ),
        )
        for case_name, markdown in cases:
            with self.subTest(case_name):
                case_root = self.fresh_c03_root(case_name)
                skill = case_root / "skills/product-development-workflow/SKILL.md"
                with skill.open("a", encoding="utf-8") as stream:
                    stream.write(f"\n{markdown}\n")
                self.assert_check(self.checker.check_c03(case_root), "C03", "FAIL")

    def test_c04_detects_wrong_display_name(self):
        self.assert_check(self.checker.check_c04(self.root), "C04", "PASS")
        self.mutate(
            "skills/product-development-workflow/agents/openai.yaml",
            'display_name: "Product Development Workflow"',
            'display_name: "Wrong Workflow"',
        )
        self.assert_check(self.checker.check_c04(self.root), "C04", "FAIL")

    def test_c04_rejects_empty_quoted_description_scalars(self):
        cases = (
            (
                "skills/product-development-workflow/SKILL.md",
                "description: Guide a digital product through evidence-based discovery, staged implementation, verification, release, and learning in Codex. Use when starting, resuming, auditing, or preparing a product, module, or release while preserving existing evidence and selecting the next incomplete gate.",
                'description: ""',
            ),
            (
                "skills/product-development-workflow/agents/openai.yaml",
                'short_description: "Guide staged product work through evidence-based gates"',
                'short_description: ""',
            ),
        )
        for relative_path, old, new in cases:
            with self.subTest(relative_path=relative_path):
                path = self.root / relative_path
                original = path.read_text(encoding="utf-8")
                self.assertIn(old, original)
                path.write_text(original.replace(old, new, 1), encoding="utf-8")
                self.assert_check(self.checker.check_c04(self.root), "C04", "FAIL")
                path.write_text(original, encoding="utf-8")

    def test_c05_detects_changed_gate_order(self):
        self.assert_check(self.checker.check_c05(self.root), "C05", "PASS")
        self.mutate(
            "skills/product-development-workflow/references/lifecycle.md",
            "## 8. Finance",
            "## 9. Finance",
        )
        self.assert_check(self.checker.check_c05(self.root), "C05", "FAIL")

    def test_c06_requires_one_light_gate_3_5_and_no_active_4_5(self):
        self.assert_check(self.checker.check_c06(self.root), "C06", "PASS")
        self.mutate(
            "skills/product-development-workflow/SKILL.md",
            "light Gate 3.5",
            "Gate 3.5",
        )
        self.assert_check(self.checker.check_c06(self.root), "C06", "FAIL")

    def test_c07_requires_each_maturity_label(self):
        self.assert_check(self.checker.check_c07(self.root), "C07", "PASS")
        cases = (
            ("references/lifecycle.md", "### working-prototype"),
            ("references/lifecycle.md", "### mvp"),
            ("references/lifecycle.md", "### scale-1"),
            ("references/lifecycle.md", "### scale-2"),
            ("references/lifecycle.md", "### mature"),
            ("SKILL.md", "- working prototype"),
            ("SKILL.md", "- MVP"),
            ("SKILL.md", "- scale 1"),
            ("SKILL.md", "- scale 2"),
            ("SKILL.md", "- mature operation"),
        )
        for relative_path, label in cases:
            with self.subTest(label=label):
                fresh = Path(self.tempdir.name) / "mutated-c07"
                if fresh.exists():
                    shutil.rmtree(fresh)
                shutil.copytree(self.root, fresh)
                path = fresh / "skills/product-development-workflow" / relative_path
                path.write_text(path.read_text(encoding="utf-8").replace(label, "removed", 1), encoding="utf-8")
                self.assert_check(self.checker.check_c07(fresh), "C07", "FAIL")

    def test_c08_requires_profile_sections_and_decision_fields(self):
        self.assert_check(self.checker.check_c08(self.root), "C08", "PASS")
        labels = (
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
            "Transition evidence required",
            "Data preservation or lifecycle rule",
            "Peak concurrent work or peak operation rate",
            "Requested model/reasoning",
            "Accepted native assignment",
            "Independently verified runtime fact",
            "Actual dependencies",
            "Unknown",
        )
        source = self.root / "skills/product-development-workflow/assets/project-profile.template.md"
        original = source.read_text(encoding="utf-8")
        for label in labels:
            with self.subTest(label=label):
                count = -1 if label == "Unknown" else 1
                source.write_text(original.replace(label, "removed", count), encoding="utf-8")
                self.assert_check(self.checker.check_c08(self.root), "C08", "FAIL")
        source.write_text(original, encoding="utf-8")

    def test_c08_rejects_a_required_field_relocated_to_the_wrong_section(self):
        source = self.root / "skills/product-development-workflow/assets/project-profile.template.md"
        original = source.read_text(encoding="utf-8")
        field_line = "- Transition evidence required: Unknown\n"
        self.assertIn(field_line, original)
        relocated = original.replace(field_line, "", 1).replace(
            "## Product\n",
            "## Product\n\n" + field_line,
            1,
        )
        source.write_text(relocated, encoding="utf-8")
        self.assertIn("Transition evidence required", relocated)
        self.assert_check(self.checker.check_c08(self.root), "C08", "FAIL")

    def test_c08_rejects_a_required_heading_with_a_suffix(self):
        source = self.root / "skills/product-development-workflow/assets/project-profile.template.md"
        original = source.read_text(encoding="utf-8")
        self.assertIn("## Architecture\n", original)
        source.write_text(
            original.replace("## Architecture\n", "## Architecture notes\n", 1),
            encoding="utf-8",
        )
        self.assert_check(self.checker.check_c08(self.root), "C08", "FAIL")

    def test_c09_requires_every_section_local_handoff_and_review_label(self):
        self.assert_check(self.checker.check_c09(self.root), "C09", "PASS")
        source = self.root / "skills/product-development-workflow/assets/work-item-and-review-templates.md"
        original = source.read_text(encoding="utf-8")
        cases = (
            ("Work package / handoff", self.checker.WORK_PACKAGE_LABELS),
            ("Review record", self.checker.REVIEW_RECORD_LABELS),
        )
        for heading, labels in cases:
            start = original.index(f"## {heading}")
            end = original.find("\n## ", start + 3)
            end = len(original) if end < 0 else end
            section = original[start:end]
            for label in labels:
                with self.subTest(section=heading, label=label):
                    mutated_section = section.replace(f"- {label}:", "- Removed:", 1)
                    self.assertNotEqual(section, mutated_section)
                    source.write_text(
                        original[:start] + mutated_section + original[end:],
                        encoding="utf-8",
                    )
                    self.assert_check(self.checker.check_c09(self.root), "C09", "FAIL")
        source.write_text(original, encoding="utf-8")

    def test_c12_rejects_operational_marker_but_allows_template_values(self):
        self.assert_check(self.checker.check_c12(self.root), "C12", "PASS")
        asset = self.root / "skills/product-development-workflow/assets/AGENTS.template.md"
        with asset.open("a", encoding="utf-8") as stream:
            stream.write("\nTODO: template value is intentionally outside the operational scan\n")
        self.assert_check(self.checker.check_c12(self.root), "C12", "PASS")
        path = self.root / "skills/product-development-workflow/references/lifecycle.md"
        with path.open("a", encoding="utf-8") as stream:
            stream.write("\nTODO: finish workflow\n")
        self.assert_check(self.checker.check_c12(self.root), "C12", "FAIL")


class WorkflowReviewIdentityTest(unittest.TestCase):
    def setUp(self):
        self.checker = load_checker_module()
        missing = [name for name in ("parse_review_state", "check_c10") if not hasattr(self.checker, name)]
        if missing:
            self.fail(f"review identity functions are missing: {', '.join(missing)}")
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name) / "repo"
        self.root.mkdir()

    def write_state(self, name: str, state: dict[str, object]) -> Path:
        path = self.root / name
        path.write_text(json.dumps(state), encoding="utf-8")
        return path

    def phase_state(self, phase: str, *, stale: bool = False) -> dict[str, object]:
        if phase == "PLAN":
            reviewed = {"plan_hash": "a" * 64, "base_sha": "1" * 40}
            current = dict(reviewed)
            if stale:
                current["plan_hash"] = "b" * 64
            return {"phase": phase, "verdict": "PLAN_PASS", "reviewed": reviewed, "current": current}
        if phase == "CHANGE_REVIEW":
            reviewed = {"base_sha": "1" * 40, "head_sha": "2" * 40}
            current = dict(reviewed)
            if stale:
                current["head_sha"] = "3" * 40
            return {"phase": phase, "verdict": "PASS", "reviewed": reviewed, "current": current}
        reviewed = {"main_sha": "1" * 40}
        current = {"main_sha": "2" * 40} if stale else dict(reviewed)
        return {"phase": "FINAL", "verdict": "FINAL_PASS", "reviewed": reviewed, "current": current}

    def test_c10_accepts_equal_and_rejects_stale_identity_for_each_phase(self):
        for phase in ("PLAN", "CHANGE_REVIEW", "FINAL"):
            with self.subTest(phase=phase, case="equal"):
                path = self.write_state(f"{phase.lower()}-equal.json", self.phase_state(phase))
                state = self.checker.parse_review_state(self.root, path.relative_to(self.root))
                check = self.checker.check_c10(state, path.relative_to(self.root).as_posix())
                self.assertEqual(("C10", "PASS"), (check.id, check.status))
                self.assertIn("provided input; not live owning-system evidence", check.evidence)
                self.assertNotIn("1" * 40, check.evidence)
            with self.subTest(phase=phase, case="stale"):
                path = self.write_state(f"{phase.lower()}-stale.json", self.phase_state(phase, stale=True))
                state = self.checker.parse_review_state(self.root, path.relative_to(self.root))
                check = self.checker.check_c10(state, path.relative_to(self.root).as_posix())
                self.assertEqual(("C10", "FAIL"), (check.id, check.status))
                self.assertNotIn("2" * 40, check.evidence)

    def test_parse_review_state_rejects_incomplete_and_extra_keys_stably(self):
        invalid_states = (
            {"phase": "FINAL", "verdict": "FINAL_PASS", "reviewed": {}, "current": {}},
            {
                "phase": "FINAL",
                "verdict": "FINAL_PASS",
                "reviewed": {"main_sha": "1" * 40},
                "current": {"main_sha": "1" * 40},
                "extra": True,
            },
            {
                "phase": "FINAL",
                "verdict": "PASS",
                "reviewed": {"main_sha": "1" * 40},
                "current": {"main_sha": "1" * 40},
            },
            {
                "phase": "FINAL",
                "verdict": "FINAL_PASS",
                "reviewed": {"main_sha": "A" * 40},
                "current": {"main_sha": "A" * 40},
            },
        )
        for index, state in enumerate(invalid_states):
            with self.subTest(index=index):
                path = self.write_state(f"invalid-{index}.json", state)
                with self.assertRaises(self.checker.InputError) as caught:
                    self.checker.parse_review_state(self.root, path.relative_to(self.root))
                self.assertEqual("invalid-review-state", caught.exception.code)
                self.assertEqual("review-state does not match the required phase schema", str(caught.exception))

    def test_parse_review_state_rejects_malformed_json_without_echoing_content(self):
        path = self.root / "malformed.json"
        path.write_text('{"phase":', encoding="utf-8")
        with self.assertRaises(self.checker.InputError) as caught:
            self.checker.parse_review_state(self.root, path.relative_to(self.root))
        self.assertEqual("invalid-review-state", caught.exception.code)
        self.assertEqual("review-state is not valid JSON", str(caught.exception))


class WorkflowPrivateBindingTest(unittest.TestCase):
    def setUp(self):
        self.checker = load_checker_module()
        if not hasattr(self.checker, "check_c11"):
            self.fail("private binding function is missing: check_c11")
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name) / "repo"
        shutil.copytree(
            ROOT,
            self.root,
            ignore=shutil.ignore_patterns(
                ".git", ".local-handoff", "__pycache__", "*.pyc", ".DS_Store"
            ),
        )
        self.leak_lines = (FIXTURES / "invalid/leaked-binding.txt").read_text(encoding="utf-8").splitlines()

    def test_c11_detects_each_named_rule_without_echoing_the_binding(self):
        expected_rules = (
            "user-path",
            "recipes-binding",
            "runtime-uuid",
            "credential-prefix",
            "client-id-marker",
        )
        active_path = self.root / "skills/product-development-workflow/SKILL.md"
        original = active_path.read_text(encoding="utf-8")
        for rule, leak in zip(expected_rules, self.leak_lines, strict=True):
            with self.subTest(rule=rule):
                active_path.write_text(original + "\n" + leak + "\n", encoding="utf-8")
                check = self.checker.check_c11(self.root)
                self.assertEqual(("C11", "FAIL"), (check.id, check.status))
                self.assertIn(rule, check.evidence)
                self.assertIn("skills/product-development-workflow/SKILL.md", check.evidence)
                self.assertNotIn(leak, check.evidence)
        active_path.write_text(original, encoding="utf-8")

    def test_c11_scans_only_the_public_allowlist(self):
        check = self.checker.check_c11(self.root)
        self.assertEqual(("C11", "PASS"), (check.id, check.status))
        self.assertNotIn(str(self.root), check.evidence)

        ignored_paths = (
            "tests/ignored-leak.md",
            "baseline/product-development-cycle/ignored-leak.md",
            "SPEC.md",
            "AUDIT.md",
            "EVALUATION.md",
            "HANDOFF.md",
            "SOURCES.md",
            "VERIFICATION.md",
            "docs/superpowers/plans/ignored-leak.md",
        )
        for relative_path in ignored_paths:
            ignored = self.root / relative_path
            ignored.parent.mkdir(parents=True, exist_ok=True)
            ignored.write_text("\n".join(self.leak_lines), encoding="utf-8")
        check = self.checker.check_c11(self.root)
        self.assertEqual(("C11", "PASS"), (check.id, check.status))

    def test_c11_aggregates_rules_and_paths_without_secret_content(self):
        active_path = self.root / "skills/product-development-workflow/references/lifecycle.md"
        with active_path.open("a", encoding="utf-8") as stream:
            stream.write("\n" + "\n".join(self.leak_lines) + "\n")
        check = self.checker.check_c11(self.root)
        self.assertEqual(("C11", "FAIL"), (check.id, check.status))
        for rule in (
            "user-path",
            "recipes-binding",
            "runtime-uuid",
            "credential-prefix",
            "client-id-marker",
        ):
            self.assertIn(rule, check.evidence)
        for leak in self.leak_lines:
            self.assertNotIn(leak, check.evidence)
        self.assertNotIn(str(self.root), check.evidence)

    def test_c11_does_not_traverse_a_symlinked_active_ancestor(self):
        outside_skills = Path(self.tempdir.name) / "outside-skills"
        (self.root / "skills").rename(outside_skills)
        leak = outside_skills / "product-development-workflow/references/leak.md"
        leak.write_text("\n".join(self.leak_lines), encoding="utf-8")
        (self.root / "skills").symlink_to(outside_skills, target_is_directory=True)

        check = self.checker.check_c11(self.root)

        self.assertEqual(("C11", "PASS"), (check.id, check.status))
        self.assertNotIn(str(outside_skills), check.evidence)


class WorkflowCheckerCliTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name) / "repo"
        shutil.copytree(
            ROOT,
            self.root,
            ignore=shutil.ignore_patterns(
                ".git", ".local-handoff", "__pycache__", "*.pyc", ".DS_Store"
            ),
        )
        self.valid_state = "tests/fixtures/review-state/valid-final.json"

    def fresh_c03_root(self, case_name: str) -> Path:
        case_root = Path(self.tempdir.name) / case_name
        shutil.copytree(self.root, case_root)
        return case_root

    def assert_c03_cli_failure(self, case_root: Path, markdown: str):
        active = case_root / "skills/product-development-workflow/SKILL.md"
        with active.open("a", encoding="utf-8") as stream:
            stream.write(f"\n{markdown}\n")

        result = run_checker(case_root, self.valid_state)

        self.assertEqual(1, result.returncode, result.stderr or result.stdout)
        self.assertEqual("", result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(
            [f"C{number:02d}" for number in range(1, 13)],
            [check["id"] for check in payload["checks"]],
        )
        self.assertEqual(["C03"], payload["failed"])
        c03 = next(check for check in payload["checks"] if check["id"] == "C03")
        self.assertIn("skills/product-development-workflow/SKILL.md", c03["evidence"])
        self.assertNotIn(str(case_root), result.stdout)
        self.assertNotIn(markdown, result.stdout)
        self.assertTrue(
            payload["checks"][-1]["evidence"].endswith(
                "Structural checks do not prove behavioral correctness."
            )
        )
        return result

    def test_json_success_has_exact_core_shape_order_and_limitation(self):
        result = run_checker(self.root, self.valid_state)
        self.assertEqual(0, result.returncode, result.stderr or result.stdout)
        self.assertEqual("", result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(["revision", "passed", "failed", "checks"], list(payload))
        self.assertRegex(payload["revision"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual([f"C{number:02d}" for number in range(1, 13)], payload["passed"])
        self.assertEqual([], payload["failed"])
        self.assertEqual([f"C{number:02d}" for number in range(1, 13)], [item["id"] for item in payload["checks"]])
        self.assertEqual({"id", "status", "evidence"}, set(payload["checks"][0]))
        self.assertTrue(payload["checks"][-1]["evidence"].endswith("Structural checks do not prove behavioral correctness."))

    def test_text_success_is_ordered_and_ends_with_limitation(self):
        result = run_checker(self.root, self.valid_state, json_output=False)
        self.assertEqual(0, result.returncode, result.stderr or result.stdout)
        lines = result.stdout.splitlines()
        self.assertEqual([f"C{number:02d}" for number in range(1, 13)], [line.split()[0] for line in lines[:12]])
        self.assertEqual("passed: 12", lines[12])
        self.assertEqual("failed: 0", lines[13])
        self.assertRegex(lines[14], r"^revision: sha256:[0-9a-f]{64}$")
        self.assertEqual("Structural checks do not prove behavioral correctness.", lines[15])

    def test_output_and_revision_are_deterministic(self):
        first = run_checker(self.root, self.valid_state)
        second = run_checker(self.root, self.valid_state)
        self.assertEqual(0, first.returncode)
        self.assertEqual(12, len(json.loads(first.stdout)["checks"]))
        self.assertEqual((0, first.stdout), (second.returncode, second.stdout))

    def test_stale_final_fails_only_c10_and_does_not_change_revision(self):
        valid = run_checker(self.root, self.valid_state)
        stale = run_checker(self.root, "tests/fixtures/invalid/stale-final.json")
        self.assertEqual(1, stale.returncode, stale.stderr or stale.stdout)
        valid_payload = json.loads(valid.stdout)
        stale_payload = json.loads(stale.stdout)
        self.assertEqual(valid_payload["revision"], stale_payload["revision"])
        self.assertEqual(["C10"], stale_payload["failed"])
        self.assertNotIn("2" * 40, stale.stdout)

    def test_injected_active_binding_fails_only_c11_and_is_redacted(self):
        leak_lines = (self.root / "tests/fixtures/invalid/leaked-binding.txt").read_text(encoding="utf-8").splitlines()
        active = self.root / "skills/product-development-workflow/references/lifecycle.md"
        with active.open("a", encoding="utf-8") as stream:
            stream.write("\n" + "\n".join(leak_lines) + "\n")
        result = run_checker(self.root, self.valid_state)
        self.assertEqual(1, result.returncode, result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(["C11"], payload["failed"])
        for leak in leak_lines:
            self.assertNotIn(leak, result.stdout)

    def test_malformed_inline_destination_returns_a_complete_c03_failure(self):
        active = self.root / "skills/product-development-workflow/SKILL.md"
        with active.open("a", encoding="utf-8") as stream:
            stream.write("\n[broken](//[)\n")

        result = run_checker(self.root, self.valid_state)

        self.assertEqual(1, result.returncode, result.stderr or result.stdout)
        self.assertEqual("", result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(12, len(payload["checks"]))
        self.assertEqual(
            [f"C{number:02d}" for number in range(1, 13)],
            [check["id"] for check in payload["checks"]],
        )
        self.assertIn("C03", payload["failed"])
        c03 = next(check for check in payload["checks"] if check["id"] == "C03")
        self.assertIn("skills/product-development-workflow/SKILL.md", c03["evidence"])
        self.assertNotIn(str(self.root), result.stdout)

    def test_network_path_destination_returns_a_complete_c03_json_failure(self):
        active = self.root / "skills/product-development-workflow/SKILL.md"
        with active.open("a", encoding="utf-8") as stream:
            stream.write("\n[external](//example.invalid)\n")

        result = run_checker(self.root, self.valid_state)

        self.assertEqual(1, result.returncode, result.stderr or result.stdout)
        self.assertEqual("", result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(12, len(payload["checks"]))
        self.assertEqual(["C03"], payload["failed"])
        c03 = next(check for check in payload["checks"] if check["id"] == "C03")
        self.assertIn("skills/product-development-workflow/SKILL.md", c03["evidence"])
        self.assertTrue(
            payload["checks"][-1]["evidence"].endswith(
                "Structural checks do not prove behavioral correctness."
            )
        )

    def test_empty_destinations_return_complete_c03_json_failures(self):
        cases = (
            ("literal-empty", "[empty]()"),
            ("whitespace-only", "[space](   )"),
        )
        for case_name, markdown in cases:
            with self.subTest(case_name):
                case_root = Path(self.tempdir.name) / case_name
                shutil.copytree(self.root, case_root)
                active = case_root / "skills/product-development-workflow/SKILL.md"
                with active.open("a", encoding="utf-8") as stream:
                    stream.write(f"\n{markdown}\n")

                result = run_checker(case_root, self.valid_state)

                self.assertEqual(1, result.returncode, result.stderr or result.stdout)
                self.assertEqual("", result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual(12, len(payload["checks"]))
                self.assertEqual(["C03"], payload["failed"])
                c03 = next(check for check in payload["checks"] if check["id"] == "C03")
                self.assertIn("skills/product-development-workflow/SKILL.md", c03["evidence"])
                self.assertNotIn(str(case_root), result.stdout)
                self.assertTrue(
                    payload["checks"][-1]["evidence"].endswith(
                        "Structural checks do not prove behavioral correctness."
                    )
                )

    def test_unsupported_scheme_returns_a_complete_c03_json_failure(self):
        active = self.root / "skills/product-development-workflow/SKILL.md"
        with active.open("a", encoding="utf-8") as stream:
            stream.write("\n[external](madeup:references/lifecycle.md?view=1#top)\n")

        result = run_checker(self.root, self.valid_state)

        self.assertEqual(1, result.returncode, result.stderr or result.stdout)
        self.assertEqual("", result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(12, len(payload["checks"]))
        self.assertEqual(
            [f"C{number:02d}" for number in range(1, 13)],
            [check["id"] for check in payload["checks"]],
        )
        self.assertEqual(["C03"], payload["failed"])
        c03 = next(check for check in payload["checks"] if check["id"] == "C03")
        self.assertIn("skills/product-development-workflow/SKILL.md", c03["evidence"])
        self.assertNotIn(str(self.root), result.stdout)
        self.assertTrue(
            payload["checks"][-1]["evidence"].endswith(
                "Structural checks do not prove behavioral correctness."
            )
        )

    def test_empty_label_failures_return_complete_c03_json(self):
        cases = (
            ("missing", "[](references/missing.md)"),
            ("empty", "[]()"),
            ("unsupported", "[](madeup:references/lifecycle.md)"),
            ("authority", "[](//example.invalid/path)"),
            ("malformed", "[](//[)"),
        )
        for case_name, markdown in cases:
            with self.subTest(case_name):
                case_root = self.fresh_c03_root(case_name)
                active = case_root / "skills/product-development-workflow/SKILL.md"
                with active.open("a", encoding="utf-8") as stream:
                    stream.write(f"\n{markdown}\n")

                result = run_checker(case_root, self.valid_state)

                self.assertEqual(1, result.returncode, result.stderr or result.stdout)
                self.assertEqual("", result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual(12, len(payload["checks"]))
                self.assertEqual(
                    [f"C{number:02d}" for number in range(1, 13)],
                    [check["id"] for check in payload["checks"]],
                )
                self.assertEqual(["C03"], payload["failed"])
                c03 = next(check for check in payload["checks"] if check["id"] == "C03")
                self.assertIn("skills/product-development-workflow/SKILL.md", c03["evidence"])
                self.assertNotIn(str(case_root), result.stdout)
                self.assertTrue(
                    payload["checks"][-1]["evidence"].endswith(
                        "Structural checks do not prove behavioral correctness."
                    )
                )

    def test_bounded_scanner_cli_regressions_are_complete_and_redacted(self):
        cases = (
            ("empty-label-missing", "[](references/missing.md)"),
            (
                "image-title-adjacent-missing",
                '![image](https://example.invalid/image.png "fake [inner](<https://example.invalid/path")'
                "[](<references/missing.md>)",
            ),
            (
                "image-title-adjacent-unsupported",
                '![image](references/ignored.md "fake [inner](https://example.invalid/path)")'
                "[](madeup:references/lifecycle.md)",
            ),
            (
                "malformed-image-adjacent-valid",
                "![bad](x title)[](<references/lifecycle.md>)",
            ),
        )
        for case_name, markdown in cases:
            with self.subTest(case_name):
                case_root = self.fresh_c03_root(f"cli-{case_name}")
                self.assert_c03_cli_failure(case_root, markdown)

    def test_adversarial_c03_cli_failure_is_byte_deterministic(self):
        case_root = self.fresh_c03_root("cli-deterministic-image-title")
        markdown = (
            '![image](https://example.invalid/image.png "fake [inner](<https://example.invalid/path")'
            "[](<references/missing.md>)"
        )
        first = self.assert_c03_cli_failure(case_root, markdown)
        second = run_checker(case_root, self.valid_state)
        self.assertEqual((1, first.stdout, ""), (second.returncode, second.stdout, second.stderr))

    def test_valid_image_and_adjacent_empty_label_angle_title_link_pass_cli(self):
        active = self.root / "skills/product-development-workflow/SKILL.md"
        with active.open("a", encoding="utf-8") as stream:
            stream.write(
                "\n![image](references/ignored.md 'fake [inner](missing)')"
                '[](<references/lifecycle.md> "title ) [fake](missing)")\n'
            )

        result = run_checker(self.root, self.valid_state)

        self.assertEqual(0, result.returncode, result.stderr or result.stdout)
        self.assertEqual("", result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual([f"C{number:02d}" for number in range(1, 13)], payload["passed"])
        self.assertEqual([], payload["failed"])
        self.assertEqual(
            [f"C{number:02d}" for number in range(1, 13)],
            [check["id"] for check in payload["checks"]],
        )
        self.assertTrue(
            payload["checks"][-1]["evidence"].endswith(
                "Structural checks do not prove behavioral correctness."
            )
        )

    def test_c12_failure_json_still_ends_with_the_mandatory_limitation(self):
        active = self.root / "skills/product-development-workflow/references/lifecycle.md"
        with active.open("a", encoding="utf-8") as stream:
            stream.write("\nTODO: synthetic operational marker\n")
        result = run_checker(self.root, self.valid_state)
        self.assertEqual(1, result.returncode, result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(["C12"], payload["failed"])
        c12 = next(check for check in payload["checks"] if check["id"] == "C12")
        self.assertTrue(
            c12["evidence"].endswith(
                "Structural checks do not prove behavioral correctness."
            )
        )

    def test_c12_unreadable_input_still_ends_with_the_mandatory_limitation(self):
        (self.root / "README.md").write_bytes(b"\xff")

        result = run_checker(self.root, self.valid_state)

        self.assertEqual(1, result.returncode, result.stderr or result.stdout)
        self.assertEqual("", result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(12, len(payload["checks"]))
        c12 = next(check for check in payload["checks"] if check["id"] == "C12")
        self.assertEqual("FAIL", c12["status"])
        self.assertTrue(
            c12["evidence"].endswith(
                "Structural checks do not prove behavioral correctness."
            )
        )
        self.assertNotIn(str(self.root), result.stdout)

    def test_incomplete_review_state_is_post_parse_exit_two_with_empty_core(self):
        result = run_checker(self.root, "tests/fixtures/invalid/incomplete-review-state.json")
        self.assertEqual(2, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual(None, payload["revision"])
        self.assertEqual([], payload["passed"])
        self.assertEqual([], payload["failed"])
        self.assertEqual([], payload["checks"])
        self.assertEqual("invalid-review-state", payload["error"]["code"])

    def test_missing_required_argument_uses_argparse_exit_two(self):
        result = run_checker(self.root, None)
        self.assertEqual(2, result.returncode)
        self.assertEqual("", result.stdout)
        self.assertIn("--review-state", result.stderr)

    def test_invalid_root_is_post_parse_exit_two(self):
        result = run_checker(self.root / "missing", self.valid_state)
        self.assertEqual(2, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual("invalid-root", payload["error"]["code"])
        self.assertEqual([], payload["checks"])

    def test_missing_directly_read_active_file_returns_twelve_structured_checks(self):
        missing = self.root / "skills/product-development-workflow/SKILL.md"
        missing.unlink()
        result = run_checker(self.root, self.valid_state)
        self.assertEqual(1, result.returncode, result.stderr or result.stdout)
        self.assertEqual("", result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(12, len(payload["checks"]))
        self.assertEqual(
            [f"C{number:02d}" for number in range(1, 13)],
            [check["id"] for check in payload["checks"]],
        )
        self.assertIn("C02", payload["failed"])
        self.assertNotIn(str(self.root), result.stdout)


if __name__ == "__main__":
    unittest.main()
