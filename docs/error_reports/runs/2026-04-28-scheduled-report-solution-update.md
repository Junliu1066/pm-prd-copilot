# Scheduled Report Solution Update - 2026-04-28

## Change

Updated all active scheduled task prompts so reports must include solution recommendations, not only findings.

## Automations Updated

| ID | Added report requirement |
|---|---|
| `bug` | solution recommendations, smallest safe fix, alternatives, risk/tradeoff, validation command, approval requirement |
| `ai-gpt-5-5` | solution recommendation for every issue, drift, bug, AI signal, pruning candidate, or approval item |
| `codex` | solution recommendation, smallest safe fix, alternatives, validation command, user confirmation requirement |

## Checks

| Check | Result | Notes |
|---|---|---|
| `git diff --check` for updated report docs | pass | No whitespace issues. |
| automation config scan | pass | All three active automations remain `gpt-5.5` and `xhigh`. |
| `harness/run_harness.py --base-dir . --project demo-project --mode advisory` | pass | Stale `pipeline-latest` governance warning was cleared by a governed rerun. |

## Resolved Warning

`pipeline-latest` was created before a governed rerun and previously reported:

- production pipeline reached approval-gated stages without enforced approval gates
- production pipeline manifest missing required approval declarations

The user later selected方案二. `demo-project` now uses pipeline-specific test overrides, `pipeline-latest` was rerun with `--governed`, and harness is pass.

## Solution Recommendation

- Recommended action: use `--governed` for approval-gated production output and keep demo-only overrides in `pipeline_assumption_overrides`.
- Smallest safe fix: keep the current pass state and do not treat demo overrides as real product approvals.
- Alternative: create a separate run id for future governed verification if `pipeline-latest` should remain a fast-draft artifact.
- Risk/tradeoff: pipeline-specific overrides clear demo warnings without granting broader workflow or prototype approval.
- Validation command: `python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory`.
- User approval: required if real approvals are added or formal delivery policy changes.
