# Error Reports

这个目录专门收集项目执行过程中的报错、测试失败、治理检查异常、回归风险和后续修复记录。

## Scope

记录：

- regression、harness、redaction、packaging、closeout、AI intel、pipeline、prototype、delivery planning 的失败或警告。
- 用户指出的执行错误和遗漏。
- 版本更新或模型更新后发现的不兼容、冗余组件、失效规则和待裁剪项。
- 自动凌晨巡检发现的 bug。

不记录：

- 密钥、token、`.env` 内容、私密凭证。
- 未经用户批准的硬删除操作。
- 未经确认的外部事实结论。

## Files

| Path | Purpose |
|---|---|
| `bug_log.md` | 长期 bug 索引和状态。 |
| `daily/` | 每日凌晨巡检报告。 |
| `runs/` | 临时或手动专项检查报告。 |

## Bug Record Format

| ID | Date | Severity | Area | Status | Evidence | Suspected cause | Solution recommendation | Next action | User approval |
|---|---|---|---|---|---|---|---|---|---|
|  |  | P0/P1/P2/P3 |  | open/fixed/watch |  |  |  |  | Yes/No |

## Handling Rule

- 自动巡检可以记录、分类和提出修复建议。
- 自动巡检不能删除、归档、commit、push、修改稳定 skill、修改 harness、切换模型供应商或更改发布策略。
- 涉及稳定架构、模型、外部数据源、清理删除、Skill/Harness/Steward 裁剪的修复，需要先提交给用户审核。
- 每个 bug 或 warning 必须附带解决方案建议、最小安全修复、验证方式和是否需要用户批准。
