---
name: skill-mcp-routing-planner
description: Route each semi-automated development stage to the correct steward, skill, MCP, artifact, source-trace requirement, fallback path, and human approval gate. Use when a project has multiple skills, MCPs, managers, or governance checks and needs each capability to stay in its lane.
---

# Skill MCP Routing Planner

## Purpose

Create a routing map for skills and MCPs so each department does the right work and no external tool or skill oversteps its boundary.

## Inputs

- capability enablement plan
- registered skills, MCPs, artifacts, and stewards
- delivery and AI plans
- source and evidence requirements

## Workflow

1. Split development into stages and assign steward ownership.
2. Assign allowed skills and MCPs per stage.
3. Define what each skill or MCP may read and write.
4. Require source trace and human verification for MCP-derived external signals.
5. Define fallback when a skill or MCP is unavailable.
6. Escalate to the chief steward when a steward exceeds capacity or a conflict appears.

## Output Contract

Read [references/output-contract.md](references/output-contract.md). Always include `stage_routing`, `steward_assignment`, `skill_boundaries`, `mcp_boundaries`, `source_trace`, `fallback`, and `escalation_rules`.

## Guardrails

- MCPs collect or act; they do not decide product scope, MVP, model choice, or skill updates.
- Skills write only declared artifacts.
- When routing is unclear, ask for human confirmation instead of guessing.
- Keep the plan detachable from any single project implementation.
