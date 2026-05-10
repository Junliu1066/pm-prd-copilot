# B5 Automation, AI Intel, And Candidate Visibility Review

- Date: 2026-04-30
- Status: partition review only
- Scope: `.github`, `.agents`, and `ai-intel`
- Rule: this file does not approve staging, commit, push, PR, archive, cleanup, deletion, automation changes, scheduled task changes, candidate plugin promotion, AI intel adoption, model changes, or stable policy changes.

## Conclusion

B5 should be split into three separate sub-batches:

1. B5a: GitHub workflow check-only safety.
2. B5b: Candidate plugin marketplace visibility.
3. B5c: AI intel data area and governance signal docs.

Do not stage B5 as one combined commit. These areas have different risk profiles:

- `.github` changes automation behavior.
- `.agents` changes candidate capability visibility.
- `ai-intel` creates an information collection and reporting surface.

## B5a: GitHub Workflow Check-Only Safety

Recommended status: `ready_for_staging_list`

Candidate files:

```text
.github/workflows/regression.yml
.github/workflows/skill-upgrade-review.yml
```

Observed change:

- Removes demo pipeline output refresh from CI workflows.
- Runs regression directly.
- Runs governance harness with `--check-only --audit --efficiency`.

Why it should be separate:

- It changes automation behavior.
- It aligns CI with the already approved harness read/write boundary.
- It reduces the risk of CI producing unreviewed project artifacts.

Recommended next action:

- Generate B5a final staging list.

## B5b: Candidate Plugin Marketplace Visibility

Recommended status: `needs_separate_staging_list`

Candidate file:

```text
.agents/plugins/marketplace.json
```

Observed change:

- Adds candidate plugin entries and governance metadata:
  - `status: candidate`
  - `stable: false`
  - `detachable: true`
  - `requiresUserReviewBeforeStableUse: true`

Why it should be separate:

- It affects what plugin capabilities appear available.
- It should not be confused with stable architecture promotion.
- It must remain aligned with registry plugin status and the "如无必要，不增 skill / harness" rule.

Recommended next action:

- After B5a, compare marketplace entries against `registry/plugins.yaml` and plugin folders.
- Then generate B5b staging list if alignment is clean.

## B5c: AI Intel Data Area And Governance Signals

Recommended status: `needs_content_and_write_boundary_review`

Candidate tracked/changed files:

```text
ai-intel/README.md
ai-intel/decisions/governance-architecture-signals.md
ai-intel/scripts/summarize_daily.py
ai-intel/scripts/update_decision_matrix.py
```

Candidate directory placeholders:

```text
ai-intel/daily/.gitkeep
ai-intel/events/.gitkeep
ai-intel/logs/.gitkeep
ai-intel/raw/.gitkeep
ai-intel/weekly/.gitkeep
```

Existing related files to consider if not already tracked:

```text
ai-intel/sources/registry.yaml
ai-intel/scripts/fetch_sources.py
ai-intel/scripts/normalize_events.py
ai-intel/decisions/model-selection-matrix.md
ai-intel/decisions/vendor-watchlist.md
ai-intel/decisions/capability-map.md
```

Must exclude:

```text
ai-intel/scripts/__pycache__/
```

Observed change:

- Adds governance architecture signal reminders to daily summaries.
- Adds `governance-architecture-signals.md` to decision matrix update checks.
- Introduces AI intel directory contract and signal classification policy.

Why it needs a separate review:

- It creates an AI information collection surface.
- It can influence model selection, workflow, registry, skills, and governance decisions.
- It must remain a signal/proposal mechanism, not an automatic stable-policy updater.

Recommended next action:

- After B5a and B5b, run an AI-intel write-boundary review and generate B5c staging list.

## Explicitly Excluded From B5

| Excluded scope | Reason |
|---|---|
| `projects/*` | Project artifacts belong to C batch. |
| `plugins/*` | Candidate plugin source belongs to D batch. |
| `registry/plugins.yaml` and `registry/skills.yaml` | Registry candidate state needs a dedicated registry/candidate alignment review. |
| `harness/*` | Harness checker additions belong to D or stable-core review, not B5. |
| `memory-cache/*` | Project preference cache data needs closeout/disposition review. |
| `docs/archive/*` | Archive evidence belongs to E batch. |
| root deleted files | Cleanup/delete state belongs to E batch and requires exact approval. |
| `ai-intel/scripts/__pycache__/*` | Python cache output; do not stage. |

## Recommended Order

1. B5a GitHub workflow check-only safety.
2. B5b candidate plugin marketplace visibility.
3. B5c AI intel data area and governance signals.
4. Registry/candidate alignment review for `registry/plugins.yaml` and `registry/skills.yaml`.
5. D batch candidate plugin source and optional checkers/scripts.

This order keeps automation safety first, then candidate visibility, then AI information governance.

## Validation Plan For This Review

```bash
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
git diff --cached --name-only
```

Expected result:

- No staging.
- No commit.
- No project files written.
- No automation or AI intel adoption happens from this review alone.
