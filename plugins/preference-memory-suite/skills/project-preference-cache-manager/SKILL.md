---
name: project-preference-cache-manager
description: Manage project-scoped user preference caches for PRD and prototype work, including creating isolated caches, recording candidate preferences, applying approved preferences, resetting into a new cache, and clearing cache usage on user request.
---

# Project Preference Cache Manager

## Purpose

Maintain project-level preference memory without leaking preferences across unrelated projects. This skill manages the cache lifecycle; downstream PRD, research, flow, and prototype skills read only the active cache for the current project.

## Lifecycle Rules

1. Create one isolated cache per product project.
2. When the user asks to restart or re-record preferences, create a new cache version and move the pointer to it. Do not merge old preferences unless the user asks.
3. When the user asks to clear memory, mark the project cache pointer as cleared so downstream skills stop reading it.
4. Record new user feedback as candidate preference first unless the user explicitly says it is approved or permanent.
5. Move candidate preferences into approved preferences only after user approval.
6. Keep source trace for each preference: user quote or source, date, affected skill/category, and approval status.
7. Never use another project's cache when working on the current project.
8. Keep project preferences separate from generic skill lessons. A project preference may inform the current project only; a generic lesson must be abstracted and approved before it changes a reusable skill.

## Preference Categories

- market and competitor assumptions.
- PRD structure and review preferences.
- prototype style and interaction preferences.
- product decision heuristics.
- source and verification preferences.
- workflow and approval preferences.

## Downstream Use

Before generating PRD analysis, business flows, prototypes, or PRD drafts:

1. Locate the current project's active cache pointer.
2. Read approved preferences only.
3. Treat candidate preferences as review context, not binding rules.
4. Mention when a preference influenced the output.

## Project Preference vs Generic Lesson

Use this distinction when processing user feedback:

- Project preference: contains a specific market, style, label, module, scenario, or domain decision for the current product.
- Generic lesson: describes a reusable method that can work across different products without carrying the original project's nouns.
- If uncertain, record the feedback as project preference first and ask before promoting it into a generic skill improvement.

## Output Contract

Read [references/output-contract.md](references/output-contract.md) for the formal artifact shape. Always include:

- `project_id`
- `cache_id`
- `operation`
- `status`
- `approved_preferences_used`
- `candidate_preferences_recorded`
- `source_trace`

## Guardrails

- Do not mix preferences between projects.
- Do not silently promote candidate preferences to approved preferences.
- Do not continue using a cleared cache.
- Do not store secrets, API keys, private credentials, or personal sensitive data.
- Do not override explicit instructions in the current user request with stale preferences.
- Do not leak project-specific preferences into generic skills or unrelated projects.
