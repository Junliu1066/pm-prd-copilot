# A2 Governance Contract Staging 前审查

- 日期：2026-04-29
- 状态：staging 前审查材料，不批准 staging / commit / push
- 审查范围：A2 Pipeline / Workflow / Harness 治理合同
- 结论：`ready_for_staging_list`
- 前提：真正 staging 仍需用户明确批准

## 1. A2 稳定目标

A2 的目标是防止治理合同被执行链路绕过：

- pipeline 默认走 governed 路径。
- 只有显式 `--fast-draft` 才允许草稿绕过审批门禁。
- `--governed` 保留为兼容参数，但默认已等同 governed。
- manifest / trace 必须记录 `governance_mode` 和 `approval_gate_enforced`。
- workflow / actions / artifacts 必须注册一致，不能再出现 workflow 引用未注册 action。
- harness 默认 `--check-only`，不写项目报告；只有显式 `--write-report` 才允许写报告。

## 2. A2 文件范围

本单元只覆盖以下 16 个 tracked 文件。

| Group | Path | Role |
|---|---|---|
| Pipeline | `pm-prd-copilot/scripts/run_pipeline.py` | 默认 governed，显式 `--fast-draft`。 |
| Trace | `pm-prd-copilot/scripts/governance_trace.py` | 写入治理模式和审批标记。 |
| Regression | `pm-prd-copilot/scripts/run_regression.py` | 覆盖 governed 阻断、fast draft 放行、demo governed manifest。 |
| Workflow | `workflow/actions.yaml` | action 合同注册。 |
| Workflow | `workflow/policies.yaml` | workflow 政策。 |
| Workflow | `workflow/prd_workflow.yaml` | PRD workflow 阶段和审批门禁。 |
| Registry | `registry/artifacts.yaml` | artifact 合同和 raw input 边界。 |
| Registry | `registry/stewards.yaml` | steward 责任注册。 |
| Governance | `governance/steward_operating_rules.yaml` | steward 操作规则。 |
| Governance | `governance/teaching_policy.yaml` | teaching / learning / 长期记忆边界。 |
| Harness | `harness/README.md` | harness 使用说明。 |
| Harness | `harness/common.py` | harness 共用逻辑。 |
| Harness | `harness/run_harness.py` | `--check-only` / `--write-report` 主入口。 |
| Harness | `harness/workflow_gate_checker.py` | workflow/action/artifact 漂移检查。 |
| Harness | `harness/efficiency_auditor.py` | 效率审计。 |
| Harness | `harness/random_audit_inspector.py` | 随机审计。 |

当前 A2 diff stat：

```text
16 files changed, 1365 insertions(+), 83 deletions(-)
```

## 3. 当前证据

关键词和代码证据显示：

- `run_pipeline.py` 中 `--fast-draft` 与 `--governed` 互斥。
- pipeline 使用 `governance_mode = "governed"` 或 `governance_mode = "fast_draft"`。
- `governance_trace.py` 写入 `governance_mode` 和 `approval_gate_enforced`。
- `run_regression.py` 覆盖 default governed、显式 governed、fast draft、demo governed manifest。
- `run_harness.py` 提供 `--check-only` 和 `--write-report`，二者互斥。
- harness 输出包含 `No project files written. Use --write-report to refresh harness reports.`。
- `workflow_gate_checker.py` 会检查 workflow/action/artifact 漂移，以及非 governed / 非 fast draft 的绕行风险。

## 4. 能否进入下一步 staging 清单

结论：`ready_for_staging_list`

理由：

- A2 文件范围明确，均属于 pipeline / workflow / registry / harness 治理合同。
- A2 不混入项目产物、不混入 candidate plugin、不混入 root 删除项。
- 当前 regression 和 harness check-only 已在 A1 commit 前后多次通过。
- 该组直接修复“workflow 写完整但 pipeline 绕过”的核心风险。

仍需用户在 staging 前确认：

- 是否接受 A2 作为独立 commit 单元。
- 是否接受 pipeline 默认 governed。
- 是否接受 `--fast-draft` 是唯一草稿绕行路径。
- 是否接受 harness / CI 默认 `--check-only`，不写项目文件。

## 5. A2 禁止混入范围

A2 staging 清单不得包含：

- A1 已提交文件。
- A3 新增 eval / checker 文件。
- A4 B 包、closeout、Codex 开发文档模板、长期偏好边界。
- `projects/*`
- `plugins/*`
- `memory-cache/*`
- root 删除项。
- `docs/proposals/*` 审查材料。

## 6. Staging 前检查命令

准备 A2 staging 清单前建议再次运行：

```bash
python3 -m py_compile pm-prd-copilot/scripts/run_pipeline.py pm-prd-copilot/scripts/run_regression.py harness/run_harness.py harness/workflow_gate_checker.py
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

## 7. 本轮动作边界

本轮只新增本审查材料。

- 未批准 A2 staging。
- 未批准 A2 commit。
- 未批准 push / PR。
- 未批准删除、恢复、移动、归档。
- 未批准写项目报告。
