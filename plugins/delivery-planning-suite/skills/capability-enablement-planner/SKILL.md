---
name: capability-enablement-planner
description: Plan the capability-enablement layer before semi-automated development by deciding whether existing skills are enough, whether manual handling is safer, which MCPs may be connected, which harness checks must guard them, and which decisions require human approval. Use only when a Codex-style development plan explicitly needs framework, skill, MCP, registry, or governance expansion before product code is written.
---

# Capability Enablement Planner

## Purpose

Decide whether enabling capabilities are needed before coding starts. This skill answers "can the current architecture handle this with existing tools, or is a supervised extension proposal truly necessary?"

## Inputs

- PRD or delivery plan
- technical scope
- AI solution plan when available
- existing registry, steward, MCP, harness, preference-cache, and teaching constraints

## Workflow

1. Identify capability gaps that block safe semi-automated development.
2. For each gap, decide reuse existing skill, update existing skill, handle manually, defer, or create a proposal for a new skill. Prefer no new component when the current architecture is enough.
3. Define MCP candidates only when external evidence or integration is actually needed.
4. Define required harness checks, registry additions, steward ownership, and human approvals only when they are necessary to prevent a concrete risk.
5. Separate project-specific preferences from generic skill improvements.
6. Route supervised skill updates through teaching and proposal flow; never update skills silently.

## Output Contract

Read [references/output-contract.md](references/output-contract.md). In any capability-enablement output, include `capability_gaps`, `skill_reuse_decision`, `memory_learning_route`, and `human_approval_required`. Include `new_skill_candidates`, `mcp_candidates`, or `harness_requirements` only when a real gap remains after reuse, manual handling, or deferral.

## Guardrails

- Do not create a new skill when an existing skill can safely handle the task.
- Do not connect MCPs unless the task needs external data or external actions.
- MCP outputs are signals only and cannot directly decide PRD, MVP, model choice, or skill updates.
- Skill creation and skill updates require human approval and generalization review.
- Harness additions require concrete failure evidence; prefer existing checks, templates, or manual review before adding another checker.
