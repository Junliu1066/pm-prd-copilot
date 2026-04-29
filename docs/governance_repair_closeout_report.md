# 治理架构修复总验收报告

- 日期：2026-04-29
- 状态：用户已确认主要治理方向，仍需逐项执行审核
- 范围：本轮治理架构遗漏问题修复、PRD 主链路收紧、项目 closeout 扫描、清理前审计和长期偏好记录
- 规则：本报告是验收和拍板材料，不批准归档、删除、移动、提交、推送、PR、plugin 转正、skill 转正、harness 转正或长期规则自动生效。

## 总结判断

本轮治理修复已经完成主链路收口：PRD 输出退化、workflow/action/artifact 漂移、pipeline 绕过审批、harness 写文件边界、candidate 能力膨胀、项目 closeout 缺口、root 删除项状态不清，都已经有对应修复或审核材料。

用户已确认本轮主要治理方向：

- 6 个 candidate plugin 暂不转 stable，继续保持 candidate / detachable。
- 5 个必要检查稳定保留。
- `taxi-hailing-prd-test/02_prd.final.md` 暂作 golden sample 候选；后续收集多篇 PRD 后再迭代。
- 0-1 PRD 收件箱条目逐条批准。
- `fitness-app-mvp` 项目偏好缓存先保留，归档前对齐。
- root 删除项接受 root 删除候选，但保留 canonical / archive。
- 历史 PRD 回扫延后。
- 当前工作区后续按分区提交。

当前还不能算“全部结束”，因为归档、删除、提交、长期记忆、stable 转正和项目经验长期化仍需要后续精确审批。

## 已完成

| 模块 | 当前状态 | 验收说明 |
|---|---|---|
| PRD 主链路 | 已修复 | PRD 默认包含页面说明、页面跳转关系、原型图层；图表放对应章节；非 AI 项目不默认输出 AI 模型选型。 |
| Pipeline 默认治理 | 已修复 | `run_pipeline.py` 默认 governed；只有显式 `--fast-draft` 才允许草稿路径。 |
| Workflow / action / artifact 合同 | 已修复 | workflow 动作、artifact 注册、harness 检查已补齐漂移检查。 |
| Harness 读写边界 | 已修复 | 默认 `--check-only`；写报告必须显式 `--write-report`，日常检查不写项目文件。 |
| 新增能力最小化审计 | 已完成 | 6 个 plugin suite 保持 candidate / detachable；不默认转 stable。 |
| 必要检查稳定化 | 已完成候选治理 | `eval_suite`、`real_output_eval`、`skill_generalization`、`prototype_preview_gate`、`external_redaction` 已作为最小保护层记录。 |
| B 包脚本泛化 | 已完成 | 外部分发包从项目硬编码改为通用打包方向，并有 redaction 检查保护。 |
| 项目偏好机制 | 已完成边界 | 只允许项目内使用；归档前对齐；长期记忆必须单项批准。 |
| 通用架构收件箱 | 已完成 | `0-1 普通业务 PRD 质量反馈` 已抽象，不用单个测试项目命名长期规则。 |
| Root 删除项精确清单 | 已完成 | 4 个 root 删除项已有 canonical/archive/审批状态记录。 |
| 所有项目 closeout 扫描 | 已完成 | 8 个项目均已生成 closeout 五件套，并写入项目扫描索引。 |
| 长期偏好 | 已写入 | 已记录“长期稳定可靠优先；能用一行清晰代码解决，就不扩展成多行、额外抽象或新增组件”。 |

## 关键产物

| 产物 | 用途 | 审核重点 |
|---|---|---|
| `docs/workspace_change_partition.md` | 当前混乱工作区分区、root 删除项、项目 closeout 索引 | 后续 staging、归档、清理前先看它。 |
| `docs/proposals/capability_minimality_review.md` | 新增 plugin / skill / harness / eval / script 最小化审计 | 防止继续膨胀。 |
| `docs/architecture-inbox/zero_to_one_prd_quality_feedback.md` | 0-1 普通业务 PRD 质量反馈收件箱 | 只作为候选知识，不直接改稳定规则。 |
| `projects/*/closeout/` | 每个项目的收口预览包 | 归档前审核项目经验、清理候选、偏好缓存处置。 |
| `pm-prd-copilot/memory/user_preferences.md` | 已批准长期偏好 | 只收录你明确批准的长期偏好。 |

## 项目状态

