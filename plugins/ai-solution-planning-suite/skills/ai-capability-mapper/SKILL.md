---
name: ai-capability-mapper
description: Map product requirements into explicit AI capabilities, task boundaries, AI/non-AI split, inputs, outputs, risks, and evaluation needs. Use when a PRD contains model-assisted generation, scoring, classification, coaching, retrieval, memory, or personalization.
---

# AI Capability Mapper

## Purpose

Translate product requirements into AI capability units. This skill answers "what AI must do" and "what should stay deterministic or human-supervised".

## Workflow

1. Read PRD scope, MVP, product flow, prototype, and risk notes.
2. Split AI work into capability units such as generation, scoring, classification, retrieval, personalization, safety screening, summarization, routing, or coaching.
3. For each capability, define trigger, input, output, quality criteria, human supervision, fallback, and risk.
4. Mark non-AI work that should remain deterministic.
5. Hand outputs to model, prompt, RAG, memory, coaching, and AI architecture planners.

## Output Contract

Read [references/output-contract.md](references/output-contract.md). Always include `ai_capabilities`, `non_ai_boundaries`, `quality_needs`, `safety_risks`, and `downstream_planning`.

## Guardrails

- Do not select specific models.
- Do not design prompts or RAG internals.
- Do not change product scope; route ambiguity back as PM questions.
