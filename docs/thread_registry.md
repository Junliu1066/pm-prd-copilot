# Thread Registry

- 日期：2026-05-03
- 状态：轻量线程台账草案，不是 stable policy。
- 作用：记录当前主线、搁置线程、待拍板项和下一步最小动作，防止线程长期搁置、任务漂移和经验丢失。
- 规则：本文件不批准归档、删除、清空缓存、staging、commit、push、PR、长期记忆写入、stable 转正或自动化创建。

## 使用规则

- 每个重要线程必须记录：主线、预期效果、状态、最后推进时间、阻塞点、待拍板项、下一步最小动作。
- 5 天没有推进的线程，应生成停滞报告，而不是自动归档或删除。
- 线程经验只能进入候选；长期规则必须用户逐条批准。
- 项目线程、归档线程、长期治理线程必须分开，不能互相污染。
- 状态不确定时，默认 `active`、`waiting_user` 或 `parked`，不能默认归档或删除。
- 默认采用例外审批制：L1 自动处理，L2 汇总给用户批量审批，L3 必须单独上报用户。

## 授权矩阵

成熟后的治理不应每一步都让用户把关。当前台账按以下授权试运行，仍不是 stable policy。

| 等级 | 处理方式 | 当前允许范围 | 用户介入 |
|---|---|---|---|
| L1 自动处理 | 直接执行，事后汇报 | 只读检查、临时目录验证、中文报告、proposal 分类、台账更新、check-only、低风险一致性修复 | 不需要逐项确认 |
| L2 汇总审批 | 我先准备方案、清单、风险和检查结果，再集中给你拍板 | staging 清单、commit 审查、candidate 样例、项目 closeout 审查、proposal 决策记录提交、可回滚补丁 | 用户集中批准 |
| L3 单独审批 | 必须单独问你，未经批准不执行 | 删除、归档、push / PR、长期记忆、stable policy、新增或稳定 skill / harness、模型成本变化、外部发布 | 用户单独批准 |

### 本台账的自动处理边界

本文件允许自动更新：

- 当前主线、下一步最小动作和状态。
- L1 / L2 / L3 分类。
- 试运行检查结果。
- 待用户拍板项的汇总。
- 已完成事项的进度记录。

本文件不授权：

- `git add`、commit、push、PR。
- 删除、归档、恢复、移动项目文件。
- 写长期记忆。
- candidate 转 stable。
- 新增 skill、harness、workflow、plugin、automation。

## 上下文恢复卡

每次恢复线程、切换任务或用户提出新方向时，先看本卡，防止上下文稀释导致遗忘或跑偏。

| 项目 | 当前记录 |
|---|---|
| 当前主线 | 治理架构收口，17 个 proposal 决策记录已提交为 `09de668`，当前正在做台账收口。 |
| 为什么做 | 用户目标是长期稳定、可监督、可迭代、自我收敛的架构系统；skill / harness / plugin 只是工具。 |
| 当前做到哪 | A/B/D/E 稳定核心和候选能力已分批收口；C 批已完成 demo、fitness、graduation、Jiaxiaoqian、taxi-hailing、AI collaboration、prompt workbench、Santoip、temp-generated 审查；C11 已提交为 `852a2d5 Add deidentified PRD structure golden case`；17 个 proposal 决策记录已提交为 `09de668 Record governance lifecycle decision proposals`。 |
| 下一步最小动作 | 单独提交台账收口；之后处理临时 proposal 30 天删除候选清单。 |
| 当前不做 | 不转 stable、不新增 skill / harness、不删除、不归档、不提交项目产物、不写长期记忆、不 push / PR。 |
| 最近检查 | 2026-05-03 regression 和 harness check-only 通过；后续每次改文档后继续跑 check-only。 |
| 需要用户拍板 | stable 转正、长期记忆、删除、归档、push / PR、低风险自动化放权、新增或稳定 skill / harness。 |

## 当前授权状态

