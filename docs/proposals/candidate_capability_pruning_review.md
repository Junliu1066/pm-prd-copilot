# Candidate 能力瘦身复盘报告

- 日期：2026-05-04
- 状态：审查和小范围边界收敛记录，不批准 staging、commit、push、PR、删除、归档、candidate 转 stable、长期记忆写入或新增 skill / harness / plugin。
- 主线任务：复核 skill / harness / plugin candidate 是否仍然必要，防止工具层膨胀影响长期稳定。
- 原则：长期稳定可靠优先；如无必要，不增 skill / harness；架构是核心资产，工具必须服从架构。

## 1. 总体结论

当前主功能可用，candidate plugin、skill 和 harness 没有发现紧急缺文件问题。真正的剩余风险不是“缺能力”，而是“候选能力过多、层级过厚、部分边界还需要继续瘦身”。

本轮建议：

1. 6 个 plugin suite 全部继续保持 `candidate`，不转 stable。
2. 4 个按需 harness checker 继续保持按需触发，不进入所有项目默认必过。
3. 暂不新增 skill、harness、workflow stage 或 plugin。
4. 已按用户批准完成两项最小收口：`memory-learning-extractor` 从 draft 改为 candidate；delivery suite 高风险 skill wording 改为轻量 / 完整模式分层。
5. 下一步不要继续加工具，先观察真实输出是否仍过重。

## 2. 当前候选能力总表

| 区域 | 数量 | 当前状态 | 判断 |
|---|---:|---|---|
| Candidate plugin suite | 6 | marketplace 可见，registry 标记 candidate / detachable / stable_use_allowed=false | 边界正确，暂不转 stable。 |
| Plugin 内注册 skill | 32 | 路径均存在 | 保留 candidate；后续按项目使用证据瘦身。 |
| 无 plugin 路径的核心概念 skill | 8 | workflow 有引用，registry 中无代码路径 | 需要单独收口，不建议马上补插件。 |
| Harness checker | 16 个 `*_checker.py` | run_harness 可运行，check-only 通过 | stable 与 candidate 混在同一 runner 中，但按需 checker 未请求时 pass。 |
| Router 后期能力入口 | 2 个主要后期入口：`closeout`、`ui-style` | 已显式命令触发 | 不影响 PRD 主链路。 |

## 3. Plugin 复核

| Plugin | Owned skills | Workflow action refs | 当前判断 | 推荐动作 |
|---|---:|---:|---|---|
| `prd-analysis-suite` | 6 | 9 | PRD 前置分析有价值，但容易让 0-1 PRD 变重。 | `keep_candidate`，只在需要深度分析时启用。 |
| `prd-prototype-suite` | 4 | 4 | 服务 PRD 原型图、页面说明和后期 HTML 原型。 | `keep_candidate`，PNG / HTML 仍需用户确认。 |
| `preference-memory-suite` | 1 | 1 | 保护项目偏好缓存边界。 | `keep_candidate`，不跨项目、不写长期记忆。 |
| `quality-evaluation-suite` | 1 | 1 | 防止 skill 泛化污染。 | `keep_candidate`，目前价值明确。 |
| `delivery-planning-suite` | 11 | 10 | 半自动开发、Codex 开发文档和交付规划价值高，但最容易过重。 | `needs_slimming`，先收敛输出边界。 |
| `ai-solution-planning-suite` | 9 | 0 | 有完整 AI 方案能力，但主 workflow 尚未注册 action。 | `keep_detachable_candidate`，不要并入主 PRD workflow。 |

### 关键判断

`ai-solution-planning-suite` 当前 `workflow/actions.yaml` 没有 action 引用。这不一定是错误，因为此前已经决定 AI solution 先作为 detachable workflow，不并入主 PRD workflow。但它必须继续标明：

- 非 AI 项目不触发。
- 未经用户确认不输出 AI 模型选型。
- 后续若要启用，应先做 detachable workflow 方案，不直接塞进主 PRD workflow。

## 4. 无 Plugin 路径 Skill 风险

当前有 8 个 registry skill 没有 `plugin` 和 `path`，但被 workflow action 引用：

