# Skill / Token 效率治理报告

- 日期：2026-05-09
- 状态：治理输入报告；不批准 staging、commit、push、PR、删除、candidate 转 stable、新增 skill / harness / plugin 或修改长期规则。
- 主线任务：拉取效率部门数据，定位是否存在 skill、MCP、产物或流程导致的 token 浪费，并给出可治理清单。
- 读者：核心团队。
- 数据来源：`registry/skills.yaml`、`registry/plugins.yaml`、`registry/mcps.yaml`、`governance/efficiency_policy.yaml`、`harness/efficiency_auditor.py`、`projects/**/runs/**/{manifest,trace,efficiency_report}.json`、`projects/**/*.meta.json`、`plugins/*/skills/*/SKILL.md`。

## 1. 总体结论

当前确实存在 token 浪费和效率审计漏报风险。问题不主要来自 MCP，目前 MCP 没有实际调用；主要来自三类：

1. PRD 后续多个生成阶段重复吃同一批上下文，且缓存命中为 0。
2. 效率审计只按 `trace.skill_calls` 计数，漏掉 manifest 中启用但未写入 trace 的 skill，导致 19 个 skill 的 run 被报告为 0 次 skill call。
3. registry 中存在 8 个无 `path` 的概念 skill，部分仍被真实 run 引用，治理上容易出现“可路由但无落地文件 / 无执行合同”的成本黑洞。

建议治理优先级：

| 优先级 | 问题 | 建议动作 |
|---|---|---|
| P0 | 效率审计漏报 skill 数和过期报告 | 先修审计口径，不先改业务 skill。 |
| P0 | `stories` / `risk` / `tracking` 重复输入上下文 | 合并或共享压缩中间上下文，减少重复 input tokens。 |
| P1 | 8 个无路径 concept skill | 明确保留为概念、补落地路径或从可执行路由中移除。 |
| P1 | 大型 planning / prototype skill 文档过长 | 加动态加载和摘要路由，不默认全量注入。 |
| P2 | 项目产物超出效率审计覆盖范围 | 扩展审计范围，覆盖 `ai/`、`delivery/`、`prototype/` 等非固定 5 件套。 |

## 2. 核心数据

### 2.1 Skill 注册与落地

| 指标 | 数量 | 说明 |
|---|---:|---|
| registry skill 总数 | 40 | 全部为 `candidate`。 |
| 有 `path` 的 skill | 32 | 均有对应 `SKILL.md`。 |
| 无 `path` 的 skill | 8 | 属于概念 / pipeline 承载 skill。 |
| 插件目录实际 `SKILL.md` | 32 | 位于 `plugins/*/skills/*/SKILL.md`。 |
| 插件 skill 文档总字符数 | 88,066 | 如全量进入上下文，会形成固定 token 压力。 |
| 注册 MCP | 4 | `github`、`fetch`、`firecrawl`、`apify`。 |
| 已观测 MCP 调用 | 0 | 所有 run 的 manifest / trace 中 MCP 调用为 0。 |

8 个无 `path` 的 skill：

| Skill | 当前状态 | 风险判断 |
|---|---|---|
| `pdf-prd-style-learner` | candidate / no path | 未落地；应保持按需概念，不进入默认执行。 |
| `prd-structure-planner` | candidate / no path | PRD 主链路概念 skill；需要明确由 pipeline 承载。 |
| `prd-draft-writer` | candidate / no path | 已在 demo run 引用；需要补合同或标为 pipeline internal。 |
| `user-story-ac-generator` | candidate / no path | 有 token 元数据对应输出；需要治理重复上下文。 |
| `risk-edgecase-checker` | candidate / no path | 有 token 元数据对应输出；需要治理重复上下文。 |
| `tracking-plan-designer` | candidate / no path | 有 token 元数据对应输出；demo 中出现 attempt=2。 |
| `prd-quality-reviewer` | candidate / no path | 暂无实际 token 元数据；保留候选即可。 |
| `memory-learning-extractor` | candidate / no path | 学习链路概念 skill；不能直接写长期记忆。 |

### 2.2 已观测 token 使用

目前只有部分项目存在 `.meta.json` usage 数据，能直接计算 token 的项目为 `demo-project` 和 `fitness-app-mvp`。

