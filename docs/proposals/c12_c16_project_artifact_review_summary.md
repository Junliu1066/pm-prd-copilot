# C12-C16 项目产物审查汇总

- 日期：2026-05-03
- 状态：L2 审核材料 / 项目产物汇总，不是 stable policy。
- 主线任务：汇总 C12-C16 的项目产物审查结果，帮助判断哪些项目证据应保留、哪些不应提交、哪些后续可归档或进入 30 天删除候选。
- 边界：本文件不批准提交项目产物、归档、删除、长期记忆写入、stable 转正或新增工具。

## 1. 总结论

C12-C16 已经完成 L1 审查，结论一致：

1. 不提交任何 `projects/*` 项目目录。
2. 不提交任何 zip、HTML、PNG、raw 项目产物。
3. 不把低证据原型项目当成 PRD golden sample。
4. 不把项目里的业务机制直接升级为 stable policy。
5. 所有归档和删除继续走 L3 单独审批。

这轮审查的实际效果是：把项目产物和稳定治理核心彻底分开，避免后续提交时把项目历史、原型包、zip 或临时项目混进架构。

## 2. 项目分层结果

| ID | 项目 / 范围 | 判断 | 推荐状态 | 后续动作 |
|---|---|---|---|---|
| C12 | `ai-collaboration-efficiency-platform` | 高价值复杂项目证据，旧 closeout 只扫到 1 个文件，不能直接归档。 | `closeout_candidate_refreshed` | 项目内保留；不提交项目产物；后续可作为复杂 AI / Skill 治理产品交付链路候选。 |
| C13 | `prompt-optimization-workbench` | 低证据 HTML 原型项目，缺 PRD、开发文档和验收边界。 | `prototype_artifact_closeout_candidate` | 项目内保留；不作为 PRD 样例；不提炼 stable。 |
| C14 | `santoip-ai-brand-video` | 业务更完整的 HTML 原型项目，但仍缺 PRD 和开发边界。 | `prototype_artifact_closeout_candidate` | 项目内保留；可作为业务原型候选，暂不稳定化。 |
| C15 | `temp-generated-project` | 临时项目隔离证据，不能直接删除，但不适合长期保留。 | `temporary_project_evidence_delete_after_30_days_candidate` | 本轮总验收后可列入 30 天删除候选；不现在删除。 |
| C16 | 项目 zip / package | 发现 12 个压缩包，需要区分 canonical、archive evidence、prototype zip、duplicate candidate。 | `package_zip_lifecycle_review_done` | 不提交 zip；不删除 zip；后续按 package 生命周期单独审批。 |

## 3. 架构反哺候选

只保留候选，不直接改稳定规则。

| 候选 | 来源 | 当前建议 |
|---|---|---|
| 复杂项目交付链路：PRD -> Codex 开发文档 -> 图表 -> 页面级原型 -> HTML 原型 | C12 | 作为复杂交付链路候选，不直接 stable。 |
| 低证据 HTML 原型不能反推 PRD 或 stable UI 规则 | C13 / C14 | 可作为项目产物边界案例。 |
| 临时项目必须强隔离，不能触碰 stable 目录 | C15 | 可作为生命周期治理反例，不提交项目目录。 |
| 每个项目同类 zip 最多保留一个 canonical 包 | C16 | 候选规则，后续不新增脚本，先用审查表管理。 |
| archive evidence 只能证明历史，不能回流为当前执行源 | C16 | 候选规则，后续归档策略确认后再处理。 |

## 4. 不能做的事

| 禁止动作 | 原因 |
|---|---|
| 提交 `projects/ai-collaboration-efficiency-platform/` | 项目含本地路径、HTML、PNG、zip 和历史旧口径，直接提交会污染稳定治理。 |
| 提交 C13 / C14 项目目录 | 它们只是低证据 HTML 原型，不是 PRD 或开发文档样例。 |
| 删除 C15 临时项目 | 虽然是临时项目，但仍有临时隔离证据价值，必须走 30 天候选和二次审批。 |
| 提交或删除 zip | zip 需要 canonical / duplicate / archive evidence 分类后单独审批。 |
| 把项目经验写入长期记忆 | 项目经验只能进入候选，长期记忆必须逐条批准。 |
| 新增 skill / harness / workflow | 当前问题可用审查表和生命周期台账处理，不需要新增工具。 |

## 5. 需要你后续拍板的功能项

| 拍板项 | 我的建议 | 选择后的效果 |
|---|---|---|
| 是否提交 C12-C16 详细审查报告 | 建议作为 17 个 proposal 决策记录候选的一部分提交 | 能保留项目产物边界判断；不会提交项目产物。 |
| 是否把 C12 作为复杂交付链路候选案例 | 保持 candidate | 后续和 Jiaxiaoqian、Graduation 项目对比后再决定是否沉淀。 |
| 是否把 C13 / C14 作为 UI / UX 原型案例 | 暂缓 | 现在提炼容易过拟合；等更多原型项目再比较。 |
| 是否把 C15 放入 30 天删除候选 | 建议总验收后放入 | 能逐步瘦身工作区，但不会马上删除。 |
| 是否确认 Jiaxiaoqian 英文完整包为 canonical | 暂定，后续归档前确认 | 能降低重复包管理成本，但现在不删除中文包。 |

## 6. 推荐下一步

下一步不处理项目目录，先做 17 个 proposal 决策记录候选的提交计划。

原因：

- 项目产物边界已经看清楚。
- 详细判断需要先以 proposal 形式保留下来。
- 这样后续清理临时 proposal、项目 zip、raw 和临时项目时有依据。

本汇总文件本身是 L2 审核材料，暂不放进 17 个决策记录候选提交范围，避免提交计划自我引用。
