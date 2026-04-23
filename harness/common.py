#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml


VALID_STATUSES = {"draft", "candidate", "active", "deprecated", "archived"}
VALID_RESULT_STATUSES = {"pass", "warn", "fail"}


@dataclass
class CheckResult:
    check: str
    status: str
    message: str
    details: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return data


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def overall_status(results: list[CheckResult], mode: str) -> str:
    if any(result.status == "fail" for result in results):
        return "fail"
    if any(result.status == "warn" for result in results):
        return "warn" if mode == "advisory" else "fail"
    return "pass"


def result_from_issues(check: str, issues: list[str], *, warn_only: bool = False) -> CheckResult:
    if issues:
        return CheckResult(
            check=check,
            status="warn" if warn_only else "fail",
            message=f"{len(issues)} issue(s) found.",
            details=issues,
        )
    return CheckResult(check=check, status="pass", message="No issues found.", details=[])
