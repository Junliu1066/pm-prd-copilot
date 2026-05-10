# AI 协作效率平台数据库字段管理文档

- 文档状态: 产品方案 Ready / 一期开发范围待确认 / 上线前业务参数待补齐
- 生成日期: 2026-05-08
- 适用读者: 后端、数据库工程师、测试、开发 Agent、研发负责人
- 文档用途: 单独管理数据库表、字段、主外键、唯一约束、索引、软删除、审计字段和 JSONB 结构，避免开发时从 PRD / 原型 / 开发文档里自行脑补字段。
- 关联文档:
  - PRD: [01_product_document.md](/Users/liujun/Desktop/产品经理skill/projects/ai-collaboration-efficiency-platform/01_product_document.md)
  - 开发文档: [02_development_document.md](/Users/liujun/Desktop/产品经理skill/projects/ai-collaboration-efficiency-platform/02_development_document.md)
  - 原型图: [06_prototype_wireframes.md](/Users/liujun/Desktop/产品经理skill/projects/ai-collaboration-efficiency-platform/06_prototype_wireframes.md)

---

## 0. 字段管理结论

本文件是数据库建模和 Alembic migration 的字段依据。开发 Agent 拆数据库任务时，以本文件的“一期表清单”和“一期字段清单”为准；PRD、原型图和开发文档中的二期规划不得反向扩大一期数据库范围。

一期只建 Skill 价值计算闭环所需的生产表:

```text
账号 / 组织 / RBAC
Skill / SkillVersion / SkillSourcePackage
Task / SkillCall / TaskResult
Review / Feedback
Score / Formula / Metering
Authorization / Secret / Audit
ReportExport
```

一期明确不建:

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

并发执行、Prompt Lab、测试集回归、成本归集、充值、license、完整知识库、通知和申诉都属于二期或三期；一期字段不得为了这些能力提前创建生产表。

## 1. 通用数据库规则

### 1.1 数据库与命名

| 项 | 规则 |
|---|---|
| 数据库 | PostgreSQL |
| Migration | Alembic |
| 表名 | 小写复数 snake_case，例如 `skill_calls` |
| 字段名 | 小写 snake_case，例如 `skill_version_id` |
| 主键 | `uuid`，服务端生成 |
| 时间 | 全部使用 `timestamptz` |
| 金额 / 分数 / 权重 | 使用 `numeric(12,4)` 或按业务精度收敛 |
| JSON | 使用 `jsonb`，只在稳定高频查询字段上建 GIN 索引 |
| 枚举 | 一期优先用 `varchar + CHECK`，避免 PostgreSQL enum 后续迁移成本 |

### 1.2 通用字段

除 `audit_logs` 等追加型日志表、纯关联表另有说明外，所有业务主表默认包含以下字段:

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | uuid | pk | 主键 |
| created_at | timestamptz | not null | 创建时间 |
| created_by | uuid | null | 创建人，系统任务可为空 |
| updated_at | timestamptz | not null | 更新时间 |
| updated_by | uuid | null | 更新人 |
| deleted_at | timestamptz | null | 软删除时间 |
| deleted_by | uuid | null | 软删除人 |
| row_version | int | not null default 1 | 乐观锁 |
| audit_request_id | varchar(64) | null | 关联一次请求或批处理 |

规则:

- 查询默认加 `deleted_at is null`。
- 业务主表不物理删除，删除动作转为软删除或状态归档。
- 更新时必须校验 `row_version`，冲突返回 `STATE_CONFLICT`。
- 审计日志、历史计分、历史调用证据不允许普通管理员物理删除。

### 1.3 枚举管理

| 类型 | 落地方式 | 示例 |
|---|---|---|
| 状态枚举 | `varchar + CHECK` + 代码枚举 | `tasks.status`、`skill_calls.status` |
| 风险等级 | `varchar + CHECK` | `P0 / P1 / P2 / Low` |
| 运营字典 | 一期代码枚举，二期可抽字典表 | `task_type`、`feedback_type` |
| 权限动作 | `permissions.code` + `authorization_grants.action_scope` | `call`、`source_read`、`manage` |

约束:

- 状态枚举变更必须同步开发文档状态机。
- 前端不得自行维护和后端不一致的状态枚举。
- JSONB 中保存枚举时，应同时保存 `code` 和当时的展示名，避免后续改名影响历史解释。

### 1.4 JSONB 管理

JSONB 字段只能用于快照、规则、证据和不稳定结构，不能替代核心关系字段。

必须拆成普通列的字段:

- 用户、部门、Skill、SkillVersion、Task、SkillCall、TaskResult、Review、Score、Usage、Report 的主外键。
- 状态、风险等级、版本号、发生时间、创建人。
- 看板高频筛选字段，例如 `user_id`、`department_id`、`skill_id`、`skill_version_id`、`created_at`、`status`。

允许使用 JSONB 的字段:

- `input_schema`、`output_schema`
- `review_rule`
- `manifest`
- `context_snapshot`
- `authorization_snapshot`
- `input_size_snapshot`
- `execution_snapshot`
- `formula_snapshot`
- `evidence_ref`
- `scope`
- `constraints`

## 2. 一期表清单

| 模块 | 表 | 一期用途 |
|---|---|---|
| 组织账号 | `departments` | 部门树、数据权限范围 |
| 组织账号 | `users` | 账号导入、员工归属、评审人 |
| RBAC | `roles` | 角色 |
| RBAC | `permissions` | 权限点 |
| RBAC | `role_permissions` | 角色权限关联 |
| 授权 | `authorization_grants` | 谁能对哪个资产做什么 |
| 审计 | `audit_logs` | 写操作和敏感操作审计 |
| 密钥 | `encrypted_secrets` | 简单加密 key_version / secret_ref 元数据 |
| Skill | `skills` | Skill 清单 |
| Skill | `skill_versions` | 可调用版本、版本绑定、公式绑定 |
| Skill | `skill_source_packages` | 加密源码包、hash、manifest |
| 计分 | `skill_score_policies` | Skill 计分策略 |
| 计分 | `score_formula_versions` | 公式版本 |
| 任务 | `tasks` | 员工业务任务上下文 |
| 调用 | `skill_calls` | 人调用 Skill 的最小事实单元 |
| 结果 | `task_results` | 产出、采用确认、人工修改耗时 |
| Review | `review_groups` | 多人评审批次 |
| Review | `review_records` | 单个评审人记录 |
| 反馈 | `skill_feedback` | 员工痛点反馈与处理状态 |
| 计分 | `score_records` | 贡献分和公式快照 |
| 计量 | `usage_meter_records` | 调用次数、耗时等基础计量证据 |
| 报表 | `report_exports` | Excel 导出任务 |

## 3. 一期字段清单

以下表格只列业务字段。除特别说明外，默认追加第 1.2 节通用字段。

