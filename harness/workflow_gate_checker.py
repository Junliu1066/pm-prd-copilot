#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from common import CheckResult, load_yaml, read_json, result_from_issues


def check_workflow_gates(base_dir: Path, project: str) -> CheckResult:
    issues: list[str] = []
    workflow = load_yaml(base_dir / "workflow" / "prd_workflow.yaml").get("stages", {})
    state = read_json(base_dir / "projects" / project / "project_state.json")
    current_stage = state.get("current_stage", "intake")
    completed = set(state.get("completed_stages", []))
    approvals = set(state.get("approvals", []))

    if current_stage not in workflow and current_stage != "done":
        issues.append(f"Unknown current_stage: {current_stage}")
        return result_from_issues("workflow_gate", issues, warn_only=True)

    for stage_name, stage in workflow.items():
        if stage_name not in completed:
            continue
        for approval in stage.get("approval_required", []) or []:
            if approval not in approvals and not state.get("assumption_overrides", {}).get(approval):
                issues.append(f"Completed stage {stage_name} without approval or assumption override: {approval}")

    if current_stage in {"prd_drafting", "review", "learning"}:
        for required_stage in ["intake", "user_analysis", "scenario_priority", "mvp_scope", "prd_planning"]:
            if required_stage not in completed:
                issues.append(f"Current stage {current_stage} requires completed stage: {required_stage}")

    return result_from_issues("workflow_gate", issues, warn_only=True)
