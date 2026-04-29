# B2 Proposal Audit Staging List

- Date: 2026-04-29
- Status: final staging list only
- Scope: proposal and audit records under `docs/proposals/`
- Rule: this file does not approve staging, commit, push, PR, archive, cleanup, deletion, plugin promotion, skill promotion, harness promotion, or stable policy promotion.

## Conclusion

B2 is ready for user review before precise staging.

This batch preserves the decision trail for A1-A4, B batch partitioning, stable core review, capability minimality review, governance lifecycle proposal, PRD structure changes, and PRD visual/page-flow mechanism discussions.

B2 proposal files are audit and planning records. They do not become stable policy by being staged or committed. Stable behavior remains controlled by the actual stable files, explicit user approvals, and later dedicated commits.

## Exact File List

| Path | Reason |
|---|---|
| `docs/proposals/a1_prd_core_staging_review.md` | A1 PRD core staging pre-review record. |
| `docs/proposals/a1_prd_core_staging_list.md` | A1 PRD core exact staging list. |
| `docs/proposals/a1_prd_core_commit_review.md` | A1 PRD core commit review record. |
| `docs/proposals/a2_governance_contract_staging_review.md` | A2 governance contract staging pre-review record. |
| `docs/proposals/a2_governance_contract_staging_list.md` | A2 governance contract exact staging list. |
| `docs/proposals/a2_governance_contract_commit_review.md` | A2 governance contract commit review record. |
| `docs/proposals/a3_essential_checks_staging_review.md` | A3 essential checks staging pre-review record. |
| `docs/proposals/a3_essential_checks_staging_list.md` | A3 essential checks exact staging list. |
| `docs/proposals/a3_essential_checks_commit_review.md` | A3 essential checks commit review record. |
| `docs/proposals/a4_delivery_closeout_real_output_review.md` | A4 delivery and closeout real-output review record. |
| `docs/proposals/a4_delivery_closeout_staging_list.md` | A4 delivery and closeout exact staging list. |
| `docs/proposals/a4_delivery_closeout_commit_review.md` | A4 delivery and closeout commit review record. |
| `docs/proposals/b_governance_docs_staging_review.md` | B batch split review and B1-B5 boundary record. |
| `docs/proposals/b1_core_governance_docs_staging_list.md` | B1 core governance docs exact staging list. |
| `docs/proposals/b1_core_governance_docs_commit_review.md` | B1 core governance docs commit review record. |
| `docs/proposals/b2_proposal_audit_staging_list.md` | This B2 exact staging list. |
| `docs/proposals/capability_minimality_review.md` | Capability minimality audit and candidate/stable recommendation record. |
| `docs/proposals/governance_lifecycle_policy.md` | Governance lifecycle proposal; remains proposal, not stable policy. |
| `docs/proposals/stable_core_submission_plan.md` | Stable core submission and batch review plan. |
| `docs/proposals/precise_submission_plan.md` | Precise submission partition plan. |
| `docs/proposals/stable_core_review_packet.md` | Stable core A1-A4 review packet. |
| `docs/proposals/prd_structure_change_impact_review.md` | PRD structure change impact record. |
| `docs/proposals/prd_visual_and_page_flow_mechanism.md` | PRD visual/page-flow mechanism proposal record. |

## Exact Staging Command

If the user approves B2 precise staging, use only this command:

```bash
git add docs/proposals/a1_prd_core_staging_review.md docs/proposals/a1_prd_core_staging_list.md docs/proposals/a1_prd_core_commit_review.md docs/proposals/a2_governance_contract_staging_review.md docs/proposals/a2_governance_contract_staging_list.md docs/proposals/a2_governance_contract_commit_review.md docs/proposals/a3_essential_checks_staging_review.md docs/proposals/a3_essential_checks_staging_list.md docs/proposals/a3_essential_checks_commit_review.md docs/proposals/a4_delivery_closeout_real_output_review.md docs/proposals/a4_delivery_closeout_staging_list.md docs/proposals/a4_delivery_closeout_commit_review.md docs/proposals/b_governance_docs_staging_review.md docs/proposals/b1_core_governance_docs_staging_list.md docs/proposals/b1_core_governance_docs_commit_review.md docs/proposals/b2_proposal_audit_staging_list.md docs/proposals/capability_minimality_review.md docs/proposals/governance_lifecycle_policy.md docs/proposals/stable_core_submission_plan.md docs/proposals/precise_submission_plan.md docs/proposals/stable_core_review_packet.md docs/proposals/prd_structure_change_impact_review.md docs/proposals/prd_visual_and_page_flow_mechanism.md
```

