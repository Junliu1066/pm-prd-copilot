# 剩余 Proposal 生命周期处置表

- 日期：2026-05-03
- 状态：proposal 生命周期审计表，不批准删除、移动、归档、push、PR、stable 转正或长期记忆写入。
- 范围：`docs/proposals/*` 中已提交的决策记录和当前剩余未跟踪临时材料。
- 主线任务：记录 17 个治理决策 proposal 已收口，并把剩余临时 proposal 标成受监督的 30 天后删除候选。

## 1. 当前结论

已完成：

```text
09de668 Record governance lifecycle decision proposals
```

该提交只包含 17 个长期追溯价值较高的 proposal 决策记录，不包含项目产物、raw、cache、archive、线程台账或临时 staging / commit 材料。

当前剩余未跟踪 proposal 共 18 个：

1. **临时 staging / commit / L2 审批材料**：16 个。
2. **已被后续材料覆盖的旧候选审查**：2 个。

推荐处理：

1. 临时材料先不删除，统一列入 `delete_after_30_days_candidate`。
2. 两个已覆盖旧审查先不提炼，除非后续需要回看历史判断。
3. 任何删除都必须等 30 天候选期，并经过你二次批准精确清单。

这样做的效果：

- 长期治理判断已入库，不会丢。
- 临时过程材料还保留可追溯性，不会马上误删。
- 后续清理可以按精确清单执行，而不是靠记忆。
- 不需要新增 skill、harness、workflow、automation 或清理脚本。

## 2. 已提交的决策记录

这些文件已在 `09de668` 中提交，后续不再视为未跟踪 proposal：

```text
docs/proposals/ai_intel_raw_lifecycle_disposition.md
docs/proposals/governance_lifecycle_embedding_plan.md
docs/proposals/architecture_self_management_system.md
docs/proposals/archive_notes_lifecycle_disposition.md
docs/proposals/thread_lifecycle_supervision_plan.md
docs/proposals/projects_lifecycle_inventory_review.md
docs/proposals/c6_demo_prototype_artifact_review.md
docs/proposals/c7_fitness_memory_cache_artifact_review.md
docs/proposals/c8_project_artifact_final_disposition_checklist.md
docs/proposals/c9_graduation_defense_closeout_review.md
docs/proposals/c10_jiaxiaoqian_high_value_closeout_review.md
docs/proposals/c11_taxi_hailing_golden_sample_deidentification_plan.md
docs/proposals/c12_ai_collaboration_closeout_refresh_review.md
docs/proposals/c13_prompt_optimization_workbench_low_evidence_review.md
docs/proposals/c14_santoip_brand_video_low_evidence_review.md
docs/proposals/c15_temp_generated_project_disposition_review.md
docs/proposals/c16_project_package_zip_lifecycle_review.md
```

提交含义：

- 记录本轮治理修复中的判断依据。
- 记录项目产物和稳定架构的边界。
- 不批准 stable policy。
- 不批准项目产物提交。
- 不批准删除、归档、长期记忆或 candidate 转 stable。

## 3. 剩余未跟踪 Proposal 分类

### 3.1 临时 staging / commit 材料

这类文件只服务某次暂存、提交前检查或 L2 审批，不适合作为长期治理文档。建议进入 30 天后删除候选，但现在不删除。

