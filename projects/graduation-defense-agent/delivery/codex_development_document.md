# Codex Development Document：毕业答辩辅导智能体

document_id: `codex-development-document-20260425`
paired_prd_artifact: `projects/graduation-defense-agent/02_prd.generated.md`
document_goal: 把 PRD 转成“可交给 Codex 半自动开发”的开发文档。

## 1. 总体结构

overall_structure:

- `pm-copilot-chief` 大管家负责流程推进、阶段门禁、管家分配和人工升级。
- `capability-enablement-steward` 负责判断复用 Skill、创建 Skill、接入 MCP、增加 harness。
- `delivery-planning-steward` 负责技术范围、版本路线、工期估算、交付效果。
- `ai-architecture-steward` 和 `ai-coaching-steward` 负责模型、Prompt、RAG、记忆、画像和自适应教学。
- `development-governance-steward` 负责 Skill/MCP 路由、开发治理系统和 Codex 任务包。
- `learning-steward` 与 `pm-coach` 负责项目偏好、用户教学、Skill 更新提案和回归。
- `random-audit-inspector` 与 `efficiency-steward` 负责越界抽查和效率审计。

## 2. 主开发流程

main_development_flow:

1. 输入 PRD 和项目资料。
2. 输出 `capability_enablement_plan`，判断能力是否足够。
3. 输出 `skill_mcp_routing_plan`，确定各阶段 Skill/MCP 分工和 source_trace。
4. 输出 `technical_scope`、`release_roadmap`、`effort_estimate`、`delivery_plan`。
5. 如果涉及 AI，输出模型选型、Prompt、RAG、记忆、画像、AI 技术架构。
6. 输出 `development_operating_system_plan`，接入大管家、小管家、随机检查、效率、教师机制。
7. 输出 `codex_task_package_blueprint` 和 `codex_task_packages`。
8. 用户确认高风险 gate 后，Codex 才进入半自动开发。
9. 开发后跑 harness、测试、随机审计和效率审计。
10. 用户反馈进入项目缓存或通用 Skill 更新提案。

## 3. MVP 开发目标

mvp_development_goal:

- 用户录入论文题目、专业、摘要、目录、研究方法和核心结论。
- 系统基于题库和论文资料生成答辩问题组。
- 用户提交回答后，系统给出追问、五维评分、示范改写和训练报告。
- 系统根据薄弱项生成复练计划。
- 学术诚信风险必须被拦截，不编造数据、文献或研究过程。

## 4. 技术开发路径

technical_delivery_path:

| phase | 目标 | 用户可见效果 |
| --- | --- | --- |
| Phase 0 | 仓库理解与技术方案确认 | 输出实现方案，不写核心代码 |
| Phase 0.1 | 能力启用和治理检查 | 判断 Skill/MCP/harness 是否需要扩展 |
| Phase 1 | 数据模型与 API 契约 | 前后端可基于契约并行开发 |
| Phase 2 | 规则版训练主链路 | 不依赖模型也能完成训练闭环 |
| Phase 3 | AI service 与 fallback | 接入模型调用，同时保留规则 fallback |
| Phase 4 | 前端 MVP 主路径 | 用户完成训练、看报告、进入复练 |
| Phase 5 | 测试、观测、回归 | Prompt 回归、接口测试、隐私删除、埋点验证 |
| Phase 6 | 人类验收与迭代 | 根据反馈最小修复并沉淀经验 |

## 5. AI 方案

ai_solution_when_needed:

- 问题组生成：模型 + 题库 + 论文资料，fallback 为规则题库抽题。
- 动态追问：模型按回答质量追问，fallback 为改进建议。
- 五维评分：模型按 rubric 输出结构化评分，fallback 为固定评分模板。
- 示范改写：模型改写回答结构，fallback 为回答框架。
- 复练计划：根据弱项生成题单，fallback 为按最低分维度复练。
- 学术诚信拦截：规则 + 低成本模型分类，规则优先。
- 模型选型当前是文档初筛，不是 API 实测结论；正式开发前必须跑 benchmark 并由用户核验真实性。

## 6. Codex 任务包摘要

codex_task_packages_summary:

| task | 类型 | Codex 可做 | 需要人工确认 |
| --- | --- | --- | --- |
| Task -2 | capability_enablement | 判断 Skill/MCP/harness 是否需要扩展 | Skill/MCP/harness 新增计划 |
| Task -1 | registry_harness | 生成治理任务蓝图 | 是否允许改 registry/harness |
| Task 0 | product_development | 理解仓库并输出实现方案 | 技术框架、数据库、游客模式 |
| Task 1 | product_development | 定义数据模型与 API 契约 | database_schema |
| Task 2 | product_development | 实现规则版训练主链路 | 主链路行为 |
| Task 3 | ai_development | 接入 AI service、Prompt、fallback | model_change、provider、成本 |
| Task 4 | product_development | 实现前端 MVP 主路径 | 页面交互和文案 |
| Task 5 | qa_review | 隐私删除、诚信拦截、安全边界 | 隐私文案、删除逻辑 |
| Task 6 | qa_review / learning | 回归、benchmark、埋点、效率审计 | 发布和 GitHub push |

## 7. 人工监督点

human_supervision_gates:

- `prd_scope`：修改 MVP、目标用户、核心流程。
- `database_schema`：新增或变更数据库结构。
- `external_api`：接入外部模型、存储、监控、支付。
- `mcp_integration`：接入新 MCP 或扩大 MCP 权限。
- `registry_harness`：新增 registry、artifact、steward、harness 规则。
- `model_change`：选择、替换、升级模型。
- `github_push`：推送远程仓库、创建 PR。
- `destructive_data`：删除数据库、清理历史数据。
- `skill_update`：修改通用 Skill 或记忆机制。

## 8. Harness / 审计 / 验收

harness_audit_validation:

- `registry`：检查 Skill、MCP、artifact、steward 是否注册一致。
- `plugin_boundary`：检查插件是否可拔插，是否越界引用宿主路径。
- `source_trace`：MCP 外部数据必须有来源和人工核验标记。
- `ai_solution`：AI 方案必须有模型候选池、Prompt、RAG、记忆、评审。
- `agentic_delivery`：半自动开发必须有能力启用、路由、治理、任务包和配套开发文档。
- `skill_generalization`：防止把项目偏好写进通用 Skill。
- `random_audit`：随机抽查 Skill/MCP/产物是否越界。
- `efficiency`：检查 token 浪费、重复输出、无效流转。
- `regression`：防止历史能力退化。

## 9. 学习迭代

learning_iteration:

- 项目偏好进入项目缓存，不污染通用 Skill。
- 通用方法进入 lesson，再生成 Skill 更新提案。
- 模型效果反馈进入 benchmark 和模型选型矩阵。
- 原型/PRD 修改建议先判断是项目偏好还是通用规则。
- Skill 改进必须经用户批准，再更新 Skill。
- 不确定反馈进入 open lesson，等待继续教学。

## 10. 超载升级

overload_escalation:

- 单个小管家管理超过 7 个 Skill 时，向用户汇报并建议拆分。
- MCP 超过 3 个并跨多个领域时，建议新增 MCP 管理小管家。
- 同时跑 2 条以上独立工作流时，建议新增同级大管家或拆分项目。
- harness 连续出现协调类失败时，暂停开发，先修治理结构。