| 项目 | 当前判断 | 建议 |
|---|---|---|
| `demo-project` | active test fixture | 保留为 regression / governance fixture，不建议归档，除非先有替代 fixture。 |
| `fitness-app-mvp` | active / closeout candidate | 有项目偏好缓存，归档前必须先审核 preference disposition。 |
| `taxi-hailing-prd-test` | closeout candidate | 只作为 0-1 PRD 质量证据；是否升级 golden sample 需你确认。 |
| `ai-collaboration-efficiency-platform` | closeout candidate | 只有历史 PRD 证据，建议你决定保留还是归档候选。 |
| `graduation-defense-agent` | closeout candidate | 有 AI、交付、Codex 开发和原型材料，建议先审核完整包再决定归档。 |
| `jiaxiaoqian-ai-invest-research` | active | AI-heavy 项目，仍按 active 处理；旧口径只列历史回扫候选。 |
| `prompt-optimization-workbench` | closeout candidate | 有 HTML 原型包，建议审核后再决定是否归档。 |
| `santoip-ai-brand-video` | closeout candidate | 有 HTML 原型包，建议审核后再决定是否归档。 |

## 已确认方向

| 决策项 | 已确认方向 | 后续执行边界 |
|---|---|---|
| 6 个 candidate plugin 是否转 stable | 暂不转 | 保持 candidate / detachable；不得默认进主链路。 |
| 5 个必要检查是否进入稳定架构 | 稳定保留 | 作为最小保护层继续保留，后续新增检查仍需单独审批。 |
| `taxi-hailing-prd-test/02_prd.final.md` 是否升级 golden sample | 先作为候选 | 后续收集多篇 PRD 后再抽象、脱敏、迭代。 |
| 0-1 PRD 收件箱哪些条目进入模板/prompt/regression | 逐条批准 | 不把收件箱整包长期化。 |
| `fitness-app-mvp` 偏好缓存如何处理 | 先保留，归档前对齐 | 不跨项目复用；长期记忆仍需单项批准。 |
| root 删除项是否接受删除状态 | 接受 root 删除候选，保留 canonical / archive | 不硬删除 archive；30 天后仍需精确清单审批。 |
| 历史 PRD 是否回扫旧口径 | 延后 | 架构稳定后，只选活跃项目回扫。 |
| 当前工作区如何提交 | 分区提交 | 稳定架构、项目产物、归档候选、实验能力分开处理。 |

## 仍需后续拍板

| 待执行事项 | 为什么还需要你确认 |
|---|---|
| 哪些项目进入归档审核线程 | closeout 是审核材料，不等于归档许可。 |
| 哪些 root archive 30 天后可硬删除 | 当前只接受 root 删除候选，不接受硬删除。 |
| 哪些 0-1 PRD 收件箱条目进入 prompt / 模板 / regression | 已确认逐条批准，不能整包长期化。 |
| golden sample portfolio 的正式样例 | 需要多篇 PRD 对比后再定。 |
| 工作区具体提交批次 | 分区提交方向已确认，但每批提交范围仍需审核。 |

## 当前禁止动作

- 不归档项目目录。
- 不删除项目文件。
- 不移动到 `projects/_archives`。
- 不清空项目偏好缓存。
- 不把项目经验直接写入长期记忆。
- 不把 candidate plugin 转 stable。
- 不新增 skill。
- 不新增 harness。
- 不恢复或硬删除 root 历史文件。
- 不 `git add`、commit、push、PR。

## 剩余风险

| 风险 | 当前控制 | 后续动作 |
|---|---|---|
| 工作区仍然很大，容易混提交 | 已有分区文档 | 后续必须按分区拆提交或拆 PR。 |
| candidate plugin 可见但可能被误用 | 已标 candidate / non-stable / requires review | 继续用 regression 检查 marketplace 标识。 |
| 历史项目仍有旧 PRD 口径 | 已列 history sweep candidate | 等架构稳定后按项目回扫，不批量改。 |
| 项目 closeout 生成了大量报告 | 已明确只是审核材料 | 你审核后再决定归档、保留或删除候选。 |
| 偏好缓存可能污染长期规则 | 已限制项目内使用 | 归档时逐项决定清除、保留为项目档案或进入长期记忆。 |

## 建议下一步

1. 按已确认方向，形成长期治理生命周期方案草案。
2. 用定时周报做人工监督和判断校准，先跑 2-4 周。
3. 继续逐条处理 0-1 PRD 收件箱，不整包长期化。
4. 后续收集多篇 PRD，建立 golden sample portfolio。
5. 最后再做分区提交方案，避免把架构修复和项目产物混提交。

## 验证记录

最近一轮验证均已通过：

- `git diff --check`
- `python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict`
- `python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency`

Harness 结果显示：`No project files written. Use --write-report to refresh harness reports.`

## 自查记录

第一轮自查：已确认本轮修复覆盖 PRD、pipeline、workflow/action/artifact、harness、candidate 能力、B 包、项目偏好、closeout、root 删除清单和架构收件箱。

第二轮自查：已确认仍未执行归档、删除、移动、提交、push、PR、skill 新增、harness 新增、长期规则自动升级。

## 结论

治理架构主链路已经从“容易遗漏、容易膨胀、容易绕过治理”修到“有门禁、有候选层、有 closeout、有清理前审计、有用户拍板清单”的状态。

接下来不是继续盲修，而是你按本报告逐项拍板：哪些进入稳定架构，哪些保持候选，哪些归档，哪些 30 天后再删。
