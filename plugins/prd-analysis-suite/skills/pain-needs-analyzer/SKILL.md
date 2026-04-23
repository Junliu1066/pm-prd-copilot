---
name: pain-needs-analyzer
description: Analyze pains, needs, root causes, desired outcomes, and time-cost savings for each target user group. Use after user-universe mapping or when a PRD needs stronger demand reasoning, problem framing, JTBD analysis, or scenario inputs before ROI ranking and MVP scoping.
---

# Pain Needs Analyzer

## Overview

Convert target-user groups into concrete product demand. The output should explain what users actually want, why current workflows waste time or money, and which needs deserve product investment.

## Workflow

1. For each user group, identify pains, desired outcomes, current workaround, and hidden switching cost.
2. Separate symptom from root cause.
3. Describe the user's demand in practical language: what they want to finish faster, avoid, measure, decide, remember, or automate.
4. Estimate impact using frequency, severity, time saved, money saved, risk avoided, and emotional friction.
5. Mark evidence level and research gaps.
6. Hand scenario candidates to the scenario ROI skill. Do not decide MVP scope.

## Analysis Lens

- Functional need: task completion, measurement, planning, reminder, decision support.
- Efficiency need: reduce repeated input, search, calculation, waiting, switching apps, or manual tracking.
- Confidence need: reduce uncertainty, error, guilt, or fear of doing the wrong thing.
- Habit need: make repeated behavior easier to start and sustain.
- Social need: accountability, coaching, comparison, or proof.

## Output Contract

Read [references/output-contract.md](references/output-contract.md) for the formal artifact shape. Always include:

- `pain_needs_matrix`
- `root_cause_analysis`
- `time_cost_savings`
- `scenario_candidates`
- `research_gaps`

## Guardrails

- Do not confuse a feature request with a need.
- Do not assume high-frequency always means high value; severity and willingness to change matter.
- Keep unsupported claims visible as assumptions.
