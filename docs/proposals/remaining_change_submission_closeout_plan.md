# 剩余变更集中收口提交计划

- 日期：2026-05-04
- 状态：提交收口计划，不批准 staging、commit、push、PR、删除、归档、长期记忆写入、stable 转正或新增 skill / harness。
- 主线任务：把当前剩余未提交变更分成可提交、暂缓、项目内保留和删除候选，避免把治理修复、项目产物、raw 证据和临时材料混在一起。
- 当前暂存区：空。

## 1. 总体判断

当前确实有较多剩余变更，但不能一次性集中提交。最稳做法是：

```text
集中审查
-> 分批 staging
-> 分批 commit
-> 项目产物 / raw / archive / memory-cache 暂缓
```

原因：

- 架构修复和项目产物混提，会让后续回滚困难。
- `projects/*`、`memory-cache/*`、`ai-intel/raw/*` 数量大且含项目证据，不应污染稳定治理提交。
- 部分 proposal 是审计记录，有长期追溯价值；部分 proposal 是临时 staging / commit 材料，不应继续放大。
- 当前目标是长期稳定，不是快速清空工作区。

## 2. 推荐提交批次

### R1：开发文档轻量化与候选能力瘦身补丁

推荐动作：先提交。

建议 commit message：

```text
Constrain Codex development docs to lightweight default
```

文件范围：

```text
pm-prd-copilot/templates/codex_development_document_template.md
plugins/delivery-planning-suite/skills/capability-enablement-planner/SKILL.md
plugins/delivery-planning-suite/skills/capability-enablement-planner/references/output-contract.md
plugins/delivery-planning-suite/skills/codex-task-package-writer/SKILL.md
plugins/delivery-planning-suite/skills/codex-task-package-writer/references/output-contract.md
plugins/delivery-planning-suite/skills/development-governance-orchestrator/SKILL.md
plugins/delivery-planning-suite/skills/development-governance-orchestrator/references/output-contract.md
registry/skills.yaml
```

为什么能放一起：

- 都围绕同一条主线：普通 PRD / 普通开发文档默认轻量化。
- `memory-learning-extractor` 从 draft 收口为 candidate，和“候选能力不转 stable、不自动写长期记忆”一致。
- 没有新增 skill / harness。

不能混入：

```text
docs/proposals/*
docs/error_reports/*
projects/*
memory-cache/*
ai-intel/raw/*
docs/archive/*
```

预期效果：

- 普通 Codex 开发文档不会默认带完整 Skill/MCP/Harness、多管家、phase 1/2/3/final。
- full internal / agentic delivery 能力仍保留，但必须显式触发。
- 候选学习能力不会被误认为稳定长期记忆写入能力。

风险：

- 如果未来确实需要完整治理文档，必须明确触发 full internal 模式。
- 历史项目里的旧开发文档不会自动回扫。

回滚方式：

```bash
git revert <commit>
```

### R2：治理复核报告与线程台账

推荐动作：R1 后提交。

建议 commit message：

```text
Record lightweight development document review
```

文件范围：

```text
docs/proposals/candidate_capability_pruning_review.md
docs/proposals/codex_development_document_real_output_review.md
docs/proposals/archive_notes_lifecycle_disposition.md
docs/thread_registry.md
```

为什么能放一起：

- 都是本轮治理收口的中文审计和台账材料。
- 不改变运行逻辑。
- 给 R1 的补丁保留决策依据和后续追踪。

不能混入：

```text
临时 staging / commit review proposal
projects/*
memory-cache/*
ai-intel/raw/*
docs/error_reports/*
docs/archive/root-files/*
```

预期效果：

- 后续恢复上下文时能知道：为什么要让开发文档轻量化、哪些能力继续 candidate、哪些 archive notes 进入 30 天候选。
- 减少因为上下文稀释导致重复讨论和任务漂移。

风险：

- `docs/proposals/*` 容易继续膨胀，R2 只应收有长期追溯价值的报告，不收临时 staging 材料。

### R3：错误报告批次

推荐动作：R2 后单独处理。

建议 commit message：

```text
Record governance error reports
```

文件范围：

```text
docs/error_reports/bug_log.md
docs/error_reports/daily/2026-05-03.md
docs/error_reports/daily/2026-05-04.md
```

为什么单独提交：

- 错误报告是运行证据，不是架构规则。
- 单独提交便于后续日报、周报和错误复盘。

预期效果：

- 保留本轮修复中发现的问题和每日复盘证据。
- 后续定时汇报可以引用这些记录。

风险：

- 错误报告不能自动变成长期规则，仍需进入 architecture inbox 或 proposal 后再拍板。

### R4：临时 proposal 材料生命周期批次

推荐动作：暂缓，后续只提交“清单型处置记录”，不逐个提交临时材料。

当前未跟踪临时材料包括：

