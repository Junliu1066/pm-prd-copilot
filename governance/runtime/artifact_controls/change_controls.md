# Change Control Rules

## Purpose

Keep requirement, API, schema, and stage changes deliberate after a project has a PRD or final development document.

## Change Classification

| Change Type | Examples | Required Handling |
|---|---|---|
| Scope change | New feature, phase move, non-goal reversal | Chief steward and PRD steward review |
| API change | Field rename, endpoint change, request/response shape | Technical gate and test impact check |
| Schema change | New table, migration, constraint change | Migration and rollback note |
| Security change | Token, key, permission, logging behavior | Safety gate |
| Test change | Harness, acceptance, dry-run behavior | Test gate |
| Documentation-only | Clarification, typo, examples | Source-of-truth check |

## Change Record Template

For substantial changes, capture:

| Field | Meaning |
|---|---|
| Change | What changed |
| Source | User, review, implementation finding, test failure |
| Affected artifacts | PRD, phase docs, final dev doc, tests, deployment |
| Decision | Accepted, deferred, rejected |
| Phase | Current phase, later phase, future |
| Follow-up | Required edits or tests |

## Rules

- Do not silently move a requirement between phases.
- Do not add an API field without checking data model, Agent behavior, UI, and tests.
- Do not add a schema field without a migration and compatibility note.
- Do not update staged docs while leaving the final development document stale.
- If the user corrects the project premise, update premise statements before lower-level details.
