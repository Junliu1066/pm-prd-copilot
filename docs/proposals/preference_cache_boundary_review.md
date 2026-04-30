# 偏好缓存与长期记忆边界审查

- 日期：2026-04-30
- 状态：审查报告，不批准 staging / commit / 清空缓存 / 长期记忆写入
- 范围：`pm-prd-copilot/memory/user_preferences.md`、`memory-cache/`、`harness/preference_cache_checker.py`
- 原则：项目偏好只在项目内使用；长期记忆必须逐条批准；归档前必须对齐。

## 结论

当前偏好缓存机制方向正确：项目级偏好和长期偏好已经分层，`memory-cache` 里只有 `fitness-app-mvp` 项目缓存，且策略字段明确禁止跨项目复用。

但当前仍不建议提交或自动清理偏好缓存，因为还需要你逐条确认：

- 哪些长期偏好确实已经被你批准。
- 哪些只是 `fitness-app-mvp` 项目内偏好。
- 哪些需要在项目归档前保留为 closeout 证据。
- 哪些未来可以提炼为长期规则。

## 当前状态

| 区域 | 当前情况 | 建议 |
|---|---|---|
| `pm-prd-copilot/memory/user_preferences.md` | 已有多条长期偏好修改，覆盖 PRD、原型、开发文档、B 包、长期规则审批等 | 暂不提交，先逐条审。 |
| `memory-cache/projects/fitness-app-mvp/` | 存在项目级偏好缓存，状态为 active | 暂不清空，归档前再对齐。 |
| `harness/preference_cache_checker.py` | 能检查项目隔离、清除状态、长期记忆审批字段 | 保持按需候选，不 stable。 |

## 长期偏好初步分类

| 类型 | 条目示例 | 初步判断 |
|---|---|---|
| 已明确批准的长期偏好 | 中文报告、开发文档默认 Codex 开发文档、长期稳定可靠优先、长期规则需方案审批 | 可进入长期偏好候选，但仍建议你最后确认一次。 |
| PRD / 原型长期规则 | PRD 页面说明、页面跳转关系、原型图层、PNG/HTML 需后续确认 | 已有明确讨论基础，可保留为长期偏好候选。 |
| 开发文档 / B 包规则 | 内部版/外部保护版、B 包英文、受众分层、开发文档边界 | 建议保留，但需要和真实 B 包输出再对齐一次。 |
| 项目内偏好 | 健身项目市场、原型风格、训练计划交互等 | 只能留在 `fitness-app-mvp` 项目缓存，不能进入全局长期记忆。 |
| 需要谨慎的泛化规则 | “所有开发包包含所有资产”等较宽规则 | 应按受众、脱敏和项目阶段收敛后再长期化。 |

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
- 已批准项目偏好里有原型和训练计划细节，这些只适合健身项目。
- 归档前必须决定：保留为项目档案、清除、还是提炼为长期候选。

## Preference Checker 边界判断

| 检查项 | 价值 | 是否应 stable |
|---|---|---|
| 项目内路径限制 | 防止读取其他项目缓存 | 暂不 stable，保留候选 |
| 清除状态不可继续读取 | 防止归档后污染新项目 | 暂不 stable，保留候选 |
| 长期记忆需用户批准 | 防止自动学习越权 | 暂不 stable，保留候选 |
| source trace 必须人工核验 | 保证偏好来源可追溯 | 暂不 stable，保留候选 |

结论：`preference_cache_checker.py` 有必要，但应继续作为按需候选。等偏好缓存策略稳定后，再决定是否转 stable。

## 建议处理方式

### 1. 长期偏好文件

先不提交 `pm-prd-copilot/memory/user_preferences.md`。

下一步建议输出一份逐条清单，把每条偏好分为：

- `approved_long_term`
- `project_only`
- `needs_rewording`
- `needs_user_approval`
- `do_not_keep`

你逐条确认后，再提交长期偏好文件。

### 2. 项目偏好缓存

先不提交 `memory-cache/`。

处理规则：

- 项目活跃时可保留 active。
- 项目 closeout 前输出处置建议。
- 归档前和你对齐：保留、清除、或提炼为长期候选。
- 清空缓存必须单独批准。

### 3. Checker

先不提交 `harness/preference_cache_checker.py`。

建议等以下两个条件满足后再决定：

- 长期偏好文件逐条确认完成。
- `fitness-app-mvp` 项目缓存归档前处置规则确认。

## 需要你后续拍板

| 决策 | 我的建议 | 不同选择的结果 |
|---|---|---|
| 是否提交长期偏好文件 | 暂不 | 避免把未逐条确认的内容写成长期记忆。 |
| 是否提交 `memory-cache/` | 暂不 | 项目缓存属于项目证据，归档前再处理更稳。 |
| 是否清空项目缓存 | 不清空 | 清空会影响项目连续性，必须 closeout 对齐后再做。 |
| 是否把健身项目偏好提炼为长期规则 | 逐条批准 | 防止项目经验污染其他项目。 |
| 是否提交 `preference_cache_checker.py` | 暂不 | 等偏好策略确认后再作为候选 checker 单独处理。 |

## 下一步建议

1. 先做长期偏好逐条审查清单。
2. 再做 `fitness-app-mvp` 项目 closeout / 偏好处置建议。
3. 再决定是否提交 `pm-prd-copilot/memory/user_preferences.md`。
4. 最后决定 `preference_cache_checker.py` 是否作为按需候选 checker 提交。

## 本轮未执行

- 未提交长期偏好。
- 未提交项目缓存。
- 未清空缓存。
- 未写长期记忆。
- 未提交 preference checker。
- 未移动、归档或删除任何文件。
