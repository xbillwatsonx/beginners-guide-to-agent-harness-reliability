#!/usr/bin/env python3
"""Validate the beginner agent harness reliability package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    "justfile",
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
    "examples/warn-missing-validation.json",
    "examples/fail-complete-before-review.json",
]


FORBIDDEN_PUBLIC_MARKERS = [
    "TODO",
    "FIXME",
    "PRIVATE_WORKSPACE_MARKER",
    "/home/xbill/.openclaw",
    "AGENTMAIL_API_KEY",
]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def label(path: Path) -> str:
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return path.name


def validate_memory_proposal(path: Path) -> tuple[list[str], list[str]]:
    item = load_json(path)
    errors: list[str] = []
    warnings: list[str] = []
    required = ["id", "type", "destination", "source", "summary", "confidence", "approval", "reason"]
    for field in required:
        if field not in item:
            errors.append(f"{label(path)}: missing {field}")
    if "MEMORY.md" in item.get("destination", []) and not item.get("durable_reason"):
        errors.append(f"{label(path)}: MEMORY.md destination needs durable_reason")
    if item.get("type") == "temporary_note" and "MEMORY.md" in item.get("destination", []):
        errors.append(f"{label(path)}: temporary_note should not target MEMORY.md")
    return errors, warnings


def validate_checkpoint(path: Path) -> tuple[list[str], list[str]]:
    item = load_json(path)
    errors: list[str] = []
    warnings: list[str] = []
    required = [
        "id",
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
    for field in required:
        if field not in item:
            errors.append(f"{label(path)}: missing {field}")
    if not item.get("do_not_redo"):
        errors.append(f"{label(path)}: do_not_redo should name work the next agent should not repeat")
    if item.get("changed_paths") and not item.get("validation_done"):
        warnings.append(f"{label(path)}: changed_paths should normally have validation_done")
    return errors, warnings


def validate_tracker_update(path: Path) -> tuple[list[str], list[str]]:
    item = load_json(path)
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
    for field in required:
        if field not in item:
            errors.append(f"{label(path)}: missing {field}")
    status_change = str(item.get("status_change", "")).lower()
    if "complete" in status_change and item.get("review_state") not in {"reviewed", "not-needed"}:
        errors.append(f"{label(path)}: complete status changes need reviewed or not-needed review_state")
    if not item.get("evidence"):
        warnings.append(f"{label(path)}: task updates should include evidence")
    return errors, warnings


def classify_example(path: Path) -> tuple[list[str], list[str]]:
    item = load_json(path)
    item_type = item.get("type")
    if str(item.get("id", "")).startswith("CRP-"):
        errors, warnings = validate_checkpoint(path)
    elif item_type == "task_status_update":
        errors, warnings = validate_tracker_update(path)
    else:
        errors, warnings = validate_memory_proposal(path)

    expected = item.get("expected_validator_result", "pass")
    actual = "fail" if errors else "warn" if warnings else "pass"
    if expected != actual:
        return [f"{label(path)}: expected {expected}, got {actual}"], warnings
    return [], warnings


def validate(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel}")

    for path in root.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".txt", ".json"}:
            text = path.read_text(encoding="utf-8", errors="replace")
            for marker in FORBIDDEN_PUBLIC_MARKERS:
                if marker in text:
                    errors.append(f"{path.relative_to(root)} contains forbidden marker: {marker}")

    for path in sorted((root / "examples").glob("*.json")) if (root / "examples").is_dir() else []:
        example_errors, example_warnings = classify_example(path)
        errors.extend(example_errors)
        warnings.extend(example_warnings)
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
