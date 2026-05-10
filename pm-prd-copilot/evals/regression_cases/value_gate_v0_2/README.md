# Product Value Gate V1.0 Regression Cases

V1.0 verifies that the value gate is no longer only a coarse `A/B/C/D/E/F/G` classifier. It must first show concrete evidence, explain what each item can and cannot prove, record fetch status for external public sources, then judge whether the evidence is sufficient for full PRD, MVP, client project, internal efficiency, research, stop, or redline block. It then connects the evidence to the worth verdict and adds an operating decision layer for investment ceiling, validation window, minimum result, upgrade conditions, and stop conditions.

Required V1.0 sections:

- `agent`
- `business_worth_verdict`
- `evidence_sufficiency_gate`
- `industry_redline_rule_pack`
- `lightweight_profit_model`
- `rejudgment_package`
- `evidence_archive_policy`
- `allowed_prd_type`
- `evidence_decision_basis`
- `evidence_to_verdict_reasoning`
- `operating_decision_model`
- `evidence_ledger`
- `safe_facts_for_prd`
- `assumptions_for_prd`
- `blocked_claims`
- `hard_gate_scorecard`
- `path_recommendation`
- `decision_questions`
- `value_object_detail`
- `measurability_judgment`
- `attribution_judgment`
- `value_quality_judgment`
- `true_profit_judgment`
- `resource_fit_judgment`
- `acquisition_judgment`
- `project_to_product_judgment`
- `low_cost_mvp_judgment`
- `counter_evidence`
- `input_package_quality_gate`
- `execution_status`
- `validation_state`
- route-specific input packages

Key acceptance cases:

| Case | Expected decision | Extra V1.0 requirement |
|---|---|---|
| GEO with MVP experiment and paid peer signal | `B_LOW_COST_MVP` | Shows proof table with fetch status, states what MVP/payment/platform evidence can and cannot prove, marks evidence sufficiency as `sufficient_for_mvp`, recommends 2-4 week service MVP PRD, defers full SaaS PRD, keeps price/cost/delivery numbers as `待确认`, records user-provided plus external source evidence, includes platform-rule redline review, true-profit unknowns, and rejudgment materials. |
| GEO idea without payment proof | `B_LOW_COST_MVP` or `E_RESEARCH_REQUIRED` | Must not be promoted to full PRD. |
| Strong custom client project | `C_CLIENT_PROJECT_VALIDATION` | Must separate project value from product value. |
| Internal cost reduction | `D_INTERNAL_EFFICIENCY` | Must not be packaged as external product by default. |
| Weak profit and heavy delivery | `F_NOT_RECOMMENDED` | Must provide stop reasons and counter-evidence. |
| Financial return promise or medical diagnosis | `G_BLOCKED_BY_REDLINE` | Must block full PRD. |

V1.0 remains a lightweight agent protocol over the existing generator. It records evidence sources, optional public-source fetch status, evidence sufficiency, evidence-to-verdict reasoning, output boundaries, operating decision constraints, redline review, lightweight true-profit unknowns, rejudgment requirements, and evidence snapshot metadata. It does not perform complex financial modeling, create new skills, or create new harnesses.
