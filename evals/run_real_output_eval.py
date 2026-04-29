#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import yaml


ASSERTION_LABELS = {
    "broad_user_segments_before_narrowing": "先广泛枚举用户群体，再收窄",
    "direct_and_indirect_competitors": "竞品覆盖直接与间接影响",
    "source_trace_for_external_data": "外部信息带来源追踪与人工验证提醒",
    "preview_before_full_prototype": "先原型预览，未批准不画全流程",
    "project_preferences_do_not_leak": "项目偏好不污染其他案例",
    "system_reminder_vs_auto_advance_is_explicit": "区分系统提醒与自动推进",
    "conversion_path_has_clear_user_decision_points": "转化路径有清晰用户决策点",
    "permission_and_exception_states_are_included": "包含权限与异常状态",
    "learning_feedback_loop_is_explicit": "学习反馈闭环明确",
    "experiment_metrics_are_defined_before_optimization": "优化前先定义实验指标",
    "prd_visuals_are_section_local": "PRD 辅助理解图归位到对应章节",
    "page_specs_and_flow_present": "PRD 默认包含页面说明和页面跳转关系",
    "prd_prototype_layer_present": "PRD 默认包含原型图层",
    "default_wireframes_are_not_forced": "不默认强制原型图/线框图",
    "non_ai_omits_ai_model_selection": "非 AI 项目不强行输出 AI 模型选型",
}

LEAK_TERMS = [
    "fitness-app-mvp",
    "暗黑机械风",
    "青绿色",
    "dark mechanical",
    "China market as the default",
    "中国市场默认",
    "默认优先中国",
]


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _has_user_matrix(text: str) -> bool:
    if "用户群体矩阵" not in text:
        return False
    matrix_lines = [
        line
        for line in text.splitlines()
        if line.startswith("|") and "用户群体" not in line and "---" not in line
    ]
    return len(matrix_lines) >= 4


def _has_competitor_map(text: str) -> bool:
    required_terms = [
        ("直接",),
        ("相邻",),
        ("平台原生", "系统能力"),
        ("内容", "社区"),
        ("手动", "线下", "人工"),
    ]
    return "竞品外延" in text and all(any(term in text for term in group) for group in required_terms)


def _has_source_trace(text: str) -> bool:
    return (
        "external_truth_status" in text
        and "human_verification_required: true" in text
        and ("需人工验证" in text or "人工验证" in text)
    )


def _has_preview_gate(text: str) -> bool:
    return "prototype_mode: preview" in text and "full_prototype_blocked: true" in text


def _has_no_project_leakage(text: str) -> bool:
    return not any(term in text for term in LEAK_TERMS)


def _has_reminder_vs_auto_advance(text: str) -> bool:
    return "提醒" in text and ("不自动" in text or "等待用户" in text)


def _has_conversion_decisions(text: str) -> bool:
    return "决策点" in text and ("预约" in text or "咨询" in text)


def _has_permissions_and_exceptions(text: str) -> bool:
    return "权限" in text and ("异常" in text or "失败" in text)


def _has_learning_loop(text: str) -> bool:
    return "反馈闭环" in text and ("复习" in text or "错题" in text)


def _has_experiment_metrics(text: str) -> bool:
    return "实验指标" in text and ("优化前" in text or "先定义" in text)


def _has_section_local_prd_visuals(text: str) -> bool:
    return "产品总览思维导图" in text and "MVP 范围" in text and "PRD 可视化层" not in text


def _has_page_specs_and_flow(text: str) -> bool:
    return "页面说明" in text and "页面跳转关系" in text


def _has_prd_prototype_layer(text: str) -> bool:
    return "原型图层" in text and ("页面级低保真" in text or "页面原型说明" in text)


def _has_no_default_wireframes(text: str) -> bool:
    return "原型图 / 线框图" not in text


def _has_no_forced_ai_model_selection(text: str) -> bool:
    return "AI 模型选型" not in text


