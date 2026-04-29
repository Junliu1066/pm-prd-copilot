# 精确提交计划与人工决策清单

- 日期：2026-04-29
- 状态：proposal / 审核材料，尚未 staging、commit、push 或归档
- 基线快照：生成本文件前 `git status --short` 为 148 项，包含 `67 M`、`4 D`、`77 ??`
- 最高原则：长期稳定可靠优先；如无必要，不增 skill，不增 harness
- 当前动作边界：本文件只给提交计划，不批准提交、删除、恢复、归档、清空偏好缓存或 candidate 转 stable

## 结论

当前不建议直接 `git add .`。建议先把工作区拆成 A/B/C/D/E 五个批次，再把 A 批 Stable Core 拆成 4 个未来提交单元。

推荐顺序：

1. 先审核并冻结 A 批 Stable Core 的范围。
2. A 批通过后，按 A1 -> A2 -> A3 -> A4 分别准备 staging。
3. B 批治理文档单独审，避免和代码混交。
4. C 批项目产物按项目逐个审，不进入稳定核心。
5. D 批 candidate 能力继续保持候选，不随 A 批转 stable。
6. E 批归档/删除候选只保留清单，不提交删除状态，除非你逐项确认。

## 批次总览

| Batch | Name | Current treatment | Why |
|---|---|---|---|
| A | Stable Core 稳定核心候选 | 可优先审核，未来分单元提交 | 直接影响 PRD 主链路、governed pipeline、harness 边界和必要质量检查。 |
| B | Governance Docs 治理文档 | 单独审核/单独提交 | 是说明、报告、proposal 和监督材料，不应和代码逻辑混在一个提交里。 |
| C | Project Artifacts 项目产物 | 分项目 closeout 审核 | 是项目证据、运行产物、原型、缓存，不应进入稳定架构提交。 |
| D | Candidate Sandbox 候选能力 | 保持 candidate / detachable | plugin、按需 checker、UI/AI 扩展不能被误认为 stable。 |
| E | Archive / Delete Candidates 归档与删除候选 | 只保留清单 | root 删除和 archive 需要你逐项监督。 |

## A 批：Stable Core 未来提交单元

### A1. PRD 主链路与输出口径

建议未来提交主题：`stabilize-prd-generation-contract`

文件清单：

| Path | Reason |
|---|---|
| `pm-prd-copilot/SKILL.md` | 修正稳定 skill 里的 PRD 默认口径：图表按章节、PRD 包含页面说明/跳转/原型图层、非 AI 不强制模型选型。 |
| `pm-prd-copilot/references/output_style_guide.md` | 防止 style guide 把输出拉回旧口径。 |
| `pm-prd-copilot/references/prd_pm_2026_playbook.md` | PRD playbook 参考资产的 canonical copy。 |
| `pm-prd-copilot/templates/prd_template_2026.md` | PRD 模板主入口。 |
| `shared/schemas/prd_document.schema.json` | PRD 结构合同。 |
| `pm-prd-copilot/scripts/pipeline_common.py` | PRD 内容组织、章节与条件输出逻辑。 |
| `pm-prd-copilot/scripts/prompt_builders.py` | PRD prompt 规则入口。 |
| `pm-prd-copilot/scripts/router.py` | 项目类型/输出模式路由。 |

为什么能放一起：这些文件共同决定 PRD 输出结构和默认口径，必须一起看，否则容易出现模板、schema、prompt、脚本互相打架。

不能混入：

- `projects/*` 生成结果。
- `plugins/*` candidate suite。
- `harness/*_checker.py` 新增候选检查。
- root 删除项。

风险：

- PRD 输出口径是高影响变更，如果 wording 不准，会继续造成“集中可视化层”“默认线框图”“非 AI 强行模型选型”等回潮。
- schema 与模板不一致会让 pipeline 生成结果和检查结果冲突。

回滚方式：

