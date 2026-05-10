# GPT-5.4 -> GPT-5.5 存量 Skill / Harness 适配复核报告

- 复核日期：2026-05-05
- 复核等级：L2 能力更新
- 复核范围：GPT-5.4 阶段编写或明显按 GPT-5.4 行为调优的 skill、harness、prompt 约束、eval / regression、模型配置和输出规则。
- 本轮动作：只输出复核报告和最小补丁建议；不改 stable，不删除旧约束，不新增 skill / harness，不提交。

## 0. 总结结论

这次升级应按 L2 处理：GPT-5.5 相比 GPT-5.4 是能力更新，不是当前证据下的 L3 破坏性更新。

本仓库主链路仍能运行，但有 5 类存量规则需要适配：

| 等级 | 结论 | 对象 | 问题 | 建议动作 |
|---|---|---|---|---|
| P1 | 已拍板 / 观察 | `pm-prd-copilot/config/model_config.yaml` | 默认模型已按用户批准从 `gpt-5.4` 切到 `gpt-5.5` | 保留 env 覆盖和 actual model 记录，观察 proxy 与成本表现 |
| P1 | 放松 / 改写候选 | `harness/agentic_delivery_checker.py` | 轻量 Codex 交付和完整 agentic delivery 被同一套硬门禁检查 | 拆成 lightweight / full 两档，不新增 harness |
| P1 | 改写候选 | `harness/prototype_preview_gate_checker.py` | 固定要求 `P1/P6/P7/P12/P16/P18` 页面编号，带历史项目痕迹 | 改为读取项目页面清单 / prototype manifest |
| P2 | 放松 / 合并 | 多个 keyword harness 和 skill 输出合同 | 旧规则偏过程重、关键词重，可能限制 GPT-5.5 更自然的高质量输出 | 安全项继续 hard fail，表达项降为 advisory 或结构化检查 |
| P2 | 改写候选 | `harness/real_output_eval_checker.py` 与 eval 报告 | 缺模型版本、生成时间、样例适配状态 | 增加模型版本意识，不扩大 eval 数量 |

当前不建议全仓库重构。最小有效路径是：先修 P1 的三项，再根据真实输出决定 P2 是否跟进。

## 1. 模型能力差异卡

官方资料来源：

- OpenAI 模型文档：`https://developers.openai.com/api/docs/models`
- OpenAI Prompt guidance：`https://developers.openai.com/api/docs/guides/prompt-guidance`

| 维度 | GPT-5.4 | GPT-5.5 | 对本架构的影响 |
|---|---|---|---|
| 官方定位 | 更经济的 coding / professional work 模型 | 复杂推理与 coding 的旗舰模型 | 默认模型配置需要复核，避免 pipeline 停留在旧默认 |
| 推理强度 | 支持 `none / low / medium / high / xhigh` | 同样支持 `none / low / medium / high / xhigh` | 不应默认把所有任务升到高推理；应重新评估 low / medium 是否足够 |
| 上下文 | 1M context | 1M context | 长上下文能力不是新增风险点，但旧 prompt 的重复规则会更浪费 token |
| 最大输出 | 128K tokens | 128K tokens | 输出容量足够，不代表 PRD / 开发文档可以无边界膨胀 |
| 工具 | Functions、Web search、File search、Computer use | Functions、Web search、File search、Computer use | 工具能力口径兼容；重点复核 tool-heavy prompt 是否过度规定流程 |
| prompt 迁移重点 | 更依赖明确输出合同、工具期望和完成标准 | 更适合短、结果优先、少堆过程的 prompt | 旧的过程型 prompt stack 需要瘦身，否则会限制 5.5 |
| 成本 | 官方价格低于 5.5 | 官方价格更高 | 默认切换模型涉及成本，需要人工拍板 |
| 知识截止 | Aug 31, 2025 | Dec 1, 2025 | AI 情报和模型选择规则不应继续假设 5.4 知识边界 |

判断：本次没有发现本仓库 API 层立即破坏的证据，所以不是 L3；但 prompt、harness、eval 的行为假设已经需要复核，所以是 L2。

## 2. 受影响 Skill / Harness 清单

