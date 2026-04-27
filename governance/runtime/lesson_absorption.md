# Lesson Absorption Rules

## Purpose

Check whether reusable user corrections have actually changed future behavior. This file is for runtime verification; it is not a place to store every project-specific note.

## Absorption Principles

- A user correction is not stable behavior until it is captured, interpreted, and either accepted or kept as a proposal.
- Accepted lessons should change future outputs in observable ways.
- Project-specific corrections should not become generic rules unless the user marks them as reusable.
- Teaching may propose changes, but must not directly update stable memory, skills, or runtime policy without approval.

## Current Long-Term Checks

| Check | Expected Future Behavior | Evidence |
|---|---|---|
| Demo already works | Do not describe core feasibility as uncertain when the user says a demo/prototype has run successfully | Project facts section, PRD premise, final development document |
| Discussion only | When the user asks to discuss, align on a proposal before editing files | Conversation flow and absence of staged file changes |
| Governance hidden by default | Do not expose steward routing, runtime controls, Teaching, or efficiency policy in ordinary project artifacts | Project Markdown visible text |
| Codex development document source of truth | Once a final Codex development document exists, keep implementation decisions aligned to it | Final dev doc, phase plans, PRD |
| Long-term architecture rule | Put reusable system behavior in `governance/runtime/`, not in one project folder | Changed file paths |
| User latest instruction wins | If a later user correction changes the task boundary, update the current plan before continuing | Final response and subsequent edits |

## Review Method

During framework review:

1. Sample recent project artifacts.
2. Check whether visible text violates any current long-term check.
3. Inspect recent conversation corrections that affected reusable behavior.
4. Classify each issue as `absorbed`, `partially_absorbed`, or `not_absorbed`.
5. Recommend either a runtime policy update, Teaching proposal, template update, or no action.

## Non-Goals

- Do not use this file to store all user preferences.
- Do not expose this mechanism in project-facing artifacts.
- Do not convert one-off user feedback into stable rules automatically.
