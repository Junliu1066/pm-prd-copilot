# B5c AI 情报候选区 Commit 审查

- 日期：2026-04-30
- 状态：commit 审查材料，不批准 commit
- 范围：AI 情报候选区基础设施
- 规则：本文档不批准 commit、push、PR、联网抓取、定时自动化启用、模型/供应商变更、稳定治理规则变更、registry 变更、skill 变更、harness 变更、归档、删除或长期记忆写入。

## 结论

B5c 当前暂存范围正确，可以进入 commit 前最终审核。

建议 commit，但必须保留这次提交的性质：

- 这是 AI 情报候选区基础设施提交。
- 不是稳定自动化启用。
- 不是联网抓取启用。
- 不是模型选型结论。
- 不是供应商切换。
- 不是治理架构自动更新机制。
- 不是长期记忆写入。

推荐 commit message：

```text
Add candidate AI intel data area
```

## 当前暂存范围

当前暂存区包含 9 个文件：

```text
ai-intel/README.md
ai-intel/daily/.gitkeep
ai-intel/decisions/governance-architecture-signals.md
ai-intel/events/.gitkeep
ai-intel/logs/.gitkeep
ai-intel/raw/.gitkeep
ai-intel/scripts/summarize_daily.py
ai-intel/scripts/update_decision_matrix.py
ai-intel/weekly/.gitkeep
```

暂存统计：

```text
9 files changed, 71 insertions(+)
```

说明：

- `ai-intel/sources/registry.yaml`
- `ai-intel/decisions/model-selection-matrix.md`
- `ai-intel/decisions/vendor-watchlist.md`
- `ai-intel/decisions/capability-map.md`
- `ai-intel/scripts/fetch_sources.py`
- `ai-intel/scripts/normalize_events.py`

这些文件已经在仓库里，并且本轮没有变更，所以不会出现在本次 staged diff 里。

## 这次提交解决什么问题

之前 AI 相关信息没有一个明确的候选收集区，容易出现三类问题：

| 问题 | 风险 |
|---|---|
| AI 更新信息混在项目产物或治理文档里 | 后续难以判断哪些是信号，哪些是已批准规则。 |
| AI 模型、API、价格、废弃信息没有固定观察面 | 容易漏掉影响架构的外部变化。 |
| AI 情报可能被误当成自动决策依据 | 容易绕过用户审批，直接改模型、workflow、registry 或 skill。 |

B5c 的目标是建立一个候选情报区，让 AI 更新先进入观察、分类、提案，再由用户决定是否反哺治理架构。

## 本次提交的效果

- 新增 `ai-intel/README.md`，定义 AI 情报区用途、目录边界和治理规则。
- 新增 `governance-architecture-signals.md`，把 AI 更新对治理架构的影响分成观察、提案、需用户审批等类别。
- 更新 `summarize_daily.py`，让日报明确提示：不能从 AI 情报直接修改 workflow、registry、skill、模型供应商、外部数据源、保留/删除策略或发布行为。
- 更新 `update_decision_matrix.py`，让治理架构信号文档进入决策面板更新范围。
- 新增 `daily/events/logs/raw/weekly` 的 `.gitkeep`，只保留目录，不提交生成内容。

## 不包含的内容

本次 B5c commit 不包含：

- `ai-intel/scripts/__pycache__/*`
- `ai-intel/raw/<run-output>/*`
- `ai-intel/events/<generated-run>.json`
- `ai-intel/daily/<generated-run>.md`
- `ai-intel/logs/<generated-run>.json`
- `docs/proposals/*`
- `projects/*`
- `harness/*`
- `plugins/*`
- `docs/archive/*`
- root 删除项

## Commit 前检查要求

commit 前必须重新运行：

```bash
git diff --cached --name-only
git diff --cached --check
git diff --check
PYTHONPYCACHEPREFIX=/tmp/pycache python3 -m py_compile ai-intel/scripts/fetch_sources.py ai-intel/scripts/normalize_events.py ai-intel/scripts/summarize_daily.py ai-intel/scripts/update_decision_matrix.py
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

额外排除项检查：

```bash
git diff --cached --name-only | rg "__pycache__|ai-intel/raw/.+[^.]gitkeep$|ai-intel/events/.+\\.json|ai-intel/daily/.+\\.md|ai-intel/logs/.+\\.json|docs/proposals|projects/|harness/|plugins/|docs/archive|^prd_|skill_suite_overview"
```

预期：无输出。

## 当前已通过检查

- 暂存范围检查通过。
- 暂存排除项检查无命中。
- `git diff --cached --check` 通过。
- `git diff --check` 通过。
- AI intel 脚本编译通过。
- regression 通过。
- harness check-only 通过，且未写项目文件。

## 回滚方式

如果只是撤销暂存：

```bash
git restore --staged ai-intel/README.md ai-intel/daily/.gitkeep ai-intel/decisions/governance-architecture-signals.md ai-intel/events/.gitkeep ai-intel/logs/.gitkeep ai-intel/raw/.gitkeep ai-intel/scripts/summarize_daily.py ai-intel/scripts/update_decision_matrix.py ai-intel/weekly/.gitkeep
```

如果 commit 后需要撤销：

```bash
git revert <B5c_commit_hash>
```

不要使用 destructive reset。

## 需要你最终批准

| 决策 | 我的建议 | 说明 |
|---|---|---|
| 是否允许 B5c commit | 建议允许 | 当前暂存只包含候选 AI 情报区基础设施，不包含生成物或自动化启用。 |
| 是否启用联网抓取 | 不允许 | 需要单独审批，且可能需要网络权限。 |
| 是否启用定时自动化 | 不允许 | 需要先补 dry-run / output-dir 或明确写入边界。 |
| 是否允许 AI 情报自动修改治理架构 | 不允许 | AI 情报只能产生观察、提案或需用户审批的信号。 |
| 是否提交生成的 raw/events/daily/logs 输出 | 不允许 | 生成物需要单独证据审查。 |

## 建议下一步

如果你认可 B5c commit 审查，可以单独批准：

```text
批准 B5c commit
```

我再执行 commit，并在 commit 后核对最新提交只包含 B5c 范围。

