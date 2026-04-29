# B Batch Governance Docs Staging Review

Status: review only
Date: 2026-04-29
Owner: Codex governance repair thread
Scope: B batch governance documentation, supervision records, teaching notes, steward protocols, and related audit docs

## Conclusion

B batch should not be staged as one large commit.

Recommended path:

1. Create a B1 final staging list for core governance docs only.
2. Keep proposal and audit records as B2, separate from durable operating rules.
3. Keep teaching notes and steward protocols as B3, with user review before staging because they affect long-lived behavior.
4. Keep error reports as B4 evidence records.
5. Defer automation, AI intel, plugin marketplace, and archive/delete records to separate reviews.

This keeps long-term governance stable and avoids mixing operating rules, temporary audit evidence, automation behavior, and candidate capabilities in one commit.

## Current Workspace Evidence

Observed changed or untracked governance-adjacent areas:

- Modified tracked files:
  - `.agents/plugins/marketplace.json`
  - `.github/workflows/regression.yml`
  - `.github/workflows/skill-upgrade-review.yml`
  - `README.md`
  - `agent.md`
  - `ai-intel/scripts/summarize_daily.py`
  - `ai-intel/scripts/update_decision_matrix.py`
  - `docs/architecture.md`
  - `docs/operating_model.md`
  - `teaching/accepted_lessons.md`
  - `teaching/open_lessons.md`
  - `teaching/teaching_log.md`
  - `teaching/user_preferences.md`
- Untracked governance docs and evidence:
  - `AGENTS.md`
  - `docs/architecture-inbox/`
  - `docs/cleanup_inbox.md`
  - `docs/contract_responsibility_layer.md`
  - `docs/daily_report_template.md`
  - `docs/error_reports/`
  - `docs/governance_repair_closeout_report.md`
  - `docs/project_lifecycle.md`
  - `docs/proposals/`
  - `docs/prototype_flow.md`
  - `docs/repository_map.md`
  - `docs/scheduled_check_mechanisms.md`
  - `docs/two_round_self_check.md`
  - `docs/version_model_update_review.md`
  - `docs/workspace_change_partition.md`
  - `stewards/*.md` new operating protocols
- Adjacent but not B batch:
  - `.github/` automation changes
  - `.agents/` candidate plugin visibility changes
  - `ai-intel/` scripts and generated intelligence folders
  - `docs/archive/` archive evidence

## Proposed Split

### B1 Core Governance Docs

Recommended status: `ready_for_final_staging_list`

Purpose: stable documentation that explains how the repository is governed and how the work should be reviewed. These files do not directly change runtime behavior.

Candidate files:

| Path | Role | Notes |
|---|---|---|
| `AGENTS.md` | Repo entry instruction | Tells agents to read `agent.md` before planning or editing. |
| `README.md` | Repository entrypoint | Should describe the repo and how to run safe checks. |
| `agent.md` | Core work rules | Long-lived behavior; already aligned with supervised stable-change approval. |
| `docs/architecture.md` | Architecture overview | Stable explanatory doc. |
| `docs/operating_model.md` | Operating model | Stable explanatory doc. |
| `docs/repository_map.md` | Repository map | Helps prevent misplaced files and wrong ownership. |
| `docs/project_lifecycle.md` | Project lifecycle | Supports closeout-before-archive governance. |
| `docs/prototype_flow.md` | Prototype flow | Records PRD -> page flow -> prototype/UI handoff boundary. |
| `docs/two_round_self_check.md` | Two-round self-check | Matches the user-approved stability requirement. |
| `docs/scheduled_check_mechanisms.md` | Scheduled check design | Governance reporting design, not automation execution. |
| `docs/version_model_update_review.md` | Version/model update pruning | Supports "长期稳定可靠优先". |
| `docs/daily_report_template.md` | Report template | Reporting format only. |
| `docs/cleanup_inbox.md` | Cleanup inbox | Review queue, not deletion approval. |
| `docs/contract_responsibility_layer.md` | Contract responsibility layer | Explains ownership boundaries. |
| `docs/workspace_change_partition.md` | Workspace partition map | Audit map; not cleanup approval. |
| `docs/governance_repair_closeout_report.md` | Governance repair report | Summarizes repair state and remaining risks. |
| `docs/architecture-inbox/zero_to_one_prd_quality_feedback.md` | Architecture inbox | Candidate knowledge only, not stable rule. |

Why B1 can be separate:

- It documents stable operating boundaries.
- It does not stage code, generated project artifacts, candidate plugins, or root deletion state.
- It gives future agents a safer map before any project or archive action.

Main risk:

- `agent.md` and lifecycle docs are long-lived behavior. Their final staging should be reviewed as governance policy, not casual documentation.

Recommended next action:

- Generate `docs/proposals/b1_core_governance_docs_staging_list.md`.

### B2 Proposal And Audit Records

Recommended status: `keep_separate_audit_batch`

Purpose: preserve the decision trail for A1-A4 and governance proposals without turning every proposal into stable policy.

Candidate files:

| Path / scope | Role | Notes |
|---|---|---|
| `docs/proposals/a1_prd_core_staging_review.md` | A1 audit trail | Evidence for A1 review. |
| `docs/proposals/a1_prd_core_staging_list.md` | A1 audit trail | Evidence for A1 staging scope. |
| `docs/proposals/a1_prd_core_commit_review.md` | A1 audit trail | Evidence for A1 commit review. |
| `docs/proposals/a2_governance_contract_staging_review.md` | A2 audit trail | Evidence for A2 review. |
| `docs/proposals/a2_governance_contract_staging_list.md` | A2 audit trail | Evidence for A2 staging scope. |
| `docs/proposals/a2_governance_contract_commit_review.md` | A2 audit trail | Evidence for A2 commit review. |
| `docs/proposals/a3_essential_checks_staging_review.md` | A3 audit trail | Evidence for A3 review. |
| `docs/proposals/a3_essential_checks_staging_list.md` | A3 audit trail | Evidence for A3 staging scope. |
| `docs/proposals/a3_essential_checks_commit_review.md` | A3 audit trail | Evidence for A3 commit review. |
| `docs/proposals/a4_delivery_closeout_real_output_review.md` | A4 audit trail | Evidence for A4 real-output review. |
| `docs/proposals/a4_delivery_closeout_staging_list.md` | A4 audit trail | Evidence for A4 staging scope. |
| `docs/proposals/a4_delivery_closeout_commit_review.md` | A4 audit trail | Evidence for A4 commit review. |
| `docs/proposals/capability_minimality_review.md` | Capability minimality audit | Keeps "如无必要，不增 skill / harness" visible. |
| `docs/proposals/governance_lifecycle_policy.md` | Lifecycle proposal | Proposal only; not stable policy yet. |
| `docs/proposals/stable_core_submission_plan.md` | Stable core submission plan | Proposal record. |
| `docs/proposals/precise_submission_plan.md` | Precise submission plan | Proposal record. |
| `docs/proposals/stable_core_review_packet.md` | Stable core review packet | Proposal record. |
| `docs/proposals/prd_structure_change_impact_review.md` | PRD structure impact review | Proposal record. |
| `docs/proposals/prd_visual_and_page_flow_mechanism.md` | PRD visual/page-flow mechanism | Proposal record. |
| `docs/proposals/b_governance_docs_staging_review.md` | This review | B batch audit record. |

Why separate:

- Proposal docs explain decisions and alternatives.
- They should not be confused with stable operating rules.
- Keeping them separate makes rollback and later pruning easier.

Recommended next action:

- After B1 is handled, decide whether B2 should be committed as audit history or kept uncommitted until the broader governance repair is closed.

### B3 Teaching And Steward Protocols

Recommended status: `needs_user_content_review_before_staging`

Purpose: preserve accepted lessons, open lessons, user preferences, and steward operating protocols.

Candidate files:

| Path / scope | Role | Notes |
|---|---|---|
| `teaching/accepted_lessons.md` | Accepted lessons | Long-lived learning record. |
| `teaching/open_lessons.md` | Open lessons | Must stay non-binding until approved. |
| `teaching/teaching_log.md` | Teaching history | Evidence, not automatic stable rule. |
| `teaching/user_preferences.md` | User preferences | Sensitive long-term behavior surface. |
| `stewards/ai_architecture_steward.md` | Steward protocol | New operating protocol. |
| `stewards/ai_coaching_steward.md` | Steward protocol | New operating protocol. |
| `stewards/capability_enablement_steward.md` | Steward protocol | New operating protocol. |
| `stewards/delivery_planning_steward.md` | Steward protocol | New operating protocol. |
| `stewards/development_governance_steward.md` | Steward protocol | New operating protocol. |
| `stewards/learning_steward.md` | Steward protocol | New operating protocol. |
| `stewards/prototype_design_steward.md` | Steward protocol | New operating protocol. |

