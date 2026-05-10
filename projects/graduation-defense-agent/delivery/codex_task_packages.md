# Codex Task Packages：毕业答辩辅导智能体

task_package_id: `codex-task-packages-20260425`

## Task -2：capability_enablement 能力启用检查

- task_type: capability_enablement
- owner: Capability enablement steward
- goal: 在写产品代码前确认是否需要复用、更新或创建 Skill，是否需要 MCP，是否需要新增 harness。
- inputs: capability_enablement_plan、technical_scope、ai_technical_architecture
- allowed_write_paths: `delivery/capability_enablement_plan.md`, `delivery/skill_mcp_routing_plan.md`
- forbidden_write_paths: 产品代码、PRD 范围文件、通用 Skill 文件
- validation_commands: agentic_delivery harness check
- human_confirmation_points: skill_creation、skill_update、mcp_integration、registry_harness
- minimal_fix_strategy: 只修正能力启用计划，不进入产品代码开发

## Task -1：skill_creation / mcp_integration / registry_harness 蓝图

- task_type: skill_creation, mcp_integration, registry_harness
- owner: Development governance steward
- goal: 把 Skill 创建、MCP 接入、registry/harness 更新转成 Codex 可执行但受监督的任务包。
- inputs: codex_task_package_blueprint、development_operating_system_plan
- allowed_write_paths: `delivery/codex_task_package_blueprint.md`, `delivery/development_operating_system_plan.md`
- forbidden_write_paths: `.env`, 产品代码、未批准的 Skill 文件、未批准的 MCP 配置
- validation_commands: harness strict, regression, diff check
- human_confirmation_points: 新 Skill 创建、MCP 接入、harness 规则变更、registry 变更
- minimal_fix_strategy: 只改任务包边界和验证命令，不私自创建或接入

## Task 0：仓库理解与实现方案确认

- task_type: product_development
- owner: Product steward + Review steward
- goal: 理解现有项目框架，确认采用 Web/H5、后端服务、数据库和 AI service 的落地方式。
- inputs: PRD、technical_scope、delivery_plan、ai_technical_architecture
- allowed_write_paths: `docs/implementation_plan.md`, `docs/open_questions.md`
- forbidden_write_paths: `app/`, `src/`, `database/`, `.env`, PRD 原始文件
- validation_commands: 人工审阅实现方案，无代码测试要求
- human_confirmation_points: 技术框架、数据库选择、首发平台、是否游客模式
- minimal_fix_strategy: 只补充方案缺口，不开始写业务代码

## Task 1：数据模型与 API 契约

- task_type: product_development
- owner: Backend steward
- goal: 定义训练会话、题目、回答、评分、报告、复练和删除能力的数据结构与 API contract。
- inputs: technical_scope、ai_technical_architecture
- allowed_write_paths: `app/models/`, `app/schemas/`, `app/api/contracts/`, `tests/contracts/`
- forbidden_write_paths: PRD 范围文件、前端页面目录、Prompt 文件、`.env`
- validation_commands: `python -m compileall app`, contract tests
- human_confirmation_points: database_schema、隐私删除字段、是否支持游客模式
- minimal_fix_strategy: 只修复契约不一致和编译失败，不重写架构

## Task 2：训练主链路后端

- task_type: product_development
- owner: Backend steward
- goal: 实现创建训练、抽题、提交回答、报告生成、复练入口的规则版主链路。
- inputs: API 契约、题库结构、delivery_plan
- allowed_write_paths: `app/services/training/`, `app/api/routes/training/`, `tests/training/`
- forbidden_write_paths: PRD 范围文件、AI 模型配置、前端样式
- validation_commands: backend unit tests, API smoke tests
- human_confirmation_points: 主链路行为是否符合 PRD
- minimal_fix_strategy: 优先修复失败接口和状态流，不引入新功能

## Task 3：AI service 与 fallback

- task_type: ai_development
- owner: AI steward
- goal: 接入 model_gateway、prompt_registry、AI API、结构化输出校验和规则 fallback。
- inputs: ai_technical_architecture、model_selection_plan、prompt_architecture、rag_architecture
- allowed_write_paths: `app/ai/`, `app/services/ai/`, `tests/ai/`, `config/ai.example.yaml`
- forbidden_write_paths: `.env`, PRD 范围文件、数据库迁移、前端页面
- validation_commands: AI service unit tests, Prompt schema tests, fallback smoke tests
- human_confirmation_points: model_change、外部模型 provider、成本阈值、benchmark_plan 通过情况
- minimal_fix_strategy: 保留规则 fallback，先修复接口和 schema，不强行提升模型质量

## Task 4：前端 MVP 主路径

- task_type: product_development
- owner: Frontend steward
- goal: 实现新建训练、模拟答辩、评分反馈、报告、复练入口。
- inputs: PRD、prototype_preview、API contract
- allowed_write_paths: `src/pages/`, `src/components/training/`, `src/styles/`, `tests/frontend/`
- forbidden_write_paths: 后端数据模型、AI Prompt、PRD 范围文件
- validation_commands: frontend build, component tests, manual mobile viewport review
- human_confirmation_points: 关键页面交互、文案、报告展示方式
- minimal_fix_strategy: 优先修复主路径阻断问题，不做视觉大改

## Task 5：隐私、学术诚信和删除能力

- task_type: qa_review
- owner: Review steward + Backend steward
- goal: 验证数据删除、敏感提示、诚信拦截、外部输出免责声明。
- inputs: conversation_memory_plan、prompt_architecture、risk_report
- allowed_write_paths: `app/security/`, `app/services/privacy/`, `tests/security/`, `tests/privacy/`
- forbidden_write_paths: PRD 范围文件、模型选择文件、前端大范围重构
- validation_commands: privacy tests, integrity guardrail tests
- human_confirmation_points: destructive_data、隐私文案、学术诚信边界
- minimal_fix_strategy: 只补拦截规则和删除链路，不扩展新审核系统

## Task 6：回归、观测和发布前验收

- task_type: qa_review, learning
- owner: QA steward + Efficiency steward
- goal: 建立主路径回归、Prompt benchmark、埋点校验和效率审计。
- inputs: delivery_quality_report、ai_solution_review、tracking_plan
- allowed_write_paths: `tests/e2e/`, `tests/prompt_regression/`, `docs/release_checklist.md`
- forbidden_write_paths: 业务逻辑核心目录、PRD 范围文件、`.env`
- validation_commands: full test suite, Prompt benchmark, harness/regression
- human_confirmation_points: 发布前验收、GitHub push、是否进入下一版本
- minimal_fix_strategy: 只修复阻断发布的问题，非阻断项进入 backlog
