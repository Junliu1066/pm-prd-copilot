---
name: product-flow-mapper
description: Map user-facing product business flows for PRDs, including core paths, decision points, system feedback, and edge cases. Use when the user needs diagrams like start to page action to system response to next step, not internal agent, skill, MCP, or governance workflows.
---

# Product Flow Mapper

## Purpose

Turn confirmed PRD scope into user-facing business paths. This skill draws how the product works for the user, not how the PM Copilot or skills operate internally.

## Workflow

1. Read the confirmed or proposed MVP scope, target user, and core scenario.
2. Read approved project preferences when available; do not use cleared or unrelated project caches.
3. Select one flow at a time unless the user asks for a full set.
4. Define the flow trigger, entry page, user actions, system responses, decision points, success end state, and failure/exception paths.
5. Draw an editable flow diagram. Prefer Mermaid for PRD text and optionally provide an HTML/SVG implementation when the user wants a visual preview.
6. Keep the flow product-facing:
   - good: user enters a product scenario, takes an action, receives system feedback, makes the next decision, and reaches a product outcome.
   - bad: source collector calls scenario ranker, harness validates trace.
7. Identify general business-control points before drawing:
   - what information helps the user decide to start.
   - what the user can adjust during execution.
   - what the system records as product data.
   - where the system should only remind versus automatically advance.
   - where user confirmation is required because the real-world action happens outside the app.
8. Mark assumptions and questions instead of inventing unconfirmed product behavior.
9. Hand approved flows to `low-fi-prototype-designer`.

## Case-To-Skill Generalization

When learning from a project case, extract reusable product-flow principles rather than copying the case's domain nouns into the skill.

- Store project-specific decisions in the current project's preference cache.
- Store cross-project rules as abstract checks, for example "show decision-support summary before commitment" instead of copying a specific project's summary module.
- Do not make one project's labels, modules, or scenarios the default for other projects.
- If a lesson only works in one domain, keep it in the project cache and do not update the generic skill.

## Prototype Feedback Backflow

When the user reviews a prototype and requests changes:

1. Classify each item as business logic, page structure, copy, visual style, or exception-state feedback.
2. If feedback changes business logic, update the product flow before or together with the prototype.
3. If feedback only changes visual style, do not rewrite the product flow.
4. Keep flow diagrams, page specs, and prototype images consistent.
5. Record unresolved product decisions as approval questions.

## Output Contract

Read [references/output-contract.md](references/output-contract.md) for the formal artifact shape. Always include:

- `flow_id`
- `target_user`
- `trigger`
- `primary_path`
- `decision_points`
- `system_feedback`
- `edge_cases`
- `diagram`
- `prototype_feedback_backflow`
- `approval_questions`

## Guardrails

- Do not describe internal skill/MCP/harness workflows unless the product itself is an internal workflow tool.
- Do not decide MVP scope.
- Do not draw full wireframes; hand that to `low-fi-prototype-designer`.
- Do not skip exception states when they affect product requirements.
- Do not hard-code domain-specific paths learned from one project into the generic flow method.
