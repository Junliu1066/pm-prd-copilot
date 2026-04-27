#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from common import overall_status, read_json, write_json
from efficiency_auditor import audit_efficiency
from plugin_boundary_checker import check_plugin_boundaries
from registry_validator import validate_registry
from runtime_control_checker import check_runtime_controls
from random_audit_inspector import inspect_random_audit
from scaling_policy_checker import check_scaling_policy
from skill_update_proposal_checker import check_skill_update_proposals
from source_trace_checker import check_source_traces
from steward_contract_checker import check_steward_contracts
from teaching_absorption_checker import check_teaching_absorption
from workflow_gate_checker import check_workflow_gates


def ensure_project_state(base_dir: Path, project: str, run_id: str) -> dict:
    project_dir = base_dir / "projects" / project
    project_dir.mkdir(parents=True, exist_ok=True)
    state_path = project_dir / "project_state.json"
    state = read_json(state_path)
    if not state:
        state = {
            "project_id": project,
            "current_stage": "intake",
            "completed_stages": [],
            "approvals": [],
            "assumption_overrides": {},
        }
    state["last_run_id"] = run_id
    write_json(state_path, state)
    return state


def ensure_run_files(base_dir: Path, project: str, run_id: str) -> None:
    run_dir = base_dir / "projects" / project / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = run_dir / "manifest.json"
    trace_path = run_dir / "trace.json"
    if not manifest_path.exists():
        write_json(
            manifest_path,
            {
                "run_id": run_id,
                "project_id": project,
                "goal": "harness_validation",
                "enabled_skills": [],
                "enabled_mcps": [],
                "required_outputs": [],
            },
        )
    if not trace_path.exists():
        write_json(
            trace_path,
            {
                "run_id": run_id,
                "project_id": project,
                "skill_calls": [],
                "mcp_calls": [],
                "source_traces": [],
            },
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run PM Copilot governance harness.")
    parser.add_argument("--base-dir", default=".")
    parser.add_argument("--project", required=True)
    parser.add_argument("--run-id", default="")
    parser.add_argument("--mode", default="advisory", choices=["advisory", "strict"])
    parser.add_argument("--audit", action="store_true", help="Run risk-weighted random audit inspector.")
    parser.add_argument("--efficiency", action="store_true", help="Run efficiency steward audit.")
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    existing_state = read_json(base_dir / "projects" / args.project / "project_state.json")
    run_id = args.run_id or existing_state.get("last_run_id") or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    ensure_project_state(base_dir, args.project, run_id)
    ensure_run_files(base_dir, args.project, run_id)

    results = [
        validate_registry(base_dir),
        check_plugin_boundaries(base_dir),
        check_steward_contracts(base_dir, args.project),
        check_workflow_gates(base_dir, args.project),
        check_source_traces(base_dir, args.project),
        check_scaling_policy(base_dir),
        check_runtime_controls(base_dir, args.project),
        check_teaching_absorption(base_dir),
        check_skill_update_proposals(base_dir),
    ]
    if args.audit:
        results.append(inspect_random_audit(base_dir, args.project, run_id=run_id))
    if args.efficiency:
        results.append(audit_efficiency(base_dir, args.project, run_id=run_id))
    status = overall_status(results, args.mode)
    report = {
        "run_id": run_id,
        "project_id": args.project,
        "mode": args.mode,
        "status": status,
        "checks": [result.to_dict() for result in results],
    }
    report_path = base_dir / "projects" / args.project / "runs" / run_id / "harness_report.json"
    write_json(report_path, report)

    print(f"Harness status: {status}")
    for result in results:
        print(f"- {result.check}: {result.status} - {result.message}")
        for detail in result.details:
            print(f"  - {detail}")
    print(report_path)
    raise SystemExit(1 if status == "fail" else 0)


if __name__ == "__main__":
    main()
