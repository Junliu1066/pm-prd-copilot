---
name: learner-profile-modeler
description: Design a user capability profile model for adaptive AI coaching, including skill dimensions, evidence, confidence, update rules, decay, privacy boundaries, and reporting. Use when AI must remember what the user is strong or weak at.
---

# Learner Profile Modeler

## Purpose

Define the learner capability model that records strengths, weaknesses, evidence, and confidence so coaching can be targeted.

## Workflow

1. Read product scoring dimensions, evaluation rules, memory plan, and coaching goals.
2. Define capability dimensions and subskills.
3. Define evidence inputs and update rules.
4. Define confidence, recency decay, and minimum evidence requirements.
5. Define what users can view, correct, or clear.

## Output Contract

Read [references/output-contract.md](references/output-contract.md). Always include `profile_dimensions`, `evidence_model`, `update_rules`, `confidence_policy`, `privacy_controls`, and `reporting`.

## Guardrails

- Do not label users permanently from one weak answer.
- Do not store sensitive content beyond what is required.
- Do not hide the basis of a capability judgment.
