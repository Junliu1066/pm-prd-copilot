# Phase Codex Plan Template

Use this template only when the user asks for full agentic delivery, multi-phase Codex execution, or explicit phase plans:

- `phase_1_codex_plan.md`
- `phase_2_codex_plan.md`
- `phase_3_codex_plan.md`
- `final_codex_plan.md`

## Full-Mode Required Sections

1. `阶段目标`
   - Define the phase goal in product and development terms.
   - State the user-visible effect.

2. `本期输入`
   - PRD sections.
   - Feature matrix rows.
   - Flow/prototype pages.
   - Prior phase outputs.
   - Technical/AI/delivery artifacts.

3. `本期范围`
   - Included product capabilities.
   - Excluded capabilities.
   - Scope backflow conditions.

4. `总体框架`
   - Frontend.
   - Backend.
   - Data.
   - AI / Prompt / RAG / memory.
   - Skill / MCP.
   - Harness.
   - GitHub / PR.
   - Teaching / learning.

5. `页面与交互`
   - Pages/screens in this phase.
   - User actions.
   - Empty/error/loading states.

6. `服务与数据`
   - Services or modules.
   - Data objects.
   - API groups or contracts.
   - Migration needs.

7. `AI / Prompt / RAG / Memory`
   - AI calls.
   - Prompt assets.
   - Retrieval or knowledge source needs.
   - Conversation or project memory.
   - Fallback behavior.

8. `Skill / MCP 接入`
   - Reused skills.
   - New skill proposals.
   - MCP candidates.
   - Source trace requirements.

9. `Codex 任务包`
   - Each task must include:
     - task id.
     - goal.
     - inputs.
     - allowed write paths.
     - forbidden write paths.
     - expected outputs.
     - validation commands or manual checks.
     - human confirmation points.
     - minimal fix strategy.

10. `人工确认点`
    - List high-risk gates for this phase.

11. `GitHub / 发布流程`
    - Branch.
    - Commit boundary.
    - PR or review route.
    - Release/rollback notes.

12. `Harness / 审计 / 回归`
    - Required harness checks.
    - Random audit.
    - Efficiency audit.
    - Prompt regression if relevant.

13. `教学与记忆沉淀`
    - What feedback becomes project preference.
    - What feedback becomes open lesson.
    - What feedback becomes skill update proposal.
    - What feedback stays one-off.
    - Required approvals.

14. `风险与回滚`
    - Product risk.
    - Technical risk.
    - Data/privacy risk.
    - AI/model risk.
    - Rollback path.

15. `验收标准`
    - Product acceptance.
    - Engineering acceptance.
    - Governance acceptance.
    - Learning/teaching acceptance.

16. `下一期衔接`
    - Outputs needed by the next phase.
    - Deferred scope.

## Phase Naming

- Phase 1 should use `一期`.
- Phase 2 should use `二期`.
- Phase 3 should use `三期`.
- Final should use `最终`.

## Guardrails

- Do not merge all phases into one generic table.
- Do not omit Codex task packages.
- Do not omit teaching/learning.
- Do not omit human confirmation gates.
- Do not allow overlapping write paths unless a conflict policy is written.
- Do not create phase documents for ordinary lightweight Codex development requests unless the user explicitly asks for phase planning.
