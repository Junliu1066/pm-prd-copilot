# 清理计划 - taxi-hailing-prd-test

- 生成时间：`2026-04-29T03:36:25+00:00`
- 模式：只生成预览，不执行清理
- 本次没有删除、移动、归档、覆盖、提交或推送任何文件。
- 真正执行清理必须经过你明确批准，并且应该作为单独命令执行。
- 保留规则：先归档，硬删除至少等归档后 30 天，并且仍需你二次确认精确清单。

## 允许讨论清理的范围
- `projects/taxi-hailing-prd-test/`
- `memory-cache/projects/taxi-hailing-prd-test/`，仅在项目偏好缓存审核后处理

## 受保护目录
- `.github/`
- `ai-intel/`
- `docs/`
- `governance/`
- `harness/`
- `plugins/`
- `pm-prd-copilot/`
- `registry/`
- `shared/`
- `skills/`
- `stewards/`
- `teaching/`
- `workflow/`

## 文件处理分组
### 敏感输入先归档，暂不删除 (`archive_sensitive_input`)
- 文件数：`1`
| 路径 | 类型 | 大小 | 审批后是否可清理 | 原因 |
| --- | --- | --- | --- | --- |
| projects/taxi-hailing-prd-test/00_raw_input.md | Markdown 文档 | 1542 | 否 | 原始输入可能包含项目特定或敏感上下文，只能在监督下归档。 |

### 沉淀后归档，再考虑清理 (`archive_then_cleanup_after_distillation`)
- 文件数：`4`
| 路径 | 类型 | 大小 | 审批后是否可清理 | 原因 |
| --- | --- | --- | --- | --- |
| projects/taxi-hailing-prd-test/01_requirement_brief.json | JSON 数据 | 3523 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/taxi-hailing-prd-test/01_requirement_brief.md | Markdown 文档 | 3081 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/taxi-hailing-prd-test/02_prd.generated.json | JSON 数据 | 7462 | 是 | 生成产物应保留到有用经验提取完成后再考虑归档清理。 |
| projects/taxi-hailing-prd-test/02_prd.generated.md | Markdown 文档 | 11395 | 是 | 生成产物应保留到有用经验提取完成后再考虑归档清理。 |

### 归档和审批后可清理候选 (`delete_after_approval`)
- 文件数：`2`
| 路径 | 类型 | 大小 | 审批后是否可清理 | 原因 |
| --- | --- | --- | --- | --- |
| projects/taxi-hailing-prd-test/01_requirement_brief.meta.json | 生成元数据 | 154 | 是 | 生成元数据通常可复现，核心产物归档后可列为清理候选。 |
| projects/taxi-hailing-prd-test/02_prd.generated.meta.json | 生成元数据 | 152 | 是 | 生成元数据通常可复现，核心产物归档后可列为清理候选。 |

### 保留到经验沉淀完成 (`retain_until_distilled`)
- 文件数：`2`
| 路径 | 类型 | 大小 | 审批后是否可清理 | 原因 |
| --- | --- | --- | --- | --- |
| projects/taxi-hailing-prd-test/00_test_review_notes.md | Markdown 文档 | 3019 | 否 | 项目评审笔记包含高价值纠错证据，应保留到架构沉淀完成。 |
| projects/taxi-hailing-prd-test/02_prd.final.md | Markdown 文档 | 38850 | 否 | 人工修订后的 final 产物是高价值学习证据，应保留到沉淀完成。 |

## 清理前必须审批
- [ ] 你确认项目已经可以收口。
- [ ] 你已审核 `closeout-report.md`。
- [ ] `architecture-feedback.md` 里的建议已被接受、拒绝或转成受监督 GitHub 变更。
- [ ] 原始输入的归档 / 隐藏敏感信息 / 保留策略已确认。
- [ ] 项目偏好缓存处理方式已确认。
- [ ] 归档目标已确认。
- [ ] 所有硬删除候选已经满足归档后 30 天。
- [ ] 硬删除前已完成第二次精确清单审批。