| 项目 | 当前状态 |
|---|---|
| L1 自动处理 | 已试运行：允许我自动更新 proposal、台账、分类表和 check-only 汇报。 |
| L2 汇总审批 | 已试运行：后续 staging / commit / candidate 入库由我先做审查包，再集中请你批准。 |
| L3 单独审批 | 永久保留：删除、归档、长期记忆、stable、push / PR、新增或稳定 skill / harness 必须单独问你。 |
| 当前效果 | 减少你对低风险过程的干预，同时保留高风险监督。 |

## 架构优化迭代流程

新想法、错误、项目反馈、AI 情报或用户大方向调整，都按这个流程走，不能直接跳到新增工具或改 stable 规则。

```text
收集输入
-> 分类
-> 判断是否影响当前主线
-> 拆成最小动作
-> 排优先级
-> 执行当前主线
-> 两轮检查
-> closeout / 复盘
-> 进入 architecture inbox
-> 判断 stable / candidate / archive / delete-after-30-days
-> 上报需要用户拍板的事项
```

### 分类规则

| 类型 | 例子 | 默认处理 |
|---|---|---|
| 当前主线 | 正在处理的治理收口、项目 closeout、架构 proposal | 继续推进。 |
| 支线补充 | 能降低当前主线不确定性的证据检查 | 只做最小检查。 |
| 长期候选 | 新架构思想、流程优化、偏好、AI 情报启发 | 进入 proposal / architecture inbox。 |
| 项目特例 | 单个项目的问题、偏好、产物 | 项目内保留，不跨项目复用。 |
| 临时材料 | staging list、commit review、run output | 生命周期标记，后续 30 天删除候选。 |

### 优先级规则

| 优先级 | 含义 | 处理方式 |
|---|---|---|
| P0 | 影响稳定核心或会导致遗漏复发 | 优先处理，并跑 regression / harness。 |
| P1 | 影响当前治理收口和项目生命周期 | 当前主线后立即处理。 |
| P2 | 提升效率、观感或使用体验 | 进入看板，等待主线空档。 |
| P3 | 候选想法或低证据材料 | parked，不进入当前执行。 |

## 治理任务看板

WIP 限制：同一时间只允许 1 个 `doing` 主线，最多 1 个 `next` 候选；其它保持 `parked` 或 `waiting_user`。

| ID | 主线 | 状态 | 为什么做 | 下一步最小动作 | 需要用户拍板 |
|---|---|---|---|---|---|
| ARCH-01 | 架构自治运行机制 | `waiting_user` | 防止治理继续靠单点补丁，建立例外审批制和 L1/L2/L3 授权矩阵。 | 已更新 proposal，按 L1 试运行；暂不转 stable。 | 是否后续转 stable；是否扩大 L1/L2 授权。 |
| C11 | 打车 PRD golden sample 脱敏 | `done` | 把具体测试项目抽象成 0-1 普通业务 PRD 样例候选。 | 已提交 `852a2d5`，不提交项目产物；后续只在多项目证据足够时考虑 portfolio。 | 是否后续扩展样例组合。 |
| C12 | AI 协作平台 closeout 刷新 | `done` | 旧 closeout 只扫到 1 个文件，当前项目实际有 45 个文件，不能直接归档或提交。 | 已用临时目录刷新 closeout，生成 C12 中文审查报告；项目保持 closeout candidate。 | 后续是否提交 C12 审查报告；是否作为复杂交付链路候选。 |
| C13 | Prompt 工作台项目 | `done` | 证据较薄，实际是评测报告 / Prompt 工作台 HTML 原型输出。 | 已生成 C13 中文审查报告，标记为 `prototype_artifact_closeout_candidate`。 | 后续是否提交 C13 审查报告；是否统一归档低证据原型项目。 |
| C14 | Santoip 品牌视频项目 | `done` | 证据较薄，实际是 AI 商标品牌视频生成器 HTML 原型输出。 | 已生成 C14 中文审查报告，标记为 `prototype_artifact_closeout_candidate`。 | 后续是否提交 C14 审查报告；是否作为业务原型案例候选。 |
| C15 | temp-generated-project | `done` | 明确 temporary，但包含完整临时交付包，不能直接删除。 | 已生成 C15 中文审查报告，标记为 `temporary_project_evidence_delete_after_30_days_candidate`。 | 是否后续进入 30 天删除候选；是否提交 C15 审查报告。 |
| C16 | 项目 zip / package 生命周期 | `done` | 多个 zip 和 archive 包会持续污染工作区。 | 已生成 C16 中文审查报告，区分 project package、prototype zip、archive evidence、duplicate candidate。 | 后续是否提交 C16 审查报告；是否确认 Jiaxiaoqian 英文完整包为 canonical。 |
| ARCHIVE-01 | AI raw 生命周期 | `waiting_user` | raw 不应提交，但需要复核和删除候选边界。 | 确认是否进入 30 天删除候选。 | raw 是否保留 / 删除候选。 |
| ARCHIVE-02 | `Remod开发.md` | `parked` | 旧治理笔记可能已有内容被吸收，也可能误导新增 skill / harness。 | 判断是否提炼中文总结。 | 提炼、保留或删除候选。 |
| PRUNE-01 | skill / harness / plugin 瘦身 | `parked` | 防止工具层膨胀，保持架构轻量。 | 等项目和 proposal 收口后复核。 | 哪些 candidate 保留 / 归档 / 删除候选。 |
| REPORT-01 | 本轮治理总验收报告 | `parked` | 给用户完整验收当前治理修复成果。 | 等关键剩余项处理后输出。 | 是否提交验收报告。 |

