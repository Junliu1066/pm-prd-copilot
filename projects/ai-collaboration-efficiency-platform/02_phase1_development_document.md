# 一期开发文档：Skill 价值计算闭环

- 文档状态: 一期工程可执行 / 上线前业务参数待补齐
- 生成日期: 2026-05-08
- 适用读者: 研发负责人、前端、后端、测试、运维、AI 平台工程师
- 阶段目标: 先证明一次 Skill 调用可以被记录、授权、确认、评审、计分、解释和聚合。
- 上游文档:
  - PRD: [01_product_document.md](/Users/liujun/Desktop/产品经理skill/projects/ai-collaboration-efficiency-platform/01_product_document.md)
  - 数据库字段管理: [10_database_field_management.md](/Users/liujun/Desktop/产品经理skill/projects/ai-collaboration-efficiency-platform/10_database_field_management.md)

---

## 1. 一期冻结范围

一期只做内部 Skill 价值计算闭环:

- 账号导入 + RBAC。
- Skill 清单、released SkillVersion 读取。
- SkillSourcePackage 加密上传、加密存储、运行时解密执行、执行后清理。
- 任务创建、调用前上下文、SkillCall、TaskResult。
- 结果确认、人工修改耗时、返工情况、Skill 反馈。
- 基础 Review。
- ScoreRecord、公式快照、个人 / Skill / 组织基础看板。
- AuthorizationGrant、AuditLog、EncryptedSecret、UsageMeterRecord。
- Excel 报表导出。

一期不做:

- Prompt Lab、Prompt 候选优化、测试集回归。
- 完整 Skill 字段治理、字段级运营配置、完整 SOP / RAG / 测试样本管理。
- SkillVersion 多人发布门禁、候选版本、回滚。
- 成本归集、充值、license、真实结算。
- Skill 并发执行、ExecutionPlan、SkillSubCall、复杂 DAG。
- 完整知识库、通知、申诉。
- 外部客户 Skill 消费平台。

## 2. 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Python 3.11 + FastAPI + Pydantic |
| ORM / Migration | SQLAlchemy 2.x + Alembic |
| 数据库 | PostgreSQL |
| 队列 | Redis + Celery |
| 对象存储 | S3 兼容存储 / MinIO |
| 前端 | Next.js / React + TypeScript |
| 图表 | ECharts |
| 加密 | 服务端 AES-GCM 简单包级加密，密钥来自环境变量或部署 Secret |

## 3. 一期数据表

建表以 [10_database_field_management.md](/Users/liujun/Desktop/产品经理skill/projects/ai-collaboration-efficiency-platform/10_database_field_management.md) 为准。一期只创建:

```text
departments
users
roles
permissions
role_permissions
authorization_grants
audit_logs
encrypted_secrets
skills
skill_versions
skill_source_packages
skill_score_policies
score_formula_versions
tasks
skill_calls
task_results
review_groups
review_records
skill_feedback
score_records
usage_meter_records
report_exports
```

禁止一期创建:

```text
execution_plans
skill_sub_calls
skill_optimization_tasks
prompts
prompt_versions
datasets
dataset_cases
prompt_runs
prompt_evaluations
prompt_optimization_jobs
prompt_candidate_versions
prompt_compares
cost_allocation_records
settlement_accounts
recharge_transactions
license_entitlements
knowledge_assets
notifications
appeals
```

## 4. 一期页面

