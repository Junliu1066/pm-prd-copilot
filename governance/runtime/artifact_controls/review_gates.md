# Review Gate Controls

## Purpose

Make review a staged control mechanism, not a single final pass.

## Gate Types

| Gate | Owner | Checks |
|---|---|---|
| Scope gate | Chief steward + PRD steward | Phase scope, non-goals, acceptance criteria |
| Technical gate | Technical route steward | API, data model, state machine, module boundaries |
| Safety gate | Review steward | Token, private key, RBAC, logging, command execution |
| Test gate | Test steward | Unit tests, harness, dry-run, smoke checks |
| Efficiency gate | Efficiency steward | Duplicated content, over-fragmented skills, unused outputs |
| Learning gate | Teacher | User corrections and reusable lessons captured as proposals |

## Phase Gate Pattern

For each project phase:

1. Before development, run scope and technical gates.
2. Before test handoff, run safety and test gates.
3. Before final handoff, run review and efficiency gates.
4. After user correction, run learning gate if the correction is reusable.

## Required Final Review

Before packaging or delivering a final development artifact, verify:

- PRD, phase docs, and final development doc have matching scope.
- API names, fields, and examples match across all relevant docs.
- Database fields support the documented API and UI.
- Security rules are explicit and testable.
- Tests cover the risky paths, not only happy paths.
- Deployment and rollback notes exist when the artifact describes production or Windows/Linux handoff.

## Reporting Rule

When a review gate finds an issue, report it as:

- Finding
- Evidence path
- Impact
- Required action
- Whether it blocks the artifact