| 对象 | 受影响原因 | 判断 | 建议 |
|---|---|---|---|
| `pm-prd-copilot/config/model_config.yaml` | 默认 `model: gpt-5.5`，`reasoning_effort: low`，本地 proxy 口径需要继续观察 | 观察 | 已保留 env 覆盖和 actual model 记录，不同步上调推理强度 |
| `pm-prd-copilot/scripts/model_client.py` | 会透传 `reasoning_effort` 和 `temperature`，需要确认 5.5 / 本地 proxy 接受范围 | 观察 | 只有出现 API 兼容错误时再改 |
| `pm-prd-copilot/SKILL.md` | Codex 开发文档存在完整治理层倾向 | 放松候选 | 与“轻量任务降级，多模块才启用多分支机制”对齐 |
| `pm-prd-copilot/references/output_style_guide.md` | 有 `Always include operating-system layer` 倾向 | 放松候选 | 把默认完整治理改为条件启用 |
| `plugins/delivery-planning-suite/skills/agentic-delivery-orchestrator/` | 已区分 lightweight / full，但 harness 未完全承接 | 保留 | 不改 skill，先修 checker |
| `plugins/delivery-planning-suite/skills/codex-task-package-writer/` | 已具备分支启动包与多分支条件输出 | 保留 | 继续作为执行任务包标准 |
| `harness/agentic_delivery_checker.py` | 对轻量和完整交付使用同一套硬 fail | 改写候选 | 拆模式，保留底线检查 |
| `harness/prototype_preview_gate_checker.py` | 固定页面编号是历史项目规则 | 改写候选 | 改为 manifest / 页面清单驱动 |
| `harness/ai_solution_checker.py` | 触发后默认完整九件套，轻量 AI 功能偏重 | 放松候选 | 后续加 compact / full 模式 |
| `harness/delivery_plan_checker.py` | 关键词和阶段字段偏固定 | 观察 / 放松候选 | 先保留，真实误报后再修 |
| `harness/real_output_eval_checker.py` | 不判断模型版本和样例新鲜度 | 改写候选 | 加元信息和 stale 提醒 |
| `pm-prd-copilot/evals/*` | 回归样例未标注模型版本、模板版本 | 改写候选 | 不扩样例，先补元信息 |
| 候选 plugin suite | 多数 `Always include` 是输出合同，不一定是旧模型约束 | 保留 / 观察 | 不批量改，防止误伤 artifact 合同 |

## 3. Skill / Harness 适配矩阵

| 优先级 | 对象 | 当前问题 | 最小补丁 | 预期效果 | 结论 |
|---|---|---|---|---|---|
| P0 | 无 | 未发现立即跑不动的破坏性问题 | 无 | 不升级为 L3 | 保留 |
| P1 | 模型默认配置 | 默认仍是 5.4，可能导致实际 pipeline 与当前主模型不一致 | 增加显式当前模型配置方案：默认值、环境覆盖、实际模型记录 | 模型口径可追踪，避免暗中跑旧模型 | 需要人工拍板 |
| P1 | agentic checker | 轻量开发文档被完整治理门禁误杀 | 拆 lightweight / full 模式 | 降低过度治理，保留半自动开发安全底线 | 改写候选 |
| P1 | prototype preview gate | 固定页面 ID 污染所有项目 | 改为读取 manifest / 页面清单；无 manifest 时只查最低结构 | 原型链路更通用 | 改写候选 |
| P2 | PM Skill / style guide | 过程层规则可能过重 | 把 `Always include` 收敛成条件启用 | 让 GPT-5.5 发挥更强规划能力，不被旧 prompt stack 束缚 | 放松 |
| P2 | AI solution checker | 小 AI 功能也被完整 AI 架构压住 | 增加 compact / full | 减少 AI 小功能过度治理 | 放松 |
| P2 | real output eval | 旧报告缺模型版本 | 加 `model_id`、`prompt_template_version`、`generated_at`、`stale_after_model_update` | 模型更新后知道该不该重跑 | 改写候选 |
| P3 | delivery plan checker | 关键词和阶段判断可能偏保守 | 观察真实误报 | 避免过度修复 | 观察 |

## 4. 快速回归样例建议与本轮结果

### 4.1 本轮已跑基础验证

本轮只验证主链路没有被审查材料影响：

