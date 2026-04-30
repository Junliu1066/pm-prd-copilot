#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from common import CheckResult, read_json, result_from_issues


AI_FILES = {
    "ai_capability_map": "ai/ai_capability_map.md",
    "model_selection_plan": "ai/model_selection_plan.md",
    "prompt_architecture": "ai/prompt_architecture.md",
    "rag_architecture": "ai/rag_architecture.md",
    "conversation_memory_plan": "ai/conversation_memory_plan.md",
    "learner_profile_model": "ai/learner_profile_model.md",
    "adaptive_coaching_plan": "ai/adaptive_coaching_plan.md",
    "ai_technical_architecture": "ai/ai_technical_architecture.md",
    "ai_solution_review": "ai/ai_solution_review.json",
}

AI_SKILLS = {
    "ai-capability-mapper",
    "model-selection-planner",
    "prompt-architecture-designer",
    "rag-architecture-planner",
    "conversation-memory-planner",
    "learner-profile-modeler",
    "adaptive-coaching-planner",
    "ai-technical-architecture-planner",
    "ai-solution-reviewer",
}


def _requested_ai(project_dir: Path, run_id: str | None) -> bool:
    state = read_json(project_dir / "project_state.json")
    if state.get("requires_ai_solution_plan") is True:
        return True
    if "ai_solution_planning" in state.get("completed_stages", []):
        return True

    effective_run_id = run_id or state.get("last_run_id")
    if not effective_run_id:
        return False
    manifest = read_json(project_dir / "runs" / effective_run_id / "manifest.json")
    required_outputs = set(manifest.get("required_outputs", []))
    enabled_skills = set(manifest.get("enabled_skills", []))
    return bool(required_outputs & set(AI_FILES) or enabled_skills & AI_SKILLS)


def _contains_any(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _require_terms(issues: list[str], label: str, text: str, checks: dict[str, list[str]]) -> None:
    for check, terms in checks.items():
        if not _contains_any(text, terms):
            issues.append(f"{label} missing {check}.")


def check_ai_solution(base_dir: Path, project: str, *, run_id: str | None = None) -> CheckResult:
    project_dir = base_dir / "projects" / project
    ai_dir = project_dir / "ai"
    has_ai_files = ai_dir.exists() and any(ai_dir.iterdir())
    if not _requested_ai(project_dir, run_id) and not has_ai_files:
        return CheckResult("ai_solution", "pass", "AI solution planning not requested for this project.", [])

    issues: list[str] = []
    for artifact, relative_path in AI_FILES.items():
        path = project_dir / relative_path
        if not path.exists():
            issues.append(f"Missing required AI solution artifact: {artifact} ({relative_path})")

    _require_terms(
        issues,
        "ai_capability_map.md",
        _read_text(project_dir / AI_FILES["ai_capability_map"]),
        {
            "ai capabilities": ["ai_capabilities", "AI 能力", "capability"],
            "non-AI boundaries": ["non_ai_boundaries", "非 AI", "deterministic"],
            "quality needs": ["quality_needs", "质量", "evaluation"],
            "safety risks": ["safety_risks", "风险", "guardrail"],
            "fallback": ["fallback", "降级", "人工"],
        },
    )
    _require_terms(
        issues,
        "model_selection_plan.md",
        _read_text(project_dir / AI_FILES["model_selection_plan"]),
        {
            "official docs verification": ["docs_verification_required", "官方文档", "official docs"],
            "market candidate pool": ["candidate_model_pool", "市场候选", "候选模型池"],
            "model comparison matrix": ["model_comparison_matrix", "横向对比", "对比矩阵"],
            "benchmark plan": ["benchmark_plan", "benchmark", "评测"],
            "benchmark status": ["benchmark_status", "not_measured", "未实测", "not_run"],
            "shortlist recommendations": ["shortlist_recommendations", "推荐模型", "建议使用"],
            "fallback model policy": ["fallback", "降级", "备用"],
            "cost or latency criteria": ["cost", "latency", "成本", "延迟"],
        },
    )
    _require_terms(
        issues,
        "prompt_architecture.md",
        _read_text(project_dir / AI_FILES["prompt_architecture"]),
        {
            "prompt assets": ["prompt_assets", "prompt assets", "提示词资产"],
            "versioning": ["versioning", "版本"],
            "test cases": ["test_cases", "测试用例", "eval"],
            "safety controls": ["safety", "guardrail", "安全"],
        },
    )
    _require_terms(
        issues,
        "rag_architecture.md",
        _read_text(project_dir / AI_FILES["rag_architecture"]),
        {
            "knowledge sources": ["knowledge_sources", "知识源", "source"],
            "retrieval strategy": ["retrieval", "召回", "检索"],
            "citation or trace": ["citation", "source_trace", "引用", "溯源"],
            "fallback": ["fallback", "降级"],
            "permission controls": ["permission", "权限"],
        },
    )
    _require_terms(
        issues,
        "conversation_memory_plan.md",
        _read_text(project_dir / AI_FILES["conversation_memory_plan"]),
        {
            "memory layers": ["memory_layers", "记忆层"],
            "retention": ["retention", "保留"],
            "clear control": ["clear_control", "清除"],
            "sensitive data": ["sensitive", "敏感"],
        },
    )
    _require_terms(
        issues,
        "learner_profile_model.md",
        _read_text(project_dir / AI_FILES["learner_profile_model"]),
        {
            "dimensions": ["dimensions", "维度"],
            "evidence": ["evidence", "证据"],
            "confidence": ["confidence", "置信"],
            "privacy": ["privacy", "隐私"],
        },
    )
    _require_terms(
        issues,
        "adaptive_coaching_plan.md",
        _read_text(project_dir / AI_FILES["adaptive_coaching_plan"]),
        {
            "coaching rules": ["coaching_rules", "教练规则"],
            "difficulty": ["difficulty", "难度"],
            "guardrails": ["guardrails", "边界"],
            "improvement metrics": ["improvement_metrics", "提升指标"],
        },
    )
    _require_terms(
        issues,
        "ai_technical_architecture.md",
        _read_text(project_dir / AI_FILES["ai_technical_architecture"]),
        {
            "AI service boundary": ["ai_service_boundary", "AI 服务边界"],
            "API contracts": ["api_contracts", "API 契约"],
            "model gateway": ["model_gateway", "模型网关"],
            "prompt registry": ["prompt_registry", "Prompt 注册"],
            "RAG pipeline": ["rag_pipeline", "RAG pipeline"],
            "memory/profile storage": ["memory_profile_storage", "画像存储"],
            "observability": ["observability", "观测"],
            "fallback": ["fallback", "降级"],
        },
    )

    review_path = project_dir / AI_FILES["ai_solution_review"]
    if review_path.exists():
        review = read_json(review_path)
        status = review.get("review_status")
        if status not in {"pass", "warn", "fail"}:
            issues.append(f"ai_solution_review.json has invalid review_status: {status}")
        if "readiness_score" not in review:
            issues.append("ai_solution_review.json missing readiness_score.")
        if status == "fail":
            issues.append("ai_solution_review.json is fail; AI solution is not ready.")

    return result_from_issues("ai_solution", issues)
