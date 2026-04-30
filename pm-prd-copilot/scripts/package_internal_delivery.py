#!/usr/bin/env python3
"""Build a trusted internal delivery package for a project."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path


TOP_LEVEL_SUFFIXES = {".md", ".json"}
SUPPORT_DIRS = ["analysis", "ai", "delivery", "prototype", "governance", "closeout"]
SKIP_NAMES = {".DS_Store", "__pycache__"}
SKIP_SUFFIXES = {".zip", ".pyc"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def should_copy(path: Path) -> bool:
    if path.name in SKIP_NAMES or path.name.startswith("."):
        return False
    return path.suffix.lower() not in SKIP_SUFFIXES


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_file(src: Path, dst: Path, root: Path, copied: list[str]) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    copied.append(str(dst.relative_to(root)))


def copy_tree(src_dir: Path, dst_dir: Path, root: Path, copied: list[str]) -> None:
    for src in sorted(src_dir.rglob("*")):
        if not src.is_file() or not should_copy(src):
            continue
        copy_file(src, dst_dir / src.relative_to(src_dir), root, copied)


def collect_project_docs(project_dir: Path) -> list[Path]:
    docs: list[Path] = []
    for path in sorted(project_dir.iterdir()):
        if path.is_file() and should_copy(path) and path.suffix.lower() in TOP_LEVEL_SUFFIXES:
            docs.append(path)
    return docs


def build_readme(project_dir: Path, copied: list[str], *, include_runs: bool) -> str:
    project_id = project_dir.name
    lines = [
        f"# Internal Delivery Package - {project_id}",
        "",
        f"- Generated at: `{utc_now()}`",
        "- Audience: trusted internal owner or trusted implementation team",
        "- Boundary: internal package, not an external B execution package",
        "- External sharing: use the protected B package workflow instead",
        "",
        "## Contents",
    ]
    lines.extend(f"- `{item}`" for item in copied[:120])
    if len(copied) > 120:
        lines.append(f"- ... {len(copied) - 120} more file(s), see MANIFEST.json")
    lines.extend(
        [
            "",
            "## Safety Notes",
            "- This package may include internal planning, prototype, closeout, or governance-adjacent materials.",
            "- Do not share this package externally without a separate redaction review.",
            "- This package intentionally excludes existing zip files and project preference caches.",
            f"- `runs/` included: `{str(include_runs).lower()}`.",
        ]
    )
    return "\n".join(lines)


def zip_dir(src_dir: Path, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        out_path.unlink()
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(src_dir.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(src_dir))


def build_package(project_dir: Path, output: Path, *, include_runs: bool = False) -> dict[str, object]:
    if not project_dir.exists() or not project_dir.is_dir():
        raise SystemExit(f"Project directory not found: {project_dir}")

    copied: list[str] = []
    with tempfile.TemporaryDirectory(prefix="internal-package-") as tmp:
        root = Path(tmp)
        docs_dir = root / "docs"
        docs_dir.mkdir(parents=True, exist_ok=True)

        for src in collect_project_docs(project_dir):
            copy_file(src, docs_dir / src.name, root, copied)

        for dirname in SUPPORT_DIRS:
            src_dir = project_dir / dirname
            if src_dir.exists():
                copy_tree(src_dir, root / dirname, root, copied)

        if include_runs and (project_dir / "runs").exists():
            copy_tree(project_dir / "runs", root / "runs", root, copied)

        manifest = {
            "schema_version": "internal_delivery_package.v1",
            "project_id": project_dir.name,
            "generated_at": utc_now(),
            "source_project_dir": str(project_dir),
            "package_type": "trusted_internal",
            "include_runs": include_runs,
            "excluded_by_default": ["memory-cache", "existing zip files", "hidden files", "__pycache__"],
            "files": copied,
        }
        write_json(root / "MANIFEST.json", manifest)
        write_text(root / "README.md", build_readme(project_dir, copied, include_runs=include_runs))
        zip_dir(root, output)

    return {"output": str(output), "file_count": len(copied), "include_runs": include_runs}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a trusted internal delivery package.")
    parser.add_argument("--project-dir", required=True, help="Project directory.")
    parser.add_argument("--output", required=True, help="Output zip path.")
    parser.add_argument("--include-runs", action="store_true", help="Include project run artifacts.")
    args = parser.parse_args()

    result = build_package(Path(args.project_dir).resolve(), Path(args.output).resolve(), include_runs=args.include_runs)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