| 文件 | 推荐状态 | 原因 | 后续建议 |
|---|---|---|---|
| `docs/proposals/b2_proposal_audit_commit_review.md` | `delete_after_30_days_candidate` | B2 proposal audit 已完成正式提交，该文件只是当时 commit review。 | 满 30 天并二次批准后可删除。 |
| `docs/proposals/b3_teaching_steward_commit_review.md` | `delete_after_30_days_candidate` | B3 teaching / steward 已完成收口，该文件只是 commit review。 | 满 30 天并二次批准后可删除。 |
| `docs/proposals/b3_teaching_steward_content_review_plan.md` | `delete_after_30_days_candidate` | 已被实际内容审查和后续修复覆盖。 | 满 30 天并二次批准后可删除。 |
| `docs/proposals/b3_teaching_steward_staging_list.md` | `delete_after_30_days_candidate` | 只描述当时 staging 范围，已过期。 | 满 30 天并二次批准后可删除。 |
| `docs/proposals/b4_error_reports_commit_review.md` | `delete_after_30_days_candidate` | B4 错误报告证据已完成提交，该文件只是 commit review。 | 满 30 天并二次批准后可删除。 |
| `docs/proposals/b4_error_reports_staging_list.md` | `delete_after_30_days_candidate` | 只描述当时 staging 范围，已过期。 | 满 30 天并二次批准后可删除。 |
| `docs/proposals/b5a_github_workflows_commit_review.md` | `delete_after_30_days_candidate` | 只描述当时 workflow commit 前状态，已过期。 | 满 30 天并二次批准后可删除。 |
| `docs/proposals/b5a_github_workflows_staging_list.md` | `delete_after_30_days_candidate` | 只描述当时 staging 范围，已过期。 | 满 30 天并二次批准后可删除。 |
| `docs/proposals/b5b_candidate_marketplace_staging_list.md` | `delete_after_30_days_candidate` | 已被 D1 candidate plugin registry/source review 和实际提交取代。 | 满 30 天并二次批准后可删除。 |
| `docs/proposals/b5c_ai_intel_commit_review.md` | `delete_after_30_days_candidate` | B5c 已有写入边界审查和 AI intel evidence 提交，该文件只是 commit review。 | 满 30 天并二次批准后可删除。 |
| `docs/proposals/b5c_ai_intel_staging_list.md` | `delete_after_30_days_candidate` | 只描述当时 staging 范围，已过期。 | 满 30 天并二次批准后可删除。 |
| `docs/proposals/c3_demo_fixture_commit_review.md` | `delete_after_30_days_candidate` | demo fixture / run evidence 相关提交已完成，该文件只是 commit review。 | 满 30 天并二次批准后可删除。 |
| `docs/proposals/d1_candidate_plugin_commit_review.md` | `delete_after_30_days_candidate` | D1 candidate plugin 已完成提交，该文件只是 commit review。 | 满 30 天并二次批准后可删除。 |
| `docs/proposals/c11_golden_case_regression_l2_approval_package.md` | `delete_after_30_days_candidate` | C11 golden case + regression 已提交完成，该文件只是 L2 审批材料。 | 可保留到本轮总验收，之后进入 30 天删除候选。 |
| `docs/proposals/c12_c16_project_artifact_review_summary.md` | `delete_after_30_days_candidate` | 汇总 C12-C16 项目审查，详细长期记录已在 C12-C16 单项审查里提交。 | 可保留到本轮总验收，之后进入 30 天删除候选。 |
| `docs/proposals/proposal_decision_record_submission_plan.md` | `delete_after_30_days_candidate` | 只描述 17 个 proposal 决策记录的提交计划，提交已完成。 | 满 30 天并二次批准后可删除。 |

### 3.2 已被后续材料覆盖的旧候选审查

这类材料不建议直接提交原文，避免重复和旧口径混入。

| 文件 | 推荐状态 | 原因 | 后续建议 |
|---|---|---|---|
| `docs/proposals/b5_automation_ai_intel_candidate_review.md` | `superseded_by_later_review` | 已被 B5a workflow、B5b candidate marketplace、B5c AI intel 写入边界和 D1 candidate plugin 审查拆分覆盖。 | 如需保留，只提炼中文总结；否则进入 30 天删除候选。 |
| `docs/proposals/b5b_registry_candidate_alignment_review.md` | `superseded_by_later_review` | 决策已被 D1 candidate plugin registry/source review 和实际提交覆盖。 | 如需保留，只提炼中文总结；否则进入 30 天删除候选。 |

## 4. 30 天删除候选精确清单

当前日期为 2026-05-03。以下文件只进入候选清单，不执行删除。最早复核日建议为：

```text
2026-06-02
```

复核前置条件：

- 本轮治理总验收报告已经完成，确认不再需要这些过程材料。
- 用户逐条或整批批准删除。
- 删除前再次运行 `git status --short docs/proposals`，确认路径仍是预期临时材料。
- 删除后运行 `git diff --check`、regression、harness check-only。

### 4.1 可直接列入 30 天删除候选

