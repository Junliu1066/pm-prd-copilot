#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from pathlib import Path

from common import CheckResult, load_yaml


def check_scaling_policy(base_dir: Path) -> CheckResult:
    policy = load_yaml(base_dir / "governance" / "steward_scaling_policy.yaml")
    skills = load_yaml(base_dir / "registry" / "skills.yaml").get("skills", {})
    mcps = load_yaml(base_dir / "registry" / "mcps.yaml").get("mcps", {})

    active_or_candidate_skills = {
        skill_id: skill for skill_id, skill in skills.items() if skill.get("status") in {"active", "candidate"}
    }
    active_or_candidate_mcps = {
        mcp_id: mcp for mcp_id, mcp in mcps.items() if mcp.get("status") in {"active", "candidate"}
    }

    issues: list[str] = []
    direct = policy.get("direct_management", {})
    create_sub = policy.get("create_sub_steward_when", {})
    sub_capacity = policy.get("sub_steward_capacity", {})

    skill_count = len(active_or_candidate_skills)
    mcp_count = len(active_or_candidate_mcps)

    if skill_count > direct.get("max_skills", 5):
        issues.append(
            f"Chief steward direct skill load is {skill_count}, above limit {direct.get('max_skills', 5)}; sub-steward governance is required."
        )
    if mcp_count > direct.get("max_mcps", 2):
        issues.append(
            f"Chief steward direct MCP load is {mcp_count}, above limit {direct.get('max_mcps', 2)}; sub-steward/MCP owner governance is required."
        )

    stage_counts = Counter(skill.get("stage") for skill in active_or_candidate_skills.values())
    threshold = create_sub.get("domain_skill_count_gte", 3)
    for stage, count in sorted(stage_counts.items()):
        if count >= threshold:
            issues.append(f"Stage {stage} has {count} skills, meeting threshold {threshold} for a sub-steward.")

    steward_counts = Counter(skill.get("steward") for skill in active_or_candidate_skills.values())
    max_sub_skills = sub_capacity.get("max_skills", 7)
    for steward, count in sorted(steward_counts.items()):
        if steward and steward != "pm-copilot-chief" and count > max_sub_skills:
            issues.append(f"Sub-steward {steward} manages {count} skills, above limit {max_sub_skills}.")

    if issues:
        return CheckResult("scaling_policy", "warn", f"{len(issues)} scaling recommendation(s).", issues)
    return CheckResult("scaling_policy", "pass", "Scaling policy is within limits.", [])
