# 产品价值门禁 V0 最终 Staging 清单

- 日期：2026-05-08
- 状态：最终 staging 清单，尚未执行 `git add`
- 审查结论：`ready_for_staging_list`
- 重要边界：本文件是用户拍板材料，不等于批准 staging、commit、push、删除或归档

## 1. V0 提交意图

本批次目标是把「产品价值门禁」作为独立于 PRD 的前置判断中枢落地到主链路里。

落地后的效果：

- 用户输入想法后，先生成 `00_value_gate.json` 和 `00_value_gate.md`。
- 价值门禁先判断是否值得进入完整 PRD，而不是直接写 PRD。
- 只有 `A_ENTER_PRD` 才允许正式完整 PRD。
- `B/C/D/E/F/G` 只能进入低成本 MVP、客户项目验证、内部提效、调研补全、停止或禁止推进路径。
- `--fast-draft` 可以显式绕过，但 manifest 必须记录 `value_gate_bypassed: true`。
- PRD 模块二次校验 `decision_gate`，防止直接调用脚本绕过前置门禁。
- `产品临时.txt` 里的能力先作为目标能力和冲突对照保留，V0 不自动新增 skill / harness，不自动联网，不自动写长期记忆。

## 2. 允许 Staging 的 12 个文件

本清单只允许纳入以下 12 个文件。

| # | Path | Role |
|---:|---|---|
| 1 | `pm-prd-copilot/scripts/generate_value_gate.py` | 新增 V0 价值门禁生成脚本。 |
| 2 | `shared/schemas/value_gate.schema.json` | 新增机器可读 schema，固定门禁结果结构。 |
| 3 | `pm-prd-copilot/scripts/pipeline_common.py` | 新增价值门禁规则、Markdown 输出、PRD 输入包转换和门禁判断。 |
| 4 | `pm-prd-copilot/scripts/run_pipeline.py` | 新增 `value_gate` stage，并在正式 PRD 前执行门禁。 |
| 5 | `pm-prd-copilot/scripts/generate_prd.py` | 增加 PRD 二次门禁，防止绕过 `decision_gate`。 |
| 6 | `pm-prd-copilot/scripts/generate_requirement_brief.py` | 让 brief 读取价值门禁输入包作为 seed。 |
| 7 | `pm-prd-copilot/scripts/governance_trace.py` | manifest / trace 记录 `value_gate` 和 `value_gate_bypassed`。 |
| 8 | `pm-prd-copilot/scripts/run_regression.py` | 增加价值门禁规则、PRD 阻断和 fast draft bypass 回归。 |
| 9 | `registry/artifacts.yaml` | 注册 `value_gate` / `value_gate_markdown` artifact。 |
| 10 | `registry/skills.yaml` | 让已有 `source-collector` / `prd-draft-writer` 声明读写价值门禁产物。 |
| 11 | `workflow/actions.yaml` | 注册 `evaluate_product_value` action，并让 PRD action 读取 `value_gate`。 |
| 12 | `workflow/prd_workflow.yaml` | 将 `value_gate` 纳入 intake 必要产物。 |

## 3. 未来如获批准，只能使用的精确 Staging 命令

只有在用户明确批准「产品价值门禁 V0 staging」后，才可执行：

```bash
git add pm-prd-copilot/scripts/generate_value_gate.py shared/schemas/value_gate.schema.json pm-prd-copilot/scripts/pipeline_common.py pm-prd-copilot/scripts/run_pipeline.py pm-prd-copilot/scripts/generate_prd.py pm-prd-copilot/scripts/generate_requirement_brief.py pm-prd-copilot/scripts/governance_trace.py pm-prd-copilot/scripts/run_regression.py registry/artifacts.yaml registry/skills.yaml workflow/actions.yaml workflow/prd_workflow.yaml
```

不得使用：

```bash
git add .
git add pm-prd-copilot/
git add registry/
git add workflow/
git add docs/
git add projects/
```

## 4. 禁止混入范围

本批次不得包含：

- `projects/*`
- `memory-cache/*`
- `ai-intel/raw/*`
- `docs/archive/*`
- 其他 `docs/proposals/*`
- `.github/*`
- `.agents/*`
- `plugins/*`
- root 删除项
- 任何 PNG、HTML、B 包、closeout、run outputs
- 任何新增 skill / harness 文件
- 任何长期记忆文件变更

## 5. Staging 后验证方式

如果用户后续批准执行 staging，执行后必须立刻运行：

```bash
git diff --cached --name-only
```

期望输出必须严格等于：

```text
pm-prd-copilot/scripts/generate_prd.py
pm-prd-copilot/scripts/generate_requirement_brief.py
pm-prd-copilot/scripts/generate_value_gate.py
pm-prd-copilot/scripts/governance_trace.py
pm-prd-copilot/scripts/pipeline_common.py
pm-prd-copilot/scripts/run_pipeline.py
pm-prd-copilot/scripts/run_regression.py
registry/artifacts.yaml
registry/skills.yaml
shared/schemas/value_gate.schema.json
workflow/actions.yaml
workflow/prd_workflow.yaml
```

如果 staged 范围多出任何文件，必须停止，不 commit，并只撤销本批次 staged 状态。

## 6. Staging 后回滚方式

如需撤销 staged 状态，只撤销这 12 个文件：

```bash
git restore --staged pm-prd-copilot/scripts/generate_value_gate.py shared/schemas/value_gate.schema.json pm-prd-copilot/scripts/pipeline_common.py pm-prd-copilot/scripts/run_pipeline.py pm-prd-copilot/scripts/generate_prd.py pm-prd-copilot/scripts/generate_requirement_brief.py pm-prd-copilot/scripts/governance_trace.py pm-prd-copilot/scripts/run_regression.py registry/artifacts.yaml registry/skills.yaml workflow/actions.yaml workflow/prd_workflow.yaml
```

如果需要撤销工作区内容变更，必须另行获得用户明确批准；本清单不批准恢复或删除任何工作区文件。

## 7. Staging 前检查命令

执行真正 staging 前，建议再跑：

```bash
PYTHONPYCACHEPREFIX=/tmp/pycache python3 -m py_compile pm-prd-copilot/scripts/generate_value_gate.py pm-prd-copilot/scripts/pipeline_common.py pm-prd-copilot/scripts/generate_requirement_brief.py pm-prd-copilot/scripts/generate_prd.py pm-prd-copilot/scripts/run_pipeline.py pm-prd-copilot/scripts/governance_trace.py pm-prd-copilot/scripts/run_regression.py
python3 -m json.tool shared/schemas/value_gate.schema.json >/tmp/value_gate_schema_check.json
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

## 8. 本轮动作边界

本轮仅新增本清单文档。

- 未执行 `git add`。
- 未执行 commit / push / PR。
- 未删除、恢复、移动、归档。
- 未生成项目产物。
- 未提交 `projects/*`、`memory-cache/*`、`ai-intel/raw/*`。
- 未新增 skill / harness。

## 9. 下一步建议

如果用户认可本清单，下一步再单独申请：

```text
产品价值门禁 V0 精确 Staging 执行方案
```

该下一步只会按第 3 节命令暂存 12 个文件，并立即核对暂存区范围；仍不 commit。
