# 偏好缓存与长期记忆边界审查

- 日期：2026-04-30
- 状态：审查报告，不批准提交 `memory-cache/`，不批准清空缓存，不批准项目偏好进入长期记忆
- 范围：`pm-prd-copilot/memory/user_preferences.md`、`memory-cache/`、`pm-prd-copilot/scripts/manage_preference_cache.py`、`harness/preference_cache_checker.py`
- 原则：项目偏好只在项目内使用；长期记忆必须逐条批准；归档或清空必须有用户监督。

## 结论

当前偏好缓存方向正确，但需要把“清空 / 归档清空必须显式获得用户批准”落实到脚本和 checker。

本轮已做最小修复：

- `manage_preference_cache.py`：`clear` 和 `archive-clear` 必须带 `--approved-by-user`，否则命令拒绝执行。
- `manage_preference_cache.py`：清空后的 `current.json` 会记录 `user_approval_required: true` 和 `user_approval_confirmed: true`。
- `preference_cache_checker.py`：如果项目缓存状态是 `cleared`，必须检查是否记录了用户批准。
- `run_regression.py`：新增回归断言，未带 `--approved-by-user` 的 clear 必须失败；带批准的 archive-clear 必须成功并记录批准。

## 当前状态

| 区域 | 当前情况 | 结论 |
|---|---|---|
| `pm-prd-copilot/memory/user_preferences.md` | 已提交为中英双语长期偏好，中文为准 | 已完成，不在本轮再改。 |
| `memory-cache/projects/fitness-app-mvp/` | 存在 active 项目偏好缓存 | 不提交、不清空，等项目 closeout / 归档前对齐。 |
| `manage_preference_cache.py` | 已有 init / reset / clear / archive-clear | 已补显式用户批准门槛。 |
| `preference_cache_checker.py` | 检查项目隔离、清除状态、长期记忆审批字段 | 已补 cleared 状态批准记录检查。 |

## `fitness-app-mvp` 项目缓存审查

当前 `memory-cache/projects/fitness-app-mvp/` 包含：

- `current.json`
- `manifest.json`
- `approved_preferences.md`
- `candidate_preferences.md`
- `source_trace.json`

正向结果：

- `scope` 是 `project_only`。
- `cross_project_reuse_allowed` 是 `false`。
- `long_term_memory_requires_user_approval` 是 `true`。
- `archive_alignment_required` 是 `true`。
- `clear_after_project_archive_alignment` 是 `true`。
- source trace 均标记需要人工核验。

风险点：

- 项目缓存仍是 active，不能自动跨项目读取。
- 已批准项目偏好包含健身项目的市场、原型风格和训练计划细节，只适合 `fitness-app-mvp`。
- 归档前必须逐条决定：保留为项目档案、清除、还是经用户批准提炼为长期候选。

## 边界修复说明

### 为什么要加 `--approved-by-user`

偏好缓存的 `clear` 和 `archive-clear` 会改变项目偏好指针，属于高风险动作。如果没有命令级显式批准，后续自动化或误操作可能清空项目偏好，影响项目连续性。

新增门槛后：

- 未带 `--approved-by-user`：命令失败。
- 带 `--approved-by-user`：命令可以执行，并在清空状态里留下批准记录。
- checker 会检查 cleared 状态是否有批准记录。

这符合“必须在用户监督下清理 / 归档 / 写长期记忆”的长期规则。

### 不处理的内容

本轮没有做：

- 不提交 `memory-cache/`。
- 不清空 `fitness-app-mvp` 项目缓存。
- 不把健身项目偏好写入长期记忆。
- 不把 `preference_cache_checker.py` 转 stable。
- 不新增 skill、harness、workflow stage、plugin 或 automation。

## 当前建议

| 决策 | 我的建议 | 原因 |
|---|---|---|
| 是否提交 `memory-cache/` | 不提交 | 项目缓存是项目现场材料，归档前再处理更稳。 |
| 是否清空 `fitness-app-mvp` 缓存 | 不清空 | 该项目仍有连续性价值，清空必须等 closeout 对齐。 |
| 是否把健身项目偏好提炼为长期规则 | 暂不 | 防止项目经验污染其他项目。 |
| 是否把 `preference_cache_checker.py` 转 stable | 暂不 | 先作为按需候选；等偏好缓存流程跑过更多项目再决定。 |
| 是否提交本轮脚本 / checker 最小修复 | 建议单独提交 | 这是防误清理的底线修复，范围小、可回滚。 |

## 下一步建议

1. 本轮脚本 / checker / regression / 报告通过验证后，单独提交为“偏好缓存清空审批门槛”补丁。
2. `memory-cache/` 保持不提交。
3. 等 `fitness-app-mvp` closeout 时，再输出项目偏好处置清单。
4. 后续再单独决定 `preference_cache_checker.py` 是否继续保持候选、瘦身、或进入稳定批次。
