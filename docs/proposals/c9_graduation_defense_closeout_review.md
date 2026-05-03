# C9 Graduation Defense Agent Closeout 审查

- 日期：2026-05-02
- 状态：项目 closeout 审查材料，不批准归档、删除、移动、staging、commit、push、PR、长期记忆写入或项目产物提交。
- 范围：`projects/graduation-defense-agent/` 与相关散落归档材料 `docs/archive/notes/答辩.md`。
- 主线任务：确认该项目是否可以进入收口候选，并判断项目产物、原始输入、原型、AI 方案、Codex 开发文档和归档材料的边界。

## 结论

`graduation-defense-agent` 应保持为 `closeout_candidate`，暂不归档、暂不提交项目产物、暂不删除任何文件。

它是一个高价值项目样例，但不是稳定核心资产：

- 适合用来复核复杂链路：PRD -> AI 方案 -> delivery plan -> Codex 开发文档 -> prototype -> closeout。
- 不适合直接变成 golden sample，因为它是 AI-heavy 项目，且当前 PRD 是生成稿，不是人工确认 final PRD。
- `docs/archive/notes/答辩.md` 与该项目高度相关，应标记为该项目原始输入证据候选，但不能自动搬移、提交或归档。

## 处理后的效果

按本方案处理后，可以达到这些效果：

| 目标 | 效果 |
|---|---|
| 防止项目产物污染稳定核心 | 不把 PRD、prototype、AI 方案、delivery 文档、run 输出混入治理提交。 |
| 防止归档材料失联 | `答辩.md` 被识别为该项目原始输入证据候选，后续不会被当作无关 archive 文件误删。 |
| 保留架构反哺价值 | 复杂 AI 项目链路的经验先进入项目候选，不直接改 skill、harness、workflow 或模板。 |
| 降低清理风险 | `.DS_Store`、大图、完整交付包、原始输入都进入监督清单，不执行自动清理。 |
| 保持主线稳定 | 当前治理线程只做边界审查，不展开答辩产品功能设计。 |

## 当前证据

| 证据 | 结论 |
|---|---|
| `project_state.json` | 已标记需要 delivery plan、AI solution、agentic delivery、Codex 开发文档，并已有 prototype preview / full prototype approval。 |
| `closeout/closeout-report.md` | closeout 是 dry run，只生成报告，不执行清理；扫描 57 个文件，约 12.95MB。 |
| `closeout/cleanup-plan.md` | 明确 archive before delete，硬删除至少 30 天后且仍需二次批准。 |
| `closeout/preference-memory-disposition.md` | 未发现项目偏好缓存，不需要清空缓存，也不写长期记忆。 |
| `00_raw_input.md` | source 指向用户提供的 `text/.md/答辩.md`，摘要描述 150 个答辩问题、追问规则、评分维度和回答模板。 |
| `docs/archive/notes/答辩.md` | 内容与 `00_raw_input.md` 描述一致，是毕业答辩问题库；应视为该项目原始输入证据候选。 |
| `prototype/*` | 已有 preview、full prototype、dark/light 版本和 PNG/SVG，属于项目产物，不进入稳定核心。 |
| `ai/*` 与 `delivery/*` | 产物完整，适合作为复杂 AI 项目链路证据，但暂不稳定化。 |

## 发现的问题

### 1. 项目状态有轻微不一致

`project_state.json` 的 `current_stage` 仍是 `intake`，但 `completed_stages` 已包含 delivery planning、AI solution planning、agentic delivery planning、capability enablement、skill MCP routing、development governance 和 Codex blueprint。

判断：

- 这不是当前治理主链路故障。
- 但它说明项目生命周期状态没有完全回写，后续 closeout / archive 前应刷新项目状态或在 closeout 报告里注明。

建议：

- 先记录，不改项目文件。
- 后续如果进入正式归档前，再做项目状态刷新方案。

### 2. `答辩.md` 属于项目输入证据，但位置还没有归属决定

`00_raw_input.md` 明确记录原始输入来自 `text/.md/答辩.md`。当前散落在 `docs/archive/notes/答辩.md` 的内容就是该问题库。

判断：

- 它不应作为通用 archive note 直接提交。
- 它也不应直接进入 stable docs 或长期记忆。
- 更合理的归属是：项目原始输入证据候选，随 `graduation-defense-agent` closeout 一起处理。

建议：

- 当前不移动、不提交、不删除。
- 后续如果你确认项目归档，可以选择归入项目归档证据，或者只保留摘要并把全文列入 30 天后删除候选。

