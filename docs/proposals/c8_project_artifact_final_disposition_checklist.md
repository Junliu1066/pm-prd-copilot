# C8 项目产物最终收口清单

- 日期：2026-05-02
- 状态：最终收口清单，不批准 staging、commit、push、PR、归档、删除、清空缓存、长期记忆写入或 stable 规则变更。
- 范围：C 批项目产物，主要覆盖 `projects/demo-project/prototype/`、`projects/fitness-app-mvp/`、`memory-cache/projects/fitness-app-mvp/`。
- 主线任务：把 C1-C7 的项目产物判断合并成一个执行边界，避免后续提交、归档或清理时混入稳定治理核心。

## 总结论

C 批当前不提交项目产物。

推荐状态：

| 区域 | 最终分类 | 当前动作 |
|---|---|---|
| `projects/demo-project/prototype/` | 项目原型过程产物 / 观察样例 | 项目内保留，暂不提交。 |
| `projects/fitness-app-mvp/` | active 项目 / closeout candidate | 项目内保留，暂不提交、不归档。 |
| `memory-cache/projects/fitness-app-mvp/` | 项目级偏好缓存 | 项目内保留，不提交、不清空、不长期化。 |

这样处理的目标是：

- 稳定治理核心不被 PNG、项目 run 输出、项目偏好缓存污染。
- demo 和 fitness 的项目经验不丢，后续仍能复盘。
- 长期记忆不被单个项目偏好误写。
- 后续归档、删除和项目继续推进都能按清单受监督执行。

## 已形成的 C 批判断

| 报告 | 结论摘要 | 当前用途 |
|---|---|---|
| `c1_demo_fitness_project_artifact_review.md` | demo / fitness 均不进入稳定治理提交；memory-cache 项目内保留。 | C 批总审查依据。 |
| `c1_demo_fixture_minimal_set_review.md` | demo fixture 应保持最小集，不堆项目噪音。 | demo fixture 边界依据。 |
| `c1_run_output_minimal_audit_evidence_rule.md` | run 输出最小审计证据为 `manifest.json`、`trace.json`、`harness_report.json`。 | 后续 run 瘦身依据。 |
| `c2_fitness_project_status_decision_review.md` | fitness 是 active 项目，不归档、不清缓存。 | fitness 状态依据。 |
| `c4_fitness_project_artifact_disposition_review.md` | fitness 项目产物项目内保留，不混入稳定治理。 | fitness 文件处置依据。 |
| `c5_demo_remaining_artifacts_review.md` | demo 退化生成稿不提交；prototype 暂缓。 | demo 剩余产物依据。 |
| `c6_demo_prototype_artifact_review.md` | demo prototype 是项目原型过程产物，项目内保留。 | demo prototype 边界依据。 |
| `c7_fitness_memory_cache_artifact_review.md` | fitness memory-cache 是项目内偏好缓存，不提交、不清空、不长期化。 | 偏好缓存边界依据。 |

## 文件处理清单

### Demo Prototype

| 路径 | 分类 | 推荐动作 | 原因 |
|---|---|---|---|
| `projects/demo-project/prototype/page_png/*.png` | 页面级原型 PNG | 项目内保留，暂不提交 | 可证明 PRD -> 原型链路，但 PNG 是项目过程产物，不能进入稳定核心。 |
| `projects/demo-project/prototype/ui_style_direction.md` | UI 风格建议 | 项目内保留，暂不提交 | 仅供该 demo 原型审查，不是长期默认 UI 风格。 |
| `projects/demo-project/prototype/ui_style_direction.json` | UI 风格结构化输出 | 项目内保留，暂不提交 | 可用于后续观察 UI selector 输出，但不稳定化。 |

后续处理：

- 如果要提交，只能作为 C 批项目证据单独提交。
- 不和治理核心、skill、harness、workflow、registry、proposal 混在一起。
- 不把 `swiss_utility` 设为长期默认风格。

### Fitness 项目产物