| Project | Input tokens | Output tokens | Reasoning tokens | Total tokens |
|---|---:|---:|---:|---:|
| `demo-project` | 18,215 | 9,425 | 124 | 27,640 |
| `fitness-app-mvp` | 22,068 | 12,396 | 103 | 34,464 |
| 合计 | 40,283 | 21,821 | 227 | 62,104 |

按产物类型聚合：

| 产物 | Input tokens | Output tokens | Reasoning tokens | Total tokens |
|---|---:|---:|---:|---:|
| `04_risk_check.generated` | 9,992 | 5,890 | 79 | 15,882 |
| `02_prd.generated` | 8,631 | 5,835 | 34 | 14,466 |
| `05_tracking_plan.generated` | 10,034 | 4,245 | 26 | 14,279 |
| `03_user_stories.generated` | 10,034 | 3,275 | 61 | 13,309 |
| `01_requirement_brief` | 1,592 | 2,576 | 27 | 4,168 |

缓存情况：

- 10 个有 usage 的 `.meta.json` 中，`cached_tokens` 全部为 0。
- 这说明当前重复输入没有被缓存收益抵消。

## 3. 问题清单

### E-01：PRD 后续阶段重复输入上下文

| 字段 | 内容 |
|---|---|
| 严重级别 | P0 |
| 类型 | token waste / repeated context |
| 涉及 skill | `user-story-ac-generator`、`risk-edgecase-checker`、`tracking-plan-designer` |
| 责任 steward | `prd-writing-steward`、`efficiency-steward` |
| 证据 | `projects/demo-project/*generated.meta.json`、`projects/fitness-app-mvp/*generated.meta.json` |
| 浪费指标 | 两个项目中 `stories`、`risk`、`tracking` 三类输出合计重复输入 30,060 input tokens。 |
| 质量风险 | 中。直接合并输出可能降低专项质量，但共享压缩上下文风险可控。 |

明细：

| Project | `stories` input | `risk` input | `tracking` input | 小计 input |
|---|---:|---:|---:|---:|
| `demo-project` | 4,486 | 4,465 | 4,486 | 13,437 |
| `fitness-app-mvp` | 5,548 | 5,527 | 5,548 | 16,623 |
| 合计 | 10,034 | 9,992 | 10,034 | 30,060 |

治理建议：

1. 生成 PRD 后，先产出一个轻量 `prd_context_digest`，只包含目标用户、核心场景、MVP 范围、关键流程、约束和风险种子。
2. `stories`、`risk`、`tracking` 三个阶段改为读取 `prd_context_digest`，不要每次重复读取完整 PRD / 上游上下文。
3. 或者把三类配套输出合并为一次模型调用，再由结构化后处理拆成 3 个 artifact。
4. 如果继续拆开调用，至少启用缓存或固定前缀复用策略，并把 `cached_tokens` 纳入效率报告。

需要用户拍板：

- 是否允许改变 PRD 后续配套输出的执行方式。
- 是否优先做“共享 digest”而不是“一次性合并调用”。

### E-02：效率审计漏报启用 skill 数

| 字段 | 内容 |
|---|---|
| 严重级别 | P0 |
| 类型 | false negative / audit gap |
| 涉及文件 | `harness/efficiency_auditor.py`、`projects/graduation-defense-agent/runs/prd-draft-20260425/manifest.json`、`trace.json` |
| 责任 steward | `efficiency-steward`、`development-governance-steward` |
| 策略阈值 | `max_skill_calls: 8` |
| 实际证据 | `graduation-defense-agent` manifest 启用 19 个 skill，但 trace 为空。 |
| 报告结果 | 已保存 efficiency report 记录 `skill_call_count: 0` 且 `status: pass`。 |

根因：

- 当前审计代码用 `len(trace.get("skill_calls", []))` 作为 skill call count。
- 如果 run 只写 manifest，不写 trace skill calls，审计会把大量启用 skill 误判为 0。
- 报告中保留了 `manifest_enabled_skills`，但没有用它触发 warn。

治理建议：

1. 新增 `enabled_skill_count = len(manifest.enabled_skills)`。
2. skill 成本判断使用 `max(skill_call_count, enabled_skill_count)`，或分别输出 `trace_skill_call_count` 与 `enabled_skill_count`。
3. 如果 `enabled_skill_count > max_skill_calls`，必须产生 `too_many_enabled_skills` finding。
4. 如果 `manifest.enabled_skills` 非空而 `trace.skill_calls` 为空，产生 `trace_manifest_mismatch` finding。

