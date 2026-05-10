# 清理计划 - graduation-defense-agent

- 生成时间：`2026-04-29T03:36:25+00:00`
- 模式：只生成预览，不执行清理
- 本次没有删除、移动、归档、覆盖、提交或推送任何文件。
- 真正执行清理必须经过你明确批准，并且应该作为单独命令执行。
- 保留规则：先归档，硬删除至少等归档后 30 天，并且仍需你二次确认精确清单。

## 允许讨论清理的范围
- `projects/graduation-defense-agent/`
- `memory-cache/projects/graduation-defense-agent/`，仅在项目偏好缓存审核后处理

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
| projects/graduation-defense-agent/00_raw_input.md | Markdown 文档 | 1064 | 否 | 原始输入可能包含项目特定或敏感上下文，只能在监督下归档。 |

### 沉淀后归档，再考虑清理 (`archive_then_cleanup_after_distillation`)
- 文件数：`53`
| 路径 | 类型 | 大小 | 审批后是否可清理 | 原因 |
| --- | --- | --- | --- | --- |
| projects/graduation-defense-agent/01_requirement_brief.md | Markdown 文档 | 1810 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/02_prd.generated.md | Markdown 文档 | 50794 | 是 | 生成产物应保留到有用经验提取完成后再考虑归档清理。 |
| projects/graduation-defense-agent/ai/adaptive_coaching_plan.md | Markdown 文档 | 2120 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/ai/ai_capability_map.md | Markdown 文档 | 3972 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/ai/ai_solution_review.json | JSON 数据 | 2059 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/ai/ai_technical_architecture.md | Markdown 文档 | 3218 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/ai/conversation_memory_plan.md | Markdown 文档 | 1888 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/ai/learner_profile_model.md | Markdown 文档 | 2081 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/ai/model_selection_plan.md | Markdown 文档 | 11003 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/ai/prompt_architecture.md | Markdown 文档 | 2562 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/ai/rag_architecture.md | Markdown 文档 | 2314 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/delivery/agentic_delivery_plan.md | Markdown 文档 | 4793 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/delivery/capability_enablement_plan.md | Markdown 文档 | 4395 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/delivery/codex_development_document.md | Markdown 文档 | 6872 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/delivery/codex_development_plan.md | Markdown 文档 | 9845 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/delivery/codex_development_review.md | Markdown 文档 | 10844 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/delivery/codex_task_package_blueprint.md | Markdown 文档 | 5366 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/delivery/codex_task_packages.md | Markdown 文档 | 6514 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/delivery/delivery_plan.md | Markdown 文档 | 3078 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/delivery/delivery_quality_report.json | JSON 数据 | 1322 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/delivery/development_governance_report.json | JSON 数据 | 2651 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/delivery/development_operating_system_plan.md | Markdown 文档 | 2872 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/delivery/effort_estimate.md | Markdown 文档 | 2555 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/delivery/final_codex_plan.md | Markdown 文档 | 5393 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/delivery/human_supervision_plan.md | Markdown 文档 | 2005 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/delivery/phase_1_codex_plan.md | Markdown 文档 | 7103 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/delivery/phase_2_codex_plan.md | Markdown 文档 | 4866 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/delivery/phase_3_codex_plan.md | Markdown 文档 | 4787 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/delivery/release_roadmap.md | Markdown 文档 | 2274 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/delivery/skill_mcp_routing_plan.md | Markdown 文档 | 3677 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/delivery/technical_scope.md | Markdown 文档 | 3908 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/feature_matrix.md | Markdown 文档 | 9855 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/prototype/full_prototype.md | Markdown 文档 | 5383 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/prototype/full_prototype.png | 视觉文件 | 3836711 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/graduation-defense-agent/prototype/full_prototype.svg | 视觉文件 | 39024 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/graduation-defense-agent/prototype/full_prototype.svg.png | 视觉文件 | 2494581 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/graduation-defense-agent/prototype/full_prototype_dark.md | Markdown 文档 | 1900 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/graduation-defense-agent/prototype/full_prototype_dark.png | 视觉文件 | 3836711 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/graduation-defense-agent/prototype/full_prototype_dark.svg | 视觉文件 | 39024 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/graduation-defense-agent/prototype/full_prototype_light.png | 视觉文件 | 879614 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/graduation-defense-agent/prototype/full_prototype_light.svg | 视觉文件 | 36048 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/graduation-defense-agent/prototype/product_flow.md | Markdown 文档 | 6488 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/prototype/prototype_preview.md | Markdown 文档 | 2752 | 是 | 已注册工作流产物，任何清理前都必须先归档。 |
| projects/graduation-defense-agent/prototype/prototype_preview.png | 视觉文件 | 1530310 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/graduation-defense-agent/prototype/prototype_preview.svg | 视觉文件 | 16130 | 是 | 项目过程产物应先审核归档，再考虑清理。 |
| projects/graduation-defense-agent/runs/prd-draft-20260425/efficiency_report.json | JSON 数据 | 2335 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/graduation-defense-agent/runs/prd-draft-20260425/eval_suite_report.json | JSON 数据 | 269 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/graduation-defense-agent/runs/prd-draft-20260425/harness_report.json | JSON 数据 | 2380 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/graduation-defense-agent/runs/prd-draft-20260425/manifest.json | JSON 数据 | 1493 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/graduation-defense-agent/runs/prd-draft-20260425/random_audit_report.json | JSON 数据 | 216 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/graduation-defense-agent/runs/prd-draft-20260425/real_output_eval_status.json | JSON 数据 | 263 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/graduation-defense-agent/runs/prd-draft-20260425/skill_generalization_audit.json | JSON 数据 | 344 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |
| projects/graduation-defense-agent/runs/prd-draft-20260425/trace.json | JSON 数据 | 144 | 是 | 治理运行证据应保留到学习沉淀和审计复核完成。 |

### 需要人工审核 (`manual_review`)
- 文件数：`2`
| 路径 | 类型 | 大小 | 审批后是否可清理 | 原因 |
| --- | --- | --- | --- | --- |
| projects/graduation-defense-agent/.DS_Store | file | 8196 | 否 | 未注册文件，任何清理决定前都需要人工审核。 |
| projects/graduation-defense-agent/00_complete_delivery_package.md | Markdown 文档 | 22714 | 否 | 未注册文件，任何清理决定前都需要人工审核。 |

### 保留项目状态记录 (`retain_project_record`)
- 文件数：`1`
| 路径 | 类型 | 大小 | 审批后是否可清理 | 原因 |
| --- | --- | --- | --- | --- |
| projects/graduation-defense-agent/project_state.json | JSON 数据 | 665 | 否 | 项目状态文件是本地生命周期指针，必须保留。 |

## 清理前必须审批
- [ ] 你确认项目已经可以收口。
- [ ] 你已审核 `closeout-report.md`。
- [ ] `architecture-feedback.md` 里的建议已被接受、拒绝或转成受监督 GitHub 变更。
- [ ] 原始输入的归档 / 隐藏敏感信息 / 保留策略已确认。
- [ ] 项目偏好缓存处理方式已确认。
- [ ] 归档目标已确认。
- [ ] 所有硬删除候选已经满足归档后 30 天。
- [ ] 硬删除前已完成第二次精确清单审批。