- 只回滚 A1 文件，不动项目产物和候选 plugin。
- 如果回滚后 regression 失败，再单独处理 pipeline/schema 兼容问题。

提交前检查：

```bash
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

需要你确认：

- PRD 必须保留“页面说明、页面跳转关系、原型图层”这一稳定方向。
- 非 AI 项目不写 AI 模型选型；AI 项目按项目判断。

### A2. Pipeline / Workflow / Harness 治理合同

建议未来提交主题：`enforce-governed-pipeline-and-workflow-contract`

文件清单：

| Path | Reason |
|---|---|
| `pm-prd-copilot/scripts/run_pipeline.py` | 默认 governed，显式 `--fast-draft` 才能绕过审批。 |
| `pm-prd-copilot/scripts/governance_trace.py` | manifest / trace 写入 governance mode 和审批标记。 |
| `pm-prd-copilot/scripts/run_regression.py` | 回归验证 default governed、fast draft 和旧 `--governed` 兼容。 |
| `workflow/actions.yaml` | action 合同注册。 |
| `workflow/policies.yaml` | workflow 政策。 |
| `workflow/prd_workflow.yaml` | PRD workflow 阶段和审批门禁。 |
| `registry/artifacts.yaml` | artifact 合同，包含 raw input、输出和保留边界。 |
| `registry/stewards.yaml` | steward 责任注册。 |
| `governance/steward_operating_rules.yaml` | steward 操作规则。 |
| `governance/teaching_policy.yaml` | teaching / learning / 长期记忆边界。 |
| `harness/README.md` | harness 模式说明。 |
| `harness/common.py` | harness 共用读写边界。 |
| `harness/run_harness.py` | `--check-only` 与 `--write-report` 行为。 |
| `harness/workflow_gate_checker.py` | workflow/action/artifact 漂移检查。 |
| `harness/efficiency_auditor.py` | 效率审计。 |
| `harness/random_audit_inspector.py` | 随机审计。 |

为什么能放一起：这一组解决同一个问题：workflow 写得完整，但 pipeline 或 harness 不能绕过合同。pipeline、workflow、registry、harness 必须一起验证。

不能混入：

- PRD 具体项目输出。
- candidate plugin suite。
- 按需 checker 稳定化之外的新增能力。
- `.github/workflows/*` 自动化配置，除非另开自动化提交单元。

风险：

- governed 默认会让缺审批项目被阻断，这是正确行为，但可能影响旧测试项目。
- harness 如果默认写文件，会污染项目产物；必须确认 check-only 默认生效。

回滚方式：

- 如果 pipeline 阻断过严，先回滚 `run_pipeline.py` 和 `run_regression.py` 的 governed 默认改动，再复查 workflow gate。
- 不回滚项目生成文件。

提交前检查：

```bash
python3 -m py_compile pm-prd-copilot/scripts/run_pipeline.py pm-prd-copilot/scripts/run_regression.py harness/run_harness.py harness/workflow_gate_checker.py
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

需要你确认：

- 正式 pipeline 默认 governed。
- fast draft 只能显式 `--fast-draft`。
- 日常/CI 检查默认 `--check-only`，不写项目报告。

### A3. 5 个必要检查与 eval 基线

建议未来提交主题：`stabilize-essential-prd-quality-checks`

文件清单：

| Path | Reason |
|---|---|
| `harness/eval_suite_checker.py` | 5 个必要检查之一，防 PRD 退化。 |
| `harness/real_output_eval_checker.py` | 5 个必要检查之一，检查真实输出。 |
| `harness/skill_generalization_checker.py` | 5 个必要检查之一，防错误泛化长期规则。 |
| `harness/prototype_preview_gate_checker.py` | 5 个必要检查之一，防原型越权。 |
| `harness/external_redaction_checker.py` | 5 个必要检查之一，防 B 包/外部分发泄漏。 |
| `evals/skill_quality_cases.yaml` | 质量 case 基线。 |
| `evals/generalization_audit.yaml` | 泛化审计基线。 |
| `evals/run_real_output_eval.py` | 真实输出 eval 入口。 |
| `evals/real_outputs/20260425T000000Z/summary.md` | 真实输出基线摘要。 |
| `evals/real_outputs/20260425T000000Z/real_output_eval_report.json` | 真实输出基线报告。 |
| `evals/real_outputs/20260425T000000Z/cases/b2b_saas_approval_workflow/output.md` | 真实输出样例。 |
| `evals/real_outputs/20260425T000000Z/cases/education_exam_memo_tool/output.md` | 真实输出样例。 |
| `evals/real_outputs/20260425T000000Z/cases/fitness_training_app/output.md` | 真实输出样例。 |
| `evals/real_outputs/20260425T000000Z/cases/pet_store_service_growth/output.md` | 真实输出样例。 |
| `evals/real_outputs/20260425T000000Z/cases/prompt_ops_platform/output.md` | 真实输出样例。 |

为什么能放一起：用户已确认这 5 个检查稳定保留；eval 基线是它们的证据和回归材料。

不能混入：

- `harness/delivery_plan_checker.py`
- `harness/ai_solution_checker.py`
- `harness/agentic_delivery_checker.py`
- `harness/preference_cache_checker.py`
- candidate plugin suite。

风险：

- 过多检查会增加维护成本；本单元只允许已确认的 5 个必要检查。
- eval 基线如果过拟合某个测试项目，会让长期判断变窄。

回滚方式：

- 如果 A3 造成检查过严，优先调整 eval case 或 checker 阈值，不直接删除稳定检查。
- 如果必须回滚，只回滚 A3 文件，不动 A1/A2。

提交前检查：

```bash
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

需要你确认：

- 这 5 个检查进入稳定核心。
- 未来新增第 6 个检查仍需单独说明必要性。

### A4. B 包、Codex 开发文档、closeout 和偏好边界

建议未来提交主题：`stabilize-delivery-packaging-and-closeout-boundaries`

文件清单：

| Path | Reason |
|---|---|
| `pm-prd-copilot/scripts/package_b_delivery.py` | 通用外部 B 包打包器。 |
| `pm-prd-copilot/scripts/closeout_project.py` | 项目 closeout 预览工具。 |
| `pm-prd-copilot/rules/distribution_policy.yaml` | 分发策略机器可读规则。 |
| `pm-prd-copilot/rules/distribution_policy.md` | 分发策略说明。 |
| `pm-prd-copilot/rules/redaction_terms.yaml` | 外部分发保护词。 |
| `pm-prd-copilot/rules/external_redaction_policy.md` | 外部保护策略。 |
| `pm-prd-copilot/rules/development_document_policy.md` | Codex 开发文档规则。 |
| `pm-prd-copilot/rules/agent_embedding_policy.md` | agent 嵌入边界。 |
| `pm-prd-copilot/rules/codex_internal_governance_policy.md` | 内部治理不可外泄边界。 |
| `pm-prd-copilot/templates/codex_development_document_template.md` | Codex 开发文档模板。 |
| `pm-prd-copilot/templates/external_protected_development_document_template.md` | 外部保护版开发文档模板。 |
| `pm-prd-copilot/memory/user_preferences.md` | 已明确批准的长期偏好。 |

为什么能放一起：这组解决“内部/外部分发、开发文档、closeout、长期偏好”边界。它们共同决定项目结束前怎么总结、怎么保护外部交付物、什么能进入长期记忆。

不能混入：

- `memory-cache/` 项目偏好缓存。
- `projects/*/closeout/` 具体项目 closeout 输出。
- B 包生成出来的 zip。
- `pm-prd-copilot/scripts/package_internal_delivery.py` 候选内部打包器。

风险：

- B 包打包器如果没经过真实项目复核，可能仍带项目假设。
- 长期偏好文件只能写用户明确批准的内容，不能把项目偏好自动写进去。

回滚方式：

- B 包问题优先回滚脚本和规则，不动项目归档。
- 长期偏好如需回滚，必须只删除本次明确加入的条目，不碰历史用户偏好。

提交前检查：

```bash
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

