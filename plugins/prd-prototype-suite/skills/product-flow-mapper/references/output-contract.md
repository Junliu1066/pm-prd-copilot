# Product Flow Mapper Output Contract

Use this compact structure when writing a formal product-flow artifact.

```yaml
flow_id: ""
flow_name: ""
target_user: ""
scenario: ""
trigger: ""
entry_point: ""
primary_path:
  - step_id: ""
    user_action: ""
    system_response: ""
    screen_or_state: ""
    next_step: ""
decision_points:
  - condition: ""
    branch_a: ""
    branch_b: ""
system_feedback:
  - event: ""
    feedback: ""
edge_cases:
  - case: ""
    expected_behavior: ""
diagram:
  format: mermaid|html_svg
  content: ""
prototype_feedback_backflow:
  - feedback: ""
    classification: business_logic|page_structure|copy|visual_style|exception_state
    flow_change_required: true
    update_summary: ""
approval_questions:
  - question: ""
```
