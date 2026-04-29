# Scheduled Check Mechanisms

这个文件记录定时检查机制，避免自动化数量膨胀和检查点遗漏。

## Active Automations

| ID | Schedule | Purpose | Model | Reasoning |
|---|---|---|---|---|
| `bug` | 每天 03:00 | 错误巡检、bug 记录、自动化健康检查、Finding 3 状态检查 | `gpt-5.5` | `xhigh` |
| `ai-gpt-5-5` | 每天 09:00 | 架构治理、AI 情报、用户教学、错误巡检摘要、自动化健康摘要、Finding 3 汇报 | `gpt-5.5` | `xhigh` |
| `codex` | 每周一 10:00 | 框架层复核与备份 | `gpt-5.5` | `xhigh` |

## Automation Health Check

每天凌晨巡检必须检查：

- `ai-gpt-5-5`、`bug`、`codex` 是否存在。
- 状态是否为 `ACTIVE`。
- 可配置模型的 cron 任务是否为 `gpt-5.5`。
- 推理强度是否为 `xhigh`。
- `rrule` 是否符合预期。
- `cwds` 指向的目录是否存在。
- `cwds` 是否指向当前主工作区 `/Users/liujun/Desktop/产品经理skill`，不得继续审旧 worktree。
- 报告是否在开头写明 cwd、branch、HEAD、dirty 文件数量。
- 引用模板或检查脚本是否存在；缺失时必须报告路径和替代检查。
- 是否会写文件；如果会写，必须列出写入路径。
- 最近一次报告是否写入了预期目录。

发现异常时，写入：

- `docs/error_reports/daily/YYYY-MM-DD.md`
- `docs/error_reports/bug_log.md`

## Default Non-Writing Checks

日常和 CI 默认使用只读检查：

```bash
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

只有用户明确需要刷新报告时，才允许改用 `--write-report`。报告必须列出写入路径，并说明为什么需要写报告。

每条异常必须带解决方案建议：

- recommended action
- smallest safe fix
- alternative options
- risk / tradeoff
- validation command
- user approval needed

## Finding 3 Check

每天凌晨巡检必须检查 production pipeline 是否仍绕过 governed workflow：

- 查看 `pm-prd-copilot/scripts/run_pipeline.py` 是否默认执行 `workflow/prd_workflow.yaml` approval preflight。
- 查看是否只有显式 `--fast-draft` 才允许绕过 approval gates。
- 查看是否存在 formal delivery gate checker。
- 查看 `docs/error_reports/bug_log.md` 中 `BUG-2026-04-28-001` 是否仍为 `open`。

状态规则：

- `open`: pipeline 默认仍可绕过 governed workflow，或 fast draft 不需要显式参数。
- `watch`: 已有防护但还没有完整回归证据。
- `fixed`: 已有 governed pipeline 或 formal gate，并通过 regression 与 harness。

## No Auto-Destructive Action

这些定时检查只能记录、汇报、提出候选。不得自动：

- 删除或归档文件。
- commit、push、创建 PR。
- 修改稳定 Skill、harness、steward、workflow 或 registry。
- 切换模型供应商。
- 更改发布或外部分发策略。

需要修改时，先给用户精确清单和测试证据。

## Report Solution Requirement

所有定时任务汇报都不能只列问题。每个 finding、bug、drift、AI signal、pruning candidate、approval item 都必须包含：

- 推荐解决方案。
- 最小安全改法。
- 替代方案。
- 风险和取舍。
- 验证命令或检查方式。
- 是否需要用户批准。
- 如果暂缓处理会有什么影响。
