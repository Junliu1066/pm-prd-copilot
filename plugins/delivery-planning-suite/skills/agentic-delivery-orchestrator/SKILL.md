---
name: agentic-delivery-orchestrator
description: Convert PRD, feature matrix, flows, prototypes, delivery, AI, capability-enablement, Skill/MCP routing, and governance plans into reusable Codex-ready semi-automated development documents, phase plans, task packages, human supervision gates, and development governance reports. Use when product development should be executed by AI coding agents under human oversight.
---

# Agentic Delivery Orchestrator

## Purpose

Create a supervised AI-development execution plan only when the user is ready to turn product material into Codex execution. This skill answers "how should Codex-like agents develop this product safely under human supervision?"

It also enforces the product/development boundary:

- PRD/product package answers why, for whom, what, what scope, which functions, how users move, and what they see. The feature matrix, flow, and prototype may be embedded in the PRD or kept as companion product artifacts for rendering and review.
- Codex semi-auto development documents answer how Codex should implement, validate, govern, learn, and escalate.

## Inputs

- `prd_document` or `prd_markdown`
- `feature_matrix` when available
- `product_flow_map` and `prototype_preview` when available
- `technical_scope`
- `ai_technical_architecture` when available
- `release_roadmap`
- `effort_estimate`
- `delivery_plan`
- `delivery_quality_report`
- `capability_enablement_plan`
- `skill_mcp_routing_plan`
- `development_operating_system_plan`
- `codex_task_package_blueprint`

## Workflow

1. Verify document layering. Product materials such as feature matrices, flows, and prototype notes may live inside the PRD/product package; implementation details must be routed to the Codex development documents instead of expanding the PRD.
2. Choose the smallest output mode that satisfies the request:
   - Lightweight Codex delivery: use for ordinary development-ready PRDs, single-phase implementation plans, or when the user asks for a Codex development document.
   - Full agentic delivery: use only when the user explicitly asks for semi-automated agent delivery, multi-phase Codex execution, agent orchestration, or a complete development governance plan.
3. In lightweight mode, produce only the development document, task packages, human confirmation points, validation, rollback, and review needed for implementation.
4. In full agentic mode, verify capability enablement, Skill/MCP routing, development governance, and phase planning before producing the complete package.
5. Split the work into four phase documents only in full agentic mode or when the user explicitly asks for phase plans. Use the standard meanings:
   - Phase 1: MVP / core loop.
   - Phase 2: efficiency, personalization, and experience improvements.
   - Phase 3: collaboration, admin, backstage, or scale features.
   - Final: platformization, long-term intelligence, and advanced integrations.
6. Split Codex task packages with read/write boundaries.
7. Define development order, dependencies, and conflict rules.
8. Define human supervision gates for high-risk changes.
9. Define required checks and minimal-fix strategy.
10. Define feedback handling after human review. In lightweight mode, state whether feedback remains project-local, needs a later learning proposal, or requires no persistence.
11. Before sending development-facing documents to the user or starting implementation, route the generated plan through `codex-development-plan-reviewer` and attach the resulting `codex_development_review`.

## Output Contract

Read [references/output-contract.md](references/output-contract.md). For detailed document structure, read:

- [references/codex-development-plan-template.md](references/codex-development-plan-template.md)
- [references/phase-codex-plan-template.md](references/phase-codex-plan-template.md)

Use the output contract by mode:

- Lightweight Codex delivery must include a Codex development document or plan, Codex task packages, human supervision points, validation / rollback instructions, and `codex_development_review`.
- Full agentic delivery may additionally include `agentic_delivery_plan`, phase 1 / 2 / 3 / final Codex plans, capability enablement, Skill/MCP routing, development governance, and development governance reports.
- Do not generate full phase plans, governance operating-system details, or reusable framework mechanics for an ordinary lightweight development request unless the user explicitly asks for them.

## Guardrails

- Do not let agent tasks mutate PRD or MVP scope without human approval.
- Every task must declare allowed and forbidden write paths.
- Every task must include validation commands or manual review criteria.
- Do not assign overlapping write scopes without a conflict plan.
- Do not start product-code tasks until required capability, MCP, or harness enablement is planned or explicitly deferred.
- Do not let MCP outputs directly decide product scope, MVP, model choice, or skill updates.
- Do not let teaching or learning roles update skills without user approval.
- Do not put database schemas, API contracts, Prompt assets, model routes, GitHub process, or Codex task package details into the PRD/product package. Product feature matrices, product flows, and prototype notes are allowed there.
- Do not expand a lightweight Codex development request into full phase plans unless the user asks for phase plans or full agentic delivery.
- Do not generate a single vague development plan when the user expects phase plans. When phase plans are requested, separate phase 1, phase 2, phase 3, and final.
- Do not send development-facing documents as ready for implementation unless `codex_development_review` exists and states pass or warn with explicit blockers.
- Do not make learning persistent by default. Lightweight output must state whether feedback remains one-off or project-local. Full agentic delivery must state how user feedback becomes project memory, open lessons, skill proposals, or no persistent learning.
