#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Any

from common import CheckResult, read_json, result_from_issues


ALLOWED_CURRENT_STATUSES = {"active", "cleared"}
ALLOWED_CACHE_STATUSES = {"active", "archived", "cleared"}
REQUIRED_CACHE_FILES = {"manifest.json", "approved_preferences.md", "candidate_preferences.md", "source_trace.json"}
REQUIRED_CURRENT_POLICY = {
    "scope": "project_only",
    "candidate_requires_approval": True,
    "cleared_cache_must_not_be_used": True,
    "do_not_store_secrets": True,
    "cross_project_reuse_allowed": False,
    "long_term_memory_requires_user_approval": True,
    "archive_alignment_required": True,
    "clear_after_project_archive_alignment": True,
    "store_in_project_closeout": True,
}
REQUIRED_ISOLATION_POLICY = {
    "scope": "project_only",
    "project_id_must_match": True,
    "do_not_read_other_project_caches": True,
    "reset_creates_new_cache_folder": True,
    "clear_disables_current_pointer": True,
    "cross_project_reuse_allowed": False,
    "long_term_memory_requires_user_approval": True,
    "archive_alignment_required": True,
    "clear_after_project_archive_alignment": True,
}


def _is_project_local(base_dir: Path, project_id: str, path_value: str) -> bool:
    if not path_value:
        return False
    path = Path(path_value)
    if path.is_absolute() or ".." in path.parts:
        return False
    expected_prefix = Path("memory-cache") / "projects" / project_id
    return path == expected_prefix or expected_prefix in path.parents


def _check_source_trace(project_id: str, cache_id: str, trace: dict[str, Any], issues: list[str]) -> None:
    if trace.get("project_id") != project_id:
        issues.append(f"{project_id}/{cache_id} source_trace project_id mismatch: {trace.get('project_id')}")
    if trace.get("cache_id") != cache_id:
        issues.append(f"{project_id}/{cache_id} source_trace cache_id mismatch: {trace.get('cache_id')}")
    for index, item in enumerate(trace.get("traces", []), start=1):
        for field in ["source_trace_id", "source_type", "source_ref", "captured_at", "human_verification_required"]:
            if item.get(field) in ("", None):
                issues.append(f"{project_id}/{cache_id} source_trace[{index}] missing {field}")
        if item.get("human_verification_required") is not True:
            issues.append(f"{project_id}/{cache_id} source_trace[{index}] must require human verification")


def _check_policy(prefix: str, policy: dict[str, Any], expected: dict[str, Any], issues: list[str]) -> None:
    if not isinstance(policy, dict):
        issues.append(f"{prefix} policy must be an object")
        return
    for key, value in expected.items():
        if policy.get(key) != value:
            issues.append(f"{prefix} policy.{key} must be {value!r}, got {policy.get(key)!r}")


def check_preference_caches(base_dir: Path) -> CheckResult:
    issues: list[str] = []
    root = base_dir / "memory-cache" / "projects"
    if not root.exists():
        return CheckResult("preference_cache", "pass", "No project preference caches found.", [])

    for project_dir in sorted(path for path in root.iterdir() if path.is_dir()):
        project_id = project_dir.name
        current_path = project_dir / "current.json"
        if not current_path.exists():
            issues.append(f"{project_id} missing current.json")
            continue
        current = read_json(current_path)
        if current.get("project_id") != project_id:
            issues.append(f"{project_id} current.json project_id mismatch: {current.get('project_id')}")
        status = current.get("status")
        if status not in ALLOWED_CURRENT_STATUSES:
            issues.append(f"{project_id} current.json invalid status: {status}")
        _check_policy(f"{project_id} current.json", current.get("policy", {}), REQUIRED_CURRENT_POLICY, issues)

        active_cache_id = current.get("active_cache_id")
        active_cache_path = current.get("active_cache_path")
        if status == "cleared":
            if active_cache_id or active_cache_path:
                issues.append(f"{project_id} cleared cache pointer must not have active cache fields")
            if current.get("user_approval_required") is not True:
                issues.append(f"{project_id} cleared cache must record user_approval_required=true")
            if current.get("user_approval_confirmed") is not True:
                issues.append(f"{project_id} cleared cache must record explicit user approval")
            continue

        if not active_cache_id:
            issues.append(f"{project_id} active cache pointer missing active_cache_id")
            continue
        if not _is_project_local(base_dir, project_id, str(active_cache_path)):
            issues.append(f"{project_id} active_cache_path must stay inside its project cache folder: {active_cache_path}")
            continue

        cache_dir = base_dir / str(active_cache_path)
        if not cache_dir.exists():
            issues.append(f"{project_id} active cache folder missing: {active_cache_path}")
            continue
        missing_files = sorted(name for name in REQUIRED_CACHE_FILES if not (cache_dir / name).exists())
        if missing_files:
            issues.append(f"{project_id}/{active_cache_id} missing cache files: {', '.join(missing_files)}")
            continue

        manifest = read_json(cache_dir / "manifest.json")
        if manifest.get("project_id") != project_id:
            issues.append(f"{project_id}/{active_cache_id} manifest project_id mismatch: {manifest.get('project_id')}")
        if manifest.get("cache_id") != active_cache_id:
            issues.append(f"{project_id}/{active_cache_id} manifest cache_id mismatch: {manifest.get('cache_id')}")
        if manifest.get("status") not in ALLOWED_CACHE_STATUSES:
            issues.append(f"{project_id}/{active_cache_id} manifest invalid status: {manifest.get('status')}")
        if manifest.get("status") != "active":
            issues.append(f"{project_id}/{active_cache_id} active pointer references non-active cache")
        _check_policy(
            f"{project_id}/{active_cache_id} manifest",
            manifest.get("isolation_policy", {}),
            REQUIRED_ISOLATION_POLICY,
            issues,
        )

        approved_text = (cache_dir / "approved_preferences.md").read_text(encoding="utf-8")
        candidate_text = (cache_dir / "candidate_preferences.md").read_text(encoding="utf-8")
        if "Project: `" in approved_text and f"Project: `{project_id}`" not in approved_text:
            issues.append(f"{project_id}/{active_cache_id} approved_preferences project header mismatch")
        if "Project: `" in candidate_text and f"Project: `{project_id}`" not in candidate_text:
            issues.append(f"{project_id}/{active_cache_id} candidate_preferences project header mismatch")
        if "do_not_store_secrets" not in current_path.read_text(encoding="utf-8"):
            issues.append(f"{project_id} current.json must include do_not_store_secrets policy")

        trace = read_json(cache_dir / "source_trace.json")
        _check_source_trace(project_id, active_cache_id, trace, issues)

    return result_from_issues("preference_cache", issues)
