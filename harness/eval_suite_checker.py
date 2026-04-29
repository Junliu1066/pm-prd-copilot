#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Any

from common import CheckResult, load_yaml, read_json, write_json


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def check_eval_suite(
    base_dir: Path,
    project: str,
    *,
    run_id: str | None = None,
    write_report: bool = True,
) -> CheckResult:
    issues: list[str] = []
    eval_path = base_dir / "evals" / "skill_quality_cases.yaml"
    if not eval_path.exists():
        return CheckResult("eval_suite", "fail", "Missing evals/skill_quality_cases.yaml.", [])

    eval_suite = load_yaml(eval_path)
    requirements = eval_suite.get("requirements", {})
    cases = _as_list(eval_suite.get("cases", []))
    skills = load_yaml(base_dir / "registry" / "skills.yaml").get("skills", {})
    artifacts = load_yaml(base_dir / "registry" / "artifacts.yaml").get("artifacts", {})

    minimum_cases = int(requirements.get("minimum_cases", 5))
    minimum_unique_domains = int(requirements.get("minimum_unique_domains", 5))
    required_assertions = set(_as_list(requirements.get("required_case_assertions", [])))

    if len(cases) < minimum_cases:
        issues.append(f"Eval suite has {len(cases)} case(s), below required minimum {minimum_cases}.")

    domains = {case.get("domain") for case in cases if case.get("domain")}
    if len(domains) < minimum_unique_domains:
        issues.append(
            f"Eval suite has {len(domains)} unique domain(s), below required minimum {minimum_unique_domains}."
        )

    seen_case_ids: set[str] = set()
    for index, case in enumerate(cases, start=1):
        case_id = str(case.get("case_id", "")).strip()
        if not case_id:
            issues.append(f"Case #{index} is missing case_id.")
            continue
        if case_id in seen_case_ids:
            issues.append(f"Duplicate case_id: {case_id}.")
        seen_case_ids.add(case_id)

        for field in ("domain", "product_prompt", "market_scope_rule"):
            if not str(case.get(field, "")).strip():
                issues.append(f"{case_id} is missing {field}.")

        expected_skills = _as_list(case.get("expected_skills", []))
        expected_outputs = _as_list(case.get("expected_outputs", []))
        quality_assertions = set(_as_list(case.get("quality_assertions", [])))
        if not expected_skills:
            issues.append(f"{case_id} has no expected_skills.")
        if not expected_outputs:
            issues.append(f"{case_id} has no expected_outputs.")

        for skill_id in expected_skills:
            if skill_id not in skills:
                issues.append(f"{case_id} references unknown skill: {skill_id}.")
        for artifact_id in expected_outputs:
            if artifact_id not in artifacts:
                issues.append(f"{case_id} references unknown artifact: {artifact_id}.")

        missing_assertions = sorted(required_assertions - quality_assertions)
        if missing_assertions:
            issues.append(f"{case_id} missing required quality assertion(s): {', '.join(missing_assertions)}.")

    effective_run_id = run_id or read_json(base_dir / "projects" / project / "project_state.json").get("last_run_id")
    if write_report and effective_run_id:
        report_path = base_dir / "projects" / project / "runs" / effective_run_id / "eval_suite_report.json"
        write_json(
            report_path,
            {
                "run_id": effective_run_id,
                "project_id": project,
                "status": "fail" if issues else "pass",
                "case_count": len(cases),
                "unique_domains": sorted(domains),
                "issues": issues,
            },
        )

    if issues:
        return CheckResult("eval_suite", "fail", f"{len(issues)} eval suite issue(s).", issues)
    return CheckResult(
        "eval_suite",
        "pass",
        f"Eval suite covers {len(cases)} case(s) across {len(domains)} domain(s).",
        [],
    )
