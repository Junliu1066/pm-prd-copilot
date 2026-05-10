# B3 Teaching And Steward Staging List

- Date: 2026-04-30
- Status: final staging list only
- Scope: teaching records and steward operating protocols
- Rule: this file does not approve staging, commit, push, PR, archive, cleanup, deletion, long-term memory adoption, skill promotion, harness promotion, steward promotion, or stable policy promotion.

## Conclusion

B3 is ready for user review before precise staging.

This batch covers teaching records and steward operating protocols after wording was narrowed to avoid over-generalizing PRD visuals, Codex development documents, development packages, prototype approvals, and project preference cache behavior.

B3 should be staged only with the exact file list below. It must not include proposals, error reports, automation, AI intel, project artifacts, plugins, memory-cache files, archive files, or root deletion state.

## Exact File List

| Path | Reason |
|---|---|
| `teaching/accepted_lessons.md` | Accepted long-term lessons after wording was narrowed for PRD visuals, Codex development docs, and development package boundaries. |
| `teaching/open_lessons.md` | Non-binding candidate lessons that remain pending and should not become stable behavior by themselves. |
| `teaching/teaching_log.md` | Evidence trail for user teaching, preserving accepted/proposed status distinctions. |
| `teaching/user_preferences.md` | User preferences after narrowing PRD visual, Codex development document, and package boundaries. |
| `stewards/ai_architecture_steward.md` | AI planning steward protocol; limits AI model selection to AI projects or explicit approval. |
| `stewards/ai_coaching_steward.md` | AI coaching and memory steward protocol with privacy and approval boundaries. |
| `stewards/capability_enablement_steward.md` | Reuse-first capability steward protocol that preserves "如无必要，不增 skill / harness". |
| `stewards/delivery_planning_steward.md` | Delivery planning steward protocol with scope, release, external service, and destructive-operation approvals. |
| `stewards/development_governance_steward.md` | Development governance steward protocol for contract alignment and read/write boundaries. |
| `stewards/learning_steward.md` | Learning steward protocol with explicit project preference cache and long-term memory approval boundaries. |
| `stewards/prototype_design_steward.md` | Prototype design steward protocol with explicit approval requirements for full prototype, HTML/package, reusable UI style, and product-scope-impacting changes. |

## Exact Staging Command

If the user approves B3 precise staging, use only this command:

```bash
git add teaching/accepted_lessons.md teaching/open_lessons.md teaching/teaching_log.md teaching/user_preferences.md stewards/ai_architecture_steward.md stewards/ai_coaching_steward.md stewards/capability_enablement_steward.md stewards/delivery_planning_steward.md stewards/development_governance_steward.md stewards/learning_steward.md stewards/prototype_design_steward.md
```

Do not use:

```bash
git add .
git add teaching/
git add stewards/
git add docs/
git add docs/proposals/
git add docs/error_reports/
git add projects/
git add plugins/
```

## Must Not Be Included In B3

| Excluded scope | Reason |
|---|---|
| `docs/proposals/*` | Proposal and audit records; B3 list itself is not part of B3 staging unless separately approved. |
| `docs/error_reports/*` | B4 error evidence batch. |
| `.github/*` | Automation behavior; requires separate automation review. |
| `.agents/*` | Candidate plugin visibility; belongs to D batch. |
| `ai-intel/*` | AI intelligence collection/reporting; needs separate write-boundary review. |
| `projects/*` | Project artifacts; belongs to C batch and project-by-project review. |
| `plugins/*` | Candidate capabilities; belongs to D batch. |
| `memory-cache/*` | Project preference cache data; closeout/disposition only. |
| `docs/archive/*` | Archive evidence; belongs to E batch and must not imply deletion approval. |
| Root deleted files | Cleanup/delete state; belongs to E batch and requires exact approval. |
| Other existing steward files not listed above | Not changed in the current B3 scope. |

## Post-Staging Verification

If staging is later approved and executed, immediately run:

```bash
git diff --cached --name-only
git diff --cached --stat
```

The staged file list must exactly match the 11 B3 files above. If any extra path appears, stop and do not commit.

## Rollback Commands

If only the staged state needs to be reverted:

```bash
git restore --staged teaching/accepted_lessons.md teaching/open_lessons.md teaching/teaching_log.md teaching/user_preferences.md stewards/ai_architecture_steward.md stewards/ai_coaching_steward.md stewards/capability_enablement_steward.md stewards/delivery_planning_steward.md stewards/development_governance_steward.md stewards/learning_steward.md stewards/prototype_design_steward.md
```

This rollback only unstages B3 files. It must not restore working-tree changes and must not touch unrelated user or project changes.

## Commit Intent For Later Review

If B3 staging is approved and later passes commit review, the suggested commit topic is:

```text
Document teaching and steward boundaries
```

Suggested commit body points:

- Preserve accepted, open, and logged teaching records with explicit stable/candidate separation.
- Record user preferences after narrowing PRD visual, Codex development document, and development package scope.
- Add steward operating protocols without adding new stewards, skills, harnesses, workflows, plugins, or automations.
- Preserve project preference cache, prototype expansion, HTML package, UI style, and long-term memory approval boundaries.
- Keep proposals, error reports, automation, AI intel, project artifacts, archives, plugins, memory-cache data, and root deletion state out of this commit.

## Required Checks Before Any Future B3 Commit

```bash
git diff --cached --name-only
git diff --cached --check
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

Expected result:

- Staged paths exactly equal the 11 B3 files.
- No staged `docs/proposals/*`, `docs/error_reports/*`, `.github/*`, `.agents/*`, `ai-intel/*`, `projects/*`, `plugins/*`, `memory-cache/*`, `docs/archive/*`, or root deletion state.
- No commit, push, PR, archive, deletion, cleanup, or long-term memory adoption happens unless separately approved.
