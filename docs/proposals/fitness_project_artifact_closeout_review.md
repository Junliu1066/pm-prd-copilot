# Fitness 项目产物收口审查报告

- 日期：2026-05-04
- 项目：`fitness-app-mvp`
- 主线任务：判断 fitness 项目产物如何收口，避免项目材料污染稳定治理核心。
- 本报告性质：项目产物审查和拍板材料，不批准 staging、commit、归档、删除、清空缓存或长期记忆写入。

## 结论

`fitness-app-mvp` 不是稳定治理核心，而是一个真实项目证据包。当前它仍有 active 痕迹，也有 closeout candidate 特征：已生成 PRD、分析包、原型预览、运行证据、closeout 五件套和项目偏好缓存，但项目偏好还未归档前对齐，项目产物也未拆分提交。

我的建议是：**先不归档、不删除、不提交 memory-cache；先把 fitness 作为单项目 evidence batch 处理。** 后续只在你确认后，提交一组最小项目证据，其他生成过程文件进入归档候选或 30 天后删除候选。

## 当前文件状态

| 类别 | 路径 / 范围 | 当前状态 | 判断 |
|---|---|---|---|
| 已跟踪分析结果 | `projects/fitness-app-mvp/analysis/*.json`、`analysis/prd_analysis_suite_summary.md` | 8 个 tracked 修改的一部分 | 可作为项目证据，但不应混入治理核心。 |
| 项目状态 | `projects/fitness-app-mvp/project_state.json` | tracked 修改 | 建议保留项目内，记录 last run 和 preference cache 指针。 |
| 运行证据 | `projects/fitness-app-mvp/runs/prd-analysis-suite-20260423/*` | tracked 修改 | 可保留为分析链路证据，后续可进入项目证据批次。 |
| 原型预览 | `projects/fitness-app-mvp/prototype/` | 未跟踪 | 只属于项目产物，先不提交到治理核心。 |
| closeout 五件套 | `projects/fitness-app-mvp/closeout/` | 未跟踪 | 审核材料，不等于批准归档。 |
| 追加运行目录 | `runs/plan-execution-preview-20260425/`、`runs/prototype-preview-20260424/` | 未跟踪 | 过程证据，建议暂缓提交，等项目是否收口后再决定。 |
| 项目偏好缓存 | `memory-cache/projects/fitness-app-mvp/` | 未跟踪 | 项目内保留，不提交、不清空、不写长期记忆。 |

## 项目内容风险

| 风险 | 证据 | 控制建议 |
|---|---|---|
| 项目偏好被误写成长期偏好 | `memory-cache/projects/fitness-app-mvp/...` 中有 China market、prototype style、training plan 等偏好 | 继续项目内隔离；归档前逐条确认是否保留、清除或提议长期化。 |
| 项目功能细节干扰治理主线 | fitness 包含食物热量、组间歇、训练计划、原型风格等业务内容 | 本轮只判断文件生命周期，不讨论产品优先级。 |
| generated / final 产物质量不稳定 | closeout 报告显示 final PRD 不是 golden sample 候选 | 不升级为黄金样例；只作为反面或过程证据。 |
| 原型和 run 产物体积继续膨胀 | prototype PNG、多个 runs 目录、closeout 五件套都存在 | 项目 evidence batch 和清理候选分开处理。 |
| 原始输入可能敏感 | `00_raw_input.md` 被 closeout 标记为 sensitive input | 不公开、不外发；归档或脱敏需你批准。 |

## 推荐的处理分层

### A. 可提交为项目证据候选

只在你批准后，建议作为一个单独 commit，不混入治理核心：

- `projects/fitness-app-mvp/project_state.json`
- `projects/fitness-app-mvp/analysis/competitor_gap.json`
- `projects/fitness-app-mvp/analysis/mvp_scope.json`
- `projects/fitness-app-mvp/analysis/prd_analysis_suite_summary.md`
- `projects/fitness-app-mvp/analysis/scenario_ranking.json`
- `projects/fitness-app-mvp/analysis/user_universe.json`
- `projects/fitness-app-mvp/runs/prd-analysis-suite-20260423/harness_report.json`
- `projects/fitness-app-mvp/runs/prd-analysis-suite-20260423/trace.json`

理由：这些是当前 tracked 修改，且直接说明 fitness 项目的分析链路、来源追踪和治理检查变化。提交它们可以让工作区先减少最大噪音。

