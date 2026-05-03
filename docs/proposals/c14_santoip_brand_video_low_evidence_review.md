# C14 Santoip AI Brand Video 低证据项目审查

- 日期：2026-05-03
- 状态：proposal / low-evidence project review，不是 stable policy。
- 授权等级：L1 审查与台账更新；不执行 L2 staging / commit，不执行 L3 删除 / 归档。
- 主线任务：判断 `santoip-ai-brand-video` 是否仍有项目价值，避免把业务 HTML 原型误提交到稳定治理核心。

## 1. 结论

`projects/santoip-ai-brand-video` 当前不是完整 PRD 项目，也不是开发交付项目。它是一个中保真 HTML 原型，业务主题是 “Santoip AI 商标品牌视频生成器”。

推荐状态：

```text
prototype_artifact_closeout_candidate
```

推荐动作：

1. 项目目录暂时保留为项目证据。
2. 不提交 `projects/santoip-ai-brand-video/`。
3. 不作为 PRD golden sample，也不作为稳定 UI 风格默认样例。
4. 可作为未来“业务 HTML 原型项目”候选案例，但需要和 C13 一起比较后再决定。
5. `.DS_Store` 和 HTML prototype zip 后续可列入 30 天后删除候选，但必须先归档并单独批准。

## 2. 当前证据

| 指标 | 当前结果 |
|---|---|
| 项目大小 | 236K |
| Git 状态 | 未跟踪项目目录 |
| closeout 扫描文件数 | 12 |
| PRD / 产品文档 | 未发现 |
| Codex 开发文档 | 未发现 |
| 用户故事 / pipeline manifest | 未发现 |
| 原型产物 | 有 HTML、standalone HTML、manifest、zip |
| 架构反哺强度 | 低到中，偏原型案例价值 |

## 3. 项目内容判断

主要文件集中在：

```text
projects/santoip-ai-brand-video/prototype/html/
projects/santoip-ai-brand-video/prototype/santoip-ai-brand-video-html-prototype.zip
projects/santoip-ai-brand-video/closeout/
```

`prototype_manifest.json` 显示它是一个中保真 interactive HTML 原型，核心页面包括：

- 线索详情页
- 填写品牌信息页
- 品牌方案生成中页
- AI 品牌生成结果页
- 品牌视频案例与领取报告弹窗背景页
- 后台线索管理页

这些内容有业务原型参考价值，尤其适合后续验证“PRD -> 原型 -> HTML”的链路。但当前缺少 PRD、范围、验收、开发边界和治理反馈，不适合进入稳定主链路。

## 4. 风险

| 风险 | 影响 | 建议 |
|---|---|---|
| 只有原型，没有 PRD | 无法判断需求边界和验收标准。 | 不作为 PRD 样例。 |
| closeout 业务目标为 `unknown` | 背景不足，不能直接反哺模板。 | 保持项目证据，不转 stable。 |
| 项目有商标 / 品牌 / 线索转化场景 | 可能涉及外部业务语境，不能随意外发。 | 不提交项目产物，不对外发布。 |
| HTML / zip 是过程产物 | 容易污染治理提交。 | 项目内保留，归档前再审。 |

## 5. 文件处置建议

| 文件 / 目录 | 建议 | 原因 |
|---|---|---|
| `prototype/html/` | 项目内保留 | 是主要原型证据。 |
| `prototype/santoip-ai-brand-video-html-prototype.zip` | 归档前再审 | zip 是重复打包产物，不能直接提交或删除。 |
| `closeout/` | 项目内保留 | 当前 closeout 可证明它是低证据原型项目。 |
| `.DS_Store` | 30 天删除候选 | 系统文件，无长期价值，但仍需精确删除审批。 |

## 6. 架构反哺候选

当前没有强稳定规则候选。

可弱保留的经验候选：

| 候选 | 当前建议 |
|---|---|
| 业务 HTML 原型应明确页面、动作、状态和路由上下文传递 | 已在 prototype manifest 中体现，可作为后续原型质量检查参考。 |
| 原型项目没有 PRD 时，只能作为原型证据，不能反推需求稳定规则 | 与 C13 一起作为项目产物边界案例。 |
| AI 生成类业务页需要区分用户路径和后台路径 | 可在具体项目中参考，不进入通用 PRD 模板。 |

## 7. 需要你后续拍板

| 拍板项 | 我的建议 | 不同选择的效果 |
|---|---|---|
| 是否提交 C14 审查报告 | 后续和 C12 / C13 一起作为项目审查记录候选提交 | 提交可保留判断依据；不提交则继续留在未跟踪 proposal。 |
| 是否归档项目目录 | 暂缓 | 等 C 批剩余项目全部审完后统一处理更稳。 |
| 是否删除 `.DS_Store` 或 zip | 不现在删 | 保持受监督，避免破坏项目证据。 |
| 是否提炼为 UI / UX 原型案例 | 暂缓 | 它比 C13 更有业务完整度，但仍缺 PRD，需要后续和更多项目比较。 |

## 8. 本轮不做

- 不提交 `projects/santoip-ai-brand-video/`。
- 不删除 `.DS_Store`。
- 不删除 zip。
- 不移动到 archive。
- 不改 PRD 模板、prompt、UI style selector 或 harness。
- 不把项目经验写入长期记忆。

## 9. 推荐状态变更

建议在台账中把 C14 从：

```text
next
```

更新为：

```text
prototype_artifact_closeout_candidate
```

下一步进入 C15 `temp-generated-project` 临时项目审查，或先汇总 C12-C16 项目产物审查结果。
