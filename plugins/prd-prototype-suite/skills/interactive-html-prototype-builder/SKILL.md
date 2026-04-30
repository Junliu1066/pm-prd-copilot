---
name: interactive-html-prototype-builder
description: Build and revise editable, clickable HTML product prototypes for product managers from PRDs, user stories, natural-language requirements, sketches, screenshots, or existing wireframes. Use when the user asks for an HTML prototype, clickable prototype, editable prototype, browser preview, MoDao/墨刀-like prototype, 原型图转HTML, or screenshot-to-HTML prototype.
---

# Interactive HTML Prototype Builder

## Purpose

Create low- to mid-fidelity product prototypes that can be opened in a browser, clicked through, and revised by natural-language feedback. This skill expresses product structure and interaction intent; it does not replace UI design tools or produce final production UI.

## When To Use

Use this skill when the user wants:

- A clickable HTML/CSS/JS prototype from requirements, PRD, user stories, or a flow.
- An existing prototype image, sketch, or screenshot rebuilt as editable HTML.
- Iterative prototype modifications such as changing copy, modules, layout, pages, states, or interactions.
- A lightweight MoDao/Figma-style product prototype for PM review, not high-fidelity UI design.

If the user only asks for static wireframes or PRD-embedded diagrams, use `low-fi-prototype-designer`. If the user supplies reference images whose structure should guide the work, use `prototype-reference-analyzer` first.

## Core Workflow

1. Identify input mode:
   - `requirement_to_html`: requirements, PRD, stories, or flow to HTML prototype.
   - `preview_to_html`: approved preview/wireframe to HTML prototype.
   - `image_to_html`: user-supplied sketch, screenshot, or prototype image to editable HTML.
   - `modify_existing_html`: user feedback applied to existing prototype files.
2. Read existing artifacts before editing:
   - product scope, product flow, approved prototype preview, reference analysis, and project preference cache when available.
   - existing `index.html`, `styles.css`, `app.js`, `prototype_manifest.json`, and `prototype_notes.md` when modifying.
3. Confirm or infer the target surface:
   - mobile app prototype: phone-like viewport, bottom navigation when appropriate.
   - desktop web/SaaS prototype: app shell, sidebar/topbar, dense working views.
   - responsive prototype: clear desktop and mobile behavior.
4. Build only product-relevant screens and interactions. Preserve assumptions as notes instead of inventing unconfirmed business rules.
5. Convert important task-entry buttons into real prototype routes:
   - examples: create, edit, review, optimize, compare, publish, export setup, dataset creation, detail view.
   - prefer a destination page, drawer, or full workflow panel over a generic confirmation modal.
   - carry useful context from the source page into the destination, such as selected Case, report ID, metrics, filters, or failure reason.
6. When multiple prototype screenshots belong to the same product, consolidate them into one multi-page HTML prototype instead of separate isolated files.
7. Deliver editable static files and a concise interaction map.
8. When the user gives feedback, classify it and update only the affected files/screens.

## Preview And Image Rules

- If the user explicitly asks to see a generated visual preview before HTML, use the `imagegen` skill for a bitmap preview, then wait for alignment before implementing HTML.
- If the user provides an existing prototype image, rebuild the layout as HTML components. Do not use the image as a full-page background except as a temporary visual reference.
- Do not copy proprietary brand assets, exact competitor UI, or protected wording from external references.
- Treat generated or uploaded images as direction for structure, density, and flow; final text, states, and interactions must live in editable HTML/CSS/JS.
- If images are numbered or clearly sequential, preserve that order in the prototype route structure and build the first page before expanding the rest.

## Artifact Layout

For project-scoped work, write under the active project's prototype HTML directory:

```text
prototype/html/
  index.html
  standalone.html
  styles.css
  app.js
  prototype_manifest.json
  prototype_notes.md
  README.md
  open-mac.command
  open-windows.bat
  assets/
prototype/{prototype-name}.zip
```

For standalone work outside a project package, write under:

```text
prototype/
  index.html
  standalone.html
  styles.css
  app.js
  prototype_manifest.json
  prototype_notes.md
  README.md
  open-mac.command
  open-windows.bat
  assets/
```

Use `assets/html-prototype-template/` from this skill as a starting point when the repository has no stronger local prototype pattern.

Use `scripts/package_html_prototype.py` before every delivery to regenerate `standalone.html`, create the zip package, and check for non-portable paths.

## Cross-Platform Delivery

HTML prototype folders must work on both macOS and Windows:

- Use relative paths for all CSS, JS, images, fonts, and data files.
- Do not write OS-specific absolute paths or local file URLs inside generated prototype files.
- Keep the static entry as `index.html`; users should be able to open it directly without a dev server.
- Also produce `standalone.html` with CSS and JS inlined for one-file download or chat transfer.
- Produce a `.zip` package containing the whole prototype folder as the default handoff artifact.
- Include `open-mac.command` and `open-windows.bat` for handoff-friendly opening when useful.
- Include a short `README.md` that tells users to copy the whole prototype folder.
- Explain clearly: send the zip package by default; use `standalone.html` only when a one-file fallback is needed.
- Do not depend on shell commands, package managers, CDNs, or OS-specific browser features for core behavior.
- In final responses, local clickable links may be absolute for the current Codex app, but artifact files and instructions inside the prototype must remain portable.

## Multi-Page Prototype Defaults

For multi-screen product prototypes:

