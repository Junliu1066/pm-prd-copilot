# Accepted Lessons

## LESSON-20260423-001: Enumerate user universe before narrowing

- lesson_type: general_pm_principle
- principle: Do not narrow the target user too early. First enumerate all plausible target-user groups, then analyze pain points, needs, and scenarios.
- affected_components: user-universe-mapper, pain-needs-analyzer, scenario-roi-ranker, prd-quality-reviewer
- expected_behavior: Product analysis should start from a broad user universe and only narrow after evidence and scenario reasoning.
- verification_hint: PRD or analysis output should include multiple candidate user groups before selecting the target group.

## LESSON-20260423-002: Rank scenarios by minimum cost and maximum return

- lesson_type: general_pm_principle
- principle: Core scenarios should be selected by minimum implementation cost, maximum user/business return, time saved, and speed to MVP.
- affected_components: scenario-roi-ranker, mvp-scope-decider, prd-quality-reviewer
- expected_behavior: Scenario ranking should explain value, cost, frequency, time saving, and MVP speed rather than only importance.
- verification_hint: Scenario ranking output should include explicit ROI reasoning.

## LESSON-20260423-003: Competitor analysis should find advantage, not list features

- lesson_type: general_pm_principle
- principle: Competitor analysis should explain how competitors solve the problem, where they are weak, what advantage we can create, and how to amplify it.
- affected_components: competitor-gap-analyzer, scenario-roi-ranker, mvp-scope-decider, prd-draft-writer
- expected_behavior: Competitor output should include competitor approach, gap, opportunity, advantage, and amplification strategy.
- verification_hint: Competitor output should not be a plain feature table only.

## LESSON-20260424-004: Prototype feedback must update both artifact and product logic

- lesson_type: skill_improvement
- principle: Prototype feedback must be classified by layer before editing. Business-logic feedback updates both product flow and prototype; visual-only feedback updates only the visual artifact.
- affected_components: prototype-reference-analyzer, product-flow-mapper, low-fi-prototype-designer, prd-quality-reviewer
- expected_behavior: Prototype iteration should keep visual artifacts, product flows, page descriptions, and PRD text consistent while preserving the preview approval gate.
- verification_hint: When a prototype adds a new business module, the product flow artifact should also change; when feedback only changes style, product behavior should remain unchanged.

## LESSON-20260424-005: Project preferences need isolated versioned caches

- lesson_type: workflow_rule
- principle: Project preference memory must be project-scoped, versioned, resettable, clearable, traceable, and governed by human approval.
- affected_components: project-preference-cache-manager, workflow, harness, agent
- expected_behavior: Skills read only approved preferences from the current project's active cache and must stop reading preferences when the cache is cleared.
- verification_hint: A preference cache must have a project-local active pointer, source trace, candidate/approved separation, and no cross-project references.

## LESSON-20260425-001: Prototype delivery must be visible and visually QA'd

- lesson_type: skill_improvement
- principle: Prototype previews must include a directly viewable delivery artifact and a visual QA pass before completion is reported.
- affected_components: low-fi-prototype-designer, prd-quality-reviewer
- expected_behavior: Prototype output includes PNG or HTML fallback, editable source, synchronized Markdown, and checks for overlap, centering, clipping, readable text, contrast, and source/preview consistency.
- verification_hint: If a user cannot see the image, the next iteration should fix delivery before continuing design; if a user finds alignment/overlap issues, the skill should update visual QA guidance.

## LESSON-20260425-002: Skill improvements must generalize from project cases

- lesson_type: skill_improvement
- principle: Project cases are training examples for reusable skills, not domain-specific templates. Convert concrete project feedback into abstract, cross-product rules before changing a generic skill.
- affected_components: product-flow-mapper, low-fi-prototype-designer, project-preference-cache-manager, skill-generalization-auditor, prd-quality-reviewer
- expected_behavior: Project-specific labels, styles, modules, and scenarios stay in the project preference cache; only industry-neutral methods become reusable skill behavior.
- verification_hint: A generic skill update should avoid the original project's domain nouns unless used only as a clearly labeled example.

## LESSON-20260425-003: PRDs need governed delivery planning

- lesson_type: workflow_rule
- principle: A PRD intended for development should include a technical delivery path with phased scope, implementation modules, effort assumptions, phase effects, risks, and final target.
- affected_components: workflow, harness, technical-scope-planner, release-roadmap-planner, effort-estimator, delivery-effect-definer, delivery-quality-reviewer, prd-draft-writer
- expected_behavior: Delivery planning is handled by a detachable plugin and cannot mutate product scope; product ambiguity must route back as PM questions.
- verification_hint: When a project requests delivery planning, harness should require technical scope, release roadmap, effort estimate, delivery plan, and delivery quality report.

