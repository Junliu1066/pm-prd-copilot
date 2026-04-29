#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from common import CheckResult, read_json, write_json


def _latest_report(base_dir: Path) -> Path | None:
    reports = sorted((base_dir / "evals" / "real_outputs").glob("*/real_output_eval_report.json"))
    return reports[-1] if reports else None


def check_real_output_eval(
    base_dir: Path,
    project: str,
    *,
    run_id: str | None = None,
    write_report: bool = True,
) -> CheckResult:
    report_path = _latest_report(base_dir)
    if not report_path:
        return CheckResult("real_output_eval", "fail", "No real output evaluation report found.", [])

    report = read_json(report_path)
    status = str(report.get("status", "fail"))
    details: list[str] = []
    for case in report.get("cases", []):
        if case.get("status") != "pass":
            failed = [
                assertion.get("label", assertion.get("assertion", "unknown"))
                for assertion in case.get("assertions", [])
                if assertion.get("status") != "pass"
            ]
            details.append(f"{case.get('case_id')} failed: {', '.join(failed)}")

    effective_run_id = run_id or read_json(base_dir / "projects" / project / "project_state.json").get("last_run_id")
    if write_report and effective_run_id:
        write_json(
            base_dir / "projects" / project / "runs" / effective_run_id / "real_output_eval_status.json",
            {
                "run_id": effective_run_id,
                "project_id": project,
                "eval_run_id": report.get("run_id"),
                "status": status,
                "total_score": report.get("total_score"),
                "max_score": report.get("max_score"),
                "report_path": str(report_path.relative_to(base_dir)),
            },
        )

    if status != "pass":
        return CheckResult(
            "real_output_eval",
            "fail",
            f"Real output eval failed: {report.get('total_score')}/{report.get('max_score')}.",
            details,
        )
    return CheckResult(
        "real_output_eval",
        "pass",
        f"Real output eval passed: {report.get('total_score')}/{report.get('max_score')}.",
        [str(report_path.relative_to(base_dir))],
    )
