---
name: codex-task-package-writer
description: Convert product, delivery, AI, capability-enablement, skill/MCP routing, and governance plans into paired Codex development documents and task package blueprints with write boundaries, validation commands, human confirmation points, minimal-fix strategy, and learning routes. Use whenever a product document needs a companion development document executable by Codex-like coding agents.
---

# Codex Task Package Writer

## Purpose

Create the companion Codex development document and execution-ready task blueprints for Codex-like tools. This skill answers "what development document must ship next to the PRD, what exact tasks can be handed to coding agents, and what must humans approve?"

## Inputs

- PRD and delivery artifacts
- AI solution artifacts when available
- capability enablement plan
- skill/MCP routing plan
- development operating system plan

## Workflow

1. Create `codex_development_document` as the paired development document for the PRD.
2. Create the `development_document_output` section in the blueprint. This section explains how the PRD becomes a Codex-ready semi-automated development document.
3. Define task types: capability enablement, registry/harness, MCP integration, product code, AI code, QA, review, efficiency, and learning.
4. For each task, define owner, inputs, allowed write paths, forbidden write paths, expected outputs, validation commands, human confirmation points, and minimal-fix strategy.
5. Mark tasks that only produce proposals and cannot write implementation files.
6. Add learning routes after task review.
7. Keep tasks small enough to review and avoid overlapping write scopes.

## Output Contract

Read [references/output-contract.md](references/output-contract.md). Always include `codex_development_document`, `development_document_output`, `task_types`, `capability_enablement_tasks`, `skill_creation_tasks`, `mcp_integration_tasks`, `registry_harness_tasks`, `product_development_tasks`, `validation_commands`, `human_confirmation_points`, `minimal_fix_strategy`, and `learning_route`.

## Guardrails

- Do not allow a task to write outside its declared paths.
- Do not output a PRD without a companion `codex_development_document` unless the user explicitly disables development planning.
- Do not allow a task to create or update skills without explicit human approval.
- MCP integration tasks must include source trace and verification requirements.
- If a task changes scope, route back to PM approval instead of continuing.
- Do not write the semi-automated development scheme only into a changelog or development note. It must appear in the generated development document output.
