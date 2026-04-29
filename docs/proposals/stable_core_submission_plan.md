# 分区提交前审查与稳定核心冻结草案

- 日期：2026-04-29
- 状态：proposal，尚未执行提交
- 基线快照：生成本文件前 `git status --short` 为 148 项，`67 M`、`4 D`、`77 ??`
- 目标：先冻结稳定核心，再把治理文档、项目产物、候选能力、归档/删除候选分开审核，避免混提交
- 最高优先级：长期稳定可靠
- 禁止动作：本方案不批准 `git add`、commit、push、PR、归档、删除、恢复 root 文件、candidate 转 stable、生命周期 proposal 转 stable policy

## 总体建议

建议先只做提交前审查，不开始提交。

长期稳定角度下，当前最主要风险不是功能缺失，而是 148 项变更混在一个工作区里。下一步应该先把所有变更拆成 5 个可审批次：

| 批次 | 名称 | 建议 |
|---|---|---|
| A | Stable Core 稳定核心候选 | 先审查，未来可最先提交，但提交前还要精确确认范围。 |
| B | Governance Docs 治理文档 | 可单独提交，不和代码/项目产物混在一起。 |
| C | Project Artifacts 项目产物 | 只作为项目证据和 closeout 材料，不进稳定核心提交。 |
| D | Candidate Sandbox 候选能力 | 保持 candidate / detachable，不转 stable。 |
| E | Archive / Delete Candidates 归档与删除候选 | 只保留清单，不执行删除。 |

## A. Stable Core 稳定核心候选

这些文件可以进入稳定核心候选批次，但仍需你确认提交范围。建议先冻结这组，再处理其他批次。

### A1. PRD 主链路与默认治理

| Path | Reason | Submit risk |
|---|---|---|
| `pm-prd-copilot/SKILL.md` | 修正 PRD 默认规则、原型图层、非 AI 模型选型边界。 | 需要确认 wording 不会再次引入旧口径。 |
| `pm-prd-copilot/references/output_style_guide.md` | 输出风格与 PRD 新规则对齐。 | 与模板必须一致。 |
| `pm-prd-copilot/references/prd_pm_2026_playbook.md` | playbook 参考资料更新。 | 需要保留 archive/root 删除说明。 |
| `pm-prd-copilot/templates/prd_template_2026.md` | PRD 模板主链路。 | 高影响，必须随 regression 一起提交。 |
| `shared/schemas/prd_document.schema.json` | PRD schema 与原型图层对齐。 | 高影响，必须和 pipeline/template 同批。 |
| `pm-prd-copilot/scripts/pipeline_common.py` | PRD 结构生成与非 AI 判断。 | 高影响，必须 regression。 |
| `pm-prd-copilot/scripts/prompt_builders.py` | prompt 构建边界。 | 高影响，注意不要过度泛化。 |
| `pm-prd-copilot/scripts/router.py` | 路由策略。 | 需要确认没有绕开 governed path。 |
| `pm-prd-copilot/scripts/run_pipeline.py` | 默认 governed，显式 `--fast-draft`。 | 高影响，必须保留 fast draft 标记。 |
| `pm-prd-copilot/scripts/run_regression.py` | regression 增强。 | 必须和 evals 同步。 |
| `pm-prd-copilot/scripts/governance_trace.py` | governance trace 标记。 | 必须和 pipeline manifest 对齐。 |

### A2. Harness 稳定检查与写入边界

| Path | Reason | Submit risk |
|---|---|---|
| `harness/README.md` | 说明 check-only/write-report 和稳定检查层。 | 文档需要和 CLI 行为一致。 |
| `harness/common.py` | harness 共用逻辑。 | 影响多个 checker。 |
| `harness/run_harness.py` | check-only / write-report 主入口。 | 高影响，必须确认默认不写项目文件。 |
| `harness/workflow_gate_checker.py` | workflow/action/artifact 漂移检查。 | 高影响，防止治理绕过。 |
| `harness/efficiency_auditor.py` | 效率审计。 | 低风险。 |
| `harness/random_audit_inspector.py` | 随机审计。 | 低风险。 |
| `harness/eval_suite_checker.py` | 5 个必要检查之一。 | 稳定保留。 |
| `harness/real_output_eval_checker.py` | 5 个必要检查之一。 | 稳定保留。 |
| `harness/skill_generalization_checker.py` | 5 个必要检查之一。 | 稳定保留。 |
| `harness/prototype_preview_gate_checker.py` | 5 个必要检查之一。 | 稳定保留。 |
| `harness/external_redaction_checker.py` | 5 个必要检查之一。 | 稳定保留。 |

### A3. Eval 与真实输出保护层

