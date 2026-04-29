#!/usr/bin/env python3
"""Check B-package files for protected framework leakage."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import CheckResult


TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".html",
    ".css",
    ".js",
    ".json",
    ".yaml",
    ".yml",
    ".csv",
}


def load_blocked_terms(path: Path) -> list[str]:
    terms: list[str] = []
    in_terms = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line == "blocked_terms:":
            in_terms = True
            continue
        if in_terms and line.endswith(":") and not line.startswith("-"):
            break
        if in_terms and line.startswith("-"):
            terms.append(line[1:].strip().strip('"').strip("'"))
    return [term for term in terms if term]


def iter_text_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root] if root.suffix in TEXT_SUFFIXES else []
    files: list[Path] = []
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            files.append(path)
    return files


def check_external_redaction(base_dir: Path, target: Path, terms_path: Path | None = None) -> CheckResult:
    resolved_target = target if target.is_absolute() else base_dir / target
    resolved_terms = terms_path or base_dir / "pm-prd-copilot" / "rules" / "redaction_terms.yaml"

    issues: list[str] = []
    if not resolved_target.exists():
        return CheckResult(
            check="external_redaction",
            status="fail",
            message="Target not found.",
            details=[str(resolved_target)],
        )
    if not resolved_terms.exists():
        return CheckResult(
            check="external_redaction",
            status="fail",
            message="Terms file not found.",
            details=[str(resolved_terms)],
        )

    terms = load_blocked_terms(resolved_terms)
    for path in iter_text_files(resolved_target):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            for term in terms:
                if term in line:
                    issues.append(f"{path}:{lineno}: blocked term `{term}`")

    if issues:
        return CheckResult(
            check="external_redaction",
            status="fail",
            message=f"{len(issues)} protected-term leak(s) found.",
            details=issues,
        )
    return CheckResult(check="external_redaction", status="pass", message="No protected terms found.", details=[])


def main() -> int:
    parser = argparse.ArgumentParser(description="Check B-package files for protected framework leakage.")
    parser.add_argument("target", help="File or directory to scan.")
    parser.add_argument(
        "--terms",
        default="pm-prd-copilot/rules/redaction_terms.yaml",
        help="Path to redaction terms yaml.",
    )
    args = parser.parse_args()

    result = check_external_redaction(Path(".").resolve(), Path(args.target), Path(args.terms))
    if result.status != "pass":
        output = sys.stdout if "protected-term" in result.message else sys.stderr
        for detail in result.details:
            print(detail, file=output)
        return 2 if "not found" in result.message.lower() else 1

    print("B-package redaction check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
