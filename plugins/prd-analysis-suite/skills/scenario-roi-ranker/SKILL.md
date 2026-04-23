---
name: scenario-roi-ranker
description: Rank product usage scenarios by user value, cost, frequency, speed-to-value, risk, and strategic fit. Use when a PRD or product idea has multiple possible scenarios and needs minimum-cost maximum-return prioritization before core scenario approval or MVP scoping.
---

# Scenario ROI Ranker

## Overview

Turn user needs and competitor gaps into a ranked scenario list. The main principle is minimum build cost for maximum user value, without hiding uncertainty.

## Workflow

1. Confirm user-universe and pain-needs inputs include multiple plausible user groups before ranking scenarios.
2. Convert each pain/need into a concrete usage scenario with trigger, user action, expected outcome, and success signal.
3. Link competitor gaps or advantage hypotheses to each scenario when that evidence exists.
4. Score each scenario across user value, frequency, urgency, time saved, build cost, validation speed, risk, and differentiation.
5. Explain the score, especially where data is weak.
6. Identify the best core scenario, backup scenario, and scenarios to avoid for now.
7. Produce a clear approval question for the user: which core scenario should move into MVP scoping?

## Accepted Teaching Rules

- `LESSON-20260423-001`: Scenario ranking must not inherit premature user narrowing; include a coverage note when candidate user groups are missing.
- `LESSON-20260423-002`: Core scenarios should be selected by minimum implementation cost, maximum user/business return, time saved, and speed to MVP.
- `LESSON-20260423-003`: Competitor gaps should feed the differentiation score; do not rank scenarios without explaining how competitor weakness can become our advantage.

## Scoring Model

Use a 1-5 score for each dimension:

- `user_value`: pain relief and outcome importance.
- `frequency`: how often the scenario occurs.
- `time_savings`: avoidable time or repeated effort.
- `build_cost`: lower cost should score higher.
- `validation_speed`: how quickly the scenario can be tested.
- `risk`: lower product, privacy, technical, or operational risk should score higher.
- `differentiation`: advantage versus existing alternatives.

Default weight:

- User value: 25%
- Build cost: 20%
- Frequency: 15%
- Time savings: 15%
- Validation speed: 10%
- Risk: 10%
- Differentiation: 5%

Adjust weights only when the user or project strategy requires it.

## Output Contract

Read [references/output-contract.md](references/output-contract.md) for the formal artifact shape. Always include:

- `scenario_scores`
- `recommended_core_scenario`
- `backup_scenario`
- `avoid_for_now`
- `cost_return_summary`
- `competitor_gap_links`
- `approval_question`

## Guardrails

- Do not choose a scenario solely because it is strategically attractive if it is expensive and slow to validate.
- Do not hide tradeoffs; show where a lower-ranked scenario may still matter later.
- Do not write final MVP scope; hand the ranking to `mvp-scope-decider`.
