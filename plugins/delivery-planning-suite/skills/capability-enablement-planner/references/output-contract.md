# Capability Enablement Planner Output Contract

```yaml
capability_enablement_plan:
  plan_id: ""
  mode: "no_change|reuse_existing|proposal_needed"
  capability_gaps:
    - gap: ""
      impact_on_development: ""
      severity: "low|medium|high"
  skill_reuse_decision:
    - need: ""
      decision: "reuse_existing|update_existing|manual|defer|proposal_for_new_skill"
      target_skill: ""
      reason: ""
      human_approval_required: true
  new_skill_candidates:
    mode: "include_only_when_reuse_manual_or_defer_is_insufficient"
    candidates:
      - skill_name: ""
        purpose: ""
        owner_steward: ""
        detachable: true
        approval_status: "proposal_only"
  mcp_candidates:
    mode: "include_only_when_external_data_or_action_is_needed"
    candidates:
      - mcp_name: ""
        purpose: ""
        allowed_outputs:
          - ""
        forbidden_outputs:
          - ""
        source_trace_required: true
        human_verification_required: true
  harness_requirements:
    mode: "include_only_for_concrete_failure_risks"
    checks:
      - check_name: ""
        guards: ""
        failure_mode: ""
  memory_learning_route:
    project_preferences: ""
    generic_lessons: ""
    rejected_or_unclear_items: ""
  human_approval_required:
    - decision: ""
      reason: ""
```