## 当前治理修复快照

| 区域 | 当前进度 | 下一步 |
|---|---|---|
| A1 PRD 主链路 | 已提交，PRD 口径稳定为页面说明、页面跳转关系、原型图层，非 AI 项目不写 AI 选型。 | 后续只做回归守护。 |
| A2 治理合同 | 已提交，pipeline 默认 governed，fast draft 必须显式。 | 后续只做回归守护。 |
| A3 必要检查 | 已提交，5 个必要检查已稳定。 | 后续按版本 / 模型更新做瘦身复核。 |
| A4 交付 / closeout / 偏好边界 | 已复核并提交必要部分，长期偏好已收敛。 | A4 真实项目输出继续观察，不扩大 stable。 |
| B 批治理文档 | B1-B5 主干已分批收口。 | 剩余 proposal 临时材料继续按生命周期清单处理。 |
| D 批候选能力 | D1-D3 已收口，candidate 保持 candidate，不转 stable。 | 后续按 promotion gate 复核。 |
| E 批 root/archive | root cleanup 已提交最小 archive 证据。 | 额外 archive notes 仍需单独审。 |
| C 批项目产物 | demo run / closeout 已提交；demo prototype、fitness、memory-cache 已审查为项目内保留；其它 `projects/*` 已完成生命周期盘点；`graduation-defense-agent` 已完成 C9 closeout 审查；`jiaxiaoqian-ai-invest-research` 已完成 C10 high-value closeout 审查；`taxi-hailing-prd-test` C11 已提交脱敏样例候选和 regression 依赖修复；C12-C16 项目产物和 package 生命周期审查已完成。 | 暂不提交项目产物；下一步可汇总 C12-C16 或处理 proposal 决策记录候选。 |
| 生命周期嵌入 | `governance_lifecycle_embedding_plan.md` 已生成。 | 用它处理 AI raw、archive notes、其它项目和候选能力复盘。 |
| 线程监督 | `thread_lifecycle_supervision_plan.md` 已生成。 | 当前文件作为轻量台账试运行。 |

## 当前线程台账