```bash
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

### 4.2 建议作为 GPT-5.5 L2 快速回归的小样本

这些样例用于后续补丁前后对比，不建议扩大成完整大回归：

| 样例 | 目的 | 预期 |
|---|---|---|
| 非 AI 0-1 PRD | 验证非 AI 项目不输出 AI 模型选型 | 不出现默认 AI 选型；保留页面说明、跳转关系、原型图层 |
| 内部 Codex 开发文档 | 验证轻量 / 多分支条件启用 | 小任务不展开完整治理，多模块任务输出分支矩阵和分支启动包 |
| 完整原型请求 | 验证 prototype gate 去硬编码 | 页面编号按项目生成，不要求固定 `P1/P6/P7/P12/P16/P18` |
| 小型 AI 功能 PRD | 验证 AI solution compact | 有模型边界、fallback、评测，不强制 RAG / memory / learner profile |
| B 包脱敏 | 验证外部包不泄露内部治理 | 不暴露 steward / harness / 内部规则 |
| 长上下文项目整理 | 验证旧 prompt 是否限制 5.5 | 输出更结果导向，不堆重复过程 |
| 工具调用任务 | 验证 harness check-only 与工具链 | 不写项目文件，报告路径清楚 |

## 5. 旧规则是否限制 GPT-5.5 能力

| 旧规则类型 | 是否限制 | 证据 | 处理 |
|---|---|---|---|
| 过程型 prompt stack | 是 | 官方 prompt guidance 提醒 5.5 更适合结果优先，旧 prompt 过度规定过程会增加噪音 | 放松 |
| `Always include operating-system layer` | 部分限制 | 普通小任务会被拉成完整治理文档 | 改成条件启用 |
| 关键词式 hard fail | 部分限制 | 更自然表达可能未命中特定词 | 安全项保留，表达项 advisory |
| 固定页面 ID | 明确限制 | `P1/P6/P7/P12/P16/P18` 明显不是通用页面合同 | 改写 |
| 完整 AI 九件套 | 部分限制 | 小型 AI 能力不一定需要 RAG / memory / learner profile | 增加 compact |
| 旧模型默认配置 | 明确限制风险 | 默认值仍是 5.4 | 需要人工拍板 |
| 长上下文重复约束 | 潜在限制 | 5.5 上旧规则重复会浪费 token | 观察并瘦身 |

## 6. 最小补丁建议

建议顺序固定为小批次：

1. `agentic_delivery_checker.py` 模式拆分。
   - lightweight：任务包、允许 / 禁止范围、验证命令、人工确认、回滚、review。
   - full：才检查完整 governance report、分支矩阵、multi-manager、harness / gate。
   - 影响：立刻减少轻量 Codex 开发文档误杀。

2. `prototype_preview_gate_checker.py` 去固定页面 ID。
   - 优先读取 `prototype_manifest.json` / 页面清单。
   - 无 manifest 时只查最低结构，不要求固定编号。
   - 影响：去掉历史项目污染。

3. 模型配置兼容方案。
   - 已按用户批准把默认模型切到 `gpt-5.5`。
   - 已保留“实际调用模型记录 + env 覆盖说明 + 本地 proxy 兼容说明”。
   - 影响：避免 pipeline 和自动化模型口径漂移，同时保留回滚口。

4. `SKILL.md` / `output_style_guide.md` 轻量条件措辞收敛。
   - 把完整治理层从默认 always 改成多模块 / 半自动 / 用户要求时启用。
   - 影响：减少 GPT-5.5 被旧过程约束拖慢。

5. real-output eval 元信息。
   - 补 `model_id`、`template_version`、`generated_at`、`model_update_staleness`。
   - 影响：模型更新后知道哪些样例需要重跑。

6. AI solution compact / full。
   - 等前 5 项后再做。
   - 影响：AI 小功能不再被完整 AI 架构压垮。

## 7. 必须人工拍板事项

| 决策 | 选项 | 我的建议 | 不同结果 |
|---|---|---|---|
| 默认模型是否从 5.4 改到 5.5 | 已拍板：改为 5.5，保留 env 回滚 | 已执行 | pipeline 默认进入 GPT-5.5 口径，但仍需观察成本和 proxy 支持 |
| 是否修 agentic checker 模式冲突 | A 修；B 暂缓 | A | A 降低误杀；B 轻量文档仍可能被完整治理压住 |
| 是否去掉 prototype 固定页面 ID | A 修；B 暂缓 | A | A 清除历史项目污染；B 原型检查继续不通用 |
| 是否放松 PM Skill / style guide 的完整治理默认 | A 修；B 观察 | A，小范围措辞 | A 更适配 5.5；B 可能继续输出过重 |
| 是否给 eval 加模型版本元信息 | A 修；B 等下一次真实模型更新 | A，小补丁 | A 更可追踪；B 继续依赖人工记忆 |
| 是否删除旧约束 | A 删除；B 不删，只分 hard fail / advisory | B | A 风险高；B 稳定可回退 |
| 是否新增 skill / harness | A 新增；B 不新增 | B | A 膨胀；B 符合最小治理 |

## 8. 本轮不做

- 不做全仓库大改。
- 不直接修改 stable。
- 不自动删除旧约束。
- 不新增 skill / harness。
- 不自动提交。
- 不把候选能力转 stable。
- 不把模型更新复核扩成每日治理体检。

## 9. P1 最小补丁执行状态

状态：已完成 / 进入观察验收期。

已处理范围：

1. `harness/agentic_delivery_checker.py`
   - 已拆分 `lightweight` / `full` 检查模式。
   - `lightweight` 只检查任务包、范围、验证命令、回滚、人工确认和 review。
   - `full` 才检查完整 governance report、分支矩阵、多管家、harness / gate。

2. `harness/prototype_preview_gate_checker.py`
   - 已去掉固定页面 ID 要求。
   - 不再硬要求 `P1/P6/P7/P12/P16/P18`。
   - 优先读取 prototype manifest / 页面清单；无 manifest 时只做最低结构检查并输出 advisory。

3. `pm-prd-copilot/config/model_config.yaml` 和 `pm-prd-copilot/scripts/model_client.py`
   - 已按用户批准把默认模型切到 GPT-5.5。
   - 已保留 env 覆盖说明和本地 proxy 兼容说明。
   - 已在 LLM metadata 中记录 `requested_model` 和 `actual_model_id`。

本阶段仍不做：

- 不改 stable。
- 不新增 skill / harness。
- 不删除旧约束。
- 不自动提交。
- 不进入大 P2。

## 10. P1 观察验收期

观察期口径：当前分支线程记录，完成 3 个真实任务后验收；不再以 7 天作为主条件。

观察目标：

| 观察项 | 期望结果 | 异常处理 |
|---|---|---|
| lightweight / full agentic checker | 轻量任务不再被完整治理报告误杀；完整任务仍保留治理门禁 | 若轻量漏掉安全底线，回补 hard fail；若完整误杀，改为结构化字段检查 |
| prototype preview gate | 原型检查不再被固定页面 ID 污染 | 若项目没有 manifest 导致判断过松，补 manifest 要求或页面清单字段 |
| `requested_model` / `actual_model_id` | 能看清请求模型和实际返回模型是否一致 | 若本地 proxy 不返回模型 ID，保留 requested model 并报告 actual unknown |
| regression | 持续通过 | 失败时只定位 P1 影响范围，不扩大到全仓库重构 |
| harness check-only | 持续通过且不写项目文件 | 若出现误报，先调整现有 checker，不新增 harness |
| 新误报 / 漏报 / 安全边界不足 | 记录为观察项，不自动改 stable | 按最小补丁原则提交下一轮方案 |

观察期原则：

- 观察期不等于 stable 转正。
- 只记录真实输出中的误报、漏报、安全边界不足。
- 没有真实问题时，不继续扩展机制。
- 若观察稳定，下一步只允许进入 P2 最小两项。

### 10.1 当前分支线程观察台账

| 序号 | 真实任务 | 类型 | 观察状态 | 重点记录 | 初步结论 |
|---|---|---|---|---|---|
| 1 | 待记录 | PRD / Codex 开发文档 / 原型或 UI | 未开始 | `lightweight/full`、prototype gate、`requested_model/actual_model_id`、regression、harness、误报/漏报 | 待观察 |
| 2 | 待记录 | PRD / Codex 开发文档 / 原型或 UI | 未开始 | `lightweight/full`、prototype gate、`requested_model/actual_model_id`、regression、harness、误报/漏报 | 待观察 |
| 3 | 待记录 | PRD / Codex 开发文档 / 原型或 UI | 未开始 | `lightweight/full`、prototype gate、`requested_model/actual_model_id`、regression、harness、误报/漏报 | 待观察 |

每个真实任务完成后，追加记录：

- 任务名称和类型。
- 是否触发 `lightweight` 或 `full` agentic checker。
- 是否出现轻量误杀、完整漏检或安全边界不足。
- prototype gate 是否仍被页面编号、页面清单或 manifest 问题影响。
- LLM metadata 是否包含 `requested_model` 和 `actual_model_id`。
- regression / harness check-only 结果。
- 是否需要进入 P2，或继续观察。

验收规则：

- 3 个真实任务都未出现 P1 误报 / 漏报 / 安全边界不足，才允许进入 P2 最小两项。
- 任一任务出现 P1 问题，先修 P1，不进入 P2。
- 观察台账只作为当前分支线程记录，不自动转 stable，不自动新增 skill / harness。

## 11. 允许进入的 P2 最小项

只有 P1 观察期稳定后，才允许进入以下两项：

1. 收敛 `pm-prd-copilot/SKILL.md` / `pm-prd-copilot/references/output_style_guide.md` 的 `Always include` 完整治理层措辞。
   - 目标：把完整治理层改成多模块、半自动、用户明确要求时启用。
   - 不改产品主链路，不新增 skill / harness。

2. 给 real-output eval 增加模型版本、生成时间、模板版本、模型更新 stale 标记。
   - 目标：模型更新后知道哪些真实输出样例需要重跑。
   - 不扩大 eval 数量，不升级成全量模型更新体检。

暂缓项：

- `ai_solution_checker.py` 的 compact / full 继续暂缓。
- 只有真实 AI 项目暴露误报或过重问题后，再单独处理。