需要你确认：

- B 包脚本可作为通用外部分发打包器继续推进。
- closeout 工具只生成审核材料，不执行归档/删除。
- 项目偏好默认只保留到项目归档；长期记忆逐条批准。

## B 批：Governance Docs 未来提交单元

建议未来提交主题：`document-governance-repair-and-supervision-plan`

文件清单：

| Path / scope | Reason |
|---|---|
| `AGENTS.md` | 仓库级 agent 指令。 |
| `README.md` | 仓库入口说明。 |
| `agent.md` | 项目工作规则。 |
| `docs/workspace_change_partition.md` | 工作区分区、root 删除项、项目 closeout 索引。 |
| `docs/governance_repair_closeout_report.md` | 治理修复总验收报告。 |
| `docs/proposals/capability_minimality_review.md` | 新增能力最小化审计。 |
| `docs/proposals/governance_lifecycle_policy.md` | 长期治理生命周期 proposal。 |
| `docs/proposals/stable_core_submission_plan.md` | 分区提交前审查和稳定核心冻结草案。 |
| `docs/proposals/precise_submission_plan.md` | 本精确提交计划。 |
| `docs/proposals/prd_structure_change_impact_review.md` | PRD 结构变更影响记录。 |
| `docs/proposals/prd_visual_and_page_flow_mechanism.md` | PRD 图表与页面流转机制 proposal。 |
| `docs/architecture-inbox/zero_to_one_prd_quality_feedback.md` | 0-1 PRD 质量反馈收件箱。 |
| `docs/project_lifecycle.md` | 项目生命周期说明。 |
| `docs/prototype_flow.md` | 原型流转说明。 |
| `docs/repository_map.md` | 仓库地图。 |
| `docs/scheduled_check_mechanisms.md` | 定时检查机制。 |
| `docs/two_round_self_check.md` | 两轮自查机制。 |
| `docs/version_model_update_review.md` | 版本/模型更新瘦身审计。 |
| `docs/daily_report_template.md` | 定时汇报模板。 |
| `docs/cleanup_inbox.md` | 清理收件箱。 |
| `docs/contract_responsibility_layer.md` | 合同责任层说明。 |
| `docs/architecture.md` | 架构说明。 |
| `docs/operating_model.md` | 运行模型说明。 |
| `docs/error_reports/README.md` | 错误记录目录说明。 |
| `docs/error_reports/bug_log.md` | 错误日志。 |
| `docs/error_reports/daily/README.md` | 每日错误记录说明。 |
| `docs/error_reports/daily/2026-04-28.md` | 每日错误记录。 |
| `docs/error_reports/daily/2026-04-29.md` | 每日错误记录。 |
| `docs/error_reports/runs/README.md` | 运行错误记录说明。 |
| `docs/error_reports/runs/2026-04-28-governance-system-test.md` | 运行错误记录。 |
| `docs/error_reports/runs/2026-04-28-initial-error-check-setup.md` | 运行错误记录。 |
| `docs/error_reports/runs/2026-04-28-scheduled-report-solution-update.md` | 运行错误记录。 |
| `teaching/accepted_lessons.md` | 已接受经验。 |
| `teaching/open_lessons.md` | 待确认经验。 |
| `teaching/teaching_log.md` | teaching 日志。 |
| `teaching/user_preferences.md` | teaching 层用户偏好。 |
| `stewards/ai_architecture_steward.md` | 现有 steward 操作协议。 |
| `stewards/ai_coaching_steward.md` | 现有 steward 操作协议。 |
| `stewards/capability_enablement_steward.md` | 现有 steward 操作协议。 |
| `stewards/delivery_planning_steward.md` | 现有 steward 操作协议。 |
| `stewards/development_governance_steward.md` | 现有 steward 操作协议。 |
| `stewards/learning_steward.md` | 现有 steward 操作协议。 |
| `stewards/prototype_design_steward.md` | 现有 steward 操作协议。 |