| Path | Reason | Submit risk |
|---|---|---|
| `evals/skill_quality_cases.yaml` | PRD 退化、非 AI、原型图层等样例。 | 必须保持覆盖面。 |
| `evals/run_real_output_eval.py` | 真实输出评估。 | 输出文件写入需受控。 |
| `evals/generalization_audit.yaml` | 防止用户偏好错误泛化。 | 与 skill_generalization checker 对齐。 |
| `evals/real_outputs/20260425T000000Z/real_output_eval_report.json` | 当前真实输出基线。 | 属于基线证据，未来更新要有说明。 |
| `evals/real_outputs/20260425T000000Z/summary.md` | 当前真实输出摘要。 | 属于基线证据。 |

### A4. Workflow / Artifact / Steward 合同

| Path | Reason | Submit risk |
|---|---|---|
| `workflow/actions.yaml` | action 合同。 | 高影响，必须和 workflow gate 对齐。 |
| `workflow/policies.yaml` | workflow 政策。 | 中等风险。 |
| `workflow/prd_workflow.yaml` | PRD workflow。 | 高影响，必须和 pipeline governed 对齐。 |
| `registry/artifacts.yaml` | artifact 注册。 | 高影响，影响 trace/source。 |
| `registry/stewards.yaml` | steward 注册。 | 不新增 steward，只修责任边界。 |
| `governance/steward_operating_rules.yaml` | steward 操作规则。 | 需要避免过度流程化。 |
| `governance/teaching_policy.yaml` | teaching / learning 边界。 | 防止长期记忆误写。 |

### A5. B 包、closeout 与长期偏好边界

| Path | Reason | Submit risk |
|---|---|---|
| `pm-prd-copilot/scripts/package_b_delivery.py` | 通用 B 包打包器和 redaction。 | 高影响，需真实项目输出复核。 |
| `pm-prd-copilot/scripts/closeout_project.py` | closeout 预览和架构反哺。 | 只能生成报告，不能清理。 |
| `pm-prd-copilot/rules/distribution_policy.yaml` | B 包分发策略。 | 必须和脚本一致。 |
| `pm-prd-copilot/rules/redaction_terms.yaml` | 外部分发保护词。 | 必须和 redaction checker 对齐。 |
| `pm-prd-copilot/rules/external_redaction_policy.md` | 外部保护策略说明。 | 文档边界。 |
| `pm-prd-copilot/rules/development_document_policy.md` | Codex 开发文档规则。 | 用户已确认“开发文档”默认 Codex 开发文档。 |
| `pm-prd-copilot/rules/agent_embedding_policy.md` | agent 嵌入边界。 | 需要防止外部暴露。 |
| `pm-prd-copilot/rules/codex_internal_governance_policy.md` | 内部治理边界。 | 不得外泄到 B 包。 |
| `pm-prd-copilot/rules/distribution_policy.md` | 分发策略说明。 | 与 YAML 保持一致。 |
| `pm-prd-copilot/templates/codex_development_document_template.md` | Codex 开发文档模板。 | 稳定模板候选。 |
| `pm-prd-copilot/templates/external_protected_development_document_template.md` | 外部保护模板。 | 稳定模板候选。 |
| `pm-prd-copilot/memory/user_preferences.md` | 已批准长期偏好。 | 只能包含明确批准内容。 |

## B. Governance Docs 治理文档批次

这些文件是治理说明、报告和 proposal。建议单独提交，不和 A 批代码混在一起。

