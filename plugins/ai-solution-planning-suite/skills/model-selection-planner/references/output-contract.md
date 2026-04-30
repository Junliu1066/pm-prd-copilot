# Model Selection Planner Output Contract

```yaml
model_selection_plan:
  plan_id: ""
  docs_verification_required: true
  market_scope:
    default_market: ""
    included_provider_types:
      - "local_accessible"
      - "global_provider"
    excluded_provider_types:
      - ""
  official_source_snapshot:
    collected_at: ""
    sources:
      - provider: ""
        url: ""
        facts_used:
          - ""
        human_verification_required: true
  candidate_model_pool:
    - provider: ""
      model_id: ""
      role_fit:
        - ""
      context_window: ""
      input_price_per_1m: ""
      output_price_per_1m: ""
      strengths:
        - ""
      risks:
        - ""
      source_url: ""
  model_comparison_matrix:
    - task: ""
      candidates:
        - model_id: ""
          doc_screening_score: ""
          measured_score: "not_measured"
          reason: ""
          benchmark_required: true
  benchmark_plan:
    - benchmark_id: ""
      task: ""
      sample_count: 0
      pass_criteria: ""
      measured: false
      human_review_required: true
  benchmark_status:
    status: "not_run|partial|complete"
    reason: ""
  shortlist_recommendations:
    - recommendation_type: "primary|low_cost_fallback|quality_first|future_phase"
      model_id: ""
      provider: ""
      use_for:
        - ""
      why: ""
      conditions:
        - ""
  routing_rules:
    - rule: ""
  fallback_strategy:
    - trigger: ""
      fallback: ""
  open_decisions:
    - ""
```
