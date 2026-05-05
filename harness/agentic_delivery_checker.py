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

LIGHTWEIGHT_REQUIRED_FILES = {
    "codex_task_packages",
    "human_supervision_plan",
    "codex_development_review",
}
FULL_ONLY_FILES = {
    "agentic_delivery_plan",
    "development_governance_report",
    "capability_enablement_plan",
    "skill_mcp_routing_plan",
    "development_operating_system_plan",
    "codex_task_package_blueprint",
    "phase_1_codex_plan",
    "phase_2_codex_plan",
    "phase_3_codex_plan",
    "final_codex_plan",
}
FULL_REQUIRED_FILES = LIGHTWEIGHT_REQUIRED_FILES | {"development_governance_report"}
DEVELOPMENT_DOCUMENT_OPTIONS = ("codex_development_document", "codex_development_plan")
FULL_MODE_VALUES = {"full", "full_agentic_delivery", "agentic", "supervised", "full_supervised_package"}
LIGHTWEIGHT_MODE_VALUES = {"lightweight", "lightweight_codex_delivery", "lightweight_development_document"}


def _request_context(project_dir: Path, run_id: str | None) -> tuple[dict, dict, set[str], set[str]]:
    state = read_json(project_dir / "project_state.json")
    effective_run_id = run_id or state.get("last_run_id")
    manifest = read_json(project_dir / "runs" / effective_run_id / "manifest.json") if effective_run_id else {}
    required_outputs = set(manifest.get("required_outputs", []))
    enabled_skills = set(manifest.get("enabled_skills", []))
    return state, manifest, required_outputs, enabled_skills


def _requested_agentic(project_dir: Path, run_id: str | None) -> bool:
    state, _manifest, required_outputs, enabled_skills = _request_context(project_dir, run_id)
    if state.get("requires_agentic_delivery") is True or state.get("requires_full_agentic_delivery") is True:
        return True
    if "agentic_delivery_planning" in state.get("completed_stages", []):
        return True
    output_names = set(AGENTIC_FILES) | set(AGENTIC_FILES.values())
    return bool(required_outputs & output_names or "agentic-delivery-orchestrator" in enabled_skills)


def _agentic_mode(project_dir: Path, run_id: str | None) -> str:
    state, _manifest, required_outputs, enabled_skills = _request_context(project_dir, run_id)
    explicit_mode = str(state.get("agentic_delivery_mode") or state.get("codex_delivery_mode") or "").lower()
    if explicit_mode in FULL_MODE_VALUES:
        return "full"
    if explicit_mode in LIGHTWEIGHT_MODE_VALUES:
        return "lightweight"
    if state.get("requires_full_agentic_delivery") is True:
        return "full"
    if state.get("requires_agentic_delivery") is True or "agentic_delivery_planning" in state.get("completed_stages", []):
        return "full"

    full_output_names = FULL_ONLY_FILES | {AGENTIC_FILES[name] for name in FULL_ONLY_FILES}
    if required_outputs & full_output_names:
        return "full"
    if any((project_dir / AGENTIC_FILES[name]).exists() for name in FULL_ONLY_FILES):
        return "full"
    if {"capability-enablement-planner", "skill-mcp-routing-planner"} & enabled_skills:
        return "full"
    return "lightweight"


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


def _result(failures: list[str], warnings: list[str], *, mode: str) -> CheckResult:
    details = failures + [f"Advisory: {warning}" for warning in warnings]
    if failures:
        return CheckResult("agentic_delivery", "fail", f"{len(failures)} blocking issue(s) found.", details)
    if warnings:
        return CheckResult("agentic_delivery", "warn", f"{len(warnings)} advisory issue(s) found.", details)
    return CheckResult("agentic_delivery", "pass", f"No issues found ({mode} mode).", [])


def check_agentic_delivery(base_dir: Path, project: str, *, run_id: str | None = None) -> CheckResult:
    project_dir = base_dir / "projects" / project
    delivery_dir = project_dir / "delivery"
    has_agentic_files = any((project_dir / relative).exists() for relative in AGENTIC_FILES.values())
    if not _requested_agentic(project_dir, run_id) and not has_agentic_files:
        return CheckResult("agentic_delivery", "pass", "Agentic delivery planning not requested for this project.", [])

    mode = _agentic_mode(project_dir, run_id)
    failures: list[str] = []
    warnings: list[str] = []

    required_files = FULL_REQUIRED_FILES if mode == "full" else LIGHTWEIGHT_REQUIRED_FILES
    for artifact in required_files:
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
    if mode == "full":
        _require_terms(
            failures,
            document_label,
            development_document_text,
            {
                "branch matrix": ["分支矩阵", "branch_matrix", "branch matrix"],
                "branch governance cards": ["分支治理卡", "branch_governance", "governance card"],
                "branch startup packages": ["分支启动包", "branch_startup", "startup package"],
                "multi-manager governance": ["多管家", "责任管家", "multi-manager", "steward"],
                "harness or gate route": ["Harness", "harness", "Gate", "gate", "门禁"],
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
            message = f"development_governance_report.json has invalid review_status: {status}"
            if mode == "full":
                failures.append(message)
            else:
                warnings.append(message)
        if "readiness_score" not in report:
            message = "development_governance_report.json missing readiness_score."
            if mode == "full":
                failures.append(message)
            else:
                warnings.append(message)
        if status == "fail":
            failures.append("development_governance_report.json is fail; agentic delivery is not ready.")
    elif mode == "lightweight":
        unexpected_full_files = sorted(
            name for name in FULL_ONLY_FILES if (project_dir / AGENTIC_FILES[name]).exists()
        )
        if unexpected_full_files:
            warnings.append(
                "Lightweight agentic delivery contains full-mode artifacts; confirm this is intentional: "
                + ", ".join(unexpected_full_files)
            )

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

    return _result(failures, warnings, mode=mode)