| 路径 | 候选原因 | 最早复核日 | 删除前审批 |
|---|---|---|---|
| `docs/proposals/b2_proposal_audit_commit_review.md` | 已完成 B2 commit，只是历史 commit review。 | 2026-06-02 | 需要 |
| `docs/proposals/b3_teaching_steward_commit_review.md` | 已完成 B3 commit，只是历史 commit review。 | 2026-06-02 | 需要 |
| `docs/proposals/b3_teaching_steward_content_review_plan.md` | 已被 B3 内容审查和修复覆盖。 | 2026-06-02 | 需要 |
| `docs/proposals/b3_teaching_steward_staging_list.md` | 已过期 staging 清单。 | 2026-06-02 | 需要 |
| `docs/proposals/b4_error_reports_commit_review.md` | 已完成 B4 commit，只是历史 commit review。 | 2026-06-02 | 需要 |
| `docs/proposals/b4_error_reports_staging_list.md` | 已过期 staging 清单。 | 2026-06-02 | 需要 |
| `docs/proposals/b5a_github_workflows_commit_review.md` | 已完成 B5a commit，只是历史 commit review。 | 2026-06-02 | 需要 |
| `docs/proposals/b5a_github_workflows_staging_list.md` | 已过期 staging 清单。 | 2026-06-02 | 需要 |
| `docs/proposals/b5b_candidate_marketplace_staging_list.md` | 已被 D1 candidate plugin 提交取代。 | 2026-06-02 | 需要 |
| `docs/proposals/b5c_ai_intel_commit_review.md` | 已完成 B5c evidence 提交，只是历史 commit review。 | 2026-06-02 | 需要 |
| `docs/proposals/b5c_ai_intel_staging_list.md` | 已过期 staging 清单。 | 2026-06-02 | 需要 |
| `docs/proposals/c3_demo_fixture_commit_review.md` | demo fixture / run evidence 已提交，只是历史 commit review。 | 2026-06-02 | 需要 |
| `docs/proposals/d1_candidate_plugin_commit_review.md` | D1 candidate plugin 已提交，只是历史 commit review。 | 2026-06-02 | 需要 |
| `docs/proposals/c11_golden_case_regression_l2_approval_package.md` | C11 已提交完成，只是 L2 审批包。 | 2026-06-02 | 需要 |
| `docs/proposals/c12_c16_project_artifact_review_summary.md` | 详细记录已在 C12-C16 单项审查里提交，汇总只服务本轮审核。 | 2026-06-02 | 需要 |
| `docs/proposals/proposal_decision_record_submission_plan.md` | 17 个决策记录已提交，该计划已完成使命。 | 2026-06-02 | 需要 |

### 4.2 条件删除候选

这 2 个文件先不提炼，除非后续需要回看历史判断。若 30 天内没有使用，也可进入删除候选。

| 路径 | 当前状态 | 最早复核日 | 删除前审批 |
|---|---|---|---|
| `docs/proposals/b5_automation_ai_intel_candidate_review.md` | 已被 B5a / B5b / B5c / D1 拆分覆盖。 | 2026-06-02 | 需要 |
| `docs/proposals/b5b_registry_candidate_alignment_review.md` | 已被 D1 candidate plugin registry/source review 和实际提交覆盖。 | 2026-06-02 | 需要 |

### 4.3 未来删除执行边界

未来如果你在 2026-06-02 之后批准删除，只允许删除上面精确列出的 18 个路径。

不允许混入：

- 已提交的 17 个 proposal 决策记录。
- `docs/thread_registry.md`。
- `projects/*`。
- `memory-cache/*`。
- `ai-intel/raw/*`。
- `docs/archive/*`。
- skill、harness、workflow、registry、pipeline 或 automation 文件。

## 5. 当前不应提交的 Proposal

本轮不建议再提交以下类型：

- 所有 `*_staging_list.md`。
- 所有仅描述某次 commit 的 `*_commit_review.md`。
- 已被后续更具体审查覆盖的宽泛旧审查。
- 已完成任务的 L2 approval package。
- 汇总 / 提交计划类临时材料。

原因：

- 17 个决策记录已经提交，长期判断不缺失。
- 继续提交临时材料会增加 proposal 区噪音。
- 清理应该先进入 30 天候选，不能马上删除。

## 6. 需要你后续拍板

| 拍板项 | 我的建议 | 不同选择的效果 |
|---|---|---|
| 是否把 16 个临时材料列入 30 天后删除候选 | 是 | 能逐步减少 proposal 噪音；不会马上删除。 |
| 两个已覆盖旧审查是否提炼中文总结 | 暂不提炼，除非后续需要 | 提炼会保留历史语义，但成本高；暂不提炼更轻。 |
| 是否创建删除清理脚本 | 不创建 | 当前用清单足够，新增脚本会增加维护成本。 |
| 是否把本处置表转 stable policy | 不转 | 它只是本轮 proposal 生命周期应用，不应变成永久规则。 |

## 7. 本轮不做

- 不删除任何 proposal 文件。
- 不移动 proposal 到 archive。
- 不提交项目产物。
- 不提交 `memory-cache/*`。
- 不提交 `ai-intel/raw/*`。
- 不提交 `docs/archive/*`。
- 不修改 skill、harness、workflow、registry、pipeline 或 automation。
- 不写长期记忆。
