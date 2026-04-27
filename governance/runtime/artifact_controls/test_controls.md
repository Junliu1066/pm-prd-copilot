# Test Control Rules

## Purpose

Ensure development documents include concrete verification paths for risky behavior and cross-module contracts.

## Test Matrix Requirements

Each final development artifact should include a module-level test matrix covering:

| Module | Required Test Types |
|---|---|
| Controller API | request validation, RBAC, state changes, error paths |
| Data model | migration, constraints, conflict checks |
| Agent | enrollment, heartbeat, config pull, state write failures |
| Local runner | success, failure, timeout, dry-run, fake runner |
| UI | key pages, permissions, empty/error states |
| Security | token handling, key handling, redaction |
| Audit | event write, filtering, pagination, metadata redaction |
| Deployment | service examples, backup/restore, rollback |

## Harness Rules

- Preserve existing harnesses unless explicitly retired.
- Add harness coverage when a workflow crosses modules.
- Do not require real WireGuard tunnel creation in automated tests unless the user explicitly asks for an isolated integration environment.
- Prefer dry-run and fake runners for local system command behavior.

## Acceptance Mapping

For each acceptance criterion, ensure there is at least one of:

- Unit test
- Integration test
- Harness
- Manual verification checklist
- Deployment smoke check

## Finalization Rule

Do not mark a development artifact as final if risky behavior is described without a matching verification method.