| Path | Reason | Submit risk |
|---|---|---|
| `docs/workspace_change_partition.md` | 工作区分区、root 删除项、项目 closeout 索引。 | 审核地图，不是清理许可。 |
| `docs/governance_repair_closeout_report.md` | 总验收报告。 | 审核材料，不是 stable policy。 |
| `docs/proposals/capability_minimality_review.md` | 新增能力最小化审计。 | 审核材料，不是转 stable 许可。 |
| `docs/proposals/governance_lifecycle_policy.md` | 长期治理生命周期 proposal。 | 继续 proposal，先跑 2-4 周校准。 |
| `docs/proposals/prd_structure_change_impact_review.md` | PRD 结构变更影响记录。 | 历史决策证据。 |
| `docs/proposals/prd_visual_and_page_flow_mechanism.md` | PRD 图表/页面流转机制 proposal。 | 需要和当前 PRD 规则对齐。 |
| `docs/architecture-inbox/zero_to_one_prd_quality_feedback.md` | 0-1 PRD 质量反馈收件箱。 | 逐条批准，不整包长期化。 |
| `docs/project_lifecycle.md` | 项目生命周期规则。 | 可作为治理文档候选。 |
| `docs/prototype_flow.md` | 原型链路说明。 | 与用户确认的原型监督链路一致。 |
| `docs/repository_map.md` | 仓库地图。 | 后续可合并 overview 内容，但本批不做。 |
| `docs/scheduled_check_mechanisms.md` | 定时检查机制。 | 自动化只汇报，不执行高风险动作。 |
| `docs/two_round_self_check.md` | 两轮自查机制。 | 与用户要求一致。 |
| `docs/version_model_update_review.md` | 版本/模型更新瘦身审计。 | 与 pruning gate 对齐。 |
| `docs/daily_report_template.md` | 日报/汇报模板。 | 定时任务输出参考。 |
| `docs/error_reports/` | 错误报告目录。 | 项目/治理错误证据，不是稳定规则。 |
| `docs/cleanup_inbox.md` | 清理收件箱。 | 不等于删除许可。 |
| `docs/contract_responsibility_layer.md` | 合同责任层说明。 | 治理说明。 |
| `docs/architecture.md` | 架构说明更新。 | 需和生命周期 proposal 对齐。 |
| `docs/operating_model.md` | 运行模型说明。 | 需和当前治理边界一致。 |
| `teaching/accepted_lessons.md` | 已接受学习记录。 | 不应自动扩写长期偏好。 |
| `teaching/open_lessons.md` | 待确认学习记录。 | 需要保持 pending 边界。 |
| `teaching/teaching_log.md` | teaching 记录。 | 审计材料。 |
| `teaching/user_preferences.md` | 用户偏好记录。 | 需和长期记忆边界一致。 |
| `ai-intel/` | AI 情报和自动化记录。 | 只做汇报输入，不自动改架构。 |

## C. Project Artifacts 项目产物批次

这些只能作为项目证据或 closeout 材料，不得混入稳定核心提交。

| Path / scope | Reason | Recommendation |
|---|---|---|
| `projects/demo-project/` | regression / governance fixture 和生成产物。 | 保留为测试 fixture；不归档，除非有替代 fixture。 |
| `projects/demo-project/closeout/` | demo closeout 五件套。 | 项目证据批次。 |
| `projects/demo-project/prototype/` | demo 原型和 UI 风格产物。 | 项目产物，不进稳定核心。 |
| `projects/fitness-app-mvp/` | 真实项目、分析、原型、偏好缓存关联。 | active / closeout candidate，归档前对齐偏好缓存。 |
| `projects/fitness-app-mvp/closeout/` | fitness closeout 五件套。 | 项目证据批次。 |
| `projects/fitness-app-mvp/prototype/` | fitness 原型预览。 | 项目产物。 |
| `projects/fitness-app-mvp/runs/` | fitness 运行证据。 | 归档前保留。 |
| `memory-cache/` | 项目偏好缓存。 | 只能项目内使用；归档前人工审核。 |
| `projects/taxi-hailing-prd-test/` | 0-1 PRD 质量样例。 | golden sample 候选，不能直接稳定入库。 |
| `projects/ai-collaboration-efficiency-platform/` | 历史 PRD 证据。 | closeout candidate。 |
| `projects/graduation-defense-agent/` | AI、交付、Codex 开发、原型完整包。 | closeout candidate，先审核再归档。 |
| `projects/jiaxiaoqian-ai-invest-research/` | active AI-heavy 项目，含 PRD、开发文档、B 包和原型。 | 保持 active；旧口径延后回扫。 |
| `projects/prompt-optimization-workbench/` | HTML 原型包证据。 | closeout candidate。 |
| `projects/santoip-ai-brand-video/` | HTML 原型包证据。 | closeout candidate。 |

## D. Candidate Sandbox 候选能力批次

这些必须保持 candidate / detachable。提交前必须明确它们不是 Stable Core。

