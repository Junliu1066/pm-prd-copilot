# Architecture Knowledge Map

- Status: V0 lightweight index.
- Purpose: help the agent inspect impact, memory boundaries, and closure before changing long-lived architecture behavior.
- Boundary: this file is an index, not the source of truth. If this map conflicts with source files, source files win and this map should be updated.
- Rule: do not use this file to approve stable policy, long-term memory, deletion, archive, staging, commit, push, PR, new skill, new harness, or automation changes.
- Upstream kernel: `docs/architecture_driver_kernel.md` defines architecture governance judgment, routing, closure, and architecture distillation / 架构蒸馏机制. This map only indexes relationships and impact.

## Operating Rules

- Keep this map small. It should point to facts, not duplicate all facts.
- Keep architecture memory explicit and file-based. A model's private memory, chat context, or app state is not a stable source of truth.
- Prefer Markdown, YAML, JSON, and images for durable knowledge so the user can inspect, search, version, move, and reuse it with any AI or tool.
- Use it before changing stable rules, memory, workflow, harness, skill, automation, templates, or project lifecycle rules.
- Every stable module should be able to show a closed loop: input, action, artifact, owner, validation, feedback, and approval boundary.
- Mark a module as `partial_loop` or `open_loop` when a critical closure part is missing.
- Mark a node as `partial_loop / stale_map_node` when its source file changed but this map was not reconciled.
- Red/green tests may be executable tests or acceptance checks, but they must state what fails and what proves the path works.

## File-Based Memory Principles

The knowledge map follows a file-first personalization and architecture-memory model:

| Principle | Meaning in this repo | Required handling |
|---|---|---|
| Explicit | Architecture memory must be visible and inspectable. | Put stable knowledge in approved files; do not rely on hidden model memory. |
| User-owned | The user controls the knowledge base. | Keep durable memory in the repo or user-owned local files. |
| File over app | Files are the interoperability layer. | Prefer Markdown, YAML, JSON, and images before a database, SaaS workspace, or custom app. |
| BYOAI | The knowledge base should work with Codex, Claude, OpenCode, or future models. | Avoid provider-specific assumptions in stable memory. |
| Auditable | Every memory change needs a source and approval boundary. | Link back to source file, proposal, project closeout, or user-approved preference. |

These principles do not create a new memory system. They constrain how existing memory, proposals, projects, and governance maps should be maintained.

## Governance Module

- Governance file: `docs/architecture_knowledge_map_governance.md`
- Upstream kernel: `docs/architecture_driver_kernel.md`
- Maintainers: `development-governance-steward` for workflow, harness, skill, steward, template, and automation impact; `learning-steward` for long-term memory, project memory, proposal, and architecture-inbox boundaries.
- Trigger: any change to a long-lived architecture node listed in this map.
- Output: impact summary, closure status, red/green test or substitute check, map update need, and approval boundary.
- Boundary: the module can inspect, mark, and recommend; it cannot approve stable changes, long-term memory writes, deletion, archive, push/PR, new skill, new harness, or automation changes.

## Core Nodes

