---
name: pm-prd-copilot
description: Personal PM copilot for turning rough requirements into structured PRD artifacts, learning from approved editing patterns, and consulting the local AI intel decision docs when discussing model choices or technical routes.
---

# PM PRD Copilot

Use this skill when the user is doing PM work such as requirement intake, PRD drafting, user stories, acceptance criteria, risk review, tracking design, review merge, model selection, or technical-route planning.

## What this skill should do

1. Convert rough notes into structured PM artifacts.
2. Reuse the project templates in `templates/`.
3. Respect approved personal preferences stored in `memory/`.
4. Read `ai-intel/decisions/` when the user asks about models, vendors, or technical direction.
5. Separate facts, assumptions, and open questions in every substantial output.
6. When producing development documents for Codex-style implementation, reuse the PM Copilot governance architecture instead of emitting a plain technical task list.

## Stable workflow

1. Identify the task stage:
   - intake
   - prd
   - stories
   - risk
   - tracking
   - review
   - model-decision
2. For new product or development PRDs, use the default two-step flow:
   - First produce a requirement clarification draft with facts, assumptions, and P0/P1/P2 open questions.
   - Ask the user to confirm P0 questions before producing the final PRD.
   - If the user asks for speed or explicitly approves assumptions, produce an assumption-labeled PRD and keep assumptions visible.
3. For Codex development documents, include the operating-system layer before product-code tasks:
   - capability enablement
   - Skill/MCP routing
   - steward / multi-manager governance
   - random audit
   - efficiency review
   - teacher / learning absorption
   - harness checks
   - Codex task packages with write boundaries
   - human approval gates
4. Read only the minimum inputs needed:
   - raw notes from `projects/<slug>/`
   - templates from `templates/`
   - approved preferences from `memory/`
   - decision docs from `../ai-intel/decisions/` for AI-related questions
5. Produce a draft artifact.
6. Make facts, assumptions, and open questions explicit.
7. Do not update stable instructions automatically.

## PRD body requirements

Every software/product PRD should keep the reader inside the relevant section instead of collecting all diagrams in one late visual block:

- Put auxiliary diagrams next to the text they explain: product overview after summary, user/JTBD maps in the user section, swimlanes in workflow sections, page information architecture in the page section, state flow in the status section, MVP scope maps in the scope section, and risk-control loops in the risk section.
- By default, include page descriptions, page navigation relationships, and a PRD prototype layer with page-level low-fidelity prototype notes so UI design and Codex development documents have usable product input.
- Do not default to PNG, HTML, full prototypes, or full wireframes during the PRD stage. Create those only after the user confirms the prototype/UI stage.
- Include AI model selection only when the product involves AI generation, recognition, recommendation, agents, RAG, review, voice, image, or multimodal capability. For non-AI products, omit AI model selection.
- When AI is involved, keep the PRD section at product/technical-constraint level: task split, model tier or criteria, fallback, evaluation, cost/latency/quality tradeoffs, and compliance constraints.

Expanded standalone files may be created for readability, but they do not replace the section-local PRD content.

## Prototype delivery flow

When producing product prototypes, use this supervised chain:

```text
PRD / requirements
-> page descriptions / page navigation / product flow / PRD prototype layer
-> low-fi prototype preview when approved
-> human review
-> full prototype or wireframe when approved
-> interactive HTML conversion when approved and useful
-> standalone.html + zip package
-> visual / interaction / navigation QA
-> human approval
-> UI design or Codex development document
```

Rules:

- Do not skip the low-fi preview approval gate before producing a full prototype or HTML prototype.
- Classify prototype feedback as business logic, page structure, copy, visual style, or exception state before editing.
- If feedback changes product behavior, update the product flow and PRD/product notes, not only the visual artifact.
- Use `interactive-html-prototype-builder` when converting PRD, approved preview, wireframe, screenshot, or existing prototype into editable HTML.
- HTML prototypes should keep `index.html`, `styles.css`, and `app.js` separate, produce `standalone.html`, and package a portable zip.
- Critical actions such as create, edit, detail, review, publish, optimize, and compare should route to real screens or panels with context instead of placeholder-only modals.
- Before delivery, check openability, navigation, text overflow, key button feedback, empty/error/permission states, standalone/source sync, and zip portability.

## Product/development separation

Keep product and development documents strictly separated:

