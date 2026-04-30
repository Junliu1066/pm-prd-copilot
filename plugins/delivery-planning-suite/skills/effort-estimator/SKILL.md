---
name: effort-estimator
description: Estimate implementation effort for PRD technical scope and release phases using explicit team assumptions, module breakdowns, uncertainty, dependency risks, buffer, testing, and integration time. Use when a PRD needs development duration estimates.
---

# Effort Estimator

## Purpose

Estimate delivery effort with stated assumptions. This skill explains "how long it might take and why" without pretending estimates are exact.

## Inputs

- `technical_scope`
- `release_roadmap`
- `prd_document` or `prd_markdown`
- `risk_report` when available

## Workflow

1. State team configuration assumptions first.
2. Estimate by module and role:
   - frontend/client.
   - backend/API.
   - AI/model/prompt work.
   - data/storage.
   - QA and testing.
   - design/PM review and integration.
3. Include dependency assumptions and uncertainty level.
4. Add buffer for unknowns, integration, and regression.
5. Produce phase-level duration ranges, not single-point certainty.

## Default Assumptions

Use only when the user gives no team configuration:

- 1 frontend/client engineer.
- 1 backend engineer.
- 1 AI/model or full-stack engineer when AI work exists.
- 1 QA tester part-time.
- 1 PM/designer reviewer part-time.

## Output Contract

Read [references/output-contract.md](references/output-contract.md) for the formal artifact shape. Always include:

- `team_assumptions`
- `module_estimates`
- `phase_estimates`
- `buffer_policy`
- `uncertainty`
- `estimate_risks`

## Guardrails

- Do not output effort without team assumptions.
- Do not use a single exact duration when uncertainty exists.
- Do not exclude QA, integration, or acceptance review from estimates.
- Do not present estimates as commitments.