## LESSON-20260425-004: AI-heavy PRDs need governed AI solution planning

- lesson_type: workflow_rule
- principle: PRDs that rely on AI should separate AI capability mapping, model selection, Prompt design, RAG, memory, learner/profile modeling, adaptive coaching, AI technical architecture, and AI readiness review.
- affected_components: workflow, harness, ai-capability-mapper, model-selection-planner, prompt-architecture-designer, rag-architecture-planner, conversation-memory-planner, learner-profile-modeler, adaptive-coaching-planner, ai-technical-architecture-planner, ai-solution-reviewer
- expected_behavior: AI planning stays detachable, uses official-doc verification and benchmarks before final model choices, and treats external AI information as signals requiring human verification.
- verification_hint: When a project requests AI planning, harness should require the full AI solution artifact set and block missing review status or benchmark policy.

## LESSON-20260425-005: Delivery plans can become supervised Codex task packages

- lesson_type: workflow_rule
- principle: Development planning should be able to produce Codex-ready task packages with department ownership, write boundaries, validation commands, human confirmation points, minimal-fix strategy, and a feedback learning loop.
- affected_components: workflow, harness, agentic-delivery-orchestrator, technical-scope-planner, release-roadmap-planner, effort-estimator, delivery-effect-definer, delivery-quality-reviewer
- expected_behavior: Semi-automated development remains human-supervised and cannot mutate PRD scope, database schema, model choices, external API use, GitHub push, destructive data operations, or Skill updates without approval.
- verification_hint: Agentic delivery harness should fail task packages that lack allowed/forbidden write paths, validation commands, supervision gates, or development governance status.

## LESSON-20260425-006: Model selection must compare real market models

- lesson_type: skill_improvement
- principle: Model selection is not only a framework. It must collect current official model information, compare concrete market models, define benchmark cases, and recommend several model choices for the product.
- affected_components: model-selection-planner, ai-solution-reviewer, harness
- expected_behavior: Model selection output includes market scope, official source snapshot, candidate model pool, comparison matrix, benchmark status, shortlist recommendations, routing rules, and fallback strategy.
- verification_hint: If no real API benchmark was run, the output must label recommendations as document-screening shortlists and require human verification instead of claiming measured quality.

## LESSON-20260425-007: Semi-automated development must include the operating-system layer

- lesson_type: workflow_rule
- principle: Semi-automated development should not only generate product-code tasks. It must also plan capability enablement, Skill reuse or creation, MCP routing, steward governance, harness checks, random audit, efficiency audit, teaching absorption, preference memory, and supervised Skill updates.
- affected_components: agentic-delivery-orchestrator, capability-enablement-planner, skill-mcp-routing-planner, development-governance-orchestrator, codex-task-package-writer, harness, workflow
- expected_behavior: Agentic delivery output includes capability enablement, Skill/MCP routing, governance operating system, Codex task package blueprint, human supervision gates, and learning routes before product-code tasks start.
- verification_hint: Agentic delivery harness should fail if semi-automated development lacks Skill/MCP routing, capability enablement, governance operating-system plan, or Codex task package blueprint.

## LESSON-20260425-008: Codex-ready development schemes belong in the development document output

- lesson_type: workflow_rule
- principle: When the user asks to add the semi-automated development scheme, write it into the formal "把 PRD 转成可交给 Codex 半自动开发" development document output section, not only into a development log or retrospective note.
- affected_components: codex-task-package-writer, agentic-delivery-orchestrator, harness
- expected_behavior: The Codex task package blueprint includes a `development_document_output` section with required sections, output artifacts, supervision gates, validation, learning, and overload escalation.
- verification_hint: Agentic delivery harness should fail if the Codex task package blueprint lacks `development_document_output`.

## LESSON-20260425-009: Development-ready outputs need paired Codex development documents

- lesson_type: workflow_rule
- principle: Development-ready PRD outputs, Codex development planning requests, and semi-automated delivery packages should include a companion `codex_development_document` that turns the approved PRD scope into a Codex-ready development plan.
- affected_components: workflow, codex-task-package-writer, agentic-delivery-orchestrator, harness
- expected_behavior: When the user requests development-ready output, Codex development planning, or semi-automated delivery, the delivery planning stage should produce a paired Codex development document with structure, development flow, technical path, AI plan when needed, Codex task packages, supervision gates, validation, learning, and overload escalation.
- verification_hint: Workflow and agentic delivery harness should require `codex_development_document` when agentic delivery, Codex development planning, or development-ready PRD packaging is requested; lightweight PRDs or non-development product notes should not be forced to include it.

