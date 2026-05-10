# B5c AI Intel Candidate Staging List

- Date: 2026-04-30
- Status: final staging list only
- Scope: AI intel candidate data area and write-boundary documentation
- Rule: this file does not approve staging, commit, push, PR, network automation, scheduled job activation, model/provider changes, stable policy changes, registry changes, skill changes, harness changes, archive, cleanup, deletion, or long-term memory updates.

## Conclusion

B5c can move to user review before precise staging, but it must remain candidate infrastructure.

This batch should stage only the AI intel directory contract, curated source registry, decision surfaces, scripts, and empty output-folder placeholders. It must not stage generated raw pages, generated event JSON, generated daily reports, generated logs, or Python cache files.

Recommended next action:

- If the user approves, stage the exact B5c file list below.
- Do not commit B5c until a separate B5c commit review is generated and approved.
- Do not enable scheduled/network automation from this batch.

## Exact File List

| Path | Reason |
|---|---|
| `ai-intel/README.md` | Defines the AI intel data area, write policy, and governance guardrails. |
| `ai-intel/sources/registry.yaml` | Curated official/primary AI source registry. |
| `ai-intel/decisions/model-selection-matrix.md` | Candidate decision surface for model selection signals. |
| `ai-intel/decisions/vendor-watchlist.md` | Candidate watchlist for vendor and release changes. |
| `ai-intel/decisions/capability-map.md` | Candidate capability signal map. |
| `ai-intel/decisions/governance-architecture-signals.md` | Candidate architecture-impact classification surface. |
| `ai-intel/scripts/fetch_sources.py` | Candidate fetch script; writes raw snapshots and logs when explicitly run. |
| `ai-intel/scripts/normalize_events.py` | Candidate normalization script; writes event JSON when explicitly run. |
| `ai-intel/scripts/summarize_daily.py` | Candidate daily summary script with architecture-signal guardrails. |
| `ai-intel/scripts/update_decision_matrix.py` | Candidate decision-doc updater; includes governance architecture signals. |
| `ai-intel/daily/.gitkeep` | Placeholder only; does not approve generated daily reports. |
| `ai-intel/events/.gitkeep` | Placeholder only; does not approve generated event JSON. |
| `ai-intel/logs/.gitkeep` | Placeholder only; does not approve generated job logs. |
| `ai-intel/raw/.gitkeep` | Placeholder only; does not approve fetched raw source snapshots. |
| `ai-intel/weekly/.gitkeep` | Placeholder only; does not approve generated weekly reports. |

## Exact Staging Command

If the user approves B5c precise staging, use only this command:

```bash
git add ai-intel/README.md ai-intel/sources/registry.yaml ai-intel/decisions/model-selection-matrix.md ai-intel/decisions/vendor-watchlist.md ai-intel/decisions/capability-map.md ai-intel/decisions/governance-architecture-signals.md ai-intel/scripts/fetch_sources.py ai-intel/scripts/normalize_events.py ai-intel/scripts/summarize_daily.py ai-intel/scripts/update_decision_matrix.py ai-intel/daily/.gitkeep ai-intel/events/.gitkeep ai-intel/logs/.gitkeep ai-intel/raw/.gitkeep ai-intel/weekly/.gitkeep
```

Do not use:

```bash
git add .
git add ai-intel/
git add ai-intel/scripts/
git add docs/
```

## Must Not Be Included In B5c

| Excluded scope | Reason |
|---|---|
| `ai-intel/scripts/__pycache__/*` | Generated Python bytecode. |
| `ai-intel/raw/<run-output>/*` | Raw fetched pages need separate evidence review. |
| `ai-intel/events/<generated-run>.json` | Generated normalized events need separate evidence review. |
| `ai-intel/daily/<generated-run>.md` | Generated daily reports need separate review before commit. |
| `ai-intel/logs/<generated-run>.json` | Generated logs are run evidence, not stable candidate infrastructure. |
| `docs/proposals/*` | Review records are not part of AI intel infrastructure. |
| `projects/*` | Project artifacts belong to C batch. |
| `harness/*` | Harness additions require separate minimality review. |
| `plugins/*` | Candidate plugin source was handled separately by D1. |
| `docs/archive/*` and root deleted files | Cleanup/archive belongs to E batch. |

## Commit Intent For Later Review

If B5c precise staging is approved and later passes commit review, suggested commit topic:

```text
Add candidate AI intel data area
```

Suggested commit body points:

- Add a candidate AI intel directory contract and source registry.
- Add decision surfaces for model, vendor, capability, and governance architecture signals.
- Add fetch, normalize, daily summary, and decision update scripts as supervised candidate tools.
- Keep generated outputs, Python cache, project artifacts, harness changes, plugins, archive/delete state, and proposal docs out of the commit.
- Do not activate scheduled/network automation from this commit.

## Required Checks Before Any Future B5c Commit

```bash
git diff --cached --name-only
git diff --cached --check
git diff --check
PYTHONPYCACHEPREFIX=/tmp/pycache python3 -m py_compile ai-intel/scripts/fetch_sources.py ai-intel/scripts/normalize_events.py ai-intel/scripts/summarize_daily.py ai-intel/scripts/update_decision_matrix.py
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

Extra exclusion check:

```bash
git diff --cached --name-only | rg "__pycache__|ai-intel/raw/.+|ai-intel/events/.+\\.json|ai-intel/daily/.+\\.md|ai-intel/logs/.+\\.json|docs/proposals|projects/|harness/|plugins/|docs/archive|^prd_|skill_suite_overview"
```

Expected result for the exclusion check: no output.

## User Decisions Still Needed

| Decision | My recommendation | Reason |
|---|---|---|
| Approve B5c precise staging | Yes, after reviewing this list | It stages candidate infrastructure only, not generated outputs. |
| Approve B5c commit | Later, after commit review | Staging and commit should remain separate. |
| Enable scheduled/network AI intel automation | Not yet | Scripts write repo files and may require network access. |
| Commit generated AI intel reports | Not yet | Generated evidence needs separate review. |

