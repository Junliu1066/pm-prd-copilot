---
name: delivery-quality-reviewer
description: Review delivery plans for PRD implementation readiness, including phase boundaries, team assumptions, effort estimate quality, MVP/Future separation, user-visible effects, testing coverage, risk buffer, and product-scope backflow. Use before a PRD is treated as ready for development.
---

# Delivery Quality Reviewer

## Purpose

Audit whether a delivery plan is actionable and safe to hand to development. This skill is the department-level reviewer; it does not rewrite product scope.

## Inputs

- `technical_scope`
- `release_roadmap`
- `effort_estimate`
- `delivery_plan`
- `prd_document` or `prd_markdown`

## Workflow

1. Check phase boundaries:
   - MVP is not overloaded.
   - Future scope is not mixed into early phases.
   - deferred items have reasons.
2. Check estimates:
   - team assumptions exist.
   - estimates are ranges or have uncertainty.
   - QA, integration, and acceptance are included.
   - buffer is explained.
3. Check delivery effects:
   - each phase says what users can do after release.
   - each phase says what product/business assumption is validated.
4. Check governance:
   - delivery plan does not mutate product scope.
   - product ambiguities are routed as PM backflow questions.
5. Produce issues, severity, and minimum fixes.

## Output Contract

Read [references/output-contract.md](references/output-contract.md) for the formal artifact shape. Always include:

- `review_status`
- `findings`
- `readiness_score`
- `required_fixes`
- `pm_backflow_questions`

## Guardrails

- Do not approve a plan with missing team assumptions.
- Do not approve a plan that omits QA/integration.
- Do not approve a plan that presents estimates as commitments.
- Do not modify PRD or MVP scope directly.
