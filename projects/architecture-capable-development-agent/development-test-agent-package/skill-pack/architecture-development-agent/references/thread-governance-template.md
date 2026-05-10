# Threaded Development Testing Template

## Activation

Use threaded development only after Module A1 engineering feasibility review returns `pass` and Module A2 confirms independent write scopes, frozen contracts, integration gates, and failure return paths. Before any module business implementation, Module A3 must pass for the responsible module or thread. Keep single-thread work single-thread.

## Thread Matrix

| Thread | Development goal | Allowed writes | Forbidden writes | Dependencies | Contract | A3 preflight | Risk | Status | Module B gate |
|---|---|---|---|---|---|---|---|---|---|
| T-A |  |  |  |  | frozen / none | pending / pass / prepare_required / blocked | low / medium / high | planned | pending |

## Contract Freeze

| Contract | Status | Owner | Change policy |
|---|---|---|---|
| API | missing / draft / frozen / none | upstream | report blocker if not frozen |
| DB schema | missing / draft / frozen / none | upstream | stop unless approved |
| AI output | missing / draft / frozen / none | upstream | report blocker if unclear |
| permissions | missing / draft / frozen / none | upstream | report blocker if unclear |
| page state | missing / draft / frozen / none | upstream | report blocker if unclear |

## Startup Package

```text
Thread:
Branch:
Development goal:
Context:
Inputs:
Allowed writes:
Forbidden writes:
Locked writes:
Dependencies:
Contract:
A3 module development preflight:
Steps:
Validation:
Acceptance:
Rollback:
Module B quality gate:
Red / Green / Regression evidence:
Module B architecture feedback:
Evidence:
Approval points:
```

## State Machine

```text
planned -> ready -> running -> self_checked -> quality_reviewed
-> quality_gate_passed -> integration_pending
-> integration_passed / integration_failed
-> fix_required / blocked / closed
```

## Integration

- Do not merge directly to main unless explicitly authorized.
- Do not enter module business implementation unless A3 status is `pass`; when A3 is `prepare_required`, only complete safe preparation work, and when A3 is `blocked`, output `approval_request`.
- Integrate only threads that are `quality_gate_passed`.
- Require Red / Green / Regression evidence before `quality_gate_passed` for behavior changes, bug fixes, contract changes, and test changes; use not-applicable reason only for pure docs, comments, or no-behavior config changes.
- Locate failures through Module B and assign them to the responsible thread.
- Run Module B automatically after each module/thread self-check.
- Record Module B bug patterns, architecture issues, prevention rules, reusable checks, and upstream architecture actions as project-level architecture feedback.
- Send fixes back to the responsible thread or a scoped fix thread.
- Close every thread with checks, files, rollback, risk, architecture feedback, and upstream blocker status.

## Architecture Feedback

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

Feed ordinary bug patterns into tests and reusable checks. Feed architecture issues into contract, thread boundary, validation planning, and A3 preflight checks. Escalate high-risk boundaries with `approval_request` instead of changing contracts directly.
