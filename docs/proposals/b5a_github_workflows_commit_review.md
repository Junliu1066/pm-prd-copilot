# B5a GitHub Workflows Commit Review

- Date: 2026-04-30
- Status: commit review only
- Current staged scope: B5a 2 GitHub workflow files
- Rule: this file does not approve push, PR, archive, cleanup, deletion, broader automation changes, AI intel adoption, or candidate plugin promotion.

## 1. Current Staged Scope

The current staged area must remain exactly these 2 files:

```text
.github/workflows/regression.yml
.github/workflows/skill-upgrade-review.yml
```

Current staged stat:

```text
2 files changed, 2 insertions(+), 8 deletions(-)
```

The staged scope does not include:

- this commit review file
- `.agents/*`
- `ai-intel/*`
- `docs/proposals/*`
- `projects/*`
- `harness/*`
- `plugins/*`
- `docs/archive/*`
- root deleted files

## 2. Recommended Commit Message

```text
Make governance workflows check-only
```

Recommended commit body:

```text
- Remove CI steps that refreshed demo pipeline outputs.
- Run governance harness with --check-only in regression and skill-upgrade review workflows.
- Keep automation safety changes separate from candidate plugin visibility, AI intel, project artifacts, and cleanup/archive work.
```

## 3. Required Pre-Commit Checks

Before any B5a commit, run:

```bash
git diff --cached --name-only
git diff --cached --check
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

Acceptance criteria:

- `git diff --cached --name-only` exactly equals the 2 files in Section 1.
- `git diff --cached --check` passes.
- `git diff --check` passes.
- Regression passes.
- Harness passes in `check-only` mode.
- Harness reports no project files written.

## 4. Exact Commit Command For Later Approval

If the B5a commit is approved after this review:

```bash
git commit -m "Make governance workflows check-only"
```

## 5. Post-Commit Verification

After a future approved commit, run:

```bash
git show --stat --oneline --name-only HEAD
git status --short
```

Expected result:

- Latest commit contains only the 2 B5a workflow files from Section 1.
- This commit review file is not included unless separately staged in a later audit batch.
- No `.agents`, `ai-intel`, proposal, project, harness, plugin, archive, or root deletion path is included.

## 6. Rollback Strategy

If commit is not yet created and staged state must be reverted:

```bash
git restore --staged .github/workflows/regression.yml .github/workflows/skill-upgrade-review.yml
```

If a future commit is created and later needs to be undone:

```bash
git revert <commit>
```

Do not use `git reset --hard`. Do not revert or overwrite unrelated user or project changes.

## 7. Explicitly Not Approved By This Review

This review does not approve:

- push or PR
- staging this review file
- staging `.agents/*`, `ai-intel/*`, `docs/proposals/*`, `projects/*`, `harness/*`, `plugins/*`, `docs/archive/*`, or root deletion state
- archive, deletion, cleanup, or hard delete
- broader automation changes beyond the two staged workflow files

## 8. Next Step

If continuing according to the approved order, execute the B5a commit only after rerunning the pre-commit checks in Section 3.
