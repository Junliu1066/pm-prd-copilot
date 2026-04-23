# Pain Needs Analyzer Output Contract

Use this compact structure when writing a formal pain-needs artifact.

```yaml
pain_needs_matrix:
  - user_group: ""
    pain: ""
    root_cause: ""
    desired_outcome: ""
    current_workaround: ""
    demand_type: functional|efficiency|confidence|habit|social
    severity: 1
    frequency: 1
    evidence_level: explicit|inferred|needs_research
root_cause_analysis:
  - theme: ""
    explanation: ""
time_cost_savings:
  - user_group: ""
    wasted_time_or_cost: ""
    potential_saving: ""
scenario_candidates:
  - scenario: ""
    user_group: ""
    value_hypothesis: ""
user_group_coverage_check:
  covered_groups: []
  missing_or_underexplored_groups: []
  narrowing_risk: ""
research_gaps:
  - gap: ""
    suggested_validation: ""
```
