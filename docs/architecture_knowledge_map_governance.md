# Architecture Knowledge Map Governance

- Status: V0 governance module.
- Purpose: keep `docs/architecture_knowledge_map.md` useful, current, and lightweight.
- Boundary: this module is a document-based responsibility mechanism. It does not create a new agent, skill, harness, workflow, plugin, or automation.
- Source rule: source files remain authoritative. The knowledge map is an index and impact guide.
- Upstream kernel: `docs/architecture_driver_kernel.md` defines governance modes, approval levels, closed-loop standards, and architecture distillation / 架构蒸馏机制. This module maintains the map under that kernel.

## Goals

This module exists to prevent the knowledge map from becoming stale or misleading.

It manages:

- relationship maintenance between long-lived architecture nodes
- impact analysis before stable architecture changes
- stale-map detection
- memory boundary checks
- closure review for stable modules
- red/green or substitute acceptance checks for governance changes

It must not become a second source of truth.
It must not become the architecture driver itself; it only maintains the map and reports impact.

## Responsibility

| Owner | Responsibility |
|---|---|
| `development-governance-steward` | Workflow, action, artifact, skill, steward, harness, template, automation, and Codex development-document impact. |
| `learning-steward` | Long-term memory, project memory, proposal, architecture inbox, teaching, closeout learning, and preference-boundary impact. |
| `pm-copilot-chief` | Escalation, approval boundary, and unresolved conflict routing. |
| User | Stable policy, long-term memory, deletion, archive, push/PR, new or stable skill/harness, and other L3 approvals. |

## Trigger Conditions

Run this governance module when any of these change or are proposed to change:

- `docs/architecture_driver_kernel.md`
- `agent.md`
- `pm-prd-copilot/memory/user_preferences.md`
- `memory-cache/`
- `workflow/actions.yaml` or `workflow/prd_workflow.yaml`
- `registry/artifacts.yaml`, `registry/skills.yaml`, or `registry/stewards.yaml`
- `harness/`
- automation configuration
- PRD, Codex development document, distribution, redaction, or project lifecycle templates
- `docs/thread_registry.md`
- `docs/proposals/*` entries being promoted, archived, or deleted

## Required Output

Each run should produce a concise impact note with:

- changed or proposed source file
- governance mode from the architecture driver kernel: light, standard, or full
- affected knowledge-map node
- upstream inputs
- downstream consumers
- closure status: `closed_loop`, `partial_loop`, `open_loop`, or `stale_map_node`
- red test or substitute failure check
- green test or substitute pass check
- whether `docs/architecture_knowledge_map.md` needs an update
- approval boundary: L1, L2, or L3

## Architecture Distillation Boundary / 架构蒸馏边界

Candidate ideas, rules, tools, checks, and project learnings must not become stable directly.

Use the architecture driver kernel's distillation path:

```text
candidate signal
-> real-use evidence
-> value extraction
-> redundancy check
-> stable-fit review
-> user approval if needed
-> keep / merge / downgrade / archive candidate / delete-after-review candidate
```

This module may identify a stale or useful candidate. It cannot approve stable adoption, archive, deletion, long-term memory writes, or new skill / harness creation.

## Stale Map Rule

If a source file changes and the knowledge map does not reflect the new relationship, mark the affected node:

```text
partial_loop / stale_map_node
```

Do not treat that node as stable until the map is reconciled from the source file.

If the map conflicts with a source file:

```text
source file wins
-> map is corrected
-> affected node returns to closed_loop only after checks pass
```

## Memory Boundary Rule

The module must separate:

- long-term memory: approved reusable preferences only
- project memory: current project continuity only
- proposals: candidate knowledge only
- architecture inbox: reusable architecture feedback candidates only

It must block these mistakes:

- project preference copied into long-term memory without approval
- proposal treated as stable policy
- temporary staging or commit notes treated as reusable guidance
- closeout learning applied across projects without user approval

## Closure Standard

A stable module is closed only when these are clear:

```text
input
-> action
-> artifact
-> owner
-> validation
-> feedback / closeout
-> approval boundary
```

If one of these is missing, the module is `partial_loop`.

If owner, validation, or approval boundary is missing, the module is `open_loop` and cannot be treated as stable.

## Red / Green Checks

Use executable tests when they exist. Use acceptance checks for documents and governance rules.

Minimum checks:

- Red check: what failure, conflict, leak, or stale map condition this change prevents.
- Green check: what proves the intended path works.
- Closure proof: what shows the source file, map, and approval boundary agree.

## Forbidden Actions

This module cannot:

- approve stable policy
- override the architecture driver kernel
- write long-term memory
- delete, archive, or move evidence
- stage, commit, push, or open PRs
- create or stabilize a skill
- create or stabilize a harness
- create automation
- override source files
- bypass user approval for L3 actions

## When User Approval Is Required

Always escalate before:

- changing stable rules
- writing long-term memory
- deleting or archiving material
- changing model provider, model cost, or external publishing behavior
- adding or stabilizing skill / harness / workflow / automation
- pushing, creating PRs, or publishing external packages
- accepting unresolved high-risk conflicts

## V0 Acceptance

This module is successful when:

- changes to long-lived architecture nodes have an impact note
- stale map entries are visible instead of silently trusted
- project memory and long-term memory stay separated
- proposal material does not become stable without approval
- red/green or substitute checks are recorded for governance changes
- no new agent, skill, harness, workflow, plugin, or automation is added
