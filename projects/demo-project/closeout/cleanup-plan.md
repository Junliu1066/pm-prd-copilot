# 清理计划 - demo-project

- 生成时间：`2026-04-29T03:36:25+00:00`
- 模式：只生成预览，不执行清理
- 本次没有删除、移动、归档、覆盖、提交或推送任何文件。
- 真正执行清理必须经过你明确批准，并且应该作为单独命令执行。
- 保留规则：先归档，硬删除至少等归档后 30 天，并且仍需你二次确认精确清单。

## 允许讨论清理的范围
- `projects/demo-project/`
- `memory-cache/projects/demo-project/`，仅在项目偏好缓存审核后处理

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
| projects/demo-project/00_raw_input.md | Markdown 文档 | 196 | 否 | 原始输入可能包含项目特定或敏感上下文，只能在监督下归档。 |

### 沉淀后归档，再考虑清理 (`archive_then_cleanup_after_distillation`)
- 文件数：`30`
| 路径 | 类型 | 大小 | 审批后是否可清理 | 原因 |
| --- | --- | --- | --- | --- |
| projects/demo-project/01_requirement_brief.json | JSON 数据 | 4781 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/demo-project/01_requirement_brief.md | Markdown 文档 | 4403 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/demo-project/02_prd.generated.json | JSON 数据 | 14138 | 是 | 生成产物应保留到有用经验提取完成后再考虑归档清理。 |
| projects/demo-project/02_prd.generated.md | Markdown 文档 | 18736 | 是 | 生成产物应保留到有用经验提取完成后再考虑归档清理。 |
| projects/demo-project/03_user_stories.generated.json | JSON 数据 | 2947 | 是 | 生成产物应保留到有用经验提取完成后再考虑归档清理。 |
| projects/demo-project/03_user_stories.generated.md | Markdown 文档 | 2467 | 是 | 生成产物应保留到有用经验提取完成后再考虑归档清理。 |
| projects/demo-project/04_risk_check.generated.json | JSON 数据 | 3070 | 是 | 生成产物应保留到有用经验提取完成后再考虑归档清理。 |
| projects/demo-project/04_risk_check.generated.md | Markdown 文档 | 2096 | 是 | 生成产物应保留到有用经验提取完成后再考虑归档清理。 |
| projects/demo-project/05_tracking_plan.generated.json | JSON 数据 | 2354 | 是 | 生成产物应保留到有用经验提取完成后再考虑归档清理。 |
| projects/demo-project/05_tracking_plan.generated.md | Markdown 文档 | 2397 | 是 | 生成产物应保留到有用经验提取完成后再考虑归档清理。 |
| projects/demo-project/prototype/page_png/01_export_dashboard.png | 视觉文件 | 145975 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/demo-project/prototype/page_png/02_create_export_task.png | 视觉文件 | 122623 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/demo-project/prototype/page_png/03_export_task_detail.png | 视觉文件 | 144681 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/demo-project/prototype/page_png/04_field_permission_config.png | 视觉文件 | 133201 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/demo-project/prototype/page_png/05_audit_log.png | 视觉文件 | 155617 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/demo-project/prototype/page_png/prototype_contact_sheet.png | 视觉文件 | 219403 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/demo-project/prototype/ui_style_direction.json | JSON 数据 | 3566 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/demo-project/prototype/ui_style_direction.md | Markdown 文档 | 1821 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/demo-project/runs/governance-baseline/harness_report.json | JSON 数据 | 1039 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/demo-project/runs/governance-baseline/manifest.json | JSON 数据 | 174 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/demo-project/runs/governance-baseline/random_audit_report.json | JSON 数据 | 194 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/demo-project/runs/governance-baseline/trace.json | JSON 数据 | 133 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/demo-project/runs/pipeline-latest/efficiency_report.json | JSON 数据 | 1779 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/demo-project/runs/pipeline-latest/eval_suite_report.json | JSON 数据 | 254 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/demo-project/runs/pipeline-latest/harness_report.json | JSON 数据 | 2751 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/demo-project/runs/pipeline-latest/manifest.json | JSON 数据 | 793 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/demo-project/runs/pipeline-latest/random_audit_report.json | JSON 数据 | 291 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/demo-project/runs/pipeline-latest/real_output_eval_status.json | JSON 数据 | 248 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/demo-project/runs/pipeline-latest/skill_generalization_audit.json | JSON 数据 | 329 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/demo-project/runs/pipeline-latest/trace.json | JSON 数据 | 969 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |

### 归档和审批后可清理候选 (`delete_after_approval`)
- 文件数：`5`
| 路径 | 类型 | 大小 | 审批后是否可清理 | 原因 |
| --- | --- | --- | --- | --- |
| projects/demo-project/01_requirement_brief.meta.json | 生成元数据 | 154 | 是 | 生成元数据通常可复现，核心产物归档后可列为清理候选。 |
| projects/demo-project/02_prd.generated.meta.json | 生成元数据 | 152 | 是 | 生成元数据通常可复现，核心产物归档后可列为清理候选。 |
| projects/demo-project/03_user_stories.generated.meta.json | 生成元数据 | 156 | 是 | 生成元数据通常可复现，核心产物归档后可列为清理候选。 |
| projects/demo-project/04_risk_check.generated.meta.json | 生成元数据 | 153 | 是 | 生成元数据通常可复现，核心产物归档后可列为清理候选。 |
| projects/demo-project/05_tracking_plan.generated.meta.json | 生成元数据 | 157 | 是 | 生成元数据通常可复现，核心产物归档后可列为清理候选。 |

### 需要人工审核 (`manual_review`)
- 文件数：`3`
| 路径 | 类型 | 大小 | 审批后是否可清理 | 原因 |
| --- | --- | --- | --- | --- |
| projects/demo-project/04_risk_check.md | Markdown 文档 | 148 | 否 | 未注册文件，任何清理决定前都需要人工审核。 |
| projects/demo-project/05_tracking_plan.md | Markdown 文档 | 107 | 否 | 未注册文件，任何清理决定前都需要人工审核。 |
| projects/demo-project/06_review_merge.md | Markdown 文档 | 112 | 否 | 未注册文件，任何清理决定前都需要人工审核。 |

### 保留项目状态记录 (`retain_project_record`)
- 文件数：`1`
| 路径 | 类型 | 大小 | 审批后是否可清理 | 原因 |
| --- | --- | --- | --- | --- |
| projects/demo-project/project_state.json | JSON 数据 | 1008 | 否 | 项目状态文件是本地生命周期指针，必须保留。 |

### 保留到经验沉淀完成 (`retain_until_distilled`)
- 文件数：`2`
| 路径 | 类型 | 大小 | 审批后是否可清理 | 原因 |
| --- | --- | --- | --- | --- |
| projects/demo-project/02_prd.final.md | Markdown 文档 | 587 | 否 | 人工修订后的 final 产物是高价值学习证据，应保留到沉淀完成。 |
| projects/demo-project/03_user_stories.final.md | Markdown 文档 | 319 | 否 | 人工修订后的 final 产物是高价值学习证据，应保留到沉淀完成。 |

## 清理前必须审批
- [ ] 你确认项目已经可以收口。
- [ ] 你已审核 `closeout-report.md`。
- [ ] `architecture-feedback.md` 里的建议已被接受、拒绝或转成受监督 GitHub 变更。
- [ ] 原始输入的归档 / 隐藏敏感信息 / 保留策略已确认。
- [ ] 项目偏好缓存处理方式已确认。
- [ ] 归档目标已确认。
- [ ] 所有硬删除候选已经满足归档后 30 天。
- [ ] 硬删除前已完成第二次精确清单审批。
