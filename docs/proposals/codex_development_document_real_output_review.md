# Codex 开发文档真实输出复核报告

- 日期：2026-05-04
- 状态：复核与修复记录，不批准 staging、commit、push、PR、删除、归档、长期记忆写入、stable 转正或新增 skill / harness。
- 主线任务：确认“普通 PRD -> Codex 开发文档”的实际输出是否已经轻量化，避免把 Skill / MCP / Harness / 多管家治理系统默认塞进普通开发文档。
- 结论：delivery suite 的输出合同已经收敛为“轻量 / 完整”分层；默认 Codex 开发文档模板已完成收敛，普通 PRD 默认走轻量开发文档，完整治理结构只在 full internal / agentic delivery 模式启用。

## 0. 本轮执行结果

| 项目 | 结果 |
|---|---|
| 是否新增模板 | 否，复用并收敛现有 `codex_development_document_template.md`。 |
| 是否新增 skill / harness | 否。 |
| 是否写项目产物 | 否。 |
| 普通 PRD 默认输出 | 轻量 Codex 开发文档。 |
| 完整治理输出 | 仅作为附录保留，必须满足 full internal / agentic delivery / 多阶段治理 / Skill-MCP-Harness 改造条件。 |
| 当前状态 | `lightweight_sample_review_passed`。 |

## 1. 复核范围

| 范围 | 文件 | 复核目的 |
|---|---|---|
| 内部默认 Codex 开发文档模板 | `pm-prd-copilot/templates/codex_development_document_template.md` | 判断普通 PRD 是否会默认输出过重治理结构。 |
| 外部保护版开发文档模板 | `pm-prd-copilot/templates/external_protected_development_document_template.md` | 判断外部分发是否已经隔离内部治理机制。 |
| Agentic delivery 输出合同 | `plugins/delivery-planning-suite/skills/agentic-delivery-orchestrator/references/output-contract.md` | 判断轻量 / 完整模式是否已经分层。 |
| Codex task package 输出合同 | `plugins/delivery-planning-suite/skills/codex-task-package-writer/references/output-contract.md` | 判断任务包是否会默认生成 registry / harness / full governance。 |
| 0-1 普通业务 PRD 样例 | `pm-prd-copilot/evals/golden_cases/zero_to_one_service_prd/expected_prd.md` | 判断普通 PRD 的输入是否需要完整治理系统。 |

## 2. 复核方法

本轮不调用 LLM 生成新项目产物，也不写入 `projects/*`。原因是当前风险可以从真实模板和输出合同中直接判断：

1. 如果默认模板已经包含完整治理系统，那么任何基于该模板生成的普通 Codex 开发文档都有过重风险。
2. 如果输出合同已经要求轻量模式，但模板没有同步，说明链路存在“指令层正确、模板层拖后腿”的不一致。
3. 先记录不一致，再修模板，比直接生成一个临时开发文档更稳。

## 3. 发现的问题

### 3.1 默认 Codex 开发文档模板仍然偏重

当前 `codex_development_document_template.md` 默认写明内部机制包括内部多管家、效率部、教师 / 学习管家、Skill/MCP、harness、registry、memory、随机审计等内容。

它还默认包含：

- 总体开发运行架构。
- Capability Enablement。
- Skill / MCP Discovery 与路由。
- 内部多管家 / 部门分工。
- Harness / 审计 / 效率 / 学习。

这些内容适合“完整内部治理版”或“半自动 agentic delivery”，但不适合作为普通 PRD 的默认开发文档。否则会导致普通项目开发文档过厚、任务包不聚焦，也会让模型误以为每个开发任务都必须展开完整治理系统。

推荐状态：`needs_template_contraction`

### 3.2 Delivery suite 输出合同已经收敛，但模板还没跟上

`agentic-delivery-orchestrator` 已经定义：

- 普通开发就绪 PRD 使用 lightweight Codex delivery。
- 默认禁止输出 phase 1 / 2 / 3 / final 全套计划。
- 默认禁止完整 Skill/MCP/Harness operating-system exposition。

`codex-task-package-writer` 也已经定义：

- 普通 Codex 开发文档只需要开发范围、任务包、允许 / 禁止写入范围、验证命令、人工确认点、最小修复策略和回滚 / 审查。
- 默认禁止 new skill creation、MCP integration、registry / harness changes 和 full governance operating system。

因此当前问题不是 skill 方向错误，而是模板仍停留在旧的“内部完整版默认”口径。

推荐状态：`contract_ok_template_lagging`

### 3.3 外部保护版模板是轻的，但不能解决内部默认过重

`external_protected_development_document_template.md` 已经按 B 包 / 外部分发边界处理，内容更接近执行型开发文档，隐藏了内部治理机制。

但这只解决外部分发安全，不解决内部普通项目的默认开发文档过重问题。内部开发也需要轻量默认，否则会浪费 token 和注意力。

推荐状态：`external_template_ok_internal_default_needs_fix`

### 3.4 0-1 普通业务 PRD 不需要默认完整治理系统

当前 0-1 普通业务 PRD 样例已经包含：

- 摘要。
- 产品总览思维导图。
- 用户 / 场景 / 范围。
- 核心流程。
- 页面说明。
- 页面跳转关系。
- 原型图层。
- 状态流转。

这类输入足够支撑轻量 Codex 开发文档，不需要默认展开 Skill / MCP / Harness / 多管家治理系统。只有当项目明确涉及 agentic delivery、能力启用、MCP 接入、harness 改造或长期治理扩展时，才需要完整内部版。

推荐状态：`ordinary_prd_should_use_lightweight_default`

## 4. 修复方案与结果

### 4.1 已执行方案

