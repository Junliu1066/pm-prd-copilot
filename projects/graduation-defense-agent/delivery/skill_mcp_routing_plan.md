# Skill MCP Routing Plan：毕业答辩辅导智能体

plan_id: `skill-mcp-routing-20260425`

## stage_routing

| stage | steward_assignment | allowed_skills | allowed_mcps | input_artifacts | output_artifacts |
| --- | --- | --- | --- | --- | --- |
| capability_enablement | capability-enablement-steward | `capability-enablement-planner` | none by default | PRD, technical_scope, delivery_plan | capability_enablement_plan |
| skill_mcp_routing | capability-enablement-steward | `skill-mcp-routing-planner` | fetch/firecrawl only when external evidence needed | capability_enablement_plan | skill_mcp_routing_plan |
| ai_solution | ai-architecture-steward, ai-coaching-steward | AI solution skills | fetch/firecrawl for official docs only | ai_capability_map, model_selection_plan | ai_technical_architecture |
| development_governance | development-governance-steward | `development-governance-orchestrator` | none | capability_enablement_plan, skill_mcp_routing_plan | development_operating_system_plan |
| codex_blueprint | development-governance-steward | `codex-task-package-writer` | none | all delivery and governance artifacts | codex_task_package_blueprint |
| product_code | backend/frontend/AI/QA stewards | coding tasks from task package | GitHub/browser-use only after approval | codex_task_packages | implementation outputs |
| review_learning | review-steward, learning-steward, teacher | review, skill-generalization, preference cache | GitHub for PR status only | diff, tests, user feedback | proposals and reports |

## skill_boundaries

| skill | allowed_outputs | forbidden_outputs |
| --- | --- | --- |
| `capability-enablement-planner` | capability_enablement_plan | prd_document, mvp_scope, skill_update |
| `skill-mcp-routing-planner` | skill_mcp_routing_plan | prd_document, model_final_decision, skill_update |
| `development-governance-orchestrator` | development_operating_system_plan | direct memory update, direct skill update |
| `codex-task-package-writer` | codex_task_package_blueprint | product scope mutation |
| `agentic-delivery-orchestrator` | agentic_delivery_plan, codex_task_packages, human_supervision_plan, development_governance_report | unapproved PRD/MVP changes |

## mcp_boundaries

| mcp | allowed_outputs | forbidden_outputs | source_trace_required | human_verification_required |
| --- | --- | --- | --- | --- |
| fetch/firecrawl | web_source, official_doc_signal, pricing_signal | final_model_choice, PRD decision, Skill update | true | true |
| GitHub | repo_status, PR_status, CI_status | unapproved_push, destructive_reset | true | true |
| browser-use | local_preview_signal, screenshot_signal | product_scope_decision | false | true |

## source_trace

- 外部页面、模型价格、竞品信息必须记录 URL、访问时间、提取字段、human_verification_required。
- MCP 只能提供外部信号，不能直接决定 MVP、PRD、模型最终选型或 Skill 更新。
- AI 情报源每次输出都要提醒用户核验真实性。

## fallback

| unavailable_component | fallback_action |
| --- | --- |
| 外部网页抓取失败 | 使用用户提供资料和历史缓存，标记“外部信号缺失” |
| GitHub connector 不可用 | 只生成本地 diff 和命令，不推送 |
| browser-use 不可用 | 输出截图/HTML 文件路径供人工查看 |
| Skill 不足 | 先生成 Skill proposal，不直接写产品代码 |

## escalation_rules

- steward_assignment 超过容量时，上报 pm-copilot-chief。
- MCP 输出和 Skill 输出冲突时，由 review-steward 抽查，必要时用户决策。
- 涉及删除、推送、模型变更、数据库结构、Skill 更新时必须人工确认。
