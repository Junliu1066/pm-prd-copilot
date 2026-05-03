# 治理生命周期嵌入方案

- 日期：2026-05-02
- 状态：proposal，不是 stable policy。
- 目标：把治理生命周期机制嵌入现有 PM Skill 系统，让稳定核心、候选能力、项目产物、AI 情报、proposal、archive、memory-cache 都有身份、状态、边界和出口。
- 原则：
  - 长期稳定可靠优先。
  - 如无必要，不增 skill，不增 harness。
  - 能用现有 docs、registry、workflow、harness、pipeline、closeout 和定时汇报解决的，不新增长期组件。
  - 本方案不批准删除、归档、staging、commit、push、PR、stable 转正、长期记忆写入或自动化放权。

## 一句话方案

不要新增一套“大治理系统”。把生命周期规则嵌入已有系统，让每个对象都按同一套状态流转：

```text
临时产物
-> 候选
-> 人工审核
-> 稳定核心 / 项目内保留 / 归档候选 / 30 天后删除候选
-> 定期复盘
```

核心要求：

- 所有东西必须有身份：stable core、candidate、project artifact、archive evidence、raw evidence、memory cache、temporary proposal。
- 所有东西必须有状态：active、reviewed、deferred、archived candidate、delete-after-30-days candidate。
- 所有东西必须有边界：能不能写文件、能不能跨项目、能不能进入长期规则、能不能提交。
- 所有东西必须有出口：保留、转正、归档、删除候选、拒绝、不再处理。

## 为什么先做嵌入

当前剩余问题看起来分散，但本质相同：

| 区域 | 表面问题 | 本质问题 |
|---|---|---|
| `docs/proposals/*` | 临时材料和决策记录混在一起 | 缺少 proposal 生命周期。 |
| `ai-intel/raw/*` | raw 证据不知道是否提交 | 缺少 AI 情报证据生命周期。 |
| `docs/archive/*` | archive 证据和额外历史材料混在一起 | 缺少归档 / 删除生命周期。 |
| `projects/*` | 项目产物容易污染稳定核心 | 缺少项目产物生命周期。 |
| `memory-cache/*` | 项目偏好可能误写长期记忆 | 缺少偏好缓存生命周期。 |
| skill / harness / plugin | candidate 和 stable 容易混淆 | 缺少能力候选生命周期。 |

如果继续逐项修，会反复讨论边界。先嵌入通用生命周期，后续每块直接按状态机处理。

## 嵌入点设计

| 嵌入点 | 承担职责 | 不承担职责 |
|---|---|---|
| `docs/` | 写清生命周期规则、人工审批点、各类材料处理边界。 | 不直接执行删除、归档、转正。 |
| `registry/` | 记录 skill、plugin、artifact、steward 的 stable / candidate / detachable 状态。 | 不替代用户审批。 |
| `workflow/actions.yaml` | 声明 action 输入、输出、owner 和 artifact 类型。 | 不绕过 pipeline gate。 |
| `harness/run_harness.py` | 检查合同、边界、写文件风险；默认 check-only。 | 不新增过多 checker，不自动修复。 |
| `pipeline` | 默认 governed；只有显式 `--fast-draft` 才允许草稿路径。 | 不把草稿当正式交付。 |
| `projects/*/closeout` | 项目归档前总结、反思、偏好处置、架构反哺和清理候选。 | 不代表项目自动归档。 |
| 定时周报 | 汇报问题、建议、风险、需要用户拍板项。 | 不自动删除、归档、提交、转 stable。 |

## 对象生命周期

### 1. 项目产物生命周期

适用对象：

- `projects/*`
- `projects/*/prototype`
- `projects/*/runs`
- `projects/*/closeout`
- `projects/*/*.generated.*`
- `projects/*/*.final.*`

状态：

```text
active
-> closeout_candidate
-> closeout_reviewed
-> archived_candidate
-> hard_delete_eligible
```

规则：

- active 项目不清理、不归档、不提交到稳定核心。
- closeout 只是审核材料，不等于归档。
- prototype PNG / HTML / UI 风格是项目产物，不是稳定核心。
- run 输出默认项目内保留；fixture 才允许最小审计证据。
- final 人工稿未完成时不能升级 golden sample。

高风险审批：

- 项目归档。
- 项目产物提交。
- 清理 run 输出。
- 删除或移动项目目录。
- 项目经验进入长期规则。

### 2. Proposal 生命周期

适用对象：

- `docs/proposals/*`

状态：

