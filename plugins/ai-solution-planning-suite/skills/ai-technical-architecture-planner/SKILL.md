---
name: ai-technical-architecture-planner
description: Define the AI subsystem technical architecture for product development, including AI service boundaries, model gateway, prompt registry, RAG pipeline, memory/profile storage, task orchestration, logs, observability, fallbacks, and API contracts with the business backend.
---

# AI Technical Architecture Planner

## Purpose

Define how the AI subsystem should be built. This skill owns AI architecture only; it does not choose the entire product tech stack or mutate product scope.

## Workflow

1. Read AI capability map, model plan, prompt architecture, RAG plan, memory plan, learner profile, and coaching plan.
2. Define AI service boundaries and interface contracts with product backend.
3. Define model gateway, prompt registry, RAG pipeline, memory/profile storage, orchestration, observability, fallback, and evaluation hooks.
4. Identify development dependencies for delivery planning.
5. Hand output to `technical-scope-planner` and `effort-estimator`.

## Output Contract

Read [references/output-contract.md](references/output-contract.md). Always include `ai_service_boundary`, `api_contracts`, `model_gateway`, `prompt_registry`, `rag_pipeline`, `memory_profile_storage`, `orchestration`, `observability`, `fallbacks`, and `delivery_dependencies`.

## Guardrails

- Do not decide frontend framework or non-AI backend stack.
- Do not store sensitive user content without explicit retention rules.
- Do not bypass AI safety, logging, or evaluation hooks.
