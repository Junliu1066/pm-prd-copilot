# C1 Demo / Fitness 项目产物审查报告

- 日期：2026-04-30
- 状态：审查报告，不批准 staging、commit、push、PR、归档、删除、恢复、长期记忆写入或 root 删除状态提交。
- 范围：`projects/demo-project/`、`projects/fitness-app-mvp/`、`memory-cache/projects/fitness-app-mvp/`
- 已确认前提：root 删除项继续暂缓；C 批先审 demo + fitness；`memory-cache/` 继续项目内保留。

## 结论

C1 不建议提交任何项目产物，也不建议清空缓存或归档项目。当前最稳的处理是：

1. `demo-project` 保留为治理 / 回归测试 fixture。
2. `fitness-app-mvp` 保持 active / closeout candidate，不进入归档。
3. `memory-cache/projects/fitness-app-mvp/` 继续项目内保留，不提交、不清空、不写长期记忆。
4. 两个项目的 run 输出、prototype、closeout 报告都只作为项目证据，不混入稳定治理提交。
5. root 删除项继续暂缓，不在 C1 处理。

## 当前证据

| 项目 | 当前变更 | 关键证据 | 初步判断 |
|---|---:|---|---|
| `demo-project` | `19 M`、`5 ??` | `project_state.json` 标记 `pipeline_assumption_overrides`，备注为治理 rerun 测试覆盖，不是真实产品审批；closeout 有 42 个文件盘点；final PRD 只有 16 行 | 保留为测试 fixture，不作为真实项目样例提交 |
| `fitness-app-mvp` | `8 M`、`4 ??`，另有 `memory-cache/` | `project_state.json` 显示项目偏好缓存 active；closeout 有 61 个文件盘点；final PRD / story 只有标题；analysis / prototype 产物较多 | 保持 active / closeout candidate，不做归档和长期化 |

## Demo Project 审查

| 资产类型 | 当前内容 | 建议 | 优势 | 劣势 / 风险 |
|---|---|---|---|---|
| 测试 fixture | `project_state.json`、`pipeline-latest`、governed rerun 结果 | 项目内保留，不提交本轮变更 | 保留治理测试现场，方便后续验证 pipeline / harness | 继续留在工作区会显得混乱 |
| 生成稿 | `02_prd.generated.*`、`03_user_stories.generated.*`、风险、埋点等 | 项目内保留，等经验提取后再判断归档 | 可追溯 PRD 退化和修复效果 | 不能作为稳定模板或 golden sample |
| final 人工稿 | `02_prd.final.md`、`03_user_stories.final.md` | 保留到经验沉淀完成 | 能看到人工修订方向 | 内容很短，不适合作为完整 PRD 样例 |
| prototype PNG / UI style | `prototype/page_png/*`、`ui_style_direction.*` | 项目内保留，不进稳定架构 | 可作为后期原型链路证据 | 不能变成默认 UI 风格或长期规则 |
| closeout 五件套 | `closeout/*` | 作为审核材料保留，暂不提交项目产物 | 已明确清理前审批边界 | 如果直接提交，会把项目证据混进治理核心 |
| meta / run 输出 | `*.meta.json`、`runs/*` | 归档后再考虑清理候选 | 能减少长期噪音 | 现在清理会丢失修复现场证据 |

### Demo 我的建议

保留 `demo-project` 为测试 fixture，但不要把当前项目变更提交进稳定核心。后续如果要收口，先单独定义“demo fixture 最小保留集”，再决定哪些 run 输出可重建、哪些可以归档。

## Fitness App MVP 审查

| 资产类型 | 当前内容 | 建议 | 优势 | 劣势 / 风险 |
|---|---|---|---|---|
| 项目状态 | `project_state.json` 显示 `preference_cache.status: active` | 保持 active / closeout candidate | 保留真实项目连续性 | 工作区继续有项目状态变更 |
| 分析产物 | `analysis/*.json`、`prd_analysis_suite_summary.md` | 项目内保留，暂不提交 | 有真实需求分析价值 | 不应直接反哺长期规则 |
| final 人工稿 | `02_prd.final.md`、`03_user_stories.final.md` 只有标题 | 不作为 golden sample | 避免把空 final 固化为样例 | 需要后续补足或明确废弃 |
| prototype | `prototype/product_flow.md`、`prototype_preview.*`、`reference_analysis.json` | 项目内保留 | 可作为 PRD -> 原型链路证据 | 不应变成默认 UI / UX 产物标准 |
| run 输出 | `runs/governance-baseline`、`prd-analysis-suite`、`prototype-preview`、`plan-execution-preview` | 项目内保留，后续挑选最小审计证据 | 保留完整演化链 | 全部提交会噪音很大 |
| closeout 五件套 | `closeout/*` | 作为审核材料保留，暂不归档 | 已列出清理前审批项 | 还不能代表项目已结束 |

