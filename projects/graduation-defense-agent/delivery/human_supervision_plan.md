# Human Supervision Plan：毕业答辩辅导智能体

supervision_id: `human-supervision-20260425`

## required_gates

| gate_id | 触发条件 | 必须确认的人 | 不确认时 |
| --- | --- | --- | --- |
| prd_scope | 修改 MVP 范围、用户目标、非目标、核心流程 | 用户/PM | 停止执行并提出问题 |
| database_schema | 新增或变更训练、论文资料、画像、删除字段 | 用户/技术负责人 | 只写方案，不执行迁移 |
| external_api | 接入外部模型、存储、监控、支付或第三方服务 | 用户/技术负责人 | 使用 mock 或本地 fallback |
| mcp_integration | 接入新的 MCP、扩大 MCP 权限、让 MCP 访问外部数据或仓库 | 用户/技术负责人 | 只写 MCP 候选方案，不接入 |
| registry_harness | 新增 registry、artifact、steward、harness 检查或改变失败等级 | 用户/技术负责人 | 只生成 proposal，不改规则 |
| model_change | 选择、替换或升级模型配置 | 用户/AI 负责人 | 继续使用当前 fallback 或旧配置 |
| github_push | 推送远程仓库、创建 PR、发布版本 | 用户 | 只保留本地修改 |
| destructive_data | 删除数据库、清理历史记录、重置用户资料 | 用户 | 禁止执行 |
| skill_update | 修改通用 Skill、harness 或记忆机制 | 用户 | 只生成提案，不落地 |

## review_points

- 每个 Codex 任务完成后，先看 diff 和测试结果，再决定是否继续下一任务。
- AI 输出和外部资料只作为信号；真实性、模型效果和成本需要用户人工验证。
- 如果任务出现范围漂移，先回到 PRD 和 delivery_plan，不继续开发。
- 如果多个小管家无法管理当前任务复杂度，大管家需要向用户汇报并建议拆分同级管理者。

## approval_record_policy

- 人工确认应记录在开发日志或 PR 描述中。
- 高风险确认需要写明确认范围，而不是笼统写“同意”。
- 未记录确认的任务不能被视为完成。
