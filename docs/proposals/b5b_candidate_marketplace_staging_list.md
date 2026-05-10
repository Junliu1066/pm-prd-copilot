# B5b Candidate Plugin Marketplace Staging List

- Date: 2026-04-30
- Status: conditional staging list only
- Scope: candidate plugin marketplace visibility
- Rule: this file does not approve staging, commit, push, PR, plugin promotion, registry promotion, skill creation, harness creation, archive, cleanup, or deletion.

## Conclusion

B5b is ready for user review before precise staging, but it should not be committed as a standalone stable change unless registry alignment is also handled before or with the final commit plan.

The marketplace entries are internally consistent with the current working tree:

- All 6 candidate plugins have marketplace entries.
- All 6 marketplace entries are present in `registry/plugins.yaml` in the current working tree.
- All 6 marketplace source paths have corresponding plugin folders.
- All marketplace entries are explicitly marked as candidate, non-stable, detachable, and requiring user review before stable use.

The remaining risk is commit sequencing. If `.agents/plugins/marketplace.json` is committed before the matching registry state, the stable repository can temporarily show candidate plugins as available before the stable registry fully describes their candidate boundary.

Recommended handling:

- Allow B5b precise staging only after user approval.
- Do not commit B5b until the registry/candidate alignment commit plan is ready, unless the user explicitly accepts a temporary marketplace/registry sequencing gap.
- Keep candidate plugin source files in D batch, not B5b.

## Exact File List

| Path | Reason |
|---|---|
| `.agents/plugins/marketplace.json` | Makes candidate plugin suites visible while marking them candidate / non-stable / detachable / user-review-required. |

## Candidate Plugins Covered

| Plugin | Marketplace status | Registry status in working tree | Plugin folder |
|---|---|---|---|
| `prd-analysis-suite` | candidate / non-stable | candidate | present |
| `prd-prototype-suite` | candidate / non-stable | candidate | present |
| `preference-memory-suite` | candidate / non-stable | candidate | present |
| `quality-evaluation-suite` | candidate / non-stable | candidate | present |
| `delivery-planning-suite` | candidate / non-stable | candidate | present |
| `ai-solution-planning-suite` | candidate / non-stable | candidate | present |

## Required Marketplace Governance Fields

Each marketplace plugin entry must keep these fields:

```json
{
  "governance": {
    "status": "candidate",
    "stable": false,
    "detachable": true,
    "reviewLabel": "candidate / requires review / non-stable capability",
    "requiresUserReviewBeforeStableUse": true
  }
}
```

These fields are the guardrail that prevents visible candidate plugins from being mistaken for stable architecture.

## Exact Staging Command

If the user approves B5b precise staging, use only this command:

```bash
git add .agents/plugins/marketplace.json
```

Do not use:

```bash
git add .
git add .agents/
git add plugins/
git add registry/
git add docs/
```

## Must Not Be Included In B5b

| Excluded scope | Reason |
|---|---|
| `registry/plugins.yaml` | Needs a dedicated registry/candidate alignment review before commit sequencing is decided. |
| `registry/skills.yaml` | Skill registry changes must not be bundled with marketplace visibility. |
| `plugins/*` | Candidate plugin source belongs to D batch. |
| `harness/*` | Optional candidate checkers belong to D or later minimality review. |
| `ai-intel/*` | AI intel data area belongs to B5c. |
| `.github/*` | Workflow check-only safety was already handled by B5a. |
| `projects/*` | Project artifacts belong to C batch. |
| `docs/proposals/*` | Review docs are audit records, not part of marketplace visibility. |
| `docs/archive/*` and root deleted files | Cleanup/archive belongs to E batch and requires exact approval. |

## Validation Already Performed

Alignment check result:

```text
marketplace: prd-analysis-suite, prd-prototype-suite, preference-memory-suite, quality-evaluation-suite, delivery-planning-suite, ai-solution-planning-suite
registry: prd-analysis-suite, prd-prototype-suite, preference-memory-suite, quality-evaluation-suite, delivery-planning-suite, ai-solution-planning-suite
folders: ai-solution-planning-suite, delivery-planning-suite, prd-analysis-suite, prd-prototype-suite, preference-memory-suite, quality-evaluation-suite
issues: none
```

## Post-Staging Verification

If staging is later approved and executed, immediately run:

```bash
git diff --cached --name-only
git diff --cached --stat
```

The staged file list must exactly match:

```text
.agents/plugins/marketplace.json
```

## Commit Intent For Later Review

B5b should only move to commit review after the user decides the registry sequencing point.

Suggested commit topic if approved:

```text
Mark candidate plugins visible with governance labels
```

Suggested commit body points:

- Make candidate plugin suites visible in the local marketplace.
- Preserve candidate, non-stable, detachable, and user-review-required labels.
- Keep marketplace visibility separate from plugin source, skill registry, harness, AI intel, project artifacts, and archive/delete work.
- Confirm registry alignment before final commit or explicitly accept the temporary sequencing gap.

## Required Checks Before Any Future B5b Commit

```bash
git diff --cached --name-only
git diff --cached --check
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

Expected result:

- Staged paths exactly equal `.agents/plugins/marketplace.json`.
- No staged `registry/*`, `plugins/*`, `harness/*`, `ai-intel/*`, `.github/*`, `projects/*`, `docs/proposals/*`, `docs/archive/*`, or root deletion state.
- No commit, push, PR, plugin promotion, stable-policy adoption, archive, deletion, or cleanup happens unless separately approved.