- Keep all related screens in one prototype application unless the user asks for separate files.
- Use shared shell elements such as sidebar, topbar, user menu, and common buttons across pages.
- Map left-navigation items and page CTAs to real screens whenever a referenced screen exists.
- New pages must update `index.html`, `app.js`, `styles.css`, `prototype_manifest.json`, `prototype_notes.md`, `standalone.html`, and the zip package together.
- Use the package script after any HTML/CSS/JS change so `standalone.html` and the zip cannot drift from the editable source files.
- Treat visual fidelity as iterative: first make each page navigable and structurally faithful, then refine spacing, density, text, and visual details from user feedback.

## Implementation Standards

- Prefer plain HTML, CSS, and JavaScript. Do not add a build system or frontend framework unless the current project already requires one.
- Use semantic structure and stable hooks:
  - `data-screen` for screens.
  - `data-nav-target` for page navigation.
  - `data-action` for modal, drawer, tab, filter, and state actions.
  - `data-inline-editable` or equivalent hooks for PM-editable text.
  - clear IDs for important PM-reviewable regions.
- Keep layout editable: separate structure in HTML, visual rules in CSS, and interactions in JS.
- Use realistic PM-level copy and data, but keep sample data clearly replaceable.
- Include normal, empty, loading, error, success, and permission states when they affect the flow.
- For mobile prototypes, keep tap targets usable and fixed-format UI such as bottom tabs, cards, and step indicators stable across states.
- For desktop prototypes, prioritize scanability and working density over marketing-style hero layouts.
- Avoid high-fidelity visual polish, ornamental backgrounds, complex animations, and designer-owned decisions unless the user asks for them.
- Do not hide product meaning inside images; core text, controls, and states must be selectable/editable HTML.

## Interaction Standards

Implement the expected PM prototype interactions directly in `app.js`:

- screen navigation and back paths.
- major task-entry navigation with context transfer. For example, clicking `Create Prompt` from an evaluation report should open a Prompt creation screen prefilled with the report and selected Case context, not just show a placeholder modal.
- tab/segment switching.
- modal and drawer open/close.
- form field entry and basic validation feedback.
- button state changes such as selected, disabled, loading, success.
- list filtering or search when needed to express the product flow.
- toast or inline feedback for user actions.
- double-click text editing for non-control copy, with Enter to save, Escape to cancel, and local persistence when useful.

Keep interactions deterministic and simple. The prototype should demonstrate behavior, not implement production data logic.

## Route And Context Transfer Rules

For PM prototypes, navigation quality is part of the product expression:

- If a button implies a real workflow, create the destination screen or workflow panel.
- Keep generic modals for confirmations, lightweight messages, or irreversible-action review only.
- Destination screens should show what data came from the previous screen.
- Add obvious return paths, such as breadcrumbs, back buttons, or side navigation state.
- Record each route in `prototype_manifest.json` with trigger, source, target, and transferred context.
- Typical context transfer:
  - Evaluation report -> Create Prompt: report ID, selected Case, failure reason, suggested optimization direction.
  - Case detail -> Optimize: Case input/output, expected answer, risk level, failed rule.
  - Report -> Compare: current version, baseline version, changed metrics.
  - Report -> New Dataset: current filters, selected cases, source run.

## Modification Protocol

When revising an existing HTML prototype:

1. Parse feedback into one or more classes:
   - `copy`: labels, headings, button text, placeholder text.
   - `page_structure`: modules, layout, navigation, screen hierarchy.
   - `interaction`: clicks, transitions, modals, tabs, form behavior.
   - `state`: empty, error, loading, success, permission, selected states.
   - `visual_style`: density, color, typography weight, spacing, fidelity.
   - `business_logic`: product rules that may require updating the product flow.
2. Update only the affected screen/component unless the requested change is global.
3. Keep `prototype_manifest.json` synchronized with screen and interaction changes.
4. Keep `prototype_notes.md` synchronized with assumptions, review questions, and changed behavior.
5. If feedback changes business logic, update or flag the corresponding product flow artifact before treating the prototype as final.

## Validation

Before reporting the prototype as ready:

1. Check that all referenced local files exist.
2. Check that navigation targets in HTML match screens handled by JS.
3. Run the package script:

```bash
python3 plugins/prd-prototype-suite/skills/interactive-html-prototype-builder/scripts/package_html_prototype.py path/to/prototype/html --zip-name prototype-name.zip
```

4. Open or smoke-test the prototype when tooling is available. For static prototypes, no dev server is required; provide the HTML path.
5. Verify basic visual quality:
   - primary text is not clipped.
   - buttons and tabs do not shift layout when active.
   - modal/drawer overlays can be closed.
   - mobile and desktop surfaces fit the intended viewport.
   - no core interaction is a dead click.
6. State any unverified areas clearly in the final response.

## Output Contract

Read [references/output-contract.md](references/output-contract.md) when writing formal prototype notes or manifest summaries. Always include:

- `prototype_type`
- `input_mode`
- `screen_inventory`
- `interaction_inventory`
- `route_context_transfer`
- `editable_files`
- `platform_compatibility`
- `feedback_application_log`
- `validation_checklist`
- `open_review_questions`

## Guardrails

- Do not produce final UI design; stay at product-prototype fidelity.
- Do not use a screenshot as the final interactive surface.
- Do not rewrite unrelated screens during feedback revisions.
- Do not let visual styling override confirmed product requirements.
- Do not invent hidden business rules to make interactions look complete.
- Do not depend on external CDNs or network assets for core prototype behavior.
