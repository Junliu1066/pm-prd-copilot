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

- `00_value_gate.json`
- `00_value_gate.md`
- `00_value_gate_prd_input.json`
- `00_value_gate_owner_decision.md`
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

## Product value gate

Before PRD generation, run the product value gate as the independent front door:

```bash
python3 pm-prd-copilot/scripts/run_pipeline.py --base-dir . --project demo-project --stage value_gate --mode rule
```

It writes:

- `projects/<project>/00_value_gate.json`
- `projects/<project>/00_value_gate.md`
- `projects/<project>/00_value_gate_prd_input.json`
- `projects/<project>/00_value_gate_owner_decision.md`
- `projects/<project>/00_value_gate_evidence_snapshot.json`

V1.0 output is an evidence-driven Product Value Gate Agent result, not the PRD itself. It first shows the concrete evidence table, explains what each item can and cannot prove, then judges whether the evidence is sufficient for the proposed path. It then answers whether the opportunity is worth doing and adds an operating decision layer that states how much to invest, how long to validate, what minimum result must be reached, when to stop, and when to upgrade. It splits the output for two readers: `00_value_gate_prd_input.json` is the clean machine-readable input for the PRD module, while `00_value_gate_owner_decision.md` is the business decision report for the project owner.

The agent must keep an `evidence_ledger`. Source-backed facts can enter `safe_facts_for_prd`; unsupported claims must stay in assumptions or blocked claims. User-provided facts such as MVP experiments or paid customer signals are allowed as strong business evidence, but they must be marked as user-provided and cannot be presented as external verification.

`business_worth_verdict` is the business-worth decision layer. `worth_doing` can enter its matching PRD path, `worth_testing` can only enter MVP/client-project validation paths, `worth_researching` routes to research completion, `not_worth_doing` stops formal PRD generation, and `blocked` means redline blocked. `decision_gate = A_ENTER_PRD` now only means full PRD; service MVP or low-cost validation must route to `B_LOW_COST_MVP`.

`evidence_decision_basis` is the proof layer. Every decision-driving evidence item must state its source, proof link, fetch status, strength, what it proves, what it does not prove, and how it affects the verdict. For commercial opportunities, the owner report must separate market-shift evidence, pricing-anchor evidence, competitor-productization evidence, and user-provided business facts. `evidence_to_verdict_reasoning` connects the proof table to the final business worth verdict. `evidence_sufficiency_gate` is the hard gate: it states whether evidence is sufficient for full PRD, MVP, client project, internal efficiency, research, stop, or redline block. Unsupported or unsourced claims cannot enter the conclusion.

V1.0 also adds the commercial hardening layer:

- `industry_redline_rule_pack`: lightweight industry/platform risk rules and unresolved confirmations.
- `lightweight_profit_model`: true-profit formula, known inputs, unknown inputs, cycle dimensions, and scaling blockers.
- `rejudgment_package`: what B/C/D/E paths must collect before returning to the value gate.
- `evidence_archive_policy` and `00_value_gate_evidence_snapshot.json`: source metadata and excerpts for traceability. Full HTML, logged-in pages, unauthorized data, and sensitive personal data are not saved.

V1.1 adds the decision-hardening gates required before the output can be used as a business decision aid:

- `evidence_grade_gate`: checks whether evidence grade is enough for the current route and why it is not enough for full PRD.
- `roi_decision_model`: keeps ROI unproven until price, acquisition cost, delivery effort, tool cost, maintenance cost, and repeat-purchase evidence exist.
- `contextual_redline_filter`: narrows redline checks to the project context, while keeping conditional high-risk industries visible for confirmation.
- `route_package_completeness_gate`: checks whether the selected A/B/C/D/E/F/G handoff package has the minimum fields needed by the next module.

V1.2 adds the commercial sufficiency layer needed before the report can support investment decisions:

- `verified_evidence_gate`: separates user-claimed strong evidence from attachment/internal-record verified evidence. User-provided MVP or payment claims can support MVP validation, but cannot be treated as independently verified S-level evidence until supporting records exist.
- `value_realization_timeline`: records when value should appear, when payment/retest/repurchase should be observed, and which unknown cycles block scaling.
- `output_boundary_gate`: prevents the value gate from silently becoming a full PRD, feature list, UI plan, technical architecture, or delivery plan.
- Deeper B/C/D/E route packages: client project validation includes acceptance/reuse review, internal efficiency includes ROI input requirements, and research completion includes interview/payment/risk research tasks.

