# Output Style Guide

## General rules

- Prefer concise, working PM documents over long essays.
- Default to Chinese output unless the user asks for English.
- Always include `facts / assumptions / open_questions` for important decisions.
- Write acceptance criteria as testable statements.

## PRD conventions

- Keep the top summary short.
- Make scope and non-scope explicit.
- Put auxiliary diagrams in the relevant PRD section, not in a single late visual block: overview map after summary, JTBD/user maps in the user section, swimlanes in workflow sections, page information architecture in the page section, MVP maps in scope, and risk loops in risk.
- Default PRD output includes page descriptions, page navigation relationships, and a PRD prototype layer with page-level low-fidelity prototype notes for later UI design and Codex development documents.
- Do not default to PNG, HTML, full prototypes, or full wireframes during the PRD stage; create those only after the user confirms the prototype/UI stage.
- For AI-enabled products, include AI model selection in the PRD body with model routing, fallback, evaluation, cost/latency tradeoffs, and compliance constraints. For non-AI products, omit this section.
- Keep product and development strictly separated: PRD sections describe user-facing product behavior and product constraints; development mechanisms such as internal agents, Skill/MCP, harness, task packages, write boundaries, and engineering governance belong in development docs, not user-facing product scope.
- AI model selection in a PRD is a product/technical constraint section, not permission to expose multi-agent or development orchestration concepts to users.
- If P0 questions are unresolved, mark the PRD as assumption-labeled or stop at a clarification draft until the user confirms.
- Call out dependencies, risk, and rollout clearly.
- If evidence is weak, say so directly.

## Codex development document conventions

- A Codex development document is not a generic technical spec. It must explain how Codex should develop under supervision.
- Choose a distribution mode before writing. Default to B execution-pack mode. Use internal full mode only when the user explicitly says "内部版", "我自己用", "自己项目", "我的项目", or "可信团队".
- Always include the PM Skill framework handoff: facts, assumptions, P0/P1/P2 questions, PRD links, product flows or section-local diagrams, page descriptions, page navigation relationships, PRD prototype layer, confirmed prototype or wireframe if available, AI model selection only when AI is involved, user stories, and acceptance criteria.
- Always structure development delivery by `一期 / 二期 / 三期 / 最终` first; detailed Phase or task breakdowns can follow as execution detail.
- Always include the operating-system layer: capability enablement, Skill/MCP routing, multi-manager governance, random audit, efficiency review, teacher/learning absorption, harness checks, and human approval gates.
- Always include Codex task packages with allowed write paths, forbidden write paths, validation commands, minimal-fix strategy, and Skill/MCP Discovery results.
- Keep multi-manager, efficiency, teacher, Skill/MCP, harness, registry, and memory as development mechanisms only unless the user explicitly asks to productize them.
- For B execution-pack documents, use letter-coded filenames and package names. Do not expose internal framework names, role taxonomy, registry/steward/harness commands, memory routes, teacher mechanisms, or reusable templates. Translate them into neutral requirements such as "quality gate", "tool readiness check", "independent review", "delivery audit", "efficiency review", and "retrospective improvement".
- B execution-pack files must be English-only, including the package README and all letter-coded documents.
- If harness cannot run for a project, state that directly and provide the minimum substitute verification instead of claiming completion.

## AI decision conventions

- Summaries should separate:
  - official update observed
  - likely implication
  - questions still requiring validation
- Every AI intel summary must remind the user to verify source truth before making a technical decision.
