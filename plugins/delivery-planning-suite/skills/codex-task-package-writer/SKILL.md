---
name: codex-task-package-writer
description: Convert product, delivery, AI, capability-enablement, skill/MCP routing, and governance plans into Codex development documents and task package blueprints with write boundaries, validation commands, human confirmation points, minimal-fix strategy, and learning routes. Use when a PRD is development-ready, when the user asks for a Codex development document, or when a supervised implementation package is explicitly needed.
---

# Codex Task Package Writer

## Purpose

Create the smallest useful Codex development document and task blueprint for Codex-like tools. This skill answers "what development document is needed now, what exact tasks can be handed to coding agents, and what must humans approve?"

## Inputs

- PRD and delivery artifacts
- AI solution artifacts when available
- capability enablement plan
- skill/MCP routing plan
- development operating system plan

## Workflow

1. Choose the smallest output mode that satisfies the request:
   - Lightweight development document: default for ordinary development-ready PRDs and single-phase implementation planning.
   - Full supervised package: use only when the user asks for semi-automated delivery, capability enablement, MCP integration, registry/harness work, or multi-agent governance.
2. Create `codex_development_document` as the paired development document for the PRD.
3. Create the `development_document_output` section only as detailed as the selected mode requires.
4. Define task types only when they are relevant to the selected mode: product code, AI code, QA, review, capability enablement, registry/harness, MCP integration, efficiency, or learning.
5. For each task, define owner, inputs, allowed write paths, forbidden write paths, expected outputs, validation commands, human confirmation points, and minimal-fix strategy.
6. Mark tasks that only produce proposals and cannot write implementation files.
7. Add learning routes after task review, without making learning persistent by default.
8. Keep tasks small enough to review and avoid overlapping write scopes.

## Output Contract

Read [references/output-contract.md](references/output-contract.md). In lightweight mode, include only `codex_development_document`, relevant `product_development_tasks` or `ai_development_tasks`, `validation_commands`, `human_confirmation_points`, `minimal_fix_strategy`, and a non-persistent `learning_route` note. Include `capability_enablement_tasks`, `skill_creation_tasks`, `mcp_integration_tasks`, and `registry_harness_tasks` only when the user or approved plan explicitly requests that layer.

## Guardrails

- Do not allow a task to write outside its declared paths.
- Do not force a `codex_development_document` for exploratory PRDs that are not development-ready unless the user requests one.
- Do not allow a task to create or update skills without explicit human approval.
- MCP integration tasks must include source trace and verification requirements.
- If a task changes scope, route back to PM approval instead of continuing.
- Do not write the semi-automated development scheme only into a changelog or development note. It must appear in the generated development document output.
