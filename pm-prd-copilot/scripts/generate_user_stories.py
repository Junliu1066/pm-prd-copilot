#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from llm_stage_runner import run_stage_with_optional_llm
from prompt_builders import build_stage_prompt_bundle, build_user_stories_schema
from pipeline_common import (
    normalize_user_stories,
    prd_to_user_stories,
    project_paths,
    read_json,
    user_stories_markdown,
    validate_schema,
    write_json,
    write_text,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate user stories from PRD")
    parser.add_argument("--base-dir", default=".")
    parser.add_argument("--project", required=True)
    parser.add_argument("--mode", default="rule", choices=["rule", "llm", "auto"])
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    paths = project_paths(base_dir, args.project)
    brief = read_json(paths["brief_json"])
    prd = read_json(paths["prd_json"])
    if not brief or not prd:
        raise SystemExit("Missing brief or PRD input.")

    prompt_bundle = build_stage_prompt_bundle(base_dir, "stories", project=args.project, brief=brief, prd=prd)
    stories, meta = run_stage_with_optional_llm(
        base_dir=base_dir,
        stage="stories",
        mode=args.mode,
        prompt_bundle=prompt_bundle,
        validator_schema=build_user_stories_schema() if args.mode == "rule" else prompt_bundle["schema"],
        rule_fallback=lambda: prd_to_user_stories(prd, brief),
    )
    if isinstance(stories, dict) and "stories" in stories:
        stories = stories["stories"]
    stories = normalize_user_stories(stories)
    schema_path = base_dir / "shared" / "schemas" / "user_story.schema.json"
    errors = []
    for story in stories:
        errors.extend(validate_schema(schema_path, story))
    if errors:
        raise SystemExit(f"User story validation failed: {errors}")

    write_json(paths["stories_json"], stories)
    write_text(paths["stories_md"], user_stories_markdown(stories, brief))
    write_text(paths["stories_meta"], json.dumps(meta, ensure_ascii=False, indent=2))
    print(paths["stories_json"])
    print(paths["stories_md"])


if __name__ == "__main__":
    main()
