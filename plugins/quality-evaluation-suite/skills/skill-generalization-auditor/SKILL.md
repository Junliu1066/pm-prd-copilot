---
name: skill-generalization-auditor
description: Audit PM Copilot skills, lesson proposals, and skill-update plans for overfitting to one project, leaking project preferences into generic skills, hard-coded market/style/platform defaults, and unclear routing between project cache and reusable skill behavior.
---

# Skill Generalization Auditor

## Purpose

Protect reusable PM skills from becoming project-specific templates. This skill decides whether feedback belongs in the current project cache, a user-level preference, an open lesson, or a generic skill improvement.

## Workflow

1. Inventory the review scope: changed skills, proposed lessons, skill-update proposals, project preference changes, and any evaluation cases supplied by the harness or user.
2. Classify each learning item:
   - `project_preference`: market, style, label, module, scenario, platform, or domain choice for one product.
   - `user_preference`: durable preference that should apply across the user's future work, only after approval.
   - `generic_skill_rule`: industry-neutral method that works across unrelated products.
   - `open_decision`: not enough approval or evidence to promote.
3. Scan generic skill text for hard-coded project defaults:
   - fixed market defaults.
   - visual style defaults copied from one project.
   - domain-specific labels, buttons, flows, competitors, or platform assumptions.
   - product-specific examples that are not clearly marked as examples.
4. Route findings:
   - project-specific material goes to the active project preference cache.
   - durable user defaults require explicit user approval and trace.
   - reusable methods may become generic skill rules only after abstraction.
   - unclear items stay in open lessons or proposals.
5. Recommend the smallest safe correction and the validation that should run afterward.

## Evaluation Use

When evaluation cases are available, use them to check generality:

- The same skill should work across unrelated product domains.
- The skill should not reuse another case's market, style, labels, or feature names.
- Required outputs should be governed by registered artifacts and stage gates.
- Preview-first, source-trace, preference-cache, and human-approval rules should remain intact.

## Output Contract

Read [references/output-contract.md](references/output-contract.md) for the formal artifact shape. Always include:

- `audit_scope`
- `findings`
- `routing_decisions`
- `generic_rules_allowed`
- `project_specific_items`
- `recommended_fixes`
- `validation_plan`

## Guardrails

- Do not update skills directly; report findings and recommended fixes.
- Do not promote a project preference into a generic rule without explicit approval.
- Do not verify external truth; only check traceability, scope, and generalization risk.
- Do not block source quotes or project caches from containing project-specific terms; block only leakage into reusable skill behavior.