ASSERTION_CHECKS: dict[str, Callable[[str], bool]] = {
    "broad_user_segments_before_narrowing": _has_user_matrix,
    "direct_and_indirect_competitors": _has_competitor_map,
    "source_trace_for_external_data": _has_source_trace,
    "preview_before_full_prototype": _has_preview_gate,
    "project_preferences_do_not_leak": _has_no_project_leakage,
    "system_reminder_vs_auto_advance_is_explicit": _has_reminder_vs_auto_advance,
    "conversion_path_has_clear_user_decision_points": _has_conversion_decisions,
    "permission_and_exception_states_are_included": _has_permissions_and_exceptions,
    "learning_feedback_loop_is_explicit": _has_learning_loop,
    "experiment_metrics_are_defined_before_optimization": _has_experiment_metrics,
    "prd_visuals_are_section_local": _has_section_local_prd_visuals,
    "page_specs_and_flow_present": _has_page_specs_and_flow,
    "prd_prototype_layer_present": _has_prd_prototype_layer,
    "default_wireframes_are_not_forced": _has_no_default_wireframes,
    "non_ai_omits_ai_model_selection": _has_no_forced_ai_model_selection,
}


def _evaluate_case(case: dict[str, Any], output_path: Path) -> dict[str, Any]:
    case_id = str(case["case_id"])
    if not output_path.exists():
        return {
            "case_id": case_id,
            "status": "fail",
            "score": 0,
            "max_score": len(case.get("quality_assertions", [])),
            "output_path": str(output_path),
            "assertions": [
                {
                    "assertion": assertion,
                    "label": ASSERTION_LABELS.get(assertion, assertion),
                    "status": "fail",
                    "message": "Output artifact is missing.",
                }
                for assertion in case.get("quality_assertions", [])
            ],
        }

    text = output_path.read_text(encoding="utf-8")
    assertion_results = []
    score = 0
    for assertion in case.get("quality_assertions", []):
        checker = ASSERTION_CHECKS.get(assertion)
        passed = bool(checker(text)) if checker else False
        if passed:
            score += 1
        assertion_results.append(
            {
                "assertion": assertion,
                "label": ASSERTION_LABELS.get(assertion, assertion),
                "status": "pass" if passed else "fail",
            }
        )
    max_score = len(assertion_results)
    return {
        "case_id": case_id,
        "domain": case.get("domain"),
        "status": "pass" if score == max_score else "fail",
        "score": score,
        "max_score": max_score,
        "output_path": str(output_path),
        "assertions": assertion_results,
    }


def _write_summary(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Real Output Eval Summary",
        "",
        f"- run_id: `{report['run_id']}`",
        f"- status: `{report['status']}`",
        f"- total_score: `{report['total_score']} / {report['max_score']}`",
        "",
        "| Case | Domain | Score | Status | Output |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in report["cases"]:
        output_rel = Path(item["output_path"]).as_posix()
        lines.append(
            f"| `{item['case_id']}` | `{item.get('domain', '')}` | {item['score']} / {item['max_score']} | `{item['status']}` | [{Path(output_rel).name}]({output_rel}) |"
        )
    lines.extend(
        [
            "",
            "## Review Reminder",
            "",
            "These outputs are evaluation samples. External market and competitor signals are not verified facts; the user must validate them before product decisions.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run real output evaluation for PM Copilot skills.")
    parser.add_argument("--base-dir", default=".")
    parser.add_argument("--cases", default="evals/skill_quality_cases.yaml")
    parser.add_argument("--run-id", default="")
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    cases_path = base_dir / args.cases
    suite = _load_yaml(cases_path)
    cases = suite.get("cases", [])
    if not isinstance(cases, list) or not cases:
        raise SystemExit("No eval cases found.")

    run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = base_dir / "evals" / "real_outputs" / run_id
    evaluated_cases = []
    for case in cases:
        case_id = str(case["case_id"])
        output_path = run_dir / "cases" / case_id / "output.md"
        evaluated_cases.append(_evaluate_case(case, output_path))

    total_score = sum(item["score"] for item in evaluated_cases)
    max_score = sum(item["max_score"] for item in evaluated_cases)
    report = {
        "run_id": run_id,
        "status": "pass" if total_score == max_score else "fail",
        "total_score": total_score,
        "max_score": max_score,
        "cases": evaluated_cases,
        "verification_notice": "External market and competitor signals are evaluation samples and require human verification.",
    }
    _write_json(run_dir / "real_output_eval_report.json", report)
    _write_summary(run_dir / "summary.md", report)

    print(f"Real output eval status: {report['status']}")
    print(f"Score: {total_score}/{max_score}")
    print(run_dir / "real_output_eval_report.json")
    raise SystemExit(0 if report["status"] == "pass" else 1)


if __name__ == "__main__":
    main()
