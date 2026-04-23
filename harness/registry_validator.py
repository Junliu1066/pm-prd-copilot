#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from common import CheckResult, VALID_STATUSES, load_yaml, result_from_issues


def validate_registry(base_dir: Path) -> CheckResult:
    issues: list[str] = []
    skills = load_yaml(base_dir / "registry" / "skills.yaml").get("skills", {})
    mcps = load_yaml(base_dir / "registry" / "mcps.yaml").get("mcps", {})
    stewards = load_yaml(base_dir / "registry" / "stewards.yaml")
    artifacts = load_yaml(base_dir / "registry" / "artifacts.yaml").get("artifacts", {})

    known_stewards = set(stewards.get("chief_stewards", {}).keys()) | set(stewards.get("sub_stewards", {}).keys())
    known_artifacts = set(artifacts.keys())

    if not skills:
        issues.append("No skills registered.")
    if not known_stewards:
        issues.append("No stewards registered.")

    for skill_id, skill in skills.items():
        status = skill.get("status")
        if status not in VALID_STATUSES:
            issues.append(f"Skill {skill_id} has invalid status: {status}")
        steward = skill.get("steward")
        if steward not in known_stewards:
            issues.append(f"Skill {skill_id} references unknown steward: {steward}")
        for artifact in skill.get("writes", []):
            if artifact not in known_artifacts and not artifact.endswith("_signals"):
                issues.append(f"Skill {skill_id} writes unknown artifact: {artifact}")
        for artifact in skill.get("forbidden_outputs", []):
            if artifact in skill.get("writes", []):
                issues.append(f"Skill {skill_id} both writes and forbids artifact: {artifact}")

    for mcp_id, mcp in mcps.items():
        status = mcp.get("status")
        if status not in VALID_STATUSES:
            issues.append(f"MCP {mcp_id} has invalid status: {status}")
        for forbidden in mcp.get("forbidden_outputs", []):
            if forbidden in mcp.get("allowed_outputs", []):
                issues.append(f"MCP {mcp_id} both allows and forbids output: {forbidden}")

    return result_from_issues("registry", issues)
