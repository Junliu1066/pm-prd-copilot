#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from common import CheckResult, load_yaml, read_json, result_from_issues


ALLOWED_PROPOSAL_STATUSES = {"proposed", "approved", "rejected", "applied"}


def check_skill_update_proposals(base_dir: Path) -> CheckResult:
    issues: list[str] = []
    proposal_dir = base_dir / "pm-prd-copilot" / "proposals" / "skill-patches"
    if not proposal_dir.exists():
        return CheckResult(
            check="skill_update_proposal",
            status="pass",
            message="No skill update proposals found.",
            details=[],
        )

    skills = load_yaml(base_dir / "registry" / "skills.yaml").get("skills", {})
    proposal_files = sorted(proposal_dir.glob("skill-update-*.json"))
    for proposal_file in proposal_files:
        proposal = read_json(proposal_file)
        proposal_id = proposal.get("proposal_id", proposal_file.name)
        status = proposal.get("status")
        if status not in ALLOWED_PROPOSAL_STATUSES:
            issues.append(f"{proposal_id} has invalid status: {status}")
        if proposal.get("requires_human_approval") is not True:
            issues.append(f"{proposal_id} must require human approval.")
        if proposal.get("must_not_apply_automatically") is not True and status != "applied":
            issues.append(f"{proposal_id} must not be applied automatically.")
        if status == "applied" and not proposal.get("approved_by"):
            issues.append(f"{proposal_id} is applied without approved_by.")
        for lesson in proposal.get("source_lessons", []):
            source_file = str(lesson.get("source_file", ""))
            if Path(source_file).is_absolute():
                issues.append(f"{proposal_id} source_file must be relative: {source_file}")

        for update in proposal.get("skill_updates", []):
            skill_id = update.get("skill")
            skill = skills.get(skill_id)
            if not skill:
                issues.append(f"{proposal_id} routes to unknown skill: {skill_id}")
                continue
            expected_path = skill.get("path")
            if update.get("path") != expected_path:
                issues.append(f"{proposal_id} has stale path for {skill_id}: {update.get('path')}")
            if not expected_path or not (base_dir / expected_path / "SKILL.md").exists():
                issues.append(f"{proposal_id} target skill file is missing: {skill_id}")
            if update.get("requires_human_approval") is not True:
                issues.append(f"{proposal_id} update for {skill_id} must require human approval.")
            if update.get("must_not_apply_automatically") is not True:
                issues.append(f"{proposal_id} update for {skill_id} must not apply automatically.")

    return result_from_issues("skill_update_proposal", issues)