Do not use:

```bash
git add .
git add docs/
git add docs/proposals/
git add teaching/
git add stewards/
git add docs/error_reports/
git add projects/
git add plugins/
```

## Must Not Be Included In B2

| Excluded scope | Reason |
|---|---|
| Future `docs/proposals/*` files not listed above | Exact list only; no wildcard staging. |
| `teaching/*` | B3 teaching and preference records; needs content review. |
| `stewards/*` | B3 steward protocols; operational behavior must be reviewed separately. |
| `docs/error_reports/*` | B4 evidence records; useful history but not proposal/audit batch. |
| `.github/*` | Automation behavior; requires separate automation review. |
| `.agents/*` | Candidate plugin visibility; belongs to D batch. |
| `ai-intel/*` | AI intelligence collection/reporting; needs separate write-boundary review. |
| `docs/archive/*` | Archive evidence; belongs to E batch and must not imply deletion approval. |
| `projects/*` | Project artifacts; belongs to C batch and project-by-project review. |
| `plugins/*` | Candidate capabilities; belongs to D batch. |
| Root deleted files | Cleanup/delete state; belongs to E batch and requires exact approval. |

## Post-Staging Verification

If staging is later approved and executed, immediately run:

```bash
git diff --cached --name-only
git diff --cached --stat
```

The staged file list must exactly match the 23 B2 files above. If any extra path appears, stop and do not commit.

## Rollback Commands

If only the staged state needs to be reverted:

```bash
git restore --staged docs/proposals/a1_prd_core_staging_review.md docs/proposals/a1_prd_core_staging_list.md docs/proposals/a1_prd_core_commit_review.md docs/proposals/a2_governance_contract_staging_review.md docs/proposals/a2_governance_contract_staging_list.md docs/proposals/a2_governance_contract_commit_review.md docs/proposals/a3_essential_checks_staging_review.md docs/proposals/a3_essential_checks_staging_list.md docs/proposals/a3_essential_checks_commit_review.md docs/proposals/a4_delivery_closeout_real_output_review.md docs/proposals/a4_delivery_closeout_staging_list.md docs/proposals/a4_delivery_closeout_commit_review.md docs/proposals/b_governance_docs_staging_review.md docs/proposals/b1_core_governance_docs_staging_list.md docs/proposals/b1_core_governance_docs_commit_review.md docs/proposals/b2_proposal_audit_staging_list.md docs/proposals/capability_minimality_review.md docs/proposals/governance_lifecycle_policy.md docs/proposals/stable_core_submission_plan.md docs/proposals/precise_submission_plan.md docs/proposals/stable_core_review_packet.md docs/proposals/prd_structure_change_impact_review.md docs/proposals/prd_visual_and_page_flow_mechanism.md
```

This rollback only unstages B2 files. It must not restore working-tree changes and must not touch unrelated user or project changes.

## Commit Intent For Later Review

If B2 staging is approved and later passes commit review, the suggested commit topic is:

```text
Record governance repair proposal audit trail
```

Suggested commit body points:

- Preserve A1-A4 staging and commit review records.
- Preserve B batch partitioning and B1 commit review records.
- Preserve capability minimality, lifecycle, stable-core, and PRD structure proposal records.
- Keep proposal files as audit evidence, not stable policy.
- Keep teaching, steward protocols, error reports, automation, AI intel, project artifacts, archives, and candidate plugins out of this commit.

## Required Checks Before Any Future B2 Commit

```bash
git diff --cached --name-only
git diff --cached --check
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

Expected result:

- Staged paths exactly equal the 23 B2 files.
- No staged `teaching/*`, `stewards/*`, `docs/error_reports/*`, `.github/*`, `.agents/*`, `ai-intel/*`, `docs/archive/*`, `projects/*`, or `plugins/*`.
- No commit, push, PR, archive, deletion, or cleanup happens unless separately approved.
