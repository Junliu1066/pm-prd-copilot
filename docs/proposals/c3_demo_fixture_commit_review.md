# C3-1 Demo Fixture Commit 审查

- 日期：2026-05-01
- 状态：commit 审查材料，不批准 commit、push、PR、删除、归档、恢复或项目文件改写。
- 当前暂存范围：C3-1 demo fixture 7 个文件。
- 规则：本文件不进入本次暂存区；它只是提交前审查记录。

## 1. 当前暂存范围

当前暂存区必须严格等于以下 7 个文件：

```text
projects/demo-project/02_prd.generated.json
projects/demo-project/02_prd.generated.md
projects/demo-project/03_user_stories.generated.json
projects/demo-project/05_tracking_plan.generated.json
projects/demo-project/project_state.json
projects/demo-project/runs/pipeline-latest/manifest.json
projects/demo-project/runs/pipeline-latest/trace.json
```

当前暂存统计：

```text
7 files changed, 492 insertions(+), 535 deletions(-)
```

暂存范围不得包含：

- `projects/demo-project/*.meta.json`
- `projects/demo-project/01_requirement_brief.md`
- `projects/demo-project/03_user_stories.generated.md`
- `projects/demo-project/04_risk_check.generated.*`
- `projects/demo-project/05_tracking_plan.generated.md`
- `projects/demo-project/runs/pipeline-latest/harness_report.json`
- `projects/demo-project/runs/pipeline-latest/efficiency_report.json`
- `projects/demo-project/runs/pipeline-latest/eval_suite_report.json`
- `projects/demo-project/runs/pipeline-latest/real_output_eval_status.json`
- `projects/demo-project/runs/pipeline-latest/skill_generalization_audit.json`
- `projects/demo-project/prototype/`
- `projects/demo-project/closeout/`
- 其它项目、`memory-cache/`、`ai-intel/raw/`、`docs/archive/`、root 删除项。

## 2. 提交目的

本提交只刷新 demo fixture 的最小自动检查现场：

- 固化 demo PRD 输出口径：页面说明、页面跳转关系、原型图层。
- 保持 demo 作为非 AI 项目，不强制输出 AI 模型选型。
- 固化 `pipeline-latest` 为 governed pipeline fixture。
- 让 regression 和 harness check-only 能继续使用同一个最小、可追溯现场。

本提交不是：

- demo 项目正式产品交付。
- demo 原型 / UI / closeout 提交。
- run 报告刷新提交。
- root/archive 清理提交。

## 3. 推荐 Commit Message

```text
Refresh demo project governance fixture
```

推荐 commit body：

```text
- Keep the demo fixture focused on regression and harness inputs.
- Preserve governed pipeline manifest and trace evidence.
- Exclude prototype, closeout, meta files, risk output, and rebuildable run reports.
```

## 4. Commit 前必须再跑的检查

```bash
git diff --cached --name-only
git diff --cached --check
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

验收标准：

- `git diff --cached --name-only` 严格等于第 1 节的 7 个文件。
- `git diff --cached --check` 通过。
- `git diff --check` 通过。
- regression 通过。
- harness check-only 通过。
- harness 输出 `No project files written`。

## 5. 后续如获批准的 Commit 命令

```bash
git commit -m "Refresh demo project governance fixture"
```

## 6. 回滚方式

如果只是撤销暂存：

```bash
git restore --staged projects/demo-project/02_prd.generated.md projects/demo-project/02_prd.generated.json projects/demo-project/03_user_stories.generated.json projects/demo-project/05_tracking_plan.generated.json projects/demo-project/project_state.json projects/demo-project/runs/pipeline-latest/manifest.json projects/demo-project/runs/pipeline-latest/trace.json
```

如果 commit 后需要撤销，优先使用：

```bash
git revert <commit>
```

不要使用 `git reset --hard`。不要恢复或覆盖其它未批准的工作区变更。

## 7. 本审查不批准

- 不批准 commit。
- 不批准 push / PR。
- 不批准 staging 本审查文件。
- 不批准 staging prototype、closeout、meta、risk、run 附加报告。
- 不批准删除、恢复、移动、归档。
- 不批准写长期记忆。
- 不批准新增 skill、harness、workflow、plugin 或长期规则。