| Node | Source of truth | Role | Downstream impact | Closure status | Checks |
|---|---|---|---|---|---|
| Architecture driver kernel / 架构驱动内核 | `docs/architecture_driver_kernel.md` | Defines governance modes, routing, approval levels, closed-loop standard, and architecture distillation / 架构蒸馏机制. | Work rules, knowledge map, memory boundaries, workflow, harness, skill, automation, project lifecycle, proposals. | `partial_loop` until V0 is exercised on real architecture changes; cannot execute tasks directly. | Check that changes use light / standard / full mode and do not bypass L3 approval. |
| Work rules | `agent.md` | Defines agent behavior, task drift control, red/green tests, and delivery closure. | All repo work, templates, reports, automation prompts, user-facing delivery summaries. | `closed_loop` when changed with impact review and checks. | `git diff --check -- agent.md`; inspect this map for affected nodes. |
| Long-term memory | `pm-prd-copilot/memory/user_preferences.md` | Stores only explicitly approved long-term user preferences. | PRD defaults, Codex development docs, prototype rules, packaging, report language. | `closed_loop` when each item has explicit approval and does not conflict with project memory. | Check against `memory-cache/` and `docs/proposals/*` before adding. |
| Project memory | `memory-cache/` | Stores project-only preferences and continuity data. | Current project context and project closeout. | `partial_loop` until project closeout decides clear / archive / propose long-term memory. | `harness/preference_cache_checker.py`; closeout disposition review. |
| Thread registry | `docs/thread_registry.md` | Tracks current main thread, parked work, next actions, and approval points. | Task recovery, anti-drift behavior, daily reports, project lifecycle sequencing. | `partial_loop` while it remains trial policy. | Check current main thread before starting adjacent work. |
| Workflow actions | `workflow/actions.yaml` and `workflow/prd_workflow.yaml` | Defines workflow stages, allowed actions, and approval gates. | Pipeline, harness workflow gate, artifact ownership, steward assignment. | `closed_loop` when every workflow action has registered skill, steward, inputs, outputs, and gate behavior. | `harness/workflow_gate_checker.py`; regression. |
| Artifact registry | `registry/artifacts.yaml` | Defines produced artifacts, paths, owners, retention, and boundaries. | Pipeline outputs, project files, closeout, harness checks. | `partial_loop` when an artifact is terminal or detachable without explicit closeout notes. | Artifact producer / consumer review; harness registry validation. |
| Skill registry | `registry/skills.yaml` | Defines available skill capabilities and read/write contracts. | Workflow actions, plugin candidate visibility, harness contract checks. | `closed_loop` when each active skill has steward, reads, writes, and no hidden stable promotion. | `harness/steward_contract_checker.py`; plugin boundary checks. |
| Steward registry | `registry/stewards.yaml` | Defines owners, allowed stages, responsibilities, and approval limits. | Workflow ownership, random audit, teaching, efficiency, escalation. | `closed_loop` when action stages match steward allowed stages. | `harness/workflow_gate_checker.py`; `harness/steward_contract_checker.py`. |
| Harness checks | `harness/` | Validates registry, workflow, prototype, delivery, AI solution, preference cache, eval, source trace, efficiency. | Stable gates, daily checks, model update adaptation, project closeout. | `closed_loop` when checker is invoked, conditional scope is clear, and false-positive boundary is reviewed. | `python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency`. |
| Codex development docs | `pm-prd-copilot/templates/codex_development_document_template.md` and `pm-prd-copilot/rules/development_document_policy.md` | Defines executable Codex development documentation and multi-branch execution plan. | Agentic delivery, task packages, branch governance, validation, rollback. | `partial_loop` until real project execution evidence proves the branch system. | Real-output review; red/green task package acceptance. |
| PRD generation | `pm-prd-copilot/templates/prd_template_2026.md`, generation scripts, and schemas | Defines PRD structure, page descriptions, page navigation, prototype layer, and AI-model conditional output. | PRD, prototype flow, Codex dev docs, regression cases. | `closed_loop` when regression and schema checks pass. | `python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict`. |
| Product value gate | `pm-prd-copilot/scripts/generate_value_gate.py`, `shared/schemas/value_gate.schema.json`, workflow and pipeline contracts | Routes idea input before PRD investment. | PRD generation, MVP path, research-required path, stop/redline decisions. | `partial_loop` while current V0 changes remain unsubmitted or under observation. | Value gate regression cases; workflow gate check. |
| AI intel | `ai-intel/` | Collects AI-related signals for governance architecture candidates. | Model update review, architecture inbox, AI decision candidates. | `partial_loop` because raw evidence and decision updates remain supervised candidates. | AI intel lifecycle review; no direct stable updates. |
| Automations | `/Users/liujun/.codex/automations/*/automation.toml` | Runs scheduled sentinel, daily report, development-thread review, and weekly backup. | Governance reports, model update triggers, bug reports, GitHub backup. | `partial_loop` until overlap and permissions are rechecked after consolidation. | Automation health review; no duplicate model-update logic outside sentinel. |
| Project lifecycle | `docs/project_lifecycle.md`, `pm-prd-copilot/scripts/closeout_project.py`, project closeout reports | Controls project closeout, archive, cleanup, and architecture feedback. | `projects/*`, `memory-cache/`, architecture inbox, delete-after-30-days candidates. | `partial_loop` for active projects; `closed_loop` only after user-approved closeout. | Closeout report, cleanup plan, preference-memory disposition. |
| Proposal inbox | `docs/proposals/*` and `docs/architecture-inbox/*` | Stores candidate ideas, audits, staging plans, and architecture feedback. | Stable policy candidates, deletion candidates, future implementation plans. | `partial_loop` by design; proposals do not become stable without user approval. | Proposal lifecycle review; 30-day deletion candidate checks. |

