# Capability Enablement Planner Output Contract

```yaml
capability_enablement_plan:
  plan_id: ""
  capability_gaps:
    - gap: ""
      impact_on_development: ""
      severity: "low|medium|high"
  skill_reuse_decision:
    - need: ""
      decision: "reuse_existing|update_existing|create_new|manual"
      target_skill: ""
      reason: ""
      human_approval_required: true
  new_skill_candidates:
    - skill_name: ""
      purpose: ""
      owner_steward: ""
      detachable: true
      approval_status: "proposal_only"
  mcp_candidates:
    - mcp_name: ""
      purpose: ""
      allowed_outputs:
        - ""
      forbidden_outputs:
        - ""
      source_trace_required: true
      human_verification_required: true
  harness_requirements:
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