已对 `pm-prd-copilot/templates/codex_development_document_template.md` 做小范围收敛：

- 保留一个模板文件，不新增新模板。
- 把默认模式改成“轻量 Codex 开发文档”。
- 将完整内部治理内容改成“仅在用户明确要求完整 agentic delivery / 多阶段开发治理 / Skill-MCP-Harness 改造时启用”。
- 普通默认结构只保留：
  - 文档目标。
  - 输入材料。
  - 开发范围。
  - 任务包。
  - 允许修改范围。
  - 禁止修改范围。
  - 人工确认点。
  - 验证命令。
  - 回滚方案。
  - 待决策项。
  - 审核结论。
- 保留完整治理附录，但标记为 `full internal mode only`。

### 4.2 修复后的普通输出结构

普通 PRD 的默认 Codex 开发文档现在只要求：

1. 文档目标。
2. 输入材料。
3. 开发范围。
4. 任务包。
5. 允许修改范围。
6. 禁止修改范围。
7. 人工确认点。
8. 验证命令。
9. 回滚方案。
10. 待决策项。
11. 审核结论。

普通输出默认不展开：

- phase 1 / phase 2 / phase 3 / final 全套 Codex 计划。
- 完整 Skill / MCP / Harness 操作系统说明。
- 内部多管家 / 部门体系全量展开。
- development governance report。
- 长期记忆、skill、harness、registry 的稳定规则变更。

### 4.3 这么做的效果

| 效果 | 说明 |
|---|---|
| 降低普通开发文档负担 | 普通 PRD 不再默认生成完整治理系统，任务更聚焦。 |
| 保留完整治理能力 | 真正需要 agentic delivery 时仍可启用完整模式，不丢能力。 |
| 避免新增文件 | 复用现有模板，符合“如无必要，不新增”的原则。 |
| 降低任务漂移 | 开发文档只服务开发任务，不把架构治理讨论带入普通项目。 |
| 更利于长期稳定 | 指令层、模板层、回归样例能对齐，减少后续输出退化。 |

### 4.4 风险

| 风险 | 控制方式 |
|---|---|
| 过度收敛导致完整治理能力找不到入口 | 保留 full internal mode 附录和启用条件。 |
| 修改模板后影响已有内部完整开发文档习惯 | 先做模板 wording 修复，不批量回扫历史项目。 |
| 轻量模板太轻，漏掉关键门禁 | 保留人工确认点、验证命令、回滚方案和待决策项作为底线。 |

## 5. 需要你后续拍板

| 决策 | 我的建议 | 不同选择的效果 |
|---|---|---|
| 是否修 `codex_development_document_template.md` | 已按建议修 | 消除了“skill 合同已收敛但模板仍过重”的不一致。 |
| 是否新增轻量模板文件 | 未新增 | 复用一个模板更简单，减少长期维护入口。 |
| 是否现在生成真实项目开发文档样例 | 建议等检查通过后再按需生成 | 避免在治理线程写项目产物；后续可用临时目录或项目线程验证。 |
| 是否改外部保护版模板 | 暂不改 | 外部模板当前边界较清楚，先不扩大修改范围。 |
| 是否把完整治理版废弃 | 不废弃 | 完整治理仍服务 agentic delivery，只是不再作为普通默认。 |

## 6. 当前结论

当前链路比复核前更稳定。准确状态是：

- Skill / delivery suite 输出合同：已基本收口。
- 外部保护版开发文档模板：基本可用。
- 内部默认 Codex 开发文档模板：已收敛为轻量默认 + 完整治理附录。
- 普通 PRD 轻量开发文档样例：已通过临时目录复核。

## 7. 轻量样例复核结果

### 7.1 临时样例

| 项目 | 结果 |
|---|---|
| 临时样例路径 | `/private/tmp/codex-devdoc-lightweight-review/codex_development_document.sample.md` |
| 输入 PRD | `pm-prd-copilot/evals/golden_cases/zero_to_one_service_prd/expected_prd.md` |
| 是否写入 `projects/*` | 否 |
| 是否进入 git 暂存 | 否 |
| 复核结论 | 通过 |

### 7.2 轻量必备结构检查

样例包含以下轻量必备部分：

- 文档目标。
- 输入材料。
- 开发范围。
- 任务包。
- 允许修改范围。
- 禁止修改范围。
- 人工确认点。
- 验证命令。
- 回滚方案。
- 待决策项。
- 审核结论。

### 7.3 旧口径残留检查

样例没有默认展开以下内容：

- 内部多管家 / 部门体系。
- 完整 Skill / MCP / Harness 操作系统。
- phase 1 / phase 2 / phase 3 / final 全套计划。
- development governance report。
- Capability Enablement 全量检查。
- Skill / MCP Discovery 全量路由。
- 教师 / 学习沉淀。
- 随机审计。

样例中出现 `Skill / MCP / Harness`、`phase 1 / phase 2 / phase 3 / final`、`development governance report`、`harness`、`registry` 等词时，均用于说明“不输出”或“普通开发不改治理架构”的边界，不是默认执行内容。

### 7.4 对长期稳定的意义

这次复核说明当前模板不只是文字上变轻，按普通 PRD 使用时也能输出轻量开发文档。后续如果开发文档再次变重，问题大概率不是模板结构本身，而是调用方、prompt、项目特例或用户明确要求触发了 full internal 模式。

## 8. 下一步建议

建议下一步进入本轮治理总验收报告：

```text
汇总 A/B/C/D/E/PRUNE/ARCHIVE/THREAD 修复状态
-> 列出剩余未处理项
-> 集中列出仍需用户拍板项
-> 给出下一阶段提交 / 暂缓 / 观察建议
```
