# C13 Prompt Optimization Workbench 低证据项目审查

- 日期：2026-05-03
- 状态：proposal / low-evidence project review，不是 stable policy。
- 授权等级：L1 审查与台账更新；不执行 L2 staging / commit，不执行 L3 删除 / 归档。
- 主线任务：判断 `prompt-optimization-workbench` 是否仍有项目价值，避免把单一 HTML 原型误当成稳定架构资产。

## 1. 结论

`projects/prompt-optimization-workbench` 当前不是完整 PRD 项目，也不是稳定架构输入。它更像一次“评测报告详情页 / Prompt 工作台”的 HTML 原型输出。

推荐状态：

```text
prototype_artifact_closeout_candidate
```

推荐动作：

1. 项目目录暂时保留为项目证据。
2. 不提交 `projects/prompt-optimization-workbench/`。
3. 不把它作为 PRD golden sample、prompt 模板样例或 UI 默认风格样例。
4. 后续如果做项目归档，可把它作为“HTML 原型产物候选”处理。
5. `.DS_Store` 和 zip 后续可列入 30 天后删除候选，但必须先归档并单独批准。

## 2. 当前证据

| 指标 | 当前结果 |
|---|---|
| 项目大小 | 288K |
| Git 状态 | 未跟踪项目目录 |
| closeout 扫描文件数 | 12 |
| PRD / 产品文档 | 未发现 |
| Codex 开发文档 | 未发现 |
| 用户故事 / manifest 产物清单 | 未发现 |
| 原型产物 | 有 HTML、standalone HTML、manifest、zip |
| 架构反哺强度 | 低 |

## 3. 项目内容判断

主要文件集中在：

```text
projects/prompt-optimization-workbench/prototype/html/
projects/prompt-optimization-workbench/prototype/evaluation-report-detail-html-prototype.zip
projects/prompt-optimization-workbench/closeout/
```

`prototype_manifest.json` 显示这是一个中保真 interactive HTML 原型，核心页面包括：

- 评测报告详情页
- 创建 Prompt 页面
- Prompt 详情与编辑页
- Optimize 方案详情与回归测试页
- Run 任务详情页
- Models 页面
- Review 评审详情页
- 发布与知识沉淀页
- 失败分析详情页

这些内容对“后期 UI / UX 原型链路”有参考价值，但缺少产品定位、范围、验收、治理决策和开发边界，不适合进入稳定主链路。

## 4. 风险

| 风险 | 影响 | 建议 |
|---|---|---|
| 只有原型，没有 PRD | 容易把视觉原型误当成产品需求。 | 不作为 PRD 样例。 |
| closeout 业务目标为 `unknown` | 项目背景不足，无法反哺模板。 | 不进入 architecture inbox stable 候选。 |
| HTML / zip 是项目过程产物 | 容易污染治理提交。 | 项目内保留，归档前再审。 |
| 页面内容和 AI / Prompt 评测相关 | 可能误导为本仓库稳定 AI 能力。 | 只作项目证据，不转 stable policy。 |

## 5. 文件处置建议

| 文件 / 目录 | 建议 | 原因 |
|---|---|---|
| `prototype/html/` | 项目内保留 | 是主要原型证据。 |
| `prototype/evaluation-report-detail-html-prototype.zip` | 归档前再审 | zip 是重复打包产物，不能直接提交或删除。 |
| `closeout/` | 项目内保留 | 当前 closeout 可证明它是低证据原型项目。 |
| `.DS_Store` | 30 天删除候选 | 系统文件，无长期价值，但仍需精确删除审批。 |

## 6. 架构反哺候选

当前没有强稳定规则候选。

可弱保留的经验候选：

| 候选 | 当前建议 |
|---|---|
| Prompt / Eval 类产品可能需要 report -> optimize -> review -> release 的页面链路 | 仅作为未来具体项目参考，不进入稳定模板。 |
| HTML 原型必须和 PRD / 页面说明分开管理 | 已被 A1 / C16 覆盖，不需要新增规则。 |

## 7. 需要你后续拍板

| 拍板项 | 我的建议 | 不同选择的效果 |
|---|---|---|
| 是否提交 C13 审查报告 | 后续和 C12 / C14 一起作为项目审查记录候选提交 | 提交可保留判断依据；不提交则继续留在未跟踪 proposal。 |
| 是否归档项目目录 | 暂缓 | 现在归档过早；等 C14 和剩余项目审完后统一处理更稳。 |
| 是否删除 `.DS_Store` 或 zip | 不现在删 | 保持受监督，避免破坏项目证据。 |
| 是否提炼为 UI / UX 样例 | 暂不提炼 | 证据太薄，容易过拟合。 |

## 8. 本轮不做

- 不提交 `projects/prompt-optimization-workbench/`。
- 不删除 `.DS_Store`。
- 不删除 zip。
- 不移动到 archive。
- 不改 PRD 模板、prompt、UI style selector 或 harness。
- 不把项目经验写入长期记忆。

## 9. 推荐状态变更

建议在台账中把 C13 从：

```text
next
```

更新为：

```text
prototype_artifact_closeout_candidate
```

下一步进入 C14 `santoip-ai-brand-video` 低证据项目审查。
