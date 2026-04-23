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
approval_question: ""
```
