# B3 Teaching And Steward Commit Review

- Date: 2026-04-30
- Status: commit review only
- Current staged scope: B3 11 teaching and steward files
- Rule: this file does not approve push, PR, archive, cleanup, deletion, long-term memory adoption, skill promotion, harness promotion, steward promotion, or stable policy promotion.

## 1. Current Staged Scope

The current staged area must remain exactly these 11 files:

```text
stewards/ai_architecture_steward.md
stewards/ai_coaching_steward.md
stewards/capability_enablement_steward.md
stewards/delivery_planning_steward.md
stewards/development_governance_steward.md
stewards/learning_steward.md
stewards/prototype_design_steward.md
teaching/accepted_lessons.md
teaching/open_lessons.md
teaching/teaching_log.md
teaching/user_preferences.md
```

Current staged stat:

```text
11 files changed, 682 insertions(+)
```

The staged scope does not include:

- this commit review file
- `docs/proposals/*`
- `docs/error_reports/*`
- `.github/*`
- `.agents/*`
- `ai-intel/*`
- `projects/*`
- `plugins/*`
- `memory-cache/*`
- `docs/archive/*`
- root deleted files
- generated zip, HTML, PNG, run outputs, or project closeout artifacts

## 2. Recommended Commit Message

```text
Document teaching and steward boundaries
```

Recommended commit body:

```text
- Preserve accepted, open, and logged teaching records with stable/candidate separation.
- Record user preferences after narrowing PRD visual, Codex development document, and package boundaries.
- Add steward operating protocols without adding new stewards, skills, harnesses, workflows, plugins, or automations.
- Preserve approval gates for project preference caches, long-term memory, prototype expansion, HTML packages, reusable UI style, and product-scope changes.
```

## 3. Required Pre-Commit Checks

Before any B3 commit, run:

```bash
git diff --cached --name-only
git diff --cached --check
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

Acceptance criteria:

- `git diff --cached --name-only` exactly equals the 11 files in Section 1.
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

If the B3 commit is approved after this review:

```bash
git commit -m "Document teaching and steward boundaries"
```

## 5. Post-Commit Verification

After a future approved commit, run:

```bash
git show --stat --oneline --name-only HEAD
git status --short
```

Expected result:

- Latest commit contains only the 11 B3 files from Section 1.
- This commit review file is not included unless separately staged in a later audit batch.
- No proposal, error report, project, plugin, archive, automation, AI intel, memory-cache, or root deletion path is included.
- Remaining uncommitted work stays in the worktree for later B4/B5/C/D/E review.

## 6. Rollback Strategy

If commit is not yet created and staged state must be reverted:

```bash
git restore --staged stewards/ai_architecture_steward.md stewards/ai_coaching_steward.md stewards/capability_enablement_steward.md stewards/delivery_planning_steward.md stewards/development_governance_steward.md stewards/learning_steward.md stewards/prototype_design_steward.md teaching/accepted_lessons.md teaching/open_lessons.md teaching/teaching_log.md teaching/user_preferences.md
```

This only unstages B3 files. It must not restore working-tree changes.

If a future commit is created and later needs to be undone:

```bash
git revert <commit>
```

Do not use `git reset --hard`. Do not revert or overwrite unrelated user or project changes.

## 7. Explicitly Not Approved By This Review

This review does not approve:

- push or PR
- staging this review file
- staging any other `docs/proposals/*`
- staging `docs/error_reports/*`
- staging `.github/*`, `.agents/*`, or `ai-intel/*`
- staging `projects/*`, `plugins/*`, `memory-cache/*`, `docs/archive/*`, or root deletion state
- archive, deletion, cleanup, or hard delete
- automatic long-term memory adoption
- adding new skills, harnesses, workflows, plugins, registry categories, automations, or stewards

## 8. Next Step

If continuing according to the approved order, execute the B3 commit only after rerunning the pre-commit checks in Section 3.
