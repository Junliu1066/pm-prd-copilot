# AI Intel Data Area

This folder is the dedicated GitHub-tracked area for AI intelligence data used by PM Copilot governance.

## Purpose

Store AI-related source snapshots, normalized events, daily/weekly summaries, source registries, decision notes, and job logs separately from product project artifacts.

## Directory Contract

| Path | Purpose | Write policy |
| --- | --- | --- |
| `sources/` | Curated source registry for official or primary AI sources. | Human-reviewed changes only. |
| `raw/` | Fetched source snapshots grouped by run date. | Automation may write fetched snapshots. |
| `events/` | Normalized event JSON generated from raw snapshots. | Automation may write normalized events. |
| `daily/` | Daily AI intel summaries. | Automation may write reports. |
| `weekly/` | Weekly rollups and review notes. | Human or automation may write proposals/reports. |
| `decisions/` | Governance-facing decision surfaces and watchlists. | Human-reviewed changes before adoption. |
| `logs/` | Fetch and normalization job logs. | Automation may write non-secret logs. |
| `scripts/` | Local scripts for fetch, normalization, summary, and decision doc updates. | Code changes require review. |

## Governance Rules

- Treat AI intel as source signals until verified against the original source.
- Keep source URL, collection time, source type, and verification status with any data used for product or architecture decisions.
- Do not change model providers, stable skills, workflow gates, registry entries, retention policy, deletion policy, or publishing behavior from AI intel alone.
- Architecture-impacting signals should become proposals or watch items first.
- Do not store secrets, API keys, private customer data, or unredacted sensitive project inputs here.
