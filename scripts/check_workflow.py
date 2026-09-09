#!/usr/bin/env python3
"""Deterministic structural checks for the Product Development Workflow package."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from functools import wraps
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
from typing import Literal, Sequence
from urllib.parse import urlsplit


LIMITATION = "Structural checks do not prove behavioral correctness."
CHECK_IDS = tuple(f"C{number:02d}" for number in range(1, 13))

BASELINE_FILES = (
    "baseline/product-development-cycle/SKILL.md",
    "baseline/product-development-cycle/agents/openai.yaml",
    "baseline/product-development-cycle/assets/AGENTS.template.md",
    "baseline/product-development-cycle/references/agentic-development.md",
    "baseline/product-development-cycle/references/financial-model.md",
    "baseline/product-development-cycle/references/lifecycle.md",
    "baseline/product-development-cycle/references/quality-gates.md",
)

REQUIRED_ACTIVE_FILES = (
    "scripts/check_workflow.py",
    "BASELINE.sha256",
    "README.md",
    "CHANGELOG.md",
    "docs/PROJECT_STATUS.md",
    "skills/product-development-workflow/SKILL.md",
    "skills/product-development-workflow/agents/openai.yaml",
    "skills/product-development-workflow/assets/AGENTS.template.md",
    "skills/product-development-workflow/assets/PROJECT_STATUS.template.md",
    "skills/product-development-workflow/assets/project-profile.template.md",
    "skills/product-development-workflow/assets/role-prompts.md",
    "skills/product-development-workflow/assets/work-item-and-review-templates.md",
    "skills/product-development-workflow/references/agentic-development.md",
    "skills/product-development-workflow/references/codex-runtime.md",
    "skills/product-development-workflow/references/dependencies.md",
    "skills/product-development-workflow/references/financial-model.md",
    "skills/product-development-workflow/references/lifecycle.md",
    "skills/product-development-workflow/references/quality-gates.md",
)

REVISION_PATHS = tuple(sorted(set(REQUIRED_ACTIVE_FILES) | set(BASELINE_FILES)))

WORK_PACKAGE_LABELS = (
    "Work Item/module identity",
    "Outcome/why",
    "Scope/non-goals",
    "Binding sources",
    "Dependencies",
    "Maturity identity",
    "Architecture identity",
    "Process identity",
    "Plan identity",
    "Exact base",
    "Exact head",
    "Allowed paths",
    "Permissions/data/recovery",
    "Acceptance criteria",
    "Checks",
    "Role",
    "Executor kind",
    "Native ID",
    "Parent identity",
    "Report to identity",
    "Constraints",
    "Current state/findings",
    "Next action",
)

REVIEW_RECORD_LABELS = (
    "Phase",
    "Independent reviewer kind",
    "Independent reviewer Native ID",
    "Reviewed plan hash or base/head/main",
    "Binding sources",
    "Checks",
    "Findings",
    "Verdict",
    "Invalidation condition",
)

PROFILE_SECTION_FIELDS = {
    "Process identity": (
        "Selected release",
        "Selected commit/content identity",
        "Actually loaded identity",
        "Identity state",
    ),
    "Product": (
        "Product mode and objective",
        "Target user and outcome",
        "Communication language",
        "Decision owner/coordinator",
        "Current scope and non-goals",
    ),
    "Maturity": ("Current stage", "Target stage", "Stage outcome and exit need"),
    "Architecture": (
        "Vision identity",
        "Current implementation identity",
        "Current limits",
        "Next transition trigger",
        "Transition evidence required",
        "Data preservation or lifecycle rule",
        "Rollback/replacement path",
    ),
    "Load profile": (
        "User unit",
        "Active period",
        "Peak concurrent work or peak operation rate",
        "Heavy operation",
        "Data volume",
        "Latency/reliability objective",
        "Cost ceiling",
        "Evidence source",
        "Next measurement",
    ),
    "Sources of truth": (
        "Product/requirements identity",
        "Journey/design identity",
        "Architecture/decision identity",
        "Risk/release identity",
        "GitHub host/repository",
    ),
    "Runtime": (
        "Runtime environment",
        "Allowed parallelism",
        "Actual dependencies",
        "Transient runtime handoff location",
    ),
    "Models": (
        "Requested model/reasoning",
        "Accepted native assignment",
        "Independently verified runtime fact",
    ),
    "Economics": (
        "Mode (`commercial`, `internal`, or `non-commercial`)",
        "Commercial assumptions and targets",
        "Non-commercial budget/value constraint",
        "Current decision and investment boundary",
        "Recalculation trigger",
    ),
    "Applicability": (
        "Gate/check",
        "State",
        "Current scope/stage",
        "Evidence source and identity/date",
        "Rationale",
        "Owner/decision authority",
        "Missing evidence or accepted limitation",
        "Revisit trigger",
        "Dependent transition",
    ),
}


@dataclass(frozen=True)
class Check:
    id: str
    status: str
    evidence: str


class InputError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


class StructuralInputFailure(Exception):
    def __init__(self, relative_path: str):
        super().__init__(relative_path)
        self.relative_path = relative_path


def _relative_evidence_path(root: Path, path: Path) -> str:
    try:
        return path.absolute().relative_to(root.absolute()).as_posix()
    except ValueError:
        return "structural input"


def _has_symlink_component(root: Path, path: Path) -> bool:
    try:
        relative = path.absolute().relative_to(root.absolute())
    except ValueError:
        return True
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            return True
    return False


def _is_bounded_regular_file(root: Path, path: Path) -> bool:
    return not _has_symlink_component(root, path) and path.is_file()


def _is_bounded_directory(root: Path, path: Path) -> bool:
    return not _has_symlink_component(root, path) and path.is_dir()


def _read_path_text(root: Path, path: Path) -> str:
    if not _is_bounded_regular_file(root, path):
        raise StructuralInputFailure(_relative_evidence_path(root, path))
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise StructuralInputFailure(_relative_evidence_path(root, path)) from exc


def _read_path_bytes(root: Path, path: Path) -> bytes:
    if not _is_bounded_regular_file(root, path):
        raise StructuralInputFailure(_relative_evidence_path(root, path))
    try:
        return path.read_bytes()
    except OSError as exc:
        raise StructuralInputFailure(_relative_evidence_path(root, path)) from exc


def prerequisite_safe(check_id: str):
    def failure(evidence: str) -> Check:
        if check_id == "C12":
            evidence = f"{evidence}; {LIMITATION}"
        return Check(check_id, "FAIL", evidence)

    def decorate(function):
        @wraps(function)
        def wrapped(root: Path, *args, **kwargs):
            try:
                return function(root, *args, **kwargs)
            except StructuralInputFailure as exc:
                return failure(
                    f"required structural input is unreadable: {exc.relative_path}"
                )
            except (OSError, UnicodeError):
                return failure("required structural input is unreadable")

        return wrapped

    return decorate


def resolve_root(path: Path) -> Path:
    root = path.resolve()
    if not root.is_dir():
        raise InputError("invalid-root", "root must be an existing directory")
    return root


def resolve_review_state(root: Path, path: Path) -> Path:
    root = root.resolve()
    candidate = path if path.is_absolute() else root / path
    resolved = candidate.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise InputError(
            "invalid-review-state-path", "review-state must be inside root"
        ) from exc
    if not resolved.is_file():
        raise InputError("invalid-review-state-path", "review-state must be a readable file")
    return resolved


def _file_frame(root: Path, relative_path: str) -> tuple[bytes, bytes]:
    path = root / relative_path
    if _has_symlink_component(root, path):
        return b"O", b""
    if _is_bounded_regular_file(root, path):
        try:
            return b"F", path.read_bytes()
        except OSError:
            return b"O", b""
    if path.exists():
        return b"O", b""
    return b"M", b""


def compute_revision(root: Path) -> str:
    paths = set(REVISION_PATHS)
    validation = root / "docs/validation.md"
    if _has_symlink_component(root, validation) or validation.exists():
        paths.add("docs/validation.md")

    digest = hashlib.sha256()
    digest.update(b"PDW-STRUCTURAL-REVISION-v1\0")
    for relative_path in sorted(paths):
        encoded_path = relative_path.encode("utf-8")
        kind, content = _file_frame(root, relative_path)
        digest.update(struct.pack(">Q", len(encoded_path)))
        digest.update(encoded_path)
        digest.update(kind)
        digest.update(struct.pack(">Q", len(content)))
        digest.update(content)
    return f"sha256:{digest.hexdigest()}"


def check_c02(root: Path) -> Check:
    missing = []
    for relative_path in REQUIRED_ACTIVE_FILES:
        path = root / relative_path
        if not _is_bounded_regular_file(root, path):
            missing.append(relative_path)
    if missing:
        return Check("C02", "FAIL", f"missing or non-regular: {', '.join(missing)}")
    return Check(
        "C02",
        "PASS",
        f"required active files: {len(REQUIRED_ACTIVE_FILES)}/{len(REQUIRED_ACTIVE_FILES)} present",
    )


def _read_text(root: Path, relative_path: str) -> str:
    return _read_path_text(root, root / relative_path)


@prerequisite_safe("C01")
def check_c01(root: Path) -> Check:
    manifest_path = root / "BASELINE.sha256"
    if not _is_bounded_regular_file(root, manifest_path):
        return Check("C01", "FAIL", "baseline manifest missing or non-regular: BASELINE.sha256")
    records: dict[str, str] = {}
    malformed = False
    for line in _read_path_text(root, manifest_path).splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\s]+)", line)
        if not match or match.group(2) in records:
            malformed = True
            continue
        records[match.group(2)] = match.group(1)
    if malformed or tuple(records) != BASELINE_FILES:
        return Check("C01", "FAIL", "baseline manifest must contain the exact seven-file set")
    mismatches = []
    for relative_path, expected in records.items():
        path = root / relative_path
        if not _is_bounded_regular_file(root, path):
            mismatches.append(relative_path)
        elif hashlib.sha256(_read_path_bytes(root, path)).hexdigest() != expected:
            mismatches.append(relative_path)
    if mismatches:
        return Check("C01", "FAIL", f"baseline hash mismatch: {', '.join(mismatches)}")
    return Check("C01", "PASS", "baseline manifest: 7/7 matched")


@dataclass(frozen=True)
class InlineConstruct:
    kind: Literal["link", "image", "invalid"]
    destination: str | None


def _is_escaped_opener(line: str, start: int) -> bool:
    backslashes = 0
    cursor = start - 1
    while cursor >= 0 and line[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def _next_unescaped_opener(line: str, start: int) -> int | None:
    cursor = start
    while cursor < len(line):
        if line.startswith("![", cursor):
            if not _is_escaped_opener(line, cursor):
                return cursor
            cursor += 2
            continue
        if line[cursor] == "[":
            if not _is_escaped_opener(line, cursor):
                return cursor
            cursor += 1
            continue
        cursor += 1
    return None


def _invalid_inline_construct(line: str, payload_open: int) -> tuple[InlineConstruct, int]:
    recovery = line.find(")", payload_open + 1)
    next_index = len(line) if recovery < 0 else recovery + 1
    return InlineConstruct("invalid", None), next_index


def _scan_inline_construct(
    line: str, start: int
) -> tuple[InlineConstruct | None, int]:
    if line.startswith("![", start):
        kind: Literal["link", "image"] = "image"
        opener_length = 2
    elif start < len(line) and line[start] == "[":
        if start > 0 and line[start - 1] == "!":
            return None, start + 1
        kind = "link"
        opener_length = 1
    else:
        return None, start + 1

    if _is_escaped_opener(line, start):
        return None, start + opener_length

    label_start = start + opener_length
    next_opener = _next_unescaped_opener(line, label_start)
    payload_boundary = line.find("](", label_start)
    if next_opener is not None and (
        payload_boundary < 0 or next_opener < payload_boundary
    ):
        return None, next_opener
    if payload_boundary < 0:
        return None, start + opener_length

    payload_open = payload_boundary + 1
    label = line[label_start:payload_boundary]
    if any(
        character in "[]\\" or ord(character) < 32 or ord(character) == 127
        for character in label
    ):
        return _invalid_inline_construct(line, payload_open)

    cursor = payload_open + 1
    while cursor < len(line) and line[cursor] in " \t":
        cursor += 1

    if cursor < len(line) and line[cursor] == "<":
        destination_start = cursor + 1
        cursor = destination_start
        while cursor < len(line) and line[cursor] != ">":
            character = line[cursor]
            if character == "\\" or ord(character) < 32 or ord(character) == 127:
                return _invalid_inline_construct(line, payload_open)
            cursor += 1
        if cursor >= len(line):
            return _invalid_inline_construct(line, payload_open)
        destination = line[destination_start:cursor]
        cursor += 1
    else:
        destination_start = cursor
        while cursor < len(line) and line[cursor] not in " \t)":
            character = line[cursor]
            if (
                character in "(\\"
                or ord(character) < 32
                or ord(character) == 127
            ):
                return _invalid_inline_construct(line, payload_open)
            cursor += 1
        destination = line[destination_start:cursor]

    if cursor < len(line) and line[cursor] == ")":
        return InlineConstruct(kind, destination), cursor + 1

    separator_start = cursor
    while cursor < len(line) and line[cursor] in " \t":
        cursor += 1
    if (
        cursor == separator_start
        or cursor >= len(line)
        or line[cursor] not in {'"', "'"}
    ):
        return _invalid_inline_construct(line, payload_open)

    quote = line[cursor]
    cursor += 1
    while cursor < len(line) and line[cursor] != quote:
        character = line[cursor]
        if character == "\\" or ord(character) < 32 or ord(character) == 127:
            return _invalid_inline_construct(line, payload_open)
        cursor += 1
    if cursor >= len(line):
        return _invalid_inline_construct(line, payload_open)

    cursor += 1
    while cursor < len(line) and line[cursor] in " \t":
        cursor += 1
    if cursor >= len(line) or line[cursor] != ")":
        return _invalid_inline_construct(line, payload_open)
    return InlineConstruct(kind, destination), cursor + 1


def _scan_inline_constructs(content: str) -> tuple[InlineConstruct, ...]:
    constructs = []
    for line in content.split("\n"):
        cursor = 0
        while cursor < len(line):
            construct, next_cursor = _scan_inline_construct(line, cursor)
            if construct is not None:
                constructs.append(construct)
            cursor = next_cursor
    return tuple(constructs)


@prerequisite_safe("C03")
def check_c03(root: Path) -> Check:
    active = root / "skills/product-development-workflow"
    failures = []
    paths = active.rglob("*.md") if _is_bounded_directory(root, active) else ()
    for path in sorted(paths):
        if not _is_bounded_regular_file(root, path):
            continue
        relative_source = path.relative_to(root).as_posix()
        for construct in _scan_inline_constructs(_read_path_text(root, path)):
            if construct.kind == "image":
                continue
            if construct.kind == "invalid" or not construct.destination:
                failures.append(relative_source)
                continue
            destination = construct.destination
            try:
                parsed = urlsplit(destination)
            except ValueError:
                failures.append(relative_source)
                continue
            fragment_only = (
                destination.startswith("#")
                and not parsed.scheme
                and not parsed.netloc
                and not parsed.path
                and not parsed.query
            )
            if parsed.scheme in {"http", "https", "mailto"} or fragment_only:
                continue
            if parsed.scheme or parsed.netloc or not parsed.path:
                failures.append(relative_source)
                continue
            target_text = parsed.path
            if target_text.startswith("/"):
                failures.append(relative_source)
                continue
            target = path.parent / target_text
            if _has_symlink_component(root, target):
                failures.append(relative_source)
                continue
            resolved_target = target.resolve()
            try:
                resolved_target.relative_to(active.resolve())
            except ValueError:
                failures.append(relative_source)
                continue
            if not resolved_target.is_file():
                failures.append(relative_source)
    if failures:
        return Check("C03", "FAIL", f"invalid local link in: {', '.join(sorted(set(failures)))}")
    return Check("C03", "PASS", "active Markdown inline links resolve within the skill")


@prerequisite_safe("C04")
def check_c04(root: Path) -> Check:
    skill = _read_text(root, "skills/product-development-workflow/SKILL.md")
    metadata = _read_text(root, "skills/product-development-workflow/agents/openai.yaml")
    frontmatter = skill.split("---", 2)
    skill_metadata = frontmatter[1] if len(frontmatter) == 3 else ""
    valid_skill = (
        _metadata_scalar(skill_metadata, "name") == "product-development-workflow"
        and _metadata_scalar(skill_metadata, "description") is not None
    )
    default_prompt = _metadata_scalar(metadata, "default_prompt")
    valid_metadata = (
        _metadata_scalar(metadata, "display_name") == "Product Development Workflow"
        and _metadata_scalar(metadata, "short_description") is not None
        and default_prompt is not None
        and "$product-development-workflow" in default_prompt
    )
    if not (valid_skill and valid_metadata):
        return Check("C04", "FAIL", "skill or UI metadata does not match the workflow contract")
    return Check("C04", "PASS", "skill and UI metadata match the workflow contract")


def _metadata_scalar(content: str, key: str) -> str | None:
    values = re.findall(
        rf"(?m)^[ \t]*{re.escape(key)}:[ \t]*([^\r\n]*)$",
        content,
    )
    if len(values) != 1:
        return None
    raw = values[0].strip()
    if not raw:
        return None
    if raw[0] in {'"', "'"}:
        if len(raw) < 2 or raw[-1] != raw[0]:
            return None
        raw = raw[1:-1].strip()
    return raw or None


@prerequisite_safe("C05")
def check_c05(root: Path) -> Check:
    lifecycle = _read_text(root, "skills/product-development-workflow/references/lifecycle.md")
    gates = re.findall(r"(?m)^## (\d+(?:\.\d+)?)\.", lifecycle)
    expected = ["0", "1", "2", "3", "3.5", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"]
    if gates != expected or len(gates) != len(set(gates)):
        return Check("C05", "FAIL", "level-2 gate order does not match the canonical sequence")
    return Check("C05", "PASS", "level-2 gate order matches the canonical sequence")


@prerequisite_safe("C06")
def check_c06(root: Path) -> Check:
    lifecycle = _read_text(root, "skills/product-development-workflow/references/lifecycle.md")
    skill = _read_text(root, "skills/product-development-workflow/SKILL.md")
    route = (skill.find("Positioning"), skill.find("light Gate 3.5"), skill.find("Journey"))
    valid = (
        lifecycle.count("## 3.5. Light viability") == 1
        and "## 4.5." not in lifecycle
        and -1 not in route
        and route[0] < route[1] < route[2]
    )
    if not valid:
        return Check("C06", "FAIL", "the single light Gate 3.5 contract is not satisfied")
    return Check("C06", "PASS", "one light Gate 3.5 precedes Journey; no active Gate 4.5")


@prerequisite_safe("C07")
def check_c07(root: Path) -> Check:
    lifecycle = _read_text(root, "skills/product-development-workflow/references/lifecycle.md")
    skill = _read_text(root, "skills/product-development-workflow/SKILL.md")
    lifecycle_labels = ("### working-prototype", "### mvp", "### scale-1", "### scale-2", "### mature")
    skill_labels = ("- working prototype", "- MVP", "- scale 1", "- scale 2", "- mature operation")
    if not all(label in lifecycle for label in lifecycle_labels) or not all(label in skill for label in skill_labels):
        return Check("C07", "FAIL", "one or more required maturity stages are missing")
    return Check("C07", "PASS", "all five maturity stages are present in lifecycle and entry point")


@prerequisite_safe("C08")
def check_c08(root: Path) -> Check:
    profile = _read_text(root, "skills/product-development-workflow/assets/project-profile.template.md")
    missing = []
    for section_name, fields in PROFILE_SECTION_FIELDS.items():
        section = _markdown_section(profile, section_name)
        if not section:
            missing.append(section_name)
            continue
        missing.extend(f"{section_name}/{field}" for field in fields if field not in section)
    if missing or "Unknown" not in profile:
        return Check("C08", "FAIL", "profile is missing required sections or decision-bearing fields")
    return Check("C08", "PASS", "profile includes required sections, fields, and Unknown defaults")


def _markdown_section(content: str, heading: str) -> str:
    match = re.search(rf"(?m)^## {re.escape(heading)}$", content)
    if match is None:
        return ""
    following = re.search(r"(?m)^## .+$", content[match.end() :])
    end = len(content) if following is None else match.end() + following.start()
    return content[match.start() : end]


@prerequisite_safe("C09")
def check_c09(root: Path) -> Check:
    templates = _read_text(root, "skills/product-development-workflow/assets/work-item-and-review-templates.md")
    work_package = _markdown_section(templates, "Work package / handoff")
    review_record = _markdown_section(templates, "Review record")
    missing_work = [label for label in WORK_PACKAGE_LABELS if f"- {label}:" not in work_package]
    missing_review = [label for label in REVIEW_RECORD_LABELS if f"- {label}:" not in review_record]
    if missing_work or missing_review:
        return Check("C09", "FAIL", "handoff or review record is missing section-local labels")
    return Check("C09", "PASS", "handoff and review record contain all section-local labels")


REVIEW_PHASES = {
    "PLAN": ("PLAN_PASS", ("plan_hash", "base_sha")),
    "CHANGE_REVIEW": ("PASS", ("base_sha", "head_sha")),
    "FINAL": ("FINAL_PASS", ("main_sha",)),
}


def _valid_identity_value(key: str, value: object) -> bool:
    length = 64 if key == "plan_hash" else 40
    return isinstance(value, str) and re.fullmatch(rf"[0-9a-f]{{{length}}}", value) is not None


def parse_review_state(root: Path, path: Path) -> dict[str, object]:
    resolved = resolve_review_state(root, path)
    try:
        state = json.loads(resolved.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise InputError("invalid-review-state", "review-state is not valid JSON") from exc

    valid = isinstance(state, dict) and set(state) == {"phase", "verdict", "reviewed", "current"}
    if valid:
        phase = state["phase"]
        valid = isinstance(phase, str) and phase in REVIEW_PHASES
    if valid:
        verdict, identity_keys = REVIEW_PHASES[phase]
        valid = state["verdict"] == verdict
    if valid:
        expected_keys = set(identity_keys)
        for name in ("reviewed", "current"):
            identity = state[name]
            if not isinstance(identity, dict) or set(identity) != expected_keys:
                valid = False
                break
            if not all(_valid_identity_value(key, identity[key]) for key in identity_keys):
                valid = False
                break
    if not valid:
        raise InputError(
            "invalid-review-state", "review-state does not match the required phase schema"
        )
    return state


def check_c10(state: dict[str, object], relative_source: str) -> Check:
    evidence_suffix = "provided input; not live owning-system evidence"
    if state["reviewed"] != state["current"]:
        return Check("C10", "FAIL", f"review identity is stale in {relative_source}; {evidence_suffix}")
    return Check("C10", "PASS", f"review identity is current in {relative_source}; {evidence_suffix}")


PRIVATE_BINDING_RULES = (
    ("user-path", re.compile(r"/Users/[^\s)>`]+")),
    ("recipes-binding", re.compile(r"(?:github\.com/)?WorkKroG/recipes(?:-v\d+)?", re.IGNORECASE)),
    ("runtime-uuid", re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.IGNORECASE)),
    ("credential-prefix", re.compile(r"\b(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("client-id-marker", re.compile(r"\bclient-new-thread:[A-Za-z0-9_-]+\b")),
)


def _private_binding_files(root: Path) -> list[Path]:
    active = root / "skills/product-development-workflow"
    files = []
    if _is_bounded_directory(root, active):
        for suffix in ("*.md", "*.yaml"):
            files.extend(active.rglob(suffix))
    files.extend(root / relative for relative in ("README.md", "CHANGELOG.md", "docs/PROJECT_STATUS.md"))
    validation = root / "docs/validation.md"
    if validation.exists() or validation.is_symlink():
        files.append(validation)
    return sorted(set(files), key=lambda path: path.relative_to(root).as_posix())


@prerequisite_safe("C11")
def check_c11(root: Path) -> Check:
    findings = []
    for path in _private_binding_files(root):
        if not _is_bounded_regular_file(root, path):
            continue
        relative_path = path.relative_to(root).as_posix()
        content = _read_path_text(root, path)
        for rule_name, pattern in PRIVATE_BINDING_RULES:
            if pattern.search(content):
                findings.append(f"{rule_name}@{relative_path}")
    if findings:
        return Check("C11", "FAIL", f"private binding rules matched: {', '.join(findings)}")
    return Check("C11", "PASS", "public allowlist contains no forbidden private bindings")


def _operational_files(root: Path) -> list[Path]:
    active = root / "skills/product-development-workflow"
    files = [active / "SKILL.md", active / "agents/openai.yaml"]
    references = active / "references"
    if _is_bounded_directory(root, references):
        files.extend(sorted(references.glob("*")))
    files.extend(root / relative for relative in ("README.md", "CHANGELOG.md", "docs/PROJECT_STATUS.md"))
    validation = root / "docs/validation.md"
    if validation.exists() or validation.is_symlink():
        files.append(validation)
    return files


@prerequisite_safe("C12")
def check_c12(root: Path) -> Check:
    marker = re.compile(r"(?im)^\s*(?:[-*]\s*)?(?:TBD|TODO|FIXME|XXX|IMPLEMENT ME|FILL IN)\b")
    failures = []
    for path in _operational_files(root):
        if not _is_bounded_regular_file(root, path):
            continue
        if marker.search(_read_path_text(root, path)):
            failures.append(path.relative_to(root).as_posix())
    if failures:
        return Check(
            "C12",
            "FAIL",
            f"placeholder marker found in: {', '.join(failures)}; {LIMITATION}",
        )
    return Check("C12", "PASS", f"operational files contain no placeholder line markers; {LIMITATION}")


def render_json(revision: str, checks: Sequence[Check]) -> dict[str, object]:
    return {
        "revision": revision,
        "passed": [check.id for check in checks if check.status == "PASS"],
        "failed": [check.id for check in checks if check.status == "FAIL"],
        "checks": [asdict(check) for check in checks],
    }


def render_text(revision: str, checks: Sequence[Check]) -> str:
    lines = [f"{check.id} {check.status} {check.evidence}" for check in checks]
    passed = sum(check.status == "PASS" for check in checks)
    failed = sum(check.status == "FAIL" for check in checks)
    lines.extend(
        (
            f"passed: {passed}",
            f"failed: {failed}",
            f"revision: {revision}",
            LIMITATION,
        )
    )
    return "\n".join(lines)


def render_error_json(error: InputError) -> dict[str, object]:
    return {
        "revision": None,
        "passed": [],
        "failed": [],
        "checks": [],
        "error": {"code": error.code, "message": str(error)},
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--review-state", required=True, type=Path)
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args(argv)

    try:
        root = resolve_root(args.root)
        review_path = resolve_review_state(root, args.review_state)
        review_state = parse_review_state(root, review_path)
        relative_source = review_path.relative_to(root).as_posix()
        revision = compute_revision(root)
        checks = (
            check_c01(root),
            check_c02(root),
            check_c03(root),
            check_c04(root),
            check_c05(root),
            check_c06(root),
            check_c07(root),
            check_c08(root),
            check_c09(root),
            check_c10(review_state, relative_source),
            check_c11(root),
            check_c12(root),
        )
    except InputError as error:
        if args.json_output:
            print(json.dumps(render_error_json(error), separators=(",", ":")))
        else:
            print(f"ERROR {error.code}: {error}", file=sys.stderr)
        return 2

    if args.json_output:
        print(json.dumps(render_json(revision, checks), separators=(",", ":")))
    else:
        print(render_text(revision, checks))
    return 1 if any(check.status == "FAIL" for check in checks) else 0


if __name__ == "__main__":
    raise SystemExit(main())
