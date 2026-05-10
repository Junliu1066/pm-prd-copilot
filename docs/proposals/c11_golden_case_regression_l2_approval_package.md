# C11 Golden Case + Regression L2 批量审批包

- 日期：2026-05-03
- 状态：L2 批量审批包，不是 stable policy。
- 授权等级：L2。需要用户批量批准后，才允许精确 staging 和 commit。
- 主线任务：把 C11 脱敏 golden case candidate 和 regression 依赖修复独立收口，不混入项目产物和治理 proposal 草案。

## 1. 结论

建议把 C11 拆成一个干净的功能 / 回归提交：

```text
Add deidentified PRD structure golden case
```

这个提交只包含：

- 脱敏后的 0-1 普通业务 PRD 结构样例。
- `run_regression.py` 对该样例的检查。
- golden cases README 的中文说明。

这个提交不包含：

- `projects/taxi-hailing-prd-test/`
- `docs/proposals/*`
- `docs/thread_registry.md`
- `memory-cache/*`
- `ai-intel/raw/*`
- 任何删除、归档、push / PR。

## 2. 为什么这样拆

| 选择 | 效果 |
|---|---|
| C11 golden case + regression 单独提交 | 回归资产可复现，干净 checkout 不再依赖未跟踪项目目录。 |
| C11 proposal 不混入本提交 | 避免功能修复和过程治理记录混在一起。 |
| 不提交 `projects/taxi-hailing-prd-test/` | 保持项目产物和稳定样例库分离。 |
| 不把单个样例升级 portfolio | 避免单项目过拟合。 |

## 3. 建议 staging 文件清单

只允许暂存以下 6 个文件：

```text
pm-prd-copilot/evals/golden_cases/README.md
pm-prd-copilot/evals/golden_cases/zero_to_one_service_prd/README.md
pm-prd-copilot/evals/golden_cases/zero_to_one_service_prd/input.md
pm-prd-copilot/evals/golden_cases/zero_to_one_service_prd/expected_prd.md
pm-prd-copilot/evals/golden_cases/zero_to_one_service_prd/acceptance.md
pm-prd-copilot/scripts/run_regression.py
```

## 4. 精确 staging 命令

如果你批准，只能执行：

```bash
git add pm-prd-copilot/evals/golden_cases/README.md pm-prd-copilot/evals/golden_cases/zero_to_one_service_prd/README.md pm-prd-copilot/evals/golden_cases/zero_to_one_service_prd/input.md pm-prd-copilot/evals/golden_cases/zero_to_one_service_prd/expected_prd.md pm-prd-copilot/evals/golden_cases/zero_to_one_service_prd/acceptance.md pm-prd-copilot/scripts/run_regression.py
```

禁止使用：

```bash
git add .
```

## 5. 禁止混入

本次暂存区不得出现：

- `projects/*`
- `docs/proposals/*`
- `docs/thread_registry.md`
- `memory-cache/*`
- `ai-intel/raw/*`
- `docs/archive/*`
- root 删除项
- skill / harness / workflow / registry / plugin 变更

## 6. Commit 建议

建议 commit message：

```text
Add deidentified PRD structure golden case
```

建议 commit body：

```text
- Add a deidentified 0-1 ordinary business PRD structure case.
- Validate page notes, page transitions, prototype layer, and PNG/HTML boundary.
- Move regression away from an untracked project artifact dependency.
- Keep the source taxi-hailing project as project evidence, not a stable golden case.
```

## 7. 回滚方式

如果只是撤销暂存：

```bash
git restore --staged pm-prd-copilot/evals/golden_cases/README.md pm-prd-copilot/evals/golden_cases/zero_to_one_service_prd/README.md pm-prd-copilot/evals/golden_cases/zero_to_one_service_prd/input.md pm-prd-copilot/evals/golden_cases/zero_to_one_service_prd/expected_prd.md pm-prd-copilot/evals/golden_cases/zero_to_one_service_prd/acceptance.md pm-prd-copilot/scripts/run_regression.py
```

如果 commit 后需要撤销：

```bash
git revert <commit>
```

不使用 destructive reset。

## 8. 已完成验证

本批次准备前已通过：

```text
PYTHONPYCACHEPREFIX=/tmp/pycache python3 -m py_compile pm-prd-copilot/scripts/run_regression.py
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

额外已验证：

- 在临时 clean-base 环境中不带 `projects/taxi-hailing-prd-test/`，regression 仍通过。
- 脱敏样例正文和输入中没有 `taxi-hailing-prd-test`、`打车产品 PRD 测试输入` 或绝对路径。

## 9. 需要用户批量批准

| 决策 | 我的建议 | 效果 |
|---|---|---|
| 是否允许 C11 精确 staging | 批准 | 可以把脱敏样例和 regression 修复收口到暂存区，范围可核对。 |
| 是否允许 C11 commit | 批准 | 让干净 checkout 下的 regression 不再依赖未跟踪项目目录。 |
| 是否提交 C11 proposal 和台账 | 本批不提交 | 保持功能 / 回归提交干净；proposal 继续放在后续决策记录批次。 |
| 是否提交 `projects/taxi-hailing-prd-test/` | 不提交 | 避免项目产物污染稳定样例库。 |
| 是否把该样例转完整 stable portfolio | 不转 | 等后续有多项目样例后再升级。 |

## 10. 本轮不做

- 不 staging / commit，除非你批量批准。
- 不提交 `projects/taxi-hailing-prd-test/`。
- 不提交 proposal / thread registry。
- 不删除、归档、移动文件。
- 不写长期记忆。
- 不新增 skill、harness、workflow、plugin 或 automation。
- 不 push / PR。