为什么单独提交：这些是治理说明和监督材料，不直接改变代码运行路径。单独提交后更容易审计，也更容易回滚。

不能混入：

- A 批代码逻辑。
- C 批项目产物。
- D 批 candidate plugin。
- E 批 root 删除状态。

需要你确认：

- 生命周期方案继续 proposal，不转 stable policy。
- 定时监督先做汇报和校准，不自动执行高风险处理。

## C 批：Project Artifacts 分项目审核单元

这批不建议一次性提交。建议按项目逐个审核。

| Project / scope | Recommended treatment | User decision |
|---|---|---|
| `projects/demo-project/` | 保留为 regression/governance fixture；生成物和 run 产物不要和稳定核心混交。 | 是否保留当前 run outputs 作为 fixture evidence。 |
| `projects/demo-project/closeout/` | closeout 五件套，项目证据。 | 是否提交 demo closeout。 |
| `projects/demo-project/prototype/` | demo 原型 PNG/UI 风格输出。 | 是否保留为原型链路样例。 |
| `projects/fitness-app-mvp/` | active / closeout candidate。 | 是否仍 active；归档前先审偏好缓存。 |
| `projects/fitness-app-mvp/closeout/` | closeout 五件套。 | 是否提交 closeout。 |
| `projects/fitness-app-mvp/prototype/` | 原型预览和参考分析。 | 是否保留为项目证据。 |
| `projects/fitness-app-mvp/runs/` | run evidence。 | 是否保留到归档。 |
| `memory-cache/projects/fitness-app-mvp/` | 项目偏好缓存。 | 归档前逐条对齐；不自动长期化。 |
| `projects/taxi-hailing-prd-test/` | 0-1 PRD 质量样例。 | 是否做通用脱敏版后进入样例库。 |
| `projects/ai-collaboration-efficiency-platform/` | 历史 PRD evidence / closeout candidate。 | 是否保留历史证据或进入归档候选。 |
| `projects/graduation-defense-agent/` | AI/delivery/prototype 完整包。 | 是否 active、closeout candidate 或 archive candidate。 |
| `projects/jiaxiaoqian-ai-invest-research/` | AI-heavy active 项目。 | 保持 active；历史旧口径延后回扫。 |
| `projects/prompt-optimization-workbench/` | HTML prototype evidence。 | 是否 archive after review。 |
| `projects/santoip-ai-brand-video/` | HTML prototype evidence。 | 是否 archive after review。 |
| `projects/_archives/` | 归档区和 delivery package zip。 | 本轮不移动、不删除；后续单独审。 |

