# C12 AI 协作效率平台 Closeout 刷新审查

- 日期：2026-05-03
- 状态：proposal / project artifact review，不是 stable policy。
- 授权等级：L1 审查与台账更新；不执行 L2 staging / commit，不执行 L3 删除 / 归档。
- 主线任务：刷新 `ai-collaboration-efficiency-platform` 的 closeout 证据，判断项目产物是否可收口、是否有架构反哺价值、是否能进入后续归档或提交候选。

## 1. 结论

`projects/ai-collaboration-efficiency-platform` 是高价值项目证据，但不能直接提交项目产物，也不能直接归档或清理。

推荐状态：

```text
closeout_candidate_refreshed
```

推荐动作：

1. 保留项目目录作为项目证据。
2. 不提交 `projects/ai-collaboration-efficiency-platform/`。
3. 不用旧 closeout 五件套作为归档依据。
4. 后续如果要提交，只提交项目 closeout 审查报告或脱敏后的架构反哺，不提交原项目全文、HTML 原型、PNG 或 zip。
5. 后续如果要归档，必须先做 L3 单独审批。

## 2. 为什么需要刷新

旧 closeout 报告生成于 `2026-04-29T03:36:25+00:00`，只扫描到 1 个文件：

```text
projects/ai-collaboration-efficiency-platform/AI协作效率平台_PRD_完整测试版_v1.0.md
```

但当前项目目录实际情况：

| 指标 | 当前结果 |
|---|---|
| 实际文件数 | 45 |
| 项目大小 | 15M |
| 临时刷新 closeout 扫描数 | 40 |
| 临时刷新 closeout 总大小 | 15,387,325 bytes |

说明旧 closeout 证据过期或生成时上下文不完整，不能作为清理、归档或提交依据。

## 3. 本次刷新方式

只在临时目录生成 closeout 预览，不写回项目：

```bash
python3 pm-prd-copilot/scripts/closeout_project.py --base-dir . --project ai-collaboration-efficiency-platform --output-dir /private/tmp/c12-ai-collab-closeout
```

临时输出：

```text
/private/tmp/c12-ai-collab-closeout/manifest.json
/private/tmp/c12-ai-collab-closeout/closeout-report.md
/private/tmp/c12-ai-collab-closeout/architecture-feedback.md
/private/tmp/c12-ai-collab-closeout/cleanup-plan.md
/private/tmp/c12-ai-collab-closeout/preference-memory-disposition.md
```

本轮未写入：

- `projects/ai-collaboration-efficiency-platform/closeout/`
- `memory-cache/`
- `docs/archive/`
- stable docs
- git staging area

## 4. 项目价值

这个项目的价值不是作为普通 PRD golden sample，而是作为“复杂 AI / Skill 治理产品交付链路”的项目证据。

| 价值点 | 说明 |
|---|---|
| 产品文档完整 | 包含定位、角色、流程、模块、评分模型、权限矩阵、风险分级、成功指标、待确认问题。 |
| Codex 开发文档完整 | 包含边界、技术架构、领域模型、状态机、API、权限、测试、上线和回滚。 |
| 辅助理解图完整 | 包含思维导图、流程图、泳道图、状态机、路由决策树、风险闭环。 |
| 原型链路完整 | 有页面级原型说明、HTML 原型、standalone HTML、PNG 参考图和 zip 包。 |
| 治理议题高度相关 | 覆盖 Skill 调用、Review、评分、知识沉淀、权限、风控、审计，和本仓库治理方向有关。 |

## 5. 主要风险

| 风险 | 影响 | 建议 |
|---|---|---|
| 文档含绝对路径 | 可能泄露本地路径或微信临时文件来源。 | 不外发，不直接提交为 stable 样例。 |
| 项目里有 HTML / PNG / zip 原型包 | 项目产物重，容易污染治理提交。 | 项目内保留，归档前再逐项处理。 |
| `06_prototype_wireframes.md` 使用旧“线框图”口径 | 与最新 PRD 原型图层规则不完全一致。 | 作为历史项目证据保留，不反向污染新规则。 |
| closeout 反哺信息较少 | 临时刷新仍没有提取出强 prompt/template 回归候选。 | 先不改 stable prompt / template。 |
| 项目与治理框架高度相关 | 容易把项目产品概念误当仓库治理规则。 | 只进入 architecture inbox 候选，不能直接长期化。 |