## Memory Boundaries

| Memory type | Location | Allowed use | Forbidden use | Exit path |
|---|---|---|---|---|
| Long-term preference | `pm-prd-copilot/memory/user_preferences.md` | Approved reusable user preferences only. | Adding project-specific or inferred preferences without explicit approval. | User-approved update, then regression / harness if behavior changes. |
| Project preference | `memory-cache/projects/{project}/` | Current project continuity and project-only decisions. | Cross-project reuse or automatic long-term promotion. | Project closeout: clear, keep as project evidence, or propose long-term item. |
| Candidate learning | `docs/proposals/*`, `docs/architecture-inbox/*` | Evidence, reasoning, and proposal material. | Treating candidate material as stable behavior. | Architecture distillation: keep, merge, downgrade, archive candidate, or delete-after-review candidate with approval where required. |
| Model context | Chat context or provider-side memory | Temporary reasoning aid only. | Treating hidden or non-exportable context as durable architecture memory. | Convert useful learning into an explicit file and route through approval or distillation. |

## Change Impact Checklist

Use this checklist before changing a long-lived architecture node.

| Planned change | Must inspect | Typical downstream risk |
|---|---|---|
| Change architecture governance principles | Architecture driver kernel, work rules, knowledge map, long-term memory, workflow, harness, automation. | Over-governance, hidden stable rule changes, missing approval boundary. |
| Change `agent.md` | Long-term memory, templates, harness policy, automation prompts, thread registry. | New rule conflicts, task drift, over-governance. |
| Change `user_preferences.md` | `memory-cache/`, proposals, thread registry, PRD and Codex templates. | Project preference leaking into long-term behavior. |
| Change workflow or actions | artifact registry, skill registry, steward registry, pipeline, workflow harness. | Unknown action, missing owner, stage mismatch, bypassed approval gate. |
| Change artifact schema or path | pipeline scripts, generated project files, harness checks, closeout scripts. | Broken generated outputs or stale project artifacts. |
| Change harness | run harness entrypoint, false-positive boundary, regression, model update policy. | Over-blocking lightweight work or weakening safety checks. |
| Change automation | active status, schedule, model, reasoning effort, cwd, write paths, overlap with other automations. | Duplicate checks, automatic writes, unexpected cost or noise. |
| Change template | generator scripts, schemas, regression cases, real-output eval, B package rules. | Output drift or hidden framework exposure. |

## Closure Labels

| Label | Meaning | Landing rule |
|---|---|---|
| `closed_loop` | Inputs, action, artifact, owner, validation, feedback, and approval boundary are clear. | May be treated as stable only if source files also approve it. |
| `partial_loop` | Useful module, but one or more closure parts depend on proposal, closeout, or manual review. | Keep supervised; do not stable-promote automatically. |
| `open_loop` | Missing critical owner, action, artifact, validation, or approval boundary. | Do not land as stable; create a fix plan first. |

## Red / Green Test Examples

| Scenario | Red test | Green test | Closure proof |
|---|---|---|---|
| Stable rule change | Rule conflicts with long-term memory or lacks approval boundary. | Rule has source, impact map, checks, and approval status. | `agent.md` and this map agree, and checks pass. |
| Project preference | Preference appears in long-term memory without approval. | Preference remains in `memory-cache/` and has closeout disposition. | No cross-project reuse; long-term update requires approval. |
| Workflow change | Workflow action references unknown skill, steward, or artifact. | Workflow gate passes and registered owners match. | Action -> artifact -> steward -> harness path is visible. |
| Harness change | Checker fails ordinary lightweight tasks without trigger evidence. | Checker passes unrequested scope and fails only real boundary violations. | Trigger, validation, and advisory/full behavior are documented. |
| Automation change | Automation duplicates sentinel logic or writes files without approval. | Automation reports health and respects write boundaries. | Cwd, status, model, schedule, write paths, and approval needs are reported. |

## Update Rules

- Update this map when a stable architecture node changes.
- If a source file changes and this map is not updated, mark the affected row `partial_loop / stale_map_node` until reconciled.
- Do not add low-value nodes; prefer stable rules, memory, workflow, harness, automation, templates, and lifecycle boundaries.
- If a node becomes too detailed, move details back to its source file and keep only the relationship here.
- If this map becomes stale, mark the affected row `partial_loop` until reconciled.
