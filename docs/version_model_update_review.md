# Version And Model Update Review

每次项目版本更新、模型更新、模型供应商/SDK/API 更新后，都要做一轮治理瘦身审计，防止 skill、harness、steward、plugin、workflow、registry、长期规则和 automation 越积越多。

## Trigger

必须运行本流程：

- 版本发布、版本升级、架构重构后。
- 模型名、模型供应商、SDK、API、价格、上下文长度、工具能力、结构化输出能力、RAG/文件能力、浏览器/计算机使用能力发生变化后。
- AI intel 报告出现可能影响架构的能力、弃用、价格、合规或工具链变化后。
- 新增或修改 skill、harness checker、steward、plugin、workflow stage、registry category、长期规则或 automation 后。

## Required Test Pass

先证明系统仍然稳定：

```bash
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project <project> --mode advisory --check-only --audit --efficiency
git diff --check
```

如果涉及 B 执行包，还要运行：

```bash
python3 harness/run_harness.py --base-dir . --project <project> --mode advisory --check-only --external-package <path>
```

## Pruning Audit

逐项检查以下组件是否仍有必要：

- skill
- harness checker
- steward
- plugin
- workflow stage
- registry category
- long-lived rule
- automation
- template
- generated package path

候选移除信号：

- 没有 workflow/action 引用。
- 没有最近 trace 或项目使用证据。
- 没有 eval 覆盖，或 eval 已被更通用检查覆盖。
- 与已有组件职责重复。
- 新模型/API 已原生覆盖原来的补丁式能力。
- 维护成本高于收益。
- 只服务单个历史项目，且学习已经沉淀。
- 会让执行路径变复杂但没有提高质量或安全性。

## Removal Path

不要直接硬删除稳定组件。按这个顺序处理：

1. 标记候选：写入日报、closeout、architecture feedback 或 proposal。
2. 说明理由：为什么不再需要，替代组件是什么，风险是什么。
3. 跑测试：证明停用或移除后 regression 和 harness 仍通过。
4. 用户审核：给出精确清单，由用户确认。
5. 先 deprecate 或 archive。
6. 归档满 30 天后，如仍无回滚需求，再请求用户批准硬删除。

## Report Format

| Component | Type | Keep / Deprecate / Archive / Delete Candidate | Evidence | Replacement | Risk | User approval |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  | Yes |

## Rule

版本更新和模型更新后，目标不是增加组件，而是先确认已有组件是否仍必要。删除候选必须有测试证据和用户批准；没有批准前只能提出 proposal、deprecate 或 archive 计划。