C 批提交策略：

- 不建议 `git add projects/`。
- 每个项目单独审，单独决定是否提交 closeout、原型、run 产物或 archive 证据。
- 没有 closeout 的项目不能进入归档。
- 项目偏好缓存不能跨项目复用，不能自动写长期记忆。

## D 批：Candidate Sandbox 候选能力审核单元

这批不能和 A 批稳定核心一起提交。即使提交，也必须标题和说明标为 candidate。

| Path / scope | Recommended treatment | Reason |
|---|---|---|
| `.agents/plugins/marketplace.json` | D 批候选能力可见性配置。 | candidate 可见但必须标非稳定。 |
| `registry/plugins.yaml` | D 批候选 plugin 注册。 | 与 plugin suite 同批审。 |
| `registry/skills.yaml` | D 批 skill 状态。 | 防止 candidate 被当 stable。 |
| `plugins/ai-solution-planning-suite/` | 保持 detachable candidate。 | AI solution 不进入主 PRD workflow。 |
| `plugins/delivery-planning-suite/` | 保持 detachable candidate。 | 交付规划按需触发。 |
| `plugins/prd-prototype-suite/` | 保持 detachable candidate。 | 原型能力不反向污染 PRD 主链路。 |
| `plugins/preference-memory-suite/` | 保持 detachable candidate。 | 项目偏好只项目内，不跨项目。 |
| `plugins/quality-evaluation-suite/` | 保持 detachable candidate。 | 5 个检查可 stable，plugin 仍 candidate。 |
| `harness/delivery_plan_checker.py` | 按需 checker。 | 不进入默认稳定检查层。 |
| `harness/ai_solution_checker.py` | 按需 checker。 | 不进入默认稳定检查层。 |
| `harness/agentic_delivery_checker.py` | 按需 checker。 | 不进入默认稳定检查层。 |
| `harness/preference_cache_checker.py` | 按项目触发 checker。 | 有偏好缓存的项目才需要。 |
| `pm-prd-copilot/scripts/manage_preference_cache.py` | 项目偏好缓存工具。 | 只能项目内使用，归档前对齐。 |
| `pm-prd-copilot/scripts/package_internal_delivery.py` | 内部包候选工具。 | 还需多项目验证。 |
| `pm-prd-copilot/scripts/select_ui_style.py` | UI 风格选择候选工具。 | UI 阶段使用，不进入 PRD 必需链。 |
| `pm-prd-copilot/ui-design/NOTICE.md` | UI 设计候选资产。 | candidate 说明。 |
| `pm-prd-copilot/ui-design/README.md` | UI 设计候选资产。 | candidate 说明。 |
| `pm-prd-copilot/ui-design/data/visual_style_catalog.json` | UI 风格目录。 | 后续 UI 阶段使用。 |
| `pm-prd-copilot/ui-design/prompts/ui_quality_reviewer.md` | UI 质量 review prompt。 | candidate。 |
| `pm-prd-copilot/ui-design/prompts/ui_style_selector.md` | UI 风格选择 prompt。 | candidate。 |
| `pm-prd-copilot/proposals/skill-patches/` | skill patch proposals。 | 只作为 proposal，不自动应用。 |

