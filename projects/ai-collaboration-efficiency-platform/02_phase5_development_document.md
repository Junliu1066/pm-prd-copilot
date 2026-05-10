# 五期开发文档：智能化平台

- 文档状态: 五期工程可执行草案 / 待四期验收后冻结
- 生成日期: 2026-05-08
- 阶段目标: 在内部运营数据、外部消费数据、成本数据、质量数据和反馈数据稳定后，提供智能评分、成长建议、成本 ROI、数据治理、跨组织能力地图和自动运营建议。

---

## 1. 五期范围

五期新增能力:

- 智能评分辅助: 对 ScoreRecord、Review、反馈和业务结果做异常解释和辅助校准。
- 员工成长建议: 基于任务类型、Skill 使用、Review 反馈和学习路径生成建议。
- Skill 运营建议: 推荐推广、优化、下线、限流或加强 Review 的 Skill。
- 成本 ROI 分析: 结合 Usage、Cost、Score 和客户消费数据分析投入产出。
- 数据治理: 数据质量评分、缺失字段识别、口径漂移监控。
- 跨组织能力地图: 按组织、岗位、业务域、Skill 形成能力热力图。
- 自动运营建议: 自动生成月度 Skill 运营复盘、风险提示和改进动作。

五期不做:

- 自动奖惩、自动绩效结论、自动淘汰。
- 无人工确认的自动权重调整。
- 无审批的自动发布、自动下线或自动扣费调整。

## 2. 进入条件

- 一期到四期的数据链路稳定。
- ScoreRecord、ReviewRecord、UsageMeterRecord、CostAllocationRecord、CustomerUsageRecord 数据达到可分析样本量。
- 业务负责人确认智能建议只作为辅助，不作为自动管理动作。
- 已确认数据使用授权、脱敏口径、模型评估规则和人工复核流程。

## 3. 数据模型

新增表:

```text
insight_jobs
insight_cards
skill_operation_recommendations
employee_growth_recommendations
roi_analysis_records
data_quality_checks
metric_drift_events
organization_capability_maps
recommendation_feedback
```

核心规则:

- 所有智能建议必须保存输入数据范围、模型版本、生成时间和解释摘要。
- 建议不能直接修改权重、分数、Skill 状态、授权或结算数据。
- 用户对建议的采纳、忽略和反馈必须记录，形成 recommendation_feedback。

## 4. 页面

| 页面 | 路由 | 能力 |
|---|---|---|
| 智能洞察 | `/insights` | 组织、Skill、成本、风险洞察卡片 |
| Skill 运营建议 | `/insights/skills` | 推广、优化、下线、限流建议 |
| 成长建议 | `/insights/growth` | 个人和团队能力提升建议 |
| ROI 分析 | `/insights/roi` | 成本、价值、收益、趋势 |
| 数据质量 | `/admin/data-quality` | 缺失字段、异常值、口径漂移 |
| 能力地图 | `/insights/capability-map` | 组织 / 岗位 / 业务域能力热力图 |
| 建议反馈 | `/insights/recommendation-feedback` | 采纳、忽略、人工备注 |

## 5. 核心 API

| 方法 | 路径 | 用途 |
|---|---|---|
| POST | `/api/insight-jobs` | 创建洞察任务 |
| GET | `/api/insights` | 洞察卡片列表 |
| GET | `/api/insights/skills` | Skill 运营建议 |
| GET | `/api/insights/growth` | 成长建议 |
| GET | `/api/insights/roi` | ROI 分析 |
| GET | `/api/admin/data-quality/checks` | 数据质量检查 |
| GET | `/api/insights/capability-map` | 能力地图 |
| POST | `/api/insights/recommendations/{id}/feedback` | 建议反馈 |

## 6. Phase 拆解

### Phase 5.1：数据治理和洞察基线

交付物:

- data_quality_checks、metric_drift_events。
- insight_jobs、insight_cards。
- 数据质量页面和基础洞察卡片。

验收:

- 指标缺失、字段异常、口径漂移能被识别。
- 洞察卡片必须展示数据范围、统计口径和生成时间。

### Phase 5.2：Skill 运营建议和 ROI 分析

交付物:

- skill_operation_recommendations、roi_analysis_records。
- Skill 运营建议页面、ROI 分析页面。

验收:

- 推荐推广、优化、下线或限流都必须有证据来源。
- ROI 不能只看调用量，必须结合质量、节省工时、成本、Review 和反馈。

### Phase 5.3：成长建议和能力地图

交付物:

- employee_growth_recommendations、organization_capability_maps。
- 成长建议页面、能力地图页面。

验收:

- 成长建议只对本人、主管授权范围或 HR 汇总范围可见。
- 能力地图默认展示聚合，不暴露未授权个人敏感明细。

### Phase 5.4：自动运营建议闭环

交付物:

- recommendation_feedback。
- 建议采纳、忽略、人工备注和效果复盘。
- 自动生成月度 Skill 运营复盘草稿。

验收:

