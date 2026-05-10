#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import CheckResult, load_yaml, read_json, write_json


REPORT_VERSION = "efficiency.v2"

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

FINGERPRINT_ARTIFACT_FILES = {
    **ARTIFACT_FILES,
    "prd_context_digest": "analysis/prd_context_digest.json",
}

FINGERPRINT_FIELDS = [
    "source_manifest_hash",
    "source_trace_hash",
    "artifact_hashes",
    "meta_hashes",
    "policy_hash",
    "skills_registry_hash",
]


def _hash_file(path: Path) -> str:
    if not path.exists():
        return "missing"
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _current_fingerprints(base_dir: Path, project_dir: Path, run_dir: Path) -> dict[str, Any]:
    return {
        "source_manifest_hash": _hash_file(run_dir / "manifest.json"),
        "source_trace_hash": _hash_file(run_dir / "trace.json"),
        "artifact_hashes": {
            artifact: _hash_file(project_dir / relative)
            for artifact, relative in sorted(FINGERPRINT_ARTIFACT_FILES.items())
        },
        "meta_hashes": {
            path.name: _hash_file(path)
            for path in sorted(project_dir.glob("*.meta.json"))
        },
        "policy_hash": _hash_file(base_dir / "governance" / "efficiency_policy.yaml"),
        "skills_registry_hash": _hash_file(base_dir / "registry" / "skills.yaml"),
    }


def _report_trust_status(report: dict[str, Any], fingerprints: dict[str, Any]) -> dict[str, Any]:
    if not report:
        return {
            "status": "missing",
            "trusted": False,
            "reasons": ["efficiency_report_missing"],
        }
    missing_fields = [
        field
        for field in ["report_version", *FINGERPRINT_FIELDS]
        if field not in report
    ]
    if missing_fields:
        return {
            "status": "legacy_stale",
            "trusted": False,
            "reasons": [f"missing_field:{field}" for field in missing_fields],
        }
    if report.get("report_version") != REPORT_VERSION:
        return {
            "status": "legacy_stale",
            "trusted": False,
            "reasons": [f"report_version:{report.get('report_version')}"],
        }
    changed_fields = [
        field
        for field in FINGERPRINT_FIELDS
        if report.get(field) != fingerprints.get(field)
    ]
    if changed_fields:
        return {
            "status": "stale",
            "trusted": False,
            "reasons": [f"changed:{field}" for field in changed_fields],
        }
    return {"status": "fresh", "trusted": True, "reasons": []}


def _as_int(value: Any) -> int:
    return value if isinstance(value, int) else 0


