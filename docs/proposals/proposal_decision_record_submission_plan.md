# Proposal 决策记录候选提交计划

- 日期：2026-05-03
- 状态：L2 提交前审核材料，不是 stable policy。
- 主线任务：把 17 个有长期追溯价值的 proposal 决策记录候选整理成一个可审核、可回滚、不会污染稳定核心的未来提交批次。
- 边界：本文件不执行 staging、commit、push、PR、删除、归档、项目产物提交或 stable 转正。

## 1. 结论

建议后续单独提交 17 个 proposal 决策记录候选。

提交含义：

- 记录本轮治理修复的关键判断。
- 记录项目产物边界和生命周期判断。
- 不提交任何 `projects/*`。
- 不把 proposal 变成 stable policy。
- 不批准删除、归档、长期记忆或 candidate 转 stable。

建议 commit message：

```text
Record governance lifecycle decision proposals
```

## 2. 推荐提交范围

未来如果你批准 staging，只允许包含以下 17 个文件：

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

## 3. 精确 staging 命令

如果你后续批准 staging，只能使用精确命令，不允许 `git add .`：

```bash
git add docs/proposals/ai_intel_raw_lifecycle_disposition.md docs/proposals/governance_lifecycle_embedding_plan.md docs/proposals/architecture_self_management_system.md docs/proposals/archive_notes_lifecycle_disposition.md docs/proposals/thread_lifecycle_supervision_plan.md docs/proposals/projects_lifecycle_inventory_review.md docs/proposals/c6_demo_prototype_artifact_review.md docs/proposals/c7_fitness_memory_cache_artifact_review.md docs/proposals/c8_project_artifact_final_disposition_checklist.md docs/proposals/c9_graduation_defense_closeout_review.md docs/proposals/c10_jiaxiaoqian_high_value_closeout_review.md docs/proposals/c11_taxi_hailing_golden_sample_deidentification_plan.md docs/proposals/c12_ai_collaboration_closeout_refresh_review.md docs/proposals/c13_prompt_optimization_workbench_low_evidence_review.md docs/proposals/c14_santoip_brand_video_low_evidence_review.md docs/proposals/c15_temp_generated_project_disposition_review.md docs/proposals/c16_project_package_zip_lifecycle_review.md
```

## 4. 明确排除范围

本批次不包含：

| 排除项 | 原因 |
|---|---|
| `docs/proposals/*_staging_list.md` | 临时 staging 材料，后续可进 30 天删除候选。 |
| `docs/proposals/*_commit_review.md` | 临时 commit 审查材料，不适合作长期记录。 |
| `docs/proposals/c11_golden_case_regression_l2_approval_package.md` | C11 已提交完成，该文件只是 L2 审批过程材料。 |
| `docs/proposals/c12_c16_project_artifact_review_summary.md` | 本轮新生成的 L2 汇总材料，不纳入 17 个决策记录，避免自我引用。 |
| `docs/proposals/proposal_decision_record_submission_plan.md` | 本文件是提交计划，不应提交到自己计划的批次。 |
| `docs/thread_registry.md` | 台账仍是试运行材料，不在本批 proposal 提交范围。 |
| `projects/*` | 项目产物不进治理 proposal 提交。 |
| `memory-cache/*` | 项目偏好缓存不跨项目、不自动长期化。 |
| `ai-intel/raw/*` | raw HTML 不提交。 |
| `docs/archive/*` | archive 材料单独审查。 |
| root 删除项 | E 批已单独处理；剩余 root / archive 不混入。 |

## 5. 为什么这 17 个可以放一起

它们共同服务一个目标：记录本轮治理修复中的“判断依据”，而不是提交运行代码或项目产物。

| 分类 | 文件 | 价值 |
|---|---|---|
| 上位治理机制 | lifecycle embedding、architecture self-management、thread supervision | 记录治理从人工逐步走向可监督自运行的机制。 |
| 证据边界 | AI raw、archive notes、projects lifecycle | 记录 raw、archive、项目目录不能混入 stable 的边界。 |
| 项目产物边界 | C6-C8 | 记录 demo / fitness / memory-cache 的项目内保留规则。 |
| 高价值项目 closeout | C9-C12 | 记录 graduation、Jiaxiaoqian、taxi、AI collaboration 的价值和限制。 |
| 低证据 / 临时项目 | C13-C16 | 记录 HTML 原型、临时项目和 zip/package 生命周期边界。 |

## 6. 风险与控制

| 风险 | 控制方式 |
|---|---|
| proposal 被误读为 stable policy | 每个文件都标明 proposal / candidate，不批准 stable。 |
| 提交过多过程材料 | 本批只含决策记录候选，不含 staging / commit 临时材料。 |
| 项目产物被误提交 | 精确 `git add`，并核对暂存区只含 17 个 docs/proposals 文件。 |
| 后续清理缺依据 | 提交后可以用这些记录支撑 30 天删除候选和归档候选。 |

## 7. 提交前检查

如果后续进入 staging / commit，执行前必须跑：

```bash
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

staging 后必须核对：

```bash
git diff --cached --name-only
git diff --cached --check
```

暂存区必须严格等于 17 个推荐提交文件。

## 8. 需要你拍板

| 拍板项 | 我的建议 | 不同选择的效果 |
|---|---|---|
| 是否批准 17 个 proposal 决策记录进入 staging | 建议批准，但等你看完本计划后再执行 | 批准后可以把治理判断从未跟踪区收口；不批准则继续留在工作区。 |
| 是否把本提交拆成两批 | 不拆 | 这 17 个都是 proposal 决策记录，拆太细会增加管理成本。 |
| 是否把 C12-C16 汇总也纳入提交 | 暂不纳入 | 汇总是审核材料，详细记录已经在 17 个文件里；不纳入可减少噪音。 |
| 是否把临时 staging / commit 材料一并提交 | 不提交 | 它们只服务一次性流程，提交会长期污染 proposal 区。 |

## 9. 本轮不做

- 不执行 `git add`。
- 不 commit。
- 不 push / PR。
- 不删除 proposal。
- 不移动到 archive。
- 不提交项目产物、raw、memory-cache、zip 或 root 删除项。