```text
temporary_staging_material
decision_record
superseded_by_commit
architecture_candidate
archive_candidate
delete_after_30_days_candidate
```

规则：

- staging list / commit review 默认是临时材料。
- 有长期决策价值的中文审计报告可保留。
- 已被正式提交、正式审查或总清单覆盖的材料应标为 superseded。
- 英文旧过程材料不直接长期保留；有价值时提炼成中文总结。

高风险审批：

- 删除 proposal。
- 移入 archive。
- 将 proposal 内容转 stable policy。

### 3. AI 情报生命周期

适用对象：

- `ai-intel/raw`
- `ai-intel/events`
- `ai-intel/daily`
- `ai-intel/logs`
- `ai-intel/decisions`
- `ai-intel/scripts`

状态：

```text
raw_local_evidence
normalized_event
reviewed_daily_signal
architecture_inbox_candidate
decision_doc_candidate
adopted_after_user_approval
```

规则：

- raw 默认本地证据，不提交。
- daily / events / logs 经人工复核后可作为证据提交。
- decision docs 不能被脚本直接自动改成架构结论。
- AI 情报只能提供信号，不能自动修改 skill、harness、registry、workflow、模型策略或长期规则。

高风险审批：

- 启动联网抓取。
- 提交 raw。
- 更新 decision docs。
- 因 AI 情报改变模型、供应商、成本策略或治理架构。

### 4. Memory Cache 生命周期

适用对象：

- `memory-cache/*`
- `pm-prd-copilot/memory/user_preferences.md`
- `teaching/*`

状态：

```text
project_local_cache
approved_project_preference
candidate_project_preference
closeout_disposition
long_term_candidate
long_term_approved
cleared_after_archive_alignment
```

规则：

- `memory-cache/*` 默认项目内保留，不提交。
- 项目偏好不能跨项目复用。
- 长期记忆必须逐条批准。
- closeout 前必须对齐：保留为项目档案、清除 active 指针、提炼长期候选或拒绝。
- teaching 记录不等于长期规则。

高风险审批：

- 写入长期记忆。
- 清空 active cache。
- 跨项目复用项目偏好。
- 把用户纠错沉淀为 stable rule。

### 5. 能力候选生命周期

适用对象：

- `plugins/*`
- `.agents/plugins/marketplace.json`
- `registry/plugins.yaml`
- `registry/skills.yaml`
- `harness/*`
- `stewards/*`
- skill patch proposal

状态：

```text
candidate
detachable_candidate
validated_candidate
promotion_review
stable_core
defer_not_stable
archive_candidate
delete_after_30_days_candidate
```

规则：

- candidate 可见不等于 stable。
- 新 skill / harness / plugin 必须先证明现有文档、模板、脚本参数或现有检查不足。
- 按需 checker 只能在对应项目明确需要时触发。
- Promotion gate 必须有多项目证据、替代方案比较、写入边界、回滚方式和用户批准。

高风险审批：

- candidate 转 stable。
- 新增 skill。
- 新增 harness。
- 修改 workflow stage。
- 修改 registry category。
- 删除候选能力。

### 6. Archive / 删除生命周期

适用对象：

- `docs/archive/*`
- root 历史文件
- historical zip / old overview
- raw evidence archive

状态：

```text
archive_evidence_candidate
canonical_aligned
retention_started
delete_after_30_days_candidate
hard_delete_approved
deleted
```

规则：

- archive 是证据，不等于批准硬删除。
- root 删除必须先确认 canonical copy 和 archive copy。
- 二进制历史包不应恢复到 root。
- 硬删除必须在归档后至少 30 天，并再次拿精确清单给用户批准。

高风险审批：

- 接受 root 删除状态。
- 提交 archive 目录。
- 删除 archive copy。
- 启动 30 天删除窗口。
- 执行硬删除。

### 7. Error Report 生命周期

适用对象：

- `docs/error_reports/*`
- bug log
- daily run reports

状态：

```text
reported
triaged
fix_proposed
fixed
watch
closed_after_regression
architecture_feedback_candidate
```

规则：

- 每个 bug 必须有解决方案建议、最小安全修复、验证方式和是否需要用户批准。
- fixed 之后仍可进入 watch。
- 重复问题要反哺 regression、模板、prompt 或工作规则候选，但不能自动稳定化。

高风险审批：

- 因 bug 修改 stable skill / harness / workflow。
- 因 bug 删除或归档文件。
- 因 bug 写长期规则。

## 统一状态字段建议

后续所有清单尽量用统一字段：

