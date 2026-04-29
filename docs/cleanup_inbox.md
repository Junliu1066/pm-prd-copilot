# Cleanup Inbox

This is a supervised cleanup inbox. It lists things that make the repository feel messy, but no destructive action should happen until the user approves the exact move, archive, or deletion.

## Current State

- The framework layer and project layer are mostly separated, but root-level historical files make the repository harder to scan.
- `projects/` contains many generated artifacts and prototypes. These should be handled through project closeout, not deleted manually.
- Several new plugin suites and harness checkers are present. They should be reviewed as capability additions, not treated as junk.
- Empty or legacy folders exist and should be reviewed before removal.

## Candidate Root Cleanup

| Candidate | Current Path | Suggested Destination | Reason | Requires Approval |
| --- | --- | --- | --- | --- |
| Historical PRD playbook copy | `prd_pm_2026_playbook.md` | `docs/archive/prd_pm_2026_playbook.md` or remove if duplicated by `pm-prd-copilot/references/prd_pm_2026_playbook.md` | Root-level duplicate-like reference material. | Yes |
| Historical PRD template copy | `prd_template_2026.md` | `docs/archive/prd_template_2026.md` or remove if duplicated by `pm-prd-copilot/templates/prd_template_2026.md` | Root-level template copy competes with canonical template path. | Yes |
| Skill kit zip | `prd_skill_kit_2026.zip` | `docs/archive/prd_skill_kit_2026.zip` or external archive | Binary package at root obscures source layout. | Yes |
| Skill suite overview | `skill_suite_overview.md` | `docs/archive/skill_suite_overview.md` or merge into `docs/repository_map.md` | Root-level summary could become documentation. | Yes |
| Remod development notes | `Remod开发.md` | `docs/archive/Remod开发.md` or `docs/remod_development.md` | Useful note, but root-level placement is noisy. | Yes |

## Candidate Directory Cleanup

| Candidate | Current Path | Suggested Action | Reason | Requires Approval |
| --- | --- | --- | --- | --- |
| Empty script staging folder | `scripts/` | Remove if confirmed unused | Current canonical scripts live under `pm-prd-copilot/scripts/` and `ai-intel/scripts/`. | Yes |
| Legacy unpacked skills mirror | `skills/` | Archive or remove after confirming all content moved to `plugins/prd-analysis-suite/skills/` | It appears to mirror plugin-owned skills. | Yes |
| Loose text scratch folder | `text/` | Move contents into a named project or `docs/archive/` | `text/.md/答辩.md` is hard to discover and classify. | Yes |

## Project Cleanup Candidates

Project outputs should use the closeout workflow:

```bash
python3 pm-prd-copilot/scripts/router.py --base-dir . closeout --project <project>
```

Initial projects to review:

| Project | Suggested Next Step |
| --- | --- |
| `demo-project` | Review `projects/demo-project/closeout/` and decide what to distill before cleanup. |
| `fitness-app-mvp` | Generate a closeout package after current prototype/runs are reviewed. |
| `graduation-defense-agent` | Generate closeout before archiving; contains many delivery and AI planning artifacts. |
| `jiaxiaoqian-ai-invest-research` | Decide whether it is an active project or archive candidate. |
| `prompt-optimization-workbench` | Review prototype artifacts before archiving. |
| `santoip-ai-brand-video` | Review HTML prototype artifacts before archiving. |

## Do Not Clean Without Explicit Approval

- `pm-prd-copilot/`
- `plugins/`
- `registry/`
- `workflow/`
- `governance/`
- `harness/`
- `shared/`
- `teaching/`
- `stewards/`
- `.github/`
- `.agents/`
- `.env`

## Retention Rule

- Archive first; do not hard-delete during the same cleanup pass.
- Archived items become eligible for hard deletion only after 30 days.
- Before hard deletion, create or review a closeout summary, extract useful lessons into `docs/`, `teaching/`, or supervised proposals, and run governance checks.
- The user must approve the exact hard-delete list.

## Recommended Next Pass

1. Review this inbox with the user.
2. Pick one category: root cleanup, directory cleanup, or one project closeout.
3. Generate a concrete move/delete plan.
4. Execute only the approved moves.
5. Run regression and harness after structural changes.