### 3.1 departments

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| name | varchar(100) | not null | 部门名称 |
| parent_id | uuid | null, fk departments.id | 上级部门 |
| manager_id | uuid | null, fk users.id | 部门主管 |
| status | varchar(20) | not null check active/disabled | 状态 |

约束与索引:

- `unique(parent_id, name) where deleted_at is null`
- `idx_departments_parent(parent_id)`
- `idx_departments_manager(manager_id)`

删除策略:

- 有用户或子部门时不允许删除，只能 `status = disabled` 或归档。

### 3.2 users

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| name | varchar(100) | not null | 姓名 |
| email | varchar(255) | not null | 邮箱 |
| employee_no | varchar(64) | null | 工号 |
| department_id | uuid | not null, fk departments.id | 所属部门 |
| role_ids | uuid[] | not null default '{}' | 角色集合，一期按冻结清单保留数组字段 |
| level | varchar(20) | not null default 'newbie' | newbie / growing / skilled / expert |
| status | varchar(20) | not null check active/disabled | active / disabled |
| imported_batch_id | varchar(64) | null | 账号导入批次 |

约束与索引:

- `unique(lower(email)) where deleted_at is null`
- `unique(employee_no) where employee_no is not null and deleted_at is null`
- `idx_users_department_status(department_id, status)`
- `idx_users_role_ids_gin using gin(role_ids)`

说明:

- 员工离职或停用不删除用户，改为 `disabled`。
- 一期不额外增加 `user_roles` 表，避免扩大冻结清单；角色 ID 的合法性由应用层校验。

### 3.3 roles

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| code | varchar(64) | not null | 角色编码，例如 `employee`、`reviewer`、`skill_admin` |
| name | varchar(100) | not null | 角色名称 |
| description | text | null | 描述 |
| status | varchar(20) | not null check active/disabled | 状态 |

约束与索引:

- `unique(code) where deleted_at is null`
- `idx_roles_status(status)`

### 3.4 permissions

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| code | varchar(100) | not null | 权限编码，例如 `skill.call`、`skill.source_read` |
| resource | varchar(64) | not null | 资源类型 |
| action_scope | varchar(64) | not null | 动作范围 |
| description | text | null | 描述 |
| status | varchar(20) | not null check active/disabled | 状态 |

约束与索引:

- `unique(code) where deleted_at is null`
- `idx_permissions_resource_action(resource, action_scope)`

### 3.5 role_permissions

纯关联表，保留创建和软删除字段，不需要 `row_version`。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| role_id | uuid | not null, fk roles.id | 角色 |
| permission_id | uuid | not null, fk permissions.id | 权限 |
| created_at | timestamptz | not null | 创建时间 |
| created_by | uuid | null | 创建人 |
| deleted_at | timestamptz | null | 软删除时间 |
| deleted_by | uuid | null | 软删除人 |

约束与索引:

- `unique(role_id, permission_id) where deleted_at is null`
- `idx_role_permissions_permission(permission_id)`

### 3.6 authorization_grants

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| subject_type | varchar(32) | not null | user / role / department / service_account |
| subject_id | varchar(64) | not null | 被授权主体 ID |
| asset_type | varchar(32) | not null | skill / workflow / knowledge_pack / tool_permission / prompt / dataset |
| asset_id | varchar(64) | not null | 被授权资产 ID |
| action_scope | text[] | not null | call / read / source_read / source_export / review / manage / export |
| action_scope_hash | varchar(64) | not null | action_scope 排序后的 hash，用于唯一约束 |
| constraints | jsonb | not null default '{}' | 部门、时间、风险等级、IP、额度等约束 |
| effective_from | timestamptz | not null | 生效时间 |
| effective_to | timestamptz | null | 失效时间 |
| status | varchar(20) | not null | pending / active / suspended / expired / revoked |
| approved_by | uuid | null, fk users.id | 审批人 |
| revoke_reason | text | null | 撤销原因 |

约束与索引:

- `unique(subject_type, subject_id, asset_type, asset_id, action_scope_hash, effective_from) where deleted_at is null`
- `idx_authz_subject_asset(subject_type, subject_id, asset_type, asset_id, status)`
- `idx_authz_asset(asset_type, asset_id, status)`

规则:

- `call` 只能运行 Skill，不能读取或导出源码。
- `source_read` 和 `source_export` 必须独立授权，不能由 `manage` 或 `export` 推断。
- 授权决策结果必须写入 `skill_calls.authorization_snapshot`。

### 3.7 audit_logs

追加型日志表，不使用通用软删除字段，不允许更新和删除。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | uuid | pk | 日志 ID |
| actor_id | uuid | null, fk users.id | 操作人，系统动作可为空 |
| action | varchar(100) | not null | 操作动作 |
| target_type | varchar(64) | not null | 目标类型 |
| target_id | varchar(64) | not null | 目标 ID |
| before | jsonb | null | 变更前，必须脱敏 |
| after | jsonb | null | 变更后，必须脱敏 |
| reason | text | null | 操作原因 |
| ip | varchar(64) | null | IP |
| user_agent | text | null | UA |
| audit_request_id | varchar(64) | null | 请求 ID |
| created_at | timestamptz | not null | 发生时间 |

约束与索引:

- `idx_audit_actor_time(actor_id, created_at desc)`
- `idx_audit_target(target_type, target_id, created_at desc)`
- `idx_audit_request(audit_request_id)`

规则:

- `before` / `after` 不得保存明文源码、明文密钥、敏感附件全文。
- 源码包上传、运行时解密、权限变更、计分调整、报表导出必须写审计。

### 3.8 encrypted_secrets

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| secret_type | varchar(40) | not null | api_key / object_key / skill_source_key |
| provider | varchar(40) | not null | deployment_secret / env / local_dev / external_secret |
| encrypted_value_ref | varchar(255) | not null | 部署 Secret、本地 SecretProvider 或后续外部密钥服务引用 |
| masked_value | varchar(255) | null | 页面可展示的脱敏值 |
| key_version | varchar(64) | not null | 密钥版本 |
| owner_type | varchar(64) | not null | skill / skill_source_package / system |
| owner_id | varchar(64) | not null | 所属对象 |
| status | varchar(20) | not null | active / rotated / revoked |
| rotated_at | timestamptz | null | 轮换时间 |

约束与索引:

- `unique(owner_type, owner_id, secret_type, key_version) where deleted_at is null`
- `idx_encrypted_secrets_owner(owner_type, owner_id, status)`

规则:

- 一期只做服务端 AES-GCM 简单包级加密。
- 数据库不保存可解密明文密钥。
- 密钥轮换生成新 `key_version`，不覆盖历史记录。

