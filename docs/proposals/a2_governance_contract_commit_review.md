# A2 Governance Contract Commit 审查

- 日期：2026-04-29
- 状态：commit 前审查材料，不批准 commit / push / PR
- 当前 staged 范围：A2 16 个治理合同文件
- 前提：真正 commit 仍需用户明确批准

## 1. 当前 Staged 范围

当前暂存区严格包含以下 16 个文件：

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

当前 staged stat：

```text
16 files changed, 1365 insertions(+), 83 deletions(-)
```

未包含：

- A1 已提交文件。
- A3 eval / checker 文件。
- A4 B 包、closeout、Codex 开发文档模板、长期偏好边界。
- `projects/*`
- `plugins/*`
- root 删除项。
- `docs/proposals/*`

## 2. 推荐 Commit Message

```text
Enforce governed pipeline and workflow contracts
```

推荐 commit body：

```text
- Make the production pipeline governed by default.
- Require explicit --fast-draft for draft bypass.
- Record governance mode and approval gate state in trace/manifest output.
- Register workflow/action/artifact contracts and steward ownership.
- Add harness check-only/write-report boundaries.
- Extend regression coverage for governed and fast-draft paths.
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

`git diff --cached --name-only` 必须严格等于第 1 节的 16 个文件。

如果任一检查失败：

- 不 commit。
- 保留 staged 状态，先汇报失败项。
- 只有用户要求撤销 staged 时，才执行 A2 范围的 `git restore --staged`。

## 4. Commit 后核对

如果用户后续明确批准 commit，commit 后必须运行：

```bash
git show --stat --oneline --name-only HEAD
git status --short
```

`git show` 必须显示最新 commit 只包含 A2 16 个治理合同文件。

## 5. 回滚策略

如果 commit 前需要撤销暂存：

```bash
git restore --staged pm-prd-copilot/scripts/run_pipeline.py pm-prd-copilot/scripts/governance_trace.py pm-prd-copilot/scripts/run_regression.py workflow/actions.yaml workflow/policies.yaml workflow/prd_workflow.yaml registry/artifacts.yaml registry/stewards.yaml governance/steward_operating_rules.yaml governance/teaching_policy.yaml harness/README.md harness/common.py harness/run_harness.py harness/workflow_gate_checker.py harness/efficiency_auditor.py harness/random_audit_inspector.py
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
- 暂存 A3 / A4 / C / D / E 批次
- 把 candidate plugin 转 stable

## 7. 下一步建议

如果用户认可本审查材料，下一步再单独申请：

```text
A2 Commit 执行方案
```

该下一步只会在检查通过后创建一个 A2 独立 commit，仍不 push。
