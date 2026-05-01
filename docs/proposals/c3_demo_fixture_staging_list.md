# C3-1 Demo Fixture 精确 Staging 清单

- 日期：2026-05-01
- 状态：最终 staging 清单，不批准实际 staging、commit、push、PR、删除、归档或项目文件改写。
- 范围：`projects/demo-project/` 中用于 regression / harness 的最小 fixture 文件。
- 前置报告：`docs/proposals/c3_demo_project_minimal_fixture_review.md`

## 结论

`demo-project` 可以作为治理回归测试 fixture，但本轮 staging 清单必须极窄，只包含自动检查必读文件。
prototype、closeout、meta、risk、human-readable markdown、可重建 run 报告和历史 run 都不能混入。

当前结论：`ready_for_precise_staging_after_user_approval`。

## 精确文件清单

只允许暂存以下 7 个文件：

```text
projects/demo-project/02_prd.generated.md
projects/demo-project/02_prd.generated.json
projects/demo-project/03_user_stories.generated.json
projects/demo-project/05_tracking_plan.generated.json
projects/demo-project/project_state.json
projects/demo-project/runs/pipeline-latest/manifest.json
projects/demo-project/runs/pipeline-latest/trace.json
```

## 每个文件的必要性

| 文件 | 必要性 | 依赖方 |
|---|---|---|
| `02_prd.generated.md` | 验证 PRD 不再使用集中式可视化层，且包含页面说明、页面跳转关系、原型图层；非 AI 项目不写 AI 模型选型 | `run_regression.py` |
| `02_prd.generated.json` | 验证 PRD schema | `run_regression.py` |
| `03_user_stories.generated.json` | 验证 user story schema 且非空 | `run_regression.py` |
| `05_tracking_plan.generated.json` | 验证 tracking schema 和 linked_metric | `run_regression.py` |
| `project_state.json` | 指向 `last_run_id=pipeline-latest`，记录 demo governed rerun 只是测试覆盖，不是真实产品审批 | `harness/run_harness.py` |
| `runs/pipeline-latest/manifest.json` | 验证 production pipeline manifest 是 governed、approval gate enforced、stage_actions 完整 | `run_regression.py`、`workflow_gate_checker.py` |
| `runs/pipeline-latest/trace.json` | 验证 skill calls、stage/action/steward 边界和 harness trace 检查 | `harness/*_checker.py` |

## 明确禁止混入

不得暂存：

```text
projects/demo-project/01_requirement_brief.md
projects/demo-project/*.meta.json
projects/demo-project/03_user_stories.generated.md
projects/demo-project/04_risk_check.generated.*
projects/demo-project/05_tracking_plan.generated.md
projects/demo-project/runs/pipeline-latest/harness_report.json
projects/demo-project/runs/pipeline-latest/efficiency_report.json
projects/demo-project/runs/pipeline-latest/eval_suite_report.json
projects/demo-project/runs/pipeline-latest/real_output_eval_status.json
projects/demo-project/runs/pipeline-latest/skill_generalization_audit.json
projects/demo-project/runs/pipeline-latest/random_audit_report.json
projects/demo-project/prototype/
projects/demo-project/closeout/
projects/demo-project/runs/governance-baseline/
```

也不得混入：

```text
projects/fitness-app-mvp/
memory-cache/
ai-intel/raw/
docs/archive/
docs/proposals/*
root 删除项
```

## 未来批准后可执行的精确命令

如果你后续批准 C3-1 精确 staging，只能使用：

```bash
git add projects/demo-project/02_prd.generated.md projects/demo-project/02_prd.generated.json projects/demo-project/03_user_stories.generated.json projects/demo-project/05_tracking_plan.generated.json projects/demo-project/project_state.json projects/demo-project/runs/pipeline-latest/manifest.json projects/demo-project/runs/pipeline-latest/trace.json
```

禁止使用：

```bash
git add .
git add projects/
git add projects/demo-project/
git add projects/demo-project/runs/
```

## 提交意图

后续如果 staging 和 commit 获批，建议 commit message：

```text
Refresh demo project governance fixture
```

提交目的：

- 固化 demo 的 governed pipeline fixture。
- 固化 PRD 新输出口径：页面说明、页面跳转关系、原型图层。
- 保持非 AI 项目不输出 AI 模型选型。
- 只保留 regression / harness 必读文件，不提交可重建 run 报告和项目产物。

## Staging 后验收

如果未来执行 staging，必须立刻运行：

```bash
git diff --cached --name-only
git diff --cached --check
git diff --cached --stat
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

验收标准：

- 暂存区严格等于 7 个文件。
- regression 通过。
- harness check-only 通过。
- harness 输出 `No project files written`。
- 不出现 prototype、closeout、meta、risk、附加 report、历史 run、其它项目、cache、raw、archive 或 root 删除项。

## 回滚方式

如果未来只需要撤销暂存：

```bash
git restore --staged projects/demo-project/02_prd.generated.md projects/demo-project/02_prd.generated.json projects/demo-project/03_user_stories.generated.json projects/demo-project/05_tracking_plan.generated.json projects/demo-project/project_state.json projects/demo-project/runs/pipeline-latest/manifest.json projects/demo-project/runs/pipeline-latest/trace.json
```

不要恢复工作区内容，不要使用 destructive reset。

## 本轮不批准

- 不实际 staging。
- 不提交 `projects/demo-project/*`。
- 不删除、恢复、移动、归档 demo 文件。
- 不提交 prototype、closeout、meta、risk 或可重建 run 输出。
- 不新增 skill、harness、workflow、plugin 或长期规则。
