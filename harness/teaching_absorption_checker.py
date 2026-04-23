#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

from common import CheckResult, load_yaml, result_from_issues


LESSON_HEADING = re.compile(r"^##\s+(LESSON-[^:]+):\s+(.+)$")


def _lesson_blocks(path: Path) -> list[tuple[str, str]]:
    if not path.exists():
        return []
    blocks: list[tuple[str, str]] = []
    current_id = ""
    current_lines: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = LESSON_HEADING.match(line)
        if match:
            if current_id:
                blocks.append((current_id, "\n".join(current_lines)))
            current_id = match.group(1).strip()
            current_lines = [line]
        elif current_id:
            current_lines.append(line)
    if current_id:
        blocks.append((current_id, "\n".join(current_lines)))
    return blocks


def _field_present(block: str, field: str) -> bool:
    return re.search(rf"^-\s+{re.escape(field)}\s*:\s*\S+", block, re.MULTILINE) is not None


def _parse_components(block: str) -> list[str]:
    match = re.search(r"^-\s+affected_components\s*:\s*(.+)$", block, re.MULTILINE)
    if not match:
        return []
    return [item.strip() for item in match.group(1).split(",") if item.strip()]


def check_teaching_absorption(base_dir: Path) -> CheckResult:
    policy = load_yaml(base_dir / "governance" / "teaching_policy.yaml")
    requirements = policy.get("absorption_requirements", {})
    required_accepted = requirements.get("accepted_lessons_must_have", [])
    allowed_components = set(requirements.get("affected_components_allowed", []))
    issues: list[str] = []

    accepted_path = base_dir / "teaching" / "accepted_lessons.md"
    open_path = base_dir / "teaching" / "open_lessons.md"
    accepted_blocks = _lesson_blocks(accepted_path)

    if not accepted_blocks:
        issues.append("No accepted lessons found.")

    for lesson_id, block in accepted_blocks:
        for field in required_accepted:
            if field == "lesson_id":
                continue
            if not _field_present(block, field):
                issues.append(f"{lesson_id} missing required field: {field}")
        components = _parse_components(block)
        if not components:
            issues.append(f"{lesson_id} has no affected_components.")
        unknown = [component for component in components if component not in allowed_components]
        if unknown:
            issues.append(f"{lesson_id} references unsupported affected_components: {', '.join(unknown)}")

    open_text = open_path.read_text(encoding="utf-8") if open_path.exists() else ""
    if "status: proposed" in open_text and "pending_decision" not in open_text:
        issues.append("Open lessons include proposed item(s) without pending_decision.")

    return result_from_issues("teaching_absorption", issues, warn_only=True)
