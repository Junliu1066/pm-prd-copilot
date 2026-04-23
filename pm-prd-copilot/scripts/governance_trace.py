#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_TRACE = {
    "brief": {
        "action": "normalize_requirement",
        "skill": "source-collector",
        "steward": "research-steward",
        "inputs": ["raw_input"],
        "outputs": ["source_brief", "source_brief_markdown"],
    },
    "prd": {
        "action": "draft_prd",
        "skill": "prd-draft-writer",
        "steward": "prd-writing-steward",
        "inputs": ["source_brief"],
        "outputs": ["prd_document", "prd_markdown"],
    },
    "stories": {
        "action": "write_user_stories",
        "skill": "user-story-ac-generator",
        "steward": "prd-writing-steward",
        "inputs": ["source_brief", "prd_document"],
        "outputs": ["user_stories"],
    },
    "risk": {
        "action": "check_risks_edgecases",
        "skill": "risk-edgecase-checker",
        "steward": "review-steward",
        "inputs": ["source_brief", "prd_document"],
        "outputs": ["risk_report"],
    },
    "tracking": {
        "action": "design_tracking_plan",
        "skill": "tracking-plan-designer",
        "steward": "prd-writing-steward",
        "inputs": ["source_brief", "prd_document"],
        "outputs": ["tracking_plan"],
    },
}


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def init_governance_run(base_dir: Path, project: str, run_id: str, mode: str, stages: list[str]) -> Path:
    project_dir = base_dir / "projects" / project
    run_dir = project_dir / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    enabled_skills = [STAGE_TRACE[stage]["skill"] for stage in stages]
    required_outputs: list[str] = []
    for stage in stages:
        required_outputs.extend(STAGE_TRACE[stage]["outputs"])

    manifest = {
        "run_id": run_id,
        "project_id": project,
        "goal": "production_pipeline",
        "mode": mode,
        "ordered_stages": stages,
        "enabled_skills": enabled_skills,
        "enabled_mcps": [],
        "required_outputs": required_outputs,
        "created_at": utc_now(),
    }
    trace = {
        "run_id": run_id,
        "project_id": project,
        "mode": mode,
        "skill_calls": [],
        "mcp_calls": [],
        "source_traces": [],
        "started_at": utc_now(),
    }
    write_json(run_dir / "manifest.json", manifest)
    write_json(run_dir / "trace.json", trace)

    state_path = project_dir / "project_state.json"
    state = read_json(state_path) or {
        "project_id": project,
        "current_stage": "intake",
        "completed_stages": [],
        "approvals": [],
        "assumption_overrides": {},
    }
    state["last_run_id"] = run_id
    state["last_pipeline_mode"] = mode
    state["last_pipeline_stages"] = stages
    write_json(state_path, state)
    return run_dir


def record_stage_call(run_dir: Path, stage: str, *, status: str = "completed") -> None:
    trace_path = run_dir / "trace.json"
    trace = read_json(trace_path)
    stage_trace = STAGE_TRACE[stage]
    trace.setdefault("skill_calls", []).append(
        {
            "stage": stage,
            "action": stage_trace["action"],
            "skill": stage_trace["skill"],
            "steward": stage_trace["steward"],
            "inputs": stage_trace["inputs"],
            "outputs": stage_trace["outputs"],
            "status": status,
            "completed_at": utc_now(),
        }
    )
    write_json(trace_path, trace)


def finalize_governance_run(run_dir: Path, *, status: str) -> None:
    trace_path = run_dir / "trace.json"
    trace = read_json(trace_path)
    trace["status"] = status
    trace["completed_at"] = utc_now()
    write_json(trace_path, trace)

    manifest_path = run_dir / "manifest.json"
    manifest = read_json(manifest_path)
    manifest["status"] = status
    manifest["completed_at"] = trace["completed_at"]
    write_json(manifest_path, manifest)
