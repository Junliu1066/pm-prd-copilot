# Runtime Governance Index

This is the stable runtime entry for reusable project-development work. Keep this file small. Put detailed controls in modules and keep ordinary project artifacts focused on implementation.

## Core Principles

- The user's latest explicit instruction wins.
- Project-facing documents and system governance documents stay separate.
- A Codex development document is the implementation source of truth once it exists.
- Internal governance controls are not exposed in project-facing artifacts unless the user asks.
- Teaching captures reusable lessons as proposals; it does not silently update stable memory or skills.
- Efficiency review may recommend simplification, but must not lower quality, security, or test thresholds.
- Long-term runtime rules must be discoverable, versioned, reviewable, and reversible.

## Runtime Modules

| Module | Purpose |
|---|---|
| `triggers.yaml` | Machine-readable trigger map for when controls apply |
| `framework_backup_policy.md` | Required GitHub-backed backup before framework reviews and substantial runtime changes |
| `document_boundaries.md` | Separation between project artifacts and system governance |
| `lesson_absorption.md` | Runtime checks for whether reusable user corrections changed future behavior |
| `framework_review_template.md` | Standard output shape for periodic framework-layer reviews |
| `artifact_controls/index.md` | Source-of-truth, review, change, security, test, efficiency, and learning controls |

## Discovery

- Primary shallow entry: `agent.md`
- Runtime entry: `governance/runtime/index.md`
- Artifact control entry: `governance/runtime/artifact_controls/index.md`
- Optional project pointer:

```md
<!-- codex-runtime: apply governance/runtime/artifact_controls/index.md when updating this artifact -->
```

## Operating Rule

When a project involves staged plans, a final development document, packaging, multiple skills, or reusable lessons, read `triggers.yaml` first and then apply only the modules it requires.

Do not copy this runtime layer into project deliverables.
