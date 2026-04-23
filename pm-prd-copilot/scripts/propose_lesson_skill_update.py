#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


LESSON_HEADING = re.compile(r"^##\s+(LESSON-[^:]+):\s+(.+)$")
FIELD = re.compile(r"^-\s+([a-zA-Z_]+)\s*:\s*(.*)$")


@dataclass
class Lesson:
    lesson_id: str
    title: str
    source_file: str
    fields: dict[str, str]


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def parse_lessons(path: Path, source_file: str) -> list[Lesson]:
    if not path.exists():
        return []

    lessons: list[Lesson] = []
    current_id = ""
    current_title = ""
    current_lines: list[str] = []

    def flush() -> None:
        if not current_id:
            return
        fields: dict[str, str] = {}
        for line in current_lines:
            match = FIELD.match(line)
            if match:
                fields[match.group(1).strip()] = match.group(2).strip()
        lessons.append(Lesson(current_id, current_title, source_file, fields))

    in_comment = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if "<!--" in line:
            in_comment = True
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        match = LESSON_HEADING.match(line)
        if match:
            flush()
            current_id = match.group(1).strip()
            current_title = match.group(2).strip()
            current_lines = []
        elif current_id:
            current_lines.append(line)
    flush()
    return lessons


def split_components(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def choose_update_location(skill_md: Path, lesson: Lesson) -> list[str]:
    text = skill_md.read_text(encoding="utf-8") if skill_md.exists() else ""
    candidates: list[str] = []
    principle = " ".join(
        [
            lesson.fields.get("principle", ""),
            lesson.fields.get("expected_behavior", ""),
            lesson.fields.get("verification_hint", ""),
        ]
    ).lower()

    if "output" in principle or "include" in principle or "输出" in principle:
        candidates.append("Output Contract")
    if "verify" in principle or "should not" in principle or "不能" in principle or "不要" in principle:
        candidates.append("Guardrails")
    if "rank" in principle or "analyze" in principle or "start" in principle or "先" in principle:
        candidates.append("Workflow")

    existing_headings = {
        line.removeprefix("##").strip()
        for line in text.splitlines()
        if line.startswith("## ")
    }
    matched = [heading for heading in candidates if heading in existing_headings]
    return matched or ["Workflow", "Guardrails"]


def build_proposal(base_dir: Path, lessons: list[Lesson], output_dir: Path) -> tuple[Path, Path]:
    skills = load_yaml(base_dir / "registry" / "skills.yaml").get("skills", {})
    proposal_id = f"skill-update-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"

    routed_updates: list[dict[str, Any]] = []
    non_skill_targets: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for lesson in lessons:
        components = split_components(lesson.fields.get("affected_components", ""))
        for component in components:
            skill = skills.get(component)
            if not skill or not skill.get("path"):
                non_skill_targets.append(
                    {
                        "lesson_id": lesson.lesson_id,
                        "component": component,
                        "reason": "Component is not a registered skill with a repository path.",
                    }
                )
                continue

            key = (lesson.lesson_id, component)
            if key in seen:
                continue
            seen.add(key)
            skill_path = base_dir / str(skill["path"])
            routed_updates.append(
                {
                    "lesson_id": lesson.lesson_id,
                    "lesson_title": lesson.title,
                    "skill": component,
                    "plugin": skill.get("plugin", ""),
                    "path": str(skill["path"]),
                    "status": "proposed",
                    "requires_human_approval": True,
                    "must_not_apply_automatically": True,
                    "lesson_type": lesson.fields.get("lesson_type", ""),
                    "principle": lesson.fields.get("principle", ""),
                    "expected_behavior": lesson.fields.get("expected_behavior", ""),
                    "verification_hint": lesson.fields.get("verification_hint", ""),
                    "suggested_locations": choose_update_location(skill_path / "SKILL.md", lesson),
                }
            )

    payload = {
        "proposal_id": proposal_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "proposed",
        "requires_human_approval": True,
        "must_not_apply_automatically": True,
        "source_lessons": [
            {
                "lesson_id": lesson.lesson_id,
                "title": lesson.title,
                "source_file": lesson.source_file,
                "lesson_type": lesson.fields.get("lesson_type", ""),
            }
            for lesson in lessons
        ],
        "skill_updates": routed_updates,
        "non_skill_targets": non_skill_targets,
        "approval_checklist": [
            "User confirms the lesson is a durable preference or PM principle.",
            "User confirms the routed skill is the right owner.",
            "User approves the exact SKILL.md change before it is applied.",
            "Skill validation, plugin_boundary, harness, and regression pass after applying.",
        ],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{proposal_id}.json"
    md_path = output_dir / f"{proposal_id}.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    return md_path, json_path


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# Skill Update Proposal - {payload['proposal_id']}",
        "",
        "This is a supervised update proposal. It must not be applied automatically.",
        "",
        "## Control",
        f"- status: {payload['status']}",
        f"- requires_human_approval: {payload['requires_human_approval']}",
        f"- must_not_apply_automatically: {payload['must_not_apply_automatically']}",
        "",
        "## Source Lessons",
    ]
    for lesson in payload["source_lessons"]:
        lines.append(f"- {lesson['lesson_id']}: {lesson['title']} ({lesson['lesson_type']})")

    lines.extend(["", "## Routed Skill Updates"])
    if not payload["skill_updates"]:
        lines.append("- No registered skill updates were routed.")
    for update in payload["skill_updates"]:
        locations = ", ".join(update["suggested_locations"])
        lines.extend(
            [
                f"- skill: {update['skill']}",
                f"  path: {update['path']}",
                f"  plugin: {update['plugin'] or 'none'}",
                f"  source_lesson: {update['lesson_id']}",
                f"  suggested_locations: {locations}",
                f"  principle: {update['principle']}",
                f"  expected_behavior: {update['expected_behavior']}",
                f"  verification_hint: {update['verification_hint']}",
                "",
            ]
        )

    if payload["non_skill_targets"]:
        lines.extend(["## Non-Skill Targets"])
        for target in payload["non_skill_targets"]:
            lines.append(f"- {target['component']} from {target['lesson_id']}: {target['reason']}")
        lines.append("")

    lines.extend(
        [
            "## Approval Checklist",
            *[f"- [ ] {item}" for item in payload["approval_checklist"]],
            "",
        ]
    )
    return "\n".join(lines)


def select_lessons(base_dir: Path, lesson_id: str, source: str) -> list[Lesson]:
    lessons: list[Lesson] = []
    if source in {"accepted", "all"}:
        lessons.extend(parse_lessons(base_dir / "teaching" / "accepted_lessons.md", "teaching/accepted_lessons.md"))
    if source in {"open", "all"}:
        lessons.extend(parse_lessons(base_dir / "teaching" / "open_lessons.md", "teaching/open_lessons.md"))

    if lesson_id == "all":
        return lessons
    selected = [lesson for lesson in lessons if lesson.lesson_id == lesson_id]
    if not selected:
        raise SystemExit(f"Lesson not found: {lesson_id}")
    return selected


def main() -> None:
    parser = argparse.ArgumentParser(description="Route accepted teaching lessons into supervised skill update proposals.")
    parser.add_argument("--base-dir", default=".")
    parser.add_argument("--lesson-id", default="all")
    parser.add_argument("--source", default="accepted", choices=["accepted", "open", "all"])
    parser.add_argument("--output-dir", default="pm-prd-copilot/proposals/skill-patches")
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    lessons = select_lessons(base_dir, args.lesson_id, args.source)
    if not lessons:
        raise SystemExit("No lessons found for proposal generation.")

    md_path, json_path = build_proposal(base_dir, lessons, base_dir / args.output_dir)
    print(md_path)
    print(json_path)


if __name__ == "__main__":
    main()
