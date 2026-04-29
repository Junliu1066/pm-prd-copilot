# PM-skill

`PM-skill` is a private working repository for a personal PM Copilot. It has three jobs:

1. Turn rough requirements into PRD-ready artifacts.
2. Learn from your edits without changing the stable skill automatically.
3. Collect and summarize official AI updates for later model-selection and technical-route decisions.

## Repository layout

```text
.github/workflows/        GitHub Actions for daily intel, memory proposals, and regression
agent.md                  Chief steward operating protocol
governance/               Steward scaling and operating rules
registry/                 Registered plugins, skills, MCP tools, stewards, and artifacts
plugins/                  Detachable plugin bundles with their own manifests and skills
workflow/                 PRD workflow stages, actions, and approval policies
harness/                  Governance validation for registry, contracts, gates, sources, and scaling
teaching/                 User coaching logs, accepted lessons, open lessons, and PM principles
stewards/                 Active sub-steward responsibility protocols
pm-prd-copilot/           Stable skill, templates, memory, proposals, and evals
ai-intel/                 AI source registry, raw snapshots, events, daily reports, decision docs
shared/schemas/           Shared JSON schemas reused by PM workflows
projects/                 Project-specific inputs, generated drafts, and final edits
docs/                     Architecture and operating model notes
```

For the current canonical directory map, root file policy, UI design layer, and closeout rules, see [docs/repository_map.md](/Users/liujun/Desktop/产品经理skill/docs/repository_map.md).

For supervised cleanup candidates that should not be moved or deleted without review, see [docs/cleanup_inbox.md](/Users/liujun/Desktop/产品经理skill/docs/cleanup_inbox.md).

For the fixed daily governance report format, see [docs/daily_report_template.md](/Users/liujun/Desktop/产品经理skill/docs/daily_report_template.md).

For active, closeout, archive, and hard-delete lifecycle rules, see [docs/project_lifecycle.md](/Users/liujun/Desktop/产品经理skill/docs/project_lifecycle.md).

For the required two-round delivery self-check, see [docs/two_round_self_check.md](/Users/liujun/Desktop/产品经理skill/docs/two_round_self_check.md).

For version/model update testing and governance pruning, see [docs/version_model_update_review.md](/Users/liujun/Desktop/产品经理skill/docs/version_model_update_review.md).

For process errors, overnight test reports, and the bug index, see [docs/error_reports/README.md](/Users/liujun/Desktop/产品经理skill/docs/error_reports/README.md).

For active scheduled checks and their responsibilities, see [docs/scheduled_check_mechanisms.md](/Users/liujun/Desktop/产品经理skill/docs/scheduled_check_mechanisms.md).

For the supervised prototype preview, HTML conversion, packaging, and QA flow, see [docs/prototype_flow.md](/Users/liujun/Desktop/产品经理skill/docs/prototype_flow.md).

## Operating model

- `pm-prd-copilot/SKILL.md` is the stable layer.
- `plugins/` contains detachable plugin bundles. A plugin must be removable without changing the host pipeline except its registry reference.
- `plugins/prd-analysis-suite/` contains governed candidate PRD analysis skills that can be promoted after review.
- `pm-prd-copilot/memory/` is the learning layer.
- `pm-prd-copilot/proposals/` is the review layer.
- `pm-prd-copilot/scripts/propose_lesson_skill_update.py` routes accepted teaching lessons into supervised Skill update proposals.
- `ai-intel/` can auto-commit daily outputs.
- `memory` and `skill` changes should only move forward through reviewed proposals or PRs.
- The governed workflow is the default contract. Fast draft generation is allowed only as a labeled draft path and must not replace approval-gated delivery.
- Every file-editing task should finish with round 1 changed-work checks and round 2 omission/consistency checks.
- Do not add new skills, harness checkers, stewards, plugins, workflow stages, registry categories, long-lived rules, or automations unless existing components cannot cover the need.
- After version or model updates, run regression and harness, then propose deprecate/archive/delete candidates for unnecessary governance components. Hard deletion still requires exact user approval.
- Overnight error checks should record failures and bug candidates under `docs/error_reports/` and report items needing user approval.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 pm-prd-copilot/scripts/router.py init-project \
  --project demo-project \
  --title "商家财务流水批量导出"
