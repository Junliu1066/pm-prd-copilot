#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from governance_trace import finalize_governance_run, init_governance_run, record_stage_call


STAGE_TO_SCRIPT = {
    "brief": "generate_requirement_brief.py",
    "prd": "generate_prd.py",
    "stories": "generate_user_stories.py",
    "risk": "generate_risk_check.py",
    "tracking": "generate_tracking_plan.py",
}

CURRENT_MODE = "rule"

def run_stage(base_dir: Path, project: str, stage: str) -> None:
    script = base_dir / "pm-prd-copilot" / "scripts" / STAGE_TO_SCRIPT[stage]
    subprocess.run(
        [
            sys.executable,
            str(script),
            "--base-dir",
            str(base_dir),
            "--project",
            project,
            "--mode",
            CURRENT_MODE,
        ],
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the PM Copilot production pipeline")
    parser.add_argument("--base-dir", default=".")
    parser.add_argument("--project", required=True)
    parser.add_argument(
        "--stage",
        default="all",
        choices=["all", "brief", "prd", "stories", "risk", "tracking"],
    )
    parser.add_argument("--mode", default="rule", choices=["rule", "llm", "auto"])
    parser.add_argument(
        "--run-id",
        default="pipeline-latest",
        help="Governance run id used for manifest/trace output.",
    )
    parser.add_argument("--no-trace", action="store_true", help="Disable governance manifest/trace output.")
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    global CURRENT_MODE
    CURRENT_MODE = args.mode
    if args.stage == "all":
        ordered_stages = ["brief", "prd", "stories", "risk", "tracking"]
    elif args.stage == "brief":
        ordered_stages = ["brief"]
    elif args.stage == "prd":
        ordered_stages = ["brief", "prd"]
    elif args.stage == "stories":
        ordered_stages = ["brief", "prd", "stories"]
    elif args.stage == "risk":
        ordered_stages = ["brief", "prd", "risk"]
    else:
        ordered_stages = ["brief", "prd", "tracking"]

    run_dir = None
    if not args.no_trace:
        run_dir = init_governance_run(base_dir, args.project, args.run_id, args.mode, ordered_stages)

    try:
        for stage in ordered_stages:
            run_stage(base_dir, args.project, stage)
            if run_dir is not None:
                record_stage_call(run_dir, stage)
        if run_dir is not None:
            finalize_governance_run(run_dir, status="completed")
    except Exception:
        if run_dir is not None:
            finalize_governance_run(run_dir, status="failed")
        raise
    print(f"Pipeline completed for {args.project}: {', '.join(ordered_stages)}")


if __name__ == "__main__":
    main()
