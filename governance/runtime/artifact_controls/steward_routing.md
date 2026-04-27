# Steward Routing Controls

## Purpose

Route project development work through the existing steward model without exposing the coordination system inside ordinary deliverables.

## Steward Responsibilities

| Steward | Responsibility | Required When |
|---|---|---|
| Chief steward | Scope, phase boundaries, final merge, escalation | Any reusable project artifact |
| PRD steward | Requirements, user value, acceptance criteria | PRD or scope changes |
| Product judgment steward | MVP / phase boundary decisions | Feature prioritization or scope conflict |
| Technical route steward | Architecture, APIs, data model, module contracts | Development design or cross-module change |
| Review steward | Risks, contradictions, missing tests, edge cases | Before finalizing a stage |
| Efficiency steward | Artifact count, duplicated content, excessive skill use | When output grows or multiple skills are involved |
| Test steward | Harness, test matrix, acceptance verification | Before phase handoff or release |
| Teacher | User corrections, preference signals, reusable lessons | After explicit user coaching |

## Skill Routing

- Production skills may draft artifacts, but stewardship controls final scope and consistency.
- Review and efficiency skills inspect outputs; they do not silently rewrite the final artifact.
- Teaching captures user corrections as candidate lessons. It must not write stable memory or stable skill instructions without explicit approval.
- Cross-module decisions must route back to the chief steward and relevant domain steward.

## Coordination Rules

- Keep skill count proportional to project complexity.
- Prefer 4 to 7 active production skills for a medium development project.
- Use efficiency review when skill count exceeds 7, artifacts repeat the same content, or staged plans conflict.
- Do not let separate skills maintain separate truths for API, database, status, permissions, or security rules.
