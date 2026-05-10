# Development Testing Execution Template

## Contents

- Development Task
- Inputs
- Module A: Engineering Feasibility, Orchestration, And Preflight
- Development And Test Scope
- Impact and Upstream Approval
- Task Packages
- Validation
- Module B: Quality Stability Gate
- Rollback
- Execution Conclusion

## Development Task

| Field | Content |
|---|---|
| Current task |  |
| Reason |  |
| Expected verifiable effect |  |
| Out of scope |  |

## Inputs

| Input | Path / source | Status |
|---|---|---|
| Requirement boundary / acceptance |  | confirmed / draft / missing |
| Codex development document |  | confirmed / draft / missing |
| Prototype / flow |  | confirmed / draft / missing |
| Code context |  | inspected / missing |
| Test command |  | runnable / unknown |

## Facts, Assumptions, Questions

| Type | Item | Handling |
|---|---|---|
| Fact |  |  |
| Assumption |  | Validate by  |
| P0 blocker |  | Stop and ask |
| P1 question |  | Proceed with assumption |
| P2 follow-up |  | Track for later |

## Module A: Engineering Feasibility, Orchestration, And Preflight

```text
engineering_feasibility_review:
  status: pass | needs_revision | blocked
  blockers:
  missing_information:
  ambiguity:
  risk:
  required_document_fixes:
  recommendation:
```

Run orchestration only when the review status is `pass`.

Decision rules: `pass` requires clear goal, scope, interfaces, data flow, state flow, contract, tests, acceptance, rollback, and no unapproved L3 risk. Use `needs_revision` for missing or ambiguous low-risk information. Use `blocked` for contract, DB, model, MCP, publishing, stable governance, long-term memory, permission, or security boundaries.

```text
development_mainline_card:
thread_matrix:
thread_startup_packages:
write_boundary_table:
dependency_table:
contract_freeze_table:
dynamic_skill_harness_plan:
validation_plan:
integration_plan:
rollback_plan:
approval_points:
```

Keep single-thread execution unless independent write scopes, frozen contracts, integration gates, and failure return paths are clear.

```text
dynamic_skill_harness_plan:
  trigger:
  candidate_skill_or_harness:
  use_or_skip:
  reason:
  command_or_reference:
  expected_evidence:
  result:
  follow_up:
```

Run A3 after A2 and before module business implementation.

```text
module_development_preflight:
  status: pass | prepare_required | blocked
  module_task_brief:
  engineering_baseline:
  module_contract:
  file_boundary:
  module_skeleton:
  data_state_model:
  test_skeleton:
  quality_gate:
  local_run_preflight:
  forbidden_actions_check:
  required_preparation_fixes:
  approval_needed:
```

```text
module_task_brief:
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
```

A3 decision rules: `pass` requires Task Brief, baseline, contract, file boundary, skeleton, data/state model, test skeleton, quality gate, local run preflight, and failure handling. Use `prepare_required` for safe missing preparation such as smoke test, skeleton, test entrypoint, local run notes, or baseline record. Use `blocked` for missing/changing contract, locked path changes, DB migration, permission framework, common response body, global exception handling, MCP, model, stable governance, publishing, or other high-risk boundaries.

Baseline defaults to `git status` and `make check-all`. If `make check-all` is unavailable, record `unavailable` and choose an alternative from A2 `validation_plan`. Do not proceed when no executable baseline exists.

Contract must cover API paths, request fields, response fields, error codes, permission rules, idempotency, pagination, state enums, audit log requirements, database tables/fields, and cross-module calls. Do not invent interfaces, fields, or state while coding; use Contract Change Request when contract changes are needed.

Locked paths include DB migration, common response body, permission framework, global exception handling, common utilities, global architecture files, PRD/prototype files, and contract docs unless explicitly approved.

## Development And Test Scope

| Module | Goal | Change | Acceptance |
|---|---|---|---|
|  |  |  |  |

## Non-Goals

-

## Impact and Upstream Approval

| Surface | Involved | Handling |
|---|---|---|
| UI / client |  | implement / report blocker |
| API / service |  | implement / report blocker |
| DB / migration |  | stop unless approved |
| AI / model / prompt |  | implement approved plan only |
| External API / MCP |  | stop unless approved |
| GitHub / release |  | stop unless approved |
| stable skill / harness / memory |  | out of scope |

```text
approval_request:
  decision_needed:
  trigger:
  risk:
  options:
  recommended_option:
  default_safe_action:
  resume_condition:
```

## Task Packages

| ID | Goal | Allowed writes | Forbidden writes | Validation | Approval |
|---|---|---|---|---|---|
| T1 |  |  |  |  |  |

## Validation

| Check | Command / method | Result |
|---|---|---|
| syntax / format |  | not run |
| unit / integration |  | not run |
| manual UI / API |  | not run |
| regression |  | not run |
| red |  | not run / not applicable |
| green |  | not run / not applicable |

## Module B: Quality Stability Gate

```text
quality_stability_gate:
  status: pass | fix_required | blocked
  findings:
  test_gaps:
  red_green_test:
    red_evidence:
    green_evidence:
    regression_evidence:
    not_applicable_reason:
  contract_risks:
  boundary_violations:
  required_fixes:
  integration_readiness:
  rollback_route:
  approval_needed:
  architecture_feedback:
    bug_patterns:
    architecture_issues:
    prevention_rules:
    reusable_checks:
    upstream_architecture_actions:
```

Check `diff_scope_check`, `task_completion_check`, `bug_regression_check`, `contract_integrity_check`, `test_evidence_check`, `red_green_test_check`, `boundary_check`, `maintainability_check`, `rollback_readiness_check`, `integration_readiness_check`, and `architecture_feedback_check` before integration and closeout.

Automatically run Module B after every module or thread finishes development and self-check. Record discovered bugs, recurring failure patterns, architecture issues, contract risks, prevention rules, reusable checks, and upstream architecture actions as project-level architecture feedback. Do not convert this feedback into stable memory, registry, workflow, skill, harness, or contract changes without explicit approval.

Decision rules: `pass` requires task completion, scoped diff, contract integrity, Red / Green / Regression evidence or a valid not-applicable reason, sufficient test or substitute evidence, no blocking risk, and rollback route. Use `fix_required` for ordinary bugs, missing tests, missing Red / Green / Regression evidence, implementation gaps, or maintainability issues that can be fixed inside the responsible thread. Use `blocked` for requirement, contract, DB, model, MCP, publishing, stable governance, long-term memory, permission, or security boundary decisions.

Red / Green / Regression is mandatory for behavior changes, bug fixes, contract changes, and test changes. Red proves the new or changed test fails before the fix and captures the target issue. Green proves the implementation or fix makes the relevant test pass. Regression proves related checks still pass. Pure documentation, comments, or no-behavior config changes may use `not_applicable_reason`.

```text
architecture_feedback_register:
  source_thread:
  source_gate:
  issue_type: bug_pattern | architecture_issue | contract_risk | boundary_violation | test_gap
  root_cause:
  impact:
  prevention_rule:
  reusable_check:
  upstream_architecture_action:
  status: open | accepted | rejected | resolved
  next_a1_input: yes | no
  next_a2_input: yes | no
  next_a3_input: yes | no
```

## Rollback

| Scenario | Rollback | Recheck |
|---|---|---|
|  |  |  |

## Execution Conclusion

| Item | Status |
|---|---|
| Ready to implement | yes / no |
| Module A3 preflight | pass / prepare_required / blocked |
| P0 blockers |  |
| Minimum acceptable fix |  |
| Remaining upstream approvals |  |
| Architecture feedback feeds next A1/A2/A3 | yes / no |
