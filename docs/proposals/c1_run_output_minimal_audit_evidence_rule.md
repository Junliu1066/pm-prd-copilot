# C1-2 Run 输出最小审计证据规则

- 日期：2026-04-30
- 状态：规则审查报告，不批准 staging、commit、push、PR、归档、删除、恢复或项目 run 文件改写。
- 范围：`projects/*/runs/*`
- 前提：用户已批准建立 run 输出“最小审计证据”能力，用于降低项目 run 输出噪音。

## 结论

项目 run 输出需要分层保留。长期稳定不是“所有 report 都提交”，而是保留能解释运行事实的最小证据，并让其它报告在需要时可重建。

建议的最小审计证据：

```text
manifest.json
trace.json
harness_report.json
```

这 3 类文件足以回答：

- 这次 run 是什么目的、什么模式、是否 governed。
- 运行了哪些 stage、skill、action、输入和输出。
- 最近一次 harness 聚合结果是否通过。

其它 report 不应默认进入稳定核心或 fixture，除非它们服务于某个明确审计场景。

## Run 输出分类规则

| 文件 | 分类 | 默认处理 | 原因 |
|---|---|---|---|
| `manifest.json` | 最小审计证据 | 保留 | 记录 run 目标、模式、governance、required outputs、状态。 |
| `trace.json` | 最小审计证据 | 保留 | 记录 stage / action / skill / source trace，是追溯链核心。 |
| `harness_report.json` | 最小审计证据 | 保留最近一次有效报告 | 汇总 pass/warn/fail，便于快速复盘。 |
| `eval_suite_report.json` | 可重建检查报告 | 默认不提交，必要时作为专项证据 | `--write-report` 才写；check-only 不依赖现有文件。 |
| `real_output_eval_status.json` | 可重建检查报告 | 默认不提交，必要时作为专项证据 | 真实输出基线在 `evals/real_outputs/`，项目状态文件只是投影。 |
| `skill_generalization_audit.json` | 可重建检查报告 | 默认不提交，必要时作为专项证据 | 用于防错误泛化，但可由 harness 重新生成。 |
| `random_audit_report.json` | 附加审计证据 | 默认不提交，必要时保留 | 受随机抽样影响，不适合作为每次固定 fixture。 |
| `efficiency_report.json` | 附加审计证据 | 默认不提交，必要时保留 | 用于效率复盘，不是 run 事实最小证据。 |

## 对 demo-project 的应用

| run | 建议 | 原因 |
|---|---|---|
| `projects/demo-project/runs/pipeline-latest/` | 作为当前 fixture run | `project_state.json` 指向它，regression 和 harness 依赖它确认 governed 状态。 |
| `pipeline-latest/manifest.json` | 最小保留 | regression 直接读取并验证 `governance_mode=governed`。 |
| `pipeline-latest/trace.json` | 最小保留 | harness 检查 source trace、workflow gate 和 action 合同。 |
| `pipeline-latest/harness_report.json` | 可作为最近一次审计结果保留 | 能快速证明 fixture 最近一次 check-only / strict 状态。 |
| `pipeline-latest/eval_suite_report.json`、`real_output_eval_status.json`、`skill_generalization_audit.json` | 暂不纳入最小 fixture | 属于 `--write-report` 投影，可重建。 |
| `pipeline-latest/random_audit_report.json`、`efficiency_report.json` | 暂不纳入最小 fixture | 是附加审计，不应默认堆在 fixture。 |
| `runs/governance-baseline/*` | 历史证据候选 | 当前 last_run_id 不再指向它；可后续归档或删除候选。 |

## 对其它项目的应用

| 项目类型 | 默认规则 |
|---|---|
| active 项目 | 保留 run 输出在项目内，不提交到稳定治理批次。 |
| closeout candidate | closeout 前保留完整 run 输出；closeout 后再决定最小审计证据和归档候选。 |
| archived candidate | 归档包中可保留完整 run 证据；仓库工作区只保留必要摘要。 |
| fixture 项目 | 只保留支撑测试能力的最小 run 证据。 |

## 已批准的功能方向

| 功能方向 | 已批准结论 | 后续效果 |
|---|---|---|
| 是否建立 run 输出最小审计证据规则 | 是 | 后续可以降低 run 输出噪音。 |
| 是否默认保留所有 report | 否 | 避免每次 harness / pipeline 产生大量项目 diff。 |
| 是否允许专项审计保留额外 report | 是，但需说明目的 | 保留灵活性，不破坏最小原则。 |
| 是否清理现有 run 输出 | 否，本轮不清理 | 清理必须先归档，30 天后再精确批准。 |

## 已批准的功能决策

| 功能决策 | 已批准方向 | 预期效果 | 后续动作 |
|---|---|---|---|
| demo fixture 是否采用 `manifest + trace + harness_report` 作为最小 run 证据 | 采用 | 保持可追溯，同时减少 run 输出噪音 | 后续最小 fixture 清单按此收敛 |
| `eval_suite_report` 等可重建报告是否进入 fixture | 不进入 fixture | 专项 report 不污染默认 fixture，可按需重建 | 后续只在专项审计中保留 |
| 历史 run 如 `governance-baseline` 是否作为 archive candidate | 是，后续归档候选 | 避免旧 run 长期堆在 active 项目目录 | 后续进入归档 / 30 天删除候选清单 |
| 是否需要脚本层面支持 run 输出瘦身 | 先不加脚本，只记录规则 | 遵守“如无必要，不增 harness / script” | 后续先用人工审批清单处理 |

## 执行边界

本报告只是规则审查，不执行清理。任何 run 输出处理都必须满足：

1. 先确认项目身份：active / fixture / closeout candidate / archived candidate。
2. 先归档有价值证据。
3. 至少 30 天后再拿精确硬删除清单给用户批准。
4. 不使用 `git add .`。
5. 不把项目 run 输出混进稳定治理提交。

## 本轮不批准

- 不删除任何 `projects/*/runs/*`。
- 不移动 run 目录。
- 不提交 run 输出。
- 不新增 run 清理脚本。
- 不新增 harness。
- 不修改 `run_harness.py` 或 pipeline 行为。
