# 二期开发文档：Prompt Lab + Skill 字段治理 + 计量结算闭环

- 文档状态: 二期工程可执行草案 / 待一期验收后冻结
- 生成日期: 2026-05-08
- 适用读者: 研发负责人、前端、后端、测试、AI 平台工程师、Skill 管理员、Prompt 优化人员、结算 / 授权管理员
- 阶段目标: 基于一期真实反馈、Review 退回和失败 Case，打通测试集驱动的 Prompt / Skill 优化，同时补齐 Skill 字段治理、成本归集、充值、license 和并发执行基础。

---

## 1. 二期范围

二期新增能力:

- Skill 字段治理: 业务域、标签、触发描述、置信度阈值、置信度输出要求、数据映射摘要、SOP 摘要、专家干预红线、容错摘要。
- 字段级权限: 员工、评审人、主管 / HR、Skill 管理员、系统管理员按账号权限看到不同字段。
- Prompt Lab: Prompt、PromptVersion、Dataset、DatasetCase。
- 反馈 / Review 失败 / 低分 Case 转测试集候选。
- PromptRun、PromptEvaluation、PromptOptimizationJob、PromptCandidateVersion、PromptCompare。
- 多人评审发布门禁。
- SkillVersion 候选、发布、回滚。
- 成本归集、结算账户、充值流水、license 授权基础能力。
- Skill 并发执行基础: ExecutionPlan、SkillSubCall、Reducer、并发状态页和计量归集。
- 二期 `source_export` 审批链路，但默认只开放给强授权场景。

二期仍不做:

- 外部客户 Skill 消费平台。
- SaaS 多租户商业化门户。
- 私有化部署授权中心。
- 智能评分、自动成长建议、组织能力地图。

## 2. 二期进入条件

- 一期至少跑通 1 个试点部门和 3 个高频 Skill。
- 至少积累 30 条有效 SkillCall、10 条 Review 记录、10 条反馈或失败 Case。
- 已确认首批 PromptVersion、测试集口径和发布评审规则。
- 已确认 Skill 字段治理的字段范围和可见性策略。
- 成本中心、结算对象和 license 范围默认按内部成本中心、调用次数 + token 配额推进。
- 二期默认不接真实支付、开票和合同系统，只做内部台账和授权逻辑。

## 3. 二期数据表与字段

新增表:

```text
skill_optimization_tasks
prompts
prompt_versions
datasets
dataset_cases
prompt_runs
prompt_run_case_results
prompt_evaluations
prompt_optimization_jobs
prompt_candidate_versions
prompt_compares
cost_allocation_records
settlement_accounts
recharge_transactions
license_entitlements
execution_plans
skill_sub_calls
```

新增字段治理字段:

| 表 | 字段 | 用途 |
|---|---|---|
| skills | business_domain | 业务归因、筛选、报表聚合 |
| skills | tags | Skill 检索、分类和运营分析 |
| skills | trigger_description | 员工判断何时调用 Skill |
| skill_versions | confidence_threshold | 推荐置信度阈值 |
| skill_versions | confidence_output_required | 是否要求输出置信度 |
| skill_versions | data_mapping_summary | 数据映射摘要 |
| skill_versions | sop_summary | SOP 摘要 |
| skill_versions | expert_intervention_rules | 专家干预红线 |
| skill_versions | fault_policy_summary | 容错逻辑摘要 |
| skill_versions | parallel_policy | 并发策略 |
| skill_versions | reducer_policy | Reducer 策略 |

二期字段级权限规则以 [10_database_field_management.md](/Users/liujun/Desktop/产品经理skill/projects/ai-collaboration-efficiency-platform/10_database_field_management.md) 的 `3.23` 为准。

## 4. 二期页面

