# B2 Proposal Audit Commit Review

- Date: 2026-04-29
- Status: commit review only
- Current staged scope: B2 23 proposal and audit files
- Rule: this file does not approve commit, push, PR, archive, cleanup, deletion, plugin promotion, skill promotion, harness promotion, or stable policy promotion.

## 1. Current Staged Scope

The current staged area must remain exactly these 23 files:

```text
docs/proposals/a1_prd_core_commit_review.md
docs/proposals/a1_prd_core_staging_list.md
docs/proposals/a1_prd_core_staging_review.md
docs/proposals/a2_governance_contract_commit_review.md
docs/proposals/a2_governance_contract_staging_list.md
docs/proposals/a2_governance_contract_staging_review.md
docs/proposals/a3_essential_checks_commit_review.md
docs/proposals/a3_essential_checks_staging_list.md
docs/proposals/a3_essential_checks_staging_review.md
docs/proposals/a4_delivery_closeout_commit_review.md
docs/proposals/a4_delivery_closeout_real_output_review.md
docs/proposals/a4_delivery_closeout_staging_list.md
docs/proposals/b1_core_governance_docs_commit_review.md
docs/proposals/b1_core_governance_docs_staging_list.md
docs/proposals/b2_proposal_audit_staging_list.md
docs/proposals/b_governance_docs_staging_review.md
docs/proposals/capability_minimality_review.md
docs/proposals/governance_lifecycle_policy.md
docs/proposals/prd_structure_change_impact_review.md
docs/proposals/prd_visual_and_page_flow_mechanism.md
docs/proposals/precise_submission_plan.md
docs/proposals/stable_core_review_packet.md
docs/proposals/stable_core_submission_plan.md
```

Current staged stat:

```text
23 files changed, 4389 insertions(+)
```

The staged scope does not include:

- this commit review file
- `teaching/*`
- `stewards/*`
- `docs/error_reports/*`
- `.github/*`
- `.agents/*`
- `ai-intel/*`
- `docs/archive/*`
- `projects/*`
- `plugins/*`
- root deleted files
- generated zip, HTML, PNG, run outputs, or project closeout artifacts

## 2. Recommended Commit Message

```text
Record governance repair proposal audit trail
```

Recommended commit body:

```text
- Preserve A1-A4 staging and commit review records.
- Preserve B batch partitioning and B1 governance-doc review records.
- Preserve capability minimality, lifecycle, stable-core, and PRD structure proposal records.
- Keep proposal files as audit evidence, not stable policy.
- Keep teaching, steward protocols, error reports, automation, AI intel, project artifacts, archives, and candidate plugins out of this commit.
```

## 3. Required Pre-Commit Checks

Before any B2 commit, run:

```bash
git diff --cached --name-only
git diff --cached --check
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

Acceptance criteria:

- `git diff --cached --name-only` exactly equals the 23 files in Section 1.
- `git diff --cached --check` passes.
- `git diff --check` passes.
- Regression passes.
- Harness passes in `check-only` mode.
- Harness reports no project files written.

If any check fails:

- Do not commit.
- Keep staged state intact unless the user asks to unstage.
- Report the failure and the exact file or command involved.

## 4. Exact Commit Command For Later Approval

If the user explicitly approves the B2 commit after this review:

```bash
git commit -m "Record governance repair proposal audit trail"
```

Do not use this command until approval is explicit.

## 5. Post-Commit Verification

After a future approved commit, run:

```bash
git show --stat --oneline --name-only HEAD
git status --short
```

Expected result:

- Latest commit contains only the 23 B2 files from Section 1.
- This commit review file is not included unless separately staged in a later audit batch.
- No teaching, steward, error report, project, plugin, archive, automation, AI intel, or root deletion path is included.
- Remaining uncommitted work stays in the worktree for later B3/B4/B5/C/D/E review.

## 6. Rollback Strategy

If commit is not yet created and staged state must be reverted:

```bash
git restore --staged docs/proposals/a1_prd_core_commit_review.md docs/proposals/a1_prd_core_staging_list.md docs/proposals/a1_prd_core_staging_review.md docs/proposals/a2_governance_contract_commit_review.md docs/proposals/a2_governance_contract_staging_list.md docs/proposals/a2_governance_contract_staging_review.md docs/proposals/a3_essential_checks_commit_review.md docs/proposals/a3_essential_checks_staging_list.md docs/proposals/a3_essential_checks_staging_review.md docs/proposals/a4_delivery_closeout_commit_review.md docs/proposals/a4_delivery_closeout_real_output_review.md docs/proposals/a4_delivery_closeout_staging_list.md docs/proposals/b1_core_governance_docs_commit_review.md docs/proposals/b1_core_governance_docs_staging_list.md docs/proposals/b2_proposal_audit_staging_list.md docs/proposals/b_governance_docs_staging_review.md docs/proposals/capability_minimality_review.md docs/proposals/governance_lifecycle_policy.md docs/proposals/prd_structure_change_impact_review.md docs/proposals/prd_visual_and_page_flow_mechanism.md docs/proposals/precise_submission_plan.md docs/proposals/stable_core_review_packet.md docs/proposals/stable_core_submission_plan.md
```

This only unstages B2 files. It must not restore working-tree changes.

If a future commit is created and later needs to be undone:

```bash
git revert <commit>
```

Do not use `git reset --hard`. Do not revert or overwrite unrelated user or project changes.

## 7. Explicitly Not Approved By This Review

This review does not approve:

- commit
- push or PR
- staging this review file
- staging future proposal files not listed in Section 1
- staging `teaching/*`
- staging `stewards/*`
- staging `docs/error_reports/*`
- staging `.github/*`, `.agents/*`, or `ai-intel/*`
- staging `projects/*`, `plugins/*`, `docs/archive/*`, or root deletion state
- archive, deletion, cleanup, or hard delete
- turning proposals into stable policy
- turning architecture inbox entries into stable policy

## 8. Next Step

If the user approves, execute the B2 commit only after rerunning the pre-commit checks in Section 3.