## LESSON-20260427-001: HTML prototypes need portable, editable delivery

- lesson_type: skill_improvement
- principle: Interactive HTML prototypes should be delivered as portable zip packages with relative paths, separated `index.html`/`styles.css`/`app.js` for editability, and a `standalone.html` fallback for one-file sharing.
- affected_components: interactive-html-prototype-builder
- expected_behavior: Generated prototypes work on Windows and macOS after unzip, require no local server, include a README, and avoid OS-specific absolute paths inside artifact files.
- verification_hint: The zip should contain the whole prototype folder; `index.html` should reference local relative CSS/JS; `standalone.html` should inline CSS/JS.

## LESSON-20260427-002: PM prototypes should support in-place copy edits

- lesson_type: skill_improvement
- principle: Product-manager-facing HTML prototypes should support lightweight in-place text editing for review and iteration, without requiring users to edit source code.
- affected_components: interactive-html-prototype-builder
- expected_behavior: Users can double-click ordinary text to edit it, press Enter or blur to save, press Escape to cancel, and reset local edits when needed.
- verification_hint: A generated prototype should include editable text behavior for non-control copy and document whether edits are stored locally or persisted elsewhere.

## LESSON-20260427-003: Critical prototype actions need real routes with context

- lesson_type: skill_improvement
- principle: Buttons that represent real product workflows should navigate to destination screens or workflow panels and carry source context, instead of only opening placeholder modals.
- affected_components: interactive-html-prototype-builder, product-flow-mapper, low-fi-prototype-designer
- expected_behavior: Create, edit, review, optimize, compare, publish, detail, and dataset actions should have real target screens when they are in scope; target screens should display transferred context such as selected item, report ID, failed case, filters, version, or metrics.
- verification_hint: `prototype_manifest.json` should include route/context transfer records for major workflow actions.

## LESSON-20260427-004: Sequential screenshots should become one multi-page prototype

- lesson_type: skill_improvement
- principle: When a user provides multiple ordered prototype screenshots for one product, rebuild them as one cohesive multi-page HTML prototype with shared navigation, not as disconnected static pages.
- affected_components: interactive-html-prototype-builder, prototype-reference-analyzer
- expected_behavior: The prototype preserves screenshot order, maps sidebar and CTA routes to corresponding pages, keeps common shell elements consistent, and updates manifest, notes, standalone file, and zip package together.
- verification_hint: The delivered prototype should allow navigation across all referenced screens and list all screens in `screen_inventory`.

## LESSON-20260428-001: PRDs need a visual reading layer

- lesson_type: output_preference
- principle: Future software/product development PRDs should include a project-fit visual reading layer in the PRD body, not only text or attachments.
- affected_components: prd-draft-writer, prd-quality-reviewer, prd-template, prd-schema
- expected_behavior: Each development-oriented PRD includes page descriptions, page jump relationships, and a prototype layer as the baseline. Additional diagrams such as product overview mind map, swimlane, MVP scope map, risk-control loop, status flow, permission matrix, or user story map should be selected by project necessity and placed in their corresponding sections rather than forced into a centralized visual block.
- verification_hint: A generated PRD should make scope, flow, pages, MVP boundary, risks, and prototype direction reviewable in the relevant sections; it should not force the same five diagrams into every project when they do not fit.

## LESSON-20260428-002: Prototype work needs a supervised HTML handoff flow

- lesson_type: output_preference
- principle: Prototype work should follow a supervised chain from PRD and product flow to preview, approval, full prototype, optional HTML conversion, package, QA, and final human approval.
- affected_components: prototype-reference-analyzer, product-flow-mapper, low-fi-prototype-designer, interactive-html-prototype-builder, prd-quality-reviewer
- expected_behavior: Future prototype work follows `PRD / requirements -> product flow / page IA -> low-fi prototype preview -> human review -> full wireframe/prototype -> interactive HTML conversion when useful -> standalone.html + zip package -> visual/interaction/navigation QA -> human approval -> UI design or Codex development document`.
- verification_hint: A prototype delivery should show the current stage, whether preview approval exists, whether feedback was classified, whether product flow/PRD changed when behavior changed, and whether HTML package QA passed before handoff.

