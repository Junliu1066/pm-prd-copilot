# 开发测试执行文档模板

- 文档状态：
- 上游开发文档 / 任务包：
- 开发 agent：
- 最后更新：
- 模式：单线程开发测试 / 分线程开发测试 / 修复测试

## 0. 开发主线与边界

| 项目 | 内容 |
|---|---|
| 当前开发任务 |  |
| 为什么做 |  |
| 预期可验证效果 |  |
| 本轮不做 |  |
| 读者 | 开发 agent / 测试 agent / 人工 reviewer |

## 1. 输入材料

### 1.1 已确认事实

-

### 1.2 工作假设

| 假设 | 影响范围 | 验证方式 | 失效处理 |
|---|---|---|---|
|  |  |  |  |

### 1.3 阻塞问题

| 优先级 | 问题 | 影响 | 当前处理 |
|---|---|---|---|
| P0 |  | 阻塞开发或测试 | 停下确认 |
| P1 |  | 可带假设推进 | 标注假设 |
| P2 |  | 不阻塞本轮 | 后续确认 |

### 1.4 输入文件

| 类型 | 路径 / 链接 | 状态 | 备注 |
|---|---|---|---|
| 需求边界 / 验收标准 |  | confirmed / draft / missing |  |
| Codex 开发文档 |  | confirmed / draft / missing |  |
| 原型 / 页面流 |  | confirmed / draft / missing |  |
| API / DB contract |  | frozen / draft / missing |  |
| 现有代码 |  | inspected / not inspected |  |
| 测试命令 |  | runnable / unknown / unavailable |  |

## A. 开发可落地性治理

模块 A 是开发前治理控制面。它不写代码，不扩大需求；先审查开发文档能否支撑工程开发，通过后才组织执行结构。

### A1. Engineering Feasibility Review

```text
engineering_feasibility_review:
  status: pass | needs_revision | blocked
  blockers:
  missing_information:
  ambiguity:
  risk:
  required_document_fixes:
  recommendation:
```

| 检查项 | 结论 | 问题 / 建议 |
|---|---|---|
| 目标是否清楚 |  |  |
| 需求边界、允许范围、禁止范围是否清楚 |  |  |
| 模块、接口、数据流、状态流是否清楚 |  |  |
| API / DB / AI / 权限 / 页面状态 contract 是否 frozen 或可执行 |  |  |
| 测试方式、验收标准、回滚方式是否明确 |  |  |
| P0 blocker / P1 assumption / P2 follow-up 是否已列出 |  |  |
| 是否触发 DB / 模型 / MCP / 发布 / stable / 长期记忆 L3 审批 |  |  |

规则：只有 `status: pass` 才能进入 A2；`needs_revision` 或 `blocked` 只输出问题清单和优化建议，不进入实现。

#### A1 Gate Decision Matrix

| 状态 | 判定条件 | 处理 |
|---|---|---|
| pass | 目标、范围、接口、数据流、状态流、contract、测试、验收、回滚都足够明确，且没有未批准 L3 风险。 | 进入 A2。 |
| needs_revision | 信息缺失或表达模糊，但不涉及高风险执行动作。 | 输出补全文档建议，不进入开发。 |
| blocked | 涉及未冻结 contract、DB、模型、MCP、发布、stable、长期记忆、权限安全等高风险边界。 | 输出 approval request，停止实现。 |

### A2. Development Orchestration

```text
development_mainline_card:
thread_matrix:
thread_startup_packages:
write_boundary_table:
dependency_table:
contract_freeze_table:
dynamic_skill_harness_plan:
validation_plan:
integration_plan:
rollback_plan:
approval_points:
```

| 输出项 | 内容 |
|---|---|
| development_mainline_card |  |
| thread_matrix |  |
| thread_startup_packages |  |
| write_boundary_table |  |
| dependency_table |  |
| contract_freeze_table |  |
| dynamic_skill_harness_plan |  |
| validation_plan |  |
| integration_plan |  |
| rollback_plan |  |
| approval_points |  |

分线程启用判断：

