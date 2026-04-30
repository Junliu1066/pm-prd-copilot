#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from common import CheckResult, read_json, result_from_issues


DELIVERY_FILES = {
    "technical_scope": "delivery/technical_scope.md",
    "release_roadmap": "delivery/release_roadmap.md",
    "effort_estimate": "delivery/effort_estimate.md",
    "delivery_plan": "delivery/delivery_plan.md",
    "delivery_quality_report": "delivery/delivery_quality_report.json",
}


def _requested_delivery(project_dir: Path, run_id: str | None) -> bool:
    state = read_json(project_dir / "project_state.json")
    if state.get("requires_delivery_plan") is True:
        return True
    if "delivery_planning" in state.get("completed_stages", []):
        return True

    effective_run_id = run_id or state.get("last_run_id")
    if not effective_run_id:
        return False
    manifest = read_json(project_dir / "runs" / effective_run_id / "manifest.json")
    required_outputs = set(manifest.get("required_outputs", []))
    enabled_skills = set(manifest.get("enabled_skills", []))
    if required_outputs & set(DELIVERY_FILES):
        return True
    return bool(
        enabled_skills
        & {
            "technical-scope-planner",
            "release-roadmap-planner",
            "effort-estimator",
            "delivery-effect-definer",
            "delivery-quality-reviewer",
        }
    )


def _contains_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def check_delivery_plan(base_dir: Path, project: str, *, run_id: str | None = None) -> CheckResult:
    project_dir = base_dir / "projects" / project
    delivery_dir = project_dir / "delivery"
    has_delivery_files = delivery_dir.exists() and any(delivery_dir.iterdir())
    if not _requested_delivery(project_dir, run_id) and not has_delivery_files:
        return CheckResult("delivery_plan", "pass", "Delivery planning not requested for this project.", [])

    issues: list[str] = []
    for artifact, relative_path in DELIVERY_FILES.items():
        path = project_dir / relative_path
        if not path.exists():
            issues.append(f"Missing required delivery artifact: {artifact} ({relative_path})")

    plan_path = project_dir / DELIVERY_FILES["delivery_plan"]
    if plan_path.exists():
        plan_text = plan_path.read_text(encoding="utf-8")
        checks = {
            "team assumptions": ["team_assumptions", "团队假设", "团队配置"],
            "phase plan": ["phase_delivery_plan", "阶段", "MVP", "V1"],
            "duration range": ["duration_range", "工期", "时长", "周"],
            "user-visible effect": ["user_visible_effect", "用户可见效果", "用户能"],
            "business validation": ["business_validation", "业务验证", "验证"],
            "future separation": ["Future", "最终目标", "长期目标"],
            "open decisions": ["open_decisions", "待决策", "待确认"],
        }
        for label, terms in checks.items():
            if not _contains_any(plan_text, terms):
                issues.append(f"delivery_plan.md missing {label}.")
        if _contains_any(plan_text, ["修改 MVP 范围", "直接修改产品范围", "覆盖产品决策"]):
            issues.append("delivery_plan.md appears to mutate product scope instead of routing backflow questions.")

    estimate_path = project_dir / DELIVERY_FILES["effort_estimate"]
    if estimate_path.exists():
        estimate_text = estimate_path.read_text(encoding="utf-8")
        if not _contains_any(estimate_text, ["team_assumptions", "团队假设", "团队配置"]):
            issues.append("effort_estimate.md must include team assumptions.")
        if not _contains_any(estimate_text, ["buffer", "缓冲", "风险预留"]):
            issues.append("effort_estimate.md must include buffer policy.")
        if not _contains_any(estimate_text, ["QA", "测试", "联调", "integration"]):
            issues.append("effort_estimate.md must include QA/integration effort.")

    quality_path = project_dir / DELIVERY_FILES["delivery_quality_report"]
    if quality_path.exists():
        quality = read_json(quality_path)
        status = quality.get("review_status")
        if status not in {"pass", "warn", "fail"}:
            issues.append(f"delivery_quality_report.json has invalid review_status: {status}")
        if "readiness_score" not in quality:
            issues.append("delivery_quality_report.json missing readiness_score.")
        if status == "fail":
            issues.append("delivery_quality_report.json is fail; delivery plan is not ready.")

    return result_from_issues("delivery_plan", issues)
