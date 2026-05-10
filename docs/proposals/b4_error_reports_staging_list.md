# B4 Error Reports Staging List

- Date: 2026-04-30
- Status: final staging list only
- Scope: error report evidence under `docs/error_reports/`
- Rule: this file does not approve staging, commit, push, PR, archive, cleanup, deletion, stable policy changes, automation changes, or scheduled task changes.

## Conclusion

B4 is ready for user review before precise staging.

This batch preserves error-report structure and evidence records. It should be treated as evidence history, not as stable automation behavior. B4 must not include `.github`, `ai-intel`, project run outputs, harness code, proposal files, archives, plugins, or root deletion state.

## Exact File List

| Path | Reason |
|---|---|
| `docs/error_reports/README.md` | Defines the error report directory scope, handling rules, and forbidden content. |
| `docs/error_reports/bug_log.md` | Long-term bug index and status rules. |
| `docs/error_reports/daily/README.md` | Daily error report directory guide. |
| `docs/error_reports/daily/2026-04-28.md` | Daily report evidence for the initial governance repair period. |
| `docs/error_reports/daily/2026-04-29.md` | Daily report evidence after governed pipeline and harness check-only fixes. |
| `docs/error_reports/runs/README.md` | Manual run report directory guide. |
| `docs/error_reports/runs/2026-04-28-governance-system-test.md` | Governance system test evidence. |
| `docs/error_reports/runs/2026-04-28-initial-error-check-setup.md` | Initial error check setup evidence. |
| `docs/error_reports/runs/2026-04-28-scheduled-report-solution-update.md` | Scheduled report solution update evidence. |

## Exact Staging Command

If the user approves B4 precise staging, use only this command:

```bash
git add docs/error_reports/README.md docs/error_reports/bug_log.md docs/error_reports/daily/README.md docs/error_reports/daily/2026-04-28.md docs/error_reports/daily/2026-04-29.md docs/error_reports/runs/README.md docs/error_reports/runs/2026-04-28-governance-system-test.md docs/error_reports/runs/2026-04-28-initial-error-check-setup.md docs/error_reports/runs/2026-04-28-scheduled-report-solution-update.md
```

Do not use:

```bash
git add .
git add docs/
git add docs/error_reports/
git add .github/
git add ai-intel/
git add projects/
git add harness/
```

## Must Not Be Included In B4

| Excluded scope | Reason |
|---|---|
| `docs/proposals/*` | Proposal and audit records are separate from error evidence. |
| `.github/*` | Automation behavior belongs to B5 automation review. |
| `ai-intel/*` | AI intelligence collection/reporting belongs to B5 AI intel review. |
| `projects/*` | Project artifacts belong to C batch. |
| `harness/*` | Harness code changes belong to stable-core or capability review, not evidence batch. |
| `plugins/*` | Candidate capabilities belong to D batch. |
| `docs/archive/*` | Archive evidence belongs to E batch. |
| root deleted files | Cleanup/delete state belongs to E batch and requires exact approval. |

## Post-Staging Verification

If staging is later approved and executed, immediately run:

```bash
git diff --cached --name-only
git diff --cached --stat
```

The staged file list must exactly match the 9 B4 files above. If any extra path appears, stop and do not commit.

## Commit Intent For Later Review

If B4 staging is approved and later passes commit review, the suggested commit topic is:

```text
Record governance error report evidence
```

Suggested commit body points:

- Add error report directory structure and bug log.
- Preserve daily and manual-run evidence from the governance repair period.
- Keep evidence records separate from automation, AI intel, project artifacts, harness code, and cleanup/delete actions.

## Required Checks Before Any Future B4 Commit

```bash
git diff --cached --name-only
git diff --cached --check
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

Expected result:

- Staged paths exactly equal the 9 B4 files.
- No staged `.github/*`, `ai-intel/*`, `projects/*`, `harness/*`, `plugins/*`, `docs/archive/*`, or root deletion state.
- No commit, push, PR, archive, deletion, cleanup, automation change, or scheduled task change happens unless separately approved.