### 3.9 skills

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| name | varchar(120) | not null | Skill 名称 |
| description | text | null | 描述 |
| owner_id | uuid | not null, fk users.id | 负责人 |
| department_scope | uuid[] | not null default '{}' | 可用部门范围 |
| version | varchar(40) | null | 当前展示版本 |
| risk_level | varchar(10) | not null | P0 / P1 / P2 / Low |
| input_schema | jsonb | not null default '{}' | 输入要求 |
| output_schema | jsonb | not null default '{}' | 输出格式 |
| review_rule | jsonb | not null default '{}' | Review 规则 |
| weight | numeric(8,4) | not null default 1.0 | Skill 权重 |
| status | varchar(20) | not null | draft / testing / published / paused / archived |

约束与索引:

- `unique(name) where deleted_at is null`
- `idx_skills_owner(owner_id)`
- `idx_skills_status_risk(status, risk_level)`
- `idx_skills_department_scope_gin using gin(department_scope)`

### 3.10 skill_versions

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| skill_id | uuid | not null, fk skills.id | 所属 Skill |
| version_code | varchar(40) | not null | 版本号 |
| source_package_id | uuid | not null, fk skill_source_packages.id | 绑定源码包 |
| model_profile_id | uuid | null | 模型配置，先保留引用 |
| prompt_version_id | uuid | null, no fk in phase 1 | 二期 PromptVersion 引用，一期不得使用 |
| dataset_baseline_id | uuid | null, no fk in phase 1 | 二期 Dataset 引用，一期不得使用 |
| input_schema | jsonb | not null default '{}' | 输入要求快照 |
| output_schema | jsonb | not null default '{}' | 输出要求快照 |
| review_rule_snapshot | jsonb | not null default '{}' | Review 规则快照 |
| score_policy_id | uuid | null, fk skill_score_policies.id | 计分策略 |
| execution_mode | varchar(20) | not null default 'single' | 一期只能为 single |
| release_status | varchar(20) | not null default 'released' | 一期只允许 released / archived |
| effective_from | timestamptz | not null | 生效时间 |
| effective_to | timestamptz | null | 失效时间 |

约束与索引:

- `unique(skill_id, version_code) where deleted_at is null`
- `idx_skill_versions_skill_status(skill_id, release_status, effective_from desc)`
- `idx_skill_versions_package(source_package_id)`
- CHECK: `execution_mode = 'single'`
- CHECK: `release_status in ('released', 'archived')`

规则:

- 一期不创建候选版本、多人发布门禁、回滚状态。
- 每个生产调用必须绑定明确的 `skill_version_id` 和 `source_package_id`。
- `source_package_id` 一旦被历史调用引用，不允许覆盖源码包，只能创建新版本。

### 3.11 skill_source_packages

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| skill_id | uuid | not null, fk skills.id | 所属 Skill |
| version_code | varchar(40) | not null | 源码包版本 |
| package_type | varchar(40) | not null | prompt_bundle / workflow_bundle / tool_adapter / mixed |
| encrypted_package_ref | varchar(500) | not null | 加密包对象存储引用 |
| package_hash | varchar(128) | not null | 加密前内容摘要 |
| key_ref_id | uuid | not null, fk encrypted_secrets.id | key_version 引用 |
| manifest | jsonb | not null default '{}' | 入口、依赖、运行时、允许工具 |
| visibility | varchar(40) | not null | private / org_restricted / shared_runtime_only |
| status | varchar(20) | not null | draft / active / revoked / archived |

约束与索引:

- `unique(skill_id, version_code) where deleted_at is null`
- `unique(package_hash) where deleted_at is null`
- `idx_skill_source_packages_skill(skill_id, status, created_at desc)`
- `idx_skill_source_packages_key(key_ref_id)`

规则:

- 包内容不可覆盖；源码变更必须生成新 `version_code` 和新 `package_hash`。
- `revoked` 后不允许新调用，历史调用继续通过快照解释。
- API、日志、报表不得返回源码明文或可下载密文引用给普通调用方。

### 3.12 skill_score_policies

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| skill_id | uuid | not null, fk skills.id | Skill |
| skill_version_id | uuid | null, fk skill_versions.id | 可绑定版本，也可作为 Skill 默认策略 |
| task_type | varchar(80) | not null | 适用任务类型 |
| baseline_minutes | int | not null | 基准人工工时 |
| complexity_coef_map | jsonb | not null default '{}' | 复杂度系数 |
| input_size_rule | jsonb | not null default '{}' | 输入规模系数 |
| adoption_factor_map | jsonb | not null default '{}' | 采纳状态系数 |
| quality_factor_rule | jsonb | not null default '{}' | Review 分数到质量系数 |
| business_value_factor | numeric(8,4) | not null default 1.0 | 业务价值系数 |
| skill_weight | numeric(8,4) | not null default 1.0 | 审批后 Skill 权重 |
| daily_cap_rule | jsonb | null | 日封顶规则 |
| anti_gaming_rule | jsonb | not null default '{}' | 去重、拆分、异常规则 |
| status | varchar(20) | not null | draft / active / archived |
| effective_from | timestamptz | not null | 生效时间 |
| effective_to | timestamptz | null | 失效时间 |
| approved_by | uuid | null, fk users.id | 审批人 |

约束与索引:

- `unique(skill_id, skill_version_id, task_type, effective_from) where deleted_at is null`
- `idx_score_policies_skill(skill_id, status, effective_from desc)`

### 3.13 score_formula_versions

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| version_code | varchar(64) | not null | 公式版本，例如 `score_v1_2026_05` |
| formula | jsonb | not null | 公式结构和系数定义 |
| rounding_rule | jsonb | not null default '{}' | 舍入规则 |
| status | varchar(20) | not null | draft / active / archived |
| effective_from | timestamptz | not null | 生效时间 |
| effective_to | timestamptz | null | 失效时间 |
| approved_by | uuid | null, fk users.id | 审批人 |

约束与索引:

- `unique(version_code) where deleted_at is null`
- `idx_formula_versions_status(status, effective_from desc)`

### 3.14 tasks

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| creator_id | uuid | not null, fk users.id | 创建人 |
| department_id | uuid | not null, fk departments.id | 所属部门 |
| title | varchar(200) | not null | 任务标题 |
| task_type | varchar(80) | not null | 任务类型 |
| business_scenario | varchar(120) | null | 业务场景 |
| business_object | varchar(200) | null | 客户、项目、合同、会议、数据表等 |
| expected_output | text | null | 期望产出 |
| business_value | varchar(20) | null | 业务价值等级 |
| complexity | varchar(20) | not null default 'standard' | simple / standard / complex / high |
| skill_id | uuid | null, fk skills.id | 选择的 Skill |
| skill_version_id | uuid | null, fk skill_versions.id | 调用版本 |
| status | varchar(20) | not null | draft / submitted / running / failed / pending_review / approved / returned / blocked / archived |
| risk_level | varchar(10) | not null default 'Low' | P0 / P1 / P2 / Low |
| input_summary | text | null | 输入摘要 |
| input_object_key | varchar(500) | null | 输入附件对象存储路径 |

