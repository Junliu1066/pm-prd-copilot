#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


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

    for stage in ordered_stages:
        run_stage(base_dir, args.project, stage)
    print(f"Pipeline completed for {args.project}: {', '.join(ordered_stages)}")


if __name__ == "__main__":
    main()
