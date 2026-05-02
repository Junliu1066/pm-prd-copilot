# 项目收口报告 - demo-project

- 生成时间：`2026-04-29T03:36:25+00:00`
- 模式：只生成报告，不执行清理
- 破坏性动作：已禁用
- 归档、删除、提交、PR、prompt、模板或框架变更都需要你审批。

## 项目概况
- 标题：商家财务流水批量导出
- 需求类型：new_feature
- 紧急度：p1
- 业务目标：提升商家对账效率，降低客服月底人工报表响应压力，满足大客户财务流水导出诉求，支持销售成交与客户维护。
- 收口解读：这是正常项目收口。
- 最近运行 ID：`pipeline-latest`
- Pipeline 状态：`completed`
- Harness 状态：`pass`
- 效率检查状态：`pass`
- 用户故事数量：`3`

## 运行要求产物
`source_brief`, `source_brief_markdown`, `prd_document`, `prd_markdown`

## 文件盘点摘要
- 扫描文件数：`42`
- 文件总大小：`996479` bytes

| 处理建议 | 文件数 |
| --- | --- |
| 敏感输入先归档，暂不删除 (`archive_sensitive_input`) | 1 |
| 沉淀后归档，再考虑清理 (`archive_then_cleanup_after_distillation`) | 30 |
| 归档和审批后可清理候选 (`delete_after_approval`) | 5 |
| 需要人工审核 (`manual_review`) | 3 |
| 保留项目状态记录 (`retain_project_record`) | 1 |
| 保留到经验沉淀完成 (`retain_until_distilled`) | 2 |

## 人工修订信号
| 生成稿 | 最终稿 | 新增行 | 删除行 |
| --- | --- | --- | --- |
| 02_prd.generated.md | 02_prd.final.md | 8 | 365 |
| 03_user_stories.generated.md | 03_user_stories.final.md | 5 | 35 |

## 项目评审笔记
- 评审文件：`06_review_merge.md`
- 评审要求补齐权限边界说明
- 评审要求增加导出审计日志

## PRD 质量信号
- 生成稿旧问题：`导出场景污染`、`Excel 场景污染`、`异步导出场景污染`
- 最终稿已具备的关键结构：_无_
- 最终稿是否可作为结构黄金样例候选：`否`

## 收口审批清单
- [ ] 确认项目可以进入收口。
- [ ] 审核 final PRD、用户故事、风险检查、埋点计划里是否有可沉淀经验。
- [ ] 决定哪些信号可以进入 GitHub 知识库或优化 backlog。
- [ ] 确认原始输入如何归档、隐藏敏感信息或保留。
- [ ] 审核 `cleanup-plan.md` 后再做任何归档或删除。
- [ ] 对认可的架构反馈，后续再走受监督分支或 PR。

## 需要人工审核的文件
| 路径 | 处理建议 | 原因 |
| --- | --- | --- |
| projects/demo-project/00_raw_input.md | 敏感输入先归档，暂不删除 (`archive_sensitive_input`) | 原始输入可能包含项目特定或敏感上下文，只能在监督下归档。 |
| projects/demo-project/02_prd.final.md | 保留到经验沉淀完成 (`retain_until_distilled`) | 人工修订后的 final 产物是高价值学习证据，应保留到沉淀完成。 |
| projects/demo-project/03_user_stories.final.md | 保留到经验沉淀完成 (`retain_until_distilled`) | 人工修订后的 final 产物是高价值学习证据，应保留到沉淀完成。 |
| projects/demo-project/04_risk_check.md | 需要人工审核 (`manual_review`) | 未注册文件，任何清理决定前都需要人工审核。 |
| projects/demo-project/05_tracking_plan.md | 需要人工审核 (`manual_review`) | 未注册文件，任何清理决定前都需要人工审核。 |
| projects/demo-project/06_review_merge.md | 需要人工审核 (`manual_review`) | 未注册文件，任何清理决定前都需要人工审核。 |
| projects/demo-project/project_state.json | 保留项目状态记录 (`retain_project_record`) | 项目状态文件是本地生命周期指针，必须保留。 |
