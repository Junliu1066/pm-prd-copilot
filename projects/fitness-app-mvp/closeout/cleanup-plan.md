# 清理计划 - fitness-app-mvp

- 生成时间：`2026-04-29T03:36:25+00:00`
- 模式：只生成预览，不执行清理
- 本次没有删除、移动、归档、覆盖、提交或推送任何文件。
- 真正执行清理必须经过你明确批准，并且应该作为单独命令执行。
- 保留规则：先归档，硬删除至少等归档后 30 天，并且仍需你二次确认精确清单。

## 允许讨论清理的范围
- `projects/fitness-app-mvp/`
- `memory-cache/projects/fitness-app-mvp/`，仅在项目偏好缓存审核后处理

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
| projects/fitness-app-mvp/00_raw_input.md | Markdown 文档 | 1010 | 否 | 原始输入可能包含项目特定或敏感上下文，只能在监督下归档。 |

### 沉淀后归档，再考虑清理 (`archive_then_cleanup_after_distillation`)
- 文件数：`44`
| 路径 | 类型 | 大小 | 审批后是否可清理 | 原因 |
| --- | --- | --- | --- | --- |
| projects/fitness-app-mvp/01_requirement_brief.json | JSON 数据 | 6232 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/fitness-app-mvp/01_requirement_brief.md | Markdown 文档 | 4049 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/fitness-app-mvp/02_prd.generated.json | JSON 数据 | 13471 | 是 | 生成产物应保留到有用经验提取完成后再考虑归档清理。 |
| projects/fitness-app-mvp/02_prd.generated.md | Markdown 文档 | 22247 | 是 | 生成产物应保留到有用经验提取完成后再考虑归档清理。 |
| projects/fitness-app-mvp/03_user_stories.generated.json | JSON 数据 | 7629 | 是 | 生成产物应保留到有用经验提取完成后再考虑归档清理。 |
| projects/fitness-app-mvp/03_user_stories.generated.md | Markdown 文档 | 7051 | 是 | 生成产物应保留到有用经验提取完成后再考虑归档清理。 |
| projects/fitness-app-mvp/04_risk_check.generated.json | JSON 数据 | 13746 | 是 | 生成产物应保留到有用经验提取完成后再考虑归档清理。 |
| projects/fitness-app-mvp/04_risk_check.generated.md | Markdown 文档 | 10896 | 是 | 生成产物应保留到有用经验提取完成后再考虑归档清理。 |
| projects/fitness-app-mvp/05_tracking_plan.generated.json | JSON 数据 | 13826 | 是 | 生成产物应保留到有用经验提取完成后再考虑归档清理。 |
| projects/fitness-app-mvp/05_tracking_plan.generated.md | Markdown 文档 | 10465 | 是 | 生成产物应保留到有用经验提取完成后再考虑归档清理。 |
| projects/fitness-app-mvp/analysis/competitor_gap.json | JSON 数据 | 16195 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/fitness-app-mvp/analysis/mvp_scope.json | JSON 数据 | 7361 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/fitness-app-mvp/analysis/pain_needs.json | JSON 数据 | 6314 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/fitness-app-mvp/analysis/prd_analysis_suite_summary.md | Markdown 文档 | 6103 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/fitness-app-mvp/analysis/scenario_ranking.json | JSON 数据 | 6982 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/fitness-app-mvp/analysis/user_universe.json | JSON 数据 | 11122 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/fitness-app-mvp/prototype/product_flow.md | Markdown 文档 | 4416 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/fitness-app-mvp/prototype/prototype_preview.md | Markdown 文档 | 2675 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/fitness-app-mvp/prototype/prototype_preview.png | 视觉文件 | 255991 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/fitness-app-mvp/prototype/prototype_preview.svg | 视觉文件 | 7791 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/fitness-app-mvp/prototype/reference_analysis.json | JSON 数据 | 2665 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/fitness-app-mvp/runs/governance-baseline/efficiency_report.json | JSON 数据 | 1665 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/governance-baseline/harness_report.json | JSON 数据 | 1438 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/governance-baseline/manifest.json | JSON 数据 | 177 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/governance-baseline/random_audit_report.json | JSON 数据 | 200 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/governance-baseline/trace.json | JSON 数据 | 136 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/plan-execution-preview-20260425/efficiency_report.json | JSON 数据 | 1779 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/plan-execution-preview-20260425/eval_suite_report.json | JSON 数据 | 273 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/plan-execution-preview-20260425/harness_report.json | JSON 数据 | 2281 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/plan-execution-preview-20260425/manifest.json | JSON 数据 | 520 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/plan-execution-preview-20260425/random_audit_report.json | JSON 数据 | 338 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/plan-execution-preview-20260425/real_output_eval_status.json | JSON 数据 | 267 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/plan-execution-preview-20260425/skill_generalization_audit.json | JSON 数据 | 348 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/plan-execution-preview-20260425/trace.json | JSON 数据 | 1000 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/prd-analysis-suite-20260423/efficiency_report.json | JSON 数据 | 1837 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/prd-analysis-suite-20260423/harness_report.json | JSON 数据 | 1590 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/prd-analysis-suite-20260423/manifest.json | JSON 数据 | 632 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/prd-analysis-suite-20260423/random_audit_report.json | JSON 数据 | 322 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/prd-analysis-suite-20260423/trace.json | JSON 数据 | 6224 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/prototype-preview-20260424/efficiency_report.json | JSON 数据 | 1770 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/prototype-preview-20260424/harness_report.json | JSON 数据 | 1718 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/prototype-preview-20260424/manifest.json | JSON 数据 | 516 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/prototype-preview-20260424/random_audit_report.json | JSON 数据 | 331 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/fitness-app-mvp/runs/prototype-preview-20260424/trace.json | JSON 数据 | 1019 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |

