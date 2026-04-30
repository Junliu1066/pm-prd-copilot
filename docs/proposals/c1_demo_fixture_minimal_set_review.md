# C1-1 Demo Project 最小 Fixture 能力集审查

- 日期：2026-04-30
- 状态：审查报告，不批准 staging、commit、push、PR、归档、删除、恢复或项目文件改写。
- 范围：`projects/demo-project/`
- 前提：用户已批准 `demo-project` 继续承担 regression / harness fixture 能力，并要求定义最小 fixture 能力集。

## 结论

`demo-project` 应保留为治理回归测试 fixture，但不能继续作为普通项目产物混在稳定治理提交里。

最小能力目标是：

1. 支撑 `run_regression.py` 对 PRD 主链路、schema、governed manifest、非 AI PRD 输出规则的检查。
2. 支撑 `harness/run_harness.py --check-only --audit --efficiency` 对 workflow、registry、prototype gate、preference cache、eval、random audit、efficiency 等检查的现场验证。
3. 明确 demo 的 pipeline approval override 只是测试覆盖，不是真实产品审批。
4. 把 prototype、closeout、run 输出从“默认提交物”降级为项目证据或可重建审计证据。

## 当前代码依赖

| 调用方 | 依赖 demo 的内容 | 作用 |
|---|---|---|
| `pm-prd-copilot/scripts/run_regression.py` | `runs/pipeline-latest/manifest.json` | 验证 demo run 必须是 governed，且 `approval_gate_enforced=true`。 |
| `run_regression.py` | `00_raw_input.md`、`02_prd.generated.md` | 验证非 AI PRD 不强行输出 AI 模型选型，并包含页面说明 / 页面跳转关系 / 原型图层。 |
| `run_regression.py` | `01_requirement_brief.json`、`02_prd.generated.json`、`03_user_stories.generated.json`、`05_tracking_plan.generated.json` | 验证 schema 和 tracking metric 链接。 |
| `harness/run_harness.py` | `project_state.json` 的 `last_run_id=pipeline-latest` | 确定 check-only 的当前 run 现场。 |
| `harness/run_harness.py` | `runs/pipeline-latest/manifest.json`、`trace.json` | 验证 source trace、workflow gate、conditional checker、audit 和 efficiency。 |
| `.github/workflows/*` | `demo-project` | CI / 定时检查继续用 demo 执行 check-only harness。 |

## 最小 Fixture 能力集

| 能力 | 必须保留的最小文件 | 是否建议进入稳定 fixture | 原因 |
|---|---|---:|---|
| 原始输入 / 非 AI 判断 | `00_raw_input.md` | 是 | 用于验证非 AI 项目不输出 AI 模型选型。 |
| requirement brief schema | `01_requirement_brief.json` | 是 | regression 直接校验 schema。 |
| PRD 输出合同 | `02_prd.generated.md`、`02_prd.generated.json` | 是 | 验证页面说明、页面跳转关系、原型图层和 schema。 |
| 用户故事 schema | `03_user_stories.generated.json` | 是 | regression 直接校验 user story schema。 |
| tracking schema | `05_tracking_plan.generated.json` | 是 | regression 直接校验 tracking schema 和 metric 链接。 |
| governed pipeline 现场 | `project_state.json`、`runs/pipeline-latest/manifest.json`、`runs/pipeline-latest/trace.json` | 是 | harness / regression 依赖这些文件确认 governed 状态和当前 run。 |
| harness check-only 审计 | `runs/pipeline-latest/harness_report.json` | 可选最小审计证据 | 不一定是运行必需，但能追溯最后一次 pass 状态。 |

## 不应作为最小 Fixture 的内容

| 内容 | 建议 | 原因 |
|---|---|---|
| `*.meta.json` | 不进最小 fixture | 可重建元数据，价值低。 |
| `*.generated.md` 中除 PRD 外的展示稿 | 不进最小 fixture | regression 主要读取 JSON；Markdown 可作为项目证据但不是最小测试能力。 |
| `02_prd.final.md`、`03_user_stories.final.md` | 项目证据，不进最小 fixture | 内容很短，不是完整 golden sample。 |
| `04_risk_check.*` | 项目证据，暂不进最小 fixture | 当前 regression 不直接依赖。 |
| `05_tracking_plan.generated.md` | 项目证据，暂不进最小 fixture | schema 依赖 JSON。 |
| `06_review_merge.md` | 项目证据，暂不进最小 fixture | 可解释人工修订，但不是自动检查依赖。 |
| `prototype/page_png/*`、`ui_style_direction.*` | 原型链路观察样例 | 不应自动成为稳定 UI / UX 样例。 |
| `closeout/*` | closeout 审核材料 | 证明流程存在，但不属于 regression 最小 fixture。 |
| `runs/governance-baseline/*` | 历史审计证据 | 当前 `last_run_id` 不指向它，可归为历史证据候选。 |
| `runs/pipeline-latest/eval_suite_report.json`、`real_output_eval_status.json`、`skill_generalization_audit.json`、`random_audit_report.json`、`efficiency_report.json` | 可选审计证据 | 只有在 `--write-report` 刷新时才需要写；check-only 不依赖现有文件。 |

## 已批准的功能方向

| 功能方向 | 已批准结论 | 后续效果 |
|---|---|---|
| demo 是否继续作为治理 fixture | 是 | 后续 regression / harness 可以继续稳定使用 demo。 |
| demo 是否代表真实产品审批 | 否 | `pipeline_assumption_overrides` 只能解释测试覆盖，不能视为真实审批。 |
| 是否定义最小 fixture | 是 | 后续可减少项目 run 输出噪音。 |
| 是否提交项目产物 | 否，本轮不提交 | 项目产物不会污染稳定核心。 |
| 是否删除或归档 demo 文件 | 否 | 等最小 fixture 策略和审计证据规则确认后再做。 |

## 已批准的功能决策

| 功能决策 | 已批准方向 | 预期效果 | 后续动作 |
|---|---|---|---|
| demo 最小 fixture 是否只覆盖 `brief + prd + stories + tracking + governed run` | 覆盖这些最小能力 | 先保障稳定核心检查，risk / prototype / closeout 用独立样例承载 | 后续可形成最小 fixture 文件清单 |
| run 输出最小审计证据是否只保留 latest manifest / trace / harness report | 只保留这 3 类 | 降低噪音，其它 report 可由 check-only 或 write-report 重建 | 已在 C1-2 规则中细化 |
| prototype 是否从 demo fixture 中剥离为原型观察样例 | 剥离 | 避免 demo PNG 被误当成稳定 UI 标准 | 后续选择更成熟原型样例再稳定化 |
| closeout 是否作为 demo fixture 的必需能力 | 不作为必需能力 | closeout 继续是归档前流程，不影响每次 regression | closeout 样例后续单独处理 |

## 文件处理建议

本报告不执行文件处理。后续如进入执行，应拆成单独计划：

1. 先写“demo fixture 最小保留清单”。
2. 再写“run 输出最小审计证据规则”。
3. 再决定是否提交最小 fixture 文件。
4. 最后才讨论其它 demo 项目产物的归档或 30 天后删除候选。

## 本轮不批准

- 不 staging / commit `projects/demo-project/*`。
- 不删除、恢复、移动、归档 demo 文件。
- 不提交 prototype、closeout 或 run 输出。
- 不把 demo final 文档升级为 golden sample。
- 不新增 skill、harness、workflow、plugin 或长期规则。
