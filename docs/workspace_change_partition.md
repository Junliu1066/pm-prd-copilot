# 工作区变更分区审查

- 日期：2026-05-01
- 快照命令：`git status --short`
- 当前快照：73 项
- 状态分布：`28 M`、`4 D`、`41 ??`
- 目的：把当前混合工作区拆成可审核、可回滚、可分批处理的清单。
- 规则：本文件只是审计地图，不批准清理、删除、恢复、归档、staging、commit、push、PR、candidate 转 stable、长期记忆写入或项目归档。

## Root 分布

| Root | 当前项数 |
|---|---:|
| `projects` | 44 |
| `docs` | 17 |
| `pm-prd-copilot` | 6 |
| `ai-intel` | 1 |
| `memory-cache` | 1 |
| `prd_pm_2026_playbook.md` | 1 |
| `prd_skill_kit_2026.zip` | 1 |
| `prd_template_2026.md` | 1 |
| `skill_suite_overview.md` | 1 |

## 当前总体结论

| 分区 | 当前内容 | 默认处理 | 是否需要你拍板 |
|---|---|---|---|
| 已收口稳定治理 | A1-A4、B1-B5 主干、D1-D3、任务漂移规则、agentic delivery 输出边界 | 保持，不再混入项目产物 | 后续新增长期规则仍需要 |
| workspace 地图 | `docs/workspace_change_partition.md` | 本轮刷新并单独处理 | 本次已按批准执行 |
| proposal 临时材料 | `docs/proposals/*_staging_list.md`、`*_commit_review.md`、旧计划材料 | 暂缓，不进稳定治理文档 | 需要决定归档或 30 天后删除候选 |
| proposal 决策候选 | `b5_automation_ai_intel_candidate_review.md`、`b5b_registry_candidate_alignment_review.md`、`e_root_archive_cleanup_review.md` 等 | 先留作候选，不混提交 | 需要逐项确认是否保留 |
| skill patch 候选 | `pm-prd-copilot/proposals/skill-patches/*` | 保持候选，不自动改 skill | 需要逐条确认是否采纳或归档 |
| AI raw 证据 | `ai-intel/raw/2026-04-30/` | 本地复核证据，不进默认提交 | 需要确认保留、归档或 30 天后删除候选 |
| 项目偏好缓存 | `memory-cache/projects/fitness-app-mvp/*` | 项目内保留，归档前处置 | 需要 closeout 前逐条对齐 |
| 项目产物 C 批 | `projects/*` 生成物、closeout、prototype、runs、新项目目录 | 逐项目审查，不混入治理提交 | 需要 |
| E 批 root/archive | 4 个 root 删除项、`docs/archive/` | 只审查，不提交删除或 archive | 需要逐条确认 |

## 已完成后不再列为待处理的事项

| 事项 | 当前状态 |
|---|---|
| B4 错误报告证据 | 已提交 `0e70b36 Record May 1 governance error report`，当前不再有 `docs/error_reports/*` 待提交。 |
| `agent.md` 禁止任务漂移规则 | 已提交 `1e74cd0 Tighten task drift guardrails`。 |
| agentic delivery 输出边界 | 已提交 `b4d1afe Refine agentic delivery output boundaries`。 |
| C2 / Harness-Skill 审查记录 | 已提交 `ecd9c3f Record project and harness skill boundary reviews`。 |

## 当前剩余项明细

### 1. Proposal 临时材料

当前未跟踪 proposal：

```text
docs/proposals/b2_proposal_audit_commit_review.md
docs/proposals/b3_teaching_steward_commit_review.md
docs/proposals/b3_teaching_steward_content_review_plan.md
docs/proposals/b3_teaching_steward_staging_list.md
docs/proposals/b4_error_reports_commit_review.md
docs/proposals/b4_error_reports_staging_list.md
docs/proposals/b5_automation_ai_intel_candidate_review.md
docs/proposals/b5a_github_workflows_commit_review.md
docs/proposals/b5a_github_workflows_staging_list.md
docs/proposals/b5b_candidate_marketplace_staging_list.md
docs/proposals/b5b_registry_candidate_alignment_review.md
docs/proposals/b5c_ai_intel_commit_review.md
docs/proposals/b5c_ai_intel_staging_list.md
docs/proposals/d1_candidate_plugin_commit_review.md
docs/proposals/e_root_archive_cleanup_review.md
```

| 类型 | 文件 | 建议 | 原因 |
|---|---|---|---|
| 临时 commit / staging 材料 | `b2_*commit_review.md`、`b3_*staging_list.md`、`b3_*commit_review.md`、`b4_*`、`b5a_*`、`b5b_candidate_marketplace_staging_list.md`、`b5c_*`、`d1_*commit_review.md` | 暂缓，后续归档或删除候选 | 这些只服务一次提交或 staging，不是长期规则。 |
| 旧计划材料 | `b3_teaching_steward_content_review_plan.md` | 暂缓 | 已被实际审查和后续提交覆盖。 |
| 候选决策记录 | `b5_automation_ai_intel_candidate_review.md`、`b5b_registry_candidate_alignment_review.md` | 暂缓 | 内容有审计价值，但范围较宽，需要单独确认是否保留。 |
| E 批审查记录 | `e_root_archive_cleanup_review.md` | 暂缓 | root 删除和 archive 策略未逐条批准前，不应提交。 |

推荐动作：先不提交这些 proposal。等 root/archive、automation、candidate marketplace 是否保留的功能决策明确后，再做一次“proposal 留存 / 归档 / 30 天后删除候选”清单。

### 2. Skill Patch 候选

当前未跟踪：

