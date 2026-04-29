# A3 必要检查与 Eval 基线 Commit 审查

- 日期：2026-04-29
- 状态：commit 前审查材料，不批准 commit / push / PR
- 当前 staged 范围：A3 15 个必要检查与 eval 基线文件
- 前提：真正 commit 仍需用户明确批准

## 1. 当前 Staged 范围

当前暂存区严格包含以下 15 个文件：

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

当前 staged stat：

```text
15 files changed, 1763 insertions(+)
```

未包含：

- A1 已提交文件。
- A2 已提交文件。
- A4 B 包、closeout、Codex 开发文档模板、长期偏好边界。
- 按需 checker：`delivery_plan`、`ai_solution`、`agentic_delivery`、`preference_cache`。
- `evals/__pycache__/*` 或 `harness/__pycache__/*`。
- `projects/*`
- `plugins/*`
- root 删除项。
- `docs/proposals/*`

## 2. 推荐 Commit Message

```text
Add essential governance checks and eval baselines
```

推荐 commit body：

```text
- Add five approved governance checks for eval quality, real outputs, skill generalization, prototype preview boundaries, and external redaction.
- Add real-output eval runner and baseline cases.
- Keep optional delivery, AI solution, agentic delivery, and preference-cache checks outside this stable batch.
- Preserve the rule that any sixth stable check requires separate necessity review.
```

## 3. Commit 前必须再次验证

真正 commit 前必须运行：

```bash
git diff --cached --name-only
git diff --cached --check
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

`git diff --cached --name-only` 必须严格等于第 1 节的 15 个文件。

如果任一检查失败：

- 不 commit。
- 保留 staged 状态，先汇报失败项。
- 只有用户要求撤销 staged 时，才执行 A3 范围的 `git restore --staged`。

## 4. Commit 后核对

如果用户后续明确批准 commit，commit 后必须运行：

```bash
git show --stat --oneline --name-only HEAD
git status --short
```

`git show` 必须显示最新 commit 只包含 A3 15 个必要检查与 eval 基线文件。

## 5. 回滚策略

如果 commit 前需要撤销暂存：

```bash
git restore --staged harness/eval_suite_checker.py harness/real_output_eval_checker.py harness/skill_generalization_checker.py harness/prototype_preview_gate_checker.py harness/external_redaction_checker.py evals/skill_quality_cases.yaml evals/generalization_audit.yaml evals/run_real_output_eval.py evals/real_outputs/20260425T000000Z/summary.md evals/real_outputs/20260425T000000Z/real_output_eval_report.json evals/real_outputs/20260425T000000Z/cases/b2b_saas_approval_workflow/output.md evals/real_outputs/20260425T000000Z/cases/education_exam_memo_tool/output.md evals/real_outputs/20260425T000000Z/cases/fitness_training_app/output.md evals/real_outputs/20260425T000000Z/cases/pet_store_service_growth/output.md evals/real_outputs/20260425T000000Z/cases/prompt_ops_platform/output.md
```

如果 commit 后需要撤销：

```bash
git revert <commit>
```

不使用 `git reset --hard`，不恢复或覆盖用户未批准的其他工作区变更。

## 6. 本轮未批准事项

本审查材料不批准：

- commit
- push / PR
- 删除、恢复、移动、归档
- 暂存 `docs/proposals/*`
- 暂存 A4 / C / D / E 批次
- 新增第 6 个稳定检查
- 把 candidate plugin 转 stable

## 7. 下一步建议

如果用户认可本审查材料，下一步再单独申请：

```text
A3 Commit 执行方案
```

该下一步只会在检查通过后创建一个 A3 独立 commit，仍不 push。
