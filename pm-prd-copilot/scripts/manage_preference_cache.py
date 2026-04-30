#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


PROJECT_CACHE_POLICY = {
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

ISOLATION_POLICY = {
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


def now_id() -> str:
    return datetime.now(timezone.utc).strftime("cache-%Y%m%dT%H%M%SZ")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def init_cache(base_dir: Path, project: str, *, reason: str, reset: bool = False) -> Path:
    cache_id = now_id()
    project_dir = base_dir / "memory-cache" / "projects" / project
    cache_dir = project_dir / cache_id
    cache_dir.mkdir(parents=True, exist_ok=False)
    created_at = datetime.now(timezone.utc).isoformat()
    write_json(
        project_dir / "current.json",
        {
            "project_id": project,
            "status": "active",
            "active_cache_id": cache_id,
            "active_cache_path": str(cache_dir.relative_to(base_dir)),
            "created_at": created_at,
            "updated_at": created_at,
            "operation": "reset" if reset else "create",
            "policy": PROJECT_CACHE_POLICY,
        },
    )
    write_json(
        cache_dir / "manifest.json",
        {
            "project_id": project,
            "cache_id": cache_id,
            "status": "active",
            "created_at": created_at,
            "reason": reason,
            "approved_preferences_path": "approved_preferences.md",
            "candidate_preferences_path": "candidate_preferences.md",
            "source_trace_path": "source_trace.json",
            "isolation_policy": ISOLATION_POLICY,
        },
    )
    (cache_dir / "approved_preferences.md").write_text(
        f"# Approved Preferences\n\nProject: `{project}`\nCache: `{cache_id}`\n\n",
        encoding="utf-8",
    )
    (cache_dir / "candidate_preferences.md").write_text(
        f"# Candidate Preferences\n\nProject: `{project}`\nCache: `{cache_id}`\n\n",
        encoding="utf-8",
    )
    write_json(cache_dir / "source_trace.json", {"project_id": project, "cache_id": cache_id, "traces": []})
    return cache_dir


def clear_cache(base_dir: Path, project: str, *, reason: str, approved_by_user: bool) -> None:
    project_dir = base_dir / "memory-cache" / "projects" / project
    current_path = project_dir / "current.json"
    current = json.loads(current_path.read_text(encoding="utf-8")) if current_path.exists() else {}
    cleared_at = datetime.now(timezone.utc).isoformat()
    write_json(
        current_path,
        {
            "project_id": project,
            "status": "cleared",
            "active_cache_id": None,
            "active_cache_path": None,
            "cleared_at": cleared_at,
            "clear_reason": reason,
            "previous_active_cache_id": current.get("active_cache_id"),
            "user_approval_required": True,
            "user_approval_confirmed": approved_by_user,
            "policy": PROJECT_CACHE_POLICY,
        },
    )


def archive_clear_cache(
    base_dir: Path,
    project: str,
    *,
    reason: str,
    approved_by_user: bool,
    archive_dir: Path | None = None,
) -> Path:
    project_dir = base_dir / "memory-cache" / "projects" / project
    current_path = project_dir / "current.json"
    current = json.loads(current_path.read_text(encoding="utf-8")) if current_path.exists() else {}
    archive_root = archive_dir or (base_dir / "projects" / project / "closeout")
    archive_root.mkdir(parents=True, exist_ok=True)
    disposition_path = archive_root / "preference-memory-disposition.json"
    active_cache_path = current.get("active_cache_path")
    active_manifest = {}
    if active_cache_path:
        manifest_path = base_dir / str(active_cache_path) / "manifest.json"
        if manifest_path.exists():
            active_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    write_json(
        disposition_path,
        {
            "project_id": project,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "reason": reason,
            "policy": PROJECT_CACHE_POLICY,
            "current_before_clear": current,
            "active_manifest_before_clear": active_manifest,
            "user_approval_required": True,
            "user_approval_confirmed": approved_by_user,
            "required_user_alignment": [
                "clear project-only preferences after archive alignment",
                "keep project evidence only in the closeout package",
                "move anything to long-term memory only after explicit user approval",
            ],
        },
    )
    clear_cache(base_dir, project, reason=reason, approved_by_user=approved_by_user)
    return disposition_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage project-scoped preference caches.")
    parser.add_argument("--base-dir", default=".")
    parser.add_argument("--project", required=True)
    parser.add_argument("--reason", default="")
    parser.add_argument("--archive-dir", default="")
    parser.add_argument(
        "--approved-by-user",
        action="store_true",
        help="Required for clear/archive-clear after explicit user approval.",
    )
    parser.add_argument("operation", choices=["init", "reset", "clear", "archive-clear"])
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    if args.operation in {"clear", "archive-clear"} and not args.approved_by_user:
        parser.error("clear/archive-clear requires --approved-by-user after explicit user approval.")

    if args.operation in {"init", "reset"}:
        cache_dir = init_cache(
            base_dir,
            args.project,
            reason=args.reason or args.operation,
            reset=args.operation == "reset",
        )
        print(cache_dir)
    elif args.operation == "clear":
        clear_cache(
            base_dir,
            args.project,
            reason=args.reason or "user requested clear",
            approved_by_user=args.approved_by_user,
        )
        print(base_dir / "memory-cache" / "projects" / args.project / "current.json")
    else:
        archive_dir = Path(args.archive_dir).resolve() if args.archive_dir else None
        disposition_path = archive_clear_cache(
            base_dir,
            args.project,
            reason=args.reason or "project archive alignment completed",
            approved_by_user=args.approved_by_user,
            archive_dir=archive_dir,
        )
        print(disposition_path)


if __name__ == "__main__":
    main()