| 路径 | 分类 | 推荐动作 | 原因 |
|---|---|---|---|
| `projects/fitness-app-mvp/analysis/*` | 项目分析产物 | 项目内保留，暂不提交 | 有项目判断价值，但不是稳定治理资产。 |
| `projects/fitness-app-mvp/project_state.json` | 项目生命周期指针 | 项目内保留，暂不提交 | 当前仍标记 active cache 和最新 run。 |
| `projects/fitness-app-mvp/runs/*` | 项目运行输出 | 项目内保留，暂不提交 | active 项目需要追溯；归档前再决定最小审计证据。 |
| `projects/fitness-app-mvp/prototype/*` | 项目原型预览产物 | 项目内保留，暂不提交 | 只服务 fitness 项目，不转稳定样例。 |
| `projects/fitness-app-mvp/closeout/*` | closeout dry-run 材料 | 项目内保留，暂不提交 | 只代表审核材料，不代表项目已归档。 |
| `projects/fitness-app-mvp/02_prd.final.md`、`03_user_stories.final.md` | 未完成 final | 保留但不作为交付完成证据 | 当前只有标题，不能作为 golden sample。 |

后续处理：

- 如果继续推进 fitness，应另开项目线程补 PRD / 原型 / 开发文档。
- 如果准备归档，应先做正式 closeout 审核，再处理 memory-cache。
- 当前治理线程不继续讨论 fitness 业务优先级，避免任务漂移。

### Fitness Memory Cache

| 路径 | 分类 | 推荐动作 | 原因 |
|---|---|---|---|
| `memory-cache/projects/fitness-app-mvp/current.json` | active cache 指针 | 项目内保留，不提交 | 项目未归档，仍需要连续性。 |
| `memory-cache/projects/fitness-app-mvp/cache-*/approved_preferences.md` | 项目内已批准偏好 | 项目内保留，不提交 | 只对 fitness 生效，不能跨项目复用。 |
| `memory-cache/projects/fitness-app-mvp/cache-*/candidate_preferences.md` | 项目内候选偏好 | 项目内保留，不提交 | 不能自动升级长期记忆。 |
| `memory-cache/projects/fitness-app-mvp/cache-*/manifest.json` | 缓存元数据 | 项目内保留，不提交 | 只服务项目归档前对齐。 |
| `memory-cache/projects/fitness-app-mvp/cache-*/source_trace.json` | 偏好来源追踪 | 项目内保留，不提交 | 可用于归档前复核，不进入稳定核心。 |

禁止动作：

- 不提交 `memory-cache/`。
- 不清空 active cache。
- 不跨项目复用。
- 不写长期记忆。
- 不把“中国市场默认”“暗黑机械风”“训练计划执行”等项目偏好泛化。

## 拍板结果与推荐动作

| 决策点 | 推荐选择 | 能达到的效果 |
|---|---|---|
| demo prototype 是否提交 | 暂不提交 | 保留原型链路证据，同时避免 PNG 噪音进入仓库历史。 |
| fitness 是否继续 active | 继续 active / closeout candidate | 保留项目后续推进空间，不提前归档半成品。 |
| fitness closeout 是否提交 | 暂不提交 | 避免 closeout dry-run 被误认为项目已完成。 |
| memory-cache 是否提交 | 不提交 | 防止项目偏好被误认为长期记忆。 |
| memory-cache 是否清空 | 不清空 | 保留项目连续性，等归档前再逐条处置。 |
| fitness 是否升级 golden sample | 不升级 | 避免把未完成或被旧场景污染的内容固化。 |
| C 批是否进入稳定治理提交 | 不进入 | 稳定核心保持轻量、可回滚。 |

## 后续执行顺序

建议后续按这个顺序处理：

1. 暂缓 C 批项目产物提交，保持项目内保留。
2. 处理剩余临时 `docs/proposals/*`：只保留有决策追溯价值的记录。
3. 处理 `ai-intel/raw/`：作为 raw 证据归档候选或 30 天删除候选，不直接提交。
4. 处理额外 archive notes：单独审，不扩大 E 批。
5. 最后输出本轮治理修复总验收报告。

## 本轮不做

- 不 staging / commit `projects/demo-project/prototype/`。
- 不 staging / commit `projects/fitness-app-mvp/*`。
- 不 staging / commit `memory-cache/*`。
- 不删除、移动、恢复、归档任何项目文件。
- 不清空项目偏好缓存。
- 不把项目偏好写入长期记忆。
- 不新增 skill、harness、workflow、plugin、registry category 或长期规则。
