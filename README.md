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
registry/                 Registered skills, MCP tools, stewards, and artifacts
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

## Operating model

- `pm-prd-copilot/SKILL.md` is the stable layer.
- `pm-prd-copilot/memory/` is the learning layer.
- `pm-prd-copilot/proposals/` is the review layer.
- `ai-intel/` can auto-commit daily outputs.
- `memory` and `skill` changes should only move forward through reviewed proposals or PRs.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 pm-prd-copilot/scripts/router.py init-project \
  --project demo-project \
  --title "商家财务流水批量导出"
python3 pm-prd-copilot/scripts/run_pipeline.py --base-dir . --project demo-project --stage all --mode rule
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --audit
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

## Review rules

- AI intel outputs must include a reminder to verify the source, date, model name, API status, and pricing before use.
- MCP outputs are source signals, not verified facts; source traces must be reviewed before being used as product evidence.
- The chief steward manages skills directly only while the system stays below the scaling thresholds in `governance/steward_scaling_policy.yaml`.
- Research, product judgment, PRD writing, and review sub-stewards are active operating roles; new sub-stewards or peer chief stewards still require human approval.
- The random audit inspector can sample run traces and report suspected boundary violations to the responsible steward, chief steward, and user; it cannot modify artifacts or verify external truth.
- The PM coach captures user teaching and turns it into supervised proposals; accepted lessons must pass teaching absorption checks before they are treated as stable behavior.
- Memory and skill updates must be reviewed before merging.
- Regression should pass before any stable-layer prompt or template change is accepted.