- 智能建议不能直接执行生产变更。
- 采纳建议后的效果必须可追踪。
- 低置信建议必须标注“不建议直接执行”。

## 7. 五期工程执行契约

### 7.1 数据迁移约束

| 表 | 关键字段 | 约束 |
|---|---|---|
| insight_jobs | `job_type`、`scope`、`model_profile_id`、`status`、`started_at/finished_at` | 必须记录数据范围和模型版本 |
| insight_cards | `job_id`、`card_type`、`title`、`summary`、`evidence_refs`、`confidence`、`status` | 只展示授权范围内证据 |
| skill_operation_recommendations | `skill_id`、`recommendation_type`、`reason_snapshot`、`confidence`、`status` | 不自动改 Skill 状态 |
| employee_growth_recommendations | `user_id`、`scope`、`recommendation`、`evidence_refs`、`status` | 只本人和授权管理者可见 |
| roi_analysis_records | `period`、`skill_id`、`cost_snapshot`、`value_snapshot`、`roi_result` | 必须保存公式和数据范围 |
| data_quality_checks | `check_code`、`target_table`、`result`、`severity`、`status` | 不直接修数据 |
| metric_drift_events | `metric_code`、`baseline_period`、`current_period`、`delta`、`status` | 只做预警 |
| organization_capability_maps | `org_id`、`period`、`map_snapshot`、`visibility_scope` | 默认聚合展示 |
| recommendation_feedback | `recommendation_id`、`actor_id`、`action`、`comment` | 采纳 / 忽略都要记录 |

### 7.2 状态机

| 对象 | 状态 | 关键约束 |
|---|---|---|
| InsightJob | `queued -> running -> succeeded/failed/canceled` | 失败不生成正式洞察卡 |
| InsightCard | `draft -> published/archived` | published 前必须完成权限过滤 |
| Recommendation | `generated -> reviewed -> accepted/ignored/rejected -> measured` | accepted 不等于自动执行 |
| DataQualityCheck | `queued -> running -> passed/warned/failed` | failed 只产生问题，不自动改数据 |
| MetricDriftEvent | `open -> triaged -> resolved/ignored` | ignored 必须填写原因 |

### 7.3 API 契约补充

`POST /api/insight-jobs`:

```json
{
  "job_type": "skill_operation",
  "scope": {
    "date_from": "2026-05-01",
    "date_to": "2026-05-31",
    "department_ids": ["dep_finance"],
    "skill_ids": ["sk_001"]
  },
  "model_profile_id": "model_insight_001",
  "idempotency_key": "insight_2026_05_finance"
}
```

响应返回 `insight_job_id`、`status`、`estimated_finish_at`。

`GET /api/insights/skills`:

请求参数:

```text
period
department_id
skill_id
recommendation_type
```

响应必须返回建议摘要、证据引用、置信度、风险提示和人工确认状态。

`POST /api/insights/recommendations/{id}/feedback`:

```json
{
  "action": "accepted",
  "comment": "纳入下月 Skill 优化计划",
  "follow_up_owner_id": "usr_001"
}
```

约束:

- `accepted` 只表示接受建议，不自动修改生产对象。
- 如果需要改 Skill、权重、授权或结算，必须回到对应管理流程审批。

### 7.4 权限与安全

- 员工只能看自己的成长建议。
- 主管看授权组织范围内的聚合建议和必要明细。
- HR 默认看聚合分布，不看敏感输入全文。
- Skill 管理员看授权 Skill 的运营建议。
- ROI 和成本明细只对授权财务 / 管理角色可见。
- 洞察生成不得把未授权敏感全文写入 insight_cards。

### 7.5 异步任务

| 任务 | 队列 | 幂等键 | 失败处理 |
|---|---|---|---|
| 洞察生成 | `insight_generate` | `job_type + scope_hash + idempotency_key` | 失败写 InsightJob.failed |
| ROI 计算 | `roi_calculate` | `period + skill_id + scope_hash` | 成本或价值缺失时标记 incomplete |
| 数据质量检查 | `data_quality_check` | `check_code + period` | 失败只记录，不修数据 |
| 能力地图生成 | `capability_map_build` | `org_id + period` | 失败不发布地图 |
| 建议效果复盘 | `recommendation_measure` | `recommendation_id + period` | 无数据标记 pending |

### 7.6 测试要求

- 权限测试: 成长建议、ROI 明细、能力地图按角色过滤。
- 数据质量测试: 缺失字段、异常值、口径漂移能被识别。
- 建议安全测试: 建议不会直接调用生产变更 API。
- 解释测试: 每张洞察卡都有数据范围、指标口径、证据引用和置信度。
- 回归测试: 采纳建议后的效果能关联后续指标，不覆盖历史数据。

### 7.7 五期 DoD

- 洞察任务能基于授权数据生成可解释洞察卡。
- Skill 运营建议、成长建议、ROI 分析和能力地图均有证据链。
- 智能建议不自动执行生产变更。
- 数据治理能发现缺失、异常和口径漂移。
- 建议采纳、忽略和效果复盘都有记录。
