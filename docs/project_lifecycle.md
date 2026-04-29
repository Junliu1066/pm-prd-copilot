# Project Lifecycle

项目清理不按文件名或体积判断，按生命周期状态判断。

## Active

项目仍在 active，当满足任一条件：

- 仍有未确认的产品范围、原型、开发文档、AI 方案或交付计划。
- 最近还在生成、修改、评审或运行 harness。
- 项目有待用户确认的 blocking questions。
- 项目沉淀还没有完成，final 文件、用户反馈、偏好缓存仍可能反哺架构。

Active 项目不能硬删除，只能整理、归档副本或生成 closeout 预览。

## Closeout Candidate

项目进入 closeout candidate，当满足：

- 核心交付已经结束或暂停。
- 近期不会继续迭代。
- 已经能列出最终交付物、废弃草稿、可沉淀经验和可清理文件。

这时只能生成 closeout 包，不能直接清理。

## Closeout Reviewed

项目进入 closeout reviewed，当用户已经审过：

- `closeout-report.md`
- `architecture-feedback.md`
- `cleanup-plan.md`
- `preference-memory-disposition.md`
- 可反哺架构的信息
- 可归档清单
- 项目偏好缓存的处理决定：清除、仅保留为项目档案、或经用户批准提炼到长期记忆

这一步之后，可以执行用户批准的 archive 操作。

## Archived

项目归档后：

- 保留 closeout 记录。
- 保留已沉淀到 `docs/`、`teaching/` 或 proposal 的架构反馈。
- 不再把项目缓存当作 active 工作上下文读取。
- 项目偏好缓存默认不跨项目复用；归档对齐后应清除 active 指针。长期记忆必须经用户明确批准。
- 记录归档日期。

## Hard Delete Eligible

硬删除只在归档后至少 30 天才进入候选，并且仍需用户再次确认精确删除清单。

禁止自动删除：

- 未沉淀的 final 人工编辑文件。
- 未审核的 raw input。
- 未审核的 project preference cache。
- closeout 审计记录。
- 任何稳定框架目录。

## Thread Route

所有项目在归档前都要做 closeout。后续线程建议分为：

- 项目线程：只处理当前项目需求、PRD、原型、UI、开发文档和交付问题。
- 归档线程：只处理 closeout、经验总结、偏好缓存处理、归档清单和 30 天后删除候选。
- 长期治理线程：只处理经用户批准的长期规则、模板、skill、harness、workflow、自动化和架构优化。

## Decision Rule

当状态不确定时，默认当作 active 或 closeout candidate，不当作可删除项目。
