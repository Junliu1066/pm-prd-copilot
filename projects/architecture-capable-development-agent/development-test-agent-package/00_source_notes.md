# 开发测试 Agent 来源笔记

- 状态：项目交付候选包，不是 stable skill，不改 registry。
- 读者：用户本人和后续负责落地的开发 agent。
- 目标：把上游任务 / 架构输入的治理边界压成开发 agent 可执行的开发测试约束。开发 agent 只负责开发、测试、修复和证据回报，不负责需求决策、治理沉淀或长期规则。

## 输入来源

| 来源 | 吸收内容 | 本包处理方式 |
|---|---|---|
| `agent.md` | 主线识别、任务漂移禁止、两轮检查、审批点、交付总结。 | 转成开发测试执行边界和自检规则。 |
| `docs/architecture.md` | stable / learning / review / intel / governance contract / responsibility layer。 | 只作为越界识别，不让开发 agent 承担治理职责。 |
| `docs/proposals/architecture_self_management_system.md` | 架构是核心资产、L1/L2/L3、promotion / pruning gate。 | 转成开发 agent 的停止条件和上报条件。 |
| `docs/thread_registry.md` | 线程台账、上下文恢复、WIP 限制、停滞处理。 | 转成开发分线程执行规则。 |
| `pm-prd-copilot/templates/codex_development_document_template.md` | 轻量开发文档、多分支执行机制、验证和回滚。 | 拆成开发测试任务包模板。 |
| `plugins/delivery-planning-suite/skills/*` | Codex 任务包、development plan reviewer、delivery quality reviewer。 | 只吸收任务包和执行审查口径。 |
| `https://github.com/addyosmani/agent-skills` | 小技能、触发描述、阶段门禁、spec-first、planning-first、验证优先的组织方式。 | 不照搬内容，只吸收“技能即可复用操作程序”的结构。 |

## 外部 skill 仓库吸收原则

从 `addyosmani/agent-skills` 只吸收结构，不复制其具体执行文本：

- 每个 skill 必须有清楚触发场景。
- skill 主体只放必要流程，详细模板进入 references。
- agent 不应跳过输入、计划、实现、验证、审查的关键门。
- 复杂开发拆成小的、可验证的任务包。
- 输出要能直接被另一个开发 agent 执行。

## 本包的核心设计

```text
读取开发输入
-> 模块 A1：审查开发文档工程可落地性
-> needs_revision / blocked 时反向输出问题清单
-> 模块 A2：组织成单线程或分线程开发结构
-> 模块 A3：模块开发前置准备门
-> 实现最小可接受变更
-> Red / Green / Regression 红绿测试
-> 运行测试
-> 修复直接失败
-> 模块 B：逐线程质量稳定性门禁
-> integration / review
-> 集成后再次经过模块 B
-> closeout
-> 沉淀 bug 模式、架构问题和预防检查为项目内架构反馈
-> architecture feedback 反哺下一轮 A1 / A2 / A3
-> 回报执行证据
```

## 本轮不做

- 不把 candidate skill 注册到 `registry/skills.yaml`。
- 不修改 stable operating model。
- 不新增 harness、workflow、automation；已有三日巡检只同步 A3 判断口径。
- 不写长期记忆。
- 不对现有项目产物做归档、删除、提交或推送。
