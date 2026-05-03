# C15 Temp Generated Project 处置审查

- 日期：2026-05-03
- 状态：proposal / temporary project disposition review，不是 stable policy。
- 授权等级：L1 审查与台账更新；不执行 L2 staging / commit，不执行 L3 删除 / 归档。
- 主线任务：判断 `temp-generated-project` 是否可以直接清理，或是否应先作为临时项目隔离证据保留。

## 1. 结论

`projects/temp-generated-project` 是明确的临时生成项目，但不是无价值目录。它有一套完整的临时交付文件，能证明“临时工作必须隔离在项目目录，不改治理架构”的边界。

推荐状态：

```text
temporary_project_evidence_delete_after_30_days_candidate
```

推荐动作：

1. 暂时保留项目目录作为临时项目隔离证据。
2. 不提交 `projects/temp-generated-project/`。
3. 不作为 PRD golden sample，不作为开发文档样例，不作为稳定模板输入。
4. 后续本轮治理总验收完成后，可列入 30 天后删除候选。
5. 真正删除前必须单独列精确清单并经你再次批准。

## 2. 当前证据

| 指标 | 当前结果 |
|---|---|
| 项目大小 | 64K |
| Git 状态 | 未跟踪项目目录 |
| 文件数 | 10 |
| PRD / 原型 / 开发文档 | 有 |
| 原型类型 | 单文件静态 HTML |
| 运行 manifest | 有，`temporary-preview-20260430` |
| 项目性质 | 明确写为“临时生成使用” |
| 架构反哺强度 | 中，偏边界治理证据 |

## 3. 项目价值

这个项目的价值不在业务本身，而在治理边界：

| 价值点 | 说明 |
|---|---|
| 写入边界清楚 | 明确只写 `projects/temp-generated-project/`，不改 stable 目录。 |
| 临时项目有完整交付包 | 包含 raw input、brief、PRD、prototype spec、development doc、delivery check、prototype、manifest。 |
| 交付检查清楚 | Round 1 / Round 2 明确检查范围和稳定目录未改。 |
| 可作为反例提醒 | 业务主题是临时假设，不能把临时产物当 stable 样例。 |

## 4. 风险

| 风险 | 影响 | 建议 |
|---|---|---|
| 项目名称和输入都说明是临时 | 长期保留会增加噪音。 | 总验收后进入 30 天删除候选。 |
| PRD 使用旧“一句话摘要”口径 | 与 A1 最新 PRD 口径不一致。 | 不作为 PRD 样例，不回扫修改。 |
| 业务主题是临时假设 | 不能代表真实项目需求。 | 只作为临时项目隔离证据。 |
| 有本地绝对路径链接 | 不适合外发或入库为样例。 | 不提交项目产物。 |

## 5. 文件处置建议

| 文件 / 目录 | 建议 | 原因 |
|---|---|---|
| `00_raw_input.md` | 暂时保留 | 证明用户要求“临时生成、不改治理架构”。 |
| `01_requirement_brief.md` | 暂时保留 | 临时交付链路证据。 |
| `02_prd.md` | 保留但不升级样例 | PRD 有旧口径，不适合作样例。 |
| `03_prototype_spec.md` | 暂时保留 | 原型说明证据。 |
| `04_development_doc.md` | 暂时保留 | Codex 开发文档类临时证据。 |
| `05_delivery_check.md` | 暂时保留 | 两轮检查和写入边界证据。 |
| `prototype/index.html` | 暂时保留 | 静态原型证据。 |
| `runs/temporary-preview/manifest.json` | 暂时保留 | 临时运行证据。 |
| `project_state.json` | 暂时保留 | 项目状态证据。 |
| `closeout/architecture-feedback.md` | 暂时保留 | 架构反馈占位。 |

## 6. 架构反哺候选

| 候选 | 当前建议 |
|---|---|
| 临时项目必须强隔离，不触碰 stable 目录 | 已在当前治理原则中体现，可作为总验收案例。 |
| 临时项目可以有完整交付包，但不能自动长期化 | 可进入 lifecycle proposal 的例子，不直接 stable。 |
| 旧 PRD 口径的历史产物不回扫修改 | 已符合当前策略，不需要额外动作。 |

## 7. 需要你后续拍板

| 拍板项 | 我的建议 | 不同选择的效果 |
|---|---|---|
| 是否提交 C15 审查报告 | 后续和 C12-C16 项目审查记录一起提交 | 提交可保留临时项目边界判断；不提交则继续留在未跟踪 proposal。 |
| 是否提交项目目录 | 不提交 | 提交会增加噪音，且临时主题不适合入库。 |
| 是否归档项目目录 | 暂缓 | 等治理总验收后再决定。 |
| 是否 30 天后删除候选 | 是 | 能逐步瘦身工作区，但不现在删除。 |

## 8. 本轮不做

- 不提交 `projects/temp-generated-project/`。
- 不删除项目目录。
- 不移动到 archive。
- 不回扫修旧 PRD 口径。
- 不把临时主题写入长期记忆。
- 不修改 stable template、skill、harness 或 workflow。

## 9. 推荐状态变更

建议在台账中把 C15 从：

```text
next
```

更新为：

```text
temporary_project_evidence_delete_after_30_days_candidate
```

下一步可汇总 C12-C16 项目审查结果，或进入 proposal 决策记录候选提交计划。
