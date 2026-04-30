---
name: prototype-reference-analyzer
description: Analyze user-provided or externally collected reference images for PRD prototypes, wireframes, product flow diagrams, annotation styles, and page-transition examples. Use when prototype output should borrow structure from reference images before drawing product flows or low-fidelity screens.
---

# Prototype Reference Analyzer

## Purpose

Extract reusable prototype expression patterns from reference images or sourced examples. This skill does not draw the final prototype; it defines what can be borrowed safely and what must not be copied.

## Workflow

1. Inventory all reference inputs: uploaded images, screenshots, PDF pages, app screenshots, external examples, or user descriptions.
2. Classify each reference as `user_provided_reference`, `external_reference`, or `inferred_reference_need`.
3. Read approved project prototype preferences when available; treat candidate preferences as non-binding review context.
4. Extract expression traits:
   - fidelity level: sketch, low-fi, mid-fi, high-fi.
   - layout structure: phone frames, screen count, canvas arrangement, spacing, labels.
   - annotation style: arrows, callouts, numbered steps, side notes.
   - information density: title, screen title, main CTA, secondary actions, empty/error states.
   - flow style: horizontal journey, branching decision, multi-screen storyboard.
5. Parse style directives from user language, not only images. Treat concrete style words as project-specific unless the user asks to make them reusable.
6. Convert style directives into prototype expression rules: palette, contrast, typography weight, density, geometry, annotation style, and what not to overdo.
7. Identify borrowable patterns and non-borrowable elements.
8. Preserve source trace. External references are signals only and require human verification.
9. Hand the analysis to `product-flow-mapper` or `low-fi-prototype-designer`.

## Output Contract

Read [references/output-contract.md](references/output-contract.md) for the formal artifact shape. Always include:

- `reference_inventory`
- `borrowable_patterns`
- `do_not_copy`
- `recommended_prototype_style`
- `style_directives`
- `trace_notes`

## Guardrails

- Do not copy proprietary UI, brand assets, exact visual identity, or competitor wording.
- Do not treat external references as verified truth.
- Do not draw product screens; this skill only extracts reference guidance.
- Do not use reference images to override confirmed PRD scope.
- Do not turn style words into high-fidelity UI unless the user explicitly asks for high fidelity.