| 条件 | 是否满足 | 证据 / 降级理由 |
|---|---|---|
| 多模块、多页面、多 API 或多端联调 |  |  |
| 独立写入范围明确 |  |  |
| contract 已 frozen |  |  |
| integration gate 可定义 |  |  |
| 失败能回流到责任线程 |  |  |

结论：启用分线程 / 保持单线程。

#### Dynamic Skill / Harness Plan

```text
dynamic_skill_harness_plan:
  trigger:
  candidate_skill_or_harness:
  use_or_skip:
  reason:
  command_or_reference:
  expected_evidence:
  result:
  follow_up:
```

| trigger | candidate_skill_or_harness | use_or_skip | reason | command_or_reference | expected_evidence | result | follow_up |
|---|---|---|---|---|---|---|---|
|  |  | use / skip |  |  |  |  |  |

规则：涉及 skill 包跑 skill 校验；涉及 harness 约束跑 harness check；涉及回归影响跑 regression；涉及 UI 跑浏览器、手工或替代验证；不相关项记录 skip reason；不得把动态使用变成新增或注册 stable skill / harness。

### A3. Module Development Preflight

A3 在 A2 后、模块业务实现前运行。它不新增工具、不新增 harness、不改 registry，只判断某个模块现在能不能开始写业务代码。

```text
module_development_preflight:
  status: pass | prepare_required | blocked
  module_task_brief:
  engineering_baseline:
  module_contract:
  file_boundary:
  module_skeleton:
  data_state_model:
  test_skeleton:
  quality_gate:
  local_run_preflight:
  forbidden_actions_check:
  required_preparation_fixes:
  approval_needed:
```

#### A3 Decision Matrix

| 状态 | 判定条件 | 处理 |
|---|---|---|
| pass | Task Brief、工程基线、契约、文件边界、骨架、数据模型、测试骨架、质量门禁、本地运行条件和失败处理协议全部明确。 | 进入模块业务实现。 |
| prepare_required | 缺少可安全补齐的准备项，例如 smoke test、模块骨架、本地运行说明、测试入口、baseline 记录。 | 只补准备项，不写业务逻辑。 |
| blocked | 契约不存在或要变、需要改 locked path，或涉及 DB migration、权限框架、公共响应体、全局异常、MCP、模型、stable、发布等高风险边界。 | 输出 approval request，停止实现。 |

#### Module Task Brief

```text
module_task_brief:
  module_name:
  module_goal:
  development_scope:
  non_goals:
  input_documents:
  allowed_files:
  forbidden_files:
  locked_files:
  dependency_modules:
  affected_modules:
  acceptance_criteria:
  required_commands:
  failure_handling:
```

没有 `module_task_brief` 时，A3 必须输出 `prepare_required`，不得进入业务实现。

#### Engineering Baseline

```text
engineering_baseline:
  git_status:
  check_all_command:
  baseline_status:
  dirty_worktree_explanation:
  baseline_action:
```

默认先检查 `git status` 和 `make check-all`。如果项目没有 `make check-all`，记录 `unavailable`，并从 A2 `validation_plan` 中指定替代 baseline 命令。没有任何可执行 baseline 时，A3 输出 `prepare_required`。

#### Module Contract

```text
module_contract:
  api_paths:
  request_fields:
  response_fields:
  error_codes:
  permission_rules:
  idempotency_rules:
  pagination_rules:
  state_enums:
  audit_log_requirements:
  database_tables_fields:
  cross_module_calls:
  contract_change_request:
```

契约缺失时先补契约；契约要变时输出 Contract Change Request。不得边写代码边发明接口、字段或状态。

#### File Boundary

```text
file_boundary:
  allowed_paths:
  forbidden_paths:
  locked_paths:
  locked_path_change_request:
```

locked path 默认包括数据库 migration、公共响应体、权限框架、全局异常、公共工具、全局架构文件、PRD / 原型 / 契约文档。需要修改 locked path 时，A3 输出 `blocked` 和 `approval_request`。

#### Skeleton, Data, Test, Gate

```text
backend_module_skeleton:
  controller:
  service:
  repository:
  entity:
  dto:
  mapper:
  validator:
  test:
```

