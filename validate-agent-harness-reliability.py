#!/usr/bin/env python3
"""Validate the beginner agent harness reliability package."""

from __future__ import annotations

import argparse
import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any


REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    "justfile",
    "make-release-zip.py",
    "runbook/agent-harness-reliability-runbook.md",
    "runbook/quick-start-card.md",
    "prompts/01-audit-current-memory.md",
    "prompts/02-create-memory-write-rules.md",
    "prompts/03-add-checkpoint-resume.md",
    "prompts/04-build-validator-fixtures.md",
    "prompts/05-review-agent-loop.md",
    "templates/MEMORY-WRITE-PROPOSAL-template.json",
    "templates/TASK-UPDATE-PROPOSAL-template.json",
    "templates/CHECKPOINT-RESUME-template.json",
    "starter-kit/memory-write-rules.md",
    "starter-kit/checkpoint-resume-template.json",
    "examples/simple-memory-write-proposal.json",
    "examples/simple-checkpoint-resume.json",
    "examples/simple-task-ready-for-review.json",
    "examples/reviewed-completion.json",
    "examples/warn-missing-validation.json",
    "examples/fail-complete-before-review.json",
]

LIMITED_HYGIENE_MARKERS = [
    "TODO",
    "FIXME",
    "PRIVATE_WORKSPACE_MARKER",
    "/home/xbill/.openclaw",
    "AGENTMAIL_API_KEY",
]

ALLOWED_RECORD_TYPES = {
    "project_decision",
    "user_preference",
    "operating_rule",
    "temporary_note",
    "task_status_update",
    "checkpoint_resume",
}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
ALLOWED_APPROVAL = {"auto-safe", "needs-review", "reviewed", "reject"}
ALLOWED_REVIEW_STATE = {"pending", "reviewed"}
ALLOWED_EXPECTED = {"pass", "warn", "fail"}
ALLOWED_CHECKPOINT_STATUS = {"in_progress", "blocked", "ready_for_review", "complete"}


