#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

required_files=(
  "AGENTS.md"
  "03_internal_development_doc.md"
  "04_codex_development_doc.md"
  "05_codex_parallel_branch_development_doc.md"
  "06_api_spec.md"
  "07_database_schema.md"
  "08_backend_engineering_spec.md"
  "09_task_breakdown.md"
  "10_test_plan.md"
  "11_local_dev_runbook.md"
  "12_codex_thread_governance.md"
  "13_task_brief_template.md"
  "14_file_boundary_matrix.md"
  "15_failure_handling_protocol.md"
  "16_codex_execution_runbook.md"
  "17_sdd_engineering_lessons.md"
  "18_contract_change_request_template.md"
  "19_merge_review_checklist.md"
  "Makefile"
  "automation/thread_registry.md"
  "tasks/p0-spring-api.brief.md"
  "tasks/p0-quant-engine.brief.md"
  "tasks/p0-points.brief.md"
  "tasks/qa-gates.brief.md"
  "scripts/check-docs.sh"
  "scripts/check-compliance.sh"
  "scripts/check-contracts.sh"
  "scripts/check-prototype.sh"
  "scripts/check-thread-boundary.sh"
)

missing=0
for file in "${required_files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "missing required file: $file" >&2
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  exit 1
fi

if rg -n --glob '!scripts/**' --glob '!Makefile' "07_data_model|08_task_breakdown\\.md|09_test_plan\\.md" . >/tmp/aquant_old_refs.txt; then
  echo "old document references found:" >&2
  cat /tmp/aquant_old_refs.txt >&2
  rm -f /tmp/aquant_old_refs.txt
  exit 1
fi
rm -f /tmp/aquant_old_refs.txt

echo "check-docs passed"