python3 pm-prd-copilot/scripts/run_pipeline.py --base-dir . --project demo-project --stage all --mode rule
python3 pm-prd-copilot/scripts/router.py --base-dir . ui-style --project demo-project
python3 pm-prd-copilot/scripts/router.py --base-dir . closeout --project demo-project
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --efficiency
```

## Main production pipeline

The PM Copilot production chain writes these files under `projects/<project>/`:

- `01_requirement_brief.json`
- `01_requirement_brief.md`
- `02_prd.generated.json`
- `02_prd.generated.md`
- `03_user_stories.generated.json`
- `03_user_stories.generated.md`
- `04_risk_check.generated.json`
- `04_risk_check.generated.md`
- `05_tracking_plan.generated.json`
- `05_tracking_plan.generated.md`

Each stage also writes a `*.meta.json` file that records whether the output came from `rule`, `llm`, or `auto` fallback mode.

Each pipeline run also writes governance files under `projects/<project>/runs/<run-id>/`:

- `manifest.json`: which skills, stages, and outputs were allowed for this run.
- `trace.json`: which registered skills actually ran and which artifacts they produced.
- `harness_report.json`: governance check results when harness runs.
- `random_audit_report.json`: random inspector samples and findings when harness runs with `--audit`.

The default pipeline run id is `pipeline-latest`. Pass `--run-id <id>` when you need a stable named run for review.

Pipeline runs enforce approval gates from `workflow/prd_workflow.yaml` by default before entering gated workflow stages. `--governed` is kept only as a compatibility flag:

```bash
python3 pm-prd-copilot/scripts/run_pipeline.py --base-dir . --project demo-project --stage prd --mode rule
```

Use `--fast-draft` only for explicit draft exploration. Fast draft output must not replace approval-gated delivery:

```bash
python3 pm-prd-copilot/scripts/run_pipeline.py --base-dir . --project demo-project --stage prd --mode rule --fast-draft
```

For demo-only governed reruns, use `pipeline_assumption_overrides` in `project_state.json` instead of global `assumption_overrides` so pipeline test coverage does not imply product workflow or prototype approval.

Pipeline stage-to-workflow action mapping is declared once in `pm-prd-copilot/scripts/governance_trace.py` and written to each production manifest as `stage_actions`; the harness reads that manifest field instead of keeping a second hard-coded mapping.

## UI design style direction

Before building high-fidelity prototypes, generate a supervised UI style direction:

```bash
python3 pm-prd-copilot/scripts/router.py --base-dir . ui-style --project demo-project
python3 pm-prd-copilot/scripts/router.py --base-dir . ui-style --project demo-project --style concrete
```

The command writes:

- `projects/<project>/prototype/ui_style_direction.json`
- `projects/<project>/prototype/ui_style_direction.md`

The style catalog lives in `pm-prd-copilot/ui-design/data/visual_style_catalog.json`. It includes restrained operational styles and expressive styles such as concrete/cement editorial, brutalist, glass depth, AI lab dark, editorial magazine, Bauhaus grid, minimal luxury, warm humanist, retro terminal, neo clay, and data newsroom. Expressive styles are candidates and still require human approval before prototype generation.

## Supervised project closeout

Project closeout is report-only by default. It scans `projects/<project>/` and the matching `memory-cache/projects/<project>/` folder, then writes a dry-run package under `projects/<project>/closeout/`:

- `manifest.json`: full file inventory, cleanup classification, protected roots, and approval requirement.
- `closeout-report.md`: project summary, run status, human edit signals, and review checklist.
- `architecture-feedback.md`: draft signals for template, prompt, workflow, data-model, eval, and ADR improvements.
- `cleanup-plan.md`: dry-run cleanup grouping. It does not delete, move, archive, commit, push, or merge anything.

Run it through the router:

```bash
python3 pm-prd-copilot/scripts/router.py --base-dir . closeout --project demo-project
```

Any archive, deletion, GitHub commit, PR, prompt update, template update, or framework change still requires explicit human approval after reviewing the closeout package.
Archived items become eligible for hard deletion only after 30 days, and the exact delete list still requires human approval.

## Model-backed generation

The pipeline now supports:

- `--mode rule`: deterministic local generation only
- `--mode llm`: require the configured model path to succeed
- `--mode auto`: try the model first, then fall back to rule generation if the call fails or the output does not validate

Example:

```bash
export OPENAI_API_KEY=...
python3 pm-prd-copilot/scripts/run_pipeline.py --base-dir . --project demo-project --stage all --mode auto
```

The default model config is in [pm-prd-copilot/config/model_config.yaml](/Users/liujun/Desktop/产品经理skill/pm-prd-copilot/config/model_config.yaml). It currently targets OpenAI's Responses API with structured JSON output. Per OpenAI's official docs, the Responses API accepts `POST /v1/responses` with bearer auth, and structured output can be requested via `text.format.type=json_schema` using a JSON schema response format. Sources: [Responses API](https://developers.openai.com/api/reference/resources/responses/methods/create), [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses).

AI intel jobs remain separate:

```bash
python3 ai-intel/scripts/fetch_sources.py --base-dir .
python3 ai-intel/scripts/normalize_events.py --base-dir .
python3 ai-intel/scripts/summarize_daily.py --base-dir .
python3 ai-intel/scripts/update_decision_matrix.py --base-dir .
```

Architecture-impacting AI signals are recorded in `ai-intel/decisions/governance-architecture-signals.md`; they are recommendations only until you approve adoption.

## Review rules

- AI intel outputs must include a reminder to verify the source, date, model name, API status, and pricing before use.
- MCP outputs are source signals, not verified facts; source traces must be reviewed before being used as product evidence.
- The chief steward manages skills directly only while the system stays below the scaling thresholds in `governance/steward_scaling_policy.yaml`.
- Research, product judgment, prototype design, PRD writing, and review sub-stewards are active operating roles; new sub-stewards or peer chief stewards still require human approval.
- The random audit inspector can sample run traces and report suspected boundary violations to the responsible steward, chief steward, and user; it cannot modify artifacts or verify external truth.
- The PM coach captures user teaching and turns it into supervised proposals; accepted lessons must pass teaching absorption checks before they are treated as stable behavior.
- Lesson-driven Skill updates must be generated as proposals first; they cannot modify plugin Skill files until the user approves the exact change.
- The efficiency steward reports token-like waste, oversized artifacts, repeated output, and unnecessary calls; it can recommend optimization but cannot lower quality thresholds or change artifacts directly.
- Registered plugins must have a `.codex-plugin/plugin.json`, plugin-relative paths, and no direct dependency on host-only folders.
- Registered skills with a `path` must have a matching `SKILL.md`; plugin-owned skills must live inside their owning plugin.
- B execution packages must pass the external redaction checker before sharing.
- Memory and skill updates must be reviewed before merging.
- Regression should pass before any stable-layer prompt or template change is accepted.
