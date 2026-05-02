# 剩余 Proposal 审计材料处置表

## 结论

本轮只做剩余 `docs/proposals/*` 过程材料的分区收口，不删除、不移动、不归档、不提交项目产物、不提交 root 删除状态。

当前建议：

- 本轮提交 2 个中文审计文件：
  - `docs/proposals/remaining_proposal_audit_materials_disposition.md`
  - `docs/proposals/e_root_archive_cleanup_review.md`
- 其余未跟踪 proposal 暂不提交，原因是它们主要是历史 staging / commit 临时材料，或者已被后续正式审查和提交覆盖。
- 后续如果要清理这些临时材料，必须单独经过你批准；本轮不删除。

## 分类原则

- 能说明长期治理决策、仍有待拍板事项的，保留为审计记录。
- 只描述某次暂存区、某次 commit 命令、某次临时 staging 范围的，不进入长期审计提交。
- 已被后续正式报告、代码提交或中文审查覆盖的，暂缓提交。
- 英文旧过程材料不直接入库；如果仍有价值，后续提炼成中文总结再处理。

## 本轮提交范围

| 文件 | 处置 | 原因 |
|---|---|---|
| `docs/proposals/remaining_proposal_audit_materials_disposition.md` | 提交 | 记录剩余 proposal 材料的统一处置口径，防止后续误提交临时材料。 |
| `docs/proposals/e_root_archive_cleanup_review.md` | 提交 | 这是当前仍未解决的 root/archive 决策表，需要长期追溯，但不批准删除或归档。 |

## 暂不提交的材料

### B2 / B3 / B4 临时提交材料

| 文件 | 处置 | 原因 |
|---|---|---|
| `docs/proposals/b2_proposal_audit_commit_review.md` | 暂不提交 | B2 已完成正式提交；该文件只是当时的 commit review。 |
| `docs/proposals/b3_teaching_steward_commit_review.md` | 暂不提交 | B3 已完成正式提交；该文件只是当时的 commit review。 |
| `docs/proposals/b3_teaching_steward_content_review_plan.md` | 暂不提交 | 已被 `b3_teaching_steward_content_review.md` 和后续修复覆盖。 |
| `docs/proposals/b3_teaching_steward_staging_list.md` | 暂不提交 | 只描述当时 staging 范围，已过期。 |
| `docs/proposals/b4_error_reports_commit_review.md` | 暂不提交 | B4 已完成错误报告证据提交；该文件只是当时的 commit review。 |
| `docs/proposals/b4_error_reports_staging_list.md` | 暂不提交 | 只描述当时 staging 范围，已过期。 |

### B5 自动化 / AI 情报 / Candidate 插件临时材料

| 文件 | 处置 | 原因 |
|---|---|---|
| `docs/proposals/b5_automation_ai_intel_candidate_review.md` | 暂不提交 | 内容有价值，但已被后续 B5a/B5b/B5c/D1 分拆审查覆盖；如需保留，应提炼成中文总结。 |
| `docs/proposals/b5a_github_workflows_commit_review.md` | 暂不提交 | 只描述当时 GitHub workflow commit 前状态，已过期。 |
| `docs/proposals/b5a_github_workflows_staging_list.md` | 暂不提交 | 只描述当时 staging 范围，已过期。 |
| `docs/proposals/b5b_candidate_marketplace_staging_list.md` | 暂不提交 | 已被 D1 coordinated candidate plugin 提交取代。 |
| `docs/proposals/b5b_registry_candidate_alignment_review.md` | 暂不提交 | 决策已被 D1 candidate plugin registry/source review 和实际提交覆盖；如需保留，后续提炼中文总结。 |
| `docs/proposals/b5c_ai_intel_commit_review.md` | 暂不提交 | B5c 已有写入边界审查和 AI intel 提交记录；该文件只是 commit review。 |
| `docs/proposals/b5c_ai_intel_staging_list.md` | 暂不提交 | 只描述当时 staging 范围，已过期。 |

### C / D 临时提交材料

| 文件 | 处置 | 原因 |
|---|---|---|
| `docs/proposals/c3_demo_fixture_commit_review.md` | 暂不提交 | demo fixture 已完成提交；该文件只是 commit review。 |
| `docs/proposals/d1_candidate_plugin_commit_review.md` | 暂不提交 | D1 candidate plugin 已完成提交；该文件只是 commit review。 |

## 仍需你后续拍板的功能 / 架构事项

| 事项 | 选项 | 我的建议 | 不同选择的效果 |
|---|---|---|---|
| 是否清理这些临时 proposal 文件 | 保留 / 归档 / 30 天后删除候选 | 先保留，等 root/archive 策略确认后再处理 | 立即清理能让工作区更干净，但会增加误删过程证据的风险。 |
| 是否正式接受 4 个 root 删除状态 | 接受 / 暂缓 / 恢复 | 暂缓到逐条确认；后续大概率接受两个已有 canonical 的 root 删除 | 接受能清理 root；暂缓更稳；恢复会让 root 重新散落历史文件。 |
| 是否提交 `docs/archive/` | 提交 / 暂缓 | 暂缓 | 现在提交会固化 archive 策略，但 archive 里还有本轮外历史材料。 |
| 是否把旧英文过程材料转中文总结 | 转 / 不转 | 只转仍有长期决策价值的材料 | 全转成本高且噪音大；不转则部分历史上下文只留在未跟踪文件里。 |

## 本轮明确不做

- 不删除任何 proposal 文件。
- 不移动到 archive。
- 不提交 root 删除状态。
- 不提交 `docs/archive/`。
- 不提交 `projects/*`。
- 不提交 `memory-cache/`。
- 不改 skill、harness、workflow、registry。
- 不 push / PR。
