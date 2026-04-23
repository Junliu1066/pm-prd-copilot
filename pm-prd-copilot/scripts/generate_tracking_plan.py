#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from llm_stage_runner import run_stage_with_optional_llm
from prompt_builders import build_stage_prompt_bundle, build_tracking_schema
from pipeline_common import (
    build_tracking_plan,
    project_paths,
    read_json,
    tracking_plan_markdown,
    validate_schema,
    write_json,
    write_text,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate tracking plan from PRD and requirement brief")
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

    prompt_bundle = build_stage_prompt_bundle(base_dir, "tracking", project=args.project, brief=brief, prd=prd)
    plan, meta = run_stage_with_optional_llm(
        base_dir=base_dir,
        stage="tracking",
        mode=args.mode,
        prompt_bundle=prompt_bundle,
        validator_schema=build_tracking_schema(),
        rule_fallback=lambda: build_tracking_plan(prd, brief),
    )
    if isinstance(plan, dict):
        for event in plan.get("events", []):
            if "event_properties" in event and "properties" not in event:
                event["properties"] = event.pop("event_properties")
    errors = validate_schema(base_dir / "shared" / "schemas" / "tracking_plan.schema.json", plan)
    if errors:
        raise SystemExit(f"Tracking plan validation failed: {errors}")

    write_json(paths["tracking_json"], plan)
    write_text(paths["tracking_md"], tracking_plan_markdown(plan, brief))
    write_text(paths["tracking_meta"], json.dumps(meta, ensure_ascii=False, indent=2))
    print(paths["tracking_json"])
    print(paths["tracking_md"])


if __name__ == "__main__":
    main()
