# B5a GitHub Workflows Staging List

- Date: 2026-04-30
- Status: final staging list only
- Scope: GitHub workflow check-only safety
- Rule: this file does not approve staging, commit, push, PR, archive, cleanup, deletion, or broader automation changes.

## Conclusion

B5a is ready for user review before precise staging.

This batch only covers the two GitHub workflows that currently ran governance checks. The change removes demo pipeline output refresh from CI and makes the governance harness run in `--check-only` mode.

## Exact File List

| Path | Reason |
|---|---|
| `.github/workflows/regression.yml` | Prevents regression CI from refreshing demo pipeline outputs and makes harness read-only with `--check-only`. |
| `.github/workflows/skill-upgrade-review.yml` | Prevents weekly skill review from refreshing demo pipeline outputs and makes harness read-only with `--check-only`. |

## Exact Staging Command

If the user approves B5a precise staging, use only this command:

```bash
git add .github/workflows/regression.yml .github/workflows/skill-upgrade-review.yml
```

Do not use:

```bash
git add .
git add .github/
git add docs/
git add ai-intel/
git add projects/
```

## Must Not Be Included In B5a

| Excluded scope | Reason |
|---|---|
| `.agents/*` | Candidate plugin visibility belongs to B5b. |
| `ai-intel/*` | AI intel data area belongs to B5c. |
| `docs/proposals/*` | Review docs are audit records and not part of the workflow change. |
| `projects/*` | Project artifacts must not be written or staged by CI safety changes. |
| `harness/*` | Harness code is already handled by stable-core or capability batches. |
| `plugins/*` | Candidate capabilities belong to D batch. |
| `docs/archive/*` and root deleted files | Cleanup/archive belongs to E batch. |

## Post-Staging Verification

If staging is later approved and executed, immediately run:

```bash
git diff --cached --name-only
git diff --cached --stat
```

The staged file list must exactly match the 2 B5a files above.

## Commit Intent For Later Review

If B5a staging is approved and later passes commit review, the suggested commit topic is:

```text
Make governance workflows check-only
```

Suggested commit body points:

- Remove CI steps that refreshed demo pipeline outputs.
- Run governance harness with `--check-only` in regression and skill-upgrade review workflows.
- Keep automation safety changes separate from candidate plugin visibility, AI intel, project artifacts, and cleanup/archive work.

## Required Checks Before Any Future B5a Commit

```bash
git diff --cached --name-only
git diff --cached --check
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

Expected result:

- Staged paths exactly equal the 2 B5a files.
- No staged `.agents/*`, `ai-intel/*`, `docs/proposals/*`, `projects/*`, `harness/*`, `plugins/*`, `docs/archive/*`, or root deletion state.
- No commit, push, PR, archive, deletion, cleanup, or broader automation change happens unless separately approved.