需要用户拍板：

- 是否允许修改效率审计器，这是长期 harness 行为变更。

### E-03：已保存效率报告存在过期 / 不一致

| 字段 | 内容 |
|---|---|
| 严重级别 | P0 |
| 类型 | stale report / data reliability |
| 影响 | 治理决策不能直接信任已有 `efficiency_report.json`。 |

已确认不一致：

| Report | 保存报告内容 | 当前相关数据 | 风险 |
|---|---|---|---|
| `projects/demo-project/runs/pipeline-latest/efficiency_report.json` | `skill_call_count: 5`，enabled skills 5 个 | 当前 manifest 只启用 2 个 skill：`source-collector`、`prd-draft-writer` | 报告可能来自旧 run 或未同步。 |
| `projects/graduation-defense-agent/runs/prd-draft-20260425/efficiency_report.json` | `skill_call_count: 0`，`status: pass` | manifest 启用 19 个 skill；只读重算会触发 warn | 漏报过重 skill 启用。 |
| `graduation-defense-agent` PRD 指标 | 保存报告记录 PRD 13,841 chars | 当前只读重算 PRD 为 23,812 chars | 报告未随产物更新。 |

治理建议：

1. efficiency report 中增加 `generated_at`、`source_manifest_hash`、`source_trace_hash`、`artifact_hashes`。
2. closeout 或治理读取报告前，先检查报告是否 stale。
3. stale 时输出 `status: stale`，不要继续显示 `pass`。

### E-04：无 path concept skill 可被真实 run 引用

| 字段 | 内容 |
|---|---|
| 严重级别 | P1 |
| 类型 | registry hygiene / routing risk |
| 涉及 skill | 8 个无 `path` skill，重点是 `prd-draft-writer` |
| 证据 | `demo-project` manifest 启用 `prd-draft-writer`，但 registry 中该 skill 无 path。 |

风险判断：

- 不是所有无 path skill 都必须补插件；部分可作为 pipeline 内部概念。
- 但如果它出现在 manifest 的 `enabled_skills` 中，就会让执行者误以为有可加载 skill 文件。
- 后续治理、审计、路由和 token 成本归因都会变得不稳定。

治理建议：

| 选项 | 做法 | 建议 |
|---|---|---|
| A | 保留为 concept skill，但加 `execution_mode: pipeline_internal` | 推荐。最小改动，符合当前 pipeline 承载现实。 |
| B | 为 8 个 skill 全部补 `path` 和 `SKILL.md` | 不推荐。会增加 skill 数和维护成本。 |
| C | 从 manifest enabled skills 中移除无 path skill，只保留 action/stage | 可选。适合不希望把概念能力算作 skill 的口径。 |

### E-05：大型 skill 文档可能造成路由上下文浪费

| 字段 | 内容 |
|---|---|
| 严重级别 | P1 |
| 类型 | static prompt overhead |
| 影响范围 | `plugins/*/skills/*/SKILL.md` |
| 总字符数 | 88,066 chars / 32 files |

最大的 10 个 skill 文档：

| Skill file | Chars |
|---|---:|
| `plugins/prd-prototype-suite/skills/interactive-html-prototype-builder/SKILL.md` | 12,507 |
| `plugins/delivery-planning-suite/skills/agentic-delivery-orchestrator/SKILL.md` | 6,994 |
| `plugins/prd-prototype-suite/skills/low-fi-prototype-designer/SKILL.md` | 6,344 |
| `plugins/delivery-planning-suite/skills/codex-task-package-writer/SKILL.md` | 4,126 |
| `plugins/prd-prototype-suite/skills/product-flow-mapper/SKILL.md` | 3,650 |
| `plugins/delivery-planning-suite/skills/codex-development-plan-reviewer/SKILL.md` | 3,430 |
| `plugins/preference-memory-suite/skills/project-preference-cache-manager/SKILL.md` | 3,297 |
| `plugins/prd-analysis-suite/skills/scenario-roi-ranker/SKILL.md` | 2,980 |
| `plugins/quality-evaluation-suite/skills/skill-generalization-auditor/SKILL.md` | 2,948 |
| `plugins/prd-prototype-suite/skills/prototype-reference-analyzer/SKILL.md` | 2,612 |

