---
name: user-universe-mapper
description: Map the full universe of plausible target users before narrowing product scope. Use when a PRD, product idea, market opportunity, or feature concept needs comprehensive user segmentation, pain discovery, adoption reasoning, or target-user prioritization without prematurely focusing on one group.
---

# User Universe Mapper

## Overview

Enumerate every plausible user group that could become the product target, then make the narrowing logic explicit. This skill exists to prevent early overfitting to one obvious segment.

## Workflow

1. Start from the product job, not from a demographic label.
2. List all plausible user groups, including primary users, adjacent users, power users, occasional users, buyers, influencers, and blockers.
3. For each group, capture motivation, frequency, urgency, willingness to pay or switch, current workaround, and why they might reject the product.
4. Mark evidence strength as `explicit`, `inferred`, or `needs_research`.
5. Group users into practical PRD segments only after the universe is visible.
6. Recommend priority candidates, but do not decide MVP scope.

## Required Dimensions

- User group name.
- Trigger situation.
- Core job-to-be-done.
- Pain intensity.
- Frequency.
- Current solution or workaround.
- Decision power.
- Acquisition path.
- Product fit risk.
- Evidence level.

## Output Contract

Read [references/output-contract.md](references/output-contract.md) for the formal artifact shape. Always include:

- `user_universe_table`
- `segment_clusters`
- `priority_candidates`
- `discarded_or_low_priority_segments`
- `research_questions`

## Guardrails

- Do not stop at the user's first stated target segment.
- Do not rank by intuition alone; make assumptions visible.
- Do not write PRD features yet.
