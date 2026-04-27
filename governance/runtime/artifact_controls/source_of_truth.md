# Source Of Truth Controls

## Purpose

Prevent project artifacts, staged plans, skill outputs, and review notes from drifting into conflicting versions of the same requirement or technical decision.

## Rules

- Treat the final development document as the primary source of truth for implementation once it exists.
- Treat PRD and staged plans as inputs to the final development document, not independent competing specifications.
- When a staged document and final development document disagree, update the final development document or explicitly record the unresolved conflict.
- Do not leave two visible artifacts with different API fields, status names, role permissions, acceptance criteria, or security rules.
- Do not present feasibility as uncertain when the user has confirmed a demo or prototype is already running.

## Required Checks

Before marking a development artifact final, verify:

- Project status and feasibility language match the user's latest statement.
- Phase names and scope boundaries are consistent across PRD, phase plans, and final development document.
- State names and user-facing labels are consistent.
- API fields are consistent across PRD, development design, Agent design, and tests.
- Database fields are consistent with API and UI requirements.
- Test requirements map to the same modules and fields described in the implementation sections.

## Conflict Handling

When conflict is found:

1. Identify the conflicting files and sections.
2. Decide which source should win based on the user's latest instruction and explicit artifact hierarchy.
3. Update the final development document first.
4. Update or annotate older staged artifacts only if they will continue to be used.
5. Report the conflict resolution briefly in the final response.
