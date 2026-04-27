# Cache Lifecycle Policy

## Purpose

Keep the Codex/PM Copilot framework clean over repeated projects by separating framework backups, project archives, validation reports, and disposable runtime cache.

This policy applies to framework operation and project closeout. It does not turn project-specific files into framework truth.

## Artifact Classes

| Class | Examples | Default Action |
|---|---|---|
| Framework backup | `framework-backup/YYYYMMDD-HHMMSS` tags | Push to GitHub and retain by policy |
| Framework source | `agent.md`, `governance/`, `registry/`, `harness/`, templates | Commit through normal framework branches |
| Project final artifact | final PRD, final Codex development document, handoff README | Keep under `projects/<project>/` |
| Project intermediate artifact | generated drafts, temporary phase docs, analysis outputs | Archive or remove during project closeout |
| Harness run artifact | `manifest.json`, `trace.json`, `harness_report.json`, efficiency reports | Keep named final runs; prune temporary runs |
| Runtime cache | `.venv/`, `dist/`, `__pycache__/`, logs, temp downloads | Ignore and delete when no longer needed |
| Package artifact | generated `.zip` or handoff bundles | Regenerate from source unless explicitly retained |

## Framework Backup Retention

- Keep at least the latest 8 weekly `framework-backup/*` tags.
- Keep backups around substantial runtime/governance changes until the next two weekly reviews pass.
- Keep major architecture baseline tags unless the user approves removal.
- Do not include uncommitted project artifacts in framework backups.

## Project Closeout

When a project ends:

1. Freeze the final source of truth.
2. Confirm final PRD, final Codex development document, and handoff README.
3. Create or update a project closeout manifest.
4. Keep named final harness runs such as `m1-final`, `release-final`, or `archive-final`.
5. Move useful intermediate context to `projects/<project>/archive/intermediate/` or remove it if explicitly disposable.
6. Delete or ignore regenerated packages under `dist/`.
7. Mark `project_state.json` as `released` or `archived`.
8. Capture reusable lessons through Teaching proposals.

## Harness Run Retention

- Keep `pipeline-latest` as the current moving run.
- Keep named final runs for significant milestones.
- Do not keep every timestamped exploratory run forever.
- Prefer relative paths in reports to avoid workspace-path noise.
- Restore generated report noise after validation unless the report change is the intended artifact.

## Git Branch And Tag Cleanup

- Delete merged feature branches after PR merge when no longer needed.
- Mark abandoned experiment branches before deleting if they contain useful context.
- Keep framework backup tags according to the retention policy.
- Use project release tags only for formal project deliveries.

## Cleanup Guardrails

- Never delete user-created artifacts without explicit request.
- Never delete the latest final source of truth.
- Never clean framework backups before confirming there is a newer known-good backup.
- Do not commit `.venv/`, generated `dist/` packages, logs, or local cache.
- If cleanup would affect project deliverables, summarize the plan before acting.

## Closeout Checklist

- [ ] Final source-of-truth artifact identified.
- [ ] Project handoff README exists or is explicitly not needed.
- [ ] Required validation has passed.
- [ ] Temporary generated reports are restored or intentionally committed.
- [ ] Disposable runtime cache is ignored or removed.
- [ ] Framework backup exists if framework rules changed during the project.
- [ ] Teaching proposal created for reusable lessons.
