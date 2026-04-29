#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from common import CheckResult, load_yaml, read_json, write_json


ARTIFACT_FILES = {
    "requirement_brief": "01_requirement_brief.md",
    "prd_markdown": "02_prd.generated.md",
    "user_stories": "03_user_stories.generated.md",
    "risk_report": "04_risk_check.generated.md",
    "tracking_plan": "05_tracking_plan.generated.md",
}

ARTIFACT_LIMIT_KEYS = {
    "requirement_brief": "requirement_brief_max_chars",
    "prd_markdown": "prd_markdown_max_chars",
    "user_stories": "user_stories_max_chars",
    "risk_report": "risk_report_max_chars",
    "tracking_plan": "tracking_plan_max_chars",
}


def _run_dir(base_dir: Path, project: str, run_id: str | None) -> tuple[str, Path]:
    project_dir = base_dir / "projects" / project
    state = read_json(project_dir / "project_state.json")
    effective_run_id = run_id or state.get("last_run_id") or "governance-baseline"
    return effective_run_id, project_dir / "runs" / effective_run_id


def _artifact_metrics(project_dir: Path, policy: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    artifact_limits = policy.get("artifact_limits", {})
    triggers = policy.get("optimization_triggers", {})
    repeated_threshold = int(triggers.get("repeated_line_threshold", 8))
    long_line_chars = int(triggers.get("long_line_chars", 500))
    metrics: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []

    for artifact, relative in ARTIFACT_FILES.items():
        path = project_dir / relative
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        chars = len(text)
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        repeated_lines = [
            line for line, count in Counter(lines).items() if count >= repeated_threshold and len(line) > 20
        ]
        long_lines = [line for line in lines if len(line) > long_line_chars]
        limit = artifact_limits.get(ARTIFACT_LIMIT_KEYS[artifact])
        metrics.append(
            {
                "artifact": artifact,
                "path": str(path),
                "chars": chars,
                "line_count": len(lines),
                "limit": limit,
                "repeated_line_count": len(repeated_lines),
                "long_line_count": len(long_lines),
            }
        )
        if triggers.get("empty_artifact_warn", True) and path.exists() and chars == 0:
            findings.append(
                {
                    "severity": "warn",
                    "type": "empty_artifact",
                    "artifact": artifact,
                    "evidence_path": str(path),
                    "responsible_steward": "prd-writing-steward",
                    "recommendation": "Regenerate or remove the empty artifact.",
                    "quality_risk": "high",
                }
            )
        if limit and chars > int(limit):
            findings.append(
                {
                    "severity": "warn",
                    "type": "oversized_artifact",
                    "artifact": artifact,
                    "chars": chars,
                    "threshold": int(limit),
                    "evidence_path": str(path),
                    "responsible_steward": "prd-writing-steward",
                    "recommendation": "Shorten the artifact or move detailed content to a supporting appendix.",
                    "quality_risk": "medium",
                }
            )
        if repeated_lines:
            findings.append(
                {
                    "severity": "warn",
                    "type": "repeated_output",
                    "artifact": artifact,
                    "repeated_line_count": len(repeated_lines),
                    "evidence_path": str(path),
                    "responsible_steward": "prd-writing-steward",
                    "recommendation": "Deduplicate repeated sections or convert repeated text into references.",
                    "quality_risk": "low",
                }
            )
        if long_lines:
            findings.append(
                {
                    "severity": "info",
                    "type": "long_line",
                    "artifact": artifact,
                    "long_line_count": len(long_lines),
                    "evidence_path": str(path),
                    "responsible_steward": "prd-writing-steward",
                    "recommendation": "Consider breaking long paragraphs into reviewable bullets.",
                    "quality_risk": "low",
                }
            )
    return metrics, findings


def audit_efficiency(
    base_dir: Path,
    project: str,
    *,
    run_id: str | None = None,
    write_report: bool = True,
) -> CheckResult:
    policy = load_yaml(base_dir / "governance" / "efficiency_policy.yaml")
    effective_run_id, run_dir = _run_dir(base_dir, project, run_id)
    project_dir = base_dir / "projects" / project
    manifest = read_json(run_dir / "manifest.json")
    trace = read_json(run_dir / "trace.json")
    run_limits = policy.get("run_limits", {})
    findings: list[dict[str, Any]] = []

    skill_call_count = len(trace.get("skill_calls", []))
    mcp_call_count = len(trace.get("mcp_calls", []))
    if skill_call_count > int(run_limits.get("max_skill_calls", 8)):
        findings.append(
            {
                "severity": "warn",
                "type": "too_many_skill_calls",
                "skill_call_count": skill_call_count,
                "threshold": int(run_limits.get("max_skill_calls", 8)),
                "responsible_steward": "pm-copilot-chief",
                "recommendation": "Split the workflow into staged runs or remove unnecessary skill calls.",
                "quality_risk": "medium",
            }
        )
    if mcp_call_count > int(run_limits.get("max_mcp_calls", 5)):
        findings.append(
            {
                "severity": "warn",
                "type": "too_many_mcp_calls",
                "mcp_call_count": mcp_call_count,
                "threshold": int(run_limits.get("max_mcp_calls", 5)),
                "responsible_steward": "research-steward",
                "recommendation": "Reduce external collection scope or batch source collection.",
                "quality_risk": "medium",
            }
        )

    artifact_metrics, artifact_findings = _artifact_metrics(project_dir, policy)
    findings.extend(artifact_findings)
    total_artifact_chars = sum(item["chars"] for item in artifact_metrics)
    if total_artifact_chars > int(run_limits.get("max_total_artifact_chars", 120000)):
        findings.append(
            {
                "severity": "warn",
                "type": "oversized_run_artifacts",
                "total_artifact_chars": total_artifact_chars,
                "threshold": int(run_limits.get("max_total_artifact_chars", 120000)),
                "responsible_steward": "pm-copilot-chief",
                "recommendation": "Move verbose sections into supporting artifacts and keep main PRD concise.",
                "quality_risk": "medium",
            }
        )

    status = "pass"
    if any(finding["severity"] in {"warn", "optimize", "escalate"} for finding in findings):
        status = "warn"

    report = {
        "run_id": effective_run_id,
        "project_id": project,
        "status": status,
        "skill_call_count": skill_call_count,
        "mcp_call_count": mcp_call_count,
        "manifest_enabled_skills": manifest.get("enabled_skills", []),
        "total_artifact_chars": total_artifact_chars,
        "artifact_metrics": artifact_metrics,
        "findings": findings,
    }
    if write_report:
        write_json(run_dir / "efficiency_report.json", report)

    details = [
        f"{finding['severity']}: {finding['type']} -> {finding.get('recommendation', '')}"
        for finding in findings
    ]
    if status == "pass":
        return CheckResult("efficiency", "pass", "No efficiency issues found.", [])
    return CheckResult("efficiency", "warn", f"{len(findings)} efficiency finding(s).", details)
