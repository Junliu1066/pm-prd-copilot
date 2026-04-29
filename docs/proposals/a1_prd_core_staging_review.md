# A1 PRD 主链路 Staging 前审查

- 日期：2026-04-29
- 状态：staging 前审查材料，不批准 staging / commit / push
- 审查范围：A1 PRD 主链路与输出口径
- 结论：`ready_for_staging`
- 前提：真正 staging 仍需用户明确批准

## 1. 用户已确认的 A1 稳定口径

本轮按以下规则审查 A1：

- PRD 正文必须包含：页面说明、页面跳转关系、原型图层。
- 图表放在对应章节，不再集中输出一个“PRD 可视化层”。
- PRD 正文只放示意图、结构图、页面级低保真原型图或引用说明。
- PNG 可以单独输出到项目文件夹，例如 `projects/<project>/prototype/png/`，但 PNG 属于项目产物，不属于 Stable Core 文件。
- PNG / HTML / 完整原型 / 高保真 UI 不作为 PRD 阶段默认必交付物；在用户确认进入原型/UI 阶段后再输出。
- 没有涉及 AI 能力的项目，不写 AI 模型选型。
- 涉及 AI 生成、识别、推荐、Agent、RAG、审核、语音、图像或多模态能力时，才写 AI 模型选型、评测、成本、fallback 和合规边界。
- 短期接受维护成本，优先稳定；核心链路稳定后再做瘦身和降成本。

## 2. A1 文件范围

本单元只覆盖 8 个文件，不混入项目产物、candidate 能力、A2/A3/A4 或 root 删除项。

| Group | Path | Current status | Review result |
|---|---|---|---|
| Skill 指令 | `pm-prd-copilot/SKILL.md` | modified | 符合 A1 方向：PRD 阶段不默认生成 PNG / HTML / 完整原型。 |
| 输出风格 | `pm-prd-copilot/references/output_style_guide.md` | modified | 符合 A1 方向：输出风格不再要求默认线框图和 AI 选型。 |
| Playbook | `pm-prd-copilot/references/prd_pm_2026_playbook.md` | modified | 可进入 A1；未发现会强制旧口径的 live 指令。 |
| 模板 | `pm-prd-copilot/templates/prd_template_2026.md` | modified | 符合 A1 方向：页面说明、页面跳转关系、原型图层均在对应章节。 |
| Schema | `shared/schemas/prd_document.schema.json` | modified | 可进入 A1；支撑 PRD 结构合同。 |
| Pipeline | `pm-prd-copilot/scripts/pipeline_common.py` | modified | 符合 A1 方向：条件生成原型图层和 AI 模型选型。 |
| Prompt | `pm-prd-copilot/scripts/prompt_builders.py` | modified | 可进入 A1；承担 PRD prompt 边界。 |
| Router | `pm-prd-copilot/scripts/router.py` | modified | 可进入 A1；承担项目/输出路由边界。 |

当前 A1 diff stat：

```text
8 files changed, 837 insertions(+), 123 deletions(-)
```

## 3. 当前变更摘要

### 模板 / 文档层

- PRD 模板把页面说明、页面跳转关系、原型图层放在业务流程附近，而不是集中放“可视化层”。
- 原型图层被定义为 PRD 阶段的低保真参考，服务于 UI 设计、原型确认和 Codex 开发文档承接。
- PNG、HTML、完整原型、高保真 UI 被明确排除为 PRD 阶段默认必交付物。
- AI 模型选型被限定为涉及 AI 能力时必备，普通业务项目不默认输出。

### Prompt / Pipeline 层

- pipeline 生成结构中包含页面说明、页面跳转关系、原型图层。
- AI 模型选型只在项目涉及 AI 能力时输出。
- 原型图层与页面说明、页面跳转关系保持一致，不作为独立堆叠章节。
- PNG / HTML / 高保真 UI 的输出被放到用户确认后的后续阶段。

### Schema / Contract 层

- schema 支撑 PRD 的页面、流转、原型图层等结构化字段。
- A1 不引入新的 workflow stage、harness、skill 或 plugin。

## 4. 旧口径残留检查

对 A1 8 个文件做了关键词检查。

| Check item | Result | Notes |
|---|---|---|
| `PRD 可视化层` | 未发现 live 残留 | A1 文件中未发现集中式章节旧口径。 |
| `原型图 / 线框图` | 未发现 live 残留 | A1 文件中未发现默认线框图旧口径。 |
| `Do not skip the PRD visualization layer` | 未发现 | 英文旧指令未残留。 |
| `Do not skip PRD flowcharts, wireframes, or AI model selection` | 未发现 | 英文旧指令未残留。 |
| 非 AI 默认 `AI 模型选型` | 未发现 | 仅发现条件语境：涉及 AI 能力时输出。 |
| PNG / HTML 默认必交付 | 未发现 | 当前口径是不默认输出，需用户确认进入原型/UI 阶段。 |
| 页面说明 | 已覆盖 | 模板和 pipeline 均覆盖。 |
| 页面跳转关系 | 已覆盖 | 模板和 pipeline 均覆盖。 |
| 原型图层 | 已覆盖 | 模板和 pipeline 均覆盖。 |

## 5. PNG 输出边界

当前 A1 文件的口径是：PRD 阶段不默认输出 PNG、HTML、完整原型或高保真 UI，除非用户确认进入原型/UI 阶段。

这与用户确认的长期口径兼容：

- PRD 正文可以放示意图、结构图、页面级低保真图或引用说明。
- PNG 可以单独输出到项目文件夹，但它是项目产物，不是 Stable Core。
- 推荐后续产物路径：`projects/<project>/prototype/png/`。
- PNG 是否保留、归档或 30 天后删除，跟随项目 closeout 审核，不随 A1 提交。

当前不建议为了 PNG 额外改 A1 代码；如果后续希望路径更明确，可以在原型链路或项目产物规则中补充，不应扩大 A1 范围。

## 6. 能否进入下一步 staging

结论：`ready_for_staging`

理由：

- A1 文件范围清楚，只有 8 个稳定主链路文件。
- 未发现旧的集中式 PRD 可视化层要求。
- 未发现默认线框图要求。
- 未发现非 AI 项目默认 AI 模型选型要求。
- 页面说明、页面跳转关系、原型图层已覆盖。
- PNG / HTML / 完整原型没有被写成 PRD 阶段默认必交付物。

仍需用户在 staging 前确认：

- 是否按这 8 个文件准备 A1 staging 清单。
- 是否接受 PNG 作为项目产物，不随 A1 stable core 提交。
- 是否确认历史项目 PRD 旧口径延后回扫。

## 7. A1 staging 禁止混入

A1 staging 清单不得包含：

- `projects/*`
- `plugins/*`
- A2 文件：pipeline governed、workflow、harness 合同之外的文件
- A3 文件：新增 eval / checker 文件
- A4 文件：B 包、closeout、Codex 开发文档模板、长期偏好边界
- root 删除项：`prd_pm_2026_playbook.md`、`prd_template_2026.md`、`prd_skill_kit_2026.zip`、`skill_suite_overview.md`
- PNG、HTML、B 包 zip、closeout 五件套、run outputs

## 8. 提交前检查命令

A1 staging 前建议再次运行：

```bash
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

## 9. 本轮动作边界

本轮只新增本审查材料。

- 未批准 `git add`。
- 未批准 commit / push / PR。
- 未批准删除、恢复、移动、归档。
- 未批准生成 PNG、HTML 或项目产物。
- 未批准修改 A1 代码文件。
- 未批准将 A2/A3/A4 混入 A1。
