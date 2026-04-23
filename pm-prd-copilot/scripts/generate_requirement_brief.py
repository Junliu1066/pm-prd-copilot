#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from llm_stage_runner import run_stage_with_optional_llm
from prompt_builders import build_brief_schema, build_stage_prompt_bundle
from pipeline_common import (
    build_requirement_brief,
    project_paths,
    read_json,
    read_text,
    requirement_brief_markdown,
    validate_schema,
    write_json,
    write_text,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate requirement brief from raw input")
    parser.add_argument("--base-dir", default=".")
    parser.add_argument("--project", required=True)
    parser.add_argument("--mode", default="rule", choices=["rule", "llm", "auto"])
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    paths = project_paths(base_dir, args.project)
    raw_text = read_text(paths["raw_input"])
    seed = read_json(paths["brief_json"])
    prompt_bundle = build_stage_prompt_bundle(base_dir, "brief", project=args.project, raw_text=raw_text)
    brief, meta = run_stage_with_optional_llm(
        base_dir=base_dir,
        stage="brief",
        mode=args.mode,
        prompt_bundle=prompt_bundle,
        validator_schema=build_brief_schema(),
        rule_fallback=lambda: build_requirement_brief(args.project, raw_text, seed=seed),
    )
    errors = validate_schema(base_dir / "shared" / "schemas" / "requirement_brief.schema.json", brief)
    if errors:
        raise SystemExit(f"Requirement brief validation failed: {errors}")

    write_json(paths["brief_json"], brief)
    write_text(paths["brief_md"], requirement_brief_markdown(brief))
    write_text(paths["brief_meta"], json.dumps(meta, ensure_ascii=False, indent=2))
    print(paths["brief_json"])
    print(paths["brief_md"])


if __name__ == "__main__":
    main()