| 线程 | 类型 | 项目 | 状态 | 最后推进 | 当前主线 | 阻塞点 | 下一步最小动作 |
|---|---|---|---|---|---|---|---|
| governance-repair-main | 长期治理 | governance | `active` | 2026-05-03 | 用生命周期机制完成剩余治理收口，保持稳定核心不被项目产物污染。 | 17 个 proposal 决策记录已提交，无 C12-C16 阻塞。 | 单独提交台账收口。 |
| architecture-self-management-system | 长期治理 | governance | `waiting_user` | 2026-05-03 | 已生成并更新“架构自我管理与最小可行治理机制”proposal，加入例外审批制和 L1/L2/L3 授权矩阵。 | 是否后续转 stable 或扩大授权，需要用户审核。 | 先按 proposal 试运行：L1 自动处理，L2 汇总审批，L3 单独审批。 |
| proposal-lifecycle-cleanup | 长期治理 | governance | `active` | 2026-05-03 | 17 个 proposal 决策记录已提交；剩余 18 个未跟踪 proposal 分成 16 个临时材料和 2 个已覆盖旧审查。 | 后续是否进入 30 天删除候选需要用户最终批准。 | 先提交台账收口；再做临时材料 30 天删除候选清单。 |
| thread-lifecycle-supervision | 长期治理 | governance | `active` | 2026-05-02 | 建立线程台账和 5 天停滞总结机制。 | 是否后续创建自动化提醒尚未批准。 | 先用本台账试运行，不创建自动化。 |
| ai-intel-raw-disposition | AI 情报 | governance | `waiting_user` | 2026-05-02 | 明确 raw、daily、events、logs、decision docs 的证据边界。 | raw 是否作为 30 天后删除候选，需要用户后续确认。 | 等用户确认 raw 不提交、暂不删除、后续进入 30 天删除候选。 |
| archive-notes-disposition | 归档治理 | governance | `waiting_user` | 2026-05-02 | 处理 `docs/archive/notes/` 和额外 archive 文件，不扩大 E 批。 | `答辩.md` 已在 C9 中识别为 `graduation-defense-agent` 原始输入证据候选；`Remod开发.md` 仍需后续判断是否提炼或列入候选清理。 | 后续随 `Remod开发.md` candidate 瘦身复盘处理；`答辩.md` 等项目正式 closeout 时拍板。 |
| demo-project-fixture | 项目 / fixture | demo-project | `parked` | 2026-05-02 | 保留 demo 作为治理 fixture，不提交 prototype PNG。 | prototype 是否后续作为项目证据提交仍暂缓。 | 暂不处理，除非进入项目证据批次。 |
| fitness-app-mvp | 项目 | fitness-app-mvp | `parked` | 2026-05-02 | 保持 active / closeout candidate，项目产物和 memory-cache 项目内保留。 | 是否继续推进 fitness 项目需在项目线程决定。 | 不在治理线程讨论业务功能；等项目线程或归档线程。 |
| remaining-projects-inventory | 项目盘点 | projects | `parked` | 2026-05-03 | 已完成项目生命周期盘点，并完成 C9-C16 审查。 | 后续是否升级 portfolio 仍需多项目证据。 | 暂停项目产物处理，先收口 proposal 临时材料和台账。 |
| skill-harness-candidate-pruning | 能力治理 | governance | `parked` | 2026-05-02 | 复核 skill / harness / plugin candidate 是否仍必要。 | 当前主线先处理剩余材料和项目产物。 | 等 proposal、AI raw、archive 和项目盘点后再做。 |

## 待用户拍板项

| 事项 | 我的建议 | 不同选择的效果 |
|---|---|---|
| 是否接受例外审批制试运行 | 接受 | 用户不再每一步把关；L1 自动、L2 汇总、L3 单独审批。 |
| 是否扩大 L1 自动处理范围 | 暂不扩大 | 先观察判断一致率，避免自动化越界。 |
| 17 个 proposal 决策记录是否已收口 | 已完成 `09de668` | 长期治理判断已入库；不代表 stable policy。 |
| 16 个临时 proposal 是否进入 30 天删除候选 | 建议进入候选，不马上删 | 能减少 proposal 噪音，同时保留二次审批。 |
| 是否创建 5 天停滞自动提醒 | 暂不创建 | 先用台账试运行更稳；直接自动化可能误报。 |
| 是否把线程台账转 stable 文档 | 暂不转 | 先观察 1-2 周，避免过早固化。 |
| `ai-intel/raw/*` 怎么处理 | 不提交 raw，先做生命周期收口清单 | 保留复核能力，同时不污染仓库。 |
| `docs/archive/notes/*` 怎么处理 | `答辩.md` 随 `graduation-defense-agent` closeout；其它继续单独审 | 避免 archive 策略被未审历史材料绑死。 |
| 其它 `projects/*` 怎么处理 | 暂停新处理，等临时 proposal 收口后再继续 | 避免项目产物和治理收口互相污染。 |
| 架构自我管理机制怎么落地 | 先做 proposal，不直接 stable | 先明确上位机制和部门制流转，避免后续继续靠单点修补；不直接 stable 可降低过早固化风险。 |