```text
pm-prd-copilot/proposals/skill-patches/skill-update-20260424T000000Z.json
pm-prd-copilot/proposals/skill-patches/skill-update-20260424T000000Z.md
pm-prd-copilot/proposals/skill-patches/skill-update-20260424T041400Z.json
pm-prd-copilot/proposals/skill-patches/skill-update-20260424T041400Z.md
pm-prd-copilot/proposals/skill-patches/skill-update-20260425T000000Z.json
pm-prd-copilot/proposals/skill-patches/skill-update-20260425T000000Z.md
```

判断：

- 这是 skill 更新候选，不是已批准 stable skill 修改。
- 不能自动应用，也不能和项目产物混提交。
- 如果保留，应作为“skill 变更候选证据”单独审查。

建议：暂缓。后续按“如无必要，不增 skill”原则逐条判断：采纳、拒绝、归档候选或 30 天后删除候选。

### 3. AI Raw 证据

当前未跟踪：

```text
ai-intel/raw/2026-04-30/
```

判断：

- raw HTML / JSON 只适合作为本地复核证据。
- 不应默认提交。
- 已提交的 AI intel evidence 应优先使用 daily / events / logs，而不是 raw。

建议：暂缓，不提交。后续可列为归档候选或 30 天后删除候选。

### 4. Memory Cache

当前未跟踪：

```text
memory-cache/
```

判断：

- 当前主要关联 `fitness-app-mvp` 项目偏好。
- 属于项目内连续性材料，不是长期记忆。
- 不能自动跨项目复用，不能自动清空，不能自动写入长期记忆。

建议：不提交、不清空。等 `fitness-app-mvp` closeout / 归档前逐条对齐。

### 5. 项目产物 C 批

当前项目变更集中在：

- `projects/demo-project/`
- `projects/fitness-app-mvp/`
- `projects/_archives/`
- `projects/ai-collaboration-efficiency-platform/`
- `projects/graduation-defense-agent/`
- `projects/jiaxiaoqian-ai-invest-research/`
- `projects/prompt-optimization-workbench/`
- `projects/santoip-ai-brand-video/`
- `projects/taxi-hailing-prd-test/`
- `projects/temp-generated-project/`

建议顺序：

1. `demo-project`：作为测试 fixture，先决定哪些 run 输出是最小可提交证据，哪些可重建。
2. `fitness-app-mvp`：保持 active 项目产物，不在治理线程讨论产品功能。
3. `taxi-hailing-prd-test`：作为 0-1 PRD 样例候选，是否脱敏成 golden sample 需要单独批准。
4. 其它项目：逐个判断 active、closeout candidate、archive candidate。

本轮不提交任何 `projects/*`。

### 6. E 批 Root / Archive

当前 root 删除项：

| 文件 | 当前判断 | 推荐 |
|---|---|---|
| `prd_pm_2026_playbook.md` | 有 canonical copy 和 archive copy，root copy 冗余 | 后续逐条确认后接受 root 删除 |
| `prd_template_2026.md` | 有 canonical copy 和 archive copy，root copy 冗余 | 后续逐条确认后接受 root 删除 |
| `prd_skill_kit_2026.zip` | 有 archive copy；二进制包不应在 root | 不恢复 root，后续列入 30 天后删除候选 |
| `skill_suite_overview.md` | 有 archive copy；可能有内容提炼价值 | 不恢复 root，后续审内容是否并入 docs |

当前 archive 文件：

```text
docs/archive/README.md
docs/archive/notes/答辩.md
docs/archive/root-files/Remod开发.md
docs/archive/root-files/prd_pm_2026_playbook.md
docs/archive/root-files/prd_skill_kit_2026.zip
docs/archive/root-files/prd_template_2026.md
docs/archive/root-files/skill_suite_overview.md
```

建议：E 批继续暂缓。不提交 root 删除状态，不提交 archive，直到你逐项批准。

## 需要你拍板的治理功能决策

| 决策 | 选项 A | 选项 B | 我的建议 |
|---|---|---|---|
| proposal 临时材料如何处理 | 暂缓，后续归档或 30 天后删除候选 | 现在全部提交 | 选 A。提交临时材料会污染长期治理文档。 |
| skill patch 候选如何处理 | 逐条审查，不自动采纳 | 直接应用或提交 | 选 A。符合“如无必要，不增 skill”。 |
| AI raw 是否提交 | 不提交，只本地保留 | 提交 raw 证据 | 选 A。raw 噪音大，长期追溯用 daily/events/logs 更稳。 |
| memory-cache 是否提交 | 不提交，项目内保留 | 提交到仓库 | 选 A。避免项目偏好污染长期记忆。 |
| C 批项目产物先处理谁 | 先 demo，再 fitness，再其它项目 | 一次性处理全部项目 | 选 A。小批次更稳，避免任务漂移。 |
| root 删除状态是否接受 | 暂缓，逐条确认 | 现在接受 4 个删除 | 选 A。删除状态必须和 canonical/archive 证据逐条对齐。 |
| docs/archive 是否提交 | 暂缓 | 现在提交 archive | 选 A。先定 archive 策略，再提交。 |

## 推荐下一步顺序

1. 提交本工作区分区地图更新。
2. 进入 C 批 demo-project 最小 fixture 审查。
3. 再处理 `fitness-app-mvp` 项目产物和偏好缓存处置边界。
4. 单独审 skill patch 候选。
5. 最后处理 E 批 root/archive。

## 本轮明确不批准

- 不删除、恢复、移动任何文件。
- 不提交 root 删除状态。
- 不提交 `docs/archive/`。
- 不提交 `memory-cache/`。
- 不提交 `projects/*`。
- 不提交 `ai-intel/raw/*`。
- 不自动采纳 skill patch。
- 不把 candidate 转 stable。
- 不新增 skill / harness / workflow / plugin。
- 不写长期记忆。
- 不 push / PR。
