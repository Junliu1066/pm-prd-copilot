# 开发测试 Agent 任务卡

这些任务卡可以直接复制给开发 agent，按项目实际路径替换占位符。

## 1. 输入梳理卡

```text
你是 Development Test Agent。请先只做开发输入梳理，不写代码。

目标：
- 读取 AGENTS.md / agent.md / README / package 配置 / 测试入口。
- 读取上游 Codex 开发文档、任务包、bug 报告、测试计划和验收标准。
- 输出当前开发主线、已确认事实、工作假设、P0/P1/P2 问题。
- 判断是否可进入开发实现。

禁止：
- 不改文件。
- 不补需求范围。
- 不新增 skill / harness / workflow。

输出：
- 开发主线卡。
- 输入材料表。
- 阻塞问题表。
- 下一步最小动作。
```

## 2. 模块 A1：开发可落地性审查卡

```text
请执行模块 A1：开发可落地性审查。只审查开发文档是否能支撑工程开发，不写代码、不拆执行线程。

输入：
- Codex 开发文档：
- 任务包：
- bug 报告：
- 测试计划：
- 验收标准：
- contract：
- 目标项目规则：

必须检查：
- 目标是否清楚。
- 需求边界、允许范围、禁止范围是否清楚。
- 模块、接口、数据流、状态流是否清楚。
- API / DB / AI / 权限 / 页面状态 contract 是否 frozen 或可执行。
- 测试方式、验收标准、回滚方式是否明确。
- 是否存在 P0 blocker、P1 assumption、P2 follow-up。
- 是否触发 DB、模型、MCP、发布、stable、长期记忆等 L3 审批。

输出：
engineering_feasibility_review:
  status: pass | needs_revision | blocked
  blockers:
  missing_information:
  ambiguity:
  risk:
  required_document_fixes:
  recommendation:

规则：
- status 不是 pass 时，不进入开发实现。
- needs_revision 时，反向输出开发文档补全建议。
- blocked 时，列出必须由用户或上游拍板的问题。
- pass 仅在目标、范围、接口、数据流、状态流、contract、测试、验收、回滚都足够明确，且没有未批准 L3 风险时使用。
- needs_revision 用于信息缺失或表达模糊但不涉及高风险执行动作。
- blocked 用于未冻结 contract、DB、模型、MCP、发布、stable、长期记忆、权限安全等高风险边界。
```

## 3. 模块 A2：开发组织编排卡

```text
请执行模块 A2：开发组织编排。前提是 A1 engineering_feasibility_review.status = pass。

目标：
- 把已通过审查的开发文档治理成可执行、可并行、可验证、可回滚的开发结构。

必须输出：
- development_mainline_card
- thread_matrix
- thread_startup_packages
- write_boundary_table
- dependency_table
- contract_freeze_table
- dynamic_skill_harness_plan
- validation_plan
- integration_plan
- rollback_plan
- approval_points

分线程启用条件：
- 多模块、多页面、多 API 或多端联调。
- 独立写入范围明确。
- contract 已 frozen。
- integration gate 可定义。
- 失败能回流到责任线程。

规则：
- 不满足分线程条件时保持单线程，并记录降级理由。
- 不扩大需求范围。
- 不批准数据库、模型、MCP、GitHub、memory 或 stable skill 变更。
- 不把分线程当作 push、PR、发布或合并授权。

dynamic_skill_harness_plan 格式：
trigger:
candidate_skill_or_harness:
use_or_skip:
reason:
command_or_reference:
expected_evidence:
result:
follow_up:

规则：
- 涉及 skill 包跑 skill 校验。
- 涉及 harness 约束跑 harness check。
- 涉及回归影响跑 regression。
- 涉及 UI 跑浏览器、手工或替代验证。
- 不相关的 skill / harness 记录 skip reason。
- 动态使用不等于新增或注册 stable skill / harness。
```

## 4. 模块 A3：模块开发前置准备门卡

