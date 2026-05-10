# 开发测试 Agent 任务卡

这些任务卡可以直接复制给开发 agent，按项目实际路径替换占位符。

## 1. 输入梳理卡

```text
你是 Development Test Agent。请先只做开发输入梳理，不写代码。

目标：
- 读取 AGENTS.md / agent.md / README / package 配置 / 测试入口。
- 读取上游 PRD、Codex 开发文档、任务包和验收标准。
- 输出当前开发主线、已确认事实、工作假设、P0/P1/P2 问题。
- 判断是否可进入开发实现。

禁止：
- 不改文件。
- 不补产品范围。
- 不新增 skill / harness / workflow。

输出：
- 开发主线卡。
- 输入材料表。
- 阻塞问题表。
- 下一步最小动作。
```

## 2. 开发测试执行文档补全卡

```text
请基于上游输入补全开发测试执行文档。

输入：
- PRD / 需求：
- Codex 开发文档：
- 原型 / 页面流：
- 代码仓库：
- 当前约束：

要求：
- 不改变产品范围。
- 选择单线程开发测试、分线程开发测试或修复测试模式。
- 生成任务包、允许修改范围、禁止修改范围、验证命令、回滚方案、人工确认点。
- 如启用分线程，只生成开发测试分线程矩阵和 integration 计划。

禁止：
- 不批准数据库、模型、MCP、GitHub、memory 或 stable skill 变更。
- 不设计治理架构。
```

## 3. 技术实现拆解卡

```text
请把已确认的开发范围拆成实现模块，不估时、不改范围。

必须输出：
- UI / client scope。
- API / service scope。
- data / migration scope，若不涉及请明确 none。
- permission / privacy / security scope。
- AI / prompt scope，若不涉及请明确 none。
- testing scope。
- blockers for upstream。

每个 scope 都要写依赖、风险和验收方式。
```

## 4. 分线程启动卡

```text
请为线程 <THREAD_ID> 执行开发测试任务。

目标：

上下文：

允许修改：

禁止修改：

依赖：

检查命令：

验收标准：

规则：
- 只改允许范围。
- 发现需要越界时，停止并生成 scope change request。
- 完成后输出修改文件、检查结果、未检查项、回滚方式和 closeout。
```

## 5. 代码实现卡

```text
请执行最小可接受实现。

如环境可用，请优先调用上游 skill：
- incremental-implementation
- test-driven-development

步骤：
1. 读取相关代码和本地模式。
2. 说明将要修改的文件和原因。
3. 实现最小变更。
4. 运行目标检查。
5. 修复直接失败。
6. 输出 Round 1 / Round 2 结果。

禁止：
- 不做无关重构。
- 不覆盖用户已有改动。
- 不新增依赖，除非任务明确批准。
- 不改发布、模型、数据库或 stable 治理组件。
```

## 6. 测试执行卡

```text
请只执行测试和验证，不新增功能。

如环境可用，请优先调用上游 skill：
- test-driven-development
- browser-testing-with-devtools（仅浏览器目标）

输入：
- 待测变更：
- 验收标准：
- 检查命令：

要求：
- 运行目标检查。
- 记录失败日志要点。
- 区分代码缺陷、测试缺陷、环境问题和输入不完整。
- 只在明确要求时修复；否则输出测试报告。
```

## 7. Review 卡

```text
请以代码审查视角检查这次变更。

如环境可用，请优先调用上游 skill：
- code-review-and-quality
- security-and-hardening（涉及输入、权限、数据、外部集成）

重点：
- bug、回归、遗漏测试、权限/数据风险。
- 写入边界是否越界。
- 是否改变产品范围。
- 是否缺少验证或回滚。
- 是否有过度实现或重复代码。

输出：
- findings，按严重程度排序。
- open questions。
- test gaps。
- 最小修复建议。
```

## 8. Integration 卡

```text
请执行 integration / test，不新增功能。

输入：
- 已通过 gate 的线程：
- contract 状态：
- 检查命令：

要求：
- 先检查依赖线程状态。
- 对齐共享契约。
- 运行集成检查。
- 失败时定位责任线程。
- 输出 integration report。

禁止：
- 不直接合 main。
- 不 push / PR。
- 不接受高风险未解决项。
```

## 9. CI / 测试失败修复卡

```text
请修复以下失败，目标是最小修复。

如环境可用，请优先调用上游 skill：
- debugging-and-error-recovery
- test-driven-development

失败信息：

相关分支 / 文件：

要求：
- 先复现或读取日志。
- 定位根因。
- 只改责任范围。
- 重跑失败检查和必要回归。
- 输出根因、修复、验证证据、剩余风险。
```

## 10. Closeout 卡

```text
请为本轮开发测试生成 closeout。

必须包含：
- 完成了什么。
- 修改了哪些文件。
- 跑了哪些检查。
- 哪些检查不能跑及原因。
- 剩余风险。
- 回滚方式。
- 用户或上游需要拍板什么。
- 哪些事项需要产品 / 架构 / 发布侧处理。

禁止：
- 不写长期记忆。
- 不把 candidate 转 stable。
- 不删除或归档文件。
```
