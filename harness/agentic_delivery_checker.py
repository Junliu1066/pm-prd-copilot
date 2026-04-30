#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from common import CheckResult, read_json


AGENTIC_FILES = {
    "agentic_delivery_plan": "delivery/agentic_delivery_plan.md",
    "codex_task_packages": "delivery/codex_task_packages.md",
    "human_supervision_plan": "delivery/human_supervision_plan.md",
    "development_governance_report": "delivery/development_governance_report.json",
    "capability_enablement_plan": "delivery/capability_enablement_plan.md",
    "skill_mcp_routing_plan": "delivery/skill_mcp_routing_plan.md",
    "development_operating_system_plan": "delivery/development_operating_system_plan.md",
    "codex_task_package_blueprint": "delivery/codex_task_package_blueprint.md",
    "codex_development_document": "delivery/codex_development_document.md",
    "codex_development_plan": "delivery/codex_development_plan.md",
    "phase_1_codex_plan": "delivery/phase_1_codex_plan.md",
    "phase_2_codex_plan": "delivery/phase_2_codex_plan.md",
    "phase_3_codex_plan": "delivery/phase_3_codex_plan.md",
    "final_codex_plan": "delivery/final_codex_plan.md",
    "codex_development_review": "delivery/codex_development_review.md",
}

REQUIRED_FILES = {
    "codex_task_packages",
    "human_supervision_plan",
    "development_governance_report",
    "codex_development_review",
}
DEVELOPMENT_DOCUMENT_OPTIONS = ("codex_development_document", "codex_development_plan")


def _requested_agentic(project_dir: Path, run_id: str | None) -> bool:
    state = read_json(project_dir / "project_state.json")
    if state.get("requires_agentic_delivery") is True:
        return True
    if "agentic_delivery_planning" in state.get("completed_stages", []):
        return True

    effective_run_id = run_id or state.get("last_run_id")
    if not effective_run_id:
        return False
    manifest = read_json(project_dir / "runs" / effective_run_id / "manifest.json")
    required_outputs = set(manifest.get("required_outputs", []))
    enabled_skills = set(manifest.get("enabled_skills", []))
    output_names = set(AGENTIC_FILES) | set(AGENTIC_FILES.values())
    return bool(required_outputs & output_names or "agentic-delivery-orchestrator" in enabled_skills)