| 页面 | 路由 | 能力 |
|---|---|---|
| 工作台 | `/` | 待办、个人基础指标、常用 Skill、风险提醒 |
| 任务列表 | `/tasks` | 搜索、筛选、状态、创建入口 |
| 新建任务 | `/tasks/new` | 任务表单、Skill 选择、敏感校验 |
| 任务详情 | `/tasks/{id}` | 输入摘要、执行记录、结果确认、提交 Review、反馈 Skill 痛点 |
| Review 队列 | `/reviews` | 待审任务筛选、风险等级、SLA |
| Review 详情 | `/reviews/{id}` | 评分、意见、通过 / 退回 / 拦截 |
| 个人看板 | `/dashboard/personal` | 个人指标、证据链、公式解释 |
| Skill 看板 | `/analytics/skills` | Skill 维度节省工时、贡献分、有效调用率 |
| 组织看板 | `/analytics/orgs` | 组织维度趋势、覆盖率、风险分布 |
| 计分说明 | `/score-calculation` | 公式版本、权重来源、封顶和反刷分 |
| Skill 清单 | `/skills` | 搜索、状态、风险、可调用状态 |
| Skill 详情 | `/skills/{id}` | 员工看说明和反馈入口；管理者看基础配置和反馈聚合 |
| 反馈管理 | `/admin/skill-feedback` | 管理者查看聚合痛点、更新处理状态 |
| 源码包上传 | `/admin/skill-source-packages` | 上传、校验 manifest、加密存储、绑定 SkillVersion |
| 授权控制台 | `/admin/authorization` | 授权 Grant、有效权限、不可用原因 |
| 报表中心 | `/reports` | Excel 报表导出 |
| 管理后台 | `/admin` | 组织、角色、风控、审计 |

## 5. 一期核心 API

| 方法 | 路径 | 用途 |
|---|---|---|
| GET | `/api/me` | 当前用户、角色、权限、部门 |
| GET | `/api/skills` | Skill 清单，按权限返回可见字段 |
| GET | `/api/skills/{id}` | Skill 详情，普通视图不返回源码包引用 |
| POST | `/api/admin/skill-source-packages` | 上传 Skill 文件夹压缩包 |
| GET | `/api/admin/skill-source-packages/{id}/metadata` | 查看源码包元数据摘要 |
| POST | `/api/tasks` | 创建任务 |
| PATCH | `/api/tasks/{id}/context` | 补充调用前上下文 |
| POST | `/api/tasks/{id}/run` | 调用 Skill，生成 SkillCall |
| GET | `/api/metering/skill-calls/{id}` | 查看基础计量证据 |
| PATCH | `/api/task-results/{id}/confirmation` | 结果采用确认 |
| POST | `/api/skills/{id}/feedback` | 提交 Skill 使用反馈 |
| GET | `/api/skills/{id}/feedback/mine` | 查看自己反馈状态 |
| GET | `/api/reviews` | Review 队列 |
| POST | `/api/reviews/{id}/decision` | Review 决策 |
| POST | `/api/skill-calls/{id}/calculate` | 生成 ScoreRecord |
| GET | `/api/score-records/{id}/explanation` | 计分解释 |
| GET | `/api/dashboard/personal` | 个人看板 |
| GET | `/api/analytics/skills` | Skill 看板 |
| GET | `/api/analytics/orgs` | 组织看板 |
| GET | `/api/authorization/effective` | 授权有效性查询 |
| POST | `/api/reports/export` | 创建 Excel 导出 |
| GET | `/api/reports/exports/{id}` | 查询导出状态 |

## 6. Sprint 拆解

### Sprint 0：工程启动与数据库基线

周期: 1 周。

交付物:

- FastAPI 项目骨架、Pydantic Schema、SQLAlchemy / Alembic 基线。
- 通用响应、错误码、认证中间件、RBAC 中间件。
- 通用审计字段、软删除、乐观锁。
- AuditLog、EncryptedSecret、SecretProvider 小接口和 AES-GCM 简单包级加密。
- users、departments、roles、permissions、role_permissions、authorization_grants。

验收:

- 权限失败返回 `FORBIDDEN`，未登录返回 `UNAUTHENTICATED`。
- 任意写操作能写入 `audit_request_id`。
- SecretProvider 可完成 AES-GCM 加密 / 解密测试，密钥不入库明文。

### Sprint 1：Skill、任务和 SkillCall

周期: 2 周。

交付物:

- skills、skill_versions、skill_source_packages、tasks、skill_calls、task_results。
- Skill 清单、Skill 详情、任务表单、执行记录页面。
- SkillSourcePackage 上传和元数据接口。
- `POST /api/tasks`、`PATCH /api/tasks/{id}/context`、`POST /api/tasks/{id}/run`。

验收:

