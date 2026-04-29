# A3 必要检查与 Eval 基线 Staging 前审查

- 日期：2026-04-29
- 状态：staging 前审查材料，不批准 staging / commit / push
- 审查范围：A3 五个必要检查与 eval 基线
- 结论：`ready_for_staging_list`
- 前提：真正 staging 仍需用户明确批准

## 1. A3 稳定目标

A3 的目标是把已确认必要的 5 个检查稳定下来，防止已发生的问题复发：

- `eval_suite`：防 PRD 结构和质量退化。
- `real_output_eval`：用真实输出基线检查模型/模板变化。
- `skill_generalization`：防项目偏好错误泛化为长期规则。
- `prototype_preview_gate`：防原型越权，确保 PNG/HTML/完整原型只在确认后进入。
- `external_redaction`：防 B 包和外部分发泄漏内部治理内容。

本单元不新增第 6 个稳定检查。

## 2. A3 文件范围

本单元只覆盖以下 15 个 untracked 文件。

| Group | Path | Role |
|---|---|---|
| Harness | `harness/eval_suite_checker.py` | 必要检查：PRD/eval 覆盖。 |
| Harness | `harness/real_output_eval_checker.py` | 必要检查：真实输出基线。 |
| Harness | `harness/skill_generalization_checker.py` | 必要检查：防错误泛化。 |
| Harness | `harness/prototype_preview_gate_checker.py` | 必要检查：原型监督边界。 |
| Harness | `harness/external_redaction_checker.py` | 必要检查：外部分发 redaction。 |
| Eval | `evals/skill_quality_cases.yaml` | 质量 case 基线。 |
| Eval | `evals/generalization_audit.yaml` | 泛化审计基线。 |
| Eval | `evals/run_real_output_eval.py` | 真实输出 eval 入口。 |
| Eval | `evals/real_outputs/20260425T000000Z/summary.md` | 真实输出摘要。 |
| Eval | `evals/real_outputs/20260425T000000Z/real_output_eval_report.json` | 真实输出报告。 |
| Eval cases | `evals/real_outputs/20260425T000000Z/cases/b2b_saas_approval_workflow/output.md` | 真实输出样例。 |
| Eval cases | `evals/real_outputs/20260425T000000Z/cases/education_exam_memo_tool/output.md` | 真实输出样例。 |
| Eval cases | `evals/real_outputs/20260425T000000Z/cases/fitness_training_app/output.md` | 真实输出样例。 |
| Eval cases | `evals/real_outputs/20260425T000000Z/cases/pet_store_service_growth/output.md` | 真实输出样例。 |
| Eval cases | `evals/real_outputs/20260425T000000Z/cases/prompt_ops_platform/output.md` | 真实输出样例。 |

已检查的 checker / eval 主文件合计约 996 行，不含 JSON 报告和 5 个 case 输出全文。

## 3. 能否进入下一步 staging 清单

结论：`ready_for_staging_list`

理由：

- 这 5 个检查已经由用户确认稳定保留。
- 当前 harness check-only 已显示：
  - `eval_suite`: pass，覆盖 5 个 domain case。
  - `real_output_eval`: pass，55/55。
  - `skill_generalization`: pass。
  - `prototype_preview_gate`: pass。
  - `external_redaction`: 由 harness 注册并可用于外部分发检查。
- A3 不混入按需 checker，不混入 candidate plugin，不混入项目产物。

仍需用户在 staging 前确认：

- 是否接受这 5 个检查作为稳定核心。
- 是否接受真实输出基线后续可迭代，但每次扩展需汇报。
- 是否保持“未来第 6 个检查必须单独必要性审计”。

## 4. A3 禁止混入范围

A3 staging 清单不得包含：

- `harness/delivery_plan_checker.py`
- `harness/ai_solution_checker.py`
- `harness/agentic_delivery_checker.py`
- `harness/preference_cache_checker.py`
- `plugins/*`
- `projects/*`
- `memory-cache/*`
- A1 已提交文件。
- A2 pipeline / workflow / harness 合同文件。
- A4 B 包、closeout、Codex 开发文档模板、长期偏好边界。
- `docs/proposals/*` 审查材料。

## 5. 风险和维护成本

- A3 会增加稳定检查维护成本；短期接受，后续核心稳定后再做瘦身。
- eval baseline 不能长期只依赖单批样例；后续需要多项目证据继续迭代。
- 检查不能替代人工监督；高风险动作仍需用户批准。

## 6. Staging 前检查命令

准备 A3 staging 清单前建议再次运行：

```bash
python3 -m py_compile harness/eval_suite_checker.py harness/real_output_eval_checker.py harness/skill_generalization_checker.py harness/prototype_preview_gate_checker.py harness/external_redaction_checker.py evals/run_real_output_eval.py
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

## 7. 本轮动作边界

本轮只新增本审查材料。

- 未批准 A3 staging。
- 未批准 A3 commit。
- 未批准 push / PR。
- 未批准删除、恢复、移动、归档。
- 未批准新增第 6 个稳定检查。