```text
frontend_module_skeleton:
  pages:
  components:
  api:
  store:
  types:
  tests:
```

```text
data_state_model:
  tables:
  primary_keys:
  unique_constraints:
  indexes:
  state_enums:
  soft_delete:
  audit_fields:
  operation_logs:
  idempotency_key:
  concurrency_control:
  migration_required:
  migration_replayable:
  empty_db_bootable:
  migration_tests:
```

测试骨架至少要有 smoke test。后端模块检查 unit、service、API、permission、exception、idempotency、state transition、migration tests；前端模块检查 render、state、API client、permission、error state、smoke tests。质量门禁优先使用 `make check-all`；不可用时必须记录 A2 validation plan 中的替代命令。

## 2. 开发测试范围

| 模块 | 目标 | 主要变更 | 验收标准 |
|---|---|---|---|
|  |  |  |  |

## 3. 不做范围

默认不做：

- 不改需求范围、MVP、优先级或业务流程。
- 不改 stable skill、harness、workflow、registry、memory。
- 不改发布、push、PR、部署。
- 不删文件、不归档、不迁移真实数据。

## 4. 影响面与上报等级

| 类型 | 是否涉及 | 开发 agent 处理 | 上报等级 |
|---|---|---|---|
| 前端页面 / 交互 |  | 可按任务包开发测试 | L1 / L2 |
| 后端接口 / 服务 |  | 可按 frozen contract 开发测试 | L1 / L2 |
| 数据库 / 数据迁移 |  | 只在明确批准后执行 | L3 |
| 权限 / 隐私 / 安全 |  | 不清楚则停下上报 | L2 / L3 |
| AI / Prompt / 模型 |  | 只实现已批准方案 | L2 / L3 |
| 外部 API / MCP |  | 不自行新增 | L3 |
| 发布 / GitHub |  | 不自行执行 | L3 |
| stable 治理组件 |  | 不自行改动 | L3 |

## 5. 技术拆解

| 层 | 工作项 | 依赖 | 风险 |
|---|---|---|---|
| UI / client |  |  |  |
| API / service |  |  |  |
| data / migration |  |  |  |
| AI / prompt |  |  |  |
| tests / QA |  |  |  |
| ops / config |  |  |  |

## 6. Contract 状态

开发 agent 不负责定义 contract，只负责检查是否足够执行。

| 契约 | 状态 | 依赖任务 | 不足时处理 |
|---|---|---|---|
| API contract | missing / draft / frozen / none |  | 上报 |
| DB schema | missing / draft / frozen / none |  | 上报 |
| AI 输出格式 | missing / draft / frozen / none |  | 上报 |
| 页面状态结构 | missing / draft / frozen / none |  | 上报 |
| 权限规则 | missing / draft / frozen / none |  | 上报 |

## 7. 任务包

| ID | 目标 | 输入 | 允许修改 | 禁止修改 | 输出 | 验证 | 人工确认 |
|---|---|---|---|---|---|---|---|
| T1 |  |  |  |  |  |  |  |

### 7.1 任务包细节

```text
任务 ID：
目标：
上下文摘要：
允许修改范围：
禁止修改范围：
依赖：
执行步骤：
预期输出：
验证命令：
验收标准：
回滚方案：
失败处理：
执行证据：
```

## 8. 分线程开发测试

仅在多模块、多页面、多 API、AI、DB/API contract 或用户明确要求并行时启用。

| 线程 | 任务 | 优先级 | 依赖 | 可并行 | 冲突预测 | 风险 | 当前状态 |
|---|---|---|---|---|---|---|---|
| main |  | P0 / P1 / P2 |  |  |  |  | planned |

状态机：

```text
planned -> ready -> running -> self_checked -> quality_reviewed
-> quality_gate_passed -> integration_pending
-> integration_passed / integration_failed
-> fix_required / blocked / closed
```

## 9. 验证计划

