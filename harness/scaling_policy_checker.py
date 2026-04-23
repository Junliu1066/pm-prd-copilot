#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from pathlib import Path

from common import CheckResult, load_yaml


def check_scaling_policy(base_dir: Path) -> CheckResult:
    policy = load_yaml(base_dir / "governance" / "steward_scaling_policy.yaml")
    skills = load_yaml(base_dir / "registry" / "skills.yaml").get("skills", {})
    mcps = load_yaml(base_dir / "registry" / "mcps.yaml").get("mcps", {})
    stewards = load_yaml(base_dir / "registry" / "stewards.yaml")

    active_or_candidate_skills = {
        skill_id: skill for skill_id, skill in skills.items() if skill.get("status") in {"active", "candidate"}
    }
    active_or_candidate_mcps = {
        mcp_id: mcp for mcp_id, mcp in mcps.items() if mcp.get("status") in {"active", "candidate"}
    }

    issues: list[str] = []
    direct = policy.get("direct_management", {})
    sub_capacity = policy.get("sub_steward_capacity", {})

    active_sub_stewards = {
        steward_id
        for steward_id, steward in stewards.get("sub_stewards", {}).items()
        if steward.get("status") == "active"
    }
    steward_counts = Counter(skill.get("steward") for skill in active_or_candidate_skills.values())
    unmanaged_skills = [
        skill_id
        for skill_id, skill in active_or_candidate_skills.items()
        if skill.get("steward") not in active_sub_stewards and skill.get("steward") != "pm-copilot-chief"
    ]
    chief_direct_skills = [
        skill_id
        for skill_id, skill in active_or_candidate_skills.items()
        if skill.get("steward") == "pm-copilot-chief"
    ] + unmanaged_skills

    mcp_owner_count = len(active_sub_stewards)
    unmanaged_mcp_count = 0 if mcp_owner_count else len(active_or_candidate_mcps)

    if len(chief_direct_skills) > direct.get("max_skills", 5):
        issues.append(
            f"Chief steward direct skill load is {len(chief_direct_skills)}, above limit {direct.get('max_skills', 5)}; sub-steward governance is required."
        )
    if unmanaged_mcp_count > direct.get("max_mcps", 2):
        issues.append(
            f"Chief steward direct MCP load is {unmanaged_mcp_count}, above limit {direct.get('max_mcps', 2)}; sub-steward/MCP owner governance is required."
        )

    for skill_id in unmanaged_skills:
        issues.append(f"Skill {skill_id} is assigned to a non-active sub-steward.")

    max_sub_skills = sub_capacity.get("max_skills", 7)
    for steward, count in sorted(steward_counts.items()):
        if steward and steward != "pm-copilot-chief" and count > max_sub_skills:
            issues.append(f"Sub-steward {steward} manages {count} skills, above limit {max_sub_skills}.")

    if issues:
        return CheckResult("scaling_policy", "warn", f"{len(issues)} scaling recommendation(s).", issues)
    return CheckResult("scaling_policy", "pass", "Scaling policy is within limits.", [])