## 6. 文件处置建议

### 6.1 应项目内保留

| 文件 / 目录 | 建议 | 原因 |
|---|---|---|
| `00_source_notes.md` | 保留 | 含输入来源、生成说明和交付边界。 |
| `01_product_document.md` | 保留 | 产品文档完整，有项目证据价值。 |
| `02_development_document.md` | 保留 | Codex 开发文档证据完整。 |
| `03_delivery_check.md` | 保留 | 记录交付范围和两轮检查。 |
| `04_mindmaps.md` | 保留 | 辅助理解图证据。 |
| `05_flowcharts.md` | 保留 | 流程、状态和风控图证据。 |
| `06_prototype_wireframes.md` | 保留但不升级规则 | 页面级原型说明有价值，但术语是历史口径。 |
| `AI协作效率平台_PRD_完整测试版_v1.0.md` | 保留 | 原 PRD 证据。 |

### 6.2 归档前再审

| 文件 / 目录 | 建议 | 原因 |
|---|---|---|
| `prototype/html/` | 归档前审 | 是完整 HTML 原型，体积不小，但有交付链路价值。 |
| `prototype/images/` | 归档前审 | PNG 参考图有价值，但不应进 stable。 |
| `prototype/ai-collaboration-efficiency-html-prototype.zip` | 归档前审 | zip 可能重复，可后续与 package / zip 生命周期策略一起处理。 |
| `.DS_Store` | 30 天删除候选 | 系统生成物，无长期价值，但仍需进入精确删除清单。 |

## 7. 架构反哺候选

只作为候选，不直接改稳定规则：

| 候选 | 价值 | 当前建议 |
|---|---|---|
| PRD -> Codex 开发文档 -> 图表 -> 页面级原型 -> HTML 原型链路 | 这个项目完整覆盖了一次从文档到原型的项目链路。 | 后续可作为“复杂项目交付链路”案例候选。 |
| 页面级原型和大图参考分离 | `06_prototype_wireframes.md` 明确原始大图只是参考，页面原型需要重建。 | 可进入 prototype flow 经验候选，但不直接 stable。 |
| AI / Skill 治理产品的权限与风控模型 | 项目内容与本仓库治理思想接近。 | 保持项目证据，不把产品机制直接写成架构规则。 |
| 交付检查中的两轮自检 | `03_delivery_check.md` 有 Round 1 / Round 2 记录。 | 可作为项目交付检查样例候选。 |

## 8. 不建议做

- 不提交 `projects/ai-collaboration-efficiency-platform/`。
- 不把它做成普通 PRD golden sample。
- 不把项目里的 Skill / Review / 权限机制直接写成仓库 stable policy。
- 不直接归档整个项目。
- 不删除 `.DS_Store`、zip、PNG 或 HTML。
- 不用旧 closeout 五件套作为归档依据。
- 不把项目偏好写入长期记忆。

## 9. 后续建议

### L1 可继续自动做

- 更新台账状态。
- 把 C12 加入 proposal 生命周期处置表。
- 跑 check-only。
- 后续对低证据项目继续做同类只读审查。

### L2 需要批量审批

| 批量审批项 | 我的建议 | 效果 |
|---|---|---|
| 是否提交 C12 审查报告 | 先不急，后续和 C9 / C10 / C11 proposal 决策记录一起处理 | 避免 proposal 过多碎提交。 |
| 是否生成脱敏架构反哺摘要 | 暂缓 | 当前反哺候选还不够强，直接提炼成本高。 |
| 是否把项目作为复杂交付链路候选案例 | 保持 candidate | 后续和 Jiaxiaoqian、graduation-defense 组合比较更稳。 |

### L3 必须单独审批

- 归档项目。
- 删除 `.DS_Store`、zip、PNG、HTML。
- 清空或迁移项目偏好缓存。
- 对外发布项目文档或原型。
- 把项目经验写入 stable policy 或长期记忆。

## 10. 推荐状态变更

建议在台账中把 C12 从：

```text
closeout_candidate_needs_refresh
```

更新为：

```text
closeout_candidate_refreshed
```

下一步可进入 C13 / C14 低证据项目审查，或先做项目 zip / package 生命周期策略。
