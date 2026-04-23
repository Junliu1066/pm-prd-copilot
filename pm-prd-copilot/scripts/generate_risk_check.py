#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from llm_stage_runner import run_stage_with_optional_llm
from prompt_builders import build_risk_schema, build_stage_prompt_bundle
from pipeline_common import (
    build_risk_report,
    project_paths,
    read_json,
    risk_report_markdown,
    write_json,
    write_text,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate risk check from PRD and requirement brief")
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

    prompt_bundle = build_stage_prompt_bundle(base_dir, "risk", project=args.project, brief=brief, prd=prd)
    report, meta = run_stage_with_optional_llm(
        base_dir=base_dir,
        stage="risk",
        mode=args.mode,
        prompt_bundle=prompt_bundle,
        validator_schema=build_risk_schema(),
        rule_fallback=lambda: build_risk_report(prd, brief),
    )
    write_json(paths["risk_json"], report)
    write_text(paths["risk_md"], risk_report_markdown(report))
    write_text(paths["risk_meta"], json.dumps(meta, ensure_ascii=False, indent=2))
    print(paths["risk_json"])
    print(paths["risk_md"])


if __name__ == "__main__":
    main()
