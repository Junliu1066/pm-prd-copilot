# Archive Notes 生命周期处置清单

- 日期：2026-05-04
- 状态：审查清单，不批准删除、移动、归档、staging、commit、push、PR、长期记忆写入、skill / harness 新增或 stable 规则变更。
- 范围：`docs/archive/notes/答辩.md`、`docs/archive/root-files/Remod开发.md`，并说明它们和已提交 root cleanup archive 的边界。
- 主线任务：把额外 archive 历史材料从 E 批 root cleanup 主证据中拆出来，防止未审历史材料绑死 archive 策略。

## 结论

当前 `docs/archive/` 已分成两类：

1. **已提交的 root cleanup 最小证据**：已在 `08f9876 Accept root cleanup with archive evidence` 中提交。
2. **额外未审历史材料**：`Remod开发.md` 和 `答辩.md`，当前不建议提交、不删除、不移动。

推荐处理：

- `docs/archive/root-files/Remod开发.md`：已在 2026-05-04 完成复核；内容大部分已被后续治理修复吸收，保留为 `delete_after_30_days_candidate`，不直接提交原文。
- `docs/archive/notes/答辩.md`：保留为 `project_input_evidence_candidate`，但不直接提交；C9 已确认它与 `graduation-defense-agent` 原始输入高度相关，不应混入 root cleanup。
- 两者后续都可进入 30 天后删除候选，但必须先确认有用信息已经提炼或不需要提炼。

## 当前文件分类

| 文件 | 当前状态 | 类型 | 推荐生命周期状态 | 当前动作 |
|---|---|---|---|---|
| `docs/archive/README.md` | 已提交 | archive 目录说明 | `archive_policy_record` | 保留。 |
| `docs/archive/root-files/prd_pm_2026_playbook.md` | 已提交 | root cleanup 证据 | `canonical_aligned_archive_evidence` | 保留。 |
| `docs/archive/root-files/prd_template_2026.md` | 已提交 | root cleanup 证据 | `canonical_aligned_archive_evidence` | 保留。 |
| `docs/archive/root-files/prd_skill_kit_2026.zip` | 已提交 | root cleanup 证据 / 历史包 | `archive_evidence` | 保留，后续可单独判断硬删除候选。 |
| `docs/archive/root-files/skill_suite_overview.md` | 已提交 | root cleanup 证据 | `archive_evidence` | 保留，后续可判断是否提炼到正式 docs。 |
| `docs/archive/root-files/Remod开发.md` | 未跟踪 | 历史开发治理笔记 | `delete_after_30_days_candidate` | 不提交原文；最早 2026-06-03 后可拿精确清单二次审批。 |
| `docs/archive/notes/答辩.md` | 未跟踪 | 毕业答辩项目原始输入证据候选 | `project_input_evidence_candidate` | 暂不提交、不删除、不移动；随 `graduation-defense-agent` closeout 处理。 |

## 文件判断

### `Remod开发.md`

当前观察：

- 约 123 行，主题是 Delivery Planning Suite、agentic delivery、Codex 半自动开发任务包、监督机制和建议新增 artifacts / harness。
- 内容与后续已完成的 agentic delivery 边界、Codex 开发文档、任务漂移治理、能力候选最小化有重叠。
- 文中包含“建议新增 Skill / Harness”的旧方向，和当前“如无必要，不增 skill / harness”的长期原则存在张力。

2026-05-04 复核结论：

- 已被吸收的内容：Codex 半自动开发任务包、人工确认点、任务允许 / 禁止修改范围、验证命令、回滚方案、开发治理报告、agentic delivery 按需触发、candidate 能力不自动 stable。
- 已被修正的旧口径：原文倾向直接新增 `agentic-delivery-orchestrator` Skill、建议新增 artifact / harness；当前治理已经改为先候选、按需触发、最小化检查，不再按原文推动新增组件。
- 未发现必须保留原文才能支撑稳定架构的独有信息。

推荐：

- 不直接提交为 archive 正文。
- 标记为 `delete_after_30_days_candidate`，但不现在删除。
- 如果 2026-06-03 前需要回看，可继续从本地未跟踪文件复核。
- 如果 2026-06-03 后确认不再需要原文，必须再次拿精确删除清单给用户批准。

不同选择的效果：

