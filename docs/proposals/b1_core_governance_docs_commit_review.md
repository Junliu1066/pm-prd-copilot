# B1 Core Governance Docs Commit Review

- Date: 2026-04-29
- Status: commit review only
- Current staged scope: B1 17 core governance documentation files
- Rule: this file does not approve commit, push, PR, archive, cleanup, deletion, plugin promotion, skill promotion, harness promotion, or stable policy promotion.

## 1. Current Staged Scope

The current staged area must remain exactly these 17 files:

```text
AGENTS.md
README.md
agent.md
docs/architecture-inbox/zero_to_one_prd_quality_feedback.md
docs/architecture.md
docs/cleanup_inbox.md
docs/contract_responsibility_layer.md
docs/daily_report_template.md
docs/governance_repair_closeout_report.md
docs/operating_model.md
docs/project_lifecycle.md
docs/prototype_flow.md
docs/repository_map.md
docs/scheduled_check_mechanisms.md
docs/two_round_self_check.md
docs/version_model_update_review.md
docs/workspace_change_partition.md
```

Current staged stat:

```text
17 files changed, 1699 insertions(+), 113 deletions(-)
```

The staged scope does not include:

- `docs/proposals/*`
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
Document core governance operating model
```

Recommended commit body:

```text
- Add repository-level governance navigation and safe operating boundaries.
- Document lifecycle, prototype flow, cleanup, daily reporting, and two-round self-check expectations.
- Record contract responsibility and workspace partition rules for supervised architecture repair.
- Keep architecture inbox entries as candidate knowledge, not automatic stable rules.
- Keep proposals, teaching, steward protocols, automation, AI intel, project artifacts, archives, and candidate plugins out of this commit.
```

## 3. Required Pre-Commit Checks

Before any B1 commit, run:

```bash
git diff --cached --name-only
git diff --cached --check
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

Acceptance criteria:

- `git diff --cached --name-only` exactly equals the 17 files in Section 1.
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

If the user explicitly approves the B1 commit after this review:

```bash
git commit -m "Document core governance operating model"
```

Do not use this command until approval is explicit.

## 5. Post-Commit Verification

After a future approved commit, run:

```bash
git show --stat --oneline --name-only HEAD
git status --short
```

Expected result:

- Latest commit contains only the 17 B1 files from Section 1.
- No `docs/proposals/*` file is included in the commit.
- No project, plugin, archive, automation, AI intel, teaching, steward, or root deletion path is included.
- Remaining uncommitted work stays in the worktree for later B2/B3/B4/B5/C/D/E review.

## 6. Rollback Strategy

If commit is not yet created and staged state must be reverted:

```bash
git restore --staged AGENTS.md README.md agent.md docs/architecture-inbox/zero_to_one_prd_quality_feedback.md docs/architecture.md docs/cleanup_inbox.md docs/contract_responsibility_layer.md docs/daily_report_template.md docs/governance_repair_closeout_report.md docs/operating_model.md docs/project_lifecycle.md docs/prototype_flow.md docs/repository_map.md docs/scheduled_check_mechanisms.md docs/two_round_self_check.md docs/version_model_update_review.md docs/workspace_change_partition.md
```

This only unstages B1 files. It must not restore working-tree changes.

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
- staging any other `docs/proposals/*`
- staging `teaching/*`
- staging `stewards/*`
- staging `docs/error_reports/*`
- staging `.github/*`, `.agents/*`, or `ai-intel/*`
- staging `projects/*`, `plugins/*`, `docs/archive/*`, or root deletion state
- archive, deletion, cleanup, or hard delete
- turning architecture inbox items into stable policy
- turning lifecycle proposal into stable policy

## 8. Next Step

If the user approves, execute the B1 commit only after rerunning the pre-commit checks in Section 3.
