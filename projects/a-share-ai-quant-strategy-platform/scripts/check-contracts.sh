#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

require_in_file() {
  local file="$1"
  local pattern="$2"
  if ! rg -n "$pattern" "$file" >/dev/null; then
    echo "missing contract marker in $file: $pattern" >&2
    exit 1
  fi
}

require_in_file "06_api_spec.md" "Idempotency-Key"
require_in_file "06_api_spec.md" "POINTS_NOT_ENOUGH"
require_in_file "06_api_spec.md" "research_only"
require_in_file "06_api_spec.md" "simulation_only"

require_in_file "07_database_schema.md" "CREATE TABLE users"
require_in_file "07_database_schema.md" "CREATE TABLE point_accounts"
require_in_file "07_database_schema.md" "CREATE TABLE backtest_runs"
require_in_file "07_database_schema.md" "V001__create_users_and_auth.sql"

require_in_file "08_backend_engineering_spec.md" "Spring Boot 3.x"
require_in_file "08_backend_engineering_spec.md" "Spring Security"
require_in_file "08_backend_engineering_spec.md" "GlobalExceptionHandler"

require_in_file "09_task_breakdown.md" "codex/p0-spring-api"
require_in_file "09_task_breakdown.md" "codex/p0-quant-engine"
require_in_file "09_task_breakdown.md" "codex/p0-points"

require_in_file "10_test_plan.md" "上线前最低门禁"
require_in_file "11_local_dev_runbook.md" "make check-all"
require_in_file "12_codex_thread_governance.md" "文件锁规则"
require_in_file "13_task_brief_template.md" "Allowed Paths"
require_in_file "14_file_boundary_matrix.md" "write"
require_in_file "15_failure_handling_protocol.md" "API 漂移"
require_in_file "16_codex_execution_runbook.md" "make check-all"
require_in_file "16_codex_execution_runbook.md" "make check-boundary"
require_in_file "18_contract_change_request_template.md" "Contract Change Request"
require_in_file "19_merge_review_checklist.md" "THREAD=<branch> make check-boundary"
require_in_file "automation/thread_registry.md" "thread_id"
require_in_file "tasks/p0-spring-api.brief.md" "THREAD=codex/p0-spring-api make check-boundary"
require_in_file "tasks/p0-quant-engine.brief.md" "research_only"
require_in_file "tasks/p0-points.brief.md" "POINTS_NOT_ENOUGH"
require_in_file "tasks/qa-gates.brief.md" "make check-all"

echo "check-contracts passed"
