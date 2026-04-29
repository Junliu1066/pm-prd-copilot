# A2 Governance Contract 最终 Staging 清单

- 日期：2026-04-29
- 状态：最终 staging 清单，不批准 staging / commit / push
- 输入材料：`docs/proposals/a2_governance_contract_staging_review.md`
- 审查结论：`ready_for_staging_list`
- 执行边界：本文件只用于用户拍板；真正 staging 必须再次获得明确批准

## 1. A2 提交意图

A2 的稳定目标是把治理合同压到执行链路里，避免再次出现“workflow 写得完整，但 pipeline / harness 实际绕过治理”的问题。

本批次只覆盖：

- pipeline 默认 governed。
- 只有显式 `--fast-draft` 才允许草稿绕过审批门禁。
- governance trace / manifest 明确记录治理模式和审批门禁状态。
- workflow / actions / artifacts 合同保持一致。
- harness 支持 `--check-only` / `--write-report`，日常检查默认只读。
- regression 覆盖 governed 阻断和 fast draft 放行。

## 2. 允许进入 A2 Staging 的精确文件

未来如果用户批准 A2 staging，只允许暂存以下 16 个文件。

| 序号 | 文件 | 归属 | 纳入原因 |
|---:|---|---|---|
| 1 | `pm-prd-copilot/scripts/run_pipeline.py` | Pipeline | 默认 governed，显式 `--fast-draft`。 |
| 2 | `pm-prd-copilot/scripts/governance_trace.py` | Trace | 记录 `governance_mode` 和 `approval_gate_enforced`。 |
| 3 | `pm-prd-copilot/scripts/run_regression.py` | Regression | 覆盖 default governed、显式 governed、fast draft 和 demo manifest。 |
| 4 | `workflow/actions.yaml` | Workflow | 注册 workflow 引用的 action 合同。 |
| 5 | `workflow/policies.yaml` | Workflow | 约束治理策略。 |
| 6 | `workflow/prd_workflow.yaml` | Workflow | 固定 PRD workflow 阶段和审批门禁。 |
| 7 | `registry/artifacts.yaml` | Registry | 固定 artifact 合同、`raw_input` 和边界。 |
| 8 | `registry/stewards.yaml` | Registry | 固定 steward 责任注册。 |
| 9 | `governance/steward_operating_rules.yaml` | Governance | 固定 steward 操作边界。 |
| 10 | `governance/teaching_policy.yaml` | Governance | 固定 teaching / learning / 长期记忆边界。 |
| 11 | `harness/README.md` | Harness | 说明 check-only / write-report 使用边界。 |
| 12 | `harness/common.py` | Harness | 共用检查逻辑。 |
| 13 | `harness/run_harness.py` | Harness | 主入口支持 `--check-only` / `--write-report`。 |
| 14 | `harness/workflow_gate_checker.py` | Harness | 检查 workflow/action/artifact 漂移和治理绕行风险。 |
| 15 | `harness/efficiency_auditor.py` | Harness | 效率审计纳入治理检查。 |
| 16 | `harness/random_audit_inspector.py` | Harness | 随机审计纳入治理检查。 |

## 3. 未来精确 Staging 命令

如果用户明确批准 A2 staging，只能使用下面这个精确命令：

```bash
git add pm-prd-copilot/scripts/run_pipeline.py pm-prd-copilot/scripts/governance_trace.py pm-prd-copilot/scripts/run_regression.py workflow/actions.yaml workflow/policies.yaml workflow/prd_workflow.yaml registry/artifacts.yaml registry/stewards.yaml governance/steward_operating_rules.yaml governance/teaching_policy.yaml harness/README.md harness/common.py harness/run_harness.py harness/workflow_gate_checker.py harness/efficiency_auditor.py harness/random_audit_inspector.py
```

禁止使用：

```bash
git add .
git add pm-prd-copilot/scripts
git add workflow
git add registry
git add governance
git add harness
git add docs/proposals
```

原因：这些宽泛命令会把 A3 checker、A4 脚本、proposal 文档、项目产物或候选能力一起带进暂存区。

## 4. Staging 后必须核对的结果

A2 staging 后必须立即运行：

```bash
git diff --cached --name-only
```

结果必须严格等于以下 16 个文件：

```text
governance/steward_operating_rules.yaml
governance/teaching_policy.yaml
harness/README.md
harness/common.py
harness/efficiency_auditor.py
harness/random_audit_inspector.py
harness/run_harness.py
harness/workflow_gate_checker.py
pm-prd-copilot/scripts/governance_trace.py
pm-prd-copilot/scripts/run_pipeline.py
pm-prd-copilot/scripts/run_regression.py
registry/artifacts.yaml
registry/stewards.yaml
workflow/actions.yaml
workflow/policies.yaml
workflow/prd_workflow.yaml
```

如果多出任何文件，必须停止，不 commit，并只撤销 A2 staged 状态：

```bash
git restore --staged pm-prd-copilot/scripts/run_pipeline.py pm-prd-copilot/scripts/governance_trace.py pm-prd-copilot/scripts/run_regression.py workflow/actions.yaml workflow/policies.yaml workflow/prd_workflow.yaml registry/artifacts.yaml registry/stewards.yaml governance/steward_operating_rules.yaml governance/teaching_policy.yaml harness/README.md harness/common.py harness/run_harness.py harness/workflow_gate_checker.py harness/efficiency_auditor.py harness/random_audit_inspector.py
```

不得使用 `git restore` 恢复工作区内容，除非用户另行批准。

## 5. A2 禁止混入范围

A2 staging 不得包含：

- A1 已提交文件：
  - `pm-prd-copilot/SKILL.md`
  - `pm-prd-copilot/references/output_style_guide.md`
  - `pm-prd-copilot/references/prd_pm_2026_playbook.md`
  - `pm-prd-copilot/templates/prd_template_2026.md`
  - `shared/schemas/prd_document.schema.json`
  - `pm-prd-copilot/scripts/pipeline_common.py`
  - `pm-prd-copilot/scripts/prompt_builders.py`
  - `pm-prd-copilot/scripts/router.py`
- A3 eval / checker 文件，例如：
  - `harness/eval_suite_checker.py`
  - `harness/real_output_eval_checker.py`
  - `harness/skill_generalization_checker.py`
  - `harness/prototype_preview_gate_checker.py`
  - `harness/external_redaction_checker.py`
  - `evals/*`
- A4 B 包 / closeout / Codex 开发文档模板 / 长期偏好边界。
- `projects/*`
- `plugins/*`
- `memory-cache/*`
- root 删除项。
- `docs/proposals/*`

## 6. Staging 前检查命令

真正 staging 前必须先跑：

```bash
python3 -m py_compile pm-prd-copilot/scripts/run_pipeline.py pm-prd-copilot/scripts/run_regression.py harness/run_harness.py harness/workflow_gate_checker.py
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

如果任一检查失败，不进入 staging。

## 7. 本轮未批准事项

本清单不批准：

- `git add`
- commit / push / PR
- 删除、恢复、移动、归档
- 写项目报告
- 把 A3 / A4 合并进 A2
- 把 candidate plugin 转 stable
- 把 proposal 文档混入稳定核心提交

## 8. 下一步建议

如果用户认可本清单，下一步再单独申请：

```text
A2 精确 Staging 执行方案
```

该下一步只会按第 3 节命令暂存 16 个 A2 文件，并立即核对暂存区范围；仍不 commit。
