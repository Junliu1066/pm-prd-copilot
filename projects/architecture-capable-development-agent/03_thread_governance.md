# 分线程开发测试操作系统

## 启用条件

满足任一条件才启用分线程开发测试：

- 多模块、多页面、多 API 或多端联调。
- DB/API/AI 输出格式等契约已经由上游冻结。
- UI、后端、测试、数据、AI 实现可以独立推进。
- 用户明确要求多分支、多线程或并行开发。

不满足时保持单线程，并记录降级理由。

## 开发主线卡

| 字段 | 内容 |
|---|---|
| 主线 ID |  |
| 当前开发目标 |  |
| 为什么做 |  |
| 可验证效果 |  |
| 本轮不做 |  |
| 当前状态 | active / waiting_user / blocked / done |
| 最近推进 |  |
| 下一步最小动作 |  |
| 需要上游拍板 |  |

## 分线程矩阵

| 线程 ID | 开发目标 | 写入范围 | 禁止范围 | 依赖 | 风险 | 负责人 | 状态 |
|---|---|---|---|---|---|---|---|
| T-A |  |  |  |  | low / medium / high | dev / test | planned |

## 写入边界规则

- 每个线程必须有唯一主写入范围。
- 共享文件只能由 integration 线程或约定 owner 修改。
- 测试文件可与对应模块同线程修改，但必须写明路径。
- migration、schema、权限、AI 输出格式、发布配置默认高风险；开发 agent 不自行决定。
- 发现需要越界时，生成 scope change request，不直接改。

## Contract 状态

开发 agent 不负责定义 contract，只负责确认是否足够开发测试。

| 契约 | owner | 状态 | 依赖线程 | 不足时处理 |
|---|---|---|---|---|
| API | 上游 / 架构侧 | missing / draft / frozen |  | 上报 |
| DB schema | 上游 / 架构侧 | missing / draft / frozen |  | L3 上报 |
| AI output | 上游 / 架构侧 | missing / draft / frozen |  | 上报 |
| permission | 上游 / 架构侧 | missing / draft / frozen |  | 上报 |
| page state | 上游 / 架构侧 | missing / draft / frozen |  | 上报 |

## 分线程启动包

```text
线程 ID：
分支名：
开发目标：
上下文摘要：
输入材料：
允许修改范围：
禁止修改范围：
依赖线程：
相关文件：
执行步骤：
验证命令：
验收标准：
失败处理：
执行证据要求：
需要用户确认：
```

## 状态机

```text
planned
-> ready
-> running
-> self_checked
-> reviewed
-> gate_passed
-> integration_pending
-> integration_passed / integration_failed
-> fix_required / blocked / closed
```

## 状态准入

| 进入状态 | 必要条件 |
|---|---|
| ready | 输入、范围、依赖、验证、回滚已明确。 |
| running | 无 P0 阻塞，写入范围明确。 |
| self_checked | 线程内检查已完成并有证据。 |
| reviewed | reviewer 已看 diff、风险和测试结果。 |
| gate_passed | 测试、范围、人工确认点通过。 |
| integration_pending | 依赖线程全部 gate_passed。 |
| integration_passed | 集成检查通过。 |
| closed | 执行证据已记录，剩余风险已上报。 |

## Integration 规则

- 所有线程先进入 integration / test，不直接合 main。
- integration 失败时先定位责任线程。
- 修复只回到责任线程或专门 fix 线程。
- 不接受“测试失败但先合”的默认处理。
- 高风险未解决项必须上报用户或上游架构侧。

## 失败回流

| 失败类型 | 处理 |
|---|---|
| 编译 / lint | 回责任线程最小修复。 |
| 单元测试失败 | 定位责任模块，补测试或修实现。 |
| API contract 破坏 | 停止并上报 contract owner。 |
| DB migration 风险 | 暂停，L3 上报。 |
| UI 回归 | 回 UI 线程，补手工或视觉证据。 |
| AI 输出漂移 | 回 prompt / eval 线程；若方案不清，停止上报。 |
| 范围漂移 | 暂停，回 PM / 用户确认。 |

## Closeout

每个线程关闭前记录：

| 字段 | 内容 |
|---|---|
| 完成内容 |  |
| 修改文件 |  |
| 检查结果 |  |
| 未检查项 |  |
| 剩余风险 |  |
| 回滚方式 |  |
| 是否越界 | yes / no |
| 需上游处理 | none / product / architecture / testing / release |

## WIP 限制

- 开发主线同时只能有 1 个。
- 高风险线程同时最多 1 个 running。
- 未冻结契约前，不启动依赖线程。
- 线程长时间无推进时只生成停滞报告，不自动归档或删除。
