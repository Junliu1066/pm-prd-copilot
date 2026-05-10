# 清理计划 - prompt-optimization-workbench

- 生成时间：`2026-04-29T03:36:26+00:00`
- 模式：只生成预览，不执行清理
- 本次没有删除、移动、归档、覆盖、提交或推送任何文件。
- 真正执行清理必须经过你明确批准，并且应该作为单独命令执行。
- 保留规则：先归档，硬删除至少等归档后 30 天，并且仍需你二次确认精确清单。

## 允许讨论清理的范围
- `projects/prompt-optimization-workbench/`
- `memory-cache/projects/prompt-optimization-workbench/`，仅在项目偏好缓存审核后处理

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
### 沉淀后归档，再考虑清理 (`archive_then_cleanup_after_distillation`)
- 文件数：`11`
| 路径 | 类型 | 大小 | 审批后是否可清理 | 原因 |
| --- | --- | --- | --- | --- |
| projects/prompt-optimization-workbench/prototype/.DS_Store | file | 6148 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/prompt-optimization-workbench/prototype/evaluation-report-detail-html-prototype.zip | zip | 46960 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/prompt-optimization-workbench/prototype/html/README.md | Markdown 文档 | 905 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/prompt-optimization-workbench/prototype/html/app.js | js | 15562 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/prompt-optimization-workbench/prototype/html/index.html | HTML 文件 | 44762 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/prompt-optimization-workbench/prototype/html/open-mac.command | command | 70 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/prompt-optimization-workbench/prototype/html/open-windows.bat | bat | 37 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/prompt-optimization-workbench/prototype/html/prototype_manifest.json | JSON 数据 | 8931 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/prompt-optimization-workbench/prototype/html/prototype_notes.md | Markdown 文档 | 3165 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/prompt-optimization-workbench/prototype/html/standalone.html | HTML 文件 | 85308 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/prompt-optimization-workbench/prototype/html/styles.css | css | 25017 | 是 | 项目过程产物应先审核归档，再考虑清理。 |

### 需要人工审核 (`manual_review`)
- 文件数：`1`
| 路径 | 类型 | 大小 | 审批后是否可清理 | 原因 |
| --- | --- | --- | --- | --- |
| projects/prompt-optimization-workbench/.DS_Store | file | 6148 | 否 | 未注册文件，任何清理决定前都需要人工审核。 |

## 清理前必须审批
- [ ] 你确认项目已经可以收口。
- [ ] 你已审核 `closeout-report.md`。
- [ ] `architecture-feedback.md` 里的建议已被接受、拒绝或转成受监督 GitHub 变更。
- [ ] 原始输入的归档 / 隐藏敏感信息 / 保留策略已确认。
- [ ] 项目偏好缓存处理方式已确认。
- [ ] 归档目标已确认。
- [ ] 所有硬删除候选已经满足归档后 30 天。
- [ ] 硬删除前已完成第二次精确清单审批。
