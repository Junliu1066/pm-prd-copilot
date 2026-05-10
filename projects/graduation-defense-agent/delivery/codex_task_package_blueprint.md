# Codex Task Package Blueprint：毕业答辩辅导智能体

blueprint_id: `codex-task-blueprint-20260425`

## development_document_output

document_goal: 把 PRD 转成“可交给 Codex 半自动开发”的开发文档。

### required_sections

| section | 内容要求 | 对应产物 |
| --- | --- | --- |
| overall_structure | 展示大管家、小管家、Skill、MCP、harness、教师、效率、随机检查的总体结构 | `development_operating_system_plan` |
| main_development_flow | 展示从 PRD 到能力启用、路由、技术方案、任务包、开发、验证、学习的主流程 | `agentic_delivery_plan` |
| steward_system | 明确各小管家的职责、容量边界和升级规则 | `development_operating_system_plan` |
| capability_enablement | 说明现有 Skill 是否够用，是否需要新 Skill、MCP、harness | `capability_enablement_plan` |
| skill_mcp_routing | 说明每个阶段允许调用哪些 Skill/MCP，MCP 如何 source_trace 和 fallback | `skill_mcp_routing_plan` |
| technical_delivery_path | 说明一期开发什么、版本路线、工期、用户可见效果、最终目标 | `technical_scope`, `release_roadmap`, `effort_estimate`, `delivery_plan` |
| ai_solution_when_needed | AI 项目必须包含模型选型、Prompt、RAG、记忆、画像、评测和 fallback | `ai_technical_architecture`, `model_selection_plan` |
| codex_task_packages | 把开发拆成 Codex 可执行任务，每个任务有写入边界、禁止区、验收命令 | `codex_task_packages` |
| human_supervision_gates | 明确 PRD、数据库、模型、MCP、Skill、GitHub、删除数据等人工确认点 | `human_supervision_plan` |
| harness_audit_validation | 明确开发前后要跑的 harness、回归、随机检查、效率审计 | `development_governance_report` |
| learning_iteration | 明确项目偏好、通用经验、Skill 提案、用户审批、回归评测的学习路径 | `development_operating_system_plan` |
| overload_escalation | 如果管家系统管不过来，必须上报用户并建议拆分同级大管家或新增小管家 | `development_operating_system_plan` |

### output_artifacts

- `capability_enablement_plan`
- `skill_mcp_routing_plan`
- `development_operating_system_plan`
- `codex_task_package_blueprint`
- `codex_development_document`
- `agentic_delivery_plan`
- `codex_task_packages`
- `human_supervision_plan`
- `development_governance_report`

### must_not_write_to

- 不能只写到开发日志。
- 不能绕过用户审批直接更新通用 Skill。
- 不能让 MCP 直接决定 PRD、MVP、模型最终选型或 Skill 更新。

## task_types

- capability_enablement
- skill_creation
- mcp_integration
- registry_harness
- product_development
- ai_development
- qa_review
- learning

## capability_enablement_tasks

| task_id | goal | allowed_write_paths | forbidden_write_paths | validation_commands | human_confirmation_points | minimal_fix_strategy |
| --- | --- | --- | --- | --- | --- | --- |
| CE-01 | 判断现有 Skill 是否够用，是否要建新 Skill/MCP/harness | delivery planning artifacts | product code, PRD scope | harness agentic_delivery | Skill/MCP 新增计划 | 只改 enablement plan |
| CE-02 | 把能力缺口转成开发前置任务 | codex task blueprint | product code | manual review | 是否允许进入开发 | 只补任务边界 |

## skill_creation_tasks

| task_id | proposal_only | human_approval_required | output |
| --- | --- | --- | --- |
| SK-01 | true | true | 新 Skill proposal，不直接落地 |
| SK-02 | true | true | Skill 更新 proposal，必须通过 generalization |

## mcp_integration_tasks

| task_id | source_trace_required | human_verification_required | output |
| --- | --- | --- | --- |
| MCP-01 | true | true | MCP 候选、权限边界、source_trace 字段 |
| MCP-02 | true | true | 外部信号收集结果，不能直接决定 PRD/MVP |

## registry_harness_tasks

| task_id | goal | validation_commands |
| --- | --- | --- |
| RH-01 | 注册 Skill、artifact、steward、plugin owner | `harness/run_harness.py --mode strict` |
| RH-02 | 新增或更新 harness 检查 | `python -m py_compile harness/*.py`, `git diff --check` |

## product_development_tasks

| task_id | goal | allowed_write_paths | forbidden_write_paths |
| --- | --- | --- | --- |
| PD-01 | 实现规则版主链路 | app/services, app/api, tests | PRD 范围文件、Skill 文件 |
| PD-02 | 接入 AI service fallback | app/ai, config example, tests/ai | `.env`, 未批准模型配置 |

## validation_commands

- registry/harness strict check
- regression check
- diff check
- product test suite
- Prompt benchmark

## human_confirmation_points

- skill_creation
- skill_update
- mcp_integration
- registry_harness
- model_change
- database_schema
- prd_scope
- github_push
- destructive_data

## minimal_fix_strategy

- 先修失败检查，不扩大重构范围。
- 先修 task package 边界，再写产品代码。
- Skill/MCP 不清楚时只生成提案，不接入生产流程。
- 外部信号不可靠时标记人工核验，不做自动决策。

## learning_route

- project_cache: 项目偏好、视觉偏好、业务取舍进入项目缓存。
- skill_update_proposal: 通用开发流程、通用评测方法、通用路由规则进入 Skill 提案。
- rejected_or_unclear: 进入 open lesson，等待用户继续教学。
