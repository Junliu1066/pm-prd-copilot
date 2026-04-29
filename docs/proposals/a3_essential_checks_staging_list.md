# A3 必要检查与 Eval 基线最终 Staging 清单

- 日期：2026-04-29
- 状态：最终 staging 清单，不批准 staging / commit / push
- 输入材料：`docs/proposals/a3_essential_checks_staging_review.md`
- 审查结论：`ready_for_staging_list`
- 执行边界：本文件只用于用户拍板；真正 staging 必须再次获得明确批准

## 1. A3 提交意图

A3 的目标是把已经确认必要的 5 个检查固定为稳定基线，防止同类问题复发：

- `eval_suite`：防 PRD 结构和质量退化。
- `real_output_eval`：用真实输出基线检查模板、模型或规则变化。
- `skill_generalization`：防项目偏好错误泛化为长期规则。
- `prototype_preview_gate`：防原型、PNG、HTML 或完整 UI 在未确认前越权进入。
- `external_redaction`：防 B 包或外部分发材料泄漏内部治理内容。

本批次不新增第 6 个稳定检查，不纳入按需 checker。

## 2. 需要用户拍板的点

| 决策 | 推荐 | 原因 | 不同选择的影响 |
|---|---|---|---|
| 5 个检查是否进入稳定核心 | 进入 A3 | 这些检查直接防 PRD 退化、泛化污染、原型越权和外部分发泄漏。 | 不进入会降低维护成本，但已修复的问题更容易复发。 |
| real-output eval 样例是否一起纳入 | 一起纳入 | 没有样例基线，checker 只能检查框架，不能检查真实输出退化。 | 暂不纳入会让检查变轻，但长期有效性不足。 |
| 后续 eval 基线如何迭代 | 允许后续收集多篇 PRD 后再汇报更新 | 符合“先稳定，再迭代”的节奏。 | 每次自动扩展会省事，但容易引入未审核样例污染。 |
| 第 6 个检查是否允许自动加入 | 不允许 | 保持“如无必要，不增 harness”。 | 允许自动加入会扩张很快，后续维护成本上升。 |
| A3 是否独立 commit | 独立 commit | A3 是 eval/checker 基线，不应和 A1/A2/A4 混在一起。 | 混合提交会降低回滚和审计清晰度。 |

## 3. 允许进入 A3 Staging 的精确文件

未来如果用户批准 A3 staging，只允许暂存以下 15 个文件。

| 序号 | 文件 | 归属 | 纳入原因 |
|---:|---|---|---|
| 1 | `harness/eval_suite_checker.py` | Harness | 必要检查：PRD/eval 覆盖。 |
| 2 | `harness/real_output_eval_checker.py` | Harness | 必要检查：真实输出基线。 |
| 3 | `harness/skill_generalization_checker.py` | Harness | 必要检查：防错误泛化。 |
| 4 | `harness/prototype_preview_gate_checker.py` | Harness | 必要检查：原型监督边界。 |
| 5 | `harness/external_redaction_checker.py` | Harness | 必要检查：外部分发 redaction。 |
| 6 | `evals/skill_quality_cases.yaml` | Eval | 质量 case 基线。 |
| 7 | `evals/generalization_audit.yaml` | Eval | 泛化审计基线。 |
| 8 | `evals/run_real_output_eval.py` | Eval | 真实输出 eval 入口。 |
| 9 | `evals/real_outputs/20260425T000000Z/summary.md` | Eval | 真实输出摘要。 |
| 10 | `evals/real_outputs/20260425T000000Z/real_output_eval_report.json` | Eval | 真实输出报告。 |
| 11 | `evals/real_outputs/20260425T000000Z/cases/b2b_saas_approval_workflow/output.md` | Eval case | 真实输出样例。 |
| 12 | `evals/real_outputs/20260425T000000Z/cases/education_exam_memo_tool/output.md` | Eval case | 真实输出样例。 |
| 13 | `evals/real_outputs/20260425T000000Z/cases/fitness_training_app/output.md` | Eval case | 真实输出样例。 |
| 14 | `evals/real_outputs/20260425T000000Z/cases/pet_store_service_growth/output.md` | Eval case | 真实输出样例。 |
| 15 | `evals/real_outputs/20260425T000000Z/cases/prompt_ops_platform/output.md` | Eval case | 真实输出样例。 |

## 4. 未来精确 Staging 命令

如果用户明确批准 A3 staging，只能使用下面这个精确命令：

