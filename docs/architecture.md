# Architecture

## Core layers

1. Stable layer
   - `pm-prd-copilot/SKILL.md`
   - templates
   - shared schemas
2. Learning layer
   - `memory/`
   - project diffs between `*.generated.md` and `*.final.md`
3. Review layer
   - `proposals/memory/`
   - `proposals/skill-patches/`
4. Intel layer
   - `ai-intel/raw/`
   - `ai-intel/events/`
   - `ai-intel/daily/`
   - `ai-intel/decisions/`
5. Governance contract layer
   - `workflow/actions.yaml`
   - `workflow/prd_workflow.yaml`
   - `registry/artifacts.yaml`
   - `registry/skills.yaml`
   - `registry/stewards.yaml`
6. Contract responsibility layer
   - `docs/contract_responsibility_layer.md`
   - `governance/steward_operating_rules.yaml`
   - owner evidence for interface, harness, schema, workflow, registry, automation, and generator changes

## Update policy

- Daily AI intel can commit directly to the repository.
- Daily memory extraction can only create reviewable proposals.
- Weekly skill-upgrade jobs can only create a draft PR or proposal file.
- Stable artifacts are updated only after human approval.
- AI governance signals can create proposals, but adoption decisions stay with the user.
- Interface, harness, schema, workflow, registry, automation, and generator contract changes must pass the contract responsibility layer before implementation.

## Failure handling

Every scheduled job should record:

- source
- runtime
- stage
- error type
- http status
- likely cause
- next action

The canonical log directory is `ai-intel/logs/`.
