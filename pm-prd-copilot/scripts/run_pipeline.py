#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

from governance_trace import STAGE_TRACE, finalize_governance_run, init_governance_run, record_stage_call


STAGE_TO_SCRIPT = {
    "brief": "generate_requirement_brief.py",
    "prd": "generate_prd.py",
    "stories": "generate_user_stories.py",
    "risk": "generate_risk_check.py",
    "tracking": "generate_tracking_plan.py",
}

CURRENT_MODE = "rule"


class GovernanceGateError(RuntimeError):
    pass


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def read_project_state(base_dir: Path, project: str) -> dict:
    state_path = base_dir / "projects" / project / "project_state.json"
    if not state_path.exists():
        return {}
    return load_json(state_path)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return data


def approvals_required_for_pipeline(base_dir: Path, pipeline_stages: list[str]) -> list[str]:
    workflow = load_yaml(base_dir / "workflow" / "prd_workflow.yaml").get("stages", {})
    actions = load_yaml(base_dir / "workflow" / "actions.yaml").get("actions", {})
    if not workflow:
        return []

    stage_order = list(workflow.keys())
    required: list[str] = []
    for pipeline_stage in pipeline_stages:
        stage_trace = STAGE_TRACE.get(pipeline_stage)
        if not stage_trace:
            raise GovernanceGateError(f"Pipeline stage {pipeline_stage} is missing from STAGE_TRACE.")
        action_name = stage_trace["action"]
        workflow_stage = actions.get(action_name, {}).get("stage")
        if workflow_stage not in workflow:
            raise GovernanceGateError(
                f"Pipeline stage {pipeline_stage} action {action_name} is not registered in workflow."
            )
        for stage_name in stage_order[: stage_order.index(workflow_stage)]:
            for approval in workflow[stage_name].get("approval_required", []) or []:
                if approval not in required:
                    required.append(approval)
    return required


def enforce_governance_gate(base_dir: Path, project: str, pipeline_stages: list[str]) -> list[str]:
    required = approvals_required_for_pipeline(base_dir, pipeline_stages)
    state = read_project_state(base_dir, project)
    approvals = set(state.get("approvals", []))
    overrides = state.get("assumption_overrides", {})
    pipeline_overrides = state.get("pipeline_assumption_overrides", {})
    missing = [
        approval
        for approval in required
        if approval not in approvals
        and not overrides.get(approval)
        and not pipeline_overrides.get(approval)
    ]
    if missing:
        missing_text = ", ".join(missing)
        raise GovernanceGateError(
            "Governed pipeline blocked: missing approval, assumption override, "
            f"or pipeline assumption override for {missing_text}."
        )
    return required


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
    parser.add_argument(
        "--governed",
        action="store_true",
        help="Compatibility flag. Approval gates are enforced by default unless --fast-draft is used.",
    )
    parser.add_argument(
        "--fast-draft",
        action="store_true",
        help="Explicitly run the labeled fast draft path without enforcing workflow approval gates.",
    )
    parser.add_argument("--no-trace", action="store_true", help="Disable governance manifest/trace output.")
    args = parser.parse_args()
    if args.fast_draft and args.governed:
        parser.error("--fast-draft and --governed are mutually exclusive.")

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

    enforce_gates = not args.fast_draft
    governance_mode = "governed" if enforce_gates else "fast_draft"
    required_approvals = approvals_required_for_pipeline(base_dir, ordered_stages)
    if enforce_gates:
        try:
            required_approvals = enforce_governance_gate(base_dir, args.project, ordered_stages)
        except GovernanceGateError as error:
            raise SystemExit(str(error)) from error

    run_dir = None
    if not args.no_trace:
        run_dir = init_governance_run(
            base_dir,
            args.project,
            args.run_id,
            args.mode,
            ordered_stages,
            approval_gate_enforced=enforce_gates,
            required_approvals=required_approvals,
            governance_mode=governance_mode,
        )

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
