# C7 Fitness 项目产物与偏好缓存边界审查

- 日期：2026-05-02
- 状态：审查报告，不批准 staging、commit、push、PR、归档、删除、清空缓存、长期记忆写入或 stable 规则变更。
- 范围：`projects/fitness-app-mvp/`、`memory-cache/projects/fitness-app-mvp/`
- 主线任务：判断 fitness 项目产物和项目偏好缓存如何处理，避免真实项目过程材料污染稳定治理核心。

## 结论

`fitness-app-mvp` 应继续作为 active / closeout candidate 项目内保留，暂不提交项目产物，暂不归档，暂不清空 `memory-cache/`。

核心原因：

- `project_state.json` 显示项目偏好缓存仍是 `active`，说明项目上下文还在使用。
- `02_prd.final.md` 和 `03_user_stories.final.md` 目前各只有 2 行，不能作为 golden sample。
- `02_prd.generated.md` 仍能搜到导出、Excel、异步导出、商家办公等旧场景污染，不能直接当作高质量 PRD 基准。
- `memory-cache` 已明确写了 `scope: project_only`、禁止跨项目复用、长期记忆需用户批准，当前边界是对的。
- prototype 和 plan-execution run 有项目过程价值，但不适合进入稳定治理核心。

## 当前状态

| 区域 | 当前状态 | 判断 |
|---|---|---|
| `analysis/*.json` 和分析总结 | 5 个 analysis 文件有修改 | 有项目分析价值，但仍待项目审核，不进入稳定治理提交。 |
| `project_state.json` | 指向 `plan-execution-preview-20260425`，偏好缓存 active | 应项目内保留，不提交为长期规则。 |
| `runs/prd-analysis-suite-20260423/*` | 2 个 tracked run 文件有修改 | 只作为项目运行证据，不单独提交。 |
| `runs/prototype-preview-20260424/` | 未跟踪 | 项目原型预览证据，不进入稳定核心。 |
| `runs/plan-execution-preview-20260425/` | 未跟踪 | 计划执行预览证据，有价值但应和项目状态一起审。 |
| `prototype/` | 未跟踪，含流程文档、SVG、PNG、参考分析 | 项目原型过程产物，不转成长期 UI / UX 规则。 |
| `closeout/` | 未跟踪五件套 | 只能作为归档前审核材料，不代表项目已归档。 |
| `memory-cache/` | 未跟踪项目偏好缓存 | 项目内保留，不提交、不清空、不跨项目复用。 |

## 功能效果

如果按推荐方案处理，可以达到这些效果：

- 保留 fitness 项目的连续工作上下文，后续还能继续补 PRD、原型或开发文档。
- 防止“食物热量拍摄”“训练计划执行”“中国市场默认”“暗黑机械风”等项目偏好被误写成长期规则。
- 保留 prototype preview 和 plan-execution preview 作为原型链路观察样例，但不把它们升级为稳定样例。
- 等项目真正 closeout 时，再做偏好缓存逐条对齐：保留为项目档案、清除 active 指针、或经你批准提炼成长期记忆。

它不能达到这些效果：

- 不能让当前工作区立刻干净。
- 不能把 fitness 变成 PRD golden sample。
- 不能证明项目偏好缓存机制已经可以全自动处理。
- 不能替代后续你对项目是否继续推进的决策。

## 架构影响

正向影响：

- 继续验证项目级偏好缓存的边界：项目内有效、禁止跨项目、长期记忆逐条批准。
- 继续验证 closeout 流程：项目归档前先总结、反思、反哺候选和清理候选。
- 继续验证 PRD -> 原型链路：先预览、人工反馈、再考虑完整原型。

风险：

- 未跟踪项目文件继续留在工作区，会增加状态噪音。
- 如果后续误提交 `memory-cache/`，项目偏好可能被当成稳定长期规则。
- 如果现在提交 fitness generated / analysis / runs，可能把未完成或被旧场景污染的内容固化。
- 如果现在清空缓存，会丢失项目连续性，也违背归档前对齐原则。

## 偏好缓存边界

当前 `memory-cache/projects/fitness-app-mvp/current.json` 的边界是正确的：

