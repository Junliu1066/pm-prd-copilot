---
name: delivery-effect-definer
description: Define the user-visible and business-visible effect of each delivery phase, integrate technical scope, roadmap, and effort estimates into a delivery plan, and clarify what each release validates. Use when a PRD needs "what ships, how long, what users can do, and what the business learns" in one development path.
---

# Delivery Effect Definer

## Purpose

Create the final delivery plan from upstream delivery artifacts. This skill keeps release planning tied to user value, validation goals, and technical reality.

## Inputs

- `technical_scope`
- `release_roadmap`
- `effort_estimate`
- `prd_document` or `prd_markdown`
- `tracking_plan` when available

## Workflow

1. For each phase, summarize:
   - development goal.
   - included technical modules.
   - estimated duration range.
   - user-visible outcome.
   - business or product validation outcome.
   - remaining risk and deferred scope.
2. State the long-term product target separately from MVP and V1.
3. Keep unresolved assumptions explicit.
4. Hand the final delivery plan to `delivery-quality-reviewer`.

## Output Contract

Read [references/output-contract.md](references/output-contract.md) for the formal artifact shape. Always include:

- `phase_delivery_plan`
- `user_visible_effects`
- `business_validation`
- `technical_validation`
- `remaining_risks`
- `final_target`
- `open_decisions`

## Guardrails

- Do not add new product scope to make a phase look better.
- Do not hide unresolved product decisions.
- Do not merge Future goals into MVP.
- Do not omit user-visible effects.
