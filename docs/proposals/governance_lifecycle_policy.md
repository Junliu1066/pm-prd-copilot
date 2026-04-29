# 长期治理生命周期方案草案

- 日期：2026-04-29
- 状态：proposal，尚未转为 stable policy
- 目标：把治理从临时判断变成可监督、可校准、可逐步自动化的生命周期机制
- 适用范围：PM Skill 治理架构、PRD 生成链路、candidate plugin / skill / harness / eval、项目 closeout、架构收件箱、归档和删除候选
- 原则：
  - 如无必要，不增 skill，不增 harness。
  - 长期稳定可靠优先；能用一行清晰代码解决，就不扩展成多行、额外抽象或新增组件。
  - 任何长期记忆、stable 转正、删除、归档、提交、模型/成本变更、外部发布，都必须人工审批。

## 总体模型

长期治理采用六层生命周期：

```text
Stable Core
-> Candidate Sandbox
-> Architecture Inbox
-> Promotion Gate
-> Pruning Gate
-> Supervision Calibration
```

这套机制的目的不是增加流程，而是把“什么时候稳定、什么时候候选、什么时候归档、什么时候必须人工审批”固定下来，减少遗漏和误扩张。

## 1. Stable Core

Stable Core 只放长期必要、已经证明价值、且维护成本合理的核心能力。

当前可进入或保持 Stable Core 的方向：

- PRD 主链路：页面说明、页面跳转关系、原型图层、图表放对应章节、非 AI 项目不默认 AI 模型选型。
- Pipeline 默认 governed，`--fast-draft` 才允许草稿路径。
- Harness 默认 `--check-only`，写报告必须显式 `--write-report`。
- 5 个必要检查：`eval_suite`、`real_output_eval`、`skill_generalization`、`prototype_preview_gate`、`external_redaction`。
- closeout 机制：清理前必须总结、反思、沉淀、归档候选和偏好缓存处置。
- B 包 redaction 和外部分发边界。

Stable Core 的边界：

- 不因为“有用”就扩大成默认主流程。
- 不把单项目经验直接写成长期规则。
- 不把 candidate plugin 自动转 stable。

## 2. Candidate Sandbox

Candidate Sandbox 用来承接探索能力。它允许试，但不允许默认稳定。

默认进入 Candidate Sandbox 的内容：

- 新 plugin suite。
- 新 skill。
- 新 harness checker。
- UI style / prototype / AI solution / delivery planning 扩展能力。
- 只被单个项目证明过的脚本、模板或流程。

Candidate Sandbox 的使用规则：

- 必须显式标记 `candidate`、`detachable`、`requires review` 或同等含义。
- 只能在项目明确需要时调用。
- 不得默认进入 PRD 主链路。
- 不得因为存在于 marketplace 就被当成 stable。
- 不得绕过用户审批写长期规则。

当前确认方向：

- 6 个 candidate plugin 继续保持 candidate / detachable，不转 stable。

## 3. Architecture Inbox

Architecture Inbox 用来接收项目反哺，但不直接改变架构。

进入 Inbox 的内容：

- 项目 closeout 发现的可复用问题。
- PRD 质量反馈。
- 用户纠错中可能适合泛化的经验。
- AI 情报中可能优化治理架构的信号。
- 版本或模型更新后发现的风险。

Inbox 条目必须包含：

- 项目证据。
- 通用建议。
- 待拍板动作。
- 是否适合进入 prompt、模板、regression、real-output eval、长期记忆或 stable policy。

当前确认方向：

- 0-1 PRD 收件箱逐条批准。
- 单个测试项目只能作为证据来源，不能作为长期规则命名。

## 4. Promotion Gate

Promotion Gate 用来判断候选能力能否进入 Stable Core。

转 stable 必须同时满足：

- 至少 2-3 个项目证明有用，或用户明确指定为长期必要能力。
- 已比较替代方案，确认不能用更小的文档、模板、脚本参数或现有检查解决。
- 不违反“如无必要，不增 skill / harness”。
- 有清楚 owner、输入、输出、写入边界和禁止事项。
- regression / harness / real-output eval 通过。
- 有回退方案。
- 用户明确批准。

不满足时：

- 保持 candidate。
- 转入 architecture inbox。
- 归档为候选。
- 或列入 30 天后删除候选。

当前确认方向：

- `taxi-hailing-prd-test/02_prd.final.md` 先作为 golden sample 候选。
- 后续收集多篇 PRD 后，再建立 golden sample portfolio。

## 5. Pruning Gate

Pruning Gate 用来防止架构越堆越大。

触发条件：

- 模型更新。
- 版本更新。
- SDK / API / 价格 / 规则变化。
- 重大架构调整。
- 周期性治理校准发现重复能力。

检查对象：

- skill。
- harness。
- plugin。
- workflow stage。
- registry 项。
- automation。
- template。
- package path。
- 项目产物。

输出分类：

- `keep_in_architecture`
- `keep_detachable_candidate`
- `defer_not_stable`
- `archive_candidate`
- `delete_after_30_days_candidate`

当前确认方向：

- 历史 PRD 回扫延后。
- root 删除接受候选，但保留 canonical / archive。
- 任何硬删除仍需 30 天窗口和精确审批。

## 6. Supervision Calibration

Supervision Calibration 用来逐步建立自动化信任。

阶段 1：人工监督

- 定时周报只检查、汇总、建议。
- 不自动修改长期规则。
- 不自动归档、删除、提交。
- 输出每个待决策项的选项、结果、风险和建议。

阶段 2：半自动

- 当连续几轮判断与用户一致后，允许低风险草案自动生成。
- 低风险动作包括：更新收件箱草案、生成 closeout 预览、刷新索引、跑 check-only 检查。
- 仍不允许自动 stable 转正、长期记忆写入、删除、归档、提交。

阶段 3：低风险授权自动

- 只对已验证稳定、可回退、低影响的动作放权。
- 每次自动动作仍需要报告。
- 高风险动作永久保留人工审批。

建议校准指标：

- 判断一致率：建议和用户最终决定是否一致。
- 误报率：不重要事项被汇报的比例。
- 漏报率：应由用户拍板但未汇报的比例。
- 自动化候选：可逐步放权的低风险动作清单。

## 永久人工审批项

以下事项不得自动执行：

- 长期记忆写入。
- stable 转正。
- 删除文件或数据。
- 归档项目。
- git add / commit / push / PR。
- 模型、模型供应商、成本策略或外部数据源变更。
- 外部发布或 B 包正式交付。
- 清空项目偏好缓存。
- 把项目经验写入长期规则。

## 当前执行建议

1. 保持本方案为 proposal，不直接转 stable policy。
2. 用周报跑 2-4 周，观察判断一致率、误报率、漏报率。
3. 只把低风险动作作为未来半自动候选。
4. 高风险动作永久保留人工审批。
5. 后续如要转 stable policy，必须另出推荐方案并由用户明确批准。

## 本方案当前不执行

- 不新增 skill。
- 不新增 harness。
- 不新增 workflow stage。
- 不新增 plugin。
- 不归档项目。
- 不删除文件。
- 不移动项目目录。
- 不提交。
- 不写入长期记忆。
- 不把本方案直接设为 stable policy。
