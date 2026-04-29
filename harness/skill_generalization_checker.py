#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Any

from common import CheckResult, load_yaml, read_json, write_json


TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".txt"}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _skill_text_files(base_dir: Path) -> list[Path]:
    skills = load_yaml(base_dir / "registry" / "skills.yaml").get("skills", {})
    paths: list[Path] = []
    for skill in skills.values():
        skill_path = skill.get("path")
        if not skill_path:
            continue
        root = base_dir / str(skill_path)
        if not root.exists():
            continue
        for file_path in root.rglob("*"):
            if file_path.is_file() and file_path.suffix in TEXT_SUFFIXES:
                paths.append(file_path)
    return sorted(set(paths))


def _scan_text(text: str, terms: list[dict[str, Any]], source: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for item in terms:
        term = str(item.get("term", ""))
        if term and term in text:
            findings.append(
                {
                    "source": source,
                    "term": term,
                    "leakage_type": str(item.get("leakage_type", "project_preference")),
                    "severity": str(item.get("severity", "fail")),
                }
            )
    return findings


def _proposal_behavior_texts(base_dir: Path, fields: list[str]) -> list[tuple[str, str]]:
    proposal_dir = base_dir / "pm-prd-copilot" / "proposals" / "skill-patches"
    if not proposal_dir.exists():
        return []
    texts: list[tuple[str, str]] = []
    for proposal_file in sorted(proposal_dir.glob("skill-update-*.json")):
        proposal = read_json(proposal_file)
        proposal_id = proposal.get("proposal_id", proposal_file.name)
        for index, update in enumerate(_as_list(proposal.get("skill_updates", [])), start=1):
            parts = [str(update.get(field, "")) for field in fields]
            texts.append((f"{proposal_id}:skill_updates[{index}]", "\n".join(parts)))
    return texts


def check_skill_generalization(
    base_dir: Path,
    project: str,
    *,
    run_id: str | None = None,
    write_report: bool = True,
) -> CheckResult:
    config_path = base_dir / "evals" / "generalization_audit.yaml"
    if not config_path.exists():
        return CheckResult("skill_generalization", "fail", "Missing evals/generalization_audit.yaml.", [])

    config = load_yaml(config_path)
    policy = config.get("scan_policy", {})
    blocked_terms = _as_list(policy.get("blocked_terms", []))
    proposal_fields = [str(field) for field in _as_list(policy.get("skill_update_proposal_fields", []))]
    findings: list[dict[str, str]] = []

    if policy.get("active_skill_files", True):
        for file_path in _skill_text_files(base_dir):
            text = file_path.read_text(encoding="utf-8")
            source = str(file_path.relative_to(base_dir))
            findings.extend(_scan_text(text, blocked_terms, source))

    for source, text in _proposal_behavior_texts(base_dir, proposal_fields):
        findings.extend(_scan_text(text, blocked_terms, source))

    issues = [
        f"{finding['severity']}: {finding['leakage_type']} term '{finding['term']}' found in {finding['source']}"
        for finding in findings
        if finding["severity"] == "fail"
    ]
    warnings = [
        f"{finding['severity']}: {finding['leakage_type']} term '{finding['term']}' found in {finding['source']}"
        for finding in findings
        if finding["severity"] != "fail"
    ]

    effective_run_id = run_id or read_json(base_dir / "projects" / project / "project_state.json").get("last_run_id")
    if write_report and effective_run_id:
        report_path = base_dir / "projects" / project / "runs" / effective_run_id / "skill_generalization_audit.json"
        write_json(
            report_path,
            {
                "run_id": effective_run_id,
                "project_id": project,
                "status": "fail" if issues else "warn" if warnings else "pass",
                "findings": findings,
                "required_routing": config.get("required_routing", {}),
            },
        )

    if issues:
        return CheckResult("skill_generalization", "fail", f"{len(issues)} generalization issue(s).", issues)
    if warnings:
        return CheckResult("skill_generalization", "warn", f"{len(warnings)} generalization warning(s).", warnings)
    return CheckResult("skill_generalization", "pass", "No project-specific leakage found in reusable skill behavior.", [])
