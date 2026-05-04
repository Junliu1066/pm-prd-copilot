# Development Governance Orchestrator Output Contract

```yaml
development_operating_system_plan:
  plan_id: ""
  mode: "lightweight_governance_note|full_governance_operating_system"
  chief_steward:
    mode: "full_governance_operating_system"
    responsibilities:
      - ""
  sub_stewards:
    mode: "full_governance_operating_system"
    stewards:
      - steward: ""
        owns:
          - ""
        capacity_limit: ""
  random_audit:
    mode: "full_governance_operating_system_or_explicit_audit_request"
    audit_scope:
      - ""
    report_to:
      - ""
  efficiency_audit:
    mode: "full_governance_operating_system_or_explicit_efficiency_request"
    metrics:
      - ""
    optimization_route: ""
  teacher:
    mode: "include_when_feedback_learning_is_requested"
    captures:
      - ""
    cannot:
      - ""
  preference_cache:
    mode: "include_when_project_preferences_are_in_scope"
    project_specific_route: ""
    clear_reset_policy: ""
  skill_update_proposal:
    mode: "proposal_only"
    proposal_route: ""
    human_approval_required: true
    generalization_check_required: true
  harness:
    mode: "reuse_existing_checks_first"
    required_checks:
      - ""
  escalation:
    - trigger: ""
      action: ""
lightweight_governance_note:
  required_sections:
    - "human_approval_points"
    - "validation_checks"
    - "rollback_or_escalation"
    - "learning_persistence_decision"
```
