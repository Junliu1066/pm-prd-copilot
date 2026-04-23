#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from common import CheckResult, load_yaml, read_json, result_from_issues


def _load_trace(base_dir: Path, project: str) -> dict:
    project_dir = base_dir / "projects" / project
    state = read_json(project_dir / "project_state.json")
    run_id = state.get("last_run_id")
    if not run_id:
        return {}
    return read_json(project_dir / "runs" / run_id / "trace.json")


def check_steward_contracts(base_dir: Path, project: str) -> CheckResult:
    issues: list[str] = []
    skills = load_yaml(base_dir / "registry" / "skills.yaml").get("skills", {})
    mcps = load_yaml(base_dir / "registry" / "mcps.yaml").get("mcps", {})
    trace = _load_trace(base_dir, project)

    for call in trace.get("skill_calls", []):
        skill_id = call.get("skill")
        if skill_id not in skills:
            issues.append(f"Trace calls unregistered skill: {skill_id}")
            continue
        skill = skills[skill_id]
        declared_writes = set(skill.get("writes", []))
        forbidden = set(skill.get("forbidden_outputs", []))
        for artifact in call.get("outputs", []):
            if artifact not in declared_writes:
                issues.append(f"Skill {skill_id} produced undeclared artifact: {artifact}")
            if artifact in forbidden:
                issues.append(f"Skill {skill_id} produced forbidden artifact: {artifact}")
        if call.get("steward") != skill.get("steward"):
            issues.append(
                f"Skill {skill_id} was called by {call.get('steward')}, expected {skill.get('steward')}"
            )

    for call in trace.get("mcp_calls", []):
        mcp_id = call.get("mcp")
        if mcp_id not in mcps:
            issues.append(f"Trace calls unregistered MCP: {mcp_id}")
            continue
        mcp = mcps[mcp_id]
        allowed = set(mcp.get("allowed_outputs", []))
        forbidden = set(mcp.get("forbidden_outputs", []))
        for output in call.get("outputs", []):
            if output not in allowed:
                issues.append(f"MCP {mcp_id} produced undeclared output: {output}")
            if output in forbidden:
                issues.append(f"MCP {mcp_id} produced forbidden output: {output}")

    return result_from_issues("steward_contract", issues)