```text
请执行模块 A3：模块开发前置准备门。前提是 A1 engineering_feasibility_review.status = pass，且 A2 已输出可执行结构。只判断模块是否具备开始写业务代码的前置条件；不写业务逻辑、不扩大需求、不新增工具。

输入：
- A1 engineering_feasibility_review：
- A2 development orchestration：
- 目标模块：
- 目标项目规则：
- 当前工作区：

必须输出：
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

engineering_baseline:
  git_status:
  check_all_command:
  baseline_status:
  dirty_worktree_explanation:
  baseline_action:

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

file_boundary:
  allowed_paths:
  forbidden_paths:
  locked_paths:
  locked_path_change_request:

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

必须检查：
- 是否已有完整 module_task_brief；没有则 prepare_required。
- 是否已运行或记录 git status。
- 是否存在 make check-all；不存在时是否从 A2 validation_plan 指定替代 baseline 命令。
- 当前工作区是否干净或脏变更可解释。
- contract 是否存在且 frozen 或足够执行。
- 是否需要 Contract Change Request。
- allowed / forbidden / locked paths 是否明确。
- 是否需要修改数据库 migration、公共响应体、权限框架、全局异常、公共工具、全局架构文件、PRD / 原型 / 契约文档。
- 后端模块是否具备 controller / service / repository / entity / dto / mapper / validator / test 骨架。
- 前端模块是否具备 pages / components / api / store / types / tests 骨架。
- 数据和状态模型是否明确。
- 是否至少有 smoke test 或测试入口。
- 质量门禁和本地运行条件是否可执行。
- 失败处理协议是否明确。

判定规则：
- pass：Task Brief、工程基线、契约、文件边界、骨架、数据模型、测试骨架、质量门禁、本地运行条件和失败处理协议全部明确。
- prepare_required：缺少可补的准备项，例如 smoke test、模块骨架、本地运行说明、测试入口、baseline 记录；只能先补准备项，不能写业务逻辑。
- blocked：契约不存在或要变、需要改 locked path，或涉及 DB migration、权限框架、公共响应体、全局异常、MCP、模型、stable、发布等高风险边界；输出 approval_request，停止实现。

禁止：
- 不边写代码边发明接口、字段或状态。
- 不修改 locked path。
- 不跳过基线、契约、文件边界、测试入口或质量门禁。
- 不为了进入实现而把未知项写成已确认。
```

## 5. 开发测试执行文档补全卡

```text
请基于上游输入补全开发测试执行文档。

输入：
- 需求边界 / 验收标准：
- Codex 开发文档：
- 原型 / 页面流：
- 代码仓库：
- 当前约束：

要求：
- 不改变需求范围。
- 选择单线程开发测试、分线程开发测试或修复测试模式。
- 生成任务包、允许修改范围、禁止修改范围、验证命令、回滚方案、人工确认点。
- 如启用分线程，只生成开发测试分线程矩阵和 integration 计划。

禁止：
- 不批准数据库、模型、MCP、GitHub、memory 或 stable skill 变更。
- 不设计治理架构。
```

## 6. 技术实现拆解卡

```text
请把已确认的开发范围拆成实现模块，不估时、不改范围。

必须输出：
- UI / client scope。
- API / service scope。
- data / migration scope，若不涉及请明确 none。
- permission / privacy / security scope。
- AI / prompt scope，若不涉及请明确 none。
- testing scope。
- blockers for upstream。

每个 scope 都要写依赖、风险和验收方式。
```

## 7. 分线程启动卡

```text
请为线程 <THREAD_ID> 执行开发测试任务。

目标：

上下文：

允许修改：

禁止修改：

依赖：

contract 状态：

A3 module_development_preflight：

检查命令：

验收标准：

模块 B 质量门禁要求：

规则：
- 只改允许范围。
- A3 未 pass 时不得进入业务实现；prepare_required 只补准备项，blocked 停止上报。
- 发现需要越界时，停止并生成 scope change request。
- 完成后输出修改文件、检查结果、未检查项、模块 B 门禁结果、回滚方式和 closeout。
```

## 8. 代码实现卡

```text
请执行最小可接受实现。

如环境可用，请优先调用上游 skill：
- incremental-implementation
- test-driven-development

步骤：
1. 确认 A3 module_development_preflight.status = pass。
2. 读取相关代码和本地模式。
3. 说明将要修改的文件和原因。
4. 实现最小变更。
5. 运行目标检查。
6. 对行为变更、bug 修复、contract 变更或测试变更执行红绿测试：先 Red，再 Green，再 Regression。
7. 修复直接失败。
8. 输出 Round 1 / Round 2 和 red / green / regression 结果。
9. 进入模块 B 质量稳定性门禁；未通过不得进入 integration 或 closeout。

禁止：
- 不做无关重构。
- 不覆盖用户已有改动。
- 不在 A3 prepare_required 或 blocked 时写业务逻辑。
- 不新增依赖，除非任务明确批准。
- 不改发布、模型、数据库或 stable 治理组件。
```

## 9. 测试执行卡

```text
请只执行测试和验证，不新增功能。

如环境可用，请优先调用上游 skill：
- test-driven-development
- browser-testing-with-devtools（仅浏览器目标）

输入：
- 待测变更：
- 验收标准：
- 检查命令：

要求：
- 运行目标检查。
- 记录失败日志要点。
- 区分代码缺陷、测试缺陷、环境问题和输入不完整。
- 只在明确要求时修复；否则输出测试报告。
```

## 10. 模块 B：开发质量稳定性门禁卡

