#!/usr/bin/env python3
from __future__ import annotations

import random
from pathlib import Path
from typing import Any

from common import CheckResult, load_yaml, read_json, write_json


def _load_run_context(base_dir: Path, project: str, run_id: str | None = None) -> tuple[str, dict[str, Any], Path]:
    project_dir = base_dir / "projects" / project
    state = read_json(project_dir / "project_state.json")
    effective_run_id = run_id or state.get("last_run_id") or "governance-baseline"
    run_dir = project_dir / "runs" / effective_run_id
    trace = read_json(run_dir / "trace.json")
    return effective_run_id, trace, run_dir


def _risk_score_for_skill(skill: dict[str, Any], policy: dict[str, Any], *, has_previous_warning: bool = False) -> int:
    weights = policy.get("risk_weights", {})
    score = weights.get("skill_status", {}).get(skill.get("status"), 1)
    artifact_weights = weights.get("writes_artifacts", {})
    for artifact in skill.get("writes", []):
        score += artifact_weights.get(artifact, 0)
    if has_previous_warning:
        score += weights.get("previous_warning", 0)
    return max(score, 1)


def _sample_items(items: list[dict[str, Any]], policy: dict[str, Any], run_id: str) -> list[dict[str, Any]]:
    sample_policy = policy.get("sample_policy", {})
    minimum = int(sample_policy.get("minimum_samples_per_run", 1))
    sample_rate = float(sample_policy.get("default_sample_rate", 0.15))
    if not items:
        return []
    sample_count = max(minimum, round(len(items) * sample_rate))
    sample_count = min(sample_count, len(items))
    rng = random.Random(run_id)
    weighted: list[dict[str, Any]] = []
    for item in items:
        weighted.extend([item] * max(int(item.get("risk_score", 1)), 1))
    selected: list[dict[str, Any]] = []
    while weighted and len(selected) < sample_count:
        candidate = rng.choice(weighted)
        key = (candidate.get("type"), candidate.get("id"))
        if key not in {(item.get("type"), item.get("id")) for item in selected}:
            selected.append(candidate)
        weighted = [item for item in weighted if (item.get("type"), item.get("id")) != key]
    return selected


def _report_to(skill: dict[str, Any]) -> list[str]:
    steward = skill.get("steward")
    return [item for item in [steward, "pm-copilot-chief", "user"] if item]