def _contains_any(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _require_terms(issues: list[str], label: str, text: str, checks: dict[str, list[str]]) -> None:
    for check, terms in checks.items():
        if not _contains_any(text, terms):
            issues.append(f"{label} missing {check}.")


def _warn_terms(warnings: list[str], label: str, text: str, checks: dict[str, list[str]]) -> None:
    for check, terms in checks.items():
        if not _contains_any(text, terms):
            warnings.append(f"{label} could improve {check}.")


def _development_document(project_dir: Path) -> tuple[str, str]:
    for artifact in DEVELOPMENT_DOCUMENT_OPTIONS:
        path = project_dir / AGENTIC_FILES[artifact]
        if path.exists():
            return f"{artifact}.md", _read_text(path)
    return "codex_development_document.md or codex_development_plan.md", ""


def _result(failures: list[str], warnings: list[str]) -> CheckResult:
    details = failures + [f"Advisory: {warning}" for warning in warnings]
    if failures:
        return CheckResult("agentic_delivery", "fail", f"{len(failures)} blocking issue(s) found.", details)
    if warnings:
        return CheckResult("agentic_delivery", "warn", f"{len(warnings)} advisory issue(s) found.", details)
    return CheckResult("agentic_delivery", "pass", "No issues found.", [])


def check_agentic_delivery(base_dir: Path, project: str, *, run_id: str | None = None) -> CheckResult:
    project_dir = base_dir / "projects" / project
    delivery_dir = project_dir / "delivery"
    has_agentic_files = any((project_dir / relative).exists() for relative in AGENTIC_FILES.values())
    if not _requested_agentic(project_dir, run_id) and not has_agentic_files:
        return CheckResult("agentic_delivery", "pass", "Agentic delivery planning not requested for this project.", [])

    failures: list[str] = []
    warnings: list[str] = []

    for artifact in REQUIRED_FILES:
        path = project_dir / AGENTIC_FILES[artifact]
        if not path.exists():
            failures.append(f"Missing required agentic delivery artifact: {artifact} ({AGENTIC_FILES[artifact]})")

    document_label, development_document_text = _development_document(project_dir)
    if not development_document_text:
        failures.append("Missing required agentic delivery artifact: codex_development_document or codex_development_plan")

    _require_terms(
        failures,
        "codex_task_packages.md",
        _read_text(project_dir / AGENTIC_FILES["codex_task_packages"]),
        {
            "allowed write paths": ["allowed_write_paths", "允许修改", "allowed paths"],
            "forbidden write paths": ["forbidden_write_paths", "禁止修改", "forbidden paths"],
            "validation commands": ["validation_commands", "验收命令", "测试命令"],
            "human confirmation points": ["human_confirmation_points", "人工确认"],
            "rollback or minimal fix strategy": ["rollback", "回滚", "minimal_fix_strategy", "最小修复"],
            "task inputs and outputs": ["inputs", "输入", "outputs", "输出"],
        },
    )
    _require_terms(
        failures,
        "human_supervision_plan.md",
        _read_text(project_dir / AGENTIC_FILES["human_supervision_plan"]),
        {
            "scope approval gate": ["prd_scope", "PRD 范围", "scope"],
            "database or data approval gate": ["database_schema", "数据库", "数据"],
            "external service approval gate": ["external_api", "外部 API", "外部服务"],
            "model approval gate": ["model_change", "模型"],
            "release approval gate": ["github_push", "发布", "push"],
            "destructive action approval gate": ["destructive_data", "删除", "清空"],
        },
    )
    _require_terms(
        failures,
        document_label,
        development_document_text,
        {
            "task package route": ["codex_task_packages", "Codex 任务包", "任务包"],
            "validation route": ["validation", "验收", "测试"],
            "human supervision gates": ["human_supervision", "人工监督", "人工确认"],
            "rollback route": ["rollback", "回滚"],
        },
    )
    _require_terms(
        failures,
        "codex_development_review.md",
        _read_text(project_dir / AGENTIC_FILES["codex_development_review"]),
        {
            "review decision": ["审核结论", "pass", "warn", "fail", "可发送", "不可发送"],
            "task executability": ["任务包可执行性", "allowed_write_paths", "validation"],
            "blockers": ["执行阻碍检查", "阻碍", "blocker"],
            "risk rollback": ["风险", "回滚"],
            "human confirmations": ["人工确认清单", "human confirmations"],
        },
    )

    task_text = _read_text(project_dir / AGENTIC_FILES["codex_task_packages"])
    if _contains_any(task_text, ["直接修改 PRD 范围", "覆盖产品决策", "跳过人工确认"]):
        failures.append("codex_task_packages.md contains unsafe product-scope mutation wording.")

    report_path = project_dir / AGENTIC_FILES["development_governance_report"]
    if report_path.exists():
        report = read_json(report_path)
        status = report.get("review_status")
        if status not in {"pass", "warn", "fail"}:
            failures.append(f"development_governance_report.json has invalid review_status: {status}")
        if "readiness_score" not in report:
            failures.append("development_governance_report.json missing readiness_score.")
        if status == "fail":
            failures.append("development_governance_report.json is fail; agentic delivery is not ready.")

    optional_checks = {
        "capability_enablement_plan": {
            "approval boundary": ["human_approval_required", "人工确认"],
            "capability gaps": ["capability_gaps", "能力缺口"],
        },
        "skill_mcp_routing_plan": {
            "fallback": ["fallback", "降级"],
            "source trace": ["source_trace", "溯源"],
        },
        "development_operating_system_plan": {
            "audit route": ["random_audit", "efficiency_audit", "审计"],
            "learning route": ["learning", "教学", "记忆沉淀"],
        },
        "codex_task_package_blueprint": {
            "write boundaries": ["allowed_write_paths", "forbidden_write_paths", "允许修改", "禁止修改"],
            "validation": ["validation_commands", "验收命令"],
        },
    }
    for artifact, checks in optional_checks.items():
        path = project_dir / AGENTIC_FILES[artifact]
        if path.exists():
            _warn_terms(warnings, f"{artifact}.md", _read_text(path), checks)

    phase_checks = {
        "phase boundary": ["阶段目标", "本期范围", "scope"],
        "human confirmation": ["人工确认"],
        "validation": ["验收", "validation"],
        "rollback": ["风险", "回滚"],
    }
    for artifact in ["phase_1_codex_plan", "phase_2_codex_plan", "phase_3_codex_plan", "final_codex_plan"]:
        path = project_dir / AGENTIC_FILES[artifact]
        if path.exists():
            _warn_terms(warnings, f"{artifact}.md", _read_text(path), phase_checks)

    if delivery_dir.exists() and not any(delivery_dir.iterdir()):
        failures.append("delivery directory exists but has no usable agentic artifacts.")

    return _result(failures, warnings)
