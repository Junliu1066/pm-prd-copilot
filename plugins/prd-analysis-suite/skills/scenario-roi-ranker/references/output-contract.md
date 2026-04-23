# Scenario ROI Ranker Output Contract

Use this compact structure when writing a formal scenario ranking artifact.

```yaml
scenario_scores:
  - scenario: ""
    user_group: ""
    trigger: ""
    expected_outcome: ""
    scores:
      user_value: 1
      build_cost: 1
      frequency: 1
      time_savings: 1
      validation_speed: 1
      risk: 1
      differentiation: 1
    weighted_score: 0
    rationale: ""
    uncertainty: ""
    competitor_gap_link: ""
recommended_core_scenario:
  scenario: ""
  rationale: ""
backup_scenario:
  scenario: ""
  rationale: ""
avoid_for_now:
  - scenario: ""
    reason: ""
cost_return_summary:
  lowest_cost_highest_return_scenario: ""
  time_saved: ""
  speed_to_mvp: ""
competitor_gap_links:
  - scenario: ""
    gap_or_advantage: ""
approval_question: ""
```
