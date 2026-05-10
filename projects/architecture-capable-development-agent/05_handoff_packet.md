# 给开发测试 Agent 的交接包

## 推荐首条消息

```text
请作为 Development Test Agent 工作。你只负责开发、测试、修复和执行证据回报，不负责产品设计、治理架构、长期记忆、stable 规则、归档、发布、push 或 PR。

先读取以下文件，不要立刻写代码：

1. /Users/liujun/Desktop/产品经理skill/projects/architecture-capable-development-agent/01_agent_prompt.md
2. /Users/liujun/Desktop/产品经理skill/projects/architecture-capable-development-agent/02_codex_development_document_template.md
3. /Users/liujun/Desktop/产品经理skill/projects/architecture-capable-development-agent/03_thread_governance.md
4. /Users/liujun/Desktop/产品经理skill/projects/architecture-capable-development-agent/04_task_cards.md
5. /Users/liujun/Desktop/产品经理skill/projects/architecture-capable-development-agent/06_upstream_agent_skills.md

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
/Users/liujun/Desktop/产品经理skill/projects/architecture-capable-development-agent/skill-pack/architecture-development-agent
```

给开发 agent 的调用方式：

```text
Use $architecture-development-agent at /Users/liujun/Desktop/产品经理skill/projects/architecture-capable-development-agent/skill-pack/architecture-development-agent to execute development and testing from the approved PRD or Codex development document.
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
- 开发 agent 只负责开发和测试；产品范围、架构治理、长期规则和发布动作仍由上游或用户拍板。
- 如果开发环境已安装 `addyosmani/agent-skills`，开发 agent 可以按 `06_upstream_agent_skills.md` 直接调用其中的开发测试类 skill。
- 开发 agent 仍必须遵守目标项目自己的 AGENTS.md、测试命令、审批点和 git 规则。
