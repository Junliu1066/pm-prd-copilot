---
name: rag-architecture-planner
description: Plan retrieval-augmented generation architecture for AI products, including knowledge sources, chunking, metadata, retrieval strategy, citations, freshness, permissions, and hallucination controls. Use when AI answers must ground in documents, knowledge bases, policies, or user-provided materials.
---

# RAG Architecture Planner

## Purpose

Design retrieval grounding so AI outputs cite appropriate sources and avoid unsupported claims.

## Workflow

1. Identify knowledge sources: product docs, user documents, internal policies, question banks, training history, public references, or structured data.
2. Define ingestion, chunking, metadata, indexing, retrieval, reranking, citation, and freshness rules.
3. Define permission boundaries and deletion requirements.
4. Define fallback when retrieval is weak or absent.
5. Define evaluation cases for citation quality and hallucination prevention.

## Output Contract

Read [references/output-contract.md](references/output-contract.md). Always include `knowledge_sources`, `ingestion_pipeline`, `retrieval_strategy`, `citation_policy`, `permission_rules`, `fallback_rules`, and `rag_eval`.

## Guardrails

- Do not treat retrieved content as verified truth when it is user-provided or external.
- Do not retrieve across users without explicit authorization.
- Do not answer as if grounded when retrieval confidence is low.
