#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Any

from common import CheckResult, read_json


def _preview_approved(state: dict) -> bool:
    approvals = set(state.get("approvals", []))
    overrides = state.get("assumption_overrides", {})
    return (
        "prototype_preview" in approvals
        or overrides.get("prototype_preview") is True
        or state.get("prototype_preview_approved") is True
    )


def _contains_any(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def _prototype_manifest(project_dir: Path) -> tuple[Path | None, dict]:
    for relative in [
        "prototype/prototype_manifest.json",
        "prototype/manifest.json",
        "prototype/full_prototype_manifest.json",
    ]:
        path = project_dir / relative
        if path.exists():
            return path, read_json(path)
    return None, {}


def _extract_page_names(value: Any) -> list[str]:
    names: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"pages", "page_list", "screens", "views", "routes"}:
                names.extend(_extract_page_names(item))
            elif key in {"id", "page_id", "name", "title", "route"} and isinstance(item, str):
                names.append(item)
            else:
                names.extend(_extract_page_names(item))
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, str):
                names.append(item)
            else:
                names.extend(_extract_page_names(item))
    return [name for name in dict.fromkeys(names) if name.strip()]


def _result(issues: list[str], warnings: list[str]) -> CheckResult:
    details = issues + [f"Advisory: {warning}" for warning in warnings]
    if issues:
        return CheckResult("prototype_preview_gate", "fail", f"{len(issues)} issue(s) found.", details)
    if warnings:
        return CheckResult("prototype_preview_gate", "warn", f"{len(warnings)} advisory issue(s) found.", details)
    return CheckResult("prototype_preview_gate", "pass", "No issues found.", [])


def check_prototype_preview_gate(base_dir: Path, project: str) -> CheckResult:
    issues: list[str] = []
    warnings: list[str] = []
    project_dir = base_dir / "projects" / project
    state = read_json(project_dir / "project_state.json")
    run_id = state.get("last_run_id")
    if not run_id:
        return CheckResult("prototype_preview_gate", "pass", "No run trace found; prototype gate skipped.", [])

    trace = read_json(project_dir / "runs" / run_id / "trace.json")
    approved = _preview_approved(state)

    for index, call in enumerate(trace.get("skill_calls", []), start=1):
        outputs = set(call.get("outputs", []))
        skill = call.get("skill")
        if "full_prototype" in outputs and not approved:
            issues.append(
                f"skill_calls[{index}] {skill} produced full_prototype before prototype_preview approval."
            )
        if {"prototype_preview", "full_prototype"}.issubset(outputs) and not approved:
            issues.append(
                f"skill_calls[{index}] {skill} produced preview and full_prototype in the same unapproved run."
            )

    overrides = state.get("assumption_overrides", {})
    if overrides.get("full_prototype_requested") is True or "full_prototype" in set(state.get("approvals", [])):
        full_md = project_dir / "prototype" / "full_prototype.md"
        full_svg = project_dir / "prototype" / "full_prototype.svg"
        full_png = project_dir / "prototype" / "full_prototype.png"
        for path in [full_md, full_svg, full_png]:
            if not path.exists():
                issues.append(f"Missing requested full prototype artifact: {path.relative_to(project_dir)}")
        if full_md.exists():
            text = full_md.read_text(encoding="utf-8")
            manifest_path, manifest = _prototype_manifest(project_dir)
            if manifest_path:
                page_names = _extract_page_names(manifest)
                if not page_names:
                    issues.append(
                        f"{manifest_path.relative_to(project_dir)} must define at least one page, screen, view, or route."
                    )
            else:
                warnings.append(
                    "No prototype manifest found; full_prototype.md was checked with minimum structure only."
                )

            minimum_structure = {
                "prototype mode": ["prototype_mode", "full", "完整原型", "全量原型"],
                "page inventory": ["页面清单", "页面列表", "page_list", "pages", "screens"],
                "navigation or transitions": ["关键转场", "页面跳转", "navigation", "transition", "flow"],
                "exception states": ["异常状态", "错误状态", "empty", "loading", "error"],
                "visual QA": ["视觉 QA", "视觉检查", "visual qa", "qa", "验收"],
            }
            for label, terms in minimum_structure.items():
                if not _contains_any(text, terms):
                    issues.append(f"full_prototype.md missing minimum structure: {label}")

    return _result(issues, warnings)