| 检查 | 命令 / 方法 | 触发条件 | 通过标准 |
|---|---|---|---|
| 格式 / 语法 |  | 每次改动后 |  |
| 单元测试 |  | 相关模块修改 |  |
| 集成 / API |  | API 或数据改动 |  |
| UI 手工检查 |  | 页面或交互改动 |  |
| 回归 |  | 共享逻辑改动 |  |
| 目标验收 |  | 本轮交付前 |  |
| Red 测试 |  | 行为变更 / bug 修复 / contract 变更 / 测试变更 | 新增或修改测试先失败并捕捉目标问题，或记录不适用原因 |
| Green 测试 |  | Red 后 / 修复后 | 相关测试通过 |
| Regression 测试 |  | Green 后 / 共享逻辑改动 | 相关回归通过 |

无法运行检查时记录：

- 原因：
- 替代检查：
- 剩余风险：

## 10. 人工确认点

| 确认点 | 触发条件 | 未确认时处理 |
|---|---|---|
| 需求范围变化 | 新增、删除或改变核心能力 | 停下回问 |
| 数据库 / 迁移 | schema、迁移、数据清洗、删除 | 停下回问 |
| 外部 API / MCP | 新接入外部能力 | 停下回问 |
| AI 模型 / 成本 | 换模型、升成本、跨境或高风险输出 | 停下回问 |
| 发布 / GitHub | push、PR、上线、外部分发 | 停下回问 |
| 长期规则 | skill、harness、registry、memory、stable policy | 停下回问 |

### 10.1 Approval Request

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

| 字段 | 内容 |
|---|---|
| decision_needed |  |
| trigger |  |
| risk |  |
| options |  |
| recommended_option |  |
| default_safe_action |  |
| resume_condition |  |

## 11. 回滚方案

| 场景 | 回滚方式 | 验证方式 |
|---|---|---|
| 单文件改坏 | 只回滚对应文件 | 重跑相关检查 |
| 功能回退 | 关闭入口或恢复旧逻辑 | 核心路径验证 |
| 数据风险 | 停止迁移或恢复备份 | 数据一致性检查 |
| 提交后撤销 | 优先 git revert | 重跑回归 |

## 12. Round 1 检查记录

| 检查 | 结果 | 证据 |
|---|---|---|
|  | pass / warn / fail / not run |  |

## 13. Round 2 检查记录

| 检查项 | 结论 | 处理 |
|---|---|---|
| 最新开发任务已重读 |  |  |
| diff 范围合理 |  |  |
| 相关测试 / 文档 / schema / 配置已同步或无需同步 |  |  |
| 未越过需求 / 治理 / 发布 / 数据边界 |  |  |
| 未覆盖用户已有改动 |  |  |
| 剩余审批点已列出 |  |  |

## B. 开发质量稳定性治理

模块 B 是开发过程和开发后的质量门禁。它不拆任务，不扩大需求，只判断开发结果是否可用、稳定、可靠、可集成。

模块或线程开发结束并完成 self-check 后，必须自动运行模块 B。B 在检查中发现的代码 bug、重复性错误模式、架构问题和 contract 问题，必须沉淀为当前项目的架构反馈经验，用于反哺后续架构和开发组织；不得自动写入 stable、长期记忆、registry、workflow、skill 或 harness。

### B1. Quality Stability Gate

```text
quality_stability_gate:
  status: pass | fix_required | blocked
  findings:
  test_gaps:
  red_green_test:
    red_evidence:
    green_evidence:
    regression_evidence:
    not_applicable_reason:
  contract_risks:
  boundary_violations:
  required_fixes:
  integration_readiness:
  rollback_route:
  approval_needed:
  architecture_feedback:
    bug_patterns:
    architecture_issues:
    prevention_rules:
    reusable_checks:
    upstream_architecture_actions:
```

| 检查项 | 结论 | 证据 / 处理 |
|---|---|---|
| diff_scope_check |  |  |
| task_completion_check |  |  |
| bug_regression_check |  |  |
| contract_integrity_check |  |  |
| test_evidence_check |  |  |
| red_green_test_check |  |  |
| boundary_check |  |  |
| maintainability_check |  |  |
| rollback_readiness_check |  |  |
| integration_readiness_check |  |  |
| architecture_feedback_check |  |  |

状态规则：

