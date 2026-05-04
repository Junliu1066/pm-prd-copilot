# 治理架构修复总验收报告

- 日期：2026-05-04
- 状态：稳定核心已可用，剩余主要是项目产物、临时材料和归档候选的收口
- 主线目标：建设长期稳定、可监督、可迭代、能自我收敛的治理架构；skill、harness、plugin、automation 都是工具层，必须服从架构。
- 本报告性质：验收和后续处理地图，不自动批准删除、归档、push、PR、长期记忆写入、candidate 转 stable 或项目经验长期化。

## 一句话结论

本轮治理修复已经从“补漏洞”进入“收口验收”阶段。PRD 主链路、pipeline 门禁、workflow 合同、harness 读写边界、必要检查、候选能力边界、长期偏好、任务漂移约束、root 清理证据、AI 情报候选区和项目产物分区都已落地。现在还没结束的不是主链路，而是剩余材料如何提交、保留、归档或 30 天后删除。

## 已落地的架构效果

| 方向 | 当前效果 | 代表提交 |
|---|---|---|
| PRD 主链路 | PRD 默认有页面说明、页面跳转关系、原型图层；图表放对应章节；非 AI 项目不写 AI 模型选型。 | `30b53f9` |
| Pipeline 治理门禁 | 默认 governed；只有显式 `--fast-draft` 才走草稿路径，避免实际管线绕过 workflow。 | `e66ead6` |
| 必要检查基线 | eval、真实输出、泛化、原型预览、外部分发脱敏等最小保护层已建立。 | `9f11949` |
| 交付和 closeout 边界 | B 包、closeout、Codex 开发文档、项目偏好缓存的边界已收紧。 | `36c117d`、`49b4784` |
| 核心治理文档 | 架构地图、运行规则、仓库入口、任务漂移约束、线程登记和生命周期记录已成体系。 | `da91f15`、`1e74cd0`、`203d2ad` |
| 教学 / steward / 长期偏好 | 已明确长期稳定优先、中文报告、项目偏好不得跨项目、长期记忆需逐条批准。 | `6320697`、`6f02be7`、`bfbba61`、`9816c87` |
| Candidate 能力治理 | 候选 plugin、UI 风格选择器、按需 harness checker 已补齐，但不默认转 stable。 | `a34e821`、`dfff924`、`e6837d0` |
| AI 情报候选区 | AI 情报有候选数据区、提取质量、reviewed evidence 和 raw 保留边界。 | `241e5b5`、`608d94d`、`d555ce4`、`207eb50` |
| Root 清理 | 4 个 root 历史文件已正式移出根目录，保留 archive evidence，不做硬删除。 | `08f9876` |
| 项目产物分区 | demo fixture、fitness 产物、临时 proposal、错误报告等已拆批次处理。 | `cf8af9a`、`c5397c8`、`8c21c6f`、`fe34f77` |

## 当前可用性判断

现在可以继续用这套架构输出 PRD、开发文档和项目材料，但建议按线程隔离：

- 新项目工作：新线程做，不混入治理收口线程。
- 治理收口：继续在本线程处理提交、清理、归档候选。
- 项目产物：按 C 批逐项目审，不混入稳定核心。
- 临时材料：按 30 天候选和保留证据分开处理。

这能保证你一边继续干活，一边不影响治理修复。

## 已提交批次

| 批次 | 已完成内容 | 当前状态 |
|---|---|---|
| A1 | PRD 主链路输出合同 | 已提交 |
| A2 | pipeline / workflow / harness 治理合同 | 已提交 |
| A3 | 5 个必要检查和 eval 基线 | 已提交 |
| A4 | 交付、closeout、B 包、开发文档边界 | 已提交核心边界；部分真实项目材料仍按项目批次处理 |
| B1-B4 | 核心治理文档、proposal 审计、教学/steward、错误报告 | 已分批提交 |
| B5 | automation / AI intel / candidate 能力边界 | 已分批提交，candidate 不转 stable |
| D1-D3 | 候选插件、按需 checker、UI 风格选择器 | 已提交候选能力，不进入默认主链路 |
| E | root/archive 最小证据 | 已提交，硬删除未批准 |
| R1-R4 | 剩余轻量开发文档、审计记录、错误报告、临时 proposal 处置 | 已提交 |

## 当前剩余未收口项