- 员工能创建任务、补充上下文并调用已发布 Skill。
- 上传的 Skill 文件夹压缩包能校验 manifest，并加密存储。
- `SkillCall.context_snapshot`、`authorization_snapshot`、`execution_snapshot` 完整入库。
- Worker 运行时临时解密源码包，执行后清理临时目录。
- 一期不创建 `ExecutionPlan`、`SkillSubCall`，不开放 execution-plan 接口。

### Sprint 2：结果确认、反馈和基础 Review

周期: 2 周。

交付物:

- 结果确认接口和确认卡片。
- Skill 反馈接口、员工反馈入口、管理端反馈聚合。
- review_groups、review_records。
- Review 队列和 Review 详情页。

验收:

- 缺少采用状态或人工修改耗时时，不允许进入确认计分。
- `major_edit`、`not_used` 必须收集问题原因。
- P1 任务必须进入 Review，Review 未通过不得计分。
- 员工只能反馈使用痛点，不能修改 Skill、Prompt、权重、风险或 Review 规则。

### Sprint 3：价值计算和基础看板

周期: 2 周。

交付物:

- skill_score_policies、score_formula_versions、score_records。
- usage_meter_records 与 ScoreRecord 关联解释。
- 计分接口、解释接口、个人 / Skill / 组织看板。

验收:

- 单次分数能解释基准工时、使用后工时、有效性系数、权重和封顶。
- `formula_snapshot` 不随规则变更回写。
- `pending`、`rejected` 不进入确认看板。
- 看板按角色权限过滤，员工不能查看他人敏感任务。

### Sprint 4：一期收口、灰度和验收

周期: 1 周。

交付物:

- report_exports 表和 Excel 导出接口。
- 权限回归测试、状态机测试、计分测试、审计测试。
- 灰度上线方案、回滚方案、一期验收清单。

验收:

- 主路径跑通: 创建任务 -> 调用 Skill -> 确认结果 -> Review -> 计分 -> 看板更新。
- 报表按权限过滤，不包含源码、密钥、成本单价或未授权敏感输入全文。
- Skill、Review、Score、授权、计量、报表导出关键动作都有审计。

## 7. 一期工程执行契约

### 7.1 状态机

| 对象 | 状态 | 迁移约束 |
|---|---|---|
| Task | `draft -> submitted -> running -> pending_review/approved/failed -> archived` | `failed` 可重新 `submitted`；P0 风险进入 `blocked` 后只能归档 |
| SkillCall | `created -> running -> succeeded/failed -> confirmed/scored` | `failed` 不得生成确认态 TaskResult；一期 `execution_mode` 固定 `single` |
| TaskResult | `candidate -> saved/submitted_review -> approved/rejected` | 进入计分前必须有 `adoption_status` 和 `human_edit_minutes` |
| ReviewGroup | `pending -> approved/returned/blocked/need_recheck` | P1 必须完成 Review 才能计分 |
| ScoreRecord | `draft -> pending -> confirmed/rejected/adjusted/frozen` | `frozen` 不能原地修改，只能追加调整记录 |
| ReportExport | `queued -> running -> succeeded/failed/expired` | 导出文件过期后不可下载 |

### 7.2 API 契约补充

通用错误码:

| HTTP | code | 场景 |
|---|---|---|
| 400 | `VALIDATION_ERROR` | 缺字段、类型错误、枚举非法 |
| 401 | `UNAUTHENTICATED` | 未登录 |
| 403 | `FORBIDDEN` | 无权限、越权访问、字段不可见 |
| 404 | `NOT_FOUND` | 对象不存在或已软删除 |
| 409 | `STATE_CONFLICT` | 状态不允许迁移或 row_version 冲突 |
| 422 | `BUSINESS_RULE_BLOCKED` | P0 风险、未确认结果、Review 未通过 |
| 503 | `SECRET_UNAVAILABLE` | 密钥不可用，停止执行 |

`POST /api/tasks`:

```json
{
  "title": "生成月度经营分析报告",
  "task_type": "business_analysis_report",
  "business_scenario": "finance_monthly_review",
  "business_object": "2026-04 月经营数据",
  "expected_output": "报告正文 + 风险点 + 建议动作",
  "complexity": "standard",
  "skill_id": "sk_001",
  "input_summary": "已上传经营数据和预算文档",
  "input_object_key": "s3://..."
}
```

响应必须返回 `task_id`、`status`、`risk_level`、`required_context_fields`。

`POST /api/tasks/{id}/run`:

```json
{
  "skill_id": "sk_001",
  "skill_version_id": "skv_001",
  "input_payload_ref": "s3://...",
  "idempotency_key": "task_run_001"
}
```

约束:

- 必须校验 `AuthorizationGrant.call`。
- 必须写 `SkillCall.authorization_snapshot`。
- 必须从 `SkillVersion.source_package_id` 运行时解密。
- 不允许请求传 `parallel_policy`、`execution_plan` 或 `max_parallelism`。

`PATCH /api/task-results/{id}/confirmation`:

```json
{
  "adoption_status": "minor_edit",
  "human_edit_minutes": 52,
  "rework_required": false,
  "business_submitted": true,
  "comment": "已小幅调整图表说明"
}
```

约束:

- 只能任务创建人确认；管理员不能代替员工确认。
- `major_edit`、`not_used` 必须要求原因并引导反馈。

`POST /api/skill-calls/{id}/calculate`:

```json
{
  "formula_version_code": "score_v1_2026_05",
  "force_recalculate": false
}
```

响应必须返回 `score_record_id`、`contribution_score`、`confirmed_saved_minutes`、`formula_snapshot` 和 `explanation`。

### 7.3 权限契约

| 角色 | 一期权限 |
|---|---|
| employee | 创建自己的任务、调用授权 Skill、确认自己的结果、提交反馈、看个人看板 |
| reviewer | 查看授权 Review 队列、提交 Review 决策 |
| manager | 查看本部门或授权范围内汇总和必要明细 |
| hr | 默认只看汇总趋势，不看敏感输入明细 |
| skill_admin | 管理授权范围内 Skill 基础配置、源码包上传、反馈处理 |
| system_admin | 管组织、角色、权限和审计；默认不自动获得源码明文 |

字段过滤:

- 普通 Skill 列表 / 详情不返回 `source_package_id`、`encrypted_package_ref`、源码、底层 API、LangChain 代码段和完整环境依赖。
- `source_read` 一期只允许 `skill_admin` / `system_admin` 看脱敏摘要。
- `source_export` 一期不开放。

### 7.4 异步任务

| 任务 | 队列 | 幂等键 | 失败处理 |
|---|---|---|---|
| Skill 运行 | `skill_run` | `task_id + skill_version_id + idempotency_key` | 失败写 SkillCall.failed 和审计，不生成确认态 TaskResult |
| 异步计分 | `score_calculate` | `skill_call_id + formula_version_code` | 可重试 2 次，仍失败标记 ScoreRecord.rejected |
| 报表导出 | `report_export` | `report_export_id` | 失败写 error_code / error_message，导出状态 failed |

### 7.5 测试要求

- 数据库迁移测试: 一期只创建一期表，不创建二期表。
- 权限测试: 员工不能看他人敏感任务；HR 只看汇总；`source_export` 不可用。
- 加密测试: 源码包加密存储、运行时解密、执行后清理、日志无源码。
- 状态机测试: Task、SkillCall、TaskResult、ReviewGroup、ScoreRecord 状态非法迁移返回 `STATE_CONFLICT`。
- 计分测试: 公式快照固定，规则变更不回写历史 ScoreRecord。
- 报表测试: Excel 导出按权限过滤，不含源码、密钥和未授权敏感全文。

### 7.6 一期 DoD

- 一期主链路可端到端跑通。
- 任意看板指标能下钻到 SkillCall、TaskResult、ReviewRecord、ScoreRecord 和公式快照。
- 所有写操作都有审计或操作日志。
- 未授权、P0 风险、密钥不可用、Review 未通过都有明确错误码。
- 一期未创建 Prompt Lab、成本结算、并发执行、知识库、消费平台和智能化相关生产表。