def _token_meta_metrics(project_dir: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    metrics: list[dict[str, Any]] = []
    for path in sorted(project_dir.glob("*.meta.json")):
        meta = read_json(path)
        if not isinstance(meta, dict):
            continue
        usage = meta.get("usage", {})
        if not isinstance(usage, dict):
            usage = {}
        input_details = usage.get("input_tokens_details", {})
        if not isinstance(input_details, dict):
            input_details = {}
        output_details = usage.get("output_tokens_details", {})
        if not isinstance(output_details, dict):
            output_details = {}
        metrics.append(
            {
                "meta_file": path.name,
                "stage": meta.get("stage") or path.name.removesuffix(".meta.json"),
                "model": meta.get("model", "unknown"),
                "input_tokens": _as_int(usage.get("input_tokens")),
                "cached_tokens": _as_int(input_details.get("cached_tokens")),
                "output_tokens": _as_int(usage.get("output_tokens")),
                "reasoning_tokens": _as_int(output_details.get("reasoning_tokens")),
                "total_tokens": _as_int(usage.get("total_tokens")),
                "attempt": _as_int(meta.get("attempt")) or 1,
                "status": meta.get("status", "unknown"),
            }
        )

    totals = {
        "meta_file_count": len(metrics),
        "models": sorted({item["model"] for item in metrics if item.get("model")}),
        "stages": sorted({item["stage"] for item in metrics if item.get("stage")}),
        "input_tokens": sum(item["input_tokens"] for item in metrics),
        "cached_tokens": sum(item["cached_tokens"] for item in metrics),
        "output_tokens": sum(item["output_tokens"] for item in metrics),
        "reasoning_tokens": sum(item["reasoning_tokens"] for item in metrics),
        "total_tokens": sum(item["total_tokens"] for item in metrics),
        "retry_count": sum(max(item["attempt"] - 1, 0) for item in metrics),
    }

    by_stage: dict[str, dict[str, Any]] = {}
    for item in metrics:
        stage = item["stage"]
        stage_metric = by_stage.setdefault(
            stage,
            {
                "stage": stage,
                "meta_file_count": 0,
                "models": set(),
                "input_tokens": 0,
                "cached_tokens": 0,
                "output_tokens": 0,
                "reasoning_tokens": 0,
                "total_tokens": 0,
                "retry_count": 0,
                "max_attempt": 0,
            },
        )
        stage_metric["meta_file_count"] += 1
        stage_metric["models"].add(item["model"])
        stage_metric["input_tokens"] += item["input_tokens"]
        stage_metric["cached_tokens"] += item["cached_tokens"]
        stage_metric["output_tokens"] += item["output_tokens"]
        stage_metric["reasoning_tokens"] += item["reasoning_tokens"]
        stage_metric["total_tokens"] += item["total_tokens"]
        stage_metric["retry_count"] += max(item["attempt"] - 1, 0)
        stage_metric["max_attempt"] = max(stage_metric["max_attempt"], item["attempt"])

    stage_metrics = []
    for stage_metric in by_stage.values():
        stage_metrics.append({**stage_metric, "models": sorted(stage_metric["models"])})
    stage_metrics.sort(key=lambda item: item["stage"])
    return totals, stage_metrics, metrics


def _finding(
    *,
    severity: str,
    type: str,
    waste_type: str,
    evidence: str,
    value_level: str,
    disposition: str,
    action_target: str,
    owner: str,
    recommendation: str,
    quality_risk: str,
    retest_required: bool,
    rollback_condition: str,
    **extra: Any,
) -> dict[str, Any]:
    payload = {
        "severity": severity,
        "type": type,
        "waste_type": waste_type,
        "evidence": evidence,
        "value_level": value_level,
        "disposition": disposition,
        "action_target": action_target,
        "owner": owner,
        "responsible_steward": owner,
        "recommendation": recommendation,
        "quality_risk": quality_risk,
        "retest_required": retest_required,
        "rollback_condition": rollback_condition,
    }
    payload.update(extra)
    return payload


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
                _finding(
                    severity="warn",
                    type="empty_artifact",
                    waste_type="artifact_gap",
                    evidence=str(path),
                    value_level="unknown",
                    disposition="gate",
                    action_target=artifact,
                    owner="prd-writing-steward",
                    recommendation="Regenerate or remove the empty artifact.",
                    quality_risk="high",
                    retest_required=True,
                    rollback_condition="If regeneration removes required evidence or downstream inputs, restore the previous artifact and escalate to review.",
                    artifact=artifact,
                    evidence_path=str(path),
                )
            )
        if limit and chars > int(limit):
            findings.append(
                _finding(
                    severity="warn",
                    type="oversized_artifact",
                    waste_type="artifact_size",
                    evidence=str(path),
                    value_level="medium",
                    disposition="optimize",
                    action_target=artifact,
                    owner="prd-writing-steward",
                    recommendation="Shorten the artifact or move detailed content to a supporting appendix.",
                    quality_risk="medium",
                    retest_required=True,
                    rollback_condition="If shortening removes acceptance, risk, or downstream input content, restore the previous artifact and split detail into an appendix.",
                    artifact=artifact,
                    chars=chars,
                    threshold=int(limit),
                    evidence_path=str(path),
                )
            )
        if repeated_lines:
            findings.append(
                _finding(
                    severity="warn",
                    type="repeated_output",
                    waste_type="repeated_output",
                    evidence=str(path),
                    value_level="low",
                    disposition="optimize",
                    action_target=artifact,
                    owner="prd-writing-steward",
                    recommendation="Deduplicate repeated sections or convert repeated text into references.",
                    quality_risk="low",
                    retest_required=True,
                    rollback_condition="If deduplication makes the artifact harder to review or drops required evidence, restore the repeated section and use references instead.",
                    artifact=artifact,
                    repeated_line_count=len(repeated_lines),
                    evidence_path=str(path),
                )
            )
        if long_lines:
            findings.append(
                _finding(
                    severity="info",
                    type="long_line",
                    waste_type="reviewability",
                    evidence=str(path),
                    value_level="low",
                    disposition="record",
                    action_target=artifact,
                    owner="prd-writing-steward",
                    recommendation="Consider breaking long paragraphs into reviewable bullets.",
                    quality_risk="low",
                    retest_required=False,
                    rollback_condition="No rollback required unless readability edits alter meaning.",
                    artifact=artifact,
                    long_line_count=len(long_lines),
                    evidence_path=str(path),
                )
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
    existing_report = read_json(run_dir / "efficiency_report.json")
    fingerprints = _current_fingerprints(base_dir, project_dir, run_dir)
    existing_report_trust = _report_trust_status(existing_report, fingerprints)
    token_usage_summary, stage_token_metrics, token_meta_metrics = _token_meta_metrics(project_dir)
    skills_registry = load_yaml(base_dir / "registry" / "skills.yaml").get("skills", {})
    run_limits = policy.get("run_limits", {})
    findings: list[dict[str, Any]] = []

    if not write_report and existing_report_trust["status"] in {"legacy_stale", "stale"}:
        findings.append(
            _finding(
                severity="warn",
                type="stale_efficiency_report",
                waste_type="stale_report",
                evidence=str(run_dir / "efficiency_report.json"),
                value_level="unknown",
                disposition="gate",
                action_target="efficiency_report_trust",
                owner="efficiency-steward",
                recommendation="Refresh the efficiency report with --write-report before using it for closeout or long-term governance decisions.",
                quality_risk="medium",
                retest_required=True,
                rollback_condition="If report refresh changes historical evidence, preserve the old report and write a new report for the corrected run.",
                secondary_owner="development-governance-steward",
                trust_status=existing_report_trust["status"],
                stale_reasons=existing_report_trust["reasons"],
            )
        )

    skill_call_count = len(trace.get("skill_calls", []))
    enabled_skills = manifest.get("enabled_skills", [])
    if not isinstance(enabled_skills, list):
        enabled_skills = []
    enabled_skill_count = len(enabled_skills)
    skill_cost_count = max(skill_call_count, enabled_skill_count)
    mcp_call_count = len(trace.get("mcp_calls", []))
    max_skill_calls = int(run_limits.get("max_skill_calls", 8))
    if skill_cost_count > max_skill_calls:
        findings.append(
            _finding(
                severity="warn",
                type="too_many_enabled_skills" if enabled_skill_count >= skill_call_count else "too_many_skill_calls",
                waste_type="skill_overuse",
                evidence=str(run_dir / "manifest.json"),
                value_level="medium",
                disposition="gate",
                action_target="workflow_skill_routing",
                owner="pm-copilot-chief",
                recommendation="Split the workflow into staged runs or remove unnecessary skill calls.",
                quality_risk="medium",
                retest_required=True,
                rollback_condition="If reducing skill calls removes required quality, risk, or delivery checks, restore the prior staged workflow and escalate.",
                skill_call_count=skill_call_count,
                enabled_skill_count=enabled_skill_count,
                skill_cost_count=skill_cost_count,
                threshold=max_skill_calls,
            )
        )
    if enabled_skill_count and skill_call_count == 0:
        findings.append(
            _finding(
                severity="warn",
                type="trace_manifest_mismatch",
                waste_type="audit_gap",
                evidence=f"{run_dir / 'manifest.json'} vs {run_dir / 'trace.json'}",
                value_level="unknown",
                disposition="gate",
                action_target="run_trace_contract",
                owner="development-governance-steward",
                recommendation="Record actual skill calls in trace or treat manifest-enabled skills as planned cost during efficiency review.",
                quality_risk="medium",
                retest_required=True,
                rollback_condition="If trace repair changes historical run evidence, preserve the old files and write a new corrected run report instead.",
                enabled_skill_count=enabled_skill_count,
                skill_call_count=skill_call_count,
            )
        )
    pipeline_internal_enabled_skills = [
        skill
        for skill in enabled_skills
        if isinstance(skill, str)
        and isinstance(skills_registry.get(skill), dict)
        and not skills_registry[skill].get("path")
        and skills_registry[skill].get("execution_mode") == "pipeline_internal"
    ]
    concept_enabled_skills = [
        skill
        for skill in enabled_skills
        if isinstance(skill, str)
        and isinstance(skills_registry.get(skill), dict)
        and not skills_registry[skill].get("path")
        and skills_registry[skill].get("execution_mode") != "pipeline_internal"
    ]
    if concept_enabled_skills:
        findings.append(
            _finding(
                severity="warn",
                type="enabled_concept_skills",
                waste_type="routing_contract_gap",
                evidence=str(run_dir / "manifest.json"),
                value_level="unknown",
                disposition="watch",
                action_target="registry_skill_execution_mode",
                owner="development-governance-steward",
                recommendation="Mark concept skills as pipeline_internal or remove them from executable skill routing.",
                quality_risk="medium",
                retest_required=True,
                rollback_condition="If marking concept skills changes pipeline behavior, restore the previous registry and keep the concept only in workflow documentation.",
                skills=concept_enabled_skills,
            )
        )
    if pipeline_internal_enabled_skills:
        findings.append(
            _finding(
                severity="info",
                type="pipeline_internal_skills_enabled",
                waste_type="routing_scope_record",
                evidence=str(run_dir / "manifest.json"),
                value_level="medium",
                disposition="record",
                action_target="pipeline_trace_only",
                owner="development-governance-steward",
                recommendation="Keep these skills in pipeline trace only; do not load them as default SKILL.md routing candidates.",
                quality_risk="low",
                retest_required=False,
                rollback_condition="If a pipeline-internal skill is promoted to a loadable skill, add a path, owner validation, and route-level tests before changing routing.",
                skills=pipeline_internal_enabled_skills,
            )
        )
    if mcp_call_count > int(run_limits.get("max_mcp_calls", 5)):
        findings.append(
            _finding(
                severity="warn",
                type="too_many_mcp_calls",
                waste_type="mcp_overuse",
                evidence=str(run_dir / "trace.json"),
                value_level="medium",
                disposition="optimize",
                action_target="mcp_collection_scope",
                owner="research-steward",
                recommendation="Reduce external collection scope or batch source collection.",
                quality_risk="medium",
                retest_required=True,
                rollback_condition="If reducing MCP calls weakens source coverage or traceability, restore the previous collection scope and batch the calls instead.",
                mcp_call_count=mcp_call_count,
                threshold=int(run_limits.get("max_mcp_calls", 5)),
            )
        )

    artifact_metrics, artifact_findings = _artifact_metrics(project_dir, policy)
    findings.extend(artifact_findings)
    total_artifact_chars = sum(item["chars"] for item in artifact_metrics)
    if total_artifact_chars > int(run_limits.get("max_total_artifact_chars", 120000)):
        findings.append(
            _finding(
                severity="warn",
                type="oversized_run_artifacts",
                waste_type="artifact_chain_size",
                evidence=str(project_dir),
                value_level="medium",
                disposition="optimize",
                action_target="project_artifact_set",
                owner="pm-copilot-chief",
                recommendation="Move verbose sections into supporting artifacts and keep main PRD concise.",
                quality_risk="medium",
                retest_required=True,
                rollback_condition="If moving detail breaks downstream review or evidence traceability, restore the prior artifact layout and add an index instead.",
                total_artifact_chars=total_artifact_chars,
                threshold=int(run_limits.get("max_total_artifact_chars", 120000)),
            )
        )

    status = "pass"
    if any(finding["severity"] in {"warn", "optimize", "escalate"} for finding in findings):
        status = "warn"

    report = {
        "report_version": REPORT_VERSION,
        "run_id": effective_run_id,
        "project_id": project,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": status,
        "report_trust_status": {"status": "fresh", "trusted": True, "reasons": []}
        if write_report
        else existing_report_trust,
        **fingerprints,
        "skill_call_count": skill_cost_count,
        "trace_skill_call_count": skill_call_count,
        "enabled_skill_count": enabled_skill_count,
        "mcp_call_count": mcp_call_count,
        "token_usage_summary": token_usage_summary,
        "stage_token_metrics": stage_token_metrics,
        "token_meta_metrics": token_meta_metrics,
        "manifest_enabled_skills": manifest.get("enabled_skills", []),
        "finding_required_fields": policy.get("finding_contract", {}).get("required_fields", []),
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
