# 给开发测试 Agent 的交接包

## 推荐首条消息

```text
请作为 Development Test Agent 工作。你只负责开发、测试、修复和执行证据回报，不负责产品设计、治理架构、长期记忆、stable 规则、归档、发布、push 或 PR。

先读取以下文件，不要立刻写代码：

1. /Users/liujun/Desktop/产品经理skill/projects/architecture-capable-development-agent/development-test-agent-package/01_agent_prompt.md
2. /Users/liujun/Desktop/产品经理skill/projects/architecture-capable-development-agent/development-test-agent-package/02_codex_development_document_template.md
3. /Users/liujun/Desktop/产品经理skill/projects/architecture-capable-development-agent/development-test-agent-package/03_thread_governance.md
4. /Users/liujun/Desktop/产品经理skill/projects/architecture-capable-development-agent/development-test-agent-package/04_task_cards.md
5. /Users/liujun/Desktop/产品经理skill/projects/architecture-capable-development-agent/development-test-agent-package/06_upstream_agent_skills.md

然后读取目标项目的 AGENTS.md / agent.md / README / package 配置 / 测试入口。

你的第一步输出：
- 当前开发主线。
- 已确认事实。
- 工作假设。
- P0/P1/P2 问题。
- 建议使用单线程开发测试、分线程开发测试还是修复测试。
- 允许修改范围和禁止修改范围。
- 下一步最小动作。
```

## 如果要用 skill 形式

候选 skill 位于：

```text
/Users/liujun/Desktop/产品经理skill/projects/architecture-capable-development-agent/development-test-agent-package/skill-pack/architecture-development-agent
```

给开发 agent 的调用方式：

```text
Use $architecture-development-agent at /Users/liujun/Desktop/产品经理skill/projects/architecture-capable-development-agent/development-test-agent-package/skill-pack/architecture-development-agent to execute development and testing from an approved Codex development document, task package, bug report, or test plan.
```

## 产出使用顺序

| 顺序 | 文件 | 用途 |
|---|---|---|
| 1 | `01_agent_prompt.md` | 开发测试 agent 的职责边界和硬规则。 |
| 2 | `02_codex_development_document_template.md` | 补全开发测试执行文档。 |
| 3 | `03_thread_governance.md` | 多分支 / 多线程开发测试时控制边界。 |
| 4 | `04_task_cards.md` | 把具体开发、测试、修复任务分发给 agent 或子线程。 |
| 5 | `06_upstream_agent_skills.md` | 直接复用 addyosmani/agent-skills 的开发测试 skill 路由。 |
| 6 | `skill-pack/architecture-development-agent` | 后续可安装成 Codex skill 的候选包。 |

## 使用边界

- 这个包可以直接给开发 agent 读取。
- 当前还不是 stable skill，除非后续你批准注册或安装。
- 开发 agent 只负责开发和测试；需求范围、架构治理、长期规则和发布动作仍由上游或用户拍板。
- 模块 A1 负责判断开发文档能不能开发，A2 负责组织成可执行开发结构，A3 负责判断模块是否具备开始写业务代码的前置条件。
- 模块 B 负责判断开发结果能不能用，并保证稳定、可靠、可集成。
- A3 未 `pass` 时不得写业务逻辑；`prepare_required` 只允许补准备项，`blocked` 必须输出 approval request。
- 每个行为变更、bug 修复、contract 变更或测试变更都必须在 B 前提供 Red / Green / Regression 证据；缺 red evidence 且无合理不适用原因时 B 不得 pass。
- 模块或线程完成后自动运行模块 B；B 发现的 bug 模式、架构问题和预防检查沉淀为项目内架构反馈，反哺后续开发和架构处理。
- A1 / A3 / B 必须按判定矩阵输出 pass、needs_revision、prepare_required、fix_required 或 blocked；高风险边界统一输出 approval request。
- architecture feedback 必须登记为项目内反馈，并作为下一轮 A1 / A2 / A3 的输入；不得自动转 stable 或长期记忆。
- A1 / A2 / A3 / B 是框架层治理能力，不是新增执行工具。
- 如果开发环境已安装 `addyosmani/agent-skills`，开发 agent 可以按 `06_upstream_agent_skills.md` 直接调用其中的开发测试类 skill。
- 开发 agent 仍必须遵守目标项目自己的 AGENTS.md、测试命令、审批点和 git 规则。
