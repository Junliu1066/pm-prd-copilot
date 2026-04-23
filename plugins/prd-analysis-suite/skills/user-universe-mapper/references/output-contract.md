# User Universe Mapper Output Contract

Use this compact structure when writing a formal user-universe artifact.

```yaml
user_universe_table:
  - user_group: ""
    trigger_situation: ""
    job_to_be_done: ""
    pain_intensity: 1
    frequency: 1
    current_solution: ""
    decision_power: high|medium|low
    acquisition_path: ""
    product_fit_risk: ""
    evidence_level: explicit|inferred|needs_research
segment_clusters:
  - cluster: ""
    included_groups: []
    rationale: ""
priority_candidates:
  - user_group: ""
    why_priority: ""
discarded_or_low_priority_segments:
  - user_group: ""
    reason: ""
narrowing_rationale:
  selected_groups: []
  deferred_groups: []
  rationale: ""
research_questions:
  - question: ""
    target_group: ""
```
