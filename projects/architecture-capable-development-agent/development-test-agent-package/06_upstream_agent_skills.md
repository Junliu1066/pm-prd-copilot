# 可直接复用的上游 Agent Skills

来源：[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)

本文件给开发测试 agent 使用。原则：开发 agent 只拿来辅助开发和测试，不接管产品定义、治理沉淀、发布、归档、push / PR。

核对基准：以上游仓库 `skills/` 目录的 20 个核心工程 skills 为准；`using-agent-skills` 是元说明 skill，不作为本开发测试 agent 的任务路由。

## 使用方式

如果目标环境已经安装 `addyosmani/agent-skills`，开发 agent 可以直接调用对应 skill。

如果未安装，把对应上游 skill 的 `SKILL.md` 作为本轮任务参考输入即可。不要把它们自动注册成本仓库 stable skill；是否安装或注册由用户另行批准。

所有 skill / harness 使用都必须由 A2 的 `dynamic_skill_harness_plan` 决定并记录：

```text
trigger:
candidate_skill_or_harness:
use_or_skip:
reason:
command_or_reference:
expected_evidence:
result:
follow_up:
```

不相关的 skill / harness 记录 skip reason，不强行运行。

无论 A2 选择哪些上游 skill，模块业务实现都必须先通过 A3 `module_development_preflight`。A3 为 `prepare_required` 时只能补准备项，A3 为 `blocked` 时停止并输出审批请求。

## 开发测试默认可用

| 上游 skill | 何时用 | 本地边界 |
|---|---|---|
| `incremental-implementation` | 任意超过单文件的小功能或修复。 | 只做垂直小切片，不提交、不 push。 |
| `test-driven-development` | 改业务逻辑、修 bug、补行为测试。 | 测试先行或补测试；不为赶进度跳过验证。 |
| `debugging-and-error-recovery` | 测试失败、构建失败、行为异常。 | 先复现和定位，再最小修复。 |
| `code-review-and-quality` | 完成实现后自审或人工 review 前。 | 只输出代码问题、测试缺口和最小修复建议。 |
| `code-simplification` | 代码可运行但复杂、重复或难维护。 | 保持行为不变；不做无关重构。 |
| `source-driven-development` | 使用框架、SDK、库 API，且存在版本或用法不确定。 | 必须查官方来源；无法联网时标注未验证。 |

## 条件可用

| 上游 skill | 触发条件 | 本地边界 |
|---|---|---|
| `frontend-ui-engineering` | 开发或修改用户界面。 | 只实现已批准 UI / 交互，不改产品流程。 |
| `browser-testing-with-devtools` | 浏览器页面、前端 bug、运行时 DOM / console / network 问题。 | 只做测试和定位，不擅自改发布配置。 |
| `api-and-interface-design` | 开发 API、模块边界、错误语义或接口兼容。 | 只能消费或细化已批准 contract；变更 contract 要上报。 |
| `security-and-hardening` | 涉及用户输入、认证、权限、数据存储、外部集成。 | 发现高风险停下上报；不自行改安全策略范围。 |
| `performance-optimization` | 有性能指标、性能回归或明确性能任务。 | 先测量再优化；不做无指标的大改。 |
| `ci-cd-and-automation` | CI 失败、测试流水线故障或本地验证脚本问题。 | 只修开发测试所需问题；修改部署流水线需上游批准。 |
| `documentation-and-adrs` | 代码变更需要补 API 文档、README、注释或 ADR。 | 只补实现相关文档；不写治理制度。 |
| `deprecation-and-migration` | 已批准迁移、删除旧代码或兼容替换。 | 数据迁移、用户影响、删除动作必须上游批准。 |

## 默认不由开发测试 agent 使用

| 上游 skill | 原因 | 处理 |
|---|---|---|
| `idea-refine` | 概念发散，不属于开发测试职责。 | 交给上游输入侧。 |
| `spec-driven-development` | 写 PRD / spec，不属于开发测试职责。 | 开发 agent 等上游转成开发任务包后再执行。 |
| `planning-and-task-breakdown` | 可用于补开发任务包，但不应改变 scope。 | 仅在上游任务包不足时受限使用。 |
| `context-engineering` | 可用于恢复上下文，但不作为开发任务本体。 | 只读规则和上下文，不写长期规则。 |
| `git-workflow-and-versioning` | 涉及 commit / branch / versioning，容易越过职责。 | 只参考小变更和原子 diff 思想；不提交、不 push。 |
| `shipping-and-launch` | 发布上线不属于开发测试职责。 | 交给发布 / 上游任务。 |

## 推荐调用顺序

普通功能：

```text
incremental-implementation
-> test-driven-development
-> code-review-and-quality
```

Bug / CI：

```text
debugging-and-error-recovery
-> test-driven-development
-> code-review-and-quality
```

前端：

```text
frontend-ui-engineering
-> browser-testing-with-devtools
-> code-review-and-quality
```

API：

```text
api-and-interface-design
-> test-driven-development
-> security-and-hardening
-> code-review-and-quality
```

性能：

```text
performance-optimization
-> test-driven-development
-> code-review-and-quality
```

## 直接交给开发 agent 的补充指令

```text
如果你当前环境能访问 addyosmani/agent-skills，请按任务类型直接调用其中的开发测试相关 skill：

- incremental-implementation
- test-driven-development
- debugging-and-error-recovery
- code-review-and-quality
- code-simplification
- frontend-ui-engineering
- browser-testing-with-devtools
- api-and-interface-design
- security-and-hardening
- performance-optimization
- source-driven-development

不要调用 idea-refine、spec-driven-development 或 shipping-and-launch 来改变本轮职责。产品、架构、发布、归档和长期治理问题全部上报。
```