```text
请执行模块 B：开发质量稳定性门禁。只检查开发结果是否可用、稳定、可靠、可集成，不拆任务、不扩大需求。

触发规则：
- 每个模块或线程开发结束并完成 self-check 后，自动运行模块 B。
- B 未输出 pass 前，不得进入 integration 或 closeout。
- B 发现的 bug、重复性问题、架构问题和 contract 风险，必须沉淀为 architecture feedback，反哺后续架构和开发组织。
- architecture feedback 不得自动写入 stable、长期记忆、registry、workflow、skill 或 harness；涉及这些边界时输出 blocked 和 approval_needed。

如环境可用，请优先调用上游 skill：
- code-review-and-quality
- security-and-hardening（涉及输入、权限、数据、外部集成）

输入：
- 当前线程任务包：
- 本轮 diff：
- 已运行检查：
- 失败日志：
- contract 状态：
- 验收标准：

必须检查：
- diff_scope_check：diff 是否只服务当前任务，有无无关重构、调试残留、临时代码、重复逻辑、大块搬运。
- task_completion_check：是否完成当前线程任务和验收标准。
- bug_regression_check：是否存在 bug、回归、错误路径缺失、空状态缺失、权限 / 数据风险。
- contract_integrity_check：是否破坏 API / DB / AI / 权限 / 页面状态 contract。
- test_evidence_check：测试、手工检查或替代验证是否覆盖改动行为。
- red_green_test_check：行为变更、bug 修复、contract 变更或测试变更是否有 Red / Green / Regression 证据；纯文档、注释或无行为配置变更是否写明 not_applicable_reason。
- boundary_check：是否越过允许写入范围、需求范围、DB / 模型 / MCP / 发布 / stable 治理边界。
- maintainability_check：命名、接口、复杂度、重复逻辑、项目模式是否可维护。
- rollback_readiness_check：是否有最小回滚路径和回滚后应重跑的检查。
- integration_readiness_check：是否可以进入 integration 或 closeout。
- architecture_feedback_check：是否已记录 bug pattern、架构问题、预防规则、可复用检查和需要架构侧处理的 action。

输出：
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

状态规则：
- pass：可以进入 integration 或 closeout。
- fix_required：回责任线程做最小修复，重跑相关检查。
- blocked：涉及需求、contract、DB、模型、MCP、发布、stable 等边界，停止并上报。

判定规则：
- pass：任务完成、diff 未越界、contract 未破坏、红绿测试或合理不适用说明充分、测试或替代验证充分、无阻断风险、回滚路径明确。
- fix_required：普通 bug、缺测试、缺 red / green / regression 证据、实现遗漏或可维护性问题仍在当前责任线程内可最小修复。
- blocked：涉及需求变化、contract 变化、DB、模型、MCP、发布、stable、长期记忆、权限安全等边界。

红绿测试硬规则：
- 有行为变更 / bug 修复 / contract 变更 / 测试变更时必须做红绿测试。
- Red：新增或修改测试先失败，并能证明捕捉目标问题。
- Green：实现或修复后相关测试通过。
- Regression：相关回归检查通过。
- 纯文档、注释或无行为配置变更可标记 not_applicable，但必须说明原因。
- 缺 red_evidence 且无 not_applicable_reason 时，B 不得 pass。

如 blocked，请同时输出：
approval_request:
  decision_needed:
  trigger:
  risk:
  options:
  recommended_option:
  default_safe_action:
  resume_condition:

每次 B 都输出 architecture feedback register；无新增经验时写 none：
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

## 11. Integration 卡

```text
请执行 integration / test，不新增功能。

输入：
- 已通过 gate 的线程：
- contract 状态：
- 检查命令：

要求：
- 先检查依赖线程是否全部通过模块 B，状态为 pass。
- 先确认相关线程 A3 前置准备门均已 pass。
- 对齐共享契约。
- 运行集成检查。
- 失败时通过模块 B 定位责任线程。
- 输出 integration report。

禁止：
- 不直接合 main。
- 不 push / PR。
- 不接受高风险未解决项。
```

## 12. CI / 测试失败修复卡

```text
请修复以下失败，目标是最小修复。

如环境可用，请优先调用上游 skill：
- debugging-and-error-recovery
- test-driven-development

失败信息：

相关分支 / 文件：

要求：
- 先复现或读取日志。
- 定位根因。
- 只改责任范围。
- 重跑失败检查和必要回归。
- 输出根因、修复、验证证据、剩余风险。
```

## 13. Closeout 卡

```text
请为本轮开发测试生成 closeout。

必须包含：
- 完成了什么。
- 修改了哪些文件。
- 跑了哪些检查。
- 哪些检查不能跑及原因。
- 模块 A1/A2/A3 是否通过及线程组织结论。
- 模块 B quality_stability_gate 结果。
- architecture feedback register，若无则写 none。
- 剩余风险。
- 回滚方式。
- 用户或上游需要拍板什么。
- 哪些事项需要需求 / 架构 / 发布侧处理。

禁止：
- 不写长期记忆。
- 不把 candidate 转 stable。
- 不删除或归档文件。
```