约束与索引:

- 不做业务唯一，允许同名任务。
- `idx_tasks_creator_status(creator_id, status) where deleted_at is null`
- `idx_tasks_department_created(department_id, created_at desc) where deleted_at is null`
- `idx_tasks_skill(skill_id, skill_version_id, created_at desc) where deleted_at is null`

### 3.15 skill_calls

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| task_id | uuid | not null, fk tasks.id | 所属任务 |
| user_id | uuid | not null, fk users.id | 调用人 |
| department_id | uuid | not null, fk departments.id | 调用人所属组织 |
| skill_id | uuid | not null, fk skills.id | Skill |
| skill_version_id | uuid | not null, fk skill_versions.id | SkillVersion |
| source_package_id | uuid | not null, fk skill_source_packages.id | 调用时源码包 |
| source_package_version | varchar(40) | not null | 源码包版本快照 |
| source_package_hash | varchar(128) | not null | 源码包 hash 快照 |
| prompt_version_id | uuid | null, no fk in phase 1 | 二期 PromptVersion 引用，一期不得使用 |
| execution_mode | varchar(20) | not null default 'single' | 一期固定 single |
| context_snapshot | jsonb | not null default '{}' | 调用前业务上下文快照 |
| authorization_snapshot | jsonb | not null default '{}' | 授权决策快照 |
| input_size_snapshot | jsonb | not null default '{}' | 字数、页数、记录数、附件数等 |
| execution_snapshot | jsonb | not null default '{}' | 模型、耗时、错误、重试等 |
| status | varchar(20) | not null | created / running / succeeded / failed / confirmed / scored |

约束与索引:

- 不做业务唯一，同一任务允许多次调用。
- CHECK: `execution_mode = 'single'`
- `idx_skill_calls_skill_period(skill_id, skill_version_id, created_at desc) where deleted_at is null`
- `idx_skill_calls_user_period(user_id, created_at desc, status) where deleted_at is null`
- `idx_skill_calls_task(task_id, created_at desc) where deleted_at is null`
- `idx_skill_calls_package(source_package_id, source_package_version) where deleted_at is null`

规则:

- `SkillCall` 是价值计算的最小事实单元。
- 一期不允许 `execution_plan_id` 字段，不创建 ExecutionPlan / SkillSubCall。
- 运行时解密成功或失败都要写入审计和 `execution_snapshot` 摘要。

### 3.16 task_results

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| task_id | uuid | not null, fk tasks.id | 任务 |
| skill_call_id | uuid | not null, fk skill_calls.id | Skill 调用 |
| skill_id | uuid | not null, fk skills.id | Skill |
| skill_version_id | uuid | not null, fk skill_versions.id | SkillVersion |
| skill_version | varchar(40) | not null | 展示版本 |
| model_name | varchar(100) | null | 模型名称 |
| prompt_version_id | uuid | null, no fk in phase 1 | 二期 PromptVersion 引用，一期不得使用 |
| prompt_version | varchar(40) | null | Prompt 版本展示值 |
| output_summary | text | not null | 输出摘要 |
| output_object_key | varchar(500) | null | 输出附件 |
| confidence | numeric(6,4) | null | 置信度 |
| estimated_saved_minutes | int | null | 预计节省工时 |
| execution_ms | int | not null | 执行耗时 |
| adoption_status | varchar(30) | null | direct_use / minor_edit / major_edit / reference_only / not_used |
| human_edit_minutes | int | null | 员工确认的人工修改耗时 |
| rework_required | bool | null | 是否返工 |
| rework_minutes | int | null | 返工耗时 |
| business_submitted | bool | null | 是否进入业务流程 |
| status | varchar(20) | not null | candidate / saved / submitted_review / approved / rejected |

约束与索引:

- `unique(skill_call_id) where deleted_at is null`
- `idx_task_results_task(task_id, created_at desc) where deleted_at is null`
- `idx_task_results_status(status, created_at desc) where deleted_at is null`

规则:

- 保存、导出、提交 Review 或进入贡献计算前必须确认 `adoption_status` 和 `human_edit_minutes`。
- `not_used` 默认不计贡献。

### 3.17 review_groups

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| review_type | varchar(40) | not null | 一期只允许 task_output |
| target_type | varchar(40) | not null | task_result |
| target_id | uuid | not null | 目标结果 ID，应用层校验到 task_results.id |
| task_id | uuid | not null, fk tasks.id | 任务 |
| result_id | uuid | not null, fk task_results.id | 结果 |
| pass_rule | jsonb | not null default '{}' | 例如 2/3 通过 |
| required_reviewer_count | int | not null default 1 | 应评人数 |
| approved_count | int | not null default 0 | 已通过人数 |
| returned_count | int | not null default 0 | 退回人数 |
| blocked_count | int | not null default 0 | 拦截人数 |
| status | varchar(20) | not null | pending / approved / returned / blocked / need_recheck |
| due_at | timestamptz | null | SLA 截止时间 |

约束与索引:

- `idx_review_groups_queue(status, due_at, created_at desc) where deleted_at is null`
- `idx_review_groups_result(result_id) where deleted_at is null`

规则:

- Prompt 候选评审和 SkillVersion 发布评审属于二期，不进入一期 `review_type`。

### 3.18 review_records

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| review_group_id | uuid | not null, fk review_groups.id | 评审批次 |
| task_id | uuid | not null, fk tasks.id | 任务 |
| result_id | uuid | not null, fk task_results.id | 任务结果 |
| review_type | varchar(40) | not null | 一期只允许 task_output |
| reviewer_id | uuid | not null, fk users.id | 评审人 |
| score_quality | int | null | 质量评分 |
| score_risk | int | null | 风险评分 |
| score_reuse | int | null | 复用价值 |
| action | varchar(30) | not null | approve / return / block / request_changes |
| comment | text | not null | 评审意见 |
| reason_code | varchar(80) | null | 退回或拦截原因 |
| passed | bool | not null | 是否通过 |

约束与索引:

- `unique(review_group_id, reviewer_id) where deleted_at is null`
- `idx_reviews_queue(review_type, action, created_at desc) where deleted_at is null`
- `idx_reviews_reviewer(reviewer_id, created_at desc) where deleted_at is null`