```text
docs/proposals/b2_proposal_audit_commit_review.md
docs/proposals/b3_teaching_steward_commit_review.md
docs/proposals/b3_teaching_steward_content_review_plan.md
docs/proposals/b3_teaching_steward_staging_list.md
docs/proposals/b4_error_reports_commit_review.md
docs/proposals/b4_error_reports_staging_list.md
docs/proposals/b5_automation_ai_intel_candidate_review.md
docs/proposals/b5a_github_workflows_commit_review.md
docs/proposals/b5a_github_workflows_staging_list.md
docs/proposals/b5b_candidate_marketplace_staging_list.md
docs/proposals/b5b_registry_candidate_alignment_review.md
docs/proposals/b5c_ai_intel_commit_review.md
docs/proposals/b5c_ai_intel_staging_list.md
docs/proposals/c11_golden_case_regression_l2_approval_package.md
docs/proposals/c12_c16_project_artifact_review_summary.md
docs/proposals/c3_demo_fixture_commit_review.md
docs/proposals/d1_candidate_plugin_commit_review.md
docs/proposals/proposal_decision_record_submission_plan.md
```

我的建议：

- 不逐个提交。
- 保留在工作区或后续列入 30 天删除候选。
- 只把“哪些已覆盖、哪些有价值、哪些 30 天后删除候选”的处置记录入库。

预期效果：

- 防止 `docs/proposals/` 继续变成临时过程材料堆积区。
- 保留必要审计轨迹，不保留每一个 staging / commit 过程文件。

### R5：项目产物批次

推荐动作：暂缓。

范围：

```text
projects/*
memory-cache/*
projects/_archives/*
projects/fitness-app-mvp/*
```

为什么暂缓：

- 项目产物数量多，且混合 PRD、原型、zip、closeout、run output、缓存。
- 它们应该按项目 closeout / active / archive candidate 分项目处理。
- 当前主线是治理收口，不是项目归档或项目提交。

预期效果：

- 避免把真实项目产物混进稳定架构提交。
- 保持后续项目线程可独立推进。

### R6：AI raw / archive notes / 删除候选

推荐动作：暂缓。

范围：

```text
ai-intel/raw/2026-04-30/*
docs/archive/notes/*
docs/archive/root-files/Remod开发.md
```

为什么暂缓：

- raw 只作为本地复核证据，不提交。
- `Remod开发.md` 已列为 2026-06-03 后删除候选，不应现在提交原文。
- `答辩.md` 应随 `graduation-defense-agent` 项目 closeout 处理。

预期效果：

- 遵守 30 天删除候选和二次审批规则。
- 不让历史原文重新污染仓库。

## 3. 推荐执行顺序

| 顺序 | 批次 | 动作 | 需要用户批准 |
|---|---|---|---|
| 1 | R1 开发文档轻量化与候选能力瘦身补丁 | 精确 staging，检查，通过后 commit | 是 |
| 2 | R2 治理复核报告与线程台账 | 精确 staging，检查，通过后 commit | 是 |
| 3 | R3 错误报告批次 | 精确 staging，检查，通过后 commit | 是 |
| 4 | R4 临时 proposal 生命周期 | 暂缓，只保留处置记录思路 | 后续是 |
| 5 | R5 项目产物 | 暂缓，分项目 closeout | 后续是 |
| 6 | R6 raw / archive / 删除候选 | 暂缓，等 30 天和二次审批 | 后续是 |

## 4. 现在需要你拍板的事项

| 决策 | 我的建议 | 不同选择的效果 |
|---|---|---|
| 是否先执行 R1 | 是 | 能先把真正影响功能输出的模板和 skill wording 稳住；不做则轻量开发文档修复继续停在未提交状态。 |
| R1 是否混入报告和项目产物 | 不混 | 混入会让补丁难回滚；不混最稳。 |
| 是否执行 R2 | R1 后执行 | 能保留审计依据；但应和 R1 分开，避免逻辑补丁和报告混在一起。 |
| 是否执行 R3 | R2 后执行 | 错误报告有价值，但不应混入架构补丁。 |
| 项目产物是否现在提交 | 不提交 | 暂缓能避免污染治理核心；现在提交会让工作区看起来干净，但长期风险更高。 |
| raw / archive 是否现在提交 | 不提交 | 符合 30 天候选和二次审批；现在提交会把本来不该入库的原始证据放回仓库。 |

## 5. R1 精确 staging 命令草案

如你批准 R1，只能使用：

```bash
git add pm-prd-copilot/templates/codex_development_document_template.md plugins/delivery-planning-suite/skills/capability-enablement-planner/SKILL.md plugins/delivery-planning-suite/skills/capability-enablement-planner/references/output-contract.md plugins/delivery-planning-suite/skills/codex-task-package-writer/SKILL.md plugins/delivery-planning-suite/skills/codex-task-package-writer/references/output-contract.md plugins/delivery-planning-suite/skills/development-governance-orchestrator/SKILL.md plugins/delivery-planning-suite/skills/development-governance-orchestrator/references/output-contract.md registry/skills.yaml
```

不得使用：

```bash
git add .
```

## 6. R1 检查命令

R1 staging 前后都应运行：

```bash
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
git diff --cached --name-only
git diff --cached --check
```

暂存区必须严格等于 R1 文件列表。

## 7. 本轮不执行

- 不 `git add .`。
- 不提交 `projects/*`。
- 不提交 `memory-cache/*`。
- 不提交 `ai-intel/raw/*`。
- 不提交 `docs/archive/notes/*` 或 `Remod开发.md` 原文。
- 不删除、恢复、移动、归档。
- 不 push / PR。
- 不新增 skill / harness。

