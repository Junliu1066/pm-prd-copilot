# B1 Core Governance Docs Staging List

- Date: 2026-04-29
- Status: final staging list only
- Scope: core governance documentation
- Rule: this file does not approve staging, commit, push, archive, cleanup, deletion, plugin promotion, skill promotion, harness promotion, or stable policy promotion.

## Conclusion

B1 is ready for user review before precise staging.

This staging list only covers core governance docs: repository entry rules, architecture map, operating model, lifecycle boundaries, prototype flow, self-check protocol, scheduled reporting description, cleanup inbox, contract responsibility layer, workspace audit map, governance repair report, and architecture inbox.

B1 does not include proposal audit records, teaching notes, steward protocols, error report evidence, automation, AI intel, candidate plugin metadata, archives, root deletion state, projects, plugins, or generated artifacts.

## Exact File List

| Path | Reason |
|---|---|
| `AGENTS.md` | Repository entry instruction; points agents to `agent.md` before planning or editing. |
| `README.md` | Repository entrypoint and safe navigation guide. |
| `agent.md` | Core work rules, approval points, minimal-governance rule, and two-round delivery self-check expectations. |
| `docs/architecture.md` | High-level architecture map and update policy. |
| `docs/operating_model.md` | Daily rhythm, error check rhythm, delivery self-check rhythm, and contract responsibility rhythm. |
| `docs/repository_map.md` | Canonical directory map and root file policy. |
| `docs/project_lifecycle.md` | Active, closeout, archive, and deletion lifecycle boundaries. |
| `docs/prototype_flow.md` | PRD to page flow, prototype, HTML, UI, and Codex development document handoff. |
| `docs/two_round_self_check.md` | Two-round self-check protocol for stability after changes and mid-work corrections. |
| `docs/version_model_update_review.md` | Version/model update pruning protocol to prevent skill/harness/plugin/rule accumulation. |
| `docs/scheduled_check_mechanisms.md` | Scheduled check and reporting design; does not execute automation. |
| `docs/daily_report_template.md` | Daily governance report format. |
| `docs/cleanup_inbox.md` | Supervised cleanup candidate inbox; does not approve cleanup. |
| `docs/contract_responsibility_layer.md` | Owner and evidence requirements for interface, harness, schema, workflow, registry, automation, and generator changes. |
| `docs/workspace_change_partition.md` | Workspace audit map and decision list; does not approve staging, cleanup, deletion, or archive. |
| `docs/governance_repair_closeout_report.md` | Governance repair closeout status and remaining approval points. |
| `docs/architecture-inbox/zero_to_one_prd_quality_feedback.md` | Architecture inbox candidate knowledge for 0-1 PRD quality; not a stable rule by itself. |

## Exact Staging Command

If the user approves B1 precise staging, use only this command:

```bash
git add AGENTS.md README.md agent.md docs/architecture.md docs/operating_model.md docs/repository_map.md docs/project_lifecycle.md docs/prototype_flow.md docs/two_round_self_check.md docs/version_model_update_review.md docs/scheduled_check_mechanisms.md docs/daily_report_template.md docs/cleanup_inbox.md docs/contract_responsibility_layer.md docs/workspace_change_partition.md docs/governance_repair_closeout_report.md docs/architecture-inbox/zero_to_one_prd_quality_feedback.md
```

Do not use:

```bash
git add .
git add docs/
git add docs/proposals/
git add teaching/
git add stewards/
git add projects/
git add plugins/
```

## Must Not Be Included In B1

| Excluded scope | Reason |
|---|---|
| `docs/proposals/*` | B2 audit/proposal records; proposals are not stable policy by default. |
| `teaching/*` | B3 teaching and preference records; long-term behavior requires content review. |
| `stewards/*` | B3 steward protocols; operational behavior must be reviewed separately. |
| `docs/error_reports/*` | B4 evidence records; useful history but not core governance docs. |
| `.github/*` | Automation behavior; requires separate automation review. |
| `.agents/*` | Candidate plugin visibility; belongs to D batch. |
| `ai-intel/*` | AI intelligence collection/reporting; needs separate write-boundary review. |
| `docs/archive/*` | Archive evidence; belongs to E batch and must not imply deletion approval. |
| `projects/*` | Project artifacts; belongs to C batch and project-by-project review. |
| `plugins/*` | Candidate capabilities; belongs to D batch. |
| Root deleted files | Cleanup/delete state; belongs to E batch and requires exact approval. |
| Generated zip, HTML, PNG, run outputs, closeout artifacts | Project or package outputs, not core governance docs. |

## Post-Staging Verification

If staging is later approved and executed, immediately run:

```bash
git diff --cached --name-only
git diff --cached --stat
```

The staged file list must exactly match the 17 B1 files above. If any extra path appears, stop and do not commit.

## Rollback Commands

If only the staged state needs to be reverted:

```bash
git restore --staged AGENTS.md README.md agent.md docs/architecture.md docs/operating_model.md docs/repository_map.md docs/project_lifecycle.md docs/prototype_flow.md docs/two_round_self_check.md docs/version_model_update_review.md docs/scheduled_check_mechanisms.md docs/daily_report_template.md docs/cleanup_inbox.md docs/contract_responsibility_layer.md docs/workspace_change_partition.md docs/governance_repair_closeout_report.md docs/architecture-inbox/zero_to_one_prd_quality_feedback.md
```

This rollback only unstages B1 files. It must not restore working-tree changes and must not touch unrelated user or project changes.

## Commit Intent For Later Review

If B1 staging is approved and later passes commit review, the suggested commit topic is:

```text
Document core governance operating model
```

Suggested commit body points:

- Add repository-level governance navigation and safe operating boundaries.
- Document lifecycle, prototype flow, cleanup, daily reporting, and two-round self-check expectations.
- Keep architecture inbox entries as candidate knowledge, not automatic stable rules.
- Keep proposals, teaching, steward protocols, automation, AI intel, project artifacts, archives, and candidate plugins out of this commit.

## Required Checks Before Any Future B1 Commit

```bash
git diff --cached --name-only
git diff --cached --check
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

Expected result:

- Staged paths exactly equal the 17 B1 files.
- No staged `docs/proposals/*`, `teaching/*`, `stewards/*`, `docs/error_reports/*`, `.github/*`, `.agents/*`, `ai-intel/*`, `docs/archive/*`, `projects/*`, or `plugins/*`.
- No commit, push, PR, archive, deletion, or cleanup happens unless separately approved.
