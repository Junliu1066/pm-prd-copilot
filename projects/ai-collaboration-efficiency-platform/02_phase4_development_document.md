# 四期开发文档：Skill 消费平台 / SaaS 与私有化交付版

- 文档状态: 四期工程可执行草案 / 待三期验收后冻结
- 生成日期: 2026-05-08
- 阶段目标: 面向外部客户和企业业务用户提供 AI Skill 使用平台，支持线上 SaaS 使用版和本地部署 / 私有化授权版。

---

## 1. 产品定位

Skill 消费平台面向外部客户和企业业务用户。客户可以像使用 SaaS 工具一样选择 Skill、提交任务、获得结果、查看历史和管理额度。

无论线上 SaaS 还是本地部署，客户购买的是 Skill 使用权和运行授权，不获得 Skill 源码、Prompt、Workflow、工具代码和私有规则的明文交付。

## 2. 四期范围

四期新增能力:

- 客户租户管理。
- Skill Marketplace / Skill 目录。
- Skill 订阅、套餐、额度和 license。
- 客户任务提交、结果查看、历史记录。
- 客户侧用量看板和额度管理。
- SaaS 多租户隔离。
- 私有化部署授权。
- 加密 Skill 包分发。
- 本地运行时授权校验。
- 客户侧审计日志。
- 外部 API 调用入口。

四期不做:

- 向客户交付源码、Prompt 源、Workflow DAG、工具代码、LangChain 代码段或私有规则明文。
- 客户自行修改生产 Skill。
- 客户绕过平台调用加密 Skill 包。
- 智能化自动运营建议和能力地图。

## 3. 进入条件

- 内部 Skill 管理、版本、授权、审计、计量和源码保护机制稳定。
- 成本归集、充值 / license 和客户额度模型可解释、可审计。
- 已确认首批外部客户或企业业务用户场景。
- 已确认线上 SaaS 和私有化部署的交付边界、合同授权、数据留存和安全要求。
- 已确认私有化部署使用的 license 校验、机器指纹或租户授权策略。

## 4. 交付形态

| 形态 | 目标 | 技术要求 |
|---|---|---|
| 线上 SaaS 版 | 降低客户使用门槛，快速试用和购买 | 多租户隔离、在线额度、客户审计、在线授权校验 |
| 本地部署 / 私有化授权版 | 解决企业客户数据不出域 | 加密 Skill 包、本地运行时、离线 license、部署 Secret、客户侧审计 |

共同原则:

- Skill 包始终加密存储。
- 客户只能运行 Skill，不能读取源码明文。
- 运行授权必须绑定租户、环境、版本、有效期和额度。
- 客户数据按租户隔离，不得跨租户进入训练或分析链路，除非合同明确授权。

## 5. 数据模型

新增表:

```text
customer_tenants
customer_users
customer_roles
customer_skill_catalog_items
customer_skill_subscriptions
customer_tasks
customer_skill_calls
customer_task_results
customer_usage_records
customer_license_entitlements
customer_api_keys
deployment_packages
deployment_license_files
runtime_activation_records
customer_audit_logs
customer_billing_exports
```

核心关系:

- `customer_skill_catalog_items` 只引用内部 `skills` / `skill_versions` 的可消费版本摘要。
- `customer_skill_subscriptions` 决定客户能使用哪些 Skill、额度、有效期和部署形态。
- `deployment_packages` 保存加密 Skill 包版本，不保存源码明文。
- `runtime_activation_records` 记录私有化环境的激活、续期、撤销和审计。

## 6. 页面

| 页面 | 路由 | 能力 |
|---|---|---|
| 客户工作台 | `/customer` | 可用 Skill、任务状态、额度摘要 |
| Skill 市场 | `/customer/marketplace` | Skill 目录、适用场景、套餐、试用入口 |
| Skill 详情 | `/customer/skills/{id}` | 用途说明、输入输出要求、额度、调用入口 |
| 提交任务 | `/customer/tasks/new` | 按 Skill 输入协议提交任务 |
| 任务历史 | `/customer/tasks` | 历史任务、状态、结果下载 |
| 结果详情 | `/customer/tasks/{id}` | 输出结果、附件、审计摘要 |
| 额度管理 | `/customer/billing` | 套餐、调用次数、token、license、到期时间 |
| API Key 管理 | `/customer/api-keys` | 外部 API 调用密钥 |
| 私有化授权 | `/customer/deployments` | 部署包、license 文件、激活状态 |
| 客户审计 | `/customer/audit-logs` | 调用、授权、导出、激活记录 |
| 运营后台 | `/admin/customers` | 租户、订阅、额度、部署授权管理 |

