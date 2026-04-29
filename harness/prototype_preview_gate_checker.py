#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from common import CheckResult, read_json, result_from_issues


def _preview_approved(state: dict) -> bool:
    approvals = set(state.get("approvals", []))
    overrides = state.get("assumption_overrides", {})
    return (
        "prototype_preview" in approvals
        or overrides.get("prototype_preview") is True
        or state.get("prototype_preview_approved") is True
    )


def check_prototype_preview_gate(base_dir: Path, project: str) -> CheckResult:
    issues: list[str] = []
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
            for term in ["prototype_mode", "full", "页面清单", "关键转场", "异常状态", "视觉 QA"]:
                if term not in text:
                    issues.append(f"full_prototype.md missing required term: {term}")
            for page_id in ["P1", "P6", "P7", "P12", "P16", "P18"]:
                if page_id not in text:
                    issues.append(f"full_prototype.md missing full-stage page marker: {page_id}")

    return result_from_issues("prototype_preview_gate", issues)