- `scope`: `project_only`
- `candidate_requires_approval`: `true`
- `cross_project_reuse_allowed`: `false`
- `long_term_memory_requires_user_approval`: `true`
- `archive_alignment_required`: `true`
- `clear_after_project_archive_alignment`: `true`

当前已批准项目偏好应继续只在 fitness 项目内有效，例如：

- 中国市场默认只用于本 fitness 项目的竞品 / 市场分析。
- 原型先预览再完整展开，只用于本 fitness 项目的原型流程。
- 暗黑机械、极简、青绿色高亮等风格只用于本 fitness 项目的原型预览。
- 训练计划执行、手动开始下一组、改计划等产品行为只属于 fitness 项目。

不应进入长期记忆的内容：

- 任何具体 fitness 产品功能。
- 任何具体 UI 风格。
- 中国市场默认，除非未来多项目反复证明且你单独批准。
- 食物热量拍摄、组间歇计时、训练计划执行等项目业务判断。

可作为长期规则候选但仍需后续单独审批的内容：

- 项目偏好缓存必须项目内隔离。
- 原型预览要直接可见，并做基础视觉 QA。
- 完整原型前先预览，等待人工反馈。

这些候选目前不要在本轮转 stable，因为它们已经有部分稳定规则覆盖，继续观察更稳。

## 处理选项

| 选项 | 效果 | 优势 | 劣势 / 风险 | 我的建议 |
|---|---|---|---|---|
| A. 现在提交全部 fitness 项目产物 | 工作区更干净，项目现场完整入库 | 信息完整 | 把 active 项目、缓存、run 输出和原型混在一起，长期噪音大 | 不选 |
| B. 只提交 closeout 五件套 | 保留归档前审核材料 | 可追溯 | 项目仍 active，容易被误解为已归档 | 暂缓 |
| C. 只提交 memory-cache | 保留项目偏好证据 | 上下文完整 | 极易被误认为长期记忆，风险高 | 不选 |
| D. 项目内保留，暂不提交 | 保留连续性，等待项目或归档节点处理 | 最稳，不污染稳定核心 | 工作区继续有噪音 | 推荐 |
| E. 清空或删除 memory-cache | 工作区更干净 | 噪音少 | 丢失项目上下文，违背归档前对齐 | 不选 |

## 需要你后续拍板

| 拍板项 | 我的建议 | 不同选择的结果 |
|---|---|---|
| fitness 是否继续 active | 继续 active / closeout candidate | 继续 active 能保留后续完善空间；进入归档会提前结束项目。 |
| 是否提交 fitness closeout 五件套 | 暂缓 | 提交会保留审核证据；暂缓能避免误判项目已归档。 |
| 是否提交 `memory-cache/` | 不提交 | 提交会增加长期记忆误用风险；不提交能保持项目偏好隔离。 |
| 是否清空项目偏好缓存 | 不清空 | 清空能减少噪音；不清空能保留项目连续性，等归档前对齐。 |
| 是否把中国市场默认提炼为长期规则 | 不提炼 | 提炼会影响所有项目市场判断；不提炼更符合按项目判断。 |
| 是否把 prototype / plan-execution 作为稳定原型样例 | 暂不稳定化 | 稳定化会过早绑定 fitness；观察样例能继续暴露问题。 |
| 是否恢复或重生成 fitness PRD | 后续单独处理 | 现在处理会偏离治理收口；后续处理能先明确项目是否继续推进。 |

## 后续建议

推荐下一步不要提交 fitness 项目产物，而是按这个顺序处理：

1. 先输出 “fitness active 项目保留边界清单”，只列哪些文件必须项目内保留、哪些是可重建 run 输出。
2. 等你决定 fitness 项目是否继续推进，再选择补 PRD / 原型或进入正式 closeout。
3. 归档前再逐条处理 `memory-cache`：项目档案保留、清除 active 指针、长期记忆候选。

## 本轮不做

- 不 staging / commit `projects/fitness-app-mvp/*`。
- 不 staging / commit `memory-cache/*`。
- 不清空项目偏好缓存。
- 不把项目偏好写入长期记忆。
- 不归档、删除、移动项目目录。
- 不新增 skill、harness、workflow、plugin 或长期规则。
