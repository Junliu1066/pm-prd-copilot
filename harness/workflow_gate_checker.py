#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from common import CheckResult, load_yaml, read_json, result_from_issues


def stage_actions_from_trace(trace: dict) -> dict[str, str]:
    stage_actions: dict[str, str] = {}
    for call in trace.get("skill_calls", []) or []:
        stage = call.get("stage")
        action = call.get("action")
        if isinstance(stage, str) and isinstance(action, str):
            stage_actions[stage] = action
    return stage_actions


def approvals_required_for_pipeline(
    workflow: dict,
    actions: dict,
    pipeline_stages: list[str],
    stage_actions: dict[str, str],
    issues: list[str],
) -> list[str]:
    stage_order = list(workflow.keys())
    required: list[str] = []
    for pipeline_stage in pipeline_stages:
        action_name = stage_actions.get(pipeline_stage)
        if not action_name:
            issues.append(f"Production pipeline stage {pipeline_stage} is missing a declared workflow action.")
            continue
        workflow_stage = actions.get(action_name, {}).get("stage")
        if workflow_stage not in workflow:
            issues.append(
                f"Production pipeline stage {pipeline_stage} declares action {action_name}, "
                "but that action is not registered in workflow."
            )
            continue
        for stage_name in stage_order[: stage_order.index(workflow_stage)]:
            for approval in workflow[stage_name].get("approval_required", []) or []:
                if approval not in required:
                    required.append(approval)
    return required


def check_workflow_gates(base_dir: Path, project: str) -> CheckResult:
    issues: list[str] = []
    workflow = load_yaml(base_dir / "workflow" / "prd_workflow.yaml").get("stages", {})
    actions = load_yaml(base_dir / "workflow" / "actions.yaml").get("actions", {})
    skills = load_yaml(base_dir / "registry" / "skills.yaml").get("skills", {})
    artifacts = load_yaml(base_dir / "registry" / "artifacts.yaml").get("artifacts", {})
    stewards_doc = load_yaml(base_dir / "registry" / "stewards.yaml")
    state = read_json(base_dir / "projects" / project / "project_state.json")
    run_id = state.get("last_run_id")
    manifest = read_json(base_dir / "projects" / project / "runs" / run_id / "manifest.json") if run_id else {}
    trace = read_json(base_dir / "projects" / project / "runs" / run_id / "trace.json") if run_id else {}
    current_stage = state.get("current_stage", "intake")
    completed = set(state.get("completed_stages", []))
    approvals = set(state.get("approvals", []))
    known_artifacts = set(artifacts.keys())
    known_stewards = {
        **stewards_doc.get("chief_stewards", {}),
        **stewards_doc.get("sub_stewards", {}),
    }
    output_producers: dict[str, list[str]] = {}
    for action_name, action in actions.items():
        for artifact in action.get("outputs", []) or []:
            output_producers.setdefault(artifact, []).append(action_name)
    for artifact, producers in sorted(output_producers.items()):
        if len(producers) > 1:
            issues.append(
                f"Artifact {artifact} has multiple workflow action producers: {', '.join(producers)}. "
                "Split the artifact contract or make ownership explicit."
            )

    for stage_name, stage in workflow.items():
        for action_name in stage.get("allowed_actions", []) or []:
            action = actions.get(action_name)
            if not action:
                issues.append(f"Workflow stage {stage_name} references unknown action: {action_name}")
                continue
            if action.get("stage") != stage_name:
                issues.append(
                    f"Workflow action {action_name} has stage {action.get('stage')}, expected {stage_name}"
                )
            steward_id = action.get("steward")
            steward = known_stewards.get(steward_id)
            if not steward:
                issues.append(f"Workflow action {action_name} references unknown steward: {steward_id}")
            elif stage_name not in set(steward.get("allowed_stages", [])):
                issues.append(f"Workflow action {action_name} uses steward {steward_id} outside allowed stage: {stage_name}")
            skill_id = action.get("skill")
            skill = skills.get(skill_id)
            if not skill:
                issues.append(f"Workflow action {action_name} references unknown skill: {skill_id}")
                continue
            if action.get("steward") != skill.get("steward"):
                issues.append(
                    f"Workflow action {action_name} steward {action.get('steward')} does not match skill {skill_id} steward {skill.get('steward')}"
                )
            declared_reads = set(skill.get("reads", []))
            declared_writes = set(skill.get("writes", []))
            for artifact in action.get("inputs", []) or []:
                if artifact not in known_artifacts and not artifact.endswith("_signals") and artifact not in declared_reads:
                    issues.append(f"Workflow action {action_name} reads unknown artifact: {artifact}")
                if artifact not in declared_reads:
                    issues.append(f"Workflow action {action_name} reads undeclared skill artifact: {artifact}")
            for artifact in action.get("outputs", []) or []:
                if artifact not in known_artifacts and not artifact.endswith("_signals"):
                    issues.append(f"Workflow action {action_name} writes unknown artifact: {artifact}")
                artifact_owner_stage = artifacts.get(artifact, {}).get("owner_stage")
                if artifact_owner_stage and artifact_owner_stage != stage_name:
                    issues.append(
                        f"Workflow action {action_name} writes artifact {artifact} owned by stage "
                        f"{artifact_owner_stage}, expected {stage_name}."
                    )
                if artifact not in declared_writes:
                    issues.append(f"Workflow action {action_name} writes undeclared skill artifact: {artifact}")

    for action_name, action in actions.items():
        stage_name = action.get("stage")
        if stage_name in workflow and action_name not in set(workflow[stage_name].get("allowed_actions", []) or []):
            issues.append(f"Action {action_name} is registered for stage {stage_name} but is not allowed by workflow.")

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

    pipeline_stages = manifest.get("ordered_stages") or state.get("last_pipeline_stages", [])
    if manifest.get("goal") == "production_pipeline" and pipeline_stages:
        stage_actions = manifest.get("stage_actions", {})
        if not isinstance(stage_actions, dict):
            stage_actions = {}
        stage_actions = {**stage_actions_from_trace(trace), **stage_actions}
        required_approvals = approvals_required_for_pipeline(
            workflow,
            actions,
            pipeline_stages,
            stage_actions,
            issues,
        )
        governance_mode = manifest.get("governance_mode")
        if (
            required_approvals
            and manifest.get("approval_gate_enforced") is not True
            and governance_mode != "fast_draft"
        ):
            issues.append(
                "Production pipeline run reached approval-gated workflow stages without enforced approval gates. "
                "Use the governed default path, or run `--fast-draft` only for explicitly labeled draft output."
            )
        declared_required = set(manifest.get("required_approvals", []))
        missing_declarations = [
            approval for approval in required_approvals if approval not in declared_required
        ]
        if missing_declarations:
            issues.append(
                "Production pipeline manifest missing required approval declarations: "
                + ", ".join(missing_declarations)
            )

    return result_from_issues("workflow_gate", issues, warn_only=True)
