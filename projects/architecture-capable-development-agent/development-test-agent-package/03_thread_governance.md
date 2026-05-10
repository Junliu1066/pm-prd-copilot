# 分线程开发测试操作系统

## 启用条件

分线程开发测试必须先通过模块 A：

1. A1 开发可落地性审查结果为 `pass`。
2. A2 开发组织编排确认线程结构、写入边界、依赖、contract、验证和回滚都明确。
3. A3 模块开发前置准备门确认对应模块或线程的 Task Brief、基线、契约、文件边界、骨架、测试入口、质量门禁和本地运行条件已 `pass`。

满足任一条件才启用分线程开发测试：

- 多模块、多页面、多 API 或多端联调。
- DB/API/AI 输出格式等契约已经由上游冻结。
- UI、后端、测试、数据、AI 实现可以独立推进。
- 用户明确要求多分支、多线程或并行开发。

不满足时保持单线程，并记录降级理由。

禁止为了并行而并行。contract 未冻结、写入范围不独立、integration gate 不可定义、失败无法回流责任线程时，不能启用分线程。

## 开发主线卡

| 字段 | 内容 |
|---|---|
| 主线 ID |  |
| 当前开发目标 |  |
| 为什么做 |  |
| 可验证效果 |  |
| 本轮不做 |  |
| 当前状态 | active / waiting_user / blocked / done |
| 最近推进 |  |
| 下一步最小动作 |  |
| 需要上游拍板 |  |

## 分线程矩阵

| 线程 ID | 开发目标 | 写入范围 | 禁止范围 | 依赖 | contract | A3 前置准备 | 风险 | 负责人 | 状态 | B 门禁 |
|---|---|---|---|---|---|---|---|---|---|---|
| T-A |  |  |  |  | frozen / none | pending / pass / prepare_required / blocked | low / medium / high | dev / test | planned | pending |

## 写入边界规则

- 每个线程必须有唯一主写入范围。
- 共享文件只能由 integration 线程或约定 owner 修改。
- 测试文件可与对应模块同线程修改，但必须写明路径。
- migration、schema、权限、AI 输出格式、发布配置默认高风险；开发 agent 不自行决定。
- 发现需要越界时，生成 scope change request，不直接改。

## Contract 状态

开发 agent 不负责定义 contract，只负责确认是否足够开发测试。

| 契约 | owner | 状态 | 依赖线程 | 不足时处理 |
|---|---|---|---|---|
| API | 上游 / 架构侧 | missing / draft / frozen |  | 上报 |
| DB schema | 上游 / 架构侧 | missing / draft / frozen |  | L3 上报 |
| AI output | 上游 / 架构侧 | missing / draft / frozen |  | 上报 |
| permission | 上游 / 架构侧 | missing / draft / frozen |  | 上报 |
| page state | 上游 / 架构侧 | missing / draft / frozen |  | 上报 |

## 分线程启动包

```text
线程 ID：
分支名：
开发目标：
上下文摘要：
输入材料：
允许修改范围：
禁止修改范围：
依赖线程：
contract 状态：
模块 A3 前置准备：
相关文件：
执行步骤：
验证命令：
验收标准：
失败处理：
模块 B 质量门禁要求：
红绿测试要求：
执行证据要求：
需要用户确认：
```

## 状态机

```text
planned
-> ready
-> running
-> self_checked
-> quality_reviewed
-> quality_gate_passed
-> integration_pending
-> integration_passed / integration_failed
-> fix_required / blocked / closed
```

## 状态准入

| 进入状态 | 必要条件 |
|---|---|
| ready | 输入、范围、依赖、验证、回滚已明确，且 A3 准备缺口已列明。 |
| running | A3 `module_development_preflight.status = pass`，无 P0 阻塞，写入范围明确。 |
| self_checked | 线程内检查已完成并有证据。 |
| quality_reviewed | 模块 B 已检查 diff、任务完成度、红绿测试证据、测试证据、contract、边界、可维护性、回滚和架构经验反馈。 |
| quality_gate_passed | 模块 B 输出 `status: pass`，且红绿测试、测试、范围、人工确认点通过。 |
| integration_pending | 依赖线程全部 `quality_gate_passed`。 |
| integration_passed | 集成检查通过。 |
| closed | 执行证据已记录，剩余风险已上报。 |