### 3.19 skill_feedback

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| skill_id | uuid | not null, fk skills.id | 关联 Skill |
| skill_version | varchar(40) | not null | 反馈时使用的版本 |
| task_id | uuid | null, fk tasks.id | 关联任务 |
| result_id | uuid | null, fk task_results.id | 关联结果 |
| reporter_id | uuid | not null, fk users.id | 反馈员工 |
| department_id | uuid | not null, fk departments.id | 反馈员工部门 |
| feedback_type | varchar(40) | not null | inaccurate / missing_field / wrong_format / unusable / no_time_saved / weak_risk_warning / complex_params / scenario_mismatch / new_scenario / other |
| severity | varchar(20) | not null | low / medium / high |
| description | text | not null | 反馈说明 |
| evidence_object_key | varchar(500) | null | 截图或附件 |
| status | varchar(20) | not null | submitted / triaged / planned / released / rejected |
| owner_id | uuid | null, fk users.id | 处理人 |
| resolution_note | text | null | 处理结果 |

约束与索引:

- `idx_feedback_skill_status(skill_id, status, created_at desc) where deleted_at is null`
- `idx_feedback_reporter(reporter_id, created_at desc) where deleted_at is null`
- 防重复反馈由应用层按 `reporter_id + result_id + feedback_type + 当天` 控制。

规则:

- 员工只能提交反馈和查看自己反馈处理状态。
- 一期不建 `converted_dataset_case_id`、`optimization_task_id` 字段；反馈转测试集和优化任务属于二期 migration。

### 3.20 score_records

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| user_id | uuid | not null, fk users.id | 员工 |
| department_id | uuid | not null, fk departments.id | 员工部门，便于组织看板 |
| task_id | uuid | not null, fk tasks.id | 来源任务 |
| skill_call_id | uuid | not null, fk skill_calls.id | 来源调用 |
| result_id | uuid | not null, fk task_results.id | 来源结果 |
| skill_id | uuid | not null, fk skills.id | Skill |
| skill_version_id | uuid | not null, fk skill_versions.id | SkillVersion |
| prompt_version_id | uuid | null, no fk in phase 1 | 二期 PromptVersion 引用，一期不得使用 |
| review_group_id | uuid | null, fk review_groups.id | 来源 Review 批次 |
| formula_version_id | uuid | not null, fk score_formula_versions.id | 公式版本 |
| formula_version_code | varchar(64) | not null | 公式版本编码快照 |
| baseline_minutes | int | not null | 基准人工工时 |
| after_skill_minutes | int | not null | 使用后人工工时 |
| raw_saved_minutes | int | not null | 原始节省工时 |
| confirmed_saved_minutes | int | not null | 确认节省工时 |
| contribution_score | numeric(12,4) | not null | 单次贡献分 |
| formula_snapshot | jsonb | not null | 公式和权重快照 |
| explanation | text | not null | 解释 |
| status | varchar(20) | not null | draft / pending / confirmed / rejected / adjusted / frozen |

约束与索引:

- `unique(skill_call_id, result_id, formula_version_code) where deleted_at is null`
- `idx_scores_user_period(user_id, created_at desc, status) where deleted_at is null`
- `idx_scores_department_period(department_id, created_at desc, status) where deleted_at is null`
- `idx_scores_skill_period(skill_id, skill_version_id, created_at desc, status) where deleted_at is null`
- `idx_score_formula_snapshot_gin using gin(formula_snapshot)`

规则:

- 历史解释读取 `formula_snapshot`，不得随后续权重变化回改历史分数。
- 进入个人 / Skill / 组织看板的记录必须是 `confirmed` 或 `frozen`。

### 3.21 usage_meter_records

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| skill_call_id | uuid | null, fk skill_calls.id | 关联 SkillCall |
| user_id | uuid | not null, fk users.id | 使用人 |
| department_id | uuid | not null, fk departments.id | 使用人部门 |
| cost_center_id | uuid | null | 成本中心，二期使用 |
| asset_type | varchar(40) | not null | skill / model / storage / review |
| asset_id | varchar(64) | not null | 资产 ID |
| asset_version | varchar(64) | null | 资产版本 |
| metric_type | varchar(40) | not null | call_count / execution_ms / input_tokens / output_tokens / storage_mb_day / review_minutes |
| quantity | numeric(14,4) | not null | 数量 |
| unit | varchar(30) | not null | 次、毫秒、token、MB-day、分钟 |
| occurred_at | timestamptz | not null | 发生时间 |
| evidence_ref | jsonb | not null default '{}' | SkillCall、TaskResult、ReviewRecord、日志引用 |
| status | varchar(20) | not null | pending / confirmed / voided |

约束与索引:

- `unique(skill_call_id, asset_type, asset_id, asset_version, metric_type) where skill_call_id is not null and deleted_at is null`
- `idx_usage_meter_period(asset_type, asset_id, occurred_at desc, status) where deleted_at is null`
- `idx_usage_meter_user_period(user_id, occurred_at desc, status) where deleted_at is null`
- `idx_usage_meter_department_period(department_id, occurred_at desc, status) where deleted_at is null`

规则:

- 一期只作为基础计量证据，不进入成本归集、充值或 license 扣减。

### 3.22 report_exports

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| report_type | varchar(40) | not null | personal_score / skill_score / org_score / review_summary |
| requested_by | uuid | not null, fk users.id | 导出人 |
| scope | jsonb | not null default '{}' | 时间、部门、Skill、用户等筛选范围 |
| format | varchar(10) | not null default 'xlsx' | 一期只允许 xlsx |
| status | varchar(20) | not null | queued / running / succeeded / failed / expired |
| file_object_key | varchar(500) | null | 导出文件对象存储引用 |
| error_code | varchar(80) | null | 失败码 |
| error_message | text | null | 失败说明 |
| audit_log_id | uuid | null, fk audit_logs.id | 导出审计 |
| expires_at | timestamptz | null | 下载过期时间 |

约束与索引:

- 不做业务唯一，允许同一用户重复导出。
- `idx_report_exports_user_status(requested_by, status, created_at desc) where deleted_at is null`
- `idx_report_exports_type(report_type, created_at desc) where deleted_at is null`

规则:

- 导出内容必须按操作者数据权限过滤。
- 导出文件不得包含 Skill 源码、明文密钥、成本单价或未授权敏感输入全文。

### 3.23 二期 Skill 字段治理与看板字段权限分配

这组规则用于处理“看板上到底给谁看哪些 Skill 字段”。完整 Skill 字段治理放到二期实现，不进入一期开发冻结清单。一期只返回 Skill 名称、描述、状态、版本、风险等级、可调用状态和必要的输入 / 输出摘要；二期再补充业务域、标签、触发描述、置信度、SOP、数据映射、报错对策等完整字段和字段级视图。

二期建议新增字段:

| 表 | 字段 | 类型 | 说明 |
|---|---|---|---|
| skills | business_domain | varchar(80) | 所属业务域，用于业务归因、看板筛选和报表聚合 |
| skills | tags | text[] | 技能标签，用于检索、分类和运营分析 |
| skills | trigger_description | text | Agent 触发描述，说明什么场景适合调用 |
| skill_versions | confidence_threshold | numeric(6,4) | 推荐置信度阈值 |
| skill_versions | confidence_output_required | bool | 是否要求输出置信度 |
| skill_versions | data_mapping_summary | jsonb | 数据映射摘要，不存敏感明文 |
| skill_versions | sop_summary | jsonb | 可展示 SOP 摘要 |
| skill_versions | expert_intervention_rules | jsonb | 专家干预红线 |
| skill_versions | fault_policy_summary | jsonb | 容错逻辑摘要 |

二期建议索引:

```sql
create index idx_skills_business_domain on skills (business_domain, status) where deleted_at is null;
create index idx_skills_tags_gin on skills using gin (tags) where deleted_at is null;
```

一期不新增字段级权限表；二期仍优先通过 `roles`、`permissions`、`role_permissions`、`authorization_grants` 和 API 响应脱敏层实现字段级可见性，只有当字段策略需要运营配置时再新增字段策略表。

可见性说明:

| 标记 | 含义 |
|---|---|
| 明细 | 可看完整字段内容 |
| 摘要 | 只看脱敏摘要、展示名、使用说明或风险提示 |
| 聚合 | 只看统计结果，不看单条明细 |
| 不可见 | API 不返回该字段 |
| 二期 | 一期不实现；二期按同样权限规则启用 |

字段组与权限动作:

| 字段组 | 说明 | 需要的权限动作 |
|---|---|---|
| `skill_public` | Skill 识别和检索字段 | `read` 或 `call` |
| `skill_usage_contract` | 员工调用所需的输入、输出、触发条件 | `call` |
| `skill_review_policy` | Review、置信度、专家干预红线 | `review` 或 `manage`；员工只看触发提示 |
| `skill_management_config` | 管理配置、SOP、容错、数据映射 | `manage` |
| `skill_source_protected` | 源码、底层 API、代码段、敏感环境依赖 | `source_read`；导出必须 `source_export` |
| `skill_optimization_phase2` | 测试样本、预期输出、RAG、优化数据 | 二期 `prompt_optimizer` / `skill_admin` 授权 |

角色默认字段视图:

| 角色 | 默认可见范围 |
|---|---|
| 员工 `employee` | 只看可调用 Skill 的 `skill_public`、`skill_usage_contract` 摘要、自己调用后的结果和反馈状态 |
| Review 评审人 `reviewer` | 员工可见内容 + 授权 Review 队列内的 `skill_review_policy`、结果证据和评分要求 |
| 部门主管 `manager` | 本部门聚合看板、Skill 使用表现、反馈聚合；不看源码、底层 API、代码段、未授权敏感输入全文 |
| HR `hr` | 跨部门汇总趋势和分布；默认不看个人敏感任务明细、源码和实现配置 |
| Skill 管理员 `skill_admin` | 授权范围内的 Skill 配置、反馈明细、Review 规则、版本绑定、运行摘要；源码明细仍需 `source_read` |
| 系统管理员 `system_admin` | 账号、角色、权限、审计、Secret 引用和系统配置；默认不因系统管理员身份自动获得源码明文 |
| Prompt / Skill 优化人员 `prompt_optimizer` | 二期可看授权优化任务、测试集、候选版本和 Compare；不默认看生产源码 |

看板字段分配:

| 用户提出字段 | 字段组 | 建议存储 / 来源 | 员工 | 评审人 | 主管 / HR | Skill 管理员 | 系统管理员 | 说明 |
|---|---|---|---|---|---|---|---|---|
| 技能 | `skill_public` | `skills.id` + 展示对象 | 明细 | 明细 | 聚合 / 明细按范围 | 明细 | 摘要 | 作为卡片对象，不是单独业务字段 |
| 技能名称 | `skill_public` | `skills.name` | 明细 | 明细 | 明细 | 明细 | 明细 | 必须可用于检索和归因 |
| agent说明书 | `skill_usage_contract` / `skill_management_config` | `skills.description` + `skill_source_packages.manifest` 摘要 | 摘要 | 摘要 | 摘要 | 明细 | 摘要 | 员工看使用说明，完整说明书可能包含内部策略 |
| 所属业务域 | `skill_public` | `skills.business_domain` | 明细 | 明细 | 明细 | 明细 | 明细 | 用于业务归因、看板筛选和报表聚合 |
| 技能标签 | `skill_public` | `skills.tags` | 明细 | 明细 | 明细 | 明细 | 明细 | 用于检索、分类和运营分析 |
| 技能状态 | `skill_public` | `skills.status` | 明细 | 明细 | 明细 | 明细 | 明细 | 员工只看可用 / 不可用原因，不看内部审批细节 |
| 版本号 | `skill_public` | `skills.version`、`skill_versions.version_code` | 明细 | 明细 | 明细 | 明细 | 明细 | 价值计算必须绑定版本 |
| 环境依赖 | `skill_source_protected` | `skill_source_packages.manifest.runtime/dependencies` | 不可见 | 不可见 | 不可见 | 摘要 | 摘要 | 完整依赖可能泄露实现，明细需 `source_read` |
| Agent 触发描述 | `skill_usage_contract` | `skills.trigger_description` 或 `input_schema` 摘要 | 明细 | 明细 | 摘要 | 明细 | 摘要 | 用于判断何时调用 Skill |
| 前置依赖技能 | `skill_optimization_phase2` | 二期 DAG / dependency 配置 | 二期 | 二期 | 二期 | 二期 | 二期 | 一期 single SkillCall 不实现依赖编排 |
| 容错逻辑 | `skill_management_config` | `skill_versions.fault_policy` 或 manifest 摘要 | 摘要 | 摘要 | 聚合 | 明细 | 摘要 | 员工只看失败提示和重试状态，不看完整策略 |
| 推荐置信度阈值 | `skill_review_policy` | `skill_versions.review_rule_snapshot.confidence_threshold` | 摘要 | 明细 | 聚合 | 明细 | 摘要 | 可作为低置信度强制 Review 规则 |
| 置信度输出要求 | `skill_usage_contract` / `skill_review_policy` | `output_schema` + Review 规则 | 明细 | 明细 | 摘要 | 明细 | 摘要 | 员工需要知道结果是否会输出置信度 |
| 输入参数协议 | `skill_usage_contract` | `skill_versions.input_schema` | 明细 | 明细 | 摘要 | 明细 | 摘要 | 员工只看可填写字段和校验提示 |
| 输出结果协议 | `skill_usage_contract` | `skill_versions.output_schema` | 明细 | 明细 | 摘要 | 明细 | 摘要 | 员工和评审人都需要理解输出结构 |
| 数据映射关系 | `skill_management_config` | `skill_source_packages.manifest.data_mapping` 或配置摘要 | 摘要 | 摘要 | 聚合 | 明细 | 摘要 | 涉及业务系统字段时需脱敏 |
| SOP 规则细节 | `skill_management_config` / `skill_source_protected` | `review_rule`、manifest、源码包 | 摘要 | 摘要 | 聚合 | 明细 | 摘要 | 员工看使用 SOP，完整规则细节仅管理角色 |
| 专家干预红线 | `skill_review_policy` | `review_rule` / 风险规则 | 摘要 | 明细 | 摘要 | 明细 | 摘要 | 员工需要知道哪些情况必须人工确认 |
| 参考知识库 (RAG) | `skill_optimization_phase2` | 三期 Knowledge / RAG 配置 | 二期 / 摘要 | 二期 / 摘要 | 聚合 | 二期明细 | 摘要 | 一期不做完整知识库；只允许展示来源摘要 |
| 测试输入样本 | `skill_optimization_phase2` | 二期 DatasetCase | 二期公开样例 | 二期明细 | 聚合 | 二期明细 | 不可见 | 一期不进入测试集回归 |
| 预期输出结果 | `skill_optimization_phase2` | 二期 DatasetCase.expected_output | 二期公开样例 | 二期明细 | 聚合 | 二期明细 | 不可见 | 一期不进入测试集回归 |
| 常见报错及对策 | `skill_usage_contract` / `skill_management_config` | manifest.errors 或运维手册 | 摘要 | 摘要 | 聚合 | 明细 | 摘要 | 员工看可操作提示，管理员看完整处置 |
| 实现方式 | `skill_management_config` | `skill_source_packages.package_type` | 不可见 | 不可见 | 聚合 | 明细 | 摘要 | 可显示为 prompt_bundle / workflow_bundle 等，不暴露源码 |
| 底层 API 链接 | `skill_source_protected` | `skill_source_packages.manifest.api_refs` / Secret 引用 | 不可见 | 不可见 | 不可见 | 摘要 | 摘要 | 明细需 `source_read`，导出需 `source_export` 和审计 |
| LangChain 代码段 | `skill_source_protected` | 加密源码包 | 不可见 | 不可见 | 不可见 | 不可见，除非 `source_read` | 不可见，除非 `source_read` | 属于源码保护范围，不进普通看板 |

