# C4 Fitness 项目产物处置审查

- 日期：2026-05-01
- 状态：项目产物处置审查报告，不批准 staging、commit、push、PR、删除、归档、清空缓存或长期记忆写入。
- 范围：`projects/fitness-app-mvp/`、`memory-cache/projects/fitness-app-mvp/`
- 主线任务：明确 fitness 项目当前仍是 active 项目，哪些材料保留在项目内，哪些暂缓，哪些只能归档前再处理。

## 主线边界

本报告只回答治理问题：

- 项目产物如何分类。
- 项目偏好缓存如何隔离。
- closeout 草案是否代表项目已完成。
- 哪些文件不应混入稳定治理提交。

本报告不回答产品业务问题：

- 不判断训练计时、食物热量、饮食记录等功能优先级。
- 不重写 fitness PRD。
- 不继续推进原型 / UI。
- 不把项目偏好提炼为长期记忆。

## 当前状态

`fitness-app-mvp` 当前应继续归类为 **active 项目**。

证据：

- `project_state.json` 记录 `preference_cache.status=active`。
- `last_run_id=plan-execution-preview-20260425`。
- `last_analysis_run_id=prd-analysis-suite-20260423`。
- `last_prototype_run_id=plan-execution-preview-20260425`。
- `02_prd.final.md` 和 `03_user_stories.final.md` 仍只有标题，不具备 final 交付物价值。
- `memory-cache/projects/fitness-app-mvp/current.json` 明确 `scope=project_only`，`cross_project_reuse_allowed=false`，`long_term_memory_requires_user_approval=true`。

## 当前变更分布

| 范围 | 当前状态 | 判断 |
|---|---|---|
| `analysis/*.json`、`analysis/*.md` | 有 5 个已修改分析文件 | 项目分析证据，项目内保留，不进稳定治理提交 |
| `project_state.json` | 已修改，指向 active cache 和最新 run | 项目生命周期指针，不进稳定治理提交 |
| `runs/prd-analysis-suite-20260423/harness_report.json`、`trace.json` | 已修改 | 历史分析 run 证据，项目内保留，后续 closeout 再处理 |
| `prototype/` | 未跟踪 | 项目原型材料，后续项目线程确认，不进治理提交 |
| `closeout/` | 未跟踪 | closeout dry-run 材料，不代表项目已归档 |
| `runs/plan-execution-preview-20260425/` | 未跟踪 | 当前 active prototype / preference run 证据，项目内保留 |
| `runs/prototype-preview-20260424/` | 未跟踪 | 历史 prototype preview run，后续归档候选 |
| `memory-cache/` | 未跟踪 | 项目偏好缓存，不提交、不清空、不跨项目复用 |

## 产物处置建议

| 产物类型 | 处理建议 | 原因 |
|---|---|---|
| 原始输入 `00_raw_input.md` | 保留到项目 closeout | 可能包含项目上下文，归档策略需人工确认 |
| generated PRD / stories / risk / tracking | 项目内保留 | 仍可作为后续 final 补齐输入 |
| final PRD / final stories | 保留但不作为已完成交付物 | 当前只有标题，不能归档或升级 golden sample |
| analysis 产物 | 项目内保留 | 有项目判断证据价值，但不能跨项目长期化 |
| prototype 产物 | 项目内保留 | 属于用户确认前的原型链路，不进入稳定治理 |
| closeout 五件套 | 保留为 dry-run 审核材料 | 不代表项目已完成，不批准归档 |
| run 输出 | 项目内保留 | active 项目仍需要追溯，不做清理 |
| memory-cache | 项目内保留 | 归档前逐条处置，不能自动长期化 |
| meta 文件 | 归档后清理候选 | 可重建，但现在不清理 |

## 项目偏好缓存边界

当前 approved preferences 包含项目内偏好，例如市场默认、预览优先原型、视觉风格、计划优先训练执行等。
这些偏好只能在 `fitness-app-mvp` 项目内使用。

处理规则：

1. 不提交 `memory-cache/`。
2. 不清空 active cache。
3. 不跨项目复用。
4. 不自动写入长期记忆。
5. 等项目 closeout / 归档前，逐条对齐：
   - 只保留为项目档案；
   - 清除 active cache 指针；
   - 提炼为长期记忆候选；
   - 拒绝长期化。

## 需要你拍板的治理功能决策

| 决策 | 选项 A | 选项 B | 选项 C | 我的建议 |
|---|---|---|---|---|
| fitness 当前项目状态 | active 项目 | closeout candidate | archive candidate | 选 A。final 文档未完成，cache 仍 active。 |
| analysis 产物是否提交 | 暂不提交，项目内保留 | 作为 C 批单独提交 | 混入稳定治理 | 选 A。它是项目证据，不是稳定架构。 |
| prototype 产物是否提交 | 暂不提交 | 单独作为原型样例提交 | 混入治理提交 | 选 A。项目原型未进入最终确认。 |
| closeout 是否生效 | 不生效，只作草案 | 立即视为归档完成 | 删除 closeout | 选 A。closeout 需要你审核后才生效。 |
| memory-cache 如何处理 | 项目内保留 | 清空 | 提炼长期记忆 | 选 A。项目未归档，长期记忆必须逐条批准。 |
| run 输出如何处理 | 项目内保留 | 立即瘦身 | 删除可重建报告 | 选 A。active 项目先不清理 run。 |

## 推荐下一步

当前治理线程不再深入 fitness 产品功能。建议下一步转入 **skill patch 候选审查** 或 **E 批 root/archive 逐条确认**。

如果你之后要继续 fitness 项目，应另开项目线程，并使用以下边界：

- 项目偏好只在项目内生效。
- PRD / 原型 / UI 由项目线程处理。
- closeout 前必须先做总结、反思、架构反哺候选和偏好缓存处置。

## 本轮不批准

- 不 staging / commit `projects/fitness-app-mvp/*`。
- 不 staging / commit `memory-cache/*`。
- 不删除、恢复、移动、归档 fitness 文件。
- 不清空 active cache。
- 不写长期记忆。
- 不把 fitness PRD 升级为 golden sample。
- 不新增 skill、harness、workflow、plugin 或长期规则。