## Integration 规则

- 所有线程先进入 integration / test，不直接合 main。
- 线程进入业务实现前必须先通过 A3；A3 为 `prepare_required` 时只能补准备项，A3 为 `blocked` 时必须停止并上报。
- 所有线程必须先通过模块 B 质量稳定性门禁，才能进入 integration。
- integration 失败时由模块 B 先定位责任线程。
- 模块或线程开发结束并完成 self-check 后，自动运行模块 B；不得把未过 B 的产物直接并入 integration。
- 行为变更、bug 修复、contract 变更或测试变更必须先完成 Red / Green / Regression 证据；缺 red evidence 且无合理不适用原因时不得进入 `quality_gate_passed`。
- B 发现的 bug 模式、架构问题、contract 风险和重复性问题必须记录为架构反馈经验，供后续线程、validation plan 和架构侧处理。
- 修复只回到责任线程或专门 fix 线程。
- 不接受“测试失败但先合”的默认处理。
- 高风险未解决项必须上报用户或上游架构侧。
- 架构反馈不等于自动修改架构 contract，也不等于写入 stable、长期记忆、registry、workflow、skill 或 harness；涉及这些边界时必须上报。

## 失败回流

| 失败类型 | 处理 |
|---|---|
| 编译 / lint | 回责任线程最小修复。 |
| A3 缺准备项 | 回责任线程补 Task Brief、baseline、骨架、smoke test、测试入口或本地运行说明；不得写业务逻辑。 |
| A3 blocked | 停止实现，输出 approval request。 |
| 单元测试失败 | 定位责任模块，补测试或修实现。 |
| 缺 Red / Green / Regression 证据 | 回责任线程补齐红绿测试或写明合理不适用原因。 |
| API contract 破坏 | 停止并上报 contract owner。 |
| DB migration 风险 | 暂停，L3 上报。 |
| UI 回归 | 回 UI 线程，补手工或视觉证据。 |
| AI 输出漂移 | 回 prompt / eval 线程；若方案不清，停止上报。 |
| 范围漂移 | 暂停，回 PM / 用户确认。 |
| 重复 bug / 架构模式问题 | 回责任线程做最小修复，同时沉淀 architecture feedback 和预防检查。 |

## 架构反馈登记

模块 B 发现的问题必须沉淀为当前项目内的架构反馈，并在下一轮 A1 / A2 / A3 前读取。

| source_thread | source_gate | issue_type | root_cause | impact | prevention_rule | reusable_check | upstream_architecture_action | status | next_a1_input | next_a2_input | next_a3_input |
|---|---|---|---|---|---|---|---|---|---|---|---|
|  |  | bug_pattern / architecture_issue / contract_risk / boundary_violation / test_gap |  |  |  |  |  | open / accepted / rejected / resolved | yes / no | yes / no | yes / no |

规则：

- 普通 bug pattern 反哺测试计划和 reusable check。
- 架构问题反哺 contract、线程边界和 validation plan。
- 重复问题反哺 A1 检查项、A2 编排规则和 A3 前置准备门。
- 涉及高风险边界时，不直接改架构，先生成 approval request。

## Approval Request

```text
approval_request:
  decision_needed:
  trigger:
  risk:
  options:
  recommended_option:
  default_safe_action:
  resume_condition:
```

## Closeout

每个线程关闭前记录：

| 字段 | 内容 |
|---|---|
| 完成内容 |  |
| 修改文件 |  |
| 检查结果 |  |
| red / green / regression evidence |  |
| 模块 A3 前置准备门 | pass / prepare_required / blocked |
| 模块 B 质量门禁 | pass / fix_required / blocked |
| findings / test gaps |  |
| architecture feedback | bug patterns / architecture issues / prevention rules / reusable checks / upstream actions |
| 未检查项 |  |
| 剩余风险 |  |
| 回滚方式 |  |
| 是否越界 | yes / no |
| 需上游处理 | none / requirement / architecture / testing / release |

## WIP 限制

- 开发主线同时只能有 1 个。
- 高风险线程同时最多 1 个 running。
- 未冻结契约前，不启动依赖线程。
- 线程长时间无推进时只生成停滞报告，不自动归档或删除。
