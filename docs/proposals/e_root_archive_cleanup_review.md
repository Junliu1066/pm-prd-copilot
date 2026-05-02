# E 批 Root / Archive 清理审查表

- 日期：2026-04-30
- 状态：只做审查，不批准删除、恢复、移动、归档、staging、commit、push 或 PR
- 范围：4 个根目录删除项、`docs/archive/` 历史归档证据
- 原则：长期稳定优先；归档先行；硬删除必须等 30 天后拿精确清单再次批准。

## 结论

当前 4 个 root 删除项都有归档证据，其中 2 个已有稳定 canonical copy。
本轮建议只保留审查清单，不提交 root 删除状态，不恢复 root 文件，不移动或删除 archive 文件。

当前推荐：

- `prd_pm_2026_playbook.md`：后续大概率可以接受 root 删除，但必须保留 canonical 和 archive。
- `prd_template_2026.md`：后续大概率可以接受 root 删除，但必须保留 canonical 和 archive。
- `prd_skill_kit_2026.zip`：不要恢复到 root；保留 archive，后续作为 30 天后删除候选。
- `skill_suite_overview.md`：不要恢复到 root；先保留 archive，后续再判断是否提炼内容到仓库说明。

## 当前证据

| 文件 | root 状态 | canonical copy | archive copy | 证据判断 | 当前建议 |
|---|---|---|---|---|---|
| `prd_pm_2026_playbook.md` | 已从 root 删除 | `pm-prd-copilot/references/prd_pm_2026_playbook.md` 存在，27387 bytes | `docs/archive/root-files/prd_pm_2026_playbook.md` 存在，27305 bytes | canonical 和 archive 哈希不同，archive 是历史证据，不是当前 canonical 的完全相同副本。 | 保留 canonical + archive；root 删除等用户确认后再接受。 |
| `prd_template_2026.md` | 已从 root 删除 | `pm-prd-copilot/templates/prd_template_2026.md` 存在，11944 bytes | `docs/archive/root-files/prd_template_2026.md` 存在，9554 bytes | canonical 和 archive 哈希不同，archive 是历史证据，不是当前 canonical 的完全相同副本。 | 保留 canonical + archive；root 删除等用户确认后再接受。 |
| `prd_skill_kit_2026.zip` | 已从 root 删除 | 无稳定 canonical copy | `docs/archive/root-files/prd_skill_kit_2026.zip` 存在，54109 bytes | 只有 archive 证据；二进制 zip 不应继续放在 root。 | 不恢复 root；保留 archive；后续进入 30 天后删除候选需单独批准。 |
| `skill_suite_overview.md` | 已从 root 删除 | 无稳定 canonical copy | `docs/archive/root-files/skill_suite_overview.md` 存在，403 bytes | 只有 archive 证据；可能有内容提炼价值。 | 不恢复 root；保留 archive；后续决定是否提炼到 `docs/repository_map.md`。 |

## Archive 当前内容

```text
docs/archive/README.md
docs/archive/notes/答辩.md
docs/archive/root-files/Remod开发.md
docs/archive/root-files/prd_pm_2026_playbook.md
docs/archive/root-files/prd_skill_kit_2026.zip
docs/archive/root-files/prd_template_2026.md
docs/archive/root-files/skill_suite_overview.md
```

注意：

- `docs/archive/` 当前是未跟踪目录，不代表已经批准成为正式归档区。
- `Remod开发.md` 和 `答辩.md` 不是本轮 4 个 root 删除项，但属于 archive 目录内容，后续也需要归档策略确认。
- archive copy 只是保留证据，不等于批准 root 删除，也不等于批准硬删除。

## 不同决策的结果

| 决策项 | 选项 | 结果 | 我的建议 |
|---|---|---|---|
| `prd_pm_2026_playbook.md` root 删除 | 接受 / 暂缓 / 恢复 | 接受会让 root 更干净；暂缓最稳但继续污染状态；恢复会让 root 回到历史散落状态。 | 暂缓到你逐条确认；确认后接受 root 删除。 |
| `prd_template_2026.md` root 删除 | 接受 / 暂缓 / 恢复 | 接受会保持模板只在 canonical 目录；暂缓保留审查余地；恢复会制造模板多版本入口。 | 暂缓到你逐条确认；确认后接受 root 删除。 |
| `prd_skill_kit_2026.zip` | 只保留 archive / 恢复 root / 后续删除 archive | 只保留 archive 最稳；恢复 root 会污染仓库；删除 archive 会丢历史包证据。 | 只保留 archive，不恢复 root。 |
| `skill_suite_overview.md` | 只保留 archive / 恢复 root / 提炼进 docs | 只保留 archive 最稳；恢复 root 会散落；提炼进 docs 需要内容审查。 | 先保留 archive，后续单独审内容。 |
| 是否提交 root 删除状态 | 现在提交 / 暂不提交 | 现在提交能清 status，但需要确认历史证据；暂不提交更稳。 | 暂不提交。 |
| 是否提交 `docs/archive/` | 现在提交 / 暂不提交 | 现在提交能保留证据，但会把 archive 策略固化；暂不提交继续保留本地证据。 | 暂不提交，先确认 archive 策略。 |

## 需要你拍板

| 拍板项 | 我的建议 | 原因 |
|---|---|---|
| 是否接受 `prd_pm_2026_playbook.md` root 删除 | 后续接受 | canonical 和 archive 都存在，root copy 冗余。 |
| 是否接受 `prd_template_2026.md` root 删除 | 后续接受 | canonical 和 archive 都存在，root copy 冗余。 |
| 是否恢复 `prd_skill_kit_2026.zip` 到 root | 不恢复 | 二进制包不应散落在 root。 |
| 是否恢复 `skill_suite_overview.md` 到 root | 不恢复 | 如有价值，应提炼进正式 docs，而不是恢复 root。 |
| 是否正式提交 `docs/archive/` | 暂缓 | archive 目录里有本轮外的历史材料，需要先定归档策略。 |
| 是否启动 30 天后硬删除候选 | 暂缓 | 需要先确认 archive 接受和 retention 起点。 |

## 本轮明确不做

- 不恢复 root 文件。
- 不删除 archive copy。
- 不移动 archive 目录。
- 不提交 root 删除状态。
- 不提交 `docs/archive/`。
- 不把 `skill_suite_overview.md` 合并进 `docs/repository_map.md`。
- 不启动硬删除。
- 不 push / PR。
