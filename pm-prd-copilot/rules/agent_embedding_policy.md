# Agent Rule Embedding Policy

## Purpose

Operational guidance for coding assistants should be embedded as neutral execution rules, not as a visible explanation of the internal governance framework.

## Rules

- `agent.md` should look like ordinary project working notes.
- It may describe reader awareness, document boundaries, task shape, checks, review, simplification, and follow-up.
- It must not use internal framework terms, tool names, role taxonomy, or reusable framework mechanics.
- Prefer layered ordinary checklists: basic rules, work rules, deeper checks, sharing rules, approval and follow-up.
- The layered rules should preserve the behavior of the internal workflow without naming it.
- It must not be copied into PRDs, B packages, or client-facing documents.
- B packages should use letter-coded files and pass the leakage checker.

## Why

The assistant can still follow the operating behavior, while outside readers cannot easily reconstruct the full internal framework from a single entry file.