def label(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return path.name


def load_json(path: Path, root: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            item = json.load(handle)
    except JSONDecodeError as exc:
        return None, [f"{label(path, root)}: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"]
    except OSError as exc:
        return None, [f"{label(path, root)}: cannot read file: {exc}"]
    if not isinstance(item, dict):
        return None, [f"{label(path, root)}: top-level JSON value must be an object"]
    return item, []


def require_fields(item: dict[str, Any], path: Path, root: Path, fields: list[str]) -> list[str]:
    return [f"{label(path, root)}: missing {field}" for field in fields if field not in item]


def require_non_empty_string(item: dict[str, Any], path: Path, root: Path, field: str) -> list[str]:
    value = item.get(field)
    if not isinstance(value, str) or not value.strip():
        return [f"{label(path, root)}: {field} must be a non-empty string"]
    return []


def require_string_list(item: dict[str, Any], path: Path, root: Path, field: str, *, allow_empty: bool = False) -> list[str]:
    value = item.get(field)
    if not isinstance(value, list) or not all(isinstance(entry, str) for entry in value):
        return [f"{label(path, root)}: {field} must be a list of strings"]
    if not allow_empty and not value:
        return [f"{label(path, root)}: {field} must not be empty"]
    if any(not entry.strip() for entry in value):
        return [f"{label(path, root)}: {field} must not contain empty strings"]
    return []


def require_enum(item: dict[str, Any], path: Path, root: Path, field: str, allowed: set[str]) -> list[str]:
    value = item.get(field)
    if value not in allowed:
        allowed_text = ", ".join(sorted(allowed))
        return [f"{label(path, root)}: {field} must be one of: {allowed_text}"]
    return []


def validate_memory_proposal(item: dict[str, Any], path: Path, root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    errors.extend(require_fields(item, path, root, ["id", "type", "destination", "source", "summary", "confidence", "approval", "reason"]))
    for field in ["id", "type", "source", "summary", "confidence", "approval", "reason"]:
        if field in item:
            errors.extend(require_non_empty_string(item, path, root, field))
    if "destination" in item:
        errors.extend(require_string_list(item, path, root, "destination"))
    if "type" in item:
        errors.extend(require_enum(item, path, root, "type", {"project_decision", "user_preference", "operating_rule", "temporary_note"}))
    if "confidence" in item:
        errors.extend(require_enum(item, path, root, "confidence", ALLOWED_CONFIDENCE))
    if "approval" in item:
        errors.extend(require_enum(item, path, root, "approval", ALLOWED_APPROVAL))
    destination = item.get("destination", [])
    if isinstance(destination, list) and "MEMORY.md" in destination and not item.get("durable_reason"):
        errors.append(f"{label(path, root)}: MEMORY.md destination needs durable_reason")
    if item.get("type") == "temporary_note" and isinstance(destination, list) and "MEMORY.md" in destination:
        errors.append(f"{label(path, root)}: temporary_note should not target MEMORY.md")
    return errors, warnings


def validate_checkpoint(item: dict[str, Any], path: Path, root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    required = [
        "id",
        "type",
        "task_id",
        "source",
        "goal",
        "status",
        "decisions",
        "changed_paths",
        "validation_done",
        "blockers",
        "next_action",
        "do_not_redo",
        "evidence",
    ]
    errors.extend(require_fields(item, path, root, required))
    for field in ["id", "type", "task_id", "source", "goal", "status", "next_action"]:
        if field in item:
            errors.extend(require_non_empty_string(item, path, root, field))
    for field in ["decisions", "changed_paths", "validation_done", "blockers", "do_not_redo", "evidence"]:
        if field in item:
            errors.extend(require_string_list(item, path, root, field, allow_empty=field in {"decisions", "changed_paths", "validation_done", "blockers"}))
    if "type" in item:
        errors.extend(require_enum(item, path, root, "type", {"checkpoint_resume"}))
    if "status" in item:
        errors.extend(require_enum(item, path, root, "status", ALLOWED_CHECKPOINT_STATUS))
    if item.get("changed_paths") and not item.get("validation_done"):
        warnings.append(f"{label(path, root)}: changed_paths should normally have validation_done")
    return errors, warnings


def validate_tracker_update(item: dict[str, Any], path: Path, root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    required = [
        "id",
        "task_id",
        "type",
        "source",
        "status_change",
        "summary",
        "next_step",
        "evidence",
        "approval",
        "review_state",
    ]
    errors.extend(require_fields(item, path, root, required))
    for field in ["id", "task_id", "type", "source", "status_change", "summary", "next_step", "approval", "review_state"]:
        if field in item:
            errors.extend(require_non_empty_string(item, path, root, field))
    if "evidence" in item:
        errors.extend(require_string_list(item, path, root, "evidence"))
    if "type" in item:
        errors.extend(require_enum(item, path, root, "type", {"task_status_update"}))
    if "approval" in item:
        errors.extend(require_enum(item, path, root, "approval", ALLOWED_APPROVAL))
    if "review_state" in item:
        errors.extend(require_enum(item, path, root, "review_state", ALLOWED_REVIEW_STATE))

    status_change = str(item.get("status_change", "")).lower()
    if "complete" in status_change:
        if item.get("approval") != "reviewed" or item.get("review_state") != "reviewed":
            errors.append(f"{label(path, root)}: COMPLETE status changes require approval=reviewed and review_state=reviewed")
    if "complete" not in status_change and "ready_for_review" in status_change and item.get("approval") != "needs-review":
        warnings.append(f"{label(path, root)}: READY_FOR_REVIEW updates should normally use approval=needs-review")
    return errors, warnings


def validate_record(item: dict[str, Any], path: Path, root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    record_type = item.get("type")
    if "expected_validator_result" in item:
        errors.extend(require_enum(item, path, root, "expected_validator_result", ALLOWED_EXPECTED))
    if record_type not in ALLOWED_RECORD_TYPES:
        errors.append(f"{label(path, root)}: type must be one of: {', '.join(sorted(ALLOWED_RECORD_TYPES))}")
        return errors, warnings
    if record_type == "task_status_update":
        return validate_tracker_update(item, path, root)
    if record_type == "checkpoint_resume":
        return validate_checkpoint(item, path, root)
    return validate_memory_proposal(item, path, root)


def validate_json_file(path: Path, root: Path) -> tuple[list[str], list[str]]:
    item, load_errors = load_json(path, root)
    if load_errors:
        return load_errors, []
    assert item is not None
    errors, warnings = validate_record(item, path, root)
    expected = item.get("expected_validator_result")
    if expected:
        actual = "fail" if errors else "warn" if warnings else "pass"
        if expected != actual:
            return [f"{label(path, root)}: expected {expected}, got {actual}"], warnings
        return [], warnings
    return errors, warnings


def validate(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel}")

    for path in root.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".txt", ".json"}:
            text = path.read_text(encoding="utf-8", errors="replace")
            for marker in LIMITED_HYGIENE_MARKERS:
                if marker in text:
                    errors.append(f"{label(path, root)} contains limited-hygiene marker: {marker}")

    for path in sorted(root.glob("templates/*.json")) + sorted(root.glob("starter-kit/*.json")) + sorted(root.glob("examples/*.json")):
        item_errors, item_warnings = validate_json_file(path, root)
        errors.extend(item_errors)
        warnings.extend(item_warnings)
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate agent harness reliability runbook package.")
    parser.add_argument("path", nargs="?", default=".", help="Package root to validate.")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    errors, warnings = validate(root)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    if warnings:
        print("Validation passed with expected warnings:")
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