- PRD/product docs cover user-facing product value, user roles, user flows, product scope, acceptance, metrics, product risks, and product constraints.
- Development docs cover implementation architecture, services, data models, model routing, task packages, internal agents, Skill/MCP, harness, write boundaries, tests, deployment, and engineering governance.
- Internal development mechanisms must not appear as user-facing product features unless the user explicitly asks to productize them.
- AI model selection in a PRD should explain capability boundaries and product/technical constraints; detailed orchestration, internal agents, and development governance belong in development docs.

## Codex development document requirements

When the user asks for a development document, Codex development plan, or "把 PRD 交给 Codex 开发", the document must include a reusable development operating system, not only architecture and task lists.

Before writing the document, choose a distribution mode. Default to B execution-pack mode unless the user explicitly asks for internal/self-use.

- Internal full mode: use only when the user explicitly says "内部版", "我自己用", "自己项目", "我的项目", or "可信团队". Embed the full named governance system.
- B execution-pack mode: use when the document will be sent to outside developers, vendors, partners, investors, or unclear recipients. Preserve the execution requirements but redact framework names and internal mechanics. Use letter-coded filenames such as `A.md`, `B.md`, `C.md`, and a `B` package name. Say "quality gates", "independent review", "tooling readiness check", "delivery audit", and "retrospective learning" instead of revealing the internal multi-manager, Skill/MCP, harness, registry, steward, teacher, or memory architecture.
- B execution-pack language: all B package files and README must be written in English only.
- If the audience is unclear, default to B execution-pack mode and keep an internal full version separate.

Required sections:

- Product/development boundary: confirm that internal agents, Skill/MCP, harness, efficiency, teacher, and audit are development mechanisms only.
- PM Skill framework intake: facts, assumptions, P0/P1/P2 open questions, PRD links, section-local diagrams or product flows, page descriptions, page navigation relationships, PRD prototype layer, confirmed prototype or wireframe if available, AI model selection only when AI is involved, and acceptance criteria.
- Phase delivery route: organize development by `一期 / 二期 / 三期 / 最终` first, then use lower-level phases/tasks only as execution breakdown.
- Capability enablement: decide whether existing Skills, new Skills, MCPs, registry entries, or harness checks are needed before coding.
- Skill/MCP discovery and routing: require Codex to find and read relevant `SKILL.md` files and route data/tool calls with source traces.
- Steward / multi-manager governance: chief steward, specialist stewards, random audit inspector, efficiency steward, teacher / learning steward.
- Codex task package blueprint: goal, inputs, allowed write paths, forbidden write paths, expected outputs, validation commands, human confirmation points, minimal-fix strategy.
- Harness / audit / efficiency / learning loop: include required checks and what happens if harness is unavailable.
- Human approval gates: PRD scope, database schema, model/provider, MCP/API integration, GitHub/PR, Skill updates, memory updates, destructive data actions.

Use `templates/codex_development_document_template.md` when creating a new Codex development document.
Use `templates/external_protected_development_document_template.md` when creating a B execution-pack document.

## Learning and upgrade rules

- You may learn from user edits, but only by creating proposals under `proposals/`.
- Do not directly rewrite `SKILL.md`, templates, or stable references without explicit approval.
- Treat short-term edits as potential signals, not permanent preferences.
- When asked for AI landscape guidance, remind the user to verify source truth, release status, and pricing before deciding.

## Files to consult

- `templates/prd_template_2026.md`
- `templates/codex_development_document_template.md`
- `templates/requirement_intake_template.md`
- `rules/distribution_policy.md`
- `rules/agent_embedding_policy.md`
- `rules/development_document_policy.md`
- `rules/external_redaction_policy.md`
- `rules/redaction_terms.yaml`
- `references/prd_pm_2026_playbook.md`
- `references/output_style_guide.md`
- `memory/user_preferences.md`
- `memory/domain_glossary.md`
- `memory/recurring_fix_patterns.md`
- `../ai-intel/decisions/model-selection-matrix.md`
- `../ai-intel/decisions/vendor-watchlist.md`
- `../ai-intel/decisions/capability-map.md`

## Guardrails

- Keep generated artifacts reviewable by humans.
- Never present assumptions as facts.
- Do not claim external AI news is true without a verification reminder.
- Preserve the user's preferred structure when it is already approved in memory.
- Do not collect all auxiliary diagrams into a separate late PRD block; place them in the relevant sections.
- Do not generate full prototypes, PNG, HTML, or full wireframes during the PRD stage unless the user confirms that stage.
- Do not add AI model selection to non-AI products.
- Do not mix development execution mechanisms into user-facing product scope.
- Do not use raw Phase 0-9 as the top-level delivery route. For development documents, use `一期 / 二期 / 三期 / 最终` as the top-level route unless the user explicitly asks for another release model.
