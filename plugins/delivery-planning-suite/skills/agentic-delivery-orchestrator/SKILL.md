---
name: agentic-delivery-orchestrator
description: Convert PRD, feature matrix, flows, prototypes, delivery, AI, capability-enablement, Skill/MCP routing, and governance plans into reusable Codex-ready semi-automated development documents, phase plans, task packages, human supervision gates, and development governance reports. Use when product development should be executed by AI coding agents under human oversight.
---

# Agentic Delivery Orchestrator

## Purpose

Create a supervised AI-development execution plan. This skill answers "how should Codex-like agents develop this product safely while reusing or extending the skill/MCP/harness/governance operating system?"

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
2. Verify capability enablement: existing skill reuse, new skill proposals, MCP candidates, harness requirements, and approvals.
3. Verify Skill/MCP routing: each stage has steward ownership, allowed skills/MCPs, source-trace requirements, fallback, and escalation.
4. Verify development governance: chief steward, sub-stewards, random audit, efficiency, teacher, preference cache, skill update proposal route, and harness checks.
5. Create a project-level `codex_development_plan` that can be handed to Codex for semi-automated development.
6. Split the work into four phase documents: phase 1, phase 2, phase 3, and final. Use the standard meanings:
   - Phase 1: MVP / core loop.
   - Phase 2: efficiency, personalization, and experience improvements.
   - Phase 3: collaboration, admin, backstage, or scale features.
   - Final: platformization, long-term intelligence, and advanced integrations.
7. For every phase document, include framework, teaching/learning route, Skill/MCP routing, data changes, model/Prompt/RAG/memory work, Codex task packages, write boundaries, human confirmation points, GitHub/PR flow, harness/audit/regression, risks, rollback, and acceptance criteria.
8. Split Codex task packages with read/write boundaries.
9. Define development order, dependencies, and conflict rules.
10. Define human supervision gates for high-risk changes.
11. Define required checks and minimal-fix strategy.
12. Define feedback learning loop after human review.
13. Before sending development-facing documents to the user or starting implementation, route the generated Codex development plan and phase plans through `codex-development-plan-reviewer` and attach the resulting `codex_development_review`.

## Output Contract

Read [references/output-contract.md](references/output-contract.md). For detailed document structure, read:

- [references/codex-development-plan-template.md](references/codex-development-plan-template.md)
- [references/phase-codex-plan-template.md](references/phase-codex-plan-template.md)

Always include `codex_development_plan`, `phase_1_codex_plan`, `phase_2_codex_plan`, `phase_3_codex_plan`, `final_codex_plan`, `codex_development_review`, `agentic_delivery_plan`, `codex_task_packages`, `human_supervision_plan`, and `development_governance_report`. The final plan must explicitly absorb capability enablement, Skill/MCP routing, governance operating system, Codex task package blueprint, and the send-before-review result.

## Guardrails

- Do not let agent tasks mutate PRD or MVP scope without human approval.
- Every task must declare allowed and forbidden write paths.
- Every task must include validation commands or manual review criteria.
- Do not assign overlapping write scopes without a conflict plan.
- Do not start product-code tasks until required Skill/MCP/harness enablement is planned or explicitly deferred.
- Do not let MCP outputs directly decide product scope, MVP, model choice, or skill updates.
- Do not let teaching or learning roles update skills without user approval.
- Do not put database schemas, API contracts, Prompt assets, model routes, GitHub process, or Codex task package details into the PRD/product package. Product feature matrices, product flows, and prototype notes are allowed there.
- Do not generate a single vague development plan when the user expects phase plans. Always separate phase 1, phase 2, phase 3, and final.
- Do not send development-facing documents as ready for implementation unless `codex_development_review` exists and states pass or warn with explicit blockers.
- Do not omit the teaching/learning route. Each phase must state how user feedback becomes project memory, open lessons, skill proposals, or no persistent learning.
