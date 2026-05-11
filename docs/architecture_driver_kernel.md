# Architecture Driver Kernel / 架构驱动内核

- Status: V0 architecture governance kernel.
- Purpose: turn architecture thinking into a lightweight operating mechanism for routing, closure, review, and distillation.
- Boundary: this is a governance judgment layer, not an execution tool. It does not create a new agent, skill, harness, workflow, plugin, or automation.
- Core rule: long-term stability has priority over feature count, automation volume, and process completeness.

## Positioning

The architecture driver kernel is the upstream governance layer for long-lived system behavior.

It decides:

- what kind of governance a task needs
- which existing mechanism should handle it
- whether the work loop is closed
- whether a new idea should stay candidate, be distilled, or be proposed for stable adoption
- whether user approval is required

It must not directly execute business work, write long-term memory, add stable rules, add skills, add harnesses, delete evidence, archive projects, push, or open PRs.

## Governance Modes

Use the lightest mode that can close the loop.

| Mode | Use when | Required output | Must not do |
|---|---|---|---|
| Light | Small fixes, wording edits, local docs, low-risk checks. | Main task, changed file, basic red/green or substitute check. | Trigger full governance, add tools, expand scope. |
| Standard | Templates, project lifecycle, PRD/Codex doc rules, normal workflow or harness boundary changes. | Impact note, affected node, validation, rollback note, approval boundary. | Treat candidate learning as stable. |
| Full | Stable policy, long-term memory, workflow contract, harness behavior, automation, deletion/archive, model/provider/cost change, external publishing. | Impact map, closed-loop proof, red/green tests, rollback plan, user approval. | Auto-approve, auto-stable, auto-delete, auto-push. |

Small tasks do not enter full governance unless they touch stable behavior or approval boundaries.

## Routing Responsibilities

The kernel routes work to existing mechanisms:

| Need | Route to | Kernel decision |
|---|---|---|
| Impact relationship | `docs/architecture_knowledge_map.md` | Check affected upstream and downstream nodes. |
| Map maintenance | `docs/architecture_knowledge_map_governance.md` | Mark stale or partial nodes; do not treat the map as source of truth. |
| Stable work rules | `agent.md` | Keep rules minimal and enforce task-drift control. |
| Long-term preference | `pm-prd-copilot/memory/user_preferences.md` | Require explicit approval before writing. |
| Project preference | `memory-cache/` | Keep project-local until closeout disposition. |
| Workflow / artifact / steward contracts | `workflow/` and `registry/` | Require owner, artifact, stage, and gate alignment. |
| Harness / eval | `harness/` and eval suites | Prefer conditional checks and minimal false-positive boundaries. |
| Candidate learning | `docs/proposals/` and `docs/architecture-inbox/` | Keep as candidate until distilled and approved. |

## File-First Architecture Memory

Architecture memory must stay explicit, inspectable, user-owned, and model-portable.

| Principle | Kernel rule | Risk prevented |
|---|---|---|
| Explicit memory | Long-lived knowledge must be visible in files, not hidden in model memory. | Unknown or unreviewable behavior changes. |
| User-owned data | Architecture memory belongs in the local repo or user-controlled files. | Lock-in to one AI provider or app. |
| File over app | Prefer Markdown, YAML, JSON, and images before databases or product UI. | Overbuilding storage and making knowledge hard to migrate. |
| BYOAI | Any capable AI should be able to read the same files and continue the work. | Architecture becoming dependent on one model's private memory. |

The kernel may use model context for execution, but model context is not a stable source of truth. Stable memory must be written to approved files through the normal approval boundary.

## Architecture Distillation Mechanism / 架构蒸馏机制

Do not use a simple exit mechanism for new ideas. Use architecture distillation.

Architecture distillation means:

```text
candidate signal
-> real-use evidence
-> value extraction
-> redundancy check
-> stable-fit review
-> user approval if needed
-> keep / merge / downgrade / archive candidate / delete-after-review candidate
```

The goal is to keep useful learning and remove noise without losing evidence.

## Distillation Decisions

| Decision | Meaning | Approval boundary |
|---|---|---|
| Keep as candidate | Useful, but not proven enough for stable behavior. | Kernel may recommend; no stable effect. |
| Merge into existing rule | Valuable, but should strengthen an existing rule instead of adding a new component. | User approval if it changes stable behavior. |
| Downgrade | Useful only for docs, checklist, or one project. | User approval if it affects long-term memory or project disposition. |
| Archive candidate | Keep evidence but stop active use. | User approval for archive action. |
| Delete-after-review candidate | Low value after retention period and second review. | User approval required before deletion. |
| Stable proposal | Reusable, verified, and low-maintenance enough to become stable. | User approval required. |

## Closed-Loop Standard

A module, rule, or mechanism is not landed as stable unless it can show:

```text
input
-> action
-> artifact
-> owner
-> validation
-> feedback / closeout
-> approval boundary
```

If one element is missing, mark it `partial_loop`.
If owner, validation, or approval boundary is missing, mark it `open_loop`.

## Red / Green And Rollback

Every architecture change needs an executable test or substitute acceptance check.

| Check | Meaning |
|---|---|
| Red check | What failure, conflict, over-governance, leakage, or stale behavior this change prevents. |
| Green check | What proves the intended path works. |
| Rollback path | How to undo the change without touching unrelated user work. |

For documentation-only governance changes, red/green tests may be acceptance checks.

## Approval Levels

| Level | Who decides | Examples |
|---|---|---|
| L1 automatic | Existing rules and existing approved scope. | Low-risk wording, local checklist, non-stable proposal note. |
| L2 steward / kernel recommendation | Existing components, supervised candidate work, conditional checks. | Candidate review, impact note, lifecycle inventory, non-stable distillation proposal. |
| L3 user approval | Stable, irreversible, external, costly, or high-risk changes. | Stable policy, long-term memory, deletion, archive, push/PR, new or stable skill/harness, model provider/cost, external delivery. |

## Anti-Bloat Rules

- Prefer one-line or one-file fixes when they close the loop.
- Prefer strengthening an existing rule over adding a new rule.
- Prefer conditional checks over default heavy checks.
- Prefer proposal and observation before stable adoption.
- Do not add a skill, harness, workflow stage, automation, or long-lived rule unless existing mechanisms cannot solve the problem.
- If a mechanism increases maintenance cost more than it reduces risk, keep it candidate or downgrade it.

## Success Metrics

The kernel is working when:

- small tasks stay lightweight
- architecture changes have visible impact and rollback notes
- candidate ideas do not silently become stable
- long-term memory and project memory stay separated
- stale map nodes are detected instead of trusted
- skill / harness / automation count does not grow without evidence
- user approval is concentrated on L3 decisions instead of every small step

## Relationship To The Knowledge Map

The architecture driver kernel defines how architecture governance should behave.

The architecture knowledge map shows where architecture relationships exist.

If they conflict with source files:

```text
source file wins
-> map is corrected
-> kernel checks whether the change is light, standard, or full governance
```

The map is navigation. The kernel is judgment. Existing files remain the source of truth.
