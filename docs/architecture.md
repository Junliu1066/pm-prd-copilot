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

## Update policy

- Daily AI intel can commit directly to the repository.
- Daily memory extraction can only create reviewable proposals.
- Weekly skill-upgrade jobs can only create a draft PR or proposal file.
- Stable artifacts are updated only after human approval.

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
