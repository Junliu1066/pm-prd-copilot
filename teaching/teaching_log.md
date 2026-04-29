# Teaching Log

This log captures user coaching. The teacher role classifies each lesson and proposes how the system should absorb it. Lessons are not stable rules until accepted.

## 2026-04-28 - Long-term changes need concrete recommendation plans

### User Feedback
The user clarified that long-term rules should be presented as concrete recommendation plans before writing. The assistant should include advantages, disadvantages, recommendation, and execution details, then wait for explicit approval.

### Lesson Type
workflow_rule

### Proposed Rule
Before writing any long-term rule, stable preference, Skill behavior change, harness check, workflow rule, steward rule, plugin rule, automation rule, or other governance change, provide a concrete recommendation plan covering problem background, recommended plan, advantages, disadvantages and risks, alternatives, recommendation conclusion, execution scope, validation method, and approval points. Write the change only after explicit user approval.

### Affected Components
- workflow
- learning-steward
- project-preference-cache-manager
- skill-update-proposal
- agent

### Status
accepted

## 2026-04-23 - Do not narrow user groups too early

### User Feedback
Do not stop at the weight-loss user group. First consider all user groups that could become target users, then analyze their pain points and needs, then connect them to concrete scenarios.

### Lesson Type
general_pm_principle

### Proposed Rule
Before narrowing target users, `user-universe-mapper` must enumerate the broad potential user pool and explain why each group may or may not be prioritized.

### Affected Components
- user-universe-mapper
- pain-needs-analyzer
- scenario-roi-ranker
- prd-quality-reviewer

### Status
accepted

## 2026-04-24 - Default competitor analysis to China market unless specified

### User Feedback
For competitor analysis, the target market is China by default unless the user explicitly says otherwise.

### Lesson Type
user_preference

### Proposed Rule
`source-collector` should preserve the default market assumption, and `competitor-gap-analyzer` should collect China-market competitors and channels first unless the user names another market.

### Affected Components
- source-collector
- competitor-gap-analyzer

### Status
proposed

## 2026-04-24 - Prototype feedback must update visual artifacts and product logic consistently

### User Feedback
When prototype feedback changes page structure, business behavior, copy, or visual style, the prototype preview should be updated precisely and related product-flow documents should stay consistent.

### Lesson Type
skill_improvement

### Proposed Rule
Prototype feedback must be classified by layer before editing. Business-logic feedback updates both product flow and prototype; visual-only feedback updates only the visual artifact. Full-flow prototypes remain blocked until preview approval.

### Affected Components
- prototype-reference-analyzer
- product-flow-mapper
- low-fi-prototype-designer
- prd-quality-reviewer

### Status
accepted

## 2026-04-24 - Project preferences need isolated versioned caches

### User Feedback
When starting a new product project, create a separate preference cache. If the user asks to re-record preferences, create a new folder. If the user asks to clear memory, stop using the cache. Store this in the GitHub repository so it remains versioned and manageable.

### Lesson Type
workflow_rule

### Proposed Rule
Project preference memory must be project-scoped, versioned, resettable, clearable, traceable, and governed by human approval. Skills must read only the current project's approved preferences.

### Affected Components
- project-preference-cache-manager
- workflow
- harness
- agent

### Status
accepted

## 2026-04-25 - Prototype delivery must be visible and visually QA'd

### User Feedback
The generated prototype image was not visible to the user, and previous iterations had visual issues such as overlapping text and off-center text.

### Lesson Type
skill_improvement

### Proposed Rule
Prototype previews must include directly viewable delivery artifacts, such as PNG or HTML, not only Markdown links. Before reporting completion, run a visual QA pass for overlap, centering, clipping, text size, contrast, and source/PNG consistency.

### Affected Components
- low-fi-prototype-designer
- prd-quality-reviewer

### Status
accepted

## 2026-04-24 - Competitor scope must include direct and indirect influence

### User Feedback
Competitor analysis should not focus only on vertical products. Any product or workaround inside the user-provided industry track that directly or indirectly affects the product should be included.

### Lesson Type
general_pm_principle

### Proposed Rule
`competitor-gap-analyzer` should include direct competitors, adjacent alternatives, platform-native substitutes, content/community substitutes, manual workarounds, and offline/service substitutes when they influence the target user's decision, attention, time, or workflow.

### Affected Components
- competitor-gap-analyzer
- scenario-roi-ranker
- mvp-scope-decider

### Status
proposed

## 2026-04-24 - PRD analysis outputs should include reviewable diagrams

### User Feedback
User group judgment should include a first-section matrix for easier review, and plans should include flowcharts with icons. Skill and MCP roles should also be visually represented when relevant.

### Lesson Type
output_preference

### Proposed Rule
`user-universe-mapper` should produce a review matrix when user groups are broad. Summary outputs should include a flowchart for the analysis path and, when MCPs/skills are involved, a role-boundary diagram.

### Affected Components
- user-universe-mapper
- source-collector
- competitor-gap-analyzer
- scenario-roi-ranker
- mvp-scope-decider

### Status
proposed

## 2026-04-28 - PRDs need a visual reading layer

### User Feedback
After reviewing a PRD visual preview with a product overview mind map, core business swimlane, page information architecture, MVP scope map, and risk-control loop, the user approved making these required for future PRDs.

### Lesson Type
output_preference

### Proposed Rule
Future software/product development PRDs must include these five reviewable visuals in the PRD body. Expanded visual files may supplement the PRD, but they cannot replace the body sections.

### Affected Components
- prd-draft-writer
- prd-quality-reviewer
- pm-prd-copilot template
- PRD schema

### Status
accepted

## 2026-04-28 - Prototype work needs a supervised HTML handoff flow

### User Feedback
After reviewing the proposed prototype chain, the user approved adding it to long-term behavior.

### Lesson Type
output_preference

### Proposed Rule
Future prototype work should follow this supervised chain: PRD / requirements -> product flow / page IA -> low-fi prototype preview -> human review -> full wireframe/prototype -> interactive HTML conversion when useful -> standalone.html + zip package -> visual/interaction/navigation QA -> human approval -> UI design or Codex development document.

### Affected Components
- prototype-reference-analyzer
- product-flow-mapper
- low-fi-prototype-designer
- interactive-html-prototype-builder
- prd-quality-reviewer

### Status
accepted

## 2026-04-23 - Core scenario should be judged by minimum cost and maximum return

### User Feedback
The core scenario should be selected by judging which scenario has the minimum cost and maximum return. For the fitness app case, group interval timing is likely the core scenario.

### Lesson Type
general_pm_principle

### Proposed Rule
`scenario-roi-ranker` must rank scenarios by user value, usage frequency, implementation cost, time saved, and speed to MVP.

### Affected Components
- scenario-roi-ranker
- mvp-scope-decider
- prd-quality-reviewer

### Status
accepted

## 2026-04-23 - Competitor analysis must find advantage, not list features

### User Feedback
Do not just list competitors and features. Investigate how competitors solve the problem, what our advantage is, and how to expand that advantage.

### Lesson Type
general_pm_principle

### Proposed Rule
`competitor-gap-analyzer` must output competitor approach, user complaints or gaps, our possible advantage, and how to amplify that advantage.

### Affected Components
- competitor-gap-analyzer
- scenario-roi-ranker
- mvp-scope-decider
- prd-draft-writer

### Status
accepted