def inspect_random_audit(
    base_dir: Path,
    project: str,
    *,
    run_id: str | None = None,
    write_report: bool = True,
) -> CheckResult:
    policy = load_yaml(base_dir / "governance" / "random_audit_policy.yaml")
    skills = load_yaml(base_dir / "registry" / "skills.yaml").get("skills", {})
    mcps = load_yaml(base_dir / "registry" / "mcps.yaml").get("mcps", {})
    effective_run_id, trace, run_dir = _load_run_context(base_dir, project, run_id)

    candidates: list[dict[str, Any]] = []
    for index, call in enumerate(trace.get("skill_calls", []), start=1):
        skill_id = call.get("skill")
        skill = skills.get(skill_id, {})
        candidates.append(
            {
                "type": "skill_call",
                "id": f"skill:{index}:{skill_id}",
                "call": call,
                "skill": skill,
                "risk_score": _risk_score_for_skill(skill, policy),
            }
        )
    for index, call in enumerate(trace.get("mcp_calls", []), start=1):
        candidates.append(
            {
                "type": "mcp_call",
                "id": f"mcp:{index}:{call.get('mcp')}",
                "call": call,
                "risk_score": 3,
            }
        )
    if not candidates:
        report = {
            "audit_id": f"{project}-{effective_run_id}-random-audit",
            "run_id": effective_run_id,
            "project_id": project,
            "status": "pass",
            "sampled_items": [],
            "findings": [],
        }
        if write_report:
            write_json(run_dir / "random_audit_report.json", report)
        return CheckResult("random_audit", "pass", "No trace calls to audit.", [])

    sampled = _sample_items(candidates, policy, effective_run_id)
    findings: list[dict[str, Any]] = []

    for item in sampled:
        call = item["call"]
        if item["type"] == "skill_call":
            skill_id = call.get("skill")
            skill = skills.get(skill_id)
            if not skill:
                findings.append(
                    {
                        "severity": "block",
                        "finding": f"Unregistered skill was called: {skill_id}",
                        "involved": skill_id,
                        "violated_rule": "registered_skill_required",
                        "report_to": ["pm-copilot-chief", "user"],
                        "recommended_action": "Register the skill or remove it from the run trace.",
                    }
                )
                continue
            for output in call.get("outputs", []):
                if output not in set(skill.get("writes", [])):
                    findings.append(
                        {
                            "severity": "block",
                            "finding": f"Skill produced undeclared output: {output}",
                            "involved": skill_id,
                            "violated_rule": "declared_outputs_only",
                            "report_to": _report_to(skill),
                            "recommended_action": "Update the skill registry or fix the skill output boundary.",
                        }
                    )
                if output in set(skill.get("forbidden_outputs", [])):
                    findings.append(
                        {
                            "severity": "escalate",
                            "finding": f"Skill produced forbidden output: {output}",
                            "involved": skill_id,
                            "violated_rule": "no_forbidden_outputs",
                            "report_to": _report_to(skill),
                            "recommended_action": "Pause the skill for this workflow until the supervisor reviews it.",
                        }
                    )
            if call.get("steward") != skill.get("steward"):
                findings.append(
                    {
                        "severity": "warn",
                        "finding": f"Skill was called by {call.get('steward')} but belongs to {skill.get('steward')}",
                        "involved": skill_id,
                        "violated_rule": "report_to_supervisor_on_violation",
                        "report_to": _report_to(skill),
                        "recommended_action": "Route this call through the responsible sub-steward.",
                    }
                )
        elif item["type"] == "mcp_call":
            mcp_id = call.get("mcp")
            mcp = mcps.get(mcp_id)
            if not mcp:
                findings.append(
                    {
                        "severity": "block",
                        "finding": f"Unregistered MCP was called: {mcp_id}",
                        "involved": mcp_id,
                        "violated_rule": "registered_mcp_required",
                        "report_to": ["pm-copilot-chief", "user"],
                        "recommended_action": "Register the MCP or remove it from the run trace.",
                    }
                )
                continue
            for output in call.get("outputs", []):
                if output in set(mcp.get("forbidden_outputs", [])):
                    findings.append(
                        {
                            "severity": "escalate",
                            "finding": f"MCP produced forbidden output: {output}",
                            "involved": mcp_id,
                            "violated_rule": "mcp-data-only",
                            "report_to": ["pm-copilot-chief", "user"],
                            "recommended_action": "Treat this as an MCP boundary violation and review the connector.",
                        }
                    )

    status = "pass"
    if any(finding["severity"] in {"block", "escalate"} for finding in findings):
        status = "fail"
    elif findings:
        status = "warn"

    report = {
        "audit_id": f"{project}-{effective_run_id}-random-audit",
        "run_id": effective_run_id,
        "project_id": project,
        "status": status,
        "sampled_items": [
            {
                "type": item.get("type"),
                "id": item.get("id"),
                "risk_score": item.get("risk_score"),
            }
            for item in sampled
        ],
        "findings": findings,
    }
    if write_report:
        write_json(run_dir / "random_audit_report.json", report)

    details = [
        f"{finding['severity']}: {finding['finding']} -> report_to={','.join(finding.get('report_to', []))}"
        for finding in findings
    ]
    if status == "pass":
        return CheckResult("random_audit", "pass", f"Audited {len(sampled)} item(s); no issues found.", [])
    return CheckResult("random_audit", status, f"Audited {len(sampled)} item(s); {len(findings)} finding(s).", details)