| 字段 | 含义 |
|---|---|
| `object_type` | project_artifact / proposal / ai_intel / memory_cache / capability / archive / error_report |
| `current_state` | 当前生命周期状态 |
| `recommended_state` | 推荐进入的下一状态 |
| `write_behavior` | read_only / writes_project / writes_report / writes_archive |
| `cross_project_allowed` | 是否允许跨项目 |
| `stable_allowed` | 是否可以进入 stable core |
| `user_approval_required` | 是否需要用户批准 |
| `retention_rule` | 保留、归档、30 天删除候选 |
| `validation` | 推荐检查命令 |
| `rollback` | 回退方式 |

## 嵌入执行顺序

推荐分三阶段。

### 阶段 1：Proposal 阶段

当前阶段。

动作：

- 保持本文件为 proposal。
- 用它指导剩余事项分类。
- 不修改 stable policy。
- 不新增 harness / skill。

适合处理：

- 剩余 `docs/proposals/*`。
- `ai-intel/raw/*`。
- `docs/archive/*`。
- 其它 `projects/*`。

### 阶段 2：人工监督校准

持续 2-4 周。

动作：

- 周报按生命周期状态汇报。
- 每项都给推荐选择、优劣势、暂缓影响。
- 记录用户实际拍板。
- 统计判断一致率、误报率、漏报率。

可自动做的低风险动作：

- 生成草案。
- 刷新清单。
- 跑 check-only。
- 分类建议。

仍需人工审批：

- stable 转正。
- 删除、归档。
- 提交、push、PR。
- 长期记忆。
- 模型 / 成本 / 外部数据源。

### 阶段 3：低风险规则稳定化

只有当 2-4 周判断稳定后，才考虑把低风险部分转 stable。

候选稳定项：

- `projects/*` 默认不混入稳定核心。
- `memory-cache/*` 默认不提交。
- `ai-intel/raw/*` 默认不提交。
- candidate plugin 默认不转 stable。
- closeout 不等于归档。
- 删除必须归档先行、30 天后再批准。

不建议自动稳定化的项：

- 某个具体项目偏好。
- 某个具体 UI 风格。
- 某个单项目 PRD 样例。
- 某个新增 skill / harness。

## 和现有文件的关系

| 文件 | 当前角色 | 后续关系 |
|---|---|---|
| `docs/proposals/governance_lifecycle_policy.md` | 总体生命周期 proposal | 本方案是它的嵌入执行版。 |
| `docs/project_lifecycle.md` | 项目生命周期规则 | 保持项目维度，后续可吸收 C 批稳定结论。 |
| `docs/operating_model.md` | 日常节奏 | 后续可加入生命周期状态汇报节奏。 |
| `docs/scheduled_check_mechanisms.md` | 定时任务边界 | 后续可加入生命周期状态校准指标。 |
| `docs/workspace_change_partition.md` | 工作区分区地图 | 后续可用统一状态字段刷新。 |
| `docs/proposals/c8_project_artifact_final_disposition_checklist.md` | C 批项目产物收口 | 是本方案的项目产物应用样例。 |

## 需要你后续拍板

| 拍板项 | 我的建议 | 不同选择的效果 |
|---|---|---|
| 是否把本方案作为后续剩余问题的统一判断框架 | 先作为 proposal 使用 | 能提高一致性，但不会立刻增加稳定规则负担。 |
| 是否现在转 stable policy | 不现在转 | 先跑 2-4 周校准更稳；现在转可能过早固化。 |
| 是否新增 harness 检查生命周期状态 | 不新增 | 先用文档和周报执行；后续发现人工漏项再考虑。 |
| 是否新增 skill 管理生命周期 | 不新增 | 现有 docs / registry / steward 足够先承接。 |
| 是否允许低风险半自动 | 只允许生成清单和 check-only | 能减轻人工整理负担，但不越权。 |

## 下一步应用建议

如果你认可这个 proposal，建议按以下顺序应用：

1. 用本方案处理剩余 `docs/proposals/*`。
2. 用本方案处理 `ai-intel/raw/*`。
3. 用本方案处理 `docs/archive/*`。
4. 用本方案处理其它 `projects/*`。
5. 用本方案复核 skill / harness / plugin candidate 是否仍有必要。
6. 汇总成“本轮治理修复总验收报告”。

## 本方案当前不执行

- 不修改 stable docs。
- 不修改 registry。
- 不修改 workflow。
- 不修改 harness。
- 不修改 pipeline。
- 不新增 skill、harness、plugin、workflow stage 或 automation。
- 不提交、不 push、不 PR。
- 不删除、不归档。
- 不写长期记忆。
