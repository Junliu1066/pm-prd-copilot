# Two-Round Self-Check Protocol

这个协议用于防止边做边改时出现遗漏、漂移、旧要求残留、文档未同步、生成物未刷新、或测试只覆盖局部的问题。

## When To Run

必须运行两轮自检：

- 每次修改文件后，交付前。
- 用户在工作中途指出错误、补充要求、或改变优先级后。
- 修改 workflow、registry、steward、skill 合同、harness、脚本、模板、日报、归档规则、开发文档规则时。
- 版本更新、模型更新、模型供应商/SDK/API 更新、价格变化或弃用通知后。
- 清理、归档、打包、生成外部版/B 包前。

## Mid-Work Correction Alignment

如果用户在执行中途纠正方向：

1. 暂停当前实现判断。
2. 重新读取用户最新要求和受影响文件。
3. 更新计划或检查清单。
4. 判断已经做过的改动是否仍然有效。
5. 继续前明确哪些内容需要补测、重跑、重生成或汇报。

## Round 1: Change Correctness

目标：证明刚改的东西本身是正确的。

检查项：

- 语法、格式、schema、lint 或编译检查通过。
- 相关脚本能运行。
- 相关测试、回归或治理检查通过。
- 新增/修改的 action、artifact、skill、steward、template、script 有明确合同。
- 如果新增 skill、harness checker、steward、plugin、workflow stage、registry category、长期规则或 automation，必须证明现有组件无法满足。
- 没有新增失败、警告或不可解释的输出。

常用命令示例：

```bash
python3 -m py_compile <changed-python-files>
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project <project> --mode advisory --check-only
git diff --check
```

## Round 2: Omission And Consistency

目标：证明没有遗漏上下游、用户最新要求、或项目稳定性问题。

检查项：

- 重新阅读最新用户要求，确认没有漏项。
- 看 `git diff`，确认改动范围没有越界。
- 检查上下游文件是否需要同步：README、docs、workflow、registry、harness、templates、closeout、daily report。
- 检查生成物是否需要刷新：harness report、closeout 包、UI style direction、delivery package、AI intel decision docs。
- 检查外部版/B 包是否需要 redaction 和 English-only 约束。
- 检查是否可以用已有 skill、harness、脚本、模板或文档解决，而不新增长期组件。
- 如果刚发生版本或模型更新，检查是否有不再必要的 skill、harness checker、steward、plugin、workflow stage、registry category、长期规则、automation、template 或 package path。
- 检查有没有覆盖用户已有改动。
- 列出仍需用户确认的决策。

## Minimal Governance Addition Rule

非必要不新增稳定治理组件，包括：

- skill
- harness checker
- steward
- plugin
- workflow stage
- registry category
- long-lived rule
- automation

新增前必须先回答：

- 现有组件为什么不够？
- 能否只改文档、模板、脚本参数或现有检查？
- 最小可接受改动是什么？
- 后续维护成本是什么？
- 是否需要用户批准后才能稳定化？

如果答案不清楚，先写 proposal 或 follow-up note，不直接新增。

## Version And Model Update Pruning Rule

每次版本更新或模型更新后，必须先跑测试，再做治理瘦身审计。

先运行：

```bash
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project <project> --mode advisory --check-only --audit --efficiency
git diff --check
```

然后列出可疑冗余项：

- unused: 没有 workflow/action 引用、没有 recent trace、没有 eval 覆盖。
- duplicate: 与已有 skill、harness、script、template、rule 职责重复。
- model-obsoleted: 新模型/API 已原生覆盖原来的补丁能力。
- project-specific: 只服务单个历史项目，且经验已沉淀。
- high-maintenance: 维护成本高于质量收益。

处理顺序：

1. 提出 deprecate/archive/delete candidate。
2. 说明替代路径和风险。
3. 停用或移除前后都跑测试。
4. 给用户审核精确清单。
5. 未获批准前不硬删除。

常用命令示例：

```bash
git diff --stat
git diff -- <changed-files>
git status --short
python3 harness/run_harness.py --base-dir . --project <project> --mode advisory --check-only --audit --efficiency
```

## Failure Rule

如果任一轮发现问题：

- 先修复问题。
- 只重跑受影响的最小检查，必要时重跑完整回归。
- 在最终汇报中说明失败原因、修复方式和最终结果。

如果检查无法运行：

- 说明无法运行的具体原因。
- 提供替代检查。
- 标记剩余风险。

## Final Report Requirement

交付汇报必须包含：

- Round 1 运行了什么，结果是什么。
- Round 2 复核了什么，结果是什么。
- 哪些内容没有检查或无法检查。
- 哪些决策仍需用户确认。