判断：

- 如果 skill 只在触发后按需读取，风险可接受。
- 如果路由器或总控默认读取多个完整 `SKILL.md`，会形成固定 token 成本。

治理建议：

1. 给大型 skill 增加 200 至 400 字的 routing summary。
2. 总控 / router 只读 summary；真正触发后再读完整 `SKILL.md`。
3. 对超过 6,000 chars 的 skill 设置 `large_skill_doc` 标记。
4. 对 `interactive-html-prototype-builder` 单独评审，确认是否可拆出 reference 文档。

### E-06：效率审计覆盖范围过窄

| 字段 | 内容 |
|---|---|
| 严重级别 | P2 |
| 类型 | audit coverage gap |
| 当前覆盖 | 固定 5 个 PRD artifact：requirement brief、PRD、user stories、risk、tracking。 |
| 漏掉范围 | `ai/`、`delivery/`、`prototype/`、analysis JSON、final packages 等。 |

示例：

| Project | efficiency report total chars | 项目内非 run / closeout 文档总 chars | 倍数 |
|---|---:|---:|---:|
| `demo-project` | 17,059 | 46,941 | 2.75x |
| `fitness-app-mvp` | 22,620 | 93,148 | 4.12x |
| `graduation-defense-agent` | 14,539 | 131,186 | 9.02x |

`graduation-defense-agent` 中仅 `ai/` 与 `delivery/` 两组规划产物就有 78,779 chars：

| Directory | Chars |
|---|---:|
| `projects/graduation-defense-agent/ai` | 18,557 |
| `projects/graduation-defense-agent/delivery` | 60,222 |
| 合计 | 78,779 |

治理建议：

1. 效率审计保留固定 5 件套，但增加 `project_artifact_scan`。
2. 对 `ai/`、`delivery/`、`prototype/` 等目录按 run goal 动态设置阈值。
3. 对 closeout / archive / originals 排除，避免把存档误判为当前浪费。
4. 对规划型 run 单独统计 `required_outputs` 数量和总 chars。

### E-07：重试信号未进入浪费报告

| 字段 | 内容 |
|---|---|
| 严重级别 | P2 |
| 类型 | retry visibility gap |
| 证据 | `projects/demo-project/05_tracking_plan.generated.meta.json` 中 `attempt: 2`。 |
| 影响 | 当前只能看到最终 usage，无法知道第 1 次失败消耗了多少 token。 |

治理建议：

1. `.meta.json` 增加 `attempts` 列表，记录每次尝试的 status、error、usage。
2. efficiency report 增加 `retry_count`、`retry_token_estimate`。
3. 对重复失败的 stage 生成 `stage_retry_waste` finding。

## 4. Skill 治理清单

### 4.1 立即治理，不需要先改业务输出

| 编号 | 治理项 | 文件范围 | 是否需要用户批准 |
|---|---|---|---|
| G-01 | 修正 efficiency auditor skill 计数口径 | `harness/efficiency_auditor.py`、必要测试或回归样例 | 需要。长期 harness 行为变化。 |
| G-02 | 增加 report stale 检查 | `harness/efficiency_auditor.py` 或 closeout 读取逻辑 | 需要。长期报告机制变化。 |
| G-03 | 把无 path skill 标成 concept / pipeline internal | `registry/skills.yaml` | 需要。registry 长期语义变化。 |
| G-04 | 增加大型 skill 文档摘要路由字段 | `registry/skills.yaml` 或 plugin skill metadata | 需要。skill 路由机制变化。 |

### 4.2 需要影响生成链路的治理

| 编号 | 治理项 | 影响 | 推荐先后 |
|---|---|---|---|
| G-05 | 增加 `prd_context_digest` | 影响 PRD 后续 stories/risk/tracking 输入 | 先做。收益最大且可控。 |
| G-06 | 合并 stories/risk/tracking 为一次模型调用 | 可能影响专项质量与调试粒度 | 后做或作为实验。 |
| G-07 | 给大型 planning run 增加 output budget | 会影响 delivery / AI planning 输出长度 | 后做。先修审计再判断。 |

## 5. 建议的治理顺序

### Step 1：先修审计口径

目标：让效率报告能真实暴露问题。

最小改动：