V1.3 adds the two P0 decision inputs needed before the owner can judge whether the opportunity is worth real investment:

- `evidence_verification_intake`: the intake checklist for payment proof, customer records, MVP experiment records, delivery acceptance, and repurchase/referral evidence. It explains what evidence can upgrade `S_claimed` into `S_verified`.
- `roi_input_table`: the concrete ROI input table for price, acquisition cost, delivery hours, human review cost, tool/model cost, maintenance cost, and repurchase signals. If these inputs are missing, the report must not claim high ROI.
- `payment_evidence_verification`: separates claimed payment layer from verified payment layer, so user-provided “已买单” can support MVP validation without being treated as independently verified S-level evidence.
- `value_quality_scorecard`: checks whether value is continuous, high-margin, lightweight, standardized, repeatable, replicable, capability-building, and defensible before allowing full PRD or productization claims.
- `resource_advantage_matrix`: checks whether the team has customer resources, acquisition channels, industry knowledge, technical capability, delivery capability, case proof, cost advantage, compliance capability, and team capacity.
- `acquisition_decision_table`: turns acquisition into a hard table covering first users, reach method, trust basis, CAC, and repurchase/LTV signals.
- `competitor_benchmark_table`: lists China and international competitor references with source links. Competitors can prove the market and product pattern exist, but cannot prove this project has profit, high ROI, acquisition efficiency, repeat purchase, or productization value.
- `output_boundary_gate`: keeps the value gate in its lane. It can recommend the next validation path for one idea, but it must not rank this idea against all other projects, decide company-level resource priority, or replace a separate project prioritization module.
- `value_judgment.primary_value_type` and `business_result_definition`: separate the main value from secondary value and convert business results into measurable, falsifiable outcomes. For GEO, external service/project revenue is primary; internal Agent efficiency is only a delivery-cost lever.
- `resource_advantage_matrix.claimed/verified/unverified`: separates claimed resource advantages from verified advantages. Unverified “why us” signals cannot justify scaling or full PRD.
- `rejudgment_package.required_validation_records`: records what B/C/D/E routes must collect before returning to the value gate, so MVP/client/internal/research paths remain closed loops rather than one-off reports.

V1.5 closes the handoff gap between a strong report and a usable next step:

- `mvp_input_package` must be executable for the selected route. For GEO, it includes the free diagnosis entry, paid diagnosis report, metric dashboard, recheck mechanism, optimization suggestions, service conversion path, execution record template, and concrete success/failure criteria.
- `evidence_verification_intake` now includes quote/price, delivery-time, and acquisition-source slots in addition to payment, customer, MVP, delivery, and repurchase evidence. Each slot states what it can upgrade and what it cannot prove.
- `route_package_completeness_gate.specificity_checks` flags generic MVP handoff packages. GEO handoff packages must contain concrete conversion, delivery, recheck, repurchase, and data-loop terms before they are considered complete.

V2.0 adds the first execution-oriented Evidence Research Agent layer without creating a new skill or harness:

- `source_quality_gate`: counts user-provided, external, internal, inferred, competitor, reachable, and non-success sources, then states whether the evidence can support full PRD, MVP only, research, stop, or redline block.
- `evidence_research_agent`: turns missing evidence into concrete research tracks such as customer/payment verification, ROI inputs, competitor productization, platform-rule risk, acquisition channel validation, and market-shift monitoring.
- `attachment_verification_plan`: converts the verification intake slots into materials to request, manual review method, upgrade effect, storage rule, and “no auto verification” boundary.
- `rejudgment_execution_plan`: tells the next path what records to collect, when to return for value-gate rejudgment, what can trigger upgrade, and what triggers stop or downgrade.

V2.0 still does not save raw HTML, does not verify private attachments automatically, does not generate full PRD, and does not upgrade claimed evidence to verified evidence without user-provided review material.

V2.1 makes the research layer executable without turning it into a new automation:

- `research_execution_queue`: converts every `evidence_research_agent.research_track` into a task with priority, source request, accepted evidence, acceptance criteria, output fields, done definition, downgrade rule, and whether owner material is required.
- P0 tasks are reserved for payment/customer verification and ROI operating inputs, because they determine whether the project can ever move beyond service MVP.
- Research tasks do not write repo files by default. Their outputs are only value-gate rejudgment inputs, not PRD approval, stable rules, or verified evidence by themselves.
- The task output contract rejects unsourced market numbers, untraceable payment claims, competitor-only ROI claims, fake external verification, and automatic `S_verified` upgrades.

V2.2-V2.5 closes the commercial loop without adding a new skill or harness:

- `00_value_gate_materials.json`: project-owned material intake file. It has fixed slots for payment/contract, customer records, MVP experiments, delivery acceptance, repurchase/referral, quote/price, delivery time, and acquisition source. Material presence does not equal verification; default status is `missing` or `submitted_pending_review`.
- `material_intake_summary`, `material_to_evidence_mapping`, and `rejudgment_readiness_gate`: explain which materials exist, what they can prove, what they cannot prove, and whether the project is ready for service-MVP, ROI, or productization rejudgment.
- `external_research_results`, `source_quality_scorecard`, `competitor_pricing_evidence`, and `platform_rule_evidence`: turn the research queue into a traceable evidence table with source title, URL, capture date, excerpt, proof boundary, credibility, and decision impact. External evidence can prove market, competitor, trend, and platform-rule context; it cannot prove this project’s profit, ROI, acquisition, repeat purchase, or productization by itself.
- `verified_evidence_assessment` and `s_claimed_to_s_verified_gate`: separate user-claimed strong evidence from reviewed evidence. `S_claimed` can support service MVP/customer validation, but `S_verified` requires reviewed materials such as payment/contract, customer records, MVP/delivery records, quote, delivery time, or repeat-purchase evidence.
- `real_profit_calculation`, `roi_scenario_analysis`, and `investment_decision_gate`: keep ROI blocked until price, acquisition cost, delivery hours, human review cost, tool/model cost, maintenance cost, and repeat/renewal signals are available. Investment decisions remain value-gate rejudgment inputs and require owner approval before productization or full PRD.

V2.2-V2.5 still does not read private attachments automatically, save raw HTML, generate full PRD, modify stable rules, create skill/harness, or write long-term memory.

By default the value gate stays deterministic and does not use the network. For real project evidence review, pass `--fetch-evidence` to fetch public source URLs for reachability, HTTP status, page title, and a short excerpt:

```bash
python3 pm-prd-copilot/scripts/generate_value_gate.py --base-dir . --project demo-project --mode rule --fetch-evidence
```

This does not save raw snapshots and does not automatically upgrade a claim into a business conclusion.

`operating_decision_model` is the operating layer. It records the recommended play, investment ceiling, validation window, minimum revenue signal, minimum profit conditions, delivery and acquisition thresholds, upgrade conditions, stop/downgrade conditions, and scaling blockers. If the input does not provide evidence for price, cost, delivery hours, CAC, or similar operating numbers, the output must say `待确认` instead of inventing values.

Only `decision_gate = A_ENTER_PRD`, `allowed_prd_type = 完整 PRD`, `evidence_sufficiency_gate.overall_status = sufficient_for_full_prd`, and `execution_status = ready_for_prd` can enter formal full PRD generation. Other decisions route to their own path:

- `B_LOW_COST_MVP`: low-cost MVP validation.
- `C_CLIENT_PROJECT_VALIDATION`: client project validation.
- `D_INTERNAL_EFFICIENCY`: internal efficiency plan.
- `E_RESEARCH_REQUIRED`: research completion.
- `F_NOT_RECOMMENDED`: stop with reason.
- `G_BLOCKED_BY_REDLINE`: redline block.

Formal PRD generation checks `decision_gate`, `allowed_prd_type`, `evidence_sufficiency_gate`, `value_judgment_passed`, `execution_status`, `can_enter_full_prd`, `blocked_reasons`, human confirmation, and input package quality. Fast draft can bypass this only when explicitly requested:

```bash
python3 pm-prd-copilot/scripts/run_pipeline.py --base-dir . --project demo-project --stage prd --mode rule --fast-draft
```

Fast draft is a labeled draft path only. Its manifest records `value_gate_bypassed: true`; it must not replace formal approval-gated delivery.

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
