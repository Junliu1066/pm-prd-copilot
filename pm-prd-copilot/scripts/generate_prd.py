#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from llm_stage_runner import run_stage_with_optional_llm
from prompt_builders import build_prd_schema, build_stage_prompt_bundle
from pipeline_common import (
    brief_to_prd,
    prd_markdown,
    project_paths,
    read_json,
    validate_schema,
    write_json,
    write_text,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate PRD draft from requirement brief")
    parser.add_argument("--base-dir", default=".")
    parser.add_argument("--project", required=True)
    parser.add_argument("--mode", default="rule", choices=["rule", "llm", "auto"])
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    paths = project_paths(base_dir, args.project)
    brief = read_json(paths["brief_json"])
    if not brief:
        raise SystemExit(f"Missing requirement brief: {paths['brief_json']}")

    prompt_bundle = build_stage_prompt_bundle(base_dir, "prd", project=args.project, brief=brief)
    prd, meta = run_stage_with_optional_llm(
        base_dir=base_dir,
        stage="prd",
        mode=args.mode,
        prompt_bundle=prompt_bundle,
        validator_schema=build_prd_schema(),
        rule_fallback=lambda: brief_to_prd(brief),
    )
    errors = validate_schema(base_dir / "shared" / "schemas" / "prd_document.schema.json", prd)
    if errors:
        raise SystemExit(f"PRD validation failed: {errors}")

    write_json(paths["prd_json"], prd)
    write_text(paths["prd_md"], prd_markdown(prd, brief))
    write_text(paths["prd_meta"], json.dumps(meta, ensure_ascii=False, indent=2))
    print(paths["prd_json"])
    print(paths["prd_md"])


if __name__ == "__main__":
    main()