| Path / scope | Reason | Recommendation |
|---|---|---|
| `.agents/plugins/marketplace.json` | candidate plugin 可见性和非稳定标识。 | 只能和 candidate plugin 批次一起审，避免引用不存在的 plugin。 |
| `registry/plugins.yaml` | plugin 注册状态。 | 与 plugin suite 同批审，不混入 A。 |
| `registry/skills.yaml` | candidate skill 状态。 | 与 plugin suite 同批审。 |
| `plugins/ai-solution-planning-suite/` | AI solution candidate suite。 | 保持 detachable。 |
| `plugins/delivery-planning-suite/` | delivery planning candidate suite。 | 保持 detachable。 |
| `plugins/prd-prototype-suite/` | prototype candidate suite。 | 保持 detachable。 |
| `plugins/preference-memory-suite/` | preference memory candidate suite。 | 项目内使用，不跨项目。 |
| `plugins/quality-evaluation-suite/` | quality evaluation candidate suite。 | 对应 eval/harness 可稳定，plugin 仍 candidate。 |
| `harness/delivery_plan_checker.py` | 按需 delivery 检查。 | 不进入默认稳定检查层。 |
| `harness/ai_solution_checker.py` | 按需 AI solution 检查。 | 不进入默认稳定检查层。 |
| `harness/agentic_delivery_checker.py` | 按需 Codex delivery 检查。 | 不进入默认稳定检查层。 |
| `harness/preference_cache_checker.py` | 项目偏好缓存检查。 | 按项目触发，不作为无缓存项目负担。 |
| `pm-prd-copilot/scripts/manage_preference_cache.py` | 项目偏好缓存工具。 | 保持项目内/归档对齐边界。 |
| `pm-prd-copilot/scripts/package_internal_delivery.py` | 内部包打包器。 | 继续候选，先和真实项目结构对齐。 |
| `pm-prd-copilot/scripts/select_ui_style.py` | UI 风格选择工具。 | UI 阶段候选能力。 |
| `pm-prd-copilot/ui-design/` | UI 风格库和 prompt。 | 候选能力，不反向污染 PRD 主链路。 |
| `pm-prd-copilot/proposals/skill-patches/` | skill update proposals。 | 候选学习材料，不自动应用。 |

## E. Archive / Delete Candidates 归档与删除候选批次

这些只能保留清单，不执行删除。

| Path / scope | Reason | Recommendation |
|---|---|---|
| `prd_pm_2026_playbook.md` | root 删除项，有 canonical 和 archive。 | 接受删除候选，但不提交删除状态，待逐项确认。 |
| `prd_template_2026.md` | root 删除项，有 canonical 和 archive。 | 接受删除候选，但不提交删除状态，待逐项确认。 |
| `prd_skill_kit_2026.zip` | root 删除项，只有 archive。 | 不恢复 root；30 天后仍需精确审批。 |
| `skill_suite_overview.md` | root 删除项，只有 archive。 | 先保留 archive，后续决定是否提取到 repository map。 |
| `docs/archive/` | archive evidence。 | 只作为归档证据，不硬删除。 |
| `projects/_archives/` | 项目归档区。 | 本轮不移动项目进去。 |
| `evals/__pycache__/` | 运行缓存。 | 30 天后清理候选；本轮不删除。 |

## 需要用户干预的决策

| Decision | Option A | Option B | Option C | Recommended |
|---|---|---|---|---|
| 生命周期方案是否转 stable policy | 现在转，约束立刻生效，但可能过早固化。 | 继续 proposal，跑 2-4 周校准判断一致率。 | 不推进，继续人工临时判断。 | B |
| 5 个必要检查是否进入稳定核心批次 | 进入，防复发能力强。 | 只保留文档确认，执行层不固定。 | 移回 candidate，最轻但风险回潮。 | A |
| candidate plugin 是否随稳定批次提交 | 混入 A，快但边界差。 | 单独 D 批次，边界清楚。 | 暂不处理，保留工作区杂乱。 | B |
| 项目 closeout 是否提交 | 全部提交，信息完整但噪音大。 | 分项目审核提交。 | 暂不提交，工作区继续堆积。 | B |
| root 删除项是否提交删除状态 | 接受删除，根目录干净但需确信 archive/canonical。 | 暂不提交删除状态，最稳但遗留状态。 | 恢复 root 文件，根目录继续乱。 | B |
| golden sample 候选是否入稳定批次 | 现在入，快但易过拟合。 | 保持项目候选，稳但样例库推进慢。 | 做通用脱敏版后入，最适合长期。 | C |
| 历史 PRD 是否现在回扫 | 批量回扫，风险高。 | 只选活跃项目，可控。 | 延后，先冻结稳定核心。 | C |
| 是否开始 git add / commit | 现在开始，快但风险高。 | 先出精确提交计划。 | 继续不提交，工作区继续堆积。 | B |

## 建议的执行顺序

1. 你先审核本文件。
2. 下一步如果继续推进，只生成“精确提交计划”，仍不 `git add`。
3. 精确提交计划通过后，再按批次准备 staging 清单。
4. 每个批次 staging 前跑 `git diff --check`、regression、harness check-only。
5. 每个批次单独提交，避免混合架构、项目产物和 candidate 能力。

## 本方案当前不执行

- 不 `git add`。
- 不 commit / push / PR。
- 不归档项目。
- 不删除或恢复 root 文件。
- 不清空偏好缓存。
- 不把 candidate plugin 转 stable。
- 不把生命周期 proposal 转 stable policy。
- 不把 golden sample 正式入库。
