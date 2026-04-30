---
name: model-selection-planner
description: Plan model selection for AI product capabilities using current official documentation, benchmark tasks, cost, latency, privacy, reliability, and fallback criteria. Use when an AI-heavy PRD needs model routing or model choice, without hard-coding stale model defaults.
---

# Model Selection Planner

## Purpose

Create a model-selection plan that compares real market models and recommends a short list for the product. The skill must distinguish official-document screening from actual API benchmark results.

## Workflow

1. Read `ai_capability_map` and AI quality needs.
2. Define market scope. If no market is specified, use the project's market default and include both locally accessible providers and global providers when relevant.
3. Collect a candidate pool from current official model documentation and pricing pages. Include provider, model id, context, input/output price, multimodal/tool/JSON support, deployment or data-residency notes, and source URL/date.
4. Compare candidates by product tasks: high-reasoning, low-latency, low-cost, embedding, reranking, speech, vision, moderation, or fallback.
5. Design benchmark cases and, when API keys are available, run or request real benchmark tests. If not run, mark the score as `not_measured` and do not imply real-world performance.
6. Produce recommended model combinations: primary, low-cost/fallback, quality-first alternative, and future-phase options.
7. Produce routing rules for MVP and future phases.

## Output Contract

Read [references/output-contract.md](references/output-contract.md). Always include `market_scope`, `official_source_snapshot`, `candidate_model_pool`, `model_comparison_matrix`, `benchmark_plan`, `benchmark_status`, `shortlist_recommendations`, `routing_rules`, and `fallback_strategy`.

## Guardrails

- Do not rely on memory for current model availability or pricing.
- Do not present model choice as final without official docs and benchmark evidence.
- Do not optimize only for cost if quality or safety is critical.
- Do not output only generic model categories when the user needs model selection. Name concrete market models and explain why they are recommended.
- If real API benchmark has not been executed, label recommendations as "document-screening shortlist" and require human verification.
