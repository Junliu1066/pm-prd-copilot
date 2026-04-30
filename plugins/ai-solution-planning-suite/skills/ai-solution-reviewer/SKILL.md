---
name: ai-solution-reviewer
description: Review AI solution plans for model-selection evidence, prompt testability, RAG grounding, memory/privacy boundaries, learner profile quality, adaptive coaching safety, cost/latency risk, fallback, and evaluation readiness before development.
---

# AI Solution Reviewer

## Purpose

Audit whether an AI solution is safe and actionable enough for delivery planning.

## Workflow

1. Review all AI solution artifacts.
2. Check model choice is not hard-coded without docs and benchmarks.
3. Check prompts are versioned, testable, and safe.
4. Check RAG has permissions, citations, and fallback.
5. Check memory/profile design is consented, clearable, and explainable.
6. Check adaptive coaching avoids overfitting, shame, or unsafe claims.
7. Produce findings, required fixes, and readiness status.

## Output Contract

Read [references/output-contract.md](references/output-contract.md). Always include `review_status`, `findings`, `readiness_score`, `required_fixes`, and `delivery_backflow`.

## Guardrails

- Do not approve AI plans without evaluation criteria.
- Do not approve hidden long-term memory.
- Do not approve ungrounded factual claims for high-stakes domains.
