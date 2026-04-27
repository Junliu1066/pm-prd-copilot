#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

from common import CheckResult, result_from_issues


RUNTIME_POINTER = "<!-- codex-runtime: apply governance/runtime/artifact_controls/index.md when updating this artifact -->"

DEVELOPMENT_DOC_PATTERNS = (
    "*development_design*.md",
    "*development_document*.md",
    "*开发文档*.md",
)

PROJECT_DOC_PATTERNS = (
    "*.md",
)

INTERNAL_GOVERNANCE_TERMS = (
    "steward routing",
    "efficiency policy",
    "teaching policy",
    "runtime controls",
    "artifact controls",
    "多管家",
    "效率管家",
    "Teaching 管家",
    "内部治理",
)


def _iter_project_markdown(project_dir: Path) -> list[Path]:
    if not project_dir.exists():
        return []
    paths: set[Path] = set()
    for pattern in PROJECT_DOC_PATTERNS:
        paths.update(project_dir.glob(pattern))
    return sorted(path for path in paths if path.is_file())


def _iter_development_docs(project_dir: Path) -> list[Path]:
    if not project_dir.exists():
        return []
    paths: set[Path] = set()
    for pattern in DEVELOPMENT_DOC_PATTERNS:
        paths.update(project_dir.glob(pattern))
    return sorted(path for path in paths if path.is_file())


def _visible_text(markdown: str) -> str:
    return re.sub(r"<!--.*?-->", "", markdown, flags=re.DOTALL)


def check_runtime_controls(base_dir: Path, project: str) -> CheckResult:
    issues: list[str] = []

    runtime_index = base_dir / "governance" / "runtime" / "index.md"
    triggers = base_dir / "governance" / "runtime" / "triggers.yaml"
    boundaries = base_dir / "governance" / "runtime" / "document_boundaries.md"
    template = base_dir / "pm-prd-copilot" / "templates" / "codex_development_document_template.md"

    for required in (runtime_index, triggers, boundaries, template):
        if not required.exists():
            issues.append(f"Missing runtime control file: {required.relative_to(base_dir)}")

    if template.exists() and RUNTIME_POINTER not in template.read_text(encoding="utf-8"):
        issues.append("Codex development document template is missing runtime pointer.")

    project_dir = base_dir / "projects" / project
    for path in _iter_development_docs(project_dir):
        text = path.read_text(encoding="utf-8")
        if path.name.endswith(".final.md") and RUNTIME_POINTER not in text:
            issues.append(f"Final development document missing runtime pointer: {path.relative_to(base_dir)}")

    for path in _iter_project_markdown(project_dir):
        text = _visible_text(path.read_text(encoding="utf-8"))
        lower_text = text.lower()
        exposed_terms = []
        for term in INTERNAL_GOVERNANCE_TERMS:
            haystack = lower_text if term.isascii() else text
            needle = term.lower() if term.isascii() else term
            if needle in haystack:
                exposed_terms.append(term)
        if exposed_terms:
            issues.append(
                f"Project artifact may expose runtime governance terms: {path.relative_to(base_dir)} "
                f"({', '.join(sorted(set(exposed_terms)))})"
            )

    return result_from_issues("runtime_controls", issues, warn_only=True)