二期字段级 API 规则:

- 列表接口默认只返回 `skill_public` 和调用者有权看的 `skill_usage_contract` 摘要。
- 详情接口根据 `AuthorizationGrant.action_scope` 做字段裁剪，不允许前端自己隐藏敏感字段。
- 员工、评审人、主管、HR 的 API 响应不得包含 `encrypted_package_ref`、`encrypted_value_ref`、底层 API 明细、源码片段、完整环境依赖和完整 SOP 私有规则。
- `skill_admin` 的 `manage` 权限不等于 `source_read`；能管理 Skill 不代表能看源码。
- `system_admin` 能配置账号、角色和授权，但默认不自动获得源码明文。
- 所有 `source_read`、`source_export` 命中的响应必须写 `audit_logs`。
- Excel 报表只导出当前角色可见字段；不允许因为导出绕过字段级权限。

## 4. 一期主外键关系

| 表 | 主键 | 一期外键 |
|---|---|---|
| departments | id | parent_id -> departments.id, manager_id -> users.id |
| users | id | department_id -> departments.id |
| roles | id | 无 |
| permissions | id | 无 |
| role_permissions | role_id + permission_id | role_id -> roles.id, permission_id -> permissions.id |
| authorization_grants | id | approved_by -> users.id |
| audit_logs | id | actor_id -> users.id |
| encrypted_secrets | id | owner_type + owner_id 由应用层校验 |
| skills | id | owner_id -> users.id |
| skill_versions | id | skill_id -> skills.id, source_package_id -> skill_source_packages.id, score_policy_id -> skill_score_policies.id |
| skill_source_packages | id | skill_id -> skills.id, key_ref_id -> encrypted_secrets.id |
| skill_score_policies | id | skill_id -> skills.id, skill_version_id -> skill_versions.id, approved_by -> users.id |
| score_formula_versions | id | approved_by -> users.id |
| tasks | id | creator_id -> users.id, department_id -> departments.id, skill_id -> skills.id, skill_version_id -> skill_versions.id |
| skill_calls | id | task_id -> tasks.id, user_id -> users.id, department_id -> departments.id, skill_id -> skills.id, skill_version_id -> skill_versions.id, source_package_id -> skill_source_packages.id |
| task_results | id | task_id -> tasks.id, skill_call_id -> skill_calls.id, skill_id -> skills.id, skill_version_id -> skill_versions.id |
| review_groups | id | task_id -> tasks.id, result_id -> task_results.id |
| review_records | id | review_group_id -> review_groups.id, task_id -> tasks.id, result_id -> task_results.id, reviewer_id -> users.id |
| skill_feedback | id | skill_id -> skills.id, task_id -> tasks.id, result_id -> task_results.id, reporter_id -> users.id, department_id -> departments.id, owner_id -> users.id |
| score_records | id | user_id -> users.id, department_id -> departments.id, task_id -> tasks.id, skill_call_id -> skill_calls.id, result_id -> task_results.id, skill_id -> skills.id, skill_version_id -> skill_versions.id, review_group_id -> review_groups.id, formula_version_id -> score_formula_versions.id |
| usage_meter_records | id | skill_call_id -> skill_calls.id, user_id -> users.id, department_id -> departments.id |
| report_exports | id | requested_by -> users.id, audit_log_id -> audit_logs.id |

删除策略:

- 主业务对象默认 `on delete restrict`。
- 可选管理人字段如 `manager_id`、`owner_id` 在用户禁用时不删除；必要时由业务转移负责人。
- 审计、调用、结果、计分、计量记录不做物理删除。
- 指向二期表的字段一期允许为空且不创建外键。

## 5. 一期状态字段

| 表 | 状态字段 | 一期允许值 |
|---|---|---|
| departments | status | active / disabled |
| users | status | active / disabled |
| roles | status | active / disabled |
| permissions | status | active / disabled |
| authorization_grants | status | pending / active / suspended / expired / revoked |
| encrypted_secrets | status | active / rotated / revoked |
| skills | status | draft / testing / published / paused / archived |
| skill_versions | release_status | released / archived |
| skill_source_packages | status | draft / active / revoked / archived |
| skill_score_policies | status | draft / active / archived |
| score_formula_versions | status | draft / active / archived |
| tasks | status | draft / submitted / running / failed / pending_review / approved / returned / blocked / archived |
| skill_calls | status | created / running / succeeded / failed / confirmed / scored |
| task_results | status | candidate / saved / submitted_review / approved / rejected |
| review_groups | status | pending / approved / returned / blocked / need_recheck |
| skill_feedback | status | submitted / triaged / planned / released / rejected |
| score_records | status | draft / pending / confirmed / rejected / adjusted / frozen |
| usage_meter_records | status | pending / confirmed / voided |
| report_exports | status | queued / running / succeeded / failed / expired |

