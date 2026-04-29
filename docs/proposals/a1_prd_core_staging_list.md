# A1 PRD 主链路最终 Staging 清单

- 日期：2026-04-29
- 状态：最终 staging 清单，尚未执行 `git add`
- 输入依据：`docs/proposals/a1_prd_core_staging_review.md`
- 审查结论：`ready_for_staging`
- 重要边界：本文件是用户拍板材料，不等于批准 staging、commit、push、删除或归档

## 1. A1 提交意图

A1 的目标是稳定 PRD 主链路口径：

- PRD 正文必须包含页面说明、页面跳转关系、原型图层。
- 图表放在对应章节，不再集中输出“PRD 可视化层”。
- PNG 可以单独输出到项目文件夹，但属于项目产物，不进入 Stable Core。
- 非 AI 项目不写 AI 模型选型。
- 涉及 AI 能力时，才写 AI 选型、评测、成本、fallback 和合规边界。

## 2. 允许 staging 的 8 个文件

本清单只允许纳入以下 8 个 A1 文件。

| # | Path | Role |
|---:|---|---|
| 1 | `pm-prd-copilot/SKILL.md` | 稳定 skill 入口，约束 PRD 默认输出。 |
| 2 | `pm-prd-copilot/references/output_style_guide.md` | 输出风格说明，防止旧口径回潮。 |
| 3 | `pm-prd-copilot/references/prd_pm_2026_playbook.md` | PRD playbook canonical copy。 |
| 4 | `pm-prd-copilot/templates/prd_template_2026.md` | PRD 模板主入口。 |
| 5 | `shared/schemas/prd_document.schema.json` | PRD 结构合同。 |
| 6 | `pm-prd-copilot/scripts/pipeline_common.py` | PRD 组装、章节和条件输出逻辑。 |
| 7 | `pm-prd-copilot/scripts/prompt_builders.py` | PRD prompt 边界。 |
| 8 | `pm-prd-copilot/scripts/router.py` | 项目/输出路由边界。 |

## 3. 未来如获批准，只能使用的精确 staging 命令

只有在用户明确批准 A1 staging 后，才可执行：

```bash
git add pm-prd-copilot/SKILL.md pm-prd-copilot/references/output_style_guide.md pm-prd-copilot/references/prd_pm_2026_playbook.md pm-prd-copilot/templates/prd_template_2026.md shared/schemas/prd_document.schema.json pm-prd-copilot/scripts/pipeline_common.py pm-prd-copilot/scripts/prompt_builders.py pm-prd-copilot/scripts/router.py
```

不得使用：

```bash
git add .
git add pm-prd-copilot/
git add docs/
git add projects/
```

## 4. 禁止混入 A1 staging 的范围

A1 staging 不得包含：

- `projects/*`
- `plugins/*`
- A2 文件：pipeline governed、workflow、registry、harness 合同等
- A3 文件：新增 eval / checker 文件
- A4 文件：B 包、closeout、Codex 开发文档模板、长期偏好边界
- root 删除项：`prd_pm_2026_playbook.md`、`prd_template_2026.md`、`prd_skill_kit_2026.zip`、`skill_suite_overview.md`
- PNG、HTML、B 包 zip、closeout 五件套、run outputs
- `.github/*`
- `ai-intel/*`
- `memory-cache/*`

## 5. Staging 后验证方式

如果用户后续批准执行 A1 staging，执行后必须立刻验证 staged 范围：

```bash
git diff --cached --name-only
```

期望输出必须严格等于：

```text
pm-prd-copilot/SKILL.md
pm-prd-copilot/references/output_style_guide.md
pm-prd-copilot/references/prd_pm_2026_playbook.md
pm-prd-copilot/scripts/pipeline_common.py
pm-prd-copilot/scripts/prompt_builders.py
pm-prd-copilot/scripts/router.py
pm-prd-copilot/templates/prd_template_2026.md
shared/schemas/prd_document.schema.json
```

如果 staged 范围多出任何文件，必须立即停止并向用户汇报，不能继续 commit。

## 6. Staging 后回滚方式

如需撤销 A1 staged 状态，只撤销这 8 个文件的 staged 状态：

```bash
git restore --staged pm-prd-copilot/SKILL.md pm-prd-copilot/references/output_style_guide.md pm-prd-copilot/references/prd_pm_2026_playbook.md pm-prd-copilot/templates/prd_template_2026.md shared/schemas/prd_document.schema.json pm-prd-copilot/scripts/pipeline_common.py pm-prd-copilot/scripts/prompt_builders.py pm-prd-copilot/scripts/router.py
```

如果需要撤销工作区内容变更，必须另行获得用户明确批准；本清单不批准恢复或删除任何工作区文件。

## 7. Staging 前检查命令

执行真正 staging 前，建议再跑：

```bash
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

## 8. 本轮动作边界

本轮仅新增本清单文档。

- 未执行 `git add`。
- 未执行 commit / push / PR。
- 未删除、恢复、移动、归档。
- 未生成 PNG / HTML / B 包 / closeout 产物。
- 未把 A2 / A3 / A4 混入 A1。
