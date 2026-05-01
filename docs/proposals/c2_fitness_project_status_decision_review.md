# C2 Fitness 项目产物边界审查

- 日期：2026-05-01
- 状态：治理审查报告，不是产品方案，不批准 staging、commit、push、PR、归档、删除、清空缓存或长期记忆写入。
- 范围：`projects/fitness-app-mvp/`、`memory-cache/projects/fitness-app-mvp/`
- 主线任务：判断该项目产物是否能混入稳定治理提交、是否适合 closeout、是否存在长期记忆污染风险。

## 主线边界

本报告只回答治理问题：

- 这些文件属于稳定架构、项目产物、归档候选还是临时运行输出。
- 项目偏好缓存是否能跨项目复用或进入长期记忆。
- closeout 材料是否代表项目已经可以归档。
- 后续提交时哪些内容必须排除在稳定核心之外。

本报告不回答产品业务问题：

- 不判断训练计时、食物热量、饮食记录等功能优先级。
- 不重写 fitness PRD。
- 不评价 UI / 原型方向。
- 不要求你在当前治理线程里做项目业务决策。

## 审查结论

`fitness-app-mvp` 当前应归类为 **active 项目产物**，不进入稳定治理提交，不进入归档候选，不清空项目偏好缓存。

原因：

1. `02_prd.final.md` 和 `03_user_stories.final.md` 目前只有标题，不具备归档完成度。
2. `02_prd.generated.md`、`analysis/`、`prototype/` 有项目证据价值，但它们是项目材料，不是稳定架构资产。
3. `closeout/` 已有 dry-run 审核材料，但 closeout 报告不等于项目已经归档。
4. `memory-cache/projects/fitness-app-mvp/` 是项目内偏好缓存，不能跨项目复用，也不能自动写入长期记忆。
5. 当前治理主线是架构收口，继续分析 fitness 的产品功能会造成任务漂移。

## 当前产物分类

| 范围 | 当前状态 | 治理分类 | 建议 |
|---|---|---|---|
| `projects/fitness-app-mvp/02_prd.final.md` | 只有标题 | 未完成项目交付物 | 不提交为 final，不作为 golden sample |
| `projects/fitness-app-mvp/03_user_stories.final.md` | 只有标题 | 未完成项目交付物 | 不提交为 final |
| `projects/fitness-app-mvp/02_prd.generated.*` | 有生成内容 | 项目生成产物 | 项目内保留，后续项目线程再处理 |
| `projects/fitness-app-mvp/analysis/` | 有分析输出 | 项目证据材料 | 项目内保留，不进入稳定治理 |
| `projects/fitness-app-mvp/prototype/` | 有低保真预览材料 | 项目原型材料 | 项目内保留，后续项目线程确认 |
| `projects/fitness-app-mvp/closeout/` | 已有 dry-run 五件套 | closeout 审核材料 | 不代表已归档，不提交到稳定核心 |
| `projects/fitness-app-mvp/runs/` | 多轮运行输出 | 可重建运行证据 | 默认不提交，除非专项审核需要 |
| `memory-cache/projects/fitness-app-mvp/` | 项目偏好缓存 | 项目内记忆 | 不提交、不清空、不跨项目复用 |

## 风险说明

| 风险 | 表现 | 影响 | 处理方式 |
|---|---|---|---|
| 项目产物混入稳定架构 | 把 `projects/fitness-app-mvp/*` 和治理核心一起提交 | 稳定核心变脏，后续难回滚 | C 批项目产物单独审查 |
| 项目偏好污染长期记忆 | 把 fitness 偏好写进通用规则 | 其他项目被错误引导 | 归档前逐条对齐，用户批准后才长期化 |
| closeout 状态误判 | 看到 closeout 文件就认为项目完成 | 半成品被归档，项目价值丢失 | closeout 报告只作为审核材料 |
| 任务漂移 | 从治理审查进入产品功能讨论 | 打断主线修复 | 本报告禁止产品业务判断 |

## 需要你拍板的治理功能决策

| 决策 | 选项 A | 选项 B | 选项 C | 我的建议 |
|---|---|---|---|---|
| fitness 项目状态归类 | active 项目产物 | closeout candidate | archive candidate | 选 A。final 交付物未完成，不能 closeout 或归档。 |
| fitness 项目文件是否进入治理提交 | 暂不提交 | 作为 C 批单独提交 | 混入稳定核心 | 选 A。当前主线是治理收口，不应混入项目产物。 |
| `memory-cache/projects/fitness-app-mvp/` 如何处理 | 项目内保留 | 清空 | 提炼长期记忆 | 选 A。项目未归档，缓存还有连续性价值；长期记忆必须逐条批准。 |
| `closeout/` 如何处理 | 保留为审核材料 | 视为已归档 | 删除 | 选 A。它只是 closeout 草案，不代表归档完成。 |
| 后续是否在本线程处理 fitness 产品功能 | 不处理 | 只处理一个小功能 | 继续做完整 PRD | 选 A。当前主线是治理修复，产品功能应放到项目线程。 |

## 推荐后续处理

1. C2 到此只作为项目产物边界报告保留。
2. 当前治理线程不继续深入 fitness 产品内容。
3. 后续如果你要推进 fitness 项目，应另开项目线程，并把当前治理线程产出的边界规则作为约束：
   - 项目偏好只在项目内使用。
   - 产品 PRD / 原型 / UI 由项目线程处理。
   - 归档前再做 closeout 和长期记忆候选对齐。

## 本轮不批准

- 不改 `projects/fitness-app-mvp/*`。
- 不提交项目产物。
- 不归档项目。
- 不删除或清空 `memory-cache/`。
- 不把 fitness 偏好写入长期记忆。
- 不把 fitness PRD 升级为 golden sample。
- 不新增 skill、harness、workflow、plugin 或长期规则。
