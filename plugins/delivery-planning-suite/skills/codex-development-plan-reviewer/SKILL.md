---
name: codex-development-plan-reviewer
description: Review Codex semi-automated development plans before they are sent to a user or used for implementation. Use when a development document, phase plan, Codex task package, MCP/Skill integration plan, or AI implementation plan needs an execution-readiness audit for feasibility, blockers, optimality, dependencies, human confirmation gates, validation coverage, rollback, and scope safety.
---

# Codex Development Plan Reviewer

## Purpose

Audit development-facing documents before delivery. This skill checks whether a Codex development plan is executable, appropriately phased, safe, and close to the best available implementation path under the current product scope and known constraints.

This skill does not create the development plan. It reviews plans created by planning skills and produces a send-before-review artifact.

## Inputs

- PRD/product package
- Feature matrix, flow, and prototype artifacts when available
- Codex development plan
- Phase Codex plans
- Codex task packages
- AI, Prompt, RAG, Memory plans when available
- Skill/MCP routing and governance plans when available
- Known repository, framework, model, database, deployment, and permission constraints

## Review Workflow

1. Confirm product/development boundary.
   - Product decisions may live in the PRD/product package.
   - Codex implementation details must live in development documents.
2. Check phase logic.
   - Phase 1 must produce a usable MVP/core loop.
   - Later phases must not block the MVP.
   - Dependencies must flow forward, not backward.
3. Check execution blockers.
   - Missing tech stack, repo path, database, model provider, MCP approval, GitHub permission, environment variables, test data, or legal/privacy confirmation.
4. Check task-package executability.
   - Every task must have a single goal, inputs, allowed write paths, forbidden write paths, expected outputs, validation, rollback, and human confirmation points.
5. Check optimality.
   - Prefer the smallest viable implementation that validates the product loop.
   - Flag overbuilt architecture, premature MCP integration, excessive model reliance, missing rule-based fallback, or cross-phase coupling.
6. Check safety and governance.
   - Confirm approval gates for schema changes, model/provider changes, MCPs, memory writes, GitHub push/PR, destructive data, and Skill updates.
7. Check validation depth.
   - Require unit/integration/manual checks, harness checks, prompt regression for AI behavior, privacy/deletion tests, and rollback criteria.
8. Produce the review artifact using [references/output-contract.md](references/output-contract.md).

## Decision Levels

- `pass`: ready to send and can enter implementation after listed human confirmations.
- `warn`: can be sent for review, but implementation must not start until P0 blockers are resolved.
- `fail`: should not be sent as an execution plan until blocking structural issues are fixed.

## Guardrails

- Do not approve model, database, MCP, GitHub, memory, or Skill changes on behalf of the user.
- Do not rewrite the PRD scope while reviewing a development document.
- Do not treat a plan as executable if it lacks write boundaries or validation.
- Do not hide blockers in prose; every blocker must have severity, owner, and required decision.
- Do not recommend external integrations when a local or rule-based MVP path is sufficient.
