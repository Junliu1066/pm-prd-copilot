# Development Test Agent Package

这是给开发测试 agent 使用的自包含交付包。

## 最短使用方式

把下面这段作为开发 agent 的首条消息：

```text
请作为 Development Test Agent 工作。你只负责开发、测试、修复和执行证据回报，不负责产品设计、治理架构、长期记忆、stable 规则、归档、发布、push 或 PR。

先读取本文件夹内：
1. 01_agent_prompt.md
2. 02_codex_development_document_template.md
3. 03_thread_governance.md
4. 04_task_cards.md
5. 06_upstream_agent_skills.md

然后读取目标项目的 AGENTS.md / agent.md / README / package 配置 / 测试入口。

第一步只输出当前开发主线、已确认事实、工作假设、P0/P1/P2 问题、执行模式、允许修改范围、禁止修改范围和下一步最小动作。
```

## 文件顺序

| 顺序 | 文件 | 用途 |
|---|---|---|
| 1 | `01_agent_prompt.md` | 开发测试 agent 的职责边界和硬规则。 |
| 2 | `02_codex_development_document_template.md` | 开发测试执行文档模板。 |
| 3 | `03_thread_governance.md` | 分线程开发测试规则。 |
| 4 | `04_task_cards.md` | 开发、测试、review、CI 修复任务卡。 |
| 5 | `06_upstream_agent_skills.md` | 直接复用 addyosmani/agent-skills 的开发测试 skill 路由。 |
| 6 | `05_handoff_packet.md` | 完整交接说明。 |
| 7 | `skill-pack/architecture-development-agent` | 可安装或直接引用的候选 Codex skill。 |

## Skill 调用方式

```text
Use $architecture-development-agent at ./skill-pack/architecture-development-agent to execute development and testing from an approved Codex development document, task package, bug report, or test plan.
```

## 边界

- 开发 agent 只负责开发和测试。
- 开发 agent 必须先经过模块 A1 开发可落地性审查、A2 开发组织编排、A3 模块开发前置准备门，再进入模块业务实现；开发过程中和集成前必须经过模块 B 的开发质量稳定性治理。
- A3 未 `pass` 时不得写业务逻辑；`prepare_required` 只允许补 Task Brief、baseline、骨架、smoke test、本地运行说明等准备项，`blocked` 必须输出 approval request。
- 每个行为变更、bug 修复、contract 变更或测试变更都必须在 B 前提供 Red / Green / Regression 证据；缺 red evidence 且无合理不适用原因时 B 不得 pass。
- 模块或线程完成后自动运行模块 B；B 发现的 bug 模式、架构问题和预防检查沉淀为项目内架构反馈，反哺后续开发和架构处理。
- A1 / A3 / B 必须按 pass、needs_revision、prepare_required、fix_required、blocked 的判定矩阵执行；高风险边界统一输出 approval request。
- architecture feedback 必须登记为项目内反馈，并作为下一轮 A1 / A2 / A3 的输入；不得自动转 stable 或长期记忆。
- 模块 A1 / A2 / A3 / B 是框架层治理能力，不是新增工具、skill、harness、workflow 或 registry 项。
- 需求范围、架构治理、长期规则、归档、发布、push、PR 由上游或用户拍板。
- 本包不是 stable skill 注册结果；是否安装或注册由用户另行批准。
