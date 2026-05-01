# C3 Demo Project 最小 Fixture 审查

- 日期：2026-05-01
- 状态：项目 fixture 审查报告，不批准 staging、commit、push、PR、删除、归档、恢复或项目文件改写。
- 范围：`projects/demo-project/`
- 主线任务：判断 demo 项目中哪些文件是治理回归测试必须保留的最小 fixture，哪些只是可重建项目产物或运行输出。

## 主线边界

本报告只回答治理问题：

- `demo-project` 作为 regression / harness fixture 需要哪些最小文件。
- 当前已修改和未跟踪的 demo 文件是否应该进入稳定 fixture。
- 哪些 run / prototype / closeout 输出应继续留作项目产物候选，而不是混入治理提交。

本报告不回答产品业务问题：

- 不评价 demo 产品功能。
- 不重写 demo PRD。
- 不设计 demo UI。
- 不把 demo 项目偏好推广为长期规则。

## 当前状态

`projects/demo-project/` 当前有：

- `19` 个已修改文件。
- 未跟踪 `closeout/`。
- 未跟踪 `prototype/`。
- 未跟踪 `runs/pipeline-latest/` 下 3 个可重建检查报告：
  - `eval_suite_report.json`
  - `real_output_eval_status.json`
  - `skill_generalization_audit.json`

当前 regression 和 harness check-only 均通过，说明 demo fixture 当前可用，但工作区里仍包含不应一次性提交的项目产物和可重建报告。

## 实际依赖确认

### Regression 直接依赖

| 文件 | 用途 | 最小 fixture 判断 |
|---|---|---|
| `projects/demo-project/00_raw_input.md` | 判断 demo 是否非 AI 项目，防止非 AI PRD 强行输出 AI 模型选型 | 已跟踪且未修改，保留 |
| `projects/demo-project/01_requirement_brief.json` | requirement brief schema 校验 | 已跟踪且未修改，保留 |
| `projects/demo-project/02_prd.generated.md` | PRD 输出口径校验：页面说明、页面跳转关系、原型图层、无集中式可视化层 | 最小 fixture 候选 |
| `projects/demo-project/02_prd.generated.json` | PRD schema 校验 | 最小 fixture 候选 |
| `projects/demo-project/03_user_stories.generated.json` | user story schema 校验 | 最小 fixture 候选 |
| `projects/demo-project/05_tracking_plan.generated.json` | tracking schema 和 linked_metric 校验 | 最小 fixture 候选 |
| `projects/demo-project/runs/pipeline-latest/manifest.json` | 验证 production pipeline manifest 是 governed 且 approval gate enforced | 最小 fixture 候选 |

### Harness check-only 依赖

| 文件 | 用途 | 最小 fixture 判断 |
|---|---|---|
| `projects/demo-project/project_state.json` | 指向 `last_run_id=pipeline-latest`，提供当前 run 现场 | 最小 fixture 候选 |
| `projects/demo-project/runs/pipeline-latest/manifest.json` | workflow gate、conditional checker、governance 状态检查 | 最小 fixture 候选 |
| `projects/demo-project/runs/pipeline-latest/trace.json` | steward contract、source trace、prototype gate、random audit 输入 | 最小 fixture 候选 |
| `projects/demo-project/runs/pipeline-latest/harness_report.json` | 最近一次聚合审计结果 | 可选审计证据，不是 check-only 必需输入 |

## 当前文件分类

| 分类 | 文件 | 建议 |
|---|---|---|
| 最小 fixture 候选 | `02_prd.generated.md`、`02_prd.generated.json`、`03_user_stories.generated.json`、`05_tracking_plan.generated.json`、`project_state.json`、`runs/pipeline-latest/manifest.json`、`runs/pipeline-latest/trace.json` | 后续可做 C3-1 精确 staging 清单 |
| 可选审计证据 | `runs/pipeline-latest/harness_report.json` | 如果要保留最近一次 pass 证据，可单独纳入；否则可由 check-only 输出替代 |
| 人类可读展示稿 | `01_requirement_brief.md`、`03_user_stories.generated.md`、`05_tracking_plan.generated.md` | 不进入最小 fixture，除非你希望 demo 同时保留可读样例 |
| meta 元数据 | `*.meta.json` | 不进入最小 fixture，通常可重建 |
| risk 输出 | `04_risk_check.generated.*` | 当前 regression 不直接依赖，暂不进入最小 fixture |
| 附加 run 报告 | `efficiency_report.json`、`eval_suite_report.json`、`real_output_eval_status.json`、`skill_generalization_audit.json`、`random_audit_report.json` | 可重建或附加审计，默认不进入 fixture |
| prototype 输出 | `prototype/page_png/*`、`ui_style_direction.*` | 原型观察样例，不进入 demo 最小 fixture |
| closeout 输出 | `closeout/*` | closeout 审核材料，不进入 demo 最小 fixture |
| 历史 run | `runs/governance-baseline/*` | 历史证据候选，后续归档或 30 天后删除候选 |

## 功能决策与效果

| 决策 | 选项 A | 选项 B | 选项 C | 我的建议 |
|---|---|---|---|---|
| demo fixture 是否只保留自动检查最小依赖 | 只保留 regression / harness 必读文件 | 保留全部 demo 项目产物 | 不提交任何 demo 变更 | 选 A。能保证测试稳定，同时减少项目产物污染。 |
| `harness_report.json` 是否纳入最小 fixture | 纳入为最近一次审计证据 | 不纳入，只依赖 check-only 当前输出 | 与其它 run 报告一起提交 | 选 B。check-only 已能现场输出结果，减少静态报告漂移。 |
| Markdown 展示稿是否纳入 fixture | 只纳入 `02_prd.generated.md` | 纳入所有 generated markdown | 全部排除 markdown | 选 A。PRD markdown 是输出口径校验对象，其它 markdown 不是最小依赖。 |
| prototype 是否进入 demo fixture | 不进入 | 作为 UI 样例进入 | 单独提交全部 prototype | 选 A。prototype 属于后期原型链路，不应污染 regression fixture。 |
| closeout 是否进入 demo fixture | 不进入 | 作为 closeout 样例进入 | 和项目产物一起提交 | 选 A。demo fixture 不应承担 closeout 样例职责。 |
| 历史 run 是否保留在 active fixture | 不作为 active fixture | 作为历史审计保留 | 删除 | 选 A。历史 run 后续进入归档候选，当前不删除。 |

## 推荐下一步

建议下一步做 **C3-1 Demo Fixture 精确 Staging 清单**，但仍不直接 staging。

建议 C3-1 清单只考虑：

```text
projects/demo-project/02_prd.generated.md
projects/demo-project/02_prd.generated.json
projects/demo-project/03_user_stories.generated.json
projects/demo-project/05_tracking_plan.generated.json
projects/demo-project/project_state.json
projects/demo-project/runs/pipeline-latest/manifest.json
projects/demo-project/runs/pipeline-latest/trace.json
```

暂不纳入：

```text
projects/demo-project/*.meta.json
projects/demo-project/01_requirement_brief.md
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

## 本轮不批准

- 不 staging / commit `projects/demo-project/*`。
- 不删除、恢复、移动、归档 demo 文件。
- 不提交 prototype、closeout 或可重建 run 输出。
- 不把 demo final 文档升级为 golden sample。
- 不新增 skill、harness、workflow、plugin 或长期规则。
