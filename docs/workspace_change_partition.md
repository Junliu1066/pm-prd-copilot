# 工作区变更分区审查

- 日期：2026-05-04
- 快照命令：`git status --short`
- 当前快照：38 项，全部为未跟踪文件 / 目录。
- 当前 tracked 修改：0 项。
- 目的：把剩余未跟踪材料拆成可审核、可回滚、可分批处理的清单，避免项目产物和临时材料污染稳定治理核心。
- 规则：本文件只是审计地图，不批准删除、恢复、移动、归档、staging、commit、push、PR、candidate 转 stable、长期记忆写入或项目归档。

## 当前结论

前面稳定核心和主要项目证据已经提交完毕。现在剩余工作区不再是代码或稳定架构修改，而是四类本地材料：

1. 项目目录和项目产物。
2. `memory-cache/` 项目偏好缓存。
3. `ai-intel/raw/` raw 网页证据。
4. 临时 proposal 和额外 archive 历史材料。

我的建议是：**继续不提交这些本体，只保留生命周期记录；到期或归档前再用精确清单处理。**

## Root 分布

| Root | 当前项数 | 默认处理 |
|---|---:|---|
| `projects/` | 15 | 项目产物候选区，不混入稳定治理核心。 |
| `docs/proposals/` | 19 | 临时审计 / staging / commit 材料，已列 30 天候选。 |
| `ai-intel/raw/` | 1 | raw 本地证据，不提交，30 天后复核候选。 |
| `memory-cache/` | 1 | 项目偏好缓存，不提交、不清空。 |
| `docs/archive/` 额外材料 | 2 | 未审历史材料，不提交、不删除。 |

## 剩余未跟踪项精确分区

### 1. 临时 Proposal

当前剩余 19 个临时 proposal 文件，已在 `docs/proposals/remaining_proposal_audit_materials_disposition.md` 中列为生命周期候选。

默认动作：

- 不提交本体。
- 不移动到 archive。
- 不现在删除。
- 最早 2026-06-03 后，按精确清单二次审批删除。

### 2. Project Artifacts

当前剩余项目目录：

```text
projects/_archives/
projects/a-share-ai-quant-strategy-platform/
projects/ai-collaboration-efficiency-platform/
projects/demo-project/prototype/
projects/fitness-app-mvp/closeout/
projects/fitness-app-mvp/prototype/
projects/fitness-app-mvp/runs/plan-execution-preview-20260425/
projects/fitness-app-mvp/runs/prototype-preview-20260424/
projects/geo-service-prd/
projects/graduation-defense-agent/
projects/jiaxiaoqian-ai-invest-research/
projects/prompt-optimization-workbench/
projects/santoip-ai-brand-video/
projects/taxi-hailing-prd-test/
projects/temp-generated-project/
```

默认动作：

- 不整包提交 `projects/*`。
- 不移动到 `_archives`。
- 不删除项目。
- 后续按项目 closeout / archive / 30 天删除候选逐个处理。

当前判断见 `docs/proposals/projects_lifecycle_inventory_review.md`。

新增 `projects/geo-service-prd/` 当前只作为小体量 PRD / 原型层候选样例保留，不提交、不归档、不提炼 stable。

### 3. Memory Cache

当前剩余：

```text
memory-cache/
```

默认动作：

- 不提交。
- 不清空。
- 不跨项目复用。
- 不写长期记忆。
- 等 `fitness-app-mvp` 归档前再按 `preference-memory-disposition` 逐条处置。

当前边界见 `docs/proposals/preference_cache_boundary_review.md`。

### 4. AI Raw

当前剩余：

```text
ai-intel/raw/2026-04-30/
```

默认动作：

- 不提交 raw。
- 不更新 decision docs。
- 不让 AI 情报自动改变治理架构。
- 最早 2026-06-02 后，按精确清单二次审批删除。

当前边界见 `docs/proposals/ai_intel_raw_lifecycle_disposition.md`。

### 5. Extra Archive Materials

当前剩余：

```text
docs/archive/notes/
docs/archive/root-files/Remod开发.md
```

默认动作：

- 不提交原文。
- 不移动。
- 不删除。
- `答辩.md` 随 `graduation-defense-agent` closeout 再判断。
- `Remod开发.md` 保留为 30 天后删除候选。

当前边界见 `docs/proposals/archive_notes_lifecycle_disposition.md`。

## 需要你后续拍板的功能性事项

| 决策 | 我的建议 | 效果 |
|---|---|---|
| 是否提交剩余项目目录 | 暂不提交 | 保持稳定治理核心干净，项目继续留在候选区。 |
| 是否清空 `memory-cache/` | 不清空 | 保留 fitness 项目连续性，避免误删偏好上下文。 |
| 是否提交 `ai-intel/raw/` | 不提交 | 避免 raw HTML 污染仓库，保留 daily / events / logs 作为结构化证据。 |
| 是否删除临时 proposal | 2026-06-03 后再审批 | 避免过早丢失审计材料，同时给瘦身明确时间点。 |
| 是否处理 archive 额外材料 | 暂缓 | 避免项目原始输入或旧治理笔记误入稳定 archive。 |
| 是否 push / PR | 等本地收口完全稳定后再决定 | 防止把本地候选材料误推到远端。 |

## 最快后续顺序

1. 本文件作为当前工作区地图提交。
2. 不再提交临时 proposal 本体。
3. 保留剩余未跟踪项到对应生命周期复核日。
4. 如果需要继续瘦身，下一步只能做“删除候选到期前的精确审批清单”，不能直接删除。

## 当前禁止动作

- 不 `git add .`。
- 不删除、恢复、移动任何剩余未跟踪项。
- 不提交 `projects/*`、`memory-cache/*`、`ai-intel/raw/*`、额外 `docs/archive/*`。
- 不写长期记忆。
- 不新增 skill / harness / workflow / plugin。
- 不 push / PR。

## 结论

当前工作区已经从“混合变更”收口到“38 个未跟踪候选项”。这些项都不应继续进入稳定治理提交。后续核心不是继续写更多规则，而是按生命周期到期复核：项目归项目，缓存归缓存，raw 归 raw，临时 proposal 到期再删。
