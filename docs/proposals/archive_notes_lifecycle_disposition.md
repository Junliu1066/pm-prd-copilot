# Archive Notes 生命周期处置清单

- 日期：2026-05-02
- 状态：审查清单，不批准删除、移动、归档、staging、commit、push、PR、长期记忆写入、skill / harness 新增或 stable 规则变更。
- 范围：`docs/archive/notes/答辩.md`、`docs/archive/root-files/Remod开发.md`，并说明它们和已提交 root cleanup archive 的边界。
- 主线任务：把额外 archive 历史材料从 E 批 root cleanup 主证据中拆出来，防止未审历史材料绑死 archive 策略。

## 结论

当前 `docs/archive/` 已分成两类：

1. **已提交的 root cleanup 最小证据**：已在 `08f9876 Accept root cleanup with archive evidence` 中提交。
2. **额外未审历史材料**：`Remod开发.md` 和 `答辩.md`，当前不建议提交、不删除、不移动。

推荐处理：

- `docs/archive/root-files/Remod开发.md`：保留为 `archive_evidence_candidate`，但不直接提交；先判断是否已有内容被后续治理修复吸收。
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
| `docs/archive/root-files/Remod开发.md` | 未跟踪 | 历史开发治理笔记 | `archive_evidence_candidate` | 暂不提交、不删除。 |
| `docs/archive/notes/答辩.md` | 未跟踪 | 毕业答辩项目原始输入证据候选 | `project_input_evidence_candidate` | 暂不提交、不删除、不移动；随 `graduation-defense-agent` closeout 处理。 |

## 文件判断

### `Remod开发.md`

当前观察：

- 约 123 行，主题是 Delivery Planning Suite、agentic delivery、Codex 半自动开发任务包、监督机制和建议新增 artifacts / harness。
- 内容与后续已完成的 agentic delivery 边界、Codex 开发文档、任务漂移治理、能力候选最小化有重叠。
- 文中包含“建议新增 Skill / Harness”的旧方向，和当前“如无必要，不增 skill / harness”的长期原则存在张力。

推荐：

- 不直接提交为 archive 正文。
- 先标记为 `archive_evidence_candidate`。
- 后续如果需要保留，只提炼成中文 proposal 总结，不能按原文推动新增 skill / harness。
- 如果确认其中内容已被后续治理吸收，可列入 30 天后删除候选。

不同选择的效果：

| 选项 | 效果 | 风险 | 我的建议 |
|---|---|---|---|
| 直接提交原文 | 保留完整历史证据 | 旧的“新增 skill / harness”口径可能误导后续治理 | 不选 |
| 提炼后提交总结 | 保留有价值经验，去掉旧口径噪音 | 需要额外整理成本 | 后续按需 |
| 暂不提交，本地保留 | 保留复核能力，不污染 archive 提交 | 工作区继续有未跟踪文件 | 当前选择 |
| 30 天后删除候选 | 最终瘦身 | 必须确认内容已吸收或无价值 | 后续可选 |

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
| `Remod开发.md` 是否提交 | 暂不提交 | 暂不提交可避免旧新增 skill / harness 口径误导；提交则保留完整历史。 |
| `Remod开发.md` 是否提炼中文总结 | 后续按需 | 提炼能保留经验，但当前已有大量内容被吸收。 |
| `答辩.md` 是否归入 `graduation-defense-agent` 项目 | 作为项目原始输入证据候选，正式归档前再拍板 | 归入项目更合理，但当前不移动。 |
| `答辩.md` 是否提交到 archive | 暂不提交 | 避免项目资料污染治理 archive。 |
| 两个文件是否进入 30 天后删除候选 | 可以后续列入候选 | 有利于瘦身，但必须先确认内容无保留价值。 |

## 推荐后续顺序

1. 当前只保留本审查清单。
2. `答辩.md` 已在 C9 中确认为 `graduation-defense-agent` 原始输入证据候选，等待正式项目 closeout 时拍板。
3. 做 skill / harness / plugin candidate 瘦身复盘时，复核 `Remod开发.md` 是否还有未吸收经验。
4. 经过用户确认后，再决定归档、提炼或 30 天后删除候选。

## 本轮不做

- 不提交 `docs/archive/notes/答辩.md`。
- 不提交 `docs/archive/root-files/Remod开发.md`。
- 不移动文件。
- 不删除文件。
- 不恢复 root 文件。
- 不新增 skill、harness、workflow、plugin 或 registry 项。
- 不写长期记忆。
- 不 staging / commit / push / PR。
