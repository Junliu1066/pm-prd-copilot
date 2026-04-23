# MVP Scope Decider Output Contract

Use this compact structure when writing a formal MVP scope artifact.

```yaml
core_scenario:
  name: ""
  target_user: ""
  success_signal: ""
mvp_loop:
  trigger: ""
  input: ""
  processing: ""
  output: ""
  feedback: ""
  repeat_use: ""
scope_table:
  - item: ""
    bucket: MVP|V1|Later|Non-goal
    user_value: ""
    build_cost: low|medium|high
    dependency: ""
    validation_signal: ""
    rationale: ""
deferred_items:
  - item: ""
    reason: ""
non_goals:
  - item: ""
    reason: ""
roi_basis:
  minimum_cost_reasoning: ""
  maximum_return_reasoning: ""
  time_saved: ""
  speed_to_mvp: ""
competitor_gap_basis:
  linked_gap_or_advantage: ""
  why_it_belongs_or_does_not_belong_in_mvp: ""
approval_question: ""
```
