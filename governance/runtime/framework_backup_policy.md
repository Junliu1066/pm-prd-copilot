# Framework Backup Policy

## Purpose

Create a recoverable GitHub-backed snapshot before periodic framework review or substantial runtime/governance changes.

This policy applies to the Codex/PM Copilot framework layer, not to ordinary project artifacts.

## Required Backup Timing

Create a backup before:

- Weekly framework review.
- Runtime governance changes.
- Trigger rule changes.
- Steward, Teaching, efficiency, validation, or artifact-control changes.
- Codex development document template changes.
- Any large refactor that could affect future model behavior.

## Backup Method

Preferred method:

1. Confirm current branch and `HEAD`.
2. Confirm uncommitted changes and identify project-level artifacts that should not be included.
3. Create an annotated Git tag pointing to the pre-change framework `HEAD`.
4. Use this naming pattern:

```text
framework-backup/YYYYMMDD-HHMMSS
```

5. Push the tag to `origin`.
6. Report the tag name and commit SHA in the framework review output.

## Guardrails

- Do not include uncommitted project-specific files in framework backups.
- Do not move or overwrite existing backup tags.
- If backup tag creation or push fails, stop framework changes and report the failure.
- Keep backup tags lightweight as recovery anchors; do not commit generated zip files unless the user explicitly asks for archive artifacts.
- Use GitHub tag/source archive as the default downloadable backup package.

## Recovery Rule

If a framework change causes regression, recover by checking out or branching from the latest known-good `framework-backup/*` tag.

## Review Report Requirements

Every framework review report must include:

- Backup tag.
- Backup commit SHA.
- Whether tag push succeeded.
- Any uncommitted files intentionally excluded from the backup.
