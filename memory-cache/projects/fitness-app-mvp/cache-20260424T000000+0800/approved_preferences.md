# Approved Preferences

Project: `fitness-app-mvp`
Cache: `cache-20260424T000000+0800`

Approved preferences are binding for this project only. They must not leak into other projects.

## PREF-FITNESS-20260424-001: China Market Default

- category: market_and_competitor
- source_trace_id: TRACE-FITNESS-20260424-001
- status: approved
- preference: If no market is specified, competitor and market analysis for this project defaults to China market.
- affected_skills: source-collector, competitor-gap-analyzer, scenario-roi-ranker, mvp-scope-decider
- use_rule: Prioritize China-market competitors, channels, Android distribution, and local user behavior signals.

## PREF-FITNESS-20260424-002: Preview-First Prototype Workflow

- category: workflow_and_approval
- source_trace_id: TRACE-FITNESS-20260424-002
- status: approved
- preference: Prototype work must start with a preview and wait for user feedback before full-flow prototypes.
- affected_skills: product-flow-mapper, low-fi-prototype-designer, prd-quality-reviewer
- use_rule: Do not create `full_prototype` unless `prototype_preview` is approved.

## PREF-FITNESS-20260424-003: Prototype Style Direction

- category: prototype_style
- source_trace_id: TRACE-FITNESS-20260424-003
- status: approved
- preference: Current prototype style should be dark mechanical, minimal, with cyan-green highlights, metal gradient feel, and readable text.
- affected_skills: prototype-reference-analyzer, low-fi-prototype-designer
- use_rule: Apply to prototype previews for this project unless the user gives a newer style direction.

## PREF-FITNESS-20260424-004: Prototype Feedback Format

- category: review_workflow
- source_trace_id: TRACE-FITNESS-20260424-004
- status: approved
- preference: User feedback may be given by page, problem, and modification. Apply it precisely to the preview and keep product flow docs synchronized.
- affected_skills: product-flow-mapper, low-fi-prototype-designer, prd-draft-writer, prd-quality-reviewer
- use_rule: Classify each feedback item as business logic, page structure, copy, visual style, or exception-state change before editing.

## PREF-FITNESS-20260425-001: Prototype Preview Must Be Directly Viewable

- category: prototype_delivery
- source_trace_id: TRACE-FITNESS-20260425-001
- status: approved
- preference: Prototype previews should include a directly viewable PNG or HTML fallback, not only a Markdown image link.
- affected_skills: low-fi-prototype-designer, prd-quality-reviewer
- use_rule: After generating a prototype, provide the PNG/HTML review artifact and a fallback file path if inline preview fails.

## PREF-FITNESS-20260425-002: Prototype Visual QA Required

- category: prototype_quality
- source_trace_id: TRACE-FITNESS-20260425-002
- status: approved
- preference: Prototype previews need basic visual QA for text overlap, centering, clipping, readable size, and contrast before reporting completion.
- affected_skills: low-fi-prototype-designer, prd-quality-reviewer
- use_rule: Check visible layout issues before final response, especially after user reports overlap or alignment problems.

## PREF-FITNESS-20260425-003: Plan-First Training Execution

- category: product_behavior
- source_trace_id: TRACE-FITNESS-20260425-003
- status: approved
- preference: The group rest timer should center on executing predefined training plans, not only ad-hoc rest timing.
- affected_skills: product-flow-mapper, low-fi-prototype-designer, mvp-scope-decider, prd-draft-writer
- use_rule: Default the core path to choosing a training plan, executing planned sets, using planned rest intervals, and progressing through next set or next exercise.

## PREF-FITNESS-20260425-004: Plan Summary Improves Time Estimation

- category: product_behavior
- source_trace_id: TRACE-FITNESS-20260425-004
- status: approved
- preference: Keep the training plan summary because it helps users estimate workout time and improves experience.
- affected_skills: product-flow-mapper, low-fi-prototype-designer, prd-draft-writer
- use_rule: Show summary fields such as action count, set count, estimated duration, and default rest interval when starting a plan.

## PREF-FITNESS-20260425-005: Edit Plan During Execution

- category: product_behavior
- source_trace_id: TRACE-FITNESS-20260425-005
- status: approved
- preference: During action execution, use "改计划" instead of "改重量"; it should support modifying reps/counts and weight, and record those changes.
- affected_skills: product-flow-mapper, low-fi-prototype-designer, prd-draft-writer, tracking-plan-designer
- use_rule: The action execution screen should expose plan adjustment as an explicit secondary action and persist changed weight/reps.

## PREF-FITNESS-20260425-006: Manual Start Next Set

- category: product_behavior
- source_trace_id: TRACE-FITNESS-20260425-006
- status: approved
- preference: After a rest timer ends, users should click "开始下一组" manually instead of auto-advancing, because users may have their own pacing and arrangements.
- affected_skills: product-flow-mapper, low-fi-prototype-designer, prd-draft-writer
- use_rule: Keep manual confirmation between rest completion and the next set; after the user completes a set, they click group rest to start resting.
