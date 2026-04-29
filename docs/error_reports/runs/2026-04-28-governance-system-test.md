# Governance System Test - 2026-04-28

## Commands Run

| Command | Result |
|---|---|
| `python3 -m py_compile harness/*.py pm-prd-copilot/scripts/*.py ai-intel/scripts/*.py evals/*.py` | pass |
| workflow/action static drift scan | pass: `missing_actions: []`, `stage_mismatch: []` |
| `python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict` | pass |
| `python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --audit --efficiency --external-package pm-prd-copilot/templates/external_protected_development_document_template.md` | pass |
| steward capacity count | pass: `prd-writing-steward` has 4 active/candidate skills; `prototype-design-steward` has 4 |

## Review Finding Status

| Finding | Status | Evidence |
|---|---|---|
| Finding 1: workflow actions are not contract-checked | fixed / pass | `workflow_gate` passed and static scan found no missing actions. |
| Finding 2: harness misses workflow/action drift | fixed / pass | `harness/workflow_gate_checker.py` now checks workflow action registration, stage, steward, skill, reads, and writes. |
| Finding 3: production pipeline bypasses declared governance stages | open P2 | `pm-prd-copilot/scripts/run_pipeline.py` writes governance trace but does not read `workflow/prd_workflow.yaml` approvals. |
| Finding 4: PRD writing steward exceeds capacity | fixed / pass | `prd-writing-steward` has 4 active/candidate skills after prototype work moved to `prototype-design-steward`. |

## New Bugs

| ID | Severity | Summary | User approval needed |
|---|---|---|---|
| BUG-2026-04-28-001 | P2 | Production pipeline and governed workflow are still separate execution contracts. | Yes |

## Next Action Candidate

Choose one of these before implementation:

- Add a governed pipeline mode that reads `prd_workflow.yaml`, checks completed stages and approvals, and blocks formal delivery when gates are missing.
- Keep fast draft pipeline as-is, but label it draft-only and add a separate checker that fails if a formal run bypasses workflow gates.
- Leave current state temporarily and track the gap as open until the production pipeline is refactored.

## Notes

- No files were deleted, archived, committed, pushed, or reverted during this test.
- `projects/demo-project/runs/pipeline-latest/harness_report.json` was refreshed by the harness run.
