# Development Operating System Plan：毕业答辩辅导智能体

plan_id: `development-os-20260425`

## chief_steward

- pm-copilot-chief 负责阶段推进、管家分配、harness enforcement、人工升级和最终汇总。
- 当小管家数量或复杂度超出规则时，必须向用户汇报是否新增同级大管家或拆分部门。

## sub_stewards

| sub_steward | owns | capacity_limit |
| --- | --- | --- |
| capability-enablement-steward | capability_enablement, skill reuse/create decision, MCP need assessment | max 7 skills |
| development-governance-steward | Skill/MCP routing, development OS, Codex blueprint | max 7 skills |
| delivery-planning-steward | technical scope, roadmap, effort, delivery plan, agentic final plan | max 7 skills |
| ai-architecture-steward | model, Prompt, RAG, AI architecture, AI review | max 7 skills |
| learning-steward | preference cache, lesson, Skill proposal, regression | max 7 skills |

## random_audit

- audit_scope: Skill 输出是否越界、MCP 是否越界、source_trace 是否完整、artifact 是否由正确 owner 产出。
- report_to: pm-copilot-chief, 对应小管家, user。
- 随机检查官只能报告问题，不能直接修改 artifact。

## efficiency_audit

- metrics: skill_call_count, mcp_call_count, artifact_size, repeated_output, long_line, unnecessary_rework。
- optimization_route: 发现浪费后先生成优化建议，不能降低质量阈值。
- 对单个 Skill 的无效 token 消耗，需要路由到对应小管家生成优化提案。

## teacher

- captures: 用户教学、PRD 修改建议、原型反馈、模型选型反馈、Skill/MCP 管理反馈。
- cannot: 直接更新 Skill、直接写入长期记忆、批准自己的提案、替代用户确认。
- 教师只生成 lesson、memory proposal、skill proposal、harness proposal。

## preference_cache

- project_specific_route: 项目偏好进入项目缓存，不进入通用 Skill。
- clear_reset_policy: 用户可要求清除或重建项目偏好文件夹。
- 通用方法必须先通过 skill-generalization 审计。

## skill_update_proposal

- proposal_route: user feedback -> teaching lesson -> proposal -> human approval -> Skill update -> regression。
- human_approval_required: true。
- generalization_check_required: true。

## harness

required_checks:

- registry
- plugin_boundary
- steward_contract
- source_trace
- preference_cache
- ai_solution
- agentic_delivery
- skill_generalization
- random_audit
- efficiency
- real_output_eval

## escalation

| trigger | action |
| --- | --- |
| 小管家技能数量超过规则 | 提议新增小管家或拆分部门 |
| 多个 MCP 信号冲突 | 标记人工核验，不自动决策 |
| Skill 更新影响通用能力 | 生成提案并等待用户审批 |
| Codex 任务写入边界冲突 | 停止任务，重新拆分 allowed_write_paths |
