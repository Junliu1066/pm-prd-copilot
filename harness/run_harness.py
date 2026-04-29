#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from agentic_delivery_checker import check_agentic_delivery
from ai_solution_checker import check_ai_solution
from common import overall_status, read_json, write_json
from delivery_plan_checker import check_delivery_plan
from efficiency_auditor import audit_efficiency
from eval_suite_checker import check_eval_suite
from external_redaction_checker import check_external_redaction
from preference_cache_checker import check_preference_caches
from plugin_boundary_checker import check_plugin_boundaries
from prototype_preview_gate_checker import check_prototype_preview_gate
from real_output_eval_checker import check_real_output_eval
from registry_validator import validate_registry
from random_audit_inspector import inspect_random_audit
from scaling_policy_checker import check_scaling_policy
from skill_generalization_checker import check_skill_generalization
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
    parser.add_argument("--check-only", action="store_true", help="Run checks without writing project state or reports.")
    parser.add_argument("--write-report", action="store_true", help="Allow report/state writes and print written paths.")
    parser.add_argument("--audit", action="store_true", help="Run risk-weighted random audit inspector.")
    parser.add_argument("--efficiency", action="store_true", help="Run efficiency steward audit.")
    parser.add_argument(
        "--external-package",
        default="",
        help="Optional B-package file or directory to scan for protected framework leakage.",
    )
    args = parser.parse_args()

    if args.check_only and args.write_report:
        parser.error("--check-only and --write-report are mutually exclusive.")

    base_dir = Path(args.base_dir).resolve()
    existing_state = read_json(base_dir / "projects" / args.project / "project_state.json")
    run_id = args.run_id or existing_state.get("last_run_id") or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    write_report = bool(args.write_report)
    check_only = args.check_only or not write_report
    written_paths: list[Path] = []
    if write_report:
        ensure_project_state(base_dir, args.project, run_id)
        ensure_run_files(base_dir, args.project, run_id)
        run_dir = base_dir / "projects" / args.project / "runs" / run_id
        written_paths.extend(
            [
                base_dir / "projects" / args.project / "project_state.json",
                run_dir / "manifest.json",
                run_dir / "trace.json",
            ]
        )

    results = [
        validate_registry(base_dir),
        check_plugin_boundaries(base_dir),
        check_steward_contracts(base_dir, args.project),
        check_workflow_gates(base_dir, args.project),
        check_source_traces(base_dir, args.project),
        check_prototype_preview_gate(base_dir, args.project),
        check_preference_caches(base_dir),
        check_delivery_plan(base_dir, args.project, run_id=run_id),
        check_ai_solution(base_dir, args.project, run_id=run_id),
        check_agentic_delivery(base_dir, args.project, run_id=run_id),
        check_eval_suite(base_dir, args.project, run_id=run_id, write_report=write_report),
        check_real_output_eval(base_dir, args.project, run_id=run_id, write_report=write_report),
        check_skill_generalization(base_dir, args.project, run_id=run_id, write_report=write_report),
        check_scaling_policy(base_dir),
        check_teaching_absorption(base_dir),
        check_skill_update_proposals(base_dir),
    ]
    if args.audit:
        results.append(inspect_random_audit(base_dir, args.project, run_id=run_id, write_report=write_report))
    if args.efficiency:
        results.append(audit_efficiency(base_dir, args.project, run_id=run_id, write_report=write_report))
    if args.external_package:
        results.append(check_external_redaction(base_dir, Path(args.external_package)))
    status = overall_status(results, args.mode)
    report = {
        "run_id": run_id,
        "project_id": args.project,
        "mode": args.mode,
        "check_only": check_only,
        "write_report": write_report,
        "status": status,
        "checks": [result.to_dict() for result in results],
    }
    report_path = base_dir / "projects" / args.project / "runs" / run_id / "harness_report.json"
    if write_report:
        write_json(report_path, report)
        written_paths.append(report_path)
        run_dir = base_dir / "projects" / args.project / "runs" / run_id
        written_paths.extend(
            [
                run_dir / "eval_suite_report.json",
                run_dir / "real_output_eval_status.json",
                run_dir / "skill_generalization_audit.json",
            ]
        )
        if args.audit:
            written_paths.append(run_dir / "random_audit_report.json")
        if args.efficiency:
            written_paths.append(run_dir / "efficiency_report.json")

    print(f"Harness status: {status}")
    print(f"Harness mode: {'check-only' if check_only else 'write-report'}")
    for result in results:
        print(f"- {result.check}: {result.status} - {result.message}")
        for detail in result.details:
            print(f"  - {detail}")
    if write_report:
        print("Written paths:")
        for path in written_paths:
            print(path)
    else:
        print("No project files written. Use --write-report to refresh harness reports.")
    raise SystemExit(1 if status == "fail" else 0)


if __name__ == "__main__":
    main()
