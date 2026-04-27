# Project Runtime Controls

## Purpose

Provide a compact runtime checklist for development artifact work.

## Runtime Checklist

Before editing:

- Read the latest user instruction.
- Identify whether the work is project-specific or reusable governance.
- Read the project source artifact and final development document if they exist.
- Apply `index.md` controls when the output is reusable or multi-phase.

While editing:

- Keep user-facing artifacts focused on what developers need.
- Keep governance mechanics in this control layer unless explicitly exposed.
- Update the final development document when a project-level truth changes.
- Avoid adding new artifacts unless they have a distinct purpose.

Before final response:

- Run formatting checks where practical.
- List changed files.
- State whether packaging or tests were performed.
- Mention any unresolved conflicts or open parameters.

## Quiet Pointer Pattern

If a project artifact needs to cue future model runs without exposing the full governance layer in rendered Markdown, use an HTML comment:

```md
<!-- codex-runtime: apply governance/runtime/artifact_controls/index.md when updating this artifact -->
```

Do not expand this comment into visible project content unless the user asks.