Why not mix with B1:

- These files affect future behavior and interpretation.
- They may contain user-specific teaching and long-term preferences.
- The user has required supervision before long-term memory or stable behavior changes.

Recommended next action:

- Stage only after a content review confirms no unapproved long-term rules were added.

### B4 Error Report Evidence

Recommended status: `separate_evidence_batch`

Purpose: keep bug reports and run reports as evidence for repair and future scheduled reporting.

Candidate files:

| Path / scope | Role | Notes |
|---|---|---|
| `docs/error_reports/README.md` | Error report guide | Directory-level explanation. |
| `docs/error_reports/bug_log.md` | Bug log | Evidence record. |
| `docs/error_reports/daily/README.md` | Daily report guide | Directory-level explanation. |
| `docs/error_reports/daily/2026-04-28.md` | Daily error report | Evidence record. |
| `docs/error_reports/daily/2026-04-29.md` | Daily error report | Evidence record. |
| `docs/error_reports/runs/README.md` | Run report guide | Directory-level explanation. |
| `docs/error_reports/runs/2026-04-28-governance-system-test.md` | Run evidence | Evidence record. |
| `docs/error_reports/runs/2026-04-28-initial-error-check-setup.md` | Run evidence | Evidence record. |
| `docs/error_reports/runs/2026-04-28-scheduled-report-solution-update.md` | Run evidence | Evidence record. |

Why separate:

- These are evidence records, not stable governance rules.
- They may grow frequently and should not be mixed with stable documentation commits.

Recommended next action:

- Commit only if the user wants error-report history preserved in the repository now.

### B5 Defer From B Batch

Recommended status: `defer_to_separate_review`

These paths should not be staged in B governance docs:

| Path / scope | Reason |
|---|---|
| `.agents/plugins/marketplace.json` | Candidate plugin visibility belongs to D batch. |
| `.github/workflows/regression.yml` | Automation behavior belongs to automation review. |
| `.github/workflows/skill-upgrade-review.yml` | Automation behavior belongs to automation review. |
| `ai-intel/` | AI intelligence collection/reporting needs its own safety and write-boundary review. |
| `docs/archive/` | Archive evidence belongs to E batch. |
| `projects/*` | Project artifacts belong to C batch. |
| `plugins/*` | Candidate capability source belongs to D batch. |
| root deletion state | Cleanup/delete approval belongs to E batch. |

## Forbidden In Any B Staging Command

- No `git add .`.
- No `projects/*`.
- No `plugins/*`.
- No `.agents/*` unless explicitly doing D batch.
- No `.github/*` unless explicitly doing automation review.
- No `ai-intel/*` unless explicitly doing AI intelligence review.
- No `docs/archive/*`.
- No root deleted files.
- No A1-A4 code files already committed in stable core commits.
- No generated zips, HTML, PNGs, run outputs, or closeout project artifacts.

## User Decisions Needed

| Decision | Options | Impact | Recommendation |
|---|---|---|---|
| B1 core governance docs | Stage next / defer | Stage next freezes the readable governance map; defer keeps worktree noisy. | Stage next after final list. |
| B2 proposals | Commit as audit trail / keep uncommitted | Committing preserves decision history; keeping uncommitted reduces repo noise. | Commit separately after B1. |
| B3 teaching and stewards | Stage now / content-review first / defer | Stage now is fast but risks unapproved long-term behavior; review first is safer. | Content-review first. |
| B4 error reports | Commit evidence / defer | Commit preserves bug history; defer avoids report churn. | Defer until scheduled reporting is stable, unless evidence preservation is urgent. |
| B5 automation and AI intel | Include in B / separate review | Including in B mixes behavior and docs; separate review protects stability. | Separate review. |

## Recommended Next Step

Generate a B1 final staging list:

`docs/proposals/b1_core_governance_docs_staging_list.md`

That list should contain only core governance docs and should include an exact `git add` command. It should not stage proposal docs, teaching files, steward protocols, error reports, automation, AI intel, archives, candidate plugins, or project artifacts.

## Validation Plan

After this review file is created:

```bash
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
git diff --cached --name-only
```

Expected result:

- No staging.
- No commit.
- No project files written.
- No new skill, harness, workflow stage, plugin, or automation.
- Only this proposal file is added by this step.
