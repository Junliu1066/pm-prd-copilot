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

## Stable workflow

1. Identify the task stage:
   - intake
   - prd
   - stories
   - risk
   - tracking
   - review
   - model-decision
2. Read only the minimum inputs needed:
   - raw notes from `projects/<slug>/`
   - templates from `templates/`
   - approved preferences from `memory/`
   - decision docs from `../ai-intel/decisions/` for AI-related questions
3. Produce a draft artifact.
4. Make facts, assumptions, and open questions explicit.
5. Do not update stable instructions automatically.

## Learning and upgrade rules

- You may learn from user edits, but only by creating proposals under `proposals/`.
- Do not directly rewrite `SKILL.md`, templates, or stable references without explicit approval.
- Treat short-term edits as potential signals, not permanent preferences.
- When asked for AI landscape guidance, remind the user to verify source truth, release status, and pricing before deciding.

## Files to consult

- `templates/prd_template_2026.md`
- `templates/requirement_intake_template.md`
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
