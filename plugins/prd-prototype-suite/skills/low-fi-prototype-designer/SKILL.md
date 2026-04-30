---
name: low-fi-prototype-designer
description: Create reference-driven low-fidelity PRD prototype previews and, only after human approval, full-flow wireframes. Use when the user asks for mobile or web product prototype diagrams, page wireframes, screen flows, or annotated low-fi UX previews for a PRD.
---

# Low-Fi Prototype Designer

## Purpose

Create PRD-ready low-fidelity product prototypes that show pages, key UI regions, user actions, system feedback, transitions, and exceptions. The default output is a preview, not a complete full-flow prototype.

## Preview-First Protocol

1. Start with confirmed MVP scope, an approved or draft product flow, and any reference analysis.
2. Read approved project prototype preferences when available; ignore cleared caches and do not let candidate preferences override the current user request.
3. Produce only a prototype preview first:
   - 1 to 3 key screens.
   - one core path only.
   - enough annotation for the user to judge layout direction.
4. Ask for human review on page structure, CTA placement, wording, state coverage, visual direction, and flow direction.
5. Do not produce `full_prototype` until the user explicitly approves the preview or project state records `prototype_preview`.
6. After approval, expand to the complete screen flow with normal, empty, error, permission, loading, and success states as needed.
7. When the PRD has multiple planned phases and the user asks for all prototypes, the full prototype must cover every phase as labeled screens, while clearly marking which screens are in the current implementation phase and which are future-stage prototypes.

## Feedback Iteration Protocol

When the user gives prototype feedback:

1. Parse feedback by page, problem, and requested modification.
2. Classify each requested modification:
   - `business_logic`: changes product behavior or data model.
   - `page_structure`: changes modules, layout, or screen hierarchy.
   - `copy`: changes labels, CTA text, or explanatory text.
   - `visual_style`: changes color, typography, contrast, density, or theme.
   - `exception_state`: adds or changes error, permission, loading, empty, or timeout states.
3. Apply only the requested layer. Do not rewrite unrelated screens.
4. If feedback is `business_logic`, update or request an update to the product flow artifact too.
5. If feedback is `visual_style`, keep product behavior unchanged.
6. Regenerate preview artifacts and keep Markdown explanation, SVG/HTML, and any PNG preview synchronized.
7. Continue to block `full_prototype` until preview approval exists.

## Generalization Rules

Project cases are training examples for the skill, not permanent domain templates.

When user feedback teaches a reusable rule:

1. Convert concrete product nouns into abstract prototype checks.
2. Keep project-specific interaction decisions in the active project preference cache.
3. Update this generic skill only with industry-neutral behavior, such as:
   - preserve decision-support information that helps users estimate cost, time, risk, or effort.
   - expose adjustment entry points when real execution may differ from the planned state.
   - distinguish system reminders from automatic state transitions when users control the real-world action.
   - record user adjustments when they affect future product logic, analytics, or personalization.
4. Do not apply a previous project's visual style, labels, or modules to a new project unless the current user asks for it or the current project cache approves it.

## Reference Use

- Use `prototype-reference-analyzer` outputs when available.
- Borrow structure, annotation style, and fidelity level.
- Do not copy brand identity, exact UI, protected assets, or competitor wording.
- External references require source trace and user verification.

## Output Format

Prefer editable formats:

- Markdown with Mermaid for quick PRD embedding.
- HTML/SVG for visual prototype boards.
- PNG preview for direct user review when the environment may not render SVG or local Markdown image links.
- JSON only when downstream tooling needs structured page specs.

## Deliverability and Visual QA

Before reporting a prototype preview as ready:

1. Provide at least one directly viewable preview artifact, preferably PNG, plus the editable source artifact such as SVG or HTML.
2. Use relative links inside project Markdown when possible; avoid relying only on machine-specific absolute paths.
3. If the user says the image is not visible, treat it as a delivery bug and provide an alternate preview route before continuing design work.
4. Check visual basics manually or with tooling:
   - text does not overlap nearby labels, rings, cards, or phone frames.
   - text intended to be centered is actually center-aligned.
   - important text is not too small for review.
   - content is not clipped by the viewport or phone frame.
   - contrast is sufficient in the chosen theme.
   - generated PNG matches the editable SVG/HTML source.
5. In the final response, state what file to review and provide a fallback path if inline preview fails.

Each screen must include:

- screen goal.
- entry point.
- key content regions.
- primary CTA.
- secondary actions.
- next step.
- important exception states.

## Output Contract

Read [references/output-contract.md](references/output-contract.md) for the formal artifact shape. Always include:

- `prototype_mode`
- `approval_status`
- `screen_list`
- `screen_specs`
- `transition_annotations`
- `feedback_application_log`
- `delivery_artifacts`
- `visual_qa_checklist`
- `open_review_questions`

## Guardrails

- Do not generate a complete full-flow prototype before preview approval.
- Do not draw screens that are outside confirmed or clearly marked assumed scope.
- Do not limit full prototypes to MVP screens when the product package already contains later phases and the user asks to see all prototype screens.
- Do not replace product requirements with visual design choices.
- Keep low-fi prototypes intentionally simple; avoid high-fidelity visual design unless explicitly requested.
- Do not leave prototype images and PRD text out of sync after user feedback.
- Do not assume the user can see a prototype just because a Markdown image link was written.
- Do not turn a single project case into a generic prototype template.