| 页面 | 路由 | 能力 |
|---|---|---|
| Skill 字段管理 | `/admin/skills/{id}/fields` | 业务域、标签、触发描述、SOP 摘要、红线、容错摘要 |
| 字段可见性检查 | `/admin/skills/{id}/field-visibility` | 预览不同角色看到的字段 |
| Prompt 管理 | `/prompt-lab/prompts` | Prompt 列表、结构化编辑、版本、Diff、关联 Skill |
| 测试集管理 | `/prompt-lab/datasets` | Dataset、Case、反馈转 Case、JSON 导入、评分规则 |
| 批量运行 | `/prompt-lab/runs` | PromptVersion + Dataset + Model 批量运行 |
| 教师模型评测 | `/prompt-lab/evaluations` | 总分、分项分、失败原因、风险 Case |
| 候选优化 | `/prompt-lab/optimize` | 基于失败 Case 生成候选 Prompt |
| 版本对比 | `/prompt-lab/compare` | 新旧 Prompt 对比、改好 / 改坏 Case、发布建议 |
| 发布评审 | `/prompt-lab/release-reviews` | PromptCandidate / SkillVersion 多人评审 |
| 结算控制台 | `/admin/settlement` | 成本归集、账户、充值、license |
| 并发执行详情 | `/skill-calls/{id}/execution-plan` | ExecutionPlan、SkillSubCall、Reducer、失败和计量摘要 |

## 5. 二期核心 API

| 方法 | 路径 | 用途 |
|---|---|---|
| PATCH | `/api/admin/skills/{id}/field-profile` | 更新 Skill 字段治理信息 |
| GET | `/api/admin/skills/{id}/field-visibility-preview` | 按角色预览字段可见性 |
| POST | `/api/admin/skill-feedback/{id}/convert-dataset-case` | 反馈转测试集候选 Case |
| GET/POST | `/api/prompts` | Prompt 列表和创建 |
| POST | `/api/prompts/{id}/versions` | 创建 PromptVersion |
| GET/POST | `/api/datasets` | 测试集列表和创建 |
| POST | `/api/datasets/{id}/cases` | 新增 DatasetCase |
| POST | `/api/prompt-runs` | 批量运行 |
| POST | `/api/prompt-evaluations` | 教师模型评测 |
| POST | `/api/prompt-optimization-jobs` | 候选优化 |
| POST | `/api/prompt-compares` | 版本对比 |
| POST | `/api/prompt-candidates/{id}/submit-review` | 提交候选评审 |
| POST | `/api/prompt-candidates/{id}/promote` | 晋升 PromptVersion |
| POST | `/api/skills/{id}/versions` | 创建 SkillVersion 候选 |
| POST | `/api/skill-versions/{id}/release` | 发布 SkillVersion |
| POST | `/api/skill-versions/{id}/rollback` | 回滚 SkillVersion |
| GET | `/api/admin/cost-allocations` | 成本归集列表 |
| POST | `/api/admin/settlement/accounts/{id}/recharge` | 充值入账申请 |
| POST | `/api/admin/license-entitlements` | 发放 license |
| GET | `/api/skill-calls/{id}/execution-plan` | 并发执行详情 |

## 6. Sprint 拆解

### Sprint 5：Skill 字段治理、Prompt 与测试集基础

周期: 2 周。

交付物:

- Skill 字段治理 migration 和字段级可见性服务。
- skills / skill_versions 新增二期字段。
- prompts、prompt_versions、datasets、dataset_cases。
- 字段管理页、字段可见性预览、Prompt 管理页、测试集管理页。
- 反馈转 DatasetCase 候选入口。

验收:

- 员工视图不返回底层 API、LangChain 代码段、完整环境依赖、完整 SOP 私有规则。
- `manage` 不等于 `source_read`。
- 员工反馈只能进入 DatasetCase 候选池，转正式必须由管理角色确认。

### Sprint 6：批量运行与教师模型评测

周期: 2 周。

交付物:

- prompt_runs、prompt_run_case_results、prompt_evaluations。
- Worker 队列、失败重试、运行日志。
- Runs 和 Evaluations 页面。

验收:

- PromptRun 必须绑定 PromptVersion、Dataset、ModelProfile。
- Evaluation 必须绑定已成功的 PromptRun。
- Case 级失败原因可下钻。

### Sprint 7：候选优化与 Compare

周期: 2 周。

交付物:

- prompt_optimization_jobs、prompt_candidate_versions、prompt_compares。
- 候选生成、回归运行、Compare 页面。

验收:

- 候选 Prompt 必须基于失败 Case 和 Evaluation 生成。
- Compare 必须展示改好 Case、改坏 Case、风险变化。
- 存在改坏 Case 时不能默认推荐 `promote`。

### Sprint 8：多人发布门禁与 SkillVersion

周期: 2 周。

交付物:

- PromptCandidate 多人评审。
- SkillVersion 候选、发布和回滚。
- 发布评审页、SkillVersion 详情页。