| Skill | 状态 | Workflow refs | 判断 | 推荐动作 |
|---|---|---:|---|---|
| `pdf-prd-style-learner` | candidate | 1 | 可作为历史 PRD 风格学习概念，但缺少实现路径。 | `defer_not_stable`，没有多项目证据前不补插件。 |
| `prd-structure-planner` | candidate | 1 | PRD 主链路概念 skill。 | `keep_registry_concept`，暂不新增 plugin。 |
| `prd-draft-writer` | candidate | 1 | PRD 主链路概念 skill。 | `keep_registry_concept`，由 pipeline / prompt 实现承载。 |
| `user-story-ac-generator` | candidate | 1 | PRD 配套输出概念 skill。 | `keep_registry_concept`，暂不新增 plugin。 |
| `risk-edgecase-checker` | candidate | 1 | 风险检查概念 skill。 | `keep_registry_concept`，暂不新增 plugin。 |
| `tracking-plan-designer` | candidate | 2 | 成功指标 / 埋点规划概念 skill。 | `keep_registry_concept`，后续可拆成功指标和埋点边界。 |
| `prd-quality-reviewer` | candidate | 2 | PRD 质量和预开发问题概念 skill。 | `keep_registry_concept`，后续可拆质量报告和预开发问题边界。 |
| `memory-learning-extractor` | candidate | 1 | 已从 draft 收口为 candidate，只能写 `memory_proposal`，不能直接写长期记忆或 skill update。 | `done_keep_candidate`，后续观察真实学习提案质量。 |

### 我的判断

这些无路径 skill 不应马上补插件。更稳的做法是：

- PRD 主链路概念 skill 继续由现有 pipeline / prompt / schema 承载。
- 只有真实项目证明需要独立可复用能力时，再考虑插件化。
- `memory-learning-extractor` 已完成最小收口；后续不新增插件，先用现有 workflow 概念能力承载学习提案。

## 5. Harness 复核

| Checker | 当前触发 | 判断 | 推荐动作 |
|---|---|---|---|
| `workflow_gate_checker.py` | 默认 | stable 核心检查。 | `keep_stable`。 |
| `plugin_boundary_checker.py` | 默认 | 防 candidate plugin 越界。 | `keep_stable`。 |
| `steward_contract_checker.py` | 默认 | 保护 steward / skill / action 合同。 | `keep_stable`。 |
| `prototype_preview_gate_checker.py` | 默认 | 防完整原型越权。 | `keep_stable`。 |
| `eval_suite_checker.py` | 默认 | 防规则退化。 | `keep_stable`。 |
| `real_output_eval_checker.py` | 默认 | 防真实输出退化。 | `keep_stable`。 |
| `skill_generalization_checker.py` | 默认 | 防项目偏好污染 skill。 | `keep_stable`。 |
| `external_redaction_checker.py` | 外部包参数触发 | B 包 / 外部保护需要。 | `keep_conditional`。 |
| `delivery_plan_checker.py` | 交付规划请求或已有产物触发 | 按需有价值。 | `keep_candidate`。 |
| `ai_solution_checker.py` | AI 方案请求或已有产物触发 | 按需有价值，非 AI 项目不触发。 | `keep_candidate`。 |
| `agentic_delivery_checker.py` | Codex 半自动开发请求或已有产物触发 | 已瘦身，但仍是高维护候选。 | `keep_candidate_watch`。 |
| `preference_cache_checker.py` | 存在 `memory-cache/projects/*` 时触发 | 有价值，但必须跟偏好缓存策略同步。 | `keep_candidate`。 |

### Harness 结论

当前不建议继续改 harness。原因：

- `run_harness.py --check-only` 已通过。
- 按需 checker 未请求时不会污染普通项目。
- 再加检查会增加维护成本。
- 真正更需要处理的是 skill / workflow / registry 的候选状态边界。

## 6. 输出过重风险

### 6.1 Delivery planning suite

风险最高的仍是 delivery / agentic delivery 这一组。它有价值，但容易把普通 Codex 开发文档扩成完整治理系统。

当前已有改善：

