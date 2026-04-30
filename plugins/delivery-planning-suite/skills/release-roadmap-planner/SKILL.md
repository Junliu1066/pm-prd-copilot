---
name: release-roadmap-planner
description: Split confirmed product scope and technical scope into MVP, V1, V1.5, and Future release phases with clear boundaries, dependencies, non-goals, and validation goals. Use when a PRD needs a phased development path before effort estimation or delivery planning.
---

# Release Roadmap Planner

## Purpose

Decide what should ship first, what should wait, and why. This skill creates a phased delivery roadmap; it does not estimate exact duration and does not add product scope.

## Inputs

- `mvp_scope`
- `technical_scope`
- `prd_document` or `prd_markdown`
- `scenario_ranking`
- `risk_report` when available

## Workflow

1. Start from user value, MVP learning goal, implementation dependency, and risk.
2. Define each release phase:
   - MVP / Phase 1.
   - V1 / Phase 2.
   - V1.5 or Growth / Phase 3.
   - Future / long-term target.
3. For each phase, state included modules, deferred modules, validation goal, and release exit criteria.
4. Keep Future goals separate from MVP.
5. Send the roadmap to `effort-estimator` and `delivery-effect-definer`.

## Output Contract

Read [references/output-contract.md](references/output-contract.md) for the formal artifact shape. Always include:

- `release_phases`
- `phase_boundaries`
- `dependencies`
- `deferred_scope`
- `validation_goals`
- `future_target`

## Guardrails

- Do not turn Future scope into MVP.
- Do not omit why a feature is deferred.
- Do not change product priority without a backflow question.
- Do not estimate duration; hand that to `effort-estimator`.
