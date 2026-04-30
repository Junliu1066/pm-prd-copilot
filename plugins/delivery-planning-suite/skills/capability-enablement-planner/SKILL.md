---
name: capability-enablement-planner
description: Plan the capability-enablement layer before semi-automated development by deciding which existing skills to reuse, which new skills may be needed, which MCPs may be connected, which harness checks must guard them, and which decisions require human approval. Use when a Codex-style development plan may need framework, skill, MCP, registry, or governance expansion before product code is written.
---

# Capability Enablement Planner

## Purpose

Decide what enabling capabilities are needed before coding starts. This skill answers "do we already have the right skills and tools, or must we extend the operating system first?"

## Inputs

- PRD or delivery plan
- technical scope
- AI solution plan when available
- existing registry, steward, MCP, harness, preference-cache, and teaching constraints

## Workflow

1. Identify capability gaps that block safe semi-automated development.
2. For each gap, decide reuse existing skill, update existing skill, create new skill, connect MCP, or handle manually.
3. Define MCP candidates only when external evidence or integration is actually needed.
4. Define required harness checks, registry additions, steward ownership, and human approvals.
5. Separate project-specific preferences from generic skill improvements.
6. Route supervised skill updates through teaching and proposal flow; never update skills silently.

## Output Contract

Read [references/output-contract.md](references/output-contract.md). Always include `capability_gaps`, `skill_reuse_decision`, `new_skill_candidates`, `mcp_candidates`, `harness_requirements`, `memory_learning_route`, and `human_approval_required`.

## Guardrails

- Do not create a new skill when an existing skill can safely handle the task.
- Do not connect MCPs unless the task needs external data or external actions.
- MCP outputs are signals only and cannot directly decide PRD, MVP, model choice, or skill updates.
- Skill creation and skill updates require human approval and generalization review.
