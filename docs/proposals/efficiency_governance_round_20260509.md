# 效率部治理批次 R1 - Skill / Token 处置清单

- 日期：2026-05-09
- 状态：治理处置建议，不批准 staging、commit、push、PR、删除、Skill 下线、candidate 转 stable、registry 默认路由变更或长期规则自动写入。
- 主线任务：按效率部闭环跑一轮只读治理，识别需要处理、静默、观察或暂缓的 Skill。
- 数据来源：`projects/*/runs/*/{manifest,trace}.json`、`projects/**/*.meta.json`、`registry/skills.yaml`、只读重算的 `harness/efficiency_auditor.py`。

## 1. 本轮结论

本轮扫描：

| 项 | 数量 |
|---|---:|
| run manifest | 8 |
| token meta 文件 | 10 |
| registry skill | 40 |
| 有实际调用或启用证据的 skill | 30 |
| 本轮无使用证据的注册 skill | 10 |

需要处理的不是所有 Skill，而是三类：

1. **P0：PRD 主链路 concept skill 有真实 token 成本，但无 `path` / 可加载合同。**
2. **P1：毕业答辩项目一次启用 19 个规划型 Skill，但 trace 为空，应在项目收口后默认静默。**
3. **P2：有真实调用且未发现浪费的 Skill 保持 `watch`，不转 stable。**

本轮不执行静默或 registry 变更，只给出处置建议和 owner。

## 2. Run 级治理问题

| Project / Run | Finding | Owner | 建议 |
|---|---|---|---|
| `demo-project/pipeline-latest` | `enabled_concept_skills` | `development-governance-steward` | `prd-draft-writer` 是无 path concept skill，却出现在 run manifest，应标为 `pipeline_internal` 或从可执行 Skill 路由中移除。 |
| `graduation-defense-agent/prd-draft-20260425` | `too_many_enabled_skills` | `pm-copilot-chief` | manifest 启用 19 个 Skill，超过效率阈值 8；后续应拆成 delivery planning / AI planning / governance planning 分阶段。 |
| `graduation-defense-agent/prd-draft-20260425` | `trace_manifest_mismatch` | `development-governance-steward` | manifest 启用 19 个 Skill，但 trace 记录 0 个实际调用；需要区分 planned enabled 和 actual called。 |

### 2.1 Run 级治理判断

`graduation-defense-agent` 的 19 个 Skill 不能直接判定为“无用”，但可以判定为：

- 当前没有 trace 调用证据。
- 当前 run 过重。
- 项目 closeout 后不应默认继续唤醒。
- 以后如需复用，必须由具体任务重新触发，而不是沿用该项目 manifest。

## 3. P0：必须治理的 Skill

这些 Skill 有明确合同问题或重复 token 成本。建议先治理执行口径和上下文复用，不建议马上新增插件。

| Skill | Owner | 建议处置 | 证据 | 治理动作 |
|---|---|---|---|---|
| `prd-draft-writer` | `prd-writing-steward` + `development-governance-steward` | `optimize_required` + `pipeline_internal` | 无 `path`，但被 run 启用；累计 14,466 tokens；毕业答辩 PRD 有 repeated output。 | 标明 pipeline internal；PRD 生成后增加去重 / 复核；不得作为可加载 `SKILL.md` 默认路由。 |
| `user-story-ac-generator` | `prd-writing-steward` | `optimize_required` + `pipeline_internal` | 无 `path`；累计 13,309 tokens；input 10,034，cached=0。 | 改为读取 `prd_context_digest`，避免重复读取完整 PRD。 |
| `risk-edgecase-checker` | `review-steward` | `optimize_required` + `pipeline_internal` | 无 `path`；累计 15,882 tokens；input 9,992，cached=0。 | 风险检查保留质量门槛，但输入改为 digest + 风险种子。 |
| `tracking-plan-designer` | `prd-writing-steward` | `optimize_required` + `pipeline_internal` | 无 `path`；累计 14,279 tokens；input 10,034，cached=0；demo 中 `attempt=2`。 | 改为读取 digest；记录 retry reason；失败重试必须进入效率报告。 |

