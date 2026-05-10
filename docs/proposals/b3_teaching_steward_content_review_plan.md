# B3 Teaching And Steward Content Review Plan

- Date: 2026-04-29
- Status: content review plan only
- Scope: `teaching/*` and `stewards/*`
- Rule: this file does not approve staging, commit, push, PR, archive, cleanup, deletion, long-term memory adoption, skill promotion, harness promotion, or steward promotion.

## 1. Goal

B3 is more sensitive than B1 and B2 because it touches user teaching records, preferences, and steward operating protocols. These files can affect future behavior, so they need content review before any staging.

The goal is to separate:

- accepted long-term lessons that the user has explicitly approved
- open lessons that remain non-binding
- project-specific preferences that must not cross projects
- steward protocols that clarify responsibility without creating unnecessary new roles
- any wording that accidentally turns a one-time correction into stable policy

## 2. Candidate Files

Content review should cover:

```text
teaching/accepted_lessons.md
teaching/open_lessons.md
teaching/teaching_log.md
teaching/user_preferences.md
stewards/ai_architecture_steward.md
stewards/ai_coaching_steward.md
stewards/capability_enablement_steward.md
stewards/delivery_planning_steward.md
stewards/development_governance_steward.md
stewards/learning_steward.md
stewards/prototype_design_steward.md
```

Do not include unrelated existing steward files unless a separate review shows they changed.

## 3. Review Questions

For each teaching file:

- Does it distinguish accepted lessons from open lessons?
- Does it mark project-specific preferences as project-local?
- Does it avoid automatically writing project preferences into long-term memory?
- Does it include user-approved stable preferences only?
- Does it preserve evidence without overfitting to one test project?

For each steward protocol:

- Does it clarify responsibility without adding a new steward?
- Does it respect "如无必要，不增 skill / harness"?
- Does it state inputs, outputs, forbidden actions, and approval points?
- Does it avoid granting autonomous authority over deletion, archive, push, PR, stable policy, long-term memory, or candidate promotion?
- Does it align with B1 core governance docs and existing governance registry behavior?

## 4. Recommended Treatment

| Group | Recommended action | Reason |
|---|---|---|
| `teaching/accepted_lessons.md` | Review line by line before staging | It can become long-term behavior. |
| `teaching/open_lessons.md` | Keep non-binding unless user approves promotion | Open lessons are candidates, not rules. |
| `teaching/teaching_log.md` | Preserve as evidence if no sensitive overreach | Useful history, but not automatic policy. |
| `teaching/user_preferences.md` | Require user approval for each stable preference | This directly shapes future behavior. |
| `stewards/*.md` | Review as responsibility protocols, not new governance components | They should clarify owners without expanding architecture. |

## 5. Must Not Happen In B3 Review

- No staging.
- No commit.
- No push or PR.
- No deletion, archive, cleanup, or hard delete.
- No long-term memory adoption without explicit user approval.
- No new skill, harness, workflow stage, plugin, registry category, or automation.
- No project preference promoted to global rule automatically.
- No steward given authority to bypass user approvals.

## 6. Output Of The Next B3 Step

The next B3 step should produce:

```text
docs/proposals/b3_teaching_steward_content_review.md
```

That review should include:

- file-by-file content summary
- approved / candidate / needs-user-review classification
- risky wording that should be revised before staging
- exact B3 staging recommendation
- remaining decisions that require user approval

## 7. Validation Plan

After the content review is generated:

```bash
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
git diff --cached --name-only
```

Expected result:

- B2 staged files remain unchanged unless the user has approved B2 commit.
- B3 review files remain unstaged.
- No project files are written.
- No stable policy or long-term memory is adopted by the review itself.
