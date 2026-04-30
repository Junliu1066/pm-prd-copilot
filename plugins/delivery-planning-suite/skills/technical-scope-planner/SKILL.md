---
name: technical-scope-planner
description: Translate confirmed PRD scope, MVP decisions, product flows, and prototype previews into implementation-facing technical scope without changing product requirements. Use when a PRD needs frontend, backend, model, data, permission, analytics, testing, and integration modules before release planning.
---

# Technical Scope Planner

## Purpose

Convert product requirements into technical work packages. This skill answers "what needs to be built" but does not estimate time, decide release phases, or change MVP scope.

## Inputs

- `mvp_scope`
- `prd_document` or `prd_markdown`
- `product_flow_map`
- `prototype_preview`
- `risk_report` when available

## Workflow

1. Read only confirmed or clearly marked draft PRD scope.
2. Split product requirements into implementation modules:
   - frontend or client surfaces.
   - backend services and APIs.
   - data models and storage.
   - model/AI calls and prompt assets.
   - permission, privacy, and security controls.
   - analytics and tracking.
   - QA, test data, and operational tooling.
3. Mark dependencies, assumptions, unknowns, and scope risks.
4. Identify product-scope questions that must flow back to PM instead of silently changing requirements.
5. Hand the technical scope to `release-roadmap-planner` and `effort-estimator`.

## Output Contract

Read [references/output-contract.md](references/output-contract.md) for the formal artifact shape. Always include:

- `technical_modules`
- `data_and_api_scope`
- `ai_or_model_scope`
- `privacy_security_scope`
- `analytics_scope`
- `testing_scope`
- `dependencies`
- `pm_backflow_questions`

## Guardrails

- Do not modify `mvp_scope`, `prd_document`, `product_flow_map`, or prototypes.
- Do not estimate effort; hand that to `effort-estimator`.
- Do not add engineering features that lack product value or risk justification.
- Do not hide product ambiguity inside technical assumptions.