| 类别 | 现状 | 建议 |
|---|---|---|
| `projects/fitness-app-mvp` 修改项 | 仍有分析结果、project_state、run trace/report 未提交 | 作为 fitness 项目批次单独审，不混入治理核心。 |
| 其他 `projects/*` 未跟踪项目 | 多个项目目录仍是项目产物或归档候选 | 按 C 批逐项目处理，先判断 active / closeout / archive candidate。 |
| `memory-cache/` | 项目偏好缓存仍未提交 | 项目内保留，归档前对齐，不写长期记忆。 |
| `ai-intel/raw/2026-04-30/` | raw 网页证据未提交 | 保持本地候选，验收后决定归档候选或 30 天删除候选。 |
| `docs/archive/notes/` 和额外 root archive | 仍有额外历史材料未提交 | 暂缓，后续按 archive 补充证据批次单独审。 |
| 临时 `docs/proposals/*` | 已记录为生命周期处置候选 | 不提交本体，30 天后按清单复核删除或保留。 |

## 还需要你拍板的功能性事项

| 决策 | 选项效果 | 我的建议 |
|---|---|---|
| fitness 项目产物怎么处理 | 提交能保留项目证据；暂缓能减少噪音；归档需先 closeout | 先做 fitness 单项目审查包，再决定提交哪些。 |
| `memory-cache/` 是否提交 | 提交会污染长期规则边界；不提交会保持项目内连续性 | 不提交，归档前再逐条处置。 |
| AI raw 是否长期保留 | 保留 raw 可追溯网页；不提交 raw 可避免仓库膨胀 | 不进主仓提交，先列 30 天候选。 |
| 其他项目是否归档 | 归档能瘦身；过早归档可能丢上下文 | 先按项目 closeout 报告逐个拍板。 |
| 临时 proposal 是否硬删除 | 删除能瘦身；过早删除会丢审计证据 | 已记录 30 天候选，到期再统一复核。 |
| candidate 能力是否转 stable | 转 stable 会提高默认覆盖；也会增加维护成本 | 继续 candidate，至少再跑真实项目验证。 |

## 长治久安机制已经嵌入的部分

| 机制 | 作用 |
|---|---|
| 主线任务识别 | 防止从治理修复跑偏到项目功能细节。 |
| Stable Core / Candidate Sandbox | 稳定核心和候选能力分层，避免工具膨胀。 |
| Architecture Inbox | 项目经验先进入候选收件箱，不直接污染长期规则。 |
| Promotion Gate | candidate 转 stable 需要多项目证据、替代方案比较、回归验证和你批准。 |
| Pruning Gate | 版本、模型、架构大改后做瘦身审计，删除不必要 skill/harness/plugin。 |
| Thread Registry | 记录线程和搁置事项，减少上下文稀释导致遗忘。 |
| 30 天候选机制 | 临时 proposal、raw、archive 等先记录，再定期复核，避免马上删也避免永久堆积。 |

## 仍需补强的长治久安点

| 待补强点 | 为什么需要 | 建议顺序 |
|---|---|---|
| 搁置线程 5 天提醒 | 防止重要支线被上下文稀释 | 下一个治理机制批次处理。 |
| 定时汇报的解决方案建议 | 让汇报不是流水账，而是可拍板材料 | 和线程提醒一起做。 |
| 项目 closeout 自动索引 | 归档前自动汇总经验、错误、偏好、清理候选 | 等 fitness 批次处理后抽象。 |
| 自动化授权分级 | 低风险自动处理，高风险集中给你拍板 | 需要先跑 2-4 周校准判断一致率。 |

## 当前禁止动作

除非你单独批准，仍然禁止：

- push / PR。
- 删除、恢复、移动、归档项目目录。
- 清空 `memory-cache/`。
- 把项目偏好写入长期记忆。
- 把 candidate plugin / skill / harness 转 stable。
- 把临时 proposal 本体整批提交。
- 提交 `ai-intel/raw/`。

## 建议下一步

建议下一步做 **fitness 项目产物单项目审查包**。原因是当前唯一已修改的 tracked 项目文件集中在 `projects/fitness-app-mvp`，它是工作区最大的剩余噪音源。先把它判断清楚，后面项目批次和 memory-cache 处理都会顺很多。

备选下一步是做 **搁置线程 5 天提醒机制方案**。这个更偏上位机制，也很重要，但它会新增或调整自动化规则，建议在当前项目产物噪音先收口后做。

## 验证记录

最近一轮 R4 提交前验证均已通过：

- `git diff --check`
- `python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict`
- `python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency`

Harness 结果显示：`No project files written. Use --write-report to refresh harness reports.`

## 结论

治理架构主链路已经可以稳定使用。剩下的工作重点不是继续加 skill 或 harness，而是把项目产物、缓存、raw、archive 和临时审计材料按生命周期收口。只要后续继续按“稳定核心优先、候选层隔离、项目经验先入收件箱、30 天后再清理”的机制推进，这套架构就能从人工把关逐步过渡到低风险自动处理、高风险集中拍板。
