# Harness 候选最小必要性审查报告

- 日期：2026-04-30
- 状态：审查报告，不批准 staging / commit / stable 化
- 范围：4 个按需候选 harness checker
- 原则：如无必要，不增 harness；长期稳定可靠优先。

## 结论

这 4 个 checker 有治理价值，但不应直接进入 stable core，也不应变成所有项目默认必过的主链路检查。

推荐结论：

| Checker | 建议 | 原因 |
|---|---|---|
| `delivery_plan_checker.py` | 保持按需候选 | 只在项目进入交付规划阶段时有价值；普通 PRD 不应强制交付规划。 |
| `ai_solution_checker.py` | 保持按需候选 | 只适合 AI 项目或明确进入 AI 方案阶段；非 AI 项目不应被 AI 检查污染。 |
| `agentic_delivery_checker.py` | 保持按需候选，暂不 stable | 检查面很大，和 Codex 开发文档强相关；价值高但维护成本也高。 |
| `preference_cache_checker.py` | 保持按需候选 | 只在存在项目偏好缓存时有价值；必须继续受长期记忆审批边界约束。 |

当前不要删除它们，也不要把它们并入 stable core。更稳的做法是：保留为 `candidate / conditional`，后续通过真实项目复核判断是否合并、瘦身或归档。

## 调用状态

这 4 个 checker 已被 `harness/run_harness.py` 调用，但当前行为是“无相关请求或产物时 pass”，不是强制所有项目提供产物。

| Checker | 当前触发条件 | 默认项目影响 |
|---|---|---|
| `delivery_plan` | `requires_delivery_plan`、`delivery_planning`、manifest required outputs / enabled skills、或已有 `delivery/` 文件 | 未请求时不增加项目负担。 |
| `ai_solution` | `requires_ai_solution_plan`、`ai_solution_planning`、AI required outputs / enabled skills、或已有 `ai/` 文件 | 非 AI 项目不会被强制输出 AI 模型选型。 |
| `agentic_delivery` | `requires_agentic_delivery`、`agentic_delivery_planning`、相关 delivery required outputs / enabled skills、或已有 agentic delivery 文件 | 只在 Codex 开发文档/半自动交付阶段触发。 |
| `preference_cache` | `memory-cache/projects/*` 存在 | 没有项目偏好缓存时直接 pass。 |

## 重复性判断

| Checker | 是否和 stable 检查重复 | 判断 |
|---|---|---|
| `delivery_plan` | 部分重叠 | workflow/artifact 合同能检查登记一致性，但不能检查交付计划内容质量。 |
| `ai_solution` | 部分重叠 | PRD regression 能防止非 AI 项目乱写 AI 选型，但不能检查 AI 项目方案完整性。 |
| `agentic_delivery` | 有膨胀风险 | 与开发文档、交付规划、能力启用、人工监督有交叉；需要后续瘦身。 |
| `preference_cache` | 不重复 | 它检查项目内隔离、清除状态、长期记忆审批边界，是偏好缓存专属风险。 |

## 维护成本

| Checker | 成本来源 | 风险 |
|---|---|---|
| `delivery_plan` | 需要维护交付计划关键词和产物清单 | 关键词过窄会误报，过宽会漏报。 |
| `ai_solution` | AI 方案产物多，模型、RAG、记忆、画像、教练、架构都在范围内 | 最容易随 AI 架构变化而过时。 |
| `agentic_delivery` | 检查项最多，覆盖多份 Codex 开发文档和阶段计划 | 当前最可能过重，后续应优先瘦身。 |
| `preference_cache` | 依赖 `memory-cache` 结构和归档处置规则 | 一旦偏好缓存策略变化，需要同步更新。 |

维护成本不是“写代码多一点”的问题，而是后续每次 PRD 规则、开发文档规则、AI 架构、偏好缓存策略变化时，这些 checker 都可能要一起维护。长期稳定优先，所以它们只能先保持候选。

## 逐项建议

### 1. `delivery_plan_checker.py`

建议：保留为按需候选，不进入 stable core。

理由：

- 它能防止交付规划缺少团队假设、阶段计划、工期、用户可见效果、业务验证、待决策项。
- 但不是每个项目都进入交付规划阶段。
- 当前触发条件较清楚，未请求时不会阻塞普通 PRD。

后续优化：

- 如果多个真实项目都使用交付规划，再考虑把关键词规则改成结构化 schema。
- 暂不新增检查项。

### 2. `ai_solution_checker.py`

建议：保留为按需候选，不进入 stable core。

理由：

- 它保护 AI 项目的模型选型、Prompt、RAG、记忆、画像、教练、AI 架构边界。
- 这符合“AI 模型选型按项目判断”的规则。
- 非 AI 项目不应被它强制要求 AI 产物。

后续优化：

- 先用 1-2 个 AI 项目验证是否误报。
- 如果检查项过多，优先拆成“必要底线”和“增强建议”，不要新增 harness。

### 3. `agentic_delivery_checker.py`

建议：保留为按需候选，但列为优先瘦身对象。

理由：

- 它覆盖 Codex 开发文档、任务包、人工监督、能力启用、Skill/MCP 路由、阶段计划、回滚和审查。
- 这正好对应用户确认的“开发文档默认是 Codex 开发文档”。
- 但当前检查面最大，最容易变成高维护成本组件。

后续优化：

- 先不要 stable。
- 后续真实项目中只保留最能防事故的底线检查：允许修改范围、禁止修改范围、验证命令、人工确认点、回滚方案。
- 其他细项优先放到模板和审查清单，不放进强 harness。

### 4. `preference_cache_checker.py`

建议：保留为按需候选，不进入 stable core。

理由：

- 它防止项目偏好跨项目复用、防止清除后的缓存继续被读、防止长期记忆绕过审批。
- 这是用户明确重视的治理边界。
- 没有 `memory-cache/projects/*` 时直接 pass，不影响普通项目。

后续优化：

- 和偏好缓存审查一起处理。
- 暂不自动清除、不自动归档、不自动写长期记忆。

## 需要你后续拍板

| 决策 | 我的建议 | 不同选择的结果 |
|---|---|---|
| 4 个 checker 是否直接 stable | 不 stable | 直接 stable 会增加长期维护压力；保持候选更符合“如无必要，不增 harness”。 |
| 是否删除 4 个 checker | 不删除 | 现在删除会失去已建好的边界检查；等真实项目验证后再判断是否归档。 |
| 是否提交这 4 个 checker | 暂不提交 | 先看本报告；后续若提交，应作为“按需候选 checker”单独批次，不混入 stable core。 |
| 是否优先瘦身 `agentic_delivery_checker.py` | 是 | 它检查面最大，最容易变成长期负担。 |
| 是否把偏好缓存检查改成 stable | 暂不 | 等 `memory-cache` 策略审核完，再决定。 |

## 下一步建议

1. 本报告先给你审核，不 staging、不 commit。
2. 下一步优先做 `agentic_delivery_checker.py` 瘦身方案，只提方案，不马上改。
3. 同步做偏好缓存边界审查，避免 checker 和缓存策略不一致。
4. 真实项目跑过 2-3 次后，再决定哪些 checker 可以稳定、合并或归档。

## 本轮未执行

- 未新增 harness。
- 未删除 harness。
- 未把候选 checker 转 stable。
- 未 staging / commit。
- 未改 `run_harness.py`。
- 未写项目文件。
- 未写长期记忆。