验收:

- Compare 不能绕过多人评审。
- 候选 Prompt 未通过评审不能成为正式 PromptVersion。
- SkillVersion 发布必须绑定 PromptVersion、模型配置、测试集基线和计分策略。

### Sprint 8.5：成本归集、充值与 License

周期: 2 周。

交付物:

- cost_allocation_records、settlement_accounts、recharge_transactions、license_entitlements。
- 授权与计量控制台、结算 / 充值 / license 页面。

验收:

- 没有 UsageMeterRecord 的消耗不能归集成本。
- 余额变更只能通过 RechargeTransaction，不能直接改 SettlementAccount.balance。
- license key 不在响应、日志或导出文件中出现明文。

### Sprint 8.6：Skill 并发执行基础

周期: 1-2 周。

交付物:

- execution_plans、skill_sub_calls。
- SkillVersion.execution_mode、parallel_policy、reducer_policy。
- Worker 并发调度、超时、重试、失败策略和 Reducer。
- 并发执行详情页。

验收:

- 一个多文档 Skill 能拆成多个 SkillSubCall 并发执行，再由 Reducer 汇总成一个 TaskResult。
- 并发分支继承父级授权、源码加密、license、额度、风险和审计上下文。
- 调用方只能看到执行摘要，不能拿到源码、Prompt 源、Workflow DAG 或工具代码。

### Sprint 9：二期收口和回归

周期: 1 周。

交付物:

- Prompt Lab 全链路回归。
- 字段级权限回归。
- 授权、计量、成本、充值、license 回归。
- 并发执行、Reducer 和源码包加密运行时回归。
- 二期验收报告。

验收:

- 反馈 -> DatasetCase -> PromptRun -> Evaluation -> Candidate -> Compare -> Review -> Release 链路跑通。
- 字段级权限不因导出、报表、管理页或接口复用而泄露源码和内部实现。
- 成本归集、充值、license 状态迁移均有审计。

## 7. 二期工程执行契约

### 7.1 数据迁移约束

二期 migration 分四组，必须可独立回滚:

| 组 | 迁移内容 | 约束 |
|---|---|---|
| Skill 字段治理 | `skills.business_domain`、`skills.tags`、`skills.trigger_description`；`skill_versions.confidence_threshold` 等字段 | 默认值必须兼容一期历史数据 |
| Prompt Lab | Prompt、Dataset、Run、Evaluation、Candidate、Compare 表 | 不允许员工反馈直接进入正式 DatasetCase |
| 计量结算 | CostAllocation、SettlementAccount、RechargeTransaction、LicenseEntitlement | 不允许直接更新账户余额 |
| 并发执行 | ExecutionPlan、SkillSubCall，SkillVersion 并发策略字段 | 未配置并发策略的 SkillVersion 仍按 single 执行 |

### 7.2 状态机

| 对象 | 状态 | 关键约束 |
|---|---|---|
| DatasetCase | `candidate -> accepted/rejected/archived` | 候选转正式必须由管理角色确认 |
| PromptRun | `queued -> running -> succeeded/failed/canceled` | 只能绑定固定 PromptVersion、Dataset、ModelProfile |
| PromptEvaluation | `queued -> running -> succeeded/failed` | 只能评测 succeeded 的 PromptRun |
| PromptCandidateVersion | `generated -> regression_running -> compared -> approved/rejected -> promoted` | Compare 和多人评审都通过才可 promoted |
| SkillVersion | `candidate -> reviewing -> released/rejected -> rolled_back/archived` | 发布必须绑定 PromptVersion、测试集基线、模型配置和计分策略 |
| RechargeTransaction | `pending -> approved/rejected/canceled -> posted` | posted 才能改 SettlementAccount.balance |
| LicenseEntitlement | `pending -> active/suspended/expired/revoked` | active 才能授权消费 |
| ExecutionPlan | `planned -> running -> reducing -> succeeded/partial_failed/failed/canceled` | Reducer 失败不得生成 succeeded TaskResult |
| SkillSubCall | `queued -> running -> succeeded/failed/skipped/canceled` | 子调用继承父级授权和审计上下文 |

### 7.3 API 契约补充

`PATCH /api/admin/skills/{id}/field-profile`:

```json
{
  "business_domain": "finance",
  "tags": ["经营分析", "报告生成"],
  "trigger_description": "适合生成月度经营分析报告和风险提示",
  "confidence_threshold": 0.82,
  "confidence_output_required": true,
  "data_mapping_summary": {"input": "经营数据表", "output": "分析报告"},
  "sop_summary": {"steps": ["上传数据", "确认口径", "提交 Review"]},
  "expert_intervention_rules": {"required_when": ["P0", "confidence_below_threshold"]},
  "fault_policy_summary": {"retry": 2, "fallback": "manual_review"}
}
```

权限: `skill_admin` 且具备目标 Skill 的 `manage`。  
响应: 返回更新后的字段 profile 和 `audit_log_id`。

`POST /api/admin/skill-feedback/{id}/convert-dataset-case`:

```json
{
  "dataset_id": "ds_001",
  "case_payload": {"input_ref": "s3://...", "expected_output": "..."},
  "reason": "Review 退回且可复现"
}
```

约束:

- 只能转为 `DatasetCase.candidate`。
- 不能自动进入正式测试集。

`POST /api/prompt-runs`:

```json
{
  "prompt_version_id": "prv_001",
  "dataset_id": "ds_001",
  "model_profile_id": "model_001",
  "idempotency_key": "run_001"
}
```

响应必须返回 `prompt_run_id`、`status`、`total_cases`。

`POST /api/prompt-compares`:

```json
{
  "baseline_prompt_version_id": "prv_base",
  "candidate_prompt_version_id": "pcv_001",
  "dataset_id": "ds_001"
}
```

响应必须返回 `baseline_score`、`candidate_score`、`improved_case_count`、`regressed_case_count`、`recommendation`。

`POST /api/admin/settlement/accounts/{id}/recharge`:

```json
{
  "transaction_type": "recharge",
  "amount": 10000,
  "currency": "CNY",
  "reason": "二期内部额度初始化"
}
```

约束:

- 创建状态为 `pending`。
- 审批后才能 `posted`。
- 不接真实支付、开票和合同系统。

`GET /api/skill-calls/{id}/execution-plan`:

响应只能返回执行摘要、步骤状态、耗时、失败原因和计量摘要；不得返回源码、Prompt 源、Workflow DAG 或工具代码。

### 7.4 权限与字段级可见性

- `read/call`: Skill 名称、业务域、标签、触发描述、输入输出协议摘要。
- `review`: Review 所需证据、置信度、红线、Review 规则摘要。
- `manage`: 字段治理配置、反馈明细、版本绑定、SOP 摘要。
- `source_read`: 源码相关脱敏明细，命中必须写审计。
- `source_export`: 二期强授权能力，必须二次审批和审计。
- 报表、导出、管理页和 API 复用都不能绕过字段级过滤。

### 7.5 异步任务

| 任务 | 队列 | 幂等键 | 失败处理 |
|---|---|---|---|
| PromptRun | `prompt_run` | `prompt_version_id + dataset_id + model_profile_id + idempotency_key` | Case 级失败可重试，Run 失败写失败摘要 |
| PromptEvaluation | `prompt_eval` | `prompt_run_id + teacher_model_profile_id` | 失败不允许生成 Compare |
| Candidate 生成 | `prompt_optimize` | `optimization_job_id` | 失败保留输入和失败原因 |
| CostAllocation | `cost_allocate` | `usage_meter_record_id + period` | 未归集进入 pending |
| 并发执行 | `skill_parallel_run` | `execution_plan_id` | 子任务失败按 failure_policy 处理 |

### 7.6 测试要求

- 字段级权限测试覆盖员工、评审人、主管 / HR、Skill 管理员、系统管理员。
- Prompt Lab 覆盖 DatasetCase 候选、正式、拒绝路径。
- Compare 覆盖改好、改坏、风险 Case。
- 结算测试覆盖充值 `pending -> approved -> posted`，禁止直接改余额。
- license 测试覆盖 active、expired、revoked。
- 并发测试覆盖超时、重试、Reducer 失败、预算超限。

### 7.7 二期 DoD

- 字段治理可按角色返回不同字段，不泄露源码和内部实现。
- 反馈能转 DatasetCase 候选，并经过确认进入正式测试集。
- Prompt 优化链路完整跑通。
- 成本归集、充值、license 能形成审计闭环。
- 至少一个可拆分 Skill 完成并发执行试点。