## 7. 核心 API

| 方法 | 路径 | 用途 |
|---|---|---|
| GET | `/api/customer/marketplace/skills` | 客户可见 Skill 目录 |
| GET | `/api/customer/skills/{id}` | Skill 详情和输入输出协议 |
| POST | `/api/customer/tasks` | 客户提交任务 |
| POST | `/api/customer/tasks/{id}/run` | 运行客户任务 |
| GET | `/api/customer/tasks` | 任务历史 |
| GET | `/api/customer/tasks/{id}` | 结果详情 |
| GET | `/api/customer/usage` | 用量和额度 |
| POST | `/api/customer/api-keys` | 创建 API Key |
| POST | `/api/admin/customer-tenants` | 创建客户租户 |
| POST | `/api/admin/customer-subscriptions` | 创建订阅 / 授权 |
| POST | `/api/admin/deployment-packages` | 生成私有化部署包 |
| POST | `/api/runtime/activate` | 本地运行时激活 |
| POST | `/api/runtime/validate-license` | 本地运行时授权校验 |

## 8. 安全与源码保护

- 客户 API 不返回 `encrypted_package_ref`、源码、Prompt 源、Workflow DAG、底层 API、代码段或私有规则。
- 私有化部署包只包含加密 Skill 包、运行时、license 校验器和部署配置。
- 本地运行时解密只在受控进程和临时目录内完成，执行后清理。
- license 校验失败时不允许运行 Skill。
- 客户审计日志记录调用、授权校验、额度扣减、结果导出和部署激活。

## 9. Phase 拆解

### Phase 4.1：SaaS 客户租户与 Skill 市场

交付物:

- customer_tenants、customer_users、customer_roles。
- customer_skill_catalog_items、customer_skill_subscriptions。
- 客户工作台、Skill 市场、Skill 详情。

验收:

- 不同租户 Skill 目录和数据隔离。
- 未订阅 Skill 不可调用。
- 客户只看到可消费字段，不看到内部管理字段。

### Phase 4.2：客户任务、结果和用量

交付物:

- customer_tasks、customer_skill_calls、customer_task_results、customer_usage_records。
- 任务提交、运行、结果历史、用量看板。

验收:

- 客户任务形成可审计 SkillCall。
- 用量扣减可解释，失败调用按规则处理。
- 结果导出按客户租户权限过滤。

### Phase 4.3：额度、license 和外部 API

交付物:

- customer_license_entitlements、customer_api_keys。
- 客户额度管理、API Key 管理、外部 API 调用入口。

验收:

- license 过期、额度不足、授权缺失时禁止调用。
- API Key 不返回明文二次展示。
- 外部 API 调用写入客户审计。

### Phase 4.4：私有化部署授权

交付物:

- deployment_packages、deployment_license_files、runtime_activation_records。
- 加密部署包生成、本地运行时激活、离线 license 校验。

验收:

- 私有化客户可以在数据不出域的环境中运行授权 Skill。
- 客户拿不到源码、Prompt 源、Workflow DAG 和工具代码明文。
- license 撤销、过期和机器指纹不匹配时，运行时拒绝调用并记录审计。

## 10. 四期工程执行契约

### 10.1 数据迁移约束

| 表 | 关键字段 | 约束 |
|---|---|---|
| customer_tenants | `name`、`tenant_type`、`status`、`data_region` | tenant 级唯一名称；停用后禁止新调用 |
| customer_users | `tenant_id`、`email`、`role_ids`、`status` | `unique(tenant_id, email)` |
| customer_skill_catalog_items | `tenant_id`、`skill_id`、`skill_version_id`、`display_profile`、`status` | 不保存源码明文 |
| customer_skill_subscriptions | `tenant_id`、`skill_id`、`plan_code`、`quota`、`valid_from/to`、`status` | active 才能调用 |
| customer_tasks | `tenant_id`、`created_by`、`skill_id`、`status`、`input_ref` | 租户隔离 |
| customer_skill_calls | `tenant_id`、`task_id`、`subscription_id`、`runtime_auth_snapshot`、`status` | 必须绑定订阅 |
| customer_task_results | `tenant_id`、`task_id`、`skill_call_id`、`output_ref`、`status` | 输出按租户隔离 |
| customer_usage_records | `tenant_id`、`subscription_id`、`metric_type`、`quantity`、`status` | 可扣减额度 |
| customer_license_entitlements | `tenant_id`、`deployment_id`、`license_fingerprint`、`status` | 不保存 license 明文 |
| deployment_packages | `tenant_id`、`package_version`、`encrypted_package_ref`、`package_hash` | 加密包不可覆盖 |
| runtime_activation_records | `tenant_id`、`machine_fingerprint`、`license_id`、`status` | 激活、续期、撤销可审计 |
| customer_audit_logs | `tenant_id`、`actor_id`、`action`、`target_type/id`、`created_at` | 追加型，不软删 |

