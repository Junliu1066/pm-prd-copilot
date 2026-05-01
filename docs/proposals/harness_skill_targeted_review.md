# Harness / Skill 专项边界审查

- 日期：2026-05-01
- 状态：专项审查报告，不批准 staging、commit、push、PR、删除、归档、candidate 转 stable 或新增 harness / skill。
- 主线任务：确认 harness 和 skill 是否存在缺文件、默认污染、过重输出、候选能力误用为 stable 的风险。
- 原则：长期稳定可靠优先；如无必要，不增 harness，不增 skill。

## 审查范围

本轮只审查治理边界，不改代码：

- `harness/run_harness.py`
- `harness/*_checker.py`
- `registry/plugins.yaml`
- `registry/skills.yaml`
- `.agents/plugins/marketplace.json`
- `plugins/*/skills/*/SKILL.md`
- 重点抽查：`plugins/delivery-planning-suite/skills/agentic-delivery-orchestrator/SKILL.md`

## 当前结论

### 1. Harness 当前没有紧急缺文件问题

`run_harness.py` 引用的 checker 当前都已存在且已进入 git 跟踪。最近一次检查结果：

- regression：通过
- harness check-only：通过
- harness 模式：`check-only`
- 项目文件写入：无

因此当前不需要新增 harness，也不需要立刻修改 `run_harness.py`。

### 2. 按需 checker 边界目前基本正确

| Checker | 当前状态 | 判断 |
|---|---|---|
| `delivery_plan_checker.py` | 已跟踪，按需触发 | 未请求交付规划时 pass，不污染普通 PRD。 |
| `ai_solution_checker.py` | 已跟踪，按需触发 | 未请求 AI 方案且无 `ai/` 产物时 pass，不强迫非 AI 项目写 AI 模型选型。 |
| `agentic_delivery_checker.py` | 已跟踪，按需触发 | 已瘦身到底线检查，但仍需配套 skill 输出边界收敛。 |
| `preference_cache_checker.py` | 已跟踪，按缓存存在触发 | 能保护项目偏好隔离、清除状态和长期记忆审批边界。 |

### 3. Candidate plugin / skill 没有被标成 stable

`registry/plugins.yaml` 和 `.agents/plugins/marketplace.json` 当前都把 6 个 plugin suite 标为：

- `status: candidate`
- `detachable: true`
- `stable_use_allowed: false`
- `requires_user_review_before_stable_use: true`
- `review_label: candidate / requires review / non-stable capability`

这符合当前治理要求：candidate 可见，但不能自动当 stable 使用。

### 4. 主要剩余风险在 Skill 输出过重

当前最需要针对性处理的是：

`plugins/delivery-planning-suite/skills/agentic-delivery-orchestrator/SKILL.md`

风险点：

- 它要求 always include 多份 Codex 开发计划、阶段计划、治理报告和任务包。
- 对真正进入“半自动开发交付”的项目有价值。
- 但如果被普通开发文档或轻量交付误触发，容易把 Skill / MCP / Harness / 多阶段治理内容塞得过重。

这不是当前 harness 的缺陷，而是 skill 输出合同需要更清楚地分层：

- 普通 Codex 开发文档：只要任务包、边界、验证、人工确认、回滚。
- 半自动开发交付：才需要 agentic delivery plan、phase 1 / 2 / 3 / final、治理报告等完整套件。
- 项目或用户明确要求后，才能展开完整治理链路。

## 需要你拍板的治理功能决策

| 决策 | 选项 A | 选项 B | 选项 C | 我的建议 |
|---|---|---|---|---|
| Harness 是否现在继续改代码 | 不改，保持现状 | 继续加检查 | 删除候选 checker | 选 A。当前 harness 已通过且按需触发，继续加会增加维护成本。 |
| 4 个按需 checker 是否转 stable | 保持 candidate / conditional | 转 stable | 删除 | 选 A。它们有价值，但不应成为所有项目默认必过项。 |
| Skill 是否先处理 agentic delivery | 先瘦身 agentic delivery 输出边界 | 先处理所有 skill | 暂不处理 skill | 选 A。问题最集中，改动最小，最利于长期稳定。 |
| Agentic delivery skill 如何瘦身 | 加触发条件和轻/重输出分层 | 保留 always include | 删除该 skill | 选 A。保留能力，但避免普通开发文档被过度治理化。 |
| AI solution skill 是否现在改 | 暂不改，保持按 AI 项目触发 | 立即全面瘦身 | 转 stable | 选 A。当前 AI checker 已防止非 AI 项目污染，先不扩大范围。 |
| Prototype / HTML skill 是否现在改 | 暂不改，保持确认后使用 | 默认进入 PRD | 删除 | 选 A。它属于后期原型 / UI 链路，不影响主 PRD。 |

## 建议下一步

下一步做一个小批次：**agentic delivery skill 输出边界瘦身**。

建议只改：

- `plugins/delivery-planning-suite/skills/agentic-delivery-orchestrator/SKILL.md`
- 必要时同步改：
  - `plugins/delivery-planning-suite/skills/agentic-delivery-orchestrator/references/output-contract.md`

目标：

1. 明确该 skill 只在用户要求 Codex 半自动开发、阶段交付、任务包拆分或开发治理时启用。
2. 把输出分成两层：
   - lightweight：Codex 开发文档、任务包、人工确认、验证、回滚。
   - full agentic delivery：phase 1 / 2 / 3 / final、治理报告、完整能力启用与路由。
3. 删除或收敛 `Always include` 的绝对口径，改成按请求和项目风险分层输出。
4. 保留安全底线：允许/禁止修改范围、验证命令、人工确认点、回滚策略必须存在。

## 本轮不执行

- 不新增 harness。
- 不新增 skill。
- 不删除 checker。
- 不把 candidate 转 stable。
- 不改项目文件。
- 不提交 `memory-cache/`。
- 不写长期记忆。
- 不 push / PR。