### Fitness 我的建议

`fitness-app-mvp` 不要现在归档，也不要提交项目产物。它更像真实项目 + 过程样例，应该先保留 active 状态，后续由你决定是否继续完善 PRD / 原型，或进入 closeout。

## 项目偏好缓存审查

当前缓存文件：

```text
memory-cache/projects/fitness-app-mvp/cache-20260424T000000+0800/approved_preferences.md
memory-cache/projects/fitness-app-mvp/cache-20260424T000000+0800/candidate_preferences.md
memory-cache/projects/fitness-app-mvp/cache-20260424T000000+0800/manifest.json
memory-cache/projects/fitness-app-mvp/cache-20260424T000000+0800/source_trace.json
memory-cache/projects/fitness-app-mvp/current.json
```

| 选项 | 优势 | 劣势 / 风险 | 我的建议 |
|---|---|---|---|
| 项目内保留 | 保留 fitness 项目连续性；不污染长期记忆 | 工作区继续有未跟踪缓存 | 推荐 |
| 提炼长期记忆 | 能沉淀真实偏好 | 极易把项目偏好误写成全局规则 | 不推荐，除非逐条审批 |
| 现在清空 | 工作区更干净 | 丢失项目上下文，违背归档前对齐原则 | 不推荐 |

处理边界：

- 不提交 `memory-cache/`。
- 不清空 active cache。
- 不跨项目复用。
- 不写长期记忆。
- 归档前再逐条对齐：保留为项目档案、清除 active 指针、或提议单条进入长期记忆。

## 已批准的功能决策

这里列的是“功能 / 能力是否继续保留和怎么使用”的决策，不是简单文件清理决策。你已确认按我的建议执行；文件提交、归档、删除会在功能方向确认后再拆成单独清单。

| 功能决策 | 已批准方向 | 预期效果 | 后续动作 |
|---|---|---|---|
| `demo-project` 是否继续承担治理回归测试能力 | 继续作为 regression / harness fixture | 保留 governed pipeline、harness check-only、eval 和随机审计的测试现场 | 后续定义最小 fixture 能力集 |
| `demo-project` 是否需要定义“最小 fixture 能力集” | 定义最小保留集 | 明确哪些文件支撑测试能力，减少 run 输出噪音 | 单独产出 demo fixture 最小保留方案 |
| `fitness-app-mvp` 是否继续作为真实项目连续工作样例 | 继续 active，后续可补 PRD / 原型 | 保留真实项目连续性，不把未完成 final 误归档 | 后续决定是否继续完善 PRD / 原型 |
| fitness 项目偏好缓存是否继续服务项目连续性 | 继续项目内启用 | 保留项目上下文，不跨项目复用，不写长期记忆 | 归档前再做逐条处置 |
| PRD -> 原型链路是否把这两个项目作为观察样例 | 只作为观察样例 | 保留原型链路证据，但不升级为稳定样例 | 后续选择更成熟样例再稳定化 |
| closeout 功能是否继续覆盖所有项目 | 继续作为归档前必做流程 | 归档前强制总结、反思、架构反哺和清理候选 | 后续所有项目归档前继续 closeout |
| 项目 run 输出是否要进入“最小审计证据”能力 | 建立最小审计证据规则 | 保留可追溯性，同时降低 run 输出噪音 | 单独制定 run 输出最小审计证据规则 |

## 文件处理只是后续动作

功能决策确认后，才进入文件层面的处理：

| 文件动作 | 当前默认 | 原因 |
|---|---|---|
| 项目产物提交 | 暂缓 | 先确认 demo / fitness 的功能身份，避免项目产物污染稳定核心。 |
| prototype 提交 | 暂缓 | 原型链路可以观察，但不直接转成稳定样例。 |
| closeout 五件套提交 | 暂缓 | closeout 是审核材料，不等于项目已归档。 |
| `memory-cache/` 提交 | 不提交 | 它是项目偏好，不是长期记忆。 |
| root 删除项 | 继续暂缓 | root/archive 属于 E 批，不在 C1 功能决策里处理。 |

## 后续执行建议

建议下一步不要提交项目产物，而是做两个更小的后续计划：

1. `demo-project` 最小 fixture 定义：明确哪些文件是 regression / harness 必须保留，哪些 run 输出可重建。
2. `fitness-app-mvp` 项目状态决策：你决定继续推进 PRD / 原型，还是进入正式 closeout。

## 本轮不批准

- 不 staging / commit 项目文件。
- 不归档、删除、移动项目目录。
- 不提交或清空 `memory-cache/`。
- 不把项目偏好写入长期记忆。
- 不提交 `docs/archive/`。
- 不接受 root 删除状态。
- 不新增 skill、harness、workflow、plugin 或长期规则。