## 经验候选

| 经验 | 分类 | 当前处理 |
|---|---|---|
| 先搞清楚主线任务，支线任务不能影响主线。 | 长期规则，已写入 `agent.md` | 已稳定。 |
| 线程 5 天未推进应自动总结并向用户汇报。 | 长期候选 | 已写入 proposal，先试运行台账。 |
| 项目偏好不能自动跨项目复用。 | 长期规则方向 | 已在 memory-cache 和偏好治理中落实。 |
| PRD 需要页面说明、页面跳转关系、原型图层；PNG / HTML 后置。 | 长期规则方向 | A1 已稳定。 |
| 报告默认中文。 | 长期偏好方向 | 后续所有报告继续中文。 |

## 防上下文丢失续接清单

如果上下文中断或换线程，先从这里恢复主线。当前最高优先级不是继续新增工具，而是把上位机制和剩余治理任务按生命周期推进。

### 1. 最高优先级：架构自我管理机制 proposal

目标：把用户最近确认的思想写成一份可审核 proposal，不直接 stable。

文件建议：

```text
docs/proposals/architecture_self_management_system.md
```

必须包含：

- 架构是核心资产，skill / harness / plugin / automation 只是工具。
- 用户负责定大方向和高风险拍板，架构中枢负责拆解和调度。
- 部门制执行：产品、开发、质量、治理、学习、归档、情报、瘦身。
- 输入自我流转：demo / 项目 / 错误 / 反馈 -> 识别类型 -> 拆小任务 -> 分配部门 -> 检查 -> closeout -> architecture inbox -> promotion / pruning。
- 探索期可以重，稳定期必须最小可行。
- 每个 token、文件、检查、skill、harness 都必须证明价值。
- 低风险动作可执行，高风险动作必须上报用户。
- 例外审批制：L1 自动处理，L2 汇总审批，L3 单独审批。
- 禁止任务漂移：支线必须服务主线。
- 不新增 skill / harness / workflow / automation。

当前动作：

- proposal 已生成并补入例外审批制。
- 不改 `agent.md`、`docs/operating_model.md`、workflow、harness、registry。
- 先按 L1 / L2 / L3 试运行，再决定是否进入 stable policy。

### 2. C 批项目产物剩余任务

| 顺序 | 事项 | 当前状态 | 下一步最小动作 |
|---|---|---|---|
| C11 | `taxi-hailing-prd-test` golden sample candidate | 已提交 | `852a2d5 Add deidentified PRD structure golden case`；只提交 golden case + regression 6 个文件，未提交项目产物或 proposal。 |
| C12 | `ai-collaboration-efficiency-platform` | 已完成 L1 刷新审查 | 旧 closeout 只扫到 1 个文件；已用临时目录刷新，确认项目是复杂 AI / Skill 治理产品交付链路证据，暂不提交项目产物、不归档。 |
| C13 | `prompt-optimization-workbench` | 已完成 L1 审查 | 判断为低证据 HTML 原型项目，项目内保留，暂不提交、不归档、不提炼 stable。 |
| C14 | `santoip-ai-brand-video` | 已完成 L1 审查 | 判断为低证据业务 HTML 原型项目，项目内保留，暂不提交、不归档、不提炼 stable。 |
| C15 | `temp-generated-project` | 已完成 L1 审查 | 判断为临时项目隔离证据，暂不提交、不删除；后续可进 30 天删除候选。 |
| C16 | `projects/_archives` 和项目 zip | 已完成 L1 审查 | 已识别 12 个压缩包，区分 archive evidence、HTML prototype zip、project package、duplicate candidate；不移动、不删除、不提交 zip。 |

