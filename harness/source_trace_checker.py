#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from common import CheckResult, load_yaml, read_json, result_from_issues


def check_source_traces(base_dir: Path, project: str) -> CheckResult:
    issues: list[str] = []
    policies = load_yaml(base_dir / "workflow" / "policies.yaml")
    required = set(policies.get("source_policy", {}).get("required_trace_fields", []))
    project_dir = base_dir / "projects" / project
    state = read_json(project_dir / "project_state.json")
    run_id = state.get("last_run_id")
    if not run_id:
        return CheckResult("source_trace", "pass", "No run trace found; source trace check skipped.", [])

    trace = read_json(project_dir / "runs" / run_id / "trace.json")
    source_traces = trace.get("source_traces", [])
    if trace.get("mcp_calls") and not source_traces:
        issues.append("Trace includes MCP calls but no source_traces.")

    for index, source in enumerate(source_traces, start=1):
        missing = sorted(field for field in required if field not in source or source.get(field) in ("", None))
        if missing:
            issues.append(f"source_traces[{index}] missing fields: {', '.join(missing)}")
        if source.get("human_verification_required") is not True:
            issues.append(f"source_traces[{index}] must mark human_verification_required=true")

    return result_from_issues("source_trace", issues)