### 3.1 P0 推荐整改顺序

1. Registry 层：给上述 4 个 Skill 加 `execution_mode: pipeline_internal`，避免被当作可加载 Skill。
2. Pipeline 层：生成 `prd_context_digest`，作为 stories / risk / tracking 的共同输入。
3. Efficiency 层：把 `cached_tokens`、`attempt`、`repeat_input_tokens_estimate` 写入报告。
4. Quality 层：复测 PRD、用户故事、风险、埋点输出，不允许为省 token 降低质量。

需要你拍板后才能执行 registry / pipeline 变更。

## 4. P1：项目结束后建议静默的 Skill

这些 Skill 都来自 `graduation-defense-agent/prd-draft-20260425`。manifest 启用，但 trace 没有实际调用证据。建议在该项目 closeout 后统一进入 `silent` 建议状态，不直接删除。

| Skill | Owner | 建议处置 | 原因 |
|---|---|---|---|
| `technical-scope-planner` | `delivery-planning-steward` | `silent_after_closeout` | 启用但无调用证据。 |
| `release-roadmap-planner` | `delivery-planning-steward` | `silent_after_closeout` | 启用但无调用证据。 |
| `effort-estimator` | `delivery-planning-steward` | `silent_after_closeout` | 启用但无调用证据。 |
| `delivery-effect-definer` | `delivery-planning-steward` | `silent_after_closeout` | 启用但无调用证据。 |
| `delivery-quality-reviewer` | `delivery-planning-steward` | `silent_after_closeout` | 启用但无调用证据。 |
| `agentic-delivery-orchestrator` | `delivery-planning-steward` | `silent_after_closeout` | 启用但无调用证据；高成本规划型 Skill。 |
| `capability-enablement-planner` | `capability-enablement-steward` | `silent_after_closeout` | 启用但无调用证据。 |
| `skill-mcp-routing-planner` | `capability-enablement-steward` | `silent_after_closeout` | 启用但无调用证据。 |
| `development-governance-orchestrator` | `development-governance-steward` | `silent_after_closeout` | 启用但无调用证据。 |
| `codex-task-package-writer` | `development-governance-steward` | `silent_after_closeout` | 启用但无调用证据。 |
| `ai-capability-mapper` | `ai-architecture-steward` | `silent_after_closeout` | 启用但无调用证据。 |
| `model-selection-planner` | `ai-architecture-steward` | `silent_after_closeout` | 启用但无调用证据；模型选择必须按项目重新触发。 |
| `prompt-architecture-designer` | `ai-architecture-steward` | `silent_after_closeout` | 启用但无调用证据。 |
| `rag-architecture-planner` | `ai-architecture-steward` | `silent_after_closeout` | 启用但无调用证据。 |
| `conversation-memory-planner` | `ai-coaching-steward` | `silent_after_closeout` | 启用但无调用证据。 |
| `learner-profile-modeler` | `ai-coaching-steward` | `silent_after_closeout` | 启用但无调用证据。 |
| `adaptive-coaching-planner` | `ai-coaching-steward` | `silent_after_closeout` | 启用但无调用证据。 |
| `ai-technical-architecture-planner` | `ai-architecture-steward` | `silent_after_closeout` | 启用但无调用证据。 |
| `ai-solution-reviewer` | `ai-architecture-steward` | `silent_after_closeout` | 启用但无调用证据。 |

### 4.1 P1 推荐治理动作

不逐个改 Skill 内容，先处理 workflow 级问题：

1. `graduation-defense-agent` 进入正式 closeout 时，生成并审核 `skill-disposition.md`。
2. 对这 19 个 Skill 默认选择 `silent_after_closeout`，除非你确认某个 Skill 有跨项目复用价值。
3. 后续项目需要 AI / delivery / governance 能力时，按任务重新触发，而不是继承该项目的 19 Skill manifest。
4. 修正 run 记录口径：`enabled_skills` 表示计划启用，`trace.skill_calls` 表示实际调用；两者不能混用。

## 5. P2：继续 Watch 的 Skill