- `pass`：可以进入 integration 或 closeout。
- `fix_required`：回责任线程做最小修复，重跑相关检查。
- `blocked`：涉及需求、contract、DB、模型、MCP、发布、stable 等边界，停止并上报。

B Gate Decision Matrix:

| 状态 | 判定条件 | 处理 |
|---|---|---|
| pass | 任务完成、diff 未越界、contract 未破坏、红绿测试或合理不适用说明充分、测试或替代验证充分、无阻断风险、回滚路径明确。 | 进入 integration 或 closeout。 |
| fix_required | 存在普通 bug、缺测试、缺 red / green / regression 证据、实现遗漏或可维护性问题，且都在当前责任线程内可最小修复。 | 回责任线程修复并重跑相关检查。 |
| blocked | 涉及需求变化、contract 变化、DB、模型、MCP、发布、stable、长期记忆、权限安全等边界。 | 输出 approval request，停止并上报。 |

红绿测试规则：

- 行为变更、bug 修复、contract 变更或测试变更必须执行红绿测试。
- Red：新增或修改测试必须先失败，并证明能捕捉目标问题。
- Green：实现或修复后，相关测试必须通过。
- Regression：相关回归检查必须通过。
- 纯文档、注释或无行为配置变更可写 `not_applicable_reason`。
- 缺 red evidence 且无合理不适用原因时，B 不能 `pass`。

架构经验反馈规则：

- 普通代码 bug：记录 bug pattern、根因、最小修复和新增 / 重跑的回归检查。
- 架构或 contract 问题：记录 architecture issue、影响面、需要架构侧处理的 action；如需改 contract 或高风险边界，状态为 `blocked`。
- 重复性问题：沉淀 prevention rule 和 reusable check，作为后续开发文档、validation plan 或 dynamic skill / harness plan 的输入。
- 无新增经验时明确写 `architecture_feedback: none`。

### B2. 代码产物复核记录

| 复核项 | 结论 | 证据 / 处理 |
|---|---|---|
| diff 是否只服务当前任务 |  |  |
| 是否存在无关重构 / 调试残留 / 临时代码 |  |  |
| 主路径 / 错误路径 / 空状态 / 权限或数据边界是否覆盖 |  |  |
| 测试、手工检查或替代验证是否覆盖改动行为 |  |  |
| red / green / regression evidence 是否完整 |  |  |
| 测试失败是否已区分代码缺陷 / 测试缺陷 / 环境问题 / 输入不完整 |  |  |
| 是否符合现有项目模式和可维护性要求 |  |  |
| 是否有明确回滚路径和重跑检查 |  |  |
| bug / 架构问题是否已沉淀为 architecture feedback |  |  |
| findings | none / list |  |
| test gaps | none / list |  |
| architecture feedback | none / list |  |

### B3. Architecture Feedback Register

```text
architecture_feedback_register:
  source_thread:
  source_gate:
  issue_type: bug_pattern | architecture_issue | contract_risk | boundary_violation | test_gap
  root_cause:
  impact:
  prevention_rule:
  reusable_check:
  upstream_architecture_action:
  status: open | accepted | rejected | resolved
  next_a1_input: yes | no
  next_a2_input: yes | no
  next_a3_input: yes | no
```

| source_thread | source_gate | issue_type | root_cause | impact | prevention_rule | reusable_check | upstream_architecture_action | status | next_a1_input | next_a2_input | next_a3_input |
|---|---|---|---|---|---|---|---|---|---|---|---|
|  |  | bug_pattern / architecture_issue / contract_risk / boundary_violation / test_gap |  |  |  |  |  | open / accepted / rejected / resolved | yes / no | yes / no | yes / no |

## 14. 执行结论

| 项 | 结论 |
|---|---|
| 是否完成开发 |  |
| 是否完成测试 |  |
| A3 模块开发前置准备门是否通过 | pass / prepare_required / blocked |
| 是否存在 P0 阻塞 |  |
| 最小可接受实现 |  |
| 剩余需上游处理 |  |
| architecture feedback 是否进入下一轮 A1/A2/A3 | yes / no |
