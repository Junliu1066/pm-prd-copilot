# B4 Error Reports Commit Review

- Date: 2026-04-30
- Status: commit review only
- Current staged scope: B4 9 error report evidence files
- Rule: this file does not approve push, PR, archive, cleanup, deletion, stable policy changes, automation changes, or scheduled task changes.

## 1. Current Staged Scope

The current staged area must remain exactly these 9 files:

```text
docs/error_reports/README.md
docs/error_reports/bug_log.md
docs/error_reports/daily/2026-04-28.md
docs/error_reports/daily/2026-04-29.md
docs/error_reports/daily/README.md
docs/error_reports/runs/2026-04-28-governance-system-test.md
docs/error_reports/runs/2026-04-28-initial-error-check-setup.md
docs/error_reports/runs/2026-04-28-scheduled-report-solution-update.md
docs/error_reports/runs/README.md
```

Current staged stat:

```text
9 files changed, 419 insertions(+)
```

The staged scope does not include:

- this commit review file
- `docs/proposals/*`
- `.github/*`
- `.agents/*`
- `ai-intel/*`
- `projects/*`
- `harness/*`
- `plugins/*`
- `docs/archive/*`
- root deleted files

## 2. Recommended Commit Message

```text
Record governance error report evidence
```

Recommended commit body:

```text
- Add error report directory structure and bug log.
- Preserve daily and manual-run evidence from the governance repair period.
- Keep evidence records separate from automation, AI intel, project artifacts, harness code, and cleanup/delete actions.
```

## 3. Required Pre-Commit Checks

Before any B4 commit, run:

```bash
git diff --cached --name-only
git diff --cached --check
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

Acceptance criteria:

- `git diff --cached --name-only` exactly equals the 9 files in Section 1.
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

If the B4 commit is approved after this review:

```bash
git commit -m "Record governance error report evidence"
```

## 5. Post-Commit Verification

After a future approved commit, run:

```bash
git show --stat --oneline --name-only HEAD
git status --short
```

Expected result:

- Latest commit contains only the 9 B4 files from Section 1.
- This commit review file is not included unless separately staged in a later audit batch.
- No proposal, automation, AI intel, project, harness, plugin, archive, or root deletion path is included.
- Remaining uncommitted work stays in the worktree for later B5/C/D/E review.

## 6. Rollback Strategy

If commit is not yet created and staged state must be reverted:

```bash
git restore --staged docs/error_reports/README.md docs/error_reports/bug_log.md docs/error_reports/daily/2026-04-28.md docs/error_reports/daily/2026-04-29.md docs/error_reports/daily/README.md docs/error_reports/runs/2026-04-28-governance-system-test.md docs/error_reports/runs/2026-04-28-initial-error-check-setup.md docs/error_reports/runs/2026-04-28-scheduled-report-solution-update.md docs/error_reports/runs/README.md
```

This only unstages B4 files. It must not restore working-tree changes.

If a future commit is created and later needs to be undone:

```bash
git revert <commit>
```

Do not use `git reset --hard`. Do not revert or overwrite unrelated user or project changes.

## 7. Explicitly Not Approved By This Review

This review does not approve:

- push or PR
- staging this review file
- staging `docs/proposals/*`
- staging `.github/*`, `.agents/*`, or `ai-intel/*`
- staging `projects/*`, `harness/*`, `plugins/*`, `docs/archive/*`, or root deletion state
- archive, deletion, cleanup, or hard delete
- automation changes or scheduled task changes
- stable policy changes

## 8. Next Step

If continuing according to the approved order, execute the B4 commit only after rerunning the pre-commit checks in Section 3.