### B. 项目内保留，暂不提交

- `memory-cache/projects/fitness-app-mvp/`
- `projects/fitness-app-mvp/prototype/`
- `projects/fitness-app-mvp/runs/plan-execution-preview-20260425/`
- `projects/fitness-app-mvp/runs/prototype-preview-20260424/`

理由：这些材料对项目后续有用，但要么属于偏好缓存，要么属于原型和运行过程证据。现在提交会扩大项目噪音，也可能让项目偏好或原型风格被误解为长期规则。

### C. closeout 审核材料，暂不提交

- `projects/fitness-app-mvp/closeout/closeout-report.md`
- `projects/fitness-app-mvp/closeout/architecture-feedback.md`
- `projects/fitness-app-mvp/closeout/cleanup-plan.md`
- `projects/fitness-app-mvp/closeout/preference-memory-disposition.md`
- `projects/fitness-app-mvp/closeout/manifest.json`

理由：closeout 五件套是归档前审核材料。它们有价值，但提交后容易被误解为项目已经归档。建议等你明确决定 fitness 进入 closeout 后再提交。

### D. 归档候选 / 30 天后删除候选

暂不列入本轮执行，只记录方向：

- generated meta 文件：归档后可列为 30 天后删除候选。
- 历史 run 过程证据：保留关键 manifest/trace/report 后，其余可归档候选。
- 原型中间文件：如后续已有最终确认版，可把旧预览列为归档候选。

硬删除必须满足：已归档、已过 30 天、你二次确认精确清单。

## 需要你拍板的功能性决策

| 决策 | 选项 A | 选项 B | 我的建议 | 后续效果 |
|---|---|---|---|---|
| fitness 是否继续 active | A：继续 active | B：进入 closeout candidate | 选 A，暂时 active | 保留项目连续性，不急着归档；后续仍可继续做 PRD / 原型 / 开发文档。 |
| tracked 8 个项目证据是否单独提交 | A：提交 | B：继续暂缓 | 选 A，但单独项目证据提交 | 工作区会变干净，同时不会污染稳定治理核心。 |
| closeout 五件套是否提交 | A：提交 | B：暂缓 | 选 B | 避免误判为项目已归档，等你决定项目收口后再提交。 |
| `memory-cache/` 是否提交 | A：提交 | B：项目内保留 | 选 B | 防止项目偏好污染长期记忆；归档前再逐条处置。 |
| 原型 preview 是否提交 | A：提交 | B：暂缓 | 选 B | 原型仍可本地参考，但不扩大本轮提交范围。 |
| 这些偏好是否进入长期记忆 | A：逐条提议 | B：全部拒绝长期化 | 先选 B，本轮不长期化 | 避免把 fitness 的市场、风格和训练计划偏好泛化到其他项目。 |

## 建议执行顺序

1. 先提交本审查报告，作为你后续拍板依据。
2. 你确认后，再做 `fitness-app-mvp` tracked 8 文件的 staging 清单。
3. 单独提交 tracked 8 文件，commit message 建议：`Record fitness project analysis evidence`。
4. `memory-cache/`、prototype、closeout、额外 runs 继续项目内保留。
5. 等项目归档前，再审核 `preference-memory-disposition.md`，决定清除、保留为项目档案或提议长期记忆。

## 本轮明确不做

- 不 staging。
- 不 commit。
- 不删除、移动、归档任何项目文件。
- 不提交 `memory-cache/`。
- 不清空项目偏好缓存。
- 不改 PRD、原型或产品功能。
- 不把 fitness 偏好写入长期记忆。
- 不把 fitness 产物混入治理核心。

## 验证计划

本报告生成后运行：

```bash
git diff --check -- docs/proposals/fitness_project_artifact_closeout_review.md
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
git diff --cached --name-only
```

验收标准：

- 暂存区为空。
- 只新增本报告。
- 没有项目文件写入。
- 没有 `memory-cache/` 变更。
- 没有删除、移动、归档。

## 最终建议

按长期稳定优先，fitness 不要立即归档，也不要把偏好缓存提交。最稳的下一步是：**先提交本审查报告，再单独处理 tracked 8 个项目证据文件**。这样可以清掉当前最大的 tracked 噪音，同时保留项目继续推进和未来 closeout 的空间。