### 10.2 状态机

| 对象 | 状态 | 关键约束 |
|---|---|---|
| CustomerTenant | `trial -> active/suspended/closed` | suspended 禁止新调用 |
| CustomerSkillSubscription | `pending -> active/suspended/expired/revoked` | active 且额度有效才可调用 |
| CustomerTask | `draft -> submitted -> running -> succeeded/failed/canceled` | canceled 不扣成功用量 |
| CustomerSkillCall | `created -> authorized -> running -> succeeded/failed/billed` | 未授权不得进入 running |
| CustomerUsageRecord | `pending -> confirmed/deducted/voided` | deducted 必须有关联订阅和审计 |
| DeploymentPackage | `draft -> signed -> published/revoked/archived` | published 后不可覆盖 |
| RuntimeActivation | `pending -> active/expired/revoked/failed` | revoked / expired 不允许运行 |

### 10.3 API 契约补充

`POST /api/customer/tasks`:

```json
{
  "skill_catalog_item_id": "csk_001",
  "title": "生成客户经营分析报告",
  "input_payload": {"business_scenario": "monthly_review"},
  "input_object_refs": ["s3://tenant-a/input.xlsx"],
  "idempotency_key": "customer_task_001"
}
```

响应返回 `customer_task_id`、`status`、`quota_preview`。

`POST /api/customer/tasks/{id}/run`:

约束:

- 必须校验租户、用户、订阅、额度、license、Skill 版本状态。
- 必须生成 `runtime_auth_snapshot`。
- 不返回源码包引用、Prompt 源、Workflow DAG、工具代码或私有规则。

`POST /api/admin/deployment-packages`:

```json
{
  "tenant_id": "tenant_001",
  "skill_version_ids": ["skv_001"],
  "deployment_type": "private",
  "valid_to": "2027-05-08T00:00:00+08:00"
}
```

响应返回 `deployment_package_id`、`package_hash`、`license_request_required`。

`POST /api/runtime/activate`:

```json
{
  "tenant_id": "tenant_001",
  "deployment_package_id": "dpkg_001",
  "machine_fingerprint": "fp_...",
  "license_file_ref": "file://license"
}
```

响应返回 `activation_status`、`valid_to`、`allowed_skill_versions`。

### 10.4 权限与租户隔离

- 所有 customer API 必须带 `tenant_id` 上下文。
- 客户用户只能访问本租户数据。
- 平台运营人员跨租户查看必须有 `platform_operator` 权限，并写审计。
- 客户管理员能管理本租户用户、API Key、额度视图，不能管理内部 Skill 源码。
- 私有化运行时只验证授权和运行 Skill，不暴露源码。

### 10.5 异步任务

| 任务 | 队列 | 幂等键 | 失败处理 |
|---|---|---|---|
| 客户 Skill 运行 | `customer_skill_run` | `tenant_id + task_id + idempotency_key` | 失败写 CustomerSkillCall.failed |
| 客户用量扣减 | `customer_usage_deduct` | `customer_skill_call_id + metric_type` | 扣减失败不得标记 billed |
| 部署包生成 | `deployment_package_build` | `tenant_id + package_version` | 失败不发布 package |
| 运行时激活 | `runtime_activation` | `tenant_id + machine_fingerprint + license_id` | 激活失败记录原因 |
| 客户审计导出 | `customer_audit_export` | `tenant_id + export_id` | 失败标记导出 failed |

### 10.6 测试要求

- 多租户隔离测试: tenant A 不能查询 tenant B 的任务、结果、用量和审计。
- 订阅测试: 未订阅、过期、额度不足、license revoked 都不能运行 Skill。
- 源码保护测试: SaaS 和私有化响应均不返回源码、Prompt 源、Workflow DAG、底层 API 和代码段。
- 私有化测试: 机器指纹不匹配、license 过期、包被撤销时运行失败。
- API Key 测试: 创建后只展示一次明文，后续只展示 masked value。
- 用量测试: 成功调用、失败调用、取消调用按规则计量和扣减。

### 10.7 四期 DoD

- 一个外部客户能完成注册 / 授权 / 选择 Skill / 提交任务 / 查看结果 / 查看用量。
- SaaS 多租户隔离通过自动化测试。
- 私有化部署包能在本地环境激活并运行授权 Skill。
- 客户无法通过 API、日志、报表或部署包获得源码明文。
- 客户侧调用、授权、用量、导出和激活都有审计。