D 批风险：

- 如果和 A 批一起提交，后续 worker 可能误以为 candidate 已稳定。
- plugin suite 文件很多，必须避免和主链路修复混在一起。

需要你确认：

- candidate plugin 继续可见但不 stable。
- 是否需要在 marketplace 文案里进一步加强“需审核 / 非稳定能力”。

## E 批：Archive / Delete Candidates 审核单元

这批只保留审核清单，不建议现在提交删除状态。

| Path / scope | Current status | Recommended treatment |
|---|---|---|
| `prd_pm_2026_playbook.md` | root deleted | 有 canonical 和 archive；暂不提交删除状态，等你确认。 |
| `prd_template_2026.md` | root deleted | 有 canonical 和 archive；暂不提交删除状态，等你确认。 |
| `prd_skill_kit_2026.zip` | root deleted | 有 archive，无 canonical；不恢复 root，30 天后再审硬删除。 |
| `skill_suite_overview.md` | root deleted | 有 archive，无 canonical；后续决定是否提取到 `docs/repository_map.md`。 |
| `docs/archive/README.md` | archive 说明 | 可作为 B/E 审核材料，不能代表硬删除许可。 |
| `docs/archive/root-files/prd_pm_2026_playbook.md` | archive copy | 保留。 |
| `docs/archive/root-files/prd_template_2026.md` | archive copy | 保留。 |
| `docs/archive/root-files/prd_skill_kit_2026.zip` | archive copy | 保留。 |
| `docs/archive/root-files/skill_suite_overview.md` | archive copy | 保留。 |
| `docs/archive/root-files/Remod开发.md` | archive copy | 后续确认来源和保留价值。 |
| `docs/archive/notes/答辩.md` | archive note | 后续确认是否项目相关。 |