## LESSON-20260428-003: User-led development is not personal-only usage

- lesson_type: output_preference
- principle: Do not interpret “我自己开发” or “自己开发” as meaning the product is only for personal use. It means the user will lead or implement development; the product audience still needs to be inferred from context or confirmed.
- affected_components: requirement-intake, prd-draft-writer, development-document-policy, agentic-delivery-orchestrator
- expected_behavior: When the user says they will develop the product themselves, outputs should preserve the intended market or user audience unless the user explicitly says it is personal-only or internal-only.
- verification_hint: Generated PRDs and development documents should distinguish `development owner` from `target users`; they should not downgrade platform, team, or external-user scope into a personal tool without evidence.

## LESSON-20260428-004: Approved user frameworks can be productized

- lesson_type: workflow_rule
- principle: When the user explicitly approves exposing their own framework, do not hide it as implementation. Frameworks such as multi-manager/steward systems, Skill/MCP routing, harness, audits, and learning loops may become visible product architecture and internal development governance.
- affected_components: prd-draft-writer, codex-task-package-writer, agentic-delivery-orchestrator, development-governance-orchestrator
- expected_behavior: Documents should show the framework at the appropriate audience layer: product-facing capability in PRD when it is a differentiator, engineering architecture in development docs, and task/governance rules in Codex internal docs.
- verification_hint: If the user says a framework can be “融入” or “不需要藏着”, outputs should include it explicitly instead of replacing it with generic labels or hiding all named governance mechanisms.

## LESSON-20260428-005: Development documents need audience separation

- lesson_type: workflow_rule
- principle: PRD, engineering development document, and Codex internal development document are separate artifacts with different audiences and responsibilities.
- affected_components: prd-draft-writer, technical-scope-planner, codex-task-package-writer, agentic-delivery-orchestrator, delivery-quality-reviewer
- expected_behavior: PRDs describe product value, users, flows, scope, acceptance, and constraints. Development documents describe implementation architecture, modules, APIs, data, and deployment. Codex internal documents describe agent execution, task packages, allowed/forbidden write paths, validation commands, human gates, and minimal-fix strategies.
- verification_hint: A delivery package for development should not mix these layers into one ambiguous file; each artifact should link to the others and state its audience.

## LESSON-20260428-006: Development-ready packages need audience-appropriate execution assets

- lesson_type: output_preference
- principle: When asked to package everything needed for development, include execution-relevant assets according to audience, redaction, and distribution policy, not only the newest PRD and development document.
- affected_components: delivery-quality-reviewer, codex-task-package-writer, interactive-html-prototype-builder, workflow
- expected_behavior: A complete internal package should include PRD, engineering development docs, Codex internal docs when available, flows, wireframes, AI/model notes, prototype, source materials, screenshots or visual references, package manifest, and an English-path compatibility zip when filename encoding may be an issue. External or protected packages must separate internal governance notes, private source material, and project-only memory according to redaction and distribution policy.
- verification_hint: Zip inspection should show the expected audience-appropriate docs, prototype, source-assets, screenshots/reference assets, and manifest directories or equivalents, and should not expose internal-only governance or private materials in external packages.

## LESSON-20260428-007: No-write instructions override learning actions

- lesson_type: workflow_rule
- principle: When the user says “先别改动” or equivalent, the assistant should report analysis or recommendations only and must not update files, memory, skills, proposals, packages, or project artifacts.
- affected_components: workflow, learning-steward, project-preference-cache-manager, skill-update-proposer, agent
- expected_behavior: Even if useful long-term preferences are identified, they should be reported for approval first. Writing happens only after the user explicitly approves.
- verification_hint: A turn containing “先别改动” should produce no filesystem diff unless the user later gives explicit approval.

## LESSON-20260428-008: Long-term changes need concrete recommendation plans

- lesson_type: workflow_rule
- principle: Before writing any long-term rule or stable governance change, provide a concrete recommendation plan rather than a loose note.
- affected_components: workflow, learning-steward, project-preference-cache-manager, skill-update-proposer, agent
- expected_behavior: Recommendation plans should include problem background, recommended plan, advantages, disadvantages and risks, alternatives, recommendation conclusion, execution scope, validation method, and approval points. The change is written only after explicit user approval and only within the approved scope.
- verification_hint: Any turn that proposes changing stable preferences, Skill behavior, harness checks, workflow rules, steward rules, plugin rules, automation rules, or persistent project rules should show a concrete recommendation plan before file edits.