- `agentic-delivery-orchestrator` 已区分 lightweight Codex delivery 和 full agentic delivery。
- output contract 已禁止普通 lightweight 请求默认生成完整 phase 1 / 2 / 3 / final 和完整 Skill/MCP/Harness operating-system exposition。

剩余建议：

- 暂不再改 harness。
- 已完成 `codex-task-package-writer`、`capability-enablement-planner`、`development-governance-orchestrator` 小范围 wording 瘦身。
- 后续只在真实 Codex 开发文档仍过重时继续收敛模板或 output contract。

### 6.2 AI solution suite

AI solution suite 当前是完整候选能力，但 workflow action refs 为 0。

这符合“AI solution 先 detachable，不并入主 PRD workflow”的方向。后续不要为了让 action_refs 非 0 而硬接入主流程。

建议：

- 非 AI 项目继续不触发。
- AI-heavy 项目需要时，先走 detachable workflow proposal。
- 模型选型必须按项目判断，并基于当前官方信息；这类高时效内容后续需要联网确认。

### 6.3 Prototype / UI

PRD prototype suite 和 UI style selector 属于后期原型 / UI / UX 链路。

建议：

- PRD 默认有页面说明、页面跳转关系、原型图层。
- PNG / HTML / 高保真 UI 仍在用户确认后进入。
- UI 风格库只做候选建议，不写长期默认风格。

## 7. 下一步可推动事项

今晚可以继续推动的只限 L1 低风险事项：

| 事项 | 是否可今晚继续 | 原因 | 推荐 |
|---|---|---|---|
| 更新线程台账 | 可以 | 记录 PRUNE-01 已完成只读审查，防上下文丢失。 | 做。 |
| 输出本报告 | 可以 | 只读审查，不改运行能力。 | 做。 |
| 继续跑 regression / harness | 可以 | 验证主链路不受影响。 | 做。 |
| 生成 `memory-learning-extractor` 处置方案 | 已完成最小收口 | draft 被 workflow 引用的问题已消除。 | 后续只观察。 |
| 抽查 delivery suite wording | 已完成小范围 wording 收敛 | 防“默认全量治理”。 | 后续只观察真实输出。 |
| 修改 skill / harness / registry | 不建议今晚做 | 会改变长期能力边界，需你早上拍板。 | 不做。 |
| 删除 raw / proposal / archive notes | 不允许 | 需要到期后二次批准。 | 不做。 |
| 提交项目产物 | 不允许 | 会污染稳定核心。 | 不做。 |

## 8. 需要你早上拍板

| 拍板项 | 我的建议 | 不同选择的效果 |
|---|---|---|
| `memory-learning-extractor` 后续是否插件化 | 暂不插件化 | 现有 pipeline / workflow 概念能力足够；插件化会增加维护成本。 |
| `ai-solution-planning-suite` 是否接入 workflow action | 暂不接入主 workflow，保持 detachable candidate | 非 AI 项目不被污染；需要 AI 方案时再走单独方案。 |
| delivery suite 是否继续瘦身 wording | 暂停继续改，先看真实输出 | 当前已做轻量 / 完整模式分层；继续改可能过早优化。 |
| 4 个按需 checker 是否 stable | 不 stable，继续 candidate / conditional | 保留保护能力，同时控制维护成本。 |
| 是否新增 pruning harness | 不新增 | 当前报告 + 现有 regression 足够；新增 harness 会违背最小化原则。 |
| 是否提交本报告 | 早上你验收后再决定 | 现在不 staging、不 commit，避免提前固化分类。 |

## 9. 建议执行顺序

1. 本轮只保留本报告和台账更新。
2. 早上你验收本报告。
3. 后续先跑真实 Codex 开发文档输出复核，判断是否仍过重。
4. 最后输出本轮治理总验收报告。

## 10. 本轮不做

- 不新增 skill。
- 不新增 harness。
- 不新增 plugin。
- 不把 candidate 转 stable。
- 不删除文件。
- 不归档项目。
- 不提交项目产物。
- 不提交 `memory-cache/`。
- 不提交 `ai-intel/raw/`。
- 不 staging / commit / push / PR。
