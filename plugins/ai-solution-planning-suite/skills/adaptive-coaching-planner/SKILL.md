---
name: adaptive-coaching-planner
description: Plan adaptive AI coaching strategies that use learner profiles to target weak skills, choose next exercises, control difficulty, manage pressure, and measure improvement. Use when an AI product must teach users based on strengths and weaknesses.
---

# Adaptive Coaching Planner

## Purpose

Turn learner profiles into targeted coaching paths. This skill defines "precision teaching" without overtraining or discouraging users.

## Workflow

1. Read learner profile model, product goals, scoring dimensions, and prompt/RAG capabilities.
2. Define weak-skill targeting rules.
3. Define exercise selection, difficulty progression, retry cadence, pressure control, and stop conditions.
4. Define feedback style and escalation to human review when needed.
5. Define improvement metrics and guardrails.

## Output Contract

Read [references/output-contract.md](references/output-contract.md). Always include `coaching_rules`, `exercise_selection`, `difficulty_policy`, `feedback_policy`, `improvement_metrics`, and `guardrails`.

## Guardrails

- Do not overfit coaching from one session.
- Do not shame users for weak performance.
- Do not optimize engagement by creating artificial failure.