这些 Skill 有真实调用证据，且本轮没有 efficiency finding。建议保持 `watch`，不转 stable，不默认扩大使用。

| Skill | Owner | 使用证据 | 建议 |
|---|---|---|---|
| `source-collector` | `research-steward` | `demo-project`、`fitness-app-mvp` | `watch` |
| `user-universe-mapper` | `product-judgment-steward` | `fitness-app-mvp` | `watch` |
| `pain-needs-analyzer` | `product-judgment-steward` | `fitness-app-mvp` | `watch` |
| `competitor-gap-analyzer` | `product-judgment-steward` | `fitness-app-mvp` | `watch` |
| `scenario-roi-ranker` | `product-judgment-steward` | `fitness-app-mvp` | `watch` |
| `mvp-scope-decider` | `product-judgment-steward` | `fitness-app-mvp` | `watch` |
| `prototype-reference-analyzer` | `prototype-design-steward` | `fitness-app-mvp` | `watch` |
| `product-flow-mapper` | `prototype-design-steward` | `fitness-app-mvp` | `watch` |
| `low-fi-prototype-designer` | `prototype-design-steward` | `fitness-app-mvp` | `watch` |
| `project-preference-cache-manager` | `learning-steward` | `fitness-app-mvp` | `watch` |

## 6. P3：本轮无使用证据的 Skill

这些 Skill 在 registry 中存在，但本轮 run / token meta 没看到实际使用。建议暂不删，放入低频观察池；如果连续多个项目 closeout 仍无使用证据，再进入 `archive_candidate` 审查。

| Skill | 建议 |
|---|---|
| `codex-development-plan-reviewer` | keep candidate / observe |
| `interactive-html-prototype-builder` | keep candidate / observe |
| `memory-learning-extractor` | keep candidate / observe |
| `pdf-prd-style-learner` | keep candidate / observe |
| `prd-quality-reviewer` | keep candidate / observe |
| `prd-structure-planner` | keep candidate / observe |
| `skill-generalization-auditor` | keep candidate / observe |

备注：`user-story-ac-generator`、`risk-edgecase-checker`、`tracking-plan-designer` 虽然当前 manifest 未启用，但有 token meta 证据，已归入 P0。

## 7. 本轮建议的审批项

| 决策 | 推荐 | 影响 |
|---|---|---|
| 是否处理 P0 四个 concept skill | 是 | 明确 pipeline internal，减少可执行 Skill 路由混乱。 |
| 是否先做 `prd_context_digest` | 是 | 直接减少 stories / risk / tracking 的重复 input token。 |
| 是否直接删除无 path Skill | 否 | 它们仍是 pipeline 概念，删除会破坏历史和 workflow 语义。 |
| 是否直接静默 19 个毕业答辩 Skill | 暂不直接改 registry；先在项目 closeout 中确认 | 避免误伤跨项目能力。 |
| 是否将 P2 转 stable | 否 | 当前只有调用证据，没有稳定推广证据。 |
| 是否把 P3 归档 | 暂不 | 证据不足，先继续观察。 |

## 8. 执行边界

本轮已经完成：

- 只读扫描 run / token / registry。
- 生成本治理处置清单。
- 明确 owner、建议处置和审批项。

本轮没有执行：

- 没有修改 `registry/skills.yaml`。
- 没有让任何 Skill 静默。
- 没有删除 Skill。
- 没有转 stable。
- 没有刷新项目内 `efficiency_report.json`。
- 没有修改项目 closeout 目录。

## 9. 下一步最小可执行批次

如果你批准进入执行，建议下一批只做 P0：

1. 给 4 个 PRD 主链路 concept skill 增加 `execution_mode: pipeline_internal`。
2. 在效率审计或 pipeline 说明中明确这些 concept skill 不作为可加载 `SKILL.md`。
3. 设计 `prd_context_digest` 的最小字段，不先改模型调用。
4. 跑 demo / fitness 的回归与效率审计，确认 finding 变少且质量不下降。

这批完成后，再处理毕业答辩 19 个规划型 Skill 的 closeout 静默建议。
