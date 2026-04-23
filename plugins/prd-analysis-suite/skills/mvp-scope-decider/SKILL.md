---
name: mvp-scope-decider
description: Convert approved scenario ranking, user needs, competitor gaps, and constraints into MVP, V1, Later, and non-goal scope. Use when a PRD needs a focused first-release boundary, minimum viable feature set, explicit tradeoffs, or human approval before PRD structure planning and drafting.
---

# MVP Scope Decider

## Overview

Define the smallest coherent product version that proves the core scenario. The MVP should save user time, reduce waste, and create a usable loop without absorbing every adjacent feature.

## Workflow

1. Start from the approved or proposed core scenario.
2. Define the minimum closed loop: trigger, input, processing, output, feedback, and repeat use.
3. Check that the core scenario was selected with value, cost, time saved, speed to MVP, and competitor-gap reasoning.
4. Split features into `MVP`, `V1`, `Later`, and `Non-goals`.
5. For every MVP item, state the user value, evidence, build cost, dependency, and validation signal.
6. Remove or defer anything that does not support the core loop or early validation.
7. Produce an approval question for the user before PRD planning.

## Accepted Teaching Rules

- `LESSON-20260423-002`: MVP scope should preserve the lowest-cost highest-return path and explain why expensive adjacent features are deferred.
- `LESSON-20260423-003`: Competitor gaps can justify MVP choices only when they link to a user need and a practical advantage.

## Scope Rules

- MVP must be testable by a real target user.
- MVP must contain a full user loop, not only isolated capabilities.
- MVP should prefer lower-cost implementation if user value is comparable.
- V1 contains valuable but non-blocking improvements.
- Later contains expensive, risky, or uncertain bets.
- Non-goals prevent hidden scope creep.

## Output Contract

Read [references/output-contract.md](references/output-contract.md) for the formal artifact shape. Always include:

- `core_scenario`
- `mvp_loop`
- `scope_table`
- `deferred_items`
- `non_goals`
- `roi_basis`
- `competitor_gap_basis`
- `approval_question`

## Guardrails

- Do not expand scope to satisfy every segment.
- Do not hide tradeoffs. If a useful feature is deferred, explain why.
- Do not draft the full PRD; this skill produces scope input for PRD planning.
