# Harness

The harness validates PM Copilot governance before workflow stages advance.

## Stabilized checks

The following checks are approved as the minimum stable protection layer:

- `eval_suite`: protects reusable quality cases.
- `real_output_eval`: protects real PRD/output quality from silent regression.
- `skill_generalization`: prevents project-specific lessons from leaking into generic skills.
- `prototype_preview_gate`: prevents PNG/HTML/full prototype work before user approval.
- `external_redaction`: protects B packages from protected-term leakage when a package path is supplied.

These stabilize existing checks only. They do not add a new harness or a new skill.

## Conditional checks

The following checks stay available only when the related capability is requested or present:

- `delivery_plan`: technical delivery planning requested.
- `ai_solution`: AI solution planning requested or governed AI artifacts exist.
- `agentic_delivery`: Codex-style development planning requested.
- `preference_cache`: project preference cache exists and must remain project-local.

## First-version checks
- `registry`: skills, MCP tools, stewards, and artifacts are registered consistently.
- `plugin_boundary`: plugin manifests, plugin-owned skill paths, and host dependency boundaries are valid.
- `steward_contract`: trace entries do not call unregistered capabilities or produce undeclared artifacts.
- `workflow_gate`: stage gates, workflow/action registration, steward stage ownership, skill input/output contracts, and human approvals are respected.
- `source_trace`: MCP-derived external data includes trace fields and human verification requirement.
- `prototype_preview_gate`: full-flow prototypes are blocked until prototype preview approval exists; when full prototypes are requested, Markdown, SVG, and PNG artifacts must exist and cover MVP plus later-phase page markers.
- `preference_cache`: project preference caches are isolated, active pointers are valid, and cleared caches are not reused.
- `delivery_plan`: optional delivery planning artifacts are complete when a project requests technical delivery planning.
- `ai_solution`: optional AI solution planning artifacts are complete when a project contains governed AI capability, model, prompt, RAG, memory, profile, coaching, and architecture work.
- `agentic_delivery`: optional Codex-style semi-automated development documents and task packages declare capability enablement, Skill/MCP routing, governance operating system, phase plans (`一期/二期/三期/最终`), write boundaries, validation commands, human supervision gates, teaching/memory routes, minimal-fix strategy, and a send-before-review report for optimality, blockers, executability, validation, rollback, and approval gates.
- `eval_suite`: reusable Skill evaluation cases cover multiple domains, registered Skills, required artifacts, and required quality assertions.
- `real_output_eval`: latest real output evaluation report passes all case-level quality assertions.
- `skill_generalization`: reusable Skill behavior and Skill-update proposal behavior fields do not contain project-specific leakage.
- `scaling_policy`: chief steward and sub-steward load stays within the dynamic scaling policy.
- `teaching_absorption`: accepted lessons are structured, assigned to affected components, and ready to be absorbed.
- `skill_update_proposal`: lesson-driven Skill update proposals require human approval and route to valid Skill files.
- `random_audit`: risk-weighted random audit of trace calls and boundaries when `--audit` is passed.
- `efficiency`: artifact size, Skill/MCP call count, repeated output, and token-like waste when `--efficiency` is passed.
- `external_redaction`: optional B-package protected-term scan when `--external-package` is passed.

## Usage
```bash
python3 harness/run_harness.py --base-dir . --project fitness-app-mvp --mode advisory --check-only
```

Use `--mode strict` when warnings should block advancement.
Use `--write-report` only when you intentionally want to refresh harness report files; the command prints every write path.

Run the random audit inspector:

```bash
python3 harness/run_harness.py --base-dir . --project fitness-app-mvp --mode advisory --check-only --audit
```

Run the efficiency auditor:

```bash
python3 harness/run_harness.py --base-dir . --project fitness-app-mvp --mode advisory --check-only --efficiency
```

Scan a B execution package before sharing:

```bash
python3 harness/run_harness.py --base-dir . --project fitness-app-mvp --mode advisory --check-only --external-package path/to/B-package
```

Run the real output evaluation before harness when case outputs change:

```bash
.venv/bin/python evals/run_real_output_eval.py --base-dir . --run-id 20260425T000000Z
```
