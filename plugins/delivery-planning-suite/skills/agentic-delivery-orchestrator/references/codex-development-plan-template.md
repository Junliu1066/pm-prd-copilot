# Codex Semi-Auto Development Plan Template

Use this template for the project delivery artifact named `codex_development_plan.md` only when the user asks for full agentic delivery, multi-phase Codex execution, or a complete development governance plan.

For lightweight Codex development documents, do not copy the full template. Use the smaller contract: document goal, inputs, development scope, task packages, allowed / forbidden write paths, human confirmation points, validation commands, rollback, open decisions, and review result.

## Full-Mode Required Sections

1. `文档目标`
   - State that the document converts product artifacts into Codex semi-automated development execution.
   - Link the paired PRD/product package and phase documents. If feature matrix, flow, or prototype artifacts are split out for rendering, link them as product-package companion files, not as separate development documents.

2. `当前状态`
   - State planning status.
   - List what can proceed immediately and what requires human confirmation.

3. `总体结构`
   - Show the operating framework: chief steward, sub-stewards, product, delivery, AI, MCP, GitHub, database, harness, teaching, memory.
   - Include a Mermaid diagram when useful.

4. `主开发流程`
   - Flow from PRD/product package to development planning, Codex task packages, implementation, validation, review, and learning.

5. `阶段总览`
   - Phase 1: MVP / core loop.
   - Phase 2: efficiency, personalization, experience improvement.
   - Phase 3: collaboration, admin, backstage, scale.
   - Final: platformization, long-term intelligence, advanced integrations.

6. `通用 Codex 执行框架`
   - Inputs.
   - Outputs.
   - Task package format.
   - Allowed write boundaries.
   - Forbidden write boundaries.
   - Validation rules.

7. `Skill / MCP / Harness 框架`
   - Existing skills to reuse.
   - Candidate skills to propose.
   - MCP candidates.
   - Harness checks.
   - Source trace requirements.

8. `AI / Prompt / RAG / Memory 框架`
   - Model routes.
   - Prompt assets.
   - RAG needs.
   - Short memory and long memory boundaries.
   - Privacy and deletion.

9. `教学与记忆沉淀`
   - User feedback handling.
   - Project preference cache route.
   - Open lesson route.
   - Skill update proposal route.
   - Approval requirements.

10. `人工确认点`
    - PRD scope.
    - Database schema.
    - External API / model provider.
    - MCP integration.
    - GitHub push / PR.
    - Skill update.
    - Memory update.
    - Destructive data action.

11. `验收与回归`
    - Unit / integration checks.
    - Harness checks.
    - Random audit.
    - Efficiency audit.
    - Prompt regression if AI is involved.
    - Send-before-review by `codex-development-plan-reviewer`.

12. `阶段文档索引`
    - `phase_1_codex_plan.md`
    - `phase_2_codex_plan.md`
    - `phase_3_codex_plan.md`
    - `final_codex_plan.md`
    - `codex_development_review.md`

## Full-Mode Output Links

The full-mode plan must link:

- PRD/product package
- feature matrix, product flow, and prototype preview when they are available as companion product artifacts
- delivery plan or release roadmap when available
- phase Codex plans when generated
- Codex development review
- task packages
- human supervision plan
- development governance report

## Forbidden Content

- Do not redefine product scope differently from the PRD.
- Do not approve model, MCP, database, GitHub, memory, or skill changes on behalf of the user.
- Do not bury teaching/learning in generic notes. It must be a named section.
- Do not use this full template for ordinary lightweight implementation requests.