已完成但未提交项目产物：

- `graduation-defense-agent`：C9 已审查，`答辩.md` 是项目原始输入证据候选。
- `jiaxiaoqian-ai-invest-research`：C10 已审查，是复杂 AI / 金融投研高价值项目证据，不提交项目、不升级 golden sample。

### 3. 非项目剩余任务

| 事项 | 当前状态 | 下一步最小动作 |
|---|---|---|
| `ai-intel/raw/2026-04-30/` | 已有生命周期处置材料，仍未提交 | raw 不提交；后续确认是否进入 30 天后删除候选。 |
| `docs/archive/root-files/Remod开发.md` | 未审历史开发治理笔记 | 判断是否已有经验被吸收；如有价值只提炼中文总结，不按原文推动新增 skill / harness。 |
| `docs/proposals/*` 临时材料 | 已分类为决策记录 / 临时 staging / 已覆盖 | 后续只提交有价值决策记录；临时材料进入 30 天后删除候选。 |
| skill / harness / plugin candidate 瘦身 | 等项目和 proposal 处理后再做 | 按 promotion / pruning gate 复核，非必要不转 stable。 |
| 线程 5 天停滞监督 | proposal 已有，台账试运行 | 观察 1-2 周后再决定是否创建自动化提醒。 |
| 本轮治理总验收报告 | 未生成 | 等 C 批、archive、candidate 瘦身关键剩余项处理后输出。 |

### 4. 继续禁止事项

- 不删除文件。
- 不归档项目。
- 不清空 `memory-cache/`。
- 不提交 `projects/*`。
- 不提交 `ai-intel/raw/*`。
- 不把 project feedback 自动写入长期记忆。
- 不把 candidate plugin / skill / harness 自动转 stable。
- 不新增 skill / harness / workflow / automation。
- 不 push / PR。

### 5. 需要用户拍板的高风险事项

| 拍板项 | 默认建议 |
|---|---|
| 架构自我管理机制是否转 stable | 先 proposal 试运行，不直接 stable。 |
| 例外审批制是否正式 stable | 先试运行，不直接 stable。 |
| 低风险自动化是否开启 | 先台账人工监督，观察一致率后再逐步放权。 |
| 项目是否归档或删除候选 | 逐项目 closeout 后再决定。 |
| raw / zip / 临时 proposal 是否 30 天后删除候选 | 先列清单，不直接删除。 |
| 任何长期记忆写入 | 必须逐条批准。 |
| 新增或稳定 skill / harness | 默认不新增，必须多项目证据 + 替代方案比较 + 验证通过 + 用户批准。 |

## 推进顺序

建议接下来按这个顺序，减少切换成本：

1. 用户审核 `docs/proposals/architecture_self_management_system.md`，当前只试运行，不转 stable。
2. 按例外审批制推进：L1 事项自动处理并汇报，L2 事项形成批量审批包，L3 事项单独问你。
3. 单独提交台账收口：`docs/thread_registry.md` 与 `docs/proposals/remaining_proposal_audit_materials_disposition.md`。
4. 处理剩余 18 个未跟踪 proposal：16 个临时材料进入 30 天候选，2 个已覆盖旧审查暂不提炼。
5. `projects/_archives` 和项目 zip 统一归档策略。
6. `ai-intel/raw/*` 30 天删除候选确认。
7. `Remod开发.md` 是否提炼或清理候选。
8. skill / harness / plugin candidate 瘦身复盘。
9. 输出本轮治理修复总验收报告。
10. 观察线程台账 1-2 周，再决定是否创建 5 天停滞提醒自动化。

## 本轮不执行

- 不创建自动化。
- 不归档线程。
- 不删除文件。
- 不清空项目缓存。
- 不写长期记忆。
- 不修改 skill、harness、workflow、registry、pipeline。
- 不 staging / commit / push / PR。
