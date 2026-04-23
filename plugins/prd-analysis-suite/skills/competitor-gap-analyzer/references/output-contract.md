# Competitor Gap Analyzer Output Contract

Use this compact structure when writing a formal competitor-gap artifact.

```yaml
competitor_map:
  - competitor: ""
    type: direct|adjacent|manual_workaround|platform_native
    target_user: ""
    core_loop: ""
    key_features: []
    pricing_signal: ""
    evidence_sources: []
common_solution_patterns:
  - pattern: ""
    competitors: []
user_complaint_themes:
  - theme: ""
    evidence_sources: []
    severity: low|medium|high
opportunity_gaps:
  - gap: ""
    user_need_link: ""
    why_it_matters: ""
advantage_hypotheses:
  - hypothesis: ""
    how_to_amplify: ""
    validation_needed: ""
advantage_amplification_plan:
  - advantage: ""
    linked_user_need: ""
    scenario_to_feed: ""
    validation_needed: ""
verification_checklist:
  - item: "Verify source date, product version, region, pricing, and feature availability before treating this as fact."
```