## 6. JSONB 结构示例

### 6.1 skill_source_packages.manifest

```json
{
  "entrypoint": "main.py",
  "runtime": "python3.11",
  "input_schema_path": "input_schema.json",
  "output_schema_path": "output_schema.json",
  "allowed_tools": ["spreadsheet_parser"],
  "source_visibility": "runtime_only",
  "package_hash": "sha256:..."
}
```

### 6.2 skill_calls.authorization_snapshot

```json
{
  "decision": "allow",
  "matched_grants": ["authz_001"],
  "subject": {"type": "user", "id": "usr_001"},
  "asset": {"type": "skill", "id": "sk_001", "version": "v2.3"},
  "actions": ["call"],
  "constraints": {
    "department_scope": ["finance"],
    "risk_allowed": ["P2", "Low"]
  },
  "decided_at": "2026-05-08T10:00:58+08:00"
}
```

### 6.3 skill_calls.context_snapshot

```json
{
  "task_type": "business_analysis_report",
  "business_scenario": "finance_monthly_review",
  "business_object": "2026-04 月经营数据",
  "expected_output": "报告正文 + 风险点 + 建议动作",
  "complexity": "standard",
  "manual_baseline_estimate_minutes": 480
}
```

### 6.4 skill_calls.execution_snapshot

```json
{
  "model_profile_id": "model_answer_001",
  "source_package_id": "spkg_001",
  "source_package_version": "v2.3.1",
  "started_at": "2026-05-08T10:01:00+08:00",
  "finished_at": "2026-05-08T10:01:52+08:00",
  "execution_ms": 52000,
  "retry_count": 0,
  "error_code": null
}
```

### 6.5 score_records.formula_snapshot

```json
{
  "formula_version": "score_v1_2026_05",
  "baseline_minutes": 480,
  "after_skill_minutes": 52,
  "raw_saved_minutes": 428,
  "validity": {
    "adoption_factor": 0.85,
    "quality_factor": 0.9,
    "review_gate_factor": 1.0,
    "dedup_factor": 1.0
  },
  "weights": {
    "hour_point_rate": 10,
    "skill_weight": 1.15,
    "business_value_factor": 1.0,
    "attribution_factor": 1.0
  },
  "result": {
    "confirmed_saved_minutes": 327,
    "contribution_score": 62.7
  }
}
```

### 6.6 report_exports.scope

```json
{
  "date_from": "2026-05-01",
  "date_to": "2026-05-31",
  "department_ids": ["dept_finance"],
  "skill_ids": ["sk_001"],
  "include_person_detail": false
}
```

## 7. 索引汇总

一期 migration 至少创建以下索引:

```sql
create index idx_users_department_status on users (department_id, status) where deleted_at is null;
create index idx_users_role_ids_gin on users using gin (role_ids) where deleted_at is null;
create index idx_skills_status_risk on skills (status, risk_level) where deleted_at is null;
create index idx_skill_versions_skill_status on skill_versions (skill_id, release_status, effective_from desc) where deleted_at is null;
create index idx_skill_source_packages_skill on skill_source_packages (skill_id, status, created_at desc) where deleted_at is null;
create index idx_tasks_creator_status on tasks (creator_id, status) where deleted_at is null;
create index idx_tasks_department_created on tasks (department_id, created_at desc) where deleted_at is null;
create index idx_skill_calls_skill_period on skill_calls (skill_id, skill_version_id, created_at desc) where deleted_at is null;
create index idx_skill_calls_user_period on skill_calls (user_id, created_at desc, status) where deleted_at is null;
create index idx_task_results_task on task_results (task_id, created_at desc) where deleted_at is null;
create index idx_review_groups_queue on review_groups (status, due_at, created_at desc) where deleted_at is null;
create index idx_reviews_reviewer on review_records (reviewer_id, created_at desc) where deleted_at is null;
create index idx_feedback_skill_status on skill_feedback (skill_id, status, created_at desc) where deleted_at is null;
create index idx_scores_user_period on score_records (user_id, created_at desc, status) where deleted_at is null;
create index idx_scores_department_period on score_records (department_id, created_at desc, status) where deleted_at is null;
create index idx_scores_skill_period on score_records (skill_id, skill_version_id, created_at desc, status) where deleted_at is null;
create index idx_authz_subject_asset on authorization_grants (subject_type, subject_id, asset_type, asset_id, status) where deleted_at is null;
create index idx_usage_meter_period on usage_meter_records (asset_type, asset_id, occurred_at desc, status) where deleted_at is null;
create index idx_usage_meter_user_period on usage_meter_records (user_id, occurred_at desc, status) where deleted_at is null;
create index idx_report_exports_user_status on report_exports (requested_by, status, created_at desc) where deleted_at is null;
create index idx_audit_actor_time on audit_logs (actor_id, created_at desc);
create index idx_audit_target on audit_logs (target_type, target_id, created_at desc);
```

JSONB GIN 索引一期只允许:

```sql
create index idx_score_formula_snapshot_gin on score_records using gin (formula_snapshot);
```

`skill_calls.context_snapshot` 暂不建 GIN 索引；真实查询稳定后再加，避免早期写入成本过高。

## 8. 字段变更流程

任何数据库字段变更必须按以下顺序执行:

1. 先修改本文件，说明字段用途、类型、约束、索引和一期 / 二期归属。
2. 再修改开发文档中的接口契约或数据模型摘要。
3. 再生成 Alembic migration。
4. 同步 Pydantic Schema、SQLAlchemy Model、Repository、Service。
5. 补充 API 测试、迁移测试和权限测试。
6. 对涉及计分、授权、加密、审计的字段，必须补充回归测试。

禁止行为:

- 为二期页面提前建生产表。
- 在 JSONB 中隐藏应建普通列的核心外键。
- 用前端字段临时决定数据库字段。
- 为了绕过唯一约束直接物理删除历史数据。
- 保存 Skill 源码明文、密钥明文或未授权敏感输入全文。

## 9. 开发验收口径

数据库部分达到可开发状态，需要满足:

- 一期表只包含第 2 节清单，不创建二期表。
- 每张一期表有主键、必要外键、唯一约束、索引、软删除策略和审计字段策略。
- `skill_calls` 能完整固定用户、组织、Skill、SkillVersion、SourcePackage、时间、授权快照、执行快照。
- `score_records` 能完整固定公式版本、公式快照、权重、基准工时、确认节省工时和贡献分。
- `skill_source_packages` 能保证源码包版本不可覆盖，hash 可追溯，密钥引用不泄露。
- `authorization_grants` 能区分 `call`、`read`、`source_read`、`source_export`、`manage`。
- `report_exports` 导出内容能被审计，且不包含源码、明文密钥和未授权敏感全文。
