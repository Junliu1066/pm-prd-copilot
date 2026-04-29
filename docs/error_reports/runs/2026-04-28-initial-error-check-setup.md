# Initial Error Check Setup - 2026-04-28

## Commands Run

| Command | Result |
|---|---|
| `git diff --check -- docs/error_reports README.md docs/daily_report_template.md docs/repository_map.md docs/operating_model.md` | pass |
| `python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict` | pass |
| `python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory` | pass |

## New Bugs

None found in this setup check.

## Repeated Bugs

None found in this setup check.

## Fixed Bugs

None in this setup check.

## Watch Items

- `projects/demo-project/runs/pipeline-latest/harness_report.json` was refreshed by the harness run.
- The repository already contains unrelated pending changes from earlier governance work; they were not reverted or cleaned in this setup step.

## Solution Recommendations

- Keep using the existing regression and harness commands for overnight checks.
- If future reports find failures, record the smallest safe fix, validation command, and user approval requirement before changing stable governance.

## User Approval Needed

None for this setup record. Future delete/archive/fix actions from nightly reports still require user approval when they affect stable governance, Skill/Harness/Steward, model provider, external data source, publishing, or cleanup behavior.
