# Document Boundary Rules

## Purpose

Keep project deliverables useful to developers while preserving reusable runtime governance for Codex.

## Document Classes

| Class | Audience | Content |
|---|---|---|
| Project artifact | Product, engineering, QA, deployment readers | Product facts, scope, architecture, APIs, data model, tests, deployment |
| Codex development document | Engineering handoff and model continuation | Final implementation truth, staged scope, contracts, verification, rollout |
| System governance document | Codex runtime and maintainers | Steward routing, review gates, triggers, efficiency, learning, validation |
| Teaching artifact | User and governance maintainers | Proposed reusable lessons and approved learning records |

## Rules

- Do not expose steward routing, efficiency policy, teaching policy, or runtime controls in ordinary project artifacts by default.
- Use a hidden runtime pointer when a project artifact needs future model runs to apply controls.
- Codex development documents should include implementation details, not internal governance explanations.
- System governance documents must not hard-code project-specific business decisions.
- If the user explicitly asks to reveal governance details in a project artifact, keep the section brief and mark it as process guidance rather than product or engineering requirements.

## Hidden Pointer Rules

- Required for Codex development document templates.
- Optional for phase plans intended for internal model continuation.
- Preserve the pointer for internal Windows/Linux handoff packages.
- Remove or omit the pointer for external customer-facing artifacts unless the user asks to keep it.
- Place the pointer immediately after the H1 title.

Standard pointer:

```md
<!-- codex-runtime: apply governance/runtime/artifact_controls/index.md when updating this artifact -->
```

## Boundary Checks

Before delivery, check:

- Project artifacts do not contain long explanations of internal steward systems.
- Runtime governance files do not contain project-specific requirements that belong in project artifacts.
- The final Codex development document is the only implementation source of truth.
- Older staged artifacts are either aligned with the final document or clearly treated as supporting context.