```bash
git add harness/eval_suite_checker.py harness/real_output_eval_checker.py harness/skill_generalization_checker.py harness/prototype_preview_gate_checker.py harness/external_redaction_checker.py evals/skill_quality_cases.yaml evals/generalization_audit.yaml evals/run_real_output_eval.py evals/real_outputs/20260425T000000Z/summary.md evals/real_outputs/20260425T000000Z/real_output_eval_report.json evals/real_outputs/20260425T000000Z/cases/b2b_saas_approval_workflow/output.md evals/real_outputs/20260425T000000Z/cases/education_exam_memo_tool/output.md evals/real_outputs/20260425T000000Z/cases/fitness_training_app/output.md evals/real_outputs/20260425T000000Z/cases/pet_store_service_growth/output.md evals/real_outputs/20260425T000000Z/cases/prompt_ops_platform/output.md
```

禁止使用：

```bash
git add .
git add harness
git add evals
git add docs/proposals
```

原因：这些宽泛命令会把按需 checker、缓存文件、proposal 文档、项目产物或候选能力一起带进暂存区。

## 5. Staging 后必须核对的结果

A3 staging 后必须立即运行：

```bash
git diff --cached --name-only
```

结果必须严格等于以下 15 个文件：

```text
evals/generalization_audit.yaml
evals/real_outputs/20260425T000000Z/cases/b2b_saas_approval_workflow/output.md
evals/real_outputs/20260425T000000Z/cases/education_exam_memo_tool/output.md
evals/real_outputs/20260425T000000Z/cases/fitness_training_app/output.md
evals/real_outputs/20260425T000000Z/cases/pet_store_service_growth/output.md
evals/real_outputs/20260425T000000Z/cases/prompt_ops_platform/output.md
evals/real_outputs/20260425T000000Z/real_output_eval_report.json
evals/real_outputs/20260425T000000Z/summary.md
evals/run_real_output_eval.py
evals/skill_quality_cases.yaml
harness/eval_suite_checker.py
harness/external_redaction_checker.py
harness/prototype_preview_gate_checker.py
harness/real_output_eval_checker.py
harness/skill_generalization_checker.py
```

如果多出任何文件，必须停止，不 commit，并只撤销 A3 staged 状态：

```bash
git restore --staged harness/eval_suite_checker.py harness/real_output_eval_checker.py harness/skill_generalization_checker.py harness/prototype_preview_gate_checker.py harness/external_redaction_checker.py evals/skill_quality_cases.yaml evals/generalization_audit.yaml evals/run_real_output_eval.py evals/real_outputs/20260425T000000Z/summary.md evals/real_outputs/20260425T000000Z/real_output_eval_report.json evals/real_outputs/20260425T000000Z/cases/b2b_saas_approval_workflow/output.md evals/real_outputs/20260425T000000Z/cases/education_exam_memo_tool/output.md evals/real_outputs/20260425T000000Z/cases/fitness_training_app/output.md evals/real_outputs/20260425T000000Z/cases/pet_store_service_growth/output.md evals/real_outputs/20260425T000000Z/cases/prompt_ops_platform/output.md
```

不得使用 `git restore` 恢复工作区内容，除非用户另行批准。

## 6. A3 禁止混入范围

A3 staging 不得包含：

- 按需 checker：
  - `harness/delivery_plan_checker.py`
  - `harness/ai_solution_checker.py`
  - `harness/agentic_delivery_checker.py`
  - `harness/preference_cache_checker.py`
- Python 缓存：
  - `evals/__pycache__/*`
  - `harness/__pycache__/*`
- A1 已提交文件。
- A2 已提交文件。
- A4 B 包、closeout、Codex 开发文档模板、长期偏好边界。
- `projects/*`
- `plugins/*`
- `memory-cache/*`
- root 删除项。
- `docs/proposals/*`

## 7. Staging 前检查命令

真正 staging 前必须先跑：

```bash
PYTHONPYCACHEPREFIX=/tmp/pycache python3 -m py_compile harness/eval_suite_checker.py harness/real_output_eval_checker.py harness/skill_generalization_checker.py harness/prototype_preview_gate_checker.py harness/external_redaction_checker.py evals/run_real_output_eval.py
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

如果任一检查失败，不进入 staging。

## 8. 本轮未批准事项

本清单不批准：

- `git add`
- commit / push / PR
- 删除、恢复、移动、归档
- 暂存 `docs/proposals/*`
- 暂存 A4 / C / D / E 批次
- 新增第 6 个稳定检查
- 把 candidate plugin 转 stable

## 9. 下一步建议

如果用户认可本清单，下一步再单独申请：

```text
A3 精确 Staging 执行方案
```

该下一步只会按第 4 节命令暂存 15 个 A3 文件，并立即核对暂存区范围；仍不 commit。
