# 三期开发文档：治理增强与知识协同

- 文档状态: 三期工程可执行草案 / 待二期验收后冻结
- 生成日期: 2026-05-08
- 阶段目标: 在价值计算、Prompt Lab、字段治理和计量结算稳定后，补齐组织治理、知识沉淀、通知、申诉、跨系统协同和复杂 DAG 编排。

---

## 1. 三期范围

三期新增能力:

- 知识沉淀: Prompt、SOP、Case、失败模式、Review 经验沉淀为 KnowledgeAsset。
- 知识推荐: 在任务创建、Review、反馈处理时推荐相关知识。
- 通知中心: 站内通知、邮件 / IM 适配层、SLA 提醒。
- 申诉与复核: 员工对分数、Review、结果归因提出申诉，管理角色复核。
- 报表模板: 月报、部门报表、Skill 运营报表、Review 质量报表。
- 权重模板: 不同业务域、任务类型、组织维度使用不同计分模板。
- 异常检测: 异常高频调用、刷分、低质量输出、风险上升自动预警。
- 跨系统协同: OA、IM、Agent 平台、文档系统、数据仓库集成。
- 复杂 DAG 编排: 在二期并发基础上支持更复杂依赖图。

三期不做:

- 外部客户 Skill 消费平台。
- SaaS 多租户商业化门户。
- 私有化部署授权中心。
- 智能化平台自动建议和能力地图。

## 2. 三期进入条件

- 一期和二期主链路稳定，已形成真实 SkillCall、ScoreRecord、DatasetCase、PromptRun、CostAllocationRecord 数据。
- 已有可沉淀的知识资产来源，例如高分结果、优秀 Review、常见失败 Case。
- 业务确认通知渠道、申诉处理 SLA、知识审核人和可见范围。
- 已确认哪些外部系统需要集成，具备 API 或数据同步条件。

## 3. 数据模型

新增表:

```text
knowledge_assets
knowledge_asset_versions
knowledge_reuse_records
notification_events
notification_deliveries
appeals
appeal_reviews
report_templates
score_policy_templates
risk_anomaly_events
external_integrations
dag_templates
dag_execution_nodes
```

关键规则:

- KnowledgeAsset 必须有来源引用和审核状态。
- 通知只发送当前角色有权查看的对象摘要。
- 申诉不直接改历史 ScoreRecord，必须生成复核记录或调整记录。
- 外部系统同步必须写审计和失败重试记录。
- 复杂 DAG 继承二期并发执行的授权、计量、风险和审计规则。

## 4. 页面

| 页面 | 路由 | 能力 |
|---|---|---|
| 知识库 | `/knowledge` | 资产列表、详情、版本、复用记录 |
| 知识审核 | `/admin/knowledge-reviews` | 来源审核、可见范围、发布 / 归档 |
| 通知中心 | `/notifications` | 待办、SLA 提醒、处理记录 |
| 申诉中心 | `/appeals` | 员工申诉、复核进度、处理结果 |
| 报表模板 | `/admin/report-templates` | 配置模板、字段、权限、周期 |
| 权重模板 | `/admin/score-policy-templates` | 业务域 / 任务类型权重模板 |
| 异常预警 | `/admin/anomalies` | 异常调用、风险趋势、刷分预警 |
| 集成配置 | `/admin/integrations` | OA / IM / Agent 平台接入 |
| DAG 模板 | `/admin/dag-templates` | 复杂执行图模板 |

## 5. 核心 API

| 方法 | 路径 | 用途 |
|---|---|---|
| POST | `/api/knowledge-assets` | 创建知识资产候选 |
| POST | `/api/knowledge-assets/{id}/review` | 知识审核 |
| GET | `/api/knowledge-assets/recommendations` | 知识推荐 |
| GET | `/api/notifications` | 通知列表 |
| POST | `/api/appeals` | 提交申诉 |
| POST | `/api/appeals/{id}/review` | 复核申诉 |
| GET/POST | `/api/admin/report-templates` | 报表模板管理 |
| GET/POST | `/api/admin/score-policy-templates` | 权重模板管理 |
| GET | `/api/admin/anomalies` | 异常事件列表 |
| POST | `/api/admin/integrations/{id}/sync` | 触发外部系统同步 |
| POST | `/api/admin/dag-templates` | 创建复杂 DAG 模板 |

## 6. Phase 拆解

### Phase 3.1：知识沉淀与推荐

交付物:

- knowledge_assets、knowledge_asset_versions、knowledge_reuse_records。
- 知识候选、审核、发布、归档。
- 任务和 Review 页面中的知识推荐。

验收:

- 知识资产必须能追溯来源 TaskResult、ReviewRecord 或 DatasetCase。
- 未审核知识不得进入推荐。
- 推荐结果按角色权限过滤。

### Phase 3.2：通知、申诉和复核

交付物:

- notification_events、notification_deliveries。
- appeals、appeal_reviews。
- 通知中心、申诉中心。

验收:

- 通知不泄露未授权对象明细。
- 申诉处理不覆盖历史 ScoreRecord，只能追加复核和调整证据。
- 申诉 SLA 可统计。

### Phase 3.3：报表模板、权重模板和异常检测

交付物:

- report_templates、score_policy_templates、risk_anomaly_events。
- 报表模板配置、权重模板配置、异常预警页面。

验收:

- 报表字段按权限过滤。
- 权重模板调整必须审批和审计。
- 异常检测结果只作为预警，不自动处罚员工。

### Phase 3.4：跨系统集成和复杂 DAG

交付物:

- external_integrations、dag_templates、dag_execution_nodes。
- OA / IM / Agent 平台适配层。
- 复杂 DAG 模板和执行摘要。

验收:

