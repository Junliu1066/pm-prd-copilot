# Task Package Template

Use this template for each implementation slice or subagent handoff.

```text
Task ID:
Goal:

Inputs:
-

Context summary:
-

Allowed write paths:
-

Forbidden write paths:
-

Locked write paths:
-

Dependencies:
-

Contract status:
-

Module task brief:
module_name:
module_goal:
development_scope:
non_goals:
input_documents:
allowed_files:
forbidden_files:
locked_files:
dependency_modules:
affected_modules:
acceptance_criteria:
required_commands:
failure_handling:

A3 module development preflight:
status: pass | prepare_required | blocked
engineering_baseline:
module_contract:
file_boundary:
module_skeleton:
data_state_model:
test_skeleton:
quality_gate:
local_run_preflight:
required_preparation_fixes:
approval_needed:

Execution steps:
1.
2.
3.

Expected output:
-

Validation commands or manual checks:
-

Red / Green / Regression evidence required:
red_evidence:
green_evidence:
regression_evidence:
not_applicable_reason:

Acceptance criteria:
-

Rollback:
-

Module B quality gate required before integration or closeout:
-

Module B architecture feedback required after module/thread self-check:
-

Human confirmation points:
-

Approval request when blocked:
decision_needed:
trigger:
risk:
options:
recommended_option:
default_safe_action:
resume_condition:

Minimum acceptable fix:
-

Evidence required:
-
```

## Scope Change Request

Use this when the task needs to exceed its allowed write paths or requirement scope.

```text
Requested change:
Reason:
Current allowed scope:
Required new scope:
Risk:
Options:
- extend current task
- create new task
- defer
- ask upstream owner
Recommendation:
```