E 批禁止动作：

- 不恢复 root 文件。
- 不删除 archive copy。
- 不提交 root 删除状态。
- 不把 zip 放回 root。
- 不把 overview 合并进 repository map。

需要你确认：

- 哪些 root 删除项接受删除状态。
- 哪些 archive copy 进入 30 天后硬删除候选。

## AI 情报与自动化支持

这些文件建议单独作为 B 批子单元，不和 pipeline/harness 代码混交。

| Path / scope | Treatment |
|---|---|
| `ai-intel/README.md` | AI 情报目录说明。 |
| `ai-intel/scripts/summarize_daily.py` | 每日汇总脚本。 |
| `ai-intel/scripts/update_decision_matrix.py` | 决策矩阵更新脚本。 |
| `ai-intel/daily/.gitkeep` | 目录占位。 |
| `ai-intel/weekly/.gitkeep` | 目录占位。 |
| `ai-intel/events/.gitkeep` | 目录占位。 |
| `ai-intel/logs/.gitkeep` | 目录占位。 |
| `ai-intel/raw/.gitkeep` | 目录占位。 |
| `ai-intel/decisions/governance-architecture-signals.md` | AI 情报反哺候选。 |
| `.github/workflows/regression.yml` | 自动化回归配置。 |
| `.github/workflows/skill-upgrade-review.yml` | skill/model update 审查自动化。 |

需要你确认：

- 自动化只做汇报和 check-only。
- 不自动修改长期规则、不自动删除、不自动提交。

## 需要你拍板的事项

| Decision | Option A | Option B | Option C | My recommendation |
|---|---|---|---|---|
| 生命周期方案是否转 stable policy | 现在转，立刻约束流程，但可能过早固化。 | 继续 proposal，跑 2-4 周校准。 | 暂停推进，只靠人工判断。 | B |
| 5 个必要检查是否进入稳定核心提交 | 进入 A3，防复发能力强。 | 只保留文档确认。 | 移回 candidate。 | A |
| candidate plugin 是否和稳定核心一起提交 | 混入 A，快但边界差。 | 单独 D 批，边界清楚。 | 暂不处理。 | B |
| 项目 closeout 是否提交 | 全部提交，信息完整但噪音大。 | 分项目审核。 | 暂不提交，工作区继续堆积。 | B |
| root 删除项是否提交删除状态 | 接受删除状态，根目录清爽但风险更高。 | 暂不提交删除状态，最稳。 | 恢复 root 文件，根目录继续乱。 | B |
| golden sample 是否入稳定批次 | 直接用项目 final，快但易过拟合。 | 继续项目候选。 | 做通用脱敏版后入样例库。 | C |
| 历史 PRD 是否现在回扫 | 批量回扫，风险高。 | 只回扫活跃项目。 | 延后，先冻结稳定核心。 | C |
| 是否开始 git add / commit | 现在开始，快但风险高。 | 你审核本计划后再按批次 staging。 | 继续完全不提交。 | B |

## 下一步建议

我的建议是先让你审核 A1-A4 的范围。你确认后，下一步才进入“准备 A1 staging 清单”，仍然不是直接提交。

建议执行顺序：

1. 你确认 A1-A4 哪些可以进稳定核心候选。
2. 我输出 A1 的 staging 前 diff 摘要和风险点。
3. 你批准后才 `git add` A1 文件。
4. A1 通过后再处理 A2、A3、A4。
5. B/C/D/E 继续保持分区审核。

## 本轮验证要求

本文件生成后只运行 check-only：

```bash
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

人工自查：

- 只新增本 proposal 文档。
- 没有新增 skill。
- 没有新增 harness。
- 没有新增 workflow stage。
- 没有新增 plugin。
- 没有删除、恢复、移动、归档。
- 没有 `git add`、commit、push、PR。
- 所有高风险动作仍需要你批准。