| 选项 | 效果 | 风险 | 我的建议 |
|---|---|---|---|
| 直接提交原文 | 保留完整历史证据 | 旧的“新增 skill / harness”口径可能误导后续治理 | 不选 |
| 提炼后提交总结 | 保留有价值经验，去掉旧口径噪音 | 当前独有信息不足，可能制造重复 proposal | 暂不选 |
| 暂不提交，本地保留 | 保留复核能力，不污染 archive 提交 | 工作区继续有未跟踪文件 | 仅保留到候选期 |
| 30 天后删除候选 | 最终瘦身 | 必须二次批准，不可自动删除 | 当前选择 |

### `答辩.md`

当前观察：

- 约 217 行，是毕业答辩辅导智能体问题库资料。
- 内容更像 `graduation-defense-agent` 项目材料，而不是治理框架资产。
- 不应和 root cleanup archive 混在同一批提交。

推荐：

- 不直接提交到 `docs/archive/notes/`。
- 先标记为 `project_input_evidence_candidate`。
- C9 已确认它应随 `projects/graduation-defense-agent/` closeout 处理，当前不移动、不提交、不删除。
- 不提炼为长期治理规则，除非未来明确要做“答辩智能体”项目。

不同选择的效果：

| 选项 | 效果 | 风险 | 我的建议 |
|---|---|---|---|
| 直接提交到 archive notes | 保留历史项目资料 | 项目材料污染治理 archive | 不选 |
| 移回项目目录 | 项目归属更清楚 | 需要移动文件，当前未批准 | 后续项目盘点时再判断 |
| 暂不提交，本地保留 | 最稳，不污染治理提交 | 工作区继续有未跟踪文件 | 当前选择 |
| 30 天后删除候选 | 最终瘦身 | 可能丢项目资料，需先确认项目是否保留 | 后续可选 |

## 和 E 批 Root Cleanup 的边界

E 批已提交的是最小 root cleanup 证据：

```text
docs/archive/README.md
docs/archive/root-files/prd_pm_2026_playbook.md
docs/archive/root-files/prd_template_2026.md
docs/archive/root-files/prd_skill_kit_2026.zip
docs/archive/root-files/skill_suite_overview.md
```

`Remod开发.md` 和 `答辩.md` 不属于这个最小集合：

- 它们不是已确认 root 删除项的 canonical / archive 对齐证据。
- 它们没有经过用户逐项批准进入 archive。
- 它们包含项目或旧治理思路，不能直接作为稳定 archive 策略的一部分。

## 需要用户后续拍板

| 拍板项 | 我的建议 | 不同选择的效果 |
|---|---|---|
| `Remod开发.md` 是否提交 | 不提交原文 | 避免旧新增 skill / harness 口径误导；提交则会增加 archive 噪音。 |
| `Remod开发.md` 是否提炼中文总结 | 暂不提炼 | 当前经验已被 agentic delivery、Codex 开发文档和 harness 瘦身材料吸收；提炼会重复。 |
| `答辩.md` 是否归入 `graduation-defense-agent` 项目 | 作为项目原始输入证据候选，正式归档前再拍板 | 归入项目更合理，但当前不移动。 |
| `答辩.md` 是否提交到 archive | 暂不提交 | 避免项目资料污染治理 archive。 |
| 两个文件是否进入 30 天后删除候选 | 可以后续列入候选 | 有利于瘦身，但必须先确认内容无保留价值。 |

## 推荐后续顺序

1. 当前只保留本审查清单。
2. `答辩.md` 已在 C9 中确认为 `graduation-defense-agent` 原始输入证据候选，等待正式项目 closeout 时拍板。
3. 2026-06-03 后，如果仍没有回看需求，再把 `Remod开发.md` 精确列入删除审批清单。
4. 做 skill / harness / plugin candidate 瘦身复盘时，不再引用原文作为新增组件依据，只引用已稳定或已提交的治理材料。

## 本轮不做

- 不提交 `docs/archive/notes/答辩.md`。
- 不提交 `docs/archive/root-files/Remod开发.md`。
- 不移动文件。
- 不删除文件。
- 不恢复 root 文件。
- 不新增 skill、harness、workflow、plugin 或 registry 项。
- 不写长期记忆。
- 不 staging / commit / push / PR。
