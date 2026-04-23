#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ModuleNotFoundError:  # pragma: no cover - optional local dependency
    Draft202012Validator = None


def validate_json(schema_path: Path, candidate_path: Path) -> list[str]:
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    if Draft202012Validator is None:
        return []
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(candidate), key=lambda err: list(err.path))
    return [f"{candidate_path}: {error.message}" for error in errors]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run lightweight regression checks")
    parser.add_argument("--base-dir", default=".")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    errors: list[str] = []

    schema_path = base_dir / "shared" / "schemas" / "requirement_brief.schema.json"
    candidate_path = base_dir / "projects" / "demo-project" / "01_requirement_brief.json"
    if schema_path.exists() and candidate_path.exists():
        errors.extend(validate_json(schema_path, candidate_path))

    prd_schema_path = base_dir / "shared" / "schemas" / "prd_document.schema.json"
    prd_candidate_path = base_dir / "projects" / "demo-project" / "02_prd.generated.json"
    if prd_schema_path.exists() and prd_candidate_path.exists():
        errors.extend(validate_json(prd_schema_path, prd_candidate_path))

    tracking_schema_path = base_dir / "shared" / "schemas" / "tracking_plan.schema.json"
    tracking_candidate_path = base_dir / "projects" / "demo-project" / "05_tracking_plan.generated.json"
    if tracking_schema_path.exists() and tracking_candidate_path.exists():
        errors.extend(validate_json(tracking_schema_path, tracking_candidate_path))
        tracking = json.loads(tracking_candidate_path.read_text(encoding="utf-8"))
        metric_names = {metric["name"] for metric in tracking.get("metrics", [])}
        for event in tracking.get("events", []):
            linked_metric = event.get("linked_metric")
            if linked_metric and linked_metric not in metric_names:
                errors.append(
                    f"{tracking_candidate_path}: linked_metric '{linked_metric}' is missing from metrics"
                )

    story_schema_path = base_dir / "shared" / "schemas" / "user_story.schema.json"
    stories_candidate_path = base_dir / "projects" / "demo-project" / "03_user_stories.generated.json"
    if story_schema_path.exists() and stories_candidate_path.exists():
        stories = json.loads(stories_candidate_path.read_text(encoding="utf-8"))
        if not isinstance(stories, list) or not stories:
            errors.append(f"{stories_candidate_path}: must contain a non-empty list")
        elif Draft202012Validator is not None:
            schema = json.loads(story_schema_path.read_text(encoding="utf-8"))
            validator = Draft202012Validator(schema)
            for story in stories:
                for error in validator.iter_errors(story):
                    errors.append(f"{stories_candidate_path}: {error.message}")

    stable_files = [
        base_dir / "pm-prd-copilot" / "SKILL.md",
        base_dir / "pm-prd-copilot" / "templates" / "prd_template_2026.md",
        base_dir / "pm-prd-copilot" / "memory" / "user_preferences.md",
        base_dir / "pm-prd-copilot" / "scripts" / "run_pipeline.py",
    ]
    for path in stable_files:
        if not path.exists():
            errors.append(f"Missing required file: {path}")

    if errors:
        print("Regression checks failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1 if args.strict else 0)

    print("Regression checks passed.")


if __name__ == "__main__":
    main()