- 外部同步失败可重试，失败原因可审计。
- DAG 节点继承授权、源码保护、计量和风险规则。
- 复杂 DAG 不绕过二期 Reducer 和最终风险检查。

## 7. 三期工程执行契约

### 7.1 数据迁移约束

| 模块 | 表 | 关键字段 |
|---|---|---|
| 知识 | `knowledge_assets` | `source_type`、`source_id`、`title`、`content_ref`、`visibility_scope`、`status` |
| 知识版本 | `knowledge_asset_versions` | `knowledge_asset_id`、`version_code`、`content_snapshot`、`approved_by` |
| 复用 | `knowledge_reuse_records` | `knowledge_asset_id`、`task_id`、`user_id`、`reused_at` |
| 通知 | `notification_events` | `event_type`、`target_type`、`target_id`、`payload_summary`、`status` |
| 投递 | `notification_deliveries` | `event_id`、`channel`、`recipient_id`、`status`、`retry_count` |
| 申诉 | `appeals` | `appellant_id`、`target_type`、`target_id`、`reason`、`status` |
| 复核 | `appeal_reviews` | `appeal_id`、`reviewer_id`、`decision`、`comment` |
| 模板 | `report_templates`、`score_policy_templates` | `scope`、`template_config`、`status` |
| 异常 | `risk_anomaly_events` | `anomaly_type`、`severity`、`evidence_ref`、`status` |
| 集成 | `external_integrations` | `provider`、`auth_ref_id`、`sync_policy`、`status` |
| DAG | `dag_templates`、`dag_execution_nodes` | `template_config`、`node_key`、`dependency_keys`、`status` |

所有新增表默认使用通用审计字段、软删除和 `row_version`；通知投递记录和审计类记录可追加型保存，不允许普通管理员物理删除。

### 7.2 状态机

| 对象 | 状态 | 关键约束 |
|---|---|---|
| KnowledgeAsset | `candidate -> reviewing -> published/rejected -> archived` | 未发布知识不得进入推荐 |
| NotificationDelivery | `queued -> sent/failed/skipped` | 失败可重试，超过次数标记 failed |
| Appeal | `submitted -> reviewing -> approved/rejected/adjusted -> closed` | 申诉不直接改 ScoreRecord，只能追加复核或调整 |
| ReportTemplate | `draft -> active/archived` | active 模板变更必须生成新版本 |
| RiskAnomalyEvent | `open -> triaged -> resolved/ignored` | ignored 必须填写原因 |
| ExternalIntegration | `draft -> active/suspended/failed` | active 前必须完成连通性测试 |
| DagExecutionNode | `queued -> running -> succeeded/failed/skipped/canceled` | 继承父 DAG 授权和风险上下文 |

### 7.3 API 契约补充

`POST /api/knowledge-assets`:

```json
{
  "source_type": "task_result",
  "source_id": "tr_001",
  "type": "case",
  "title": "财务月报分析优秀案例",
  "content_ref": "s3://...",
  "visibility_scope": {"departments": ["dep_finance"]},
  "reason": "Review 高分且复用价值高"
}
```

响应返回 `knowledge_asset_id`、`status = candidate`。

`POST /api/appeals`:

```json
{
  "target_type": "score_record",
  "target_id": "sr_001",
  "reason": "人工修改耗时记录错误",
  "evidence_ref": "s3://..."
}
```

约束:

- 只能申诉本人可见对象。
- 申诉通过后生成调整记录，不原地覆盖历史记录。

`GET /api/knowledge-assets/recommendations`:

请求参数:

```text
task_type
business_domain
skill_id
limit
```

响应只返回调用者可见知识摘要，不返回未授权内容全文。

`POST /api/admin/integrations/{id}/sync`:

必须传 `sync_scope`、`idempotency_key`，失败返回可重试错误和审计 ID。

### 7.4 权限契约

| 能力 | 权限 |
|---|---|
| 创建知识候选 | 任务创建人、reviewer、skill_admin |
| 发布知识 | knowledge_admin 或授权 skill_admin |
| 查看推荐知识 | 按 `visibility_scope` 和数据权限过滤 |
| 提交申诉 | 对本人可见对象 |
| 复核申诉 | manager、hr、system_admin 按授权范围 |
| 配置通知和集成 | system_admin |
| 修改权重模板 | skill_admin + 审批 |

### 7.5 异步任务

| 任务 | 队列 | 幂等键 | 失败处理 |
|---|---|---|---|
| 知识推荐索引 | `knowledge_index` | `knowledge_asset_id + version_code` | 失败不发布推荐，保留重试 |
| 通知投递 | `notification_delivery` | `event_id + channel + recipient_id` | 最多重试 3 次 |
| 外部同步 | `integration_sync` | `integration_id + sync_scope + idempotency_key` | 失败记录可重试 |
| 异常检测 | `anomaly_detect` | `period + detector_code` | 失败不生成异常结论 |
| DAG 执行 | `dag_run` | `dag_execution_id` | 节点失败按 DAG 策略处理 |

### 7.6 测试要求

- 知识权限测试: 未发布、未授权知识不能推荐。
- 通知测试: 通知摘要不泄露未授权对象字段。
- 申诉测试: 通过 / 拒绝 / 调整均有审计，不覆盖历史 ScoreRecord。
- 模板测试: active 模板变更生成新版本。
- 集成测试: 外部同步失败可重试，重复请求幂等。
- DAG 测试: 节点继承授权、计量、源码保护和风险规则。

### 7.7 三期 DoD

- 高分结果、Review 经验和失败 Case 能进入知识候选并发布。
- 任务和 Review 场景能推荐授权范围内知识。
- 通知、申诉和报表模板可按权限运行。
- 异常检测只产生预警，不自动处罚或改分。
- 复杂 DAG 不绕过二期并发、Reducer、风险和审计规则。
