# Operating Model

## Daily rhythm

1. Put raw requirement notes into `projects/<slug>/00_raw_input.md`.
2. Generate a first draft into `*.generated.md`.
3. Save your final edited version into `*.final.md`.
4. Run memory proposal generation on the diff.
5. Review proposed preference updates before accepting them.
6. Review overnight error reports in `docs/error_reports/`.
7. Report architecture health, bug status, user teaching, AI governance signals, cleanup status, and approval needs using `docs/daily_report_template.md`.

## Overnight error check rhythm

1. Run regression and harness in the workspace.
2. Check automation health for `ai-gpt-5-5`, `bug`, and `codex`.
3. Confirm Finding 3 / `BUG-2026-04-28-001` remains fixed: production pipeline defaults to governed and fast draft requires `--fast-draft`.
4. Record failures, warnings, repeated issues, and suspected causes in `docs/error_reports/daily/`.
5. Append confirmed bugs or watch items to `docs/error_reports/bug_log.md`.
6. Report issues that need user approval before fixing.
7. Do not delete, archive, commit, push, change stable skills, change harness, or switch model providers from the overnight check alone.

The scheduled check map is `docs/scheduled_check_mechanisms.md`.

## Delivery self-check rhythm

1. After editing, run round 1 checks for changed work.
2. Fix any direct issue and rerun the affected check.
3. Run round 2 checks for omissions, consistency, generated outputs, latest user corrections, and approval needs.
4. Confirm that any new skill, harness checker, steward, plugin, workflow stage, registry category, long-lived rule, or automation was necessary.
5. Report both rounds before delivery.

The full protocol is `docs/two_round_self_check.md`.

## Contract responsibility rhythm

Use `docs/contract_responsibility_layer.md` whenever a change touches interfaces, harness checks, schemas, workflow actions, registry entries, automations, templates, prompt builders, renderers, package builders, or generator outputs.

1. Name the affected contract and responsible steward before editing.
2. Decide whether the command/check is read-only or writes report/state files.
3. Check whether template, schema, prompt, renderer, sample output, regression, and daily report wording must move together.
4. Prefer extending an existing document, check, or script before proposing a new Skill, harness, steward, plugin, workflow stage, or automation.
5. Report the validation command and user approval point.
6. Do not treat a passing harness run as proof of semantic quality unless the relevant semantic checks are included.

## Version and model update rhythm

1. Run regression and harness after each version update or model/provider/SDK/API update.
2. Audit whether any skill, harness checker, steward, plugin, workflow stage, registry category, long-lived rule, automation, template, or package path is now unnecessary.
3. Classify candidates as keep, deprecate, archive, or delete candidate.
4. Report evidence, replacement path, risk, and required user approval.
5. Do not hard-delete without the user's exact approval.

The full protocol is `docs/version_model_update_review.md`.

## Weekly rhythm

1. Review accumulated memory proposals.
2. Generate a weekly skill-upgrade proposal.
3. Run regression.
4. Approve or reject the proposed change set.

## AI intel rhythm

1. GitHub Actions fetch official source pages.
2. Snapshots are normalized into events.
3. A daily report and decision documents are updated.
4. Every report must remind you to verify source truth before decision-making.
5. Architecture-impacting signals are recorded in `ai-intel/decisions/governance-architecture-signals.md` before any adoption decision.