### 归档和审批后可清理候选 (`delete_after_approval`)
- 文件数：`5`
| 路径 | 类型 | 大小 | 审批后是否可清理 | 原因 |
| --- | --- | --- | --- | --- |
| projects/fitness-app-mvp/01_requirement_brief.meta.json | 生成元数据 | 539 | 是 | 生成元数据通常可复现，核心产物归档后可列为清理候选。 |
| projects/fitness-app-mvp/02_prd.generated.meta.json | 生成元数据 | 538 | 是 | 生成元数据通常可复现，核心产物归档后可列为清理候选。 |
| projects/fitness-app-mvp/03_user_stories.generated.meta.json | 生成元数据 | 542 | 是 | 生成元数据通常可复现，核心产物归档后可列为清理候选。 |
| projects/fitness-app-mvp/04_risk_check.generated.meta.json | 生成元数据 | 539 | 是 | 生成元数据通常可复现，核心产物归档后可列为清理候选。 |
| projects/fitness-app-mvp/05_tracking_plan.generated.meta.json | 生成元数据 | 543 | 是 | 生成元数据通常可复现，核心产物归档后可列为清理候选。 |

### 需要人工审核 (`manual_review`)
- 文件数：`3`
| 路径 | 类型 | 大小 | 审批后是否可清理 | 原因 |
| --- | --- | --- | --- | --- |
| projects/fitness-app-mvp/04_risk_check.md | Markdown 文档 | 17 | 否 | 未注册文件，任何清理决定前都需要人工审核。 |
| projects/fitness-app-mvp/05_tracking_plan.md | Markdown 文档 | 17 | 否 | 未注册文件，任何清理决定前都需要人工审核。 |
| projects/fitness-app-mvp/06_review_merge.md | Markdown 文档 | 17 | 否 | 未注册文件，任何清理决定前都需要人工审核。 |

### 项目偏好缓存需要人工审核 (`manual_review_project_memory`)
- 文件数：`5`
| 路径 | 类型 | 大小 | 审批后是否可清理 | 原因 |
| --- | --- | --- | --- | --- |
| memory-cache/projects/fitness-app-mvp/cache-20260424T000000+0800/approved_preferences.md | Markdown 文档 | 5264 | 否 | 项目偏好缓存会影响后续工作，清除前必须人工审核。 |
| memory-cache/projects/fitness-app-mvp/cache-20260424T000000+0800/candidate_preferences.md | Markdown 文档 | 728 | 否 | 项目偏好缓存会影响后续工作，清除前必须人工审核。 |
| memory-cache/projects/fitness-app-mvp/cache-20260424T000000+0800/manifest.json | JSON 数据 | 829 | 否 | 项目偏好缓存会影响后续工作，清除前必须人工审核。 |
| memory-cache/projects/fitness-app-mvp/cache-20260424T000000+0800/source_trace.json | JSON 数据 | 4383 | 否 | 项目偏好缓存会影响后续工作，清除前必须人工审核。 |
| memory-cache/projects/fitness-app-mvp/current.json | JSON 数据 | 683 | 否 | 项目偏好缓存会影响后续工作，清除前必须人工审核。 |

### 保留项目状态记录 (`retain_project_record`)
- 文件数：`1`
| 路径 | 类型 | 大小 | 审批后是否可清理 | 原因 |
| --- | --- | --- | --- | --- |
| projects/fitness-app-mvp/project_state.json | JSON 数据 | 511 | 否 | 项目状态文件是本地生命周期指针，必须保留。 |

### 保留到经验沉淀完成 (`retain_until_distilled`)
- 文件数：`2`
| 路径 | 类型 | 大小 | 审批后是否可清理 | 原因 |
| --- | --- | --- | --- | --- |
| projects/fitness-app-mvp/02_prd.final.md | Markdown 文档 | 17 | 否 | 人工修订后的 final 产物是高价值学习证据，应保留到沉淀完成。 |
| projects/fitness-app-mvp/03_user_stories.final.md | Markdown 文档 | 17 | 否 | 人工修订后的 final 产物是高价值学习证据，应保留到沉淀完成。 |

## 清理前必须审批
- [ ] 你确认项目已经可以收口。
- [ ] 你已审核 `closeout-report.md`。
- [ ] `architecture-feedback.md` 里的建议已被接受、拒绝或转成受监督 GitHub 变更。
- [ ] 原始输入的归档 / 隐藏敏感信息 / 保留策略已确认。
- [ ] 项目偏好缓存处理方式已确认。
- [ ] 归档目标已确认。
- [ ] 所有硬删除候选已经满足归档后 30 天。
- [ ] 硬删除前已完成第二次精确清单审批。