1. `enabled_skill_count` 进入 efficiency report。
2. `enabled_skill_count > max_skill_calls` 触发 warn。
3. `manifest.enabled_skills` 与 `trace.skill_calls` 不一致时触发 warn。
4. report 写入 `generated_at` 和输入文件 fingerprint。

验收：

- `graduation-defense-agent/prd-draft-20260425` 应从 pass 变为 warn。
- `demo-project/pipeline-latest` 应暴露 report / manifest 不一致或在重跑后同步为 2。

### Step 2：治理 PRD 后续重复上下文

目标：减少 `stories`、`risk`、`tracking` 重复输入。

推荐方案：

- 新增或生成内部 `prd_context_digest`。
- 三个后续阶段只读取 digest 和必要专项字段。
- 先对一个 fixture 试跑，对比输出质量，再推广。

验收：

- 同类项目的后续三阶段 input tokens 降低。
- `cached_tokens` 或 digest 复用指标进入 report。
- 输出仍覆盖用户故事、风险、埋点所需质量项。

### Step 3：收口无 path skill

目标：让 registry 中的概念 skill 与可执行 skill 分清。

推荐方案：

- 不新增 8 个插件。
- 为无 path skill 增加明确执行口径，例如 `execution_mode: pipeline_internal` 或 `concept_only: true`。
- 禁止 concept skill 被统计为可加载 `SKILL.md`。

验收：

- registry validator 能区分 executable skill 与 concept skill。
- manifest 中如果出现 concept skill，report 明确标注，不再混入插件 skill 数。

### Step 4：大型 skill 文档动态加载

目标：避免总控或 router 默认读取大型 skill 全文。

推荐方案：

- 为超过 6,000 chars 的 skill 增加 summary。
- router 先读 summary；触发后再读完整 `SKILL.md` 和 references。

验收：

- `interactive-html-prototype-builder`、`agentic-delivery-orchestrator`、`low-fi-prototype-designer` 不在非相关任务中进入完整上下文。

## 6. 不建议现在做的事

| 不建议事项 | 原因 |
|---|---|
| 直接删除 skill | 当前证据证明有浪费风险，但不足以证明 skill 本身无价值。 |
| 把 8 个无 path skill 全部补成插件 | 会增加长期维护成本，且很多只是 pipeline 概念。 |
| 把 candidate skill 转 stable | 当前仍处于治理观察期。 |
| 为所有项目默认启用更多效率 checker | 会增加噪音。应先修现有漏报。 |
| 为省 token 降低 PRD / 风险 / 验收质量阈值 | 违反效率管家边界。 |

## 7. 本轮检查命令摘要

只读检查：

```bash
find projects -path '*/efficiency_report.json' -print
find projects -name '*.meta.json' -print
find projects -path '*/trace.json' -print
find projects -path '*/manifest.json' -print
rg --files plugins | rg '/skills/[^/]+/SKILL\\.md$'
PYTHONPATH=harness python3 - <<'PY'
from pathlib import Path
from harness.efficiency_auditor import audit_efficiency
for project, run in [
    ("demo-project", "pipeline-latest"),
    ("fitness-app-mvp", "governance-baseline"),
    ("fitness-app-mvp", "plan-execution-preview-20260425"),
    ("fitness-app-mvp", "prd-analysis-suite-20260423"),
    ("fitness-app-mvp", "prototype-preview-20260424"),
    ("graduation-defense-agent", "prd-draft-20260425"),
]:
    print(project, run, audit_efficiency(Path("."), project, run_id=run, write_report=False))
PY
```

未执行：

- 未改 `registry/skills.yaml`。
- 未改 `harness/efficiency_auditor.py`。
- 未重写任何 `efficiency_report.json`。
- 未删除、归档或移动任何 skill / artifact。

## 8. 结论

这次报告不建议先治理“哪个 skill 删掉”，而是建议先治理“效率审计是否能真实发现浪费”。当前最大问题是审计漏报和重复输入，而不是某个单一 skill 已经证明无用。

推荐先批准一个最小治理批次：

1. 修 `efficiency_auditor` 的 manifest / trace 计数和 stale 检查。
2. 给 PRD 后续三阶段增加共享 digest，先做一个项目试跑。
3. 给 8 个无 path skill 增加 concept / pipeline internal 口径。

完成这三步后，再根据新的效率报告决定是否瘦身、合并或冻结具体 skill。
