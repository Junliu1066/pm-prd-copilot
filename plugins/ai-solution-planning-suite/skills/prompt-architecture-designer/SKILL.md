---
name: prompt-architecture-designer
description: Design versioned prompt architecture for AI product capabilities, including system prompts, task prompts, scoring rubrics, safety instructions, input/output schemas, prompt tests, and rollback. Use when AI behavior needs controlled and testable prompts.
---

# Prompt Architecture Designer

## Purpose

Turn AI capabilities into a controlled prompt system. Prompts must be versioned, testable, and safe to iterate under human supervision.

## Workflow

1. Read AI capabilities, model selection plan, product flows, and safety constraints.
2. Define prompt assets by task: generation, follow-up, scoring, rewriting, routing, retrieval answer, safety refusal, or coaching.
3. Define input schema, output schema, rubric, tone, forbidden behavior, and fallback for each prompt.
4. Define prompt tests and regression examples.
5. Mark prompt changes as versioned artifacts requiring review.

## Output Contract

Read [references/output-contract.md](references/output-contract.md). Always include `prompt_assets`, `schemas`, `rubrics`, `safety_rules`, `test_cases`, and `versioning_policy`.

## Guardrails

- Do not embed private user data in reusable prompt templates.
- Do not let prompts invent facts when source data is missing.
- Do not update prompts silently without versioning and tests.