### 3. 项目产物完整但较重

项目包含 PRD、AI 方案、交付计划、Codex 开发文档、完整原型和多个运行报告，体量约 13MB。

判断：

- 它有审计价值和架构学习价值。
- 但直接提交整个项目会增加仓库噪音，且会把项目过程产物混进治理资产。

建议：

- 当前不提交项目。
- 后续只在项目归档批次中处理，不和稳定治理核心混合提交。

### 4. `00_complete_delivery_package.md` 是高价值但未注册的项目交付包

closeout 把它标记为 `manual_review`，原因是未注册文件。

判断：

- 它可能是对外或内部完整交付预览。
- 但未注册意味着不能自动视为正式 artifact。

建议：

- 当前保留项目内，不提交。
- 后续如果要保留，应先决定它是内部交付包、外部保护版包，还是归档证据。

### 5. `.DS_Store` 是清理候选，但不能现在删除

closeout 把 `.DS_Store` 标记为人工审核。

判断：

- 它没有产品或架构价值。
- 但当前原则是不做删除。

建议：

- 后续可以列入 30 天后删除候选。
- 现在不删除、不提交。

## 架构反哺候选

这些只进入候选，不自动改稳定规则：

| 候选 | 价值 | 建议 |
|---|---|---|
| 项目原始输入和散落 archive 的映射 | 防止 `答辩.md` 这类材料失联或误删。 | 后续在 closeout 报告里加强 `source_file -> archive candidate` 映射说明，先作为 proposal 候选。 |
| AI-heavy 项目的完整交付链路 | 可验证 PRD、AI 方案、delivery、Codex 文档、prototype 的协作边界。 | 后续作为复杂项目样例候选，不直接成为 stable golden sample。 |
| closeout 状态回写 | 当前 `current_stage=intake` 与完成产物不一致。 | 后续归档前做状态刷新或状态解释，不新增 harness。 |
| 未注册交付包识别 | `00_complete_delivery_package.md` 有价值但未注册。 | 后续可考虑 artifact registry 是否需要通用 `delivery_package_markdown`，但必须先有多项目证据和你批准。 |

## 需要你后续拍板

| 决策 | 我的建议 | 优势 | 劣势 / 风险 | 选择后的效果 |
|---|---|---|---|---|
| 项目是否进入正式 closeout | 暂缓，继续保持 `closeout_candidate` | 保留项目上下文，避免过早归档。 | 工作区继续有项目目录噪音。 | 稳定优先，后续可随时单独处理。 |
| `答辩.md` 怎么归属 | 标记为项目原始输入证据候选 | 避免误删，也避免混入通用 archive。 | 仍然暂时留在未跟踪区。 | 后续项目归档时一起处理。 |
| 是否提交整个项目 | 不提交 | 避免项目产物污染稳定核心。 | 项目证据暂时不进入 Git 历史。 | 保持主仓库稳定、轻量。 |
| 是否把它做成 AI-heavy golden sample | 暂不做 | 避免单项目过拟合。 | 暂时少一个复杂样例基线。 | 后续可和 Jiaxiaoqian 等项目组合成样例集。 |
| `00_complete_delivery_package.md` 是否保留 | 项目内保留，后续人工审核 | 保留完整交付上下文。 | 未注册 artifact 边界未定。 | 后续再决定内部版 / 外部保护版 / 归档证据。 |
| `.DS_Store` 是否删除 | 后续列入 30 天后删除候选 | 最终可减少无效文件。 | 现在删除会违反本轮不删除原则。 | 当前保留，后续精确批准后再清理。 |
| 是否把架构反馈写入 stable docs | 不直接写 | 避免项目经验过早长期化。 | 需要多一步人工筛选。 | 先进入候选，后续由你逐条批准。 |

## 推荐下一步

当前不建议继续深入答辩产品功能。下一步按治理主线，建议处理：

1. `jiaxiaoqian-ai-invest-research` high-value closeout review。
2. 重点看它的 PRD、B 包、开发文档、prototype、zip 和架构反馈。
3. 对比本项目和 Jiaxiaoqian，判断是否有通用的复杂项目 closeout 规则需要候选化。

## 本轮不做

- 不 staging / commit `projects/graduation-defense-agent/*`。
- 不移动 `docs/archive/notes/答辩.md`。
- 不删除 `.DS_Store`。
- 不归档项目。
- 不写长期记忆。
- 不把项目升级为 golden sample。
- 不修改 skill、harness、workflow、registry、pipeline 或 automation。
