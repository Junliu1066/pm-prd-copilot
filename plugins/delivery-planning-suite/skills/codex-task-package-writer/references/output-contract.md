# Codex Task Package Writer Output Contract

```yaml
mode_selection:
  lightweight_development_document:
    use_when:
      - "ordinary development-ready PRD"
      - "single-phase Codex development document"
      - "user asks for a Codex development document without full governance"
    required_sections:
      - "development_scope"
      - "task_packages"
      - "allowed_write_paths"
      - "forbidden_write_paths"
      - "validation_commands"
      - "human_confirmation_points"
      - "minimal_fix_strategy"
      - "rollback_or_review"
    forbidden_by_default:
      - "new_skill_creation"
      - "mcp_integration"
      - "registry_harness_changes"
      - "full_governance_operating_system"
  full_supervised_package:
    use_when:
      - "user explicitly asks for semi-automated development"
      - "approved capability enablement or MCP integration exists"
      - "multi-agent governance is part of the requested scope"
codex_development_document:
  document_id: ""
  paired_prd_artifact: ""
  document_goal: "把 PRD 转成可交给 Codex 半自动开发"
  overall_structure: ""
  main_development_flow: ""
  mvp_development_goal: ""
  technical_delivery_path:
    phases:
      - ""
  ai_solution_when_needed: ""
  codex_task_packages_summary: ""
  human_supervision_gates:
    - ""
  harness_audit_validation:
    - ""
  learning_iteration: ""
  overload_escalation: ""
  multi_branch_execution_when_needed:
    activation_reason: ""
    branch_matrix_required: true
    branch_governance_cards_required: true
    branch_startup_packages_required: true
    ready_done_required: true
    contract_freeze_required: true
    scope_change_control_required: true
    evidence_required: true
    user_approval_conditions_required: true
codex_task_package_blueprint:
  blueprint_id: ""
  development_document_output:
    document_goal: "把 PRD 转成可交给 Codex 半自动开发"
    required_sections:
      lightweight:
        - "development_scope"
        - "codex_task_packages"
        - "allowed_write_paths"
        - "forbidden_write_paths"
        - "validation_commands"
        - "human_confirmation_points"
        - "minimal_fix_strategy"
      full_supervised:
        - "overall_structure"
        - "main_development_flow"
        - "steward_system"
        - "capability_enablement"
        - "skill_mcp_routing"
        - "technical_delivery_path"
        - "ai_solution_when_needed"
        - "codex_task_packages"
        - "human_supervision_gates"
        - "harness_audit_validation"
        - "learning_iteration"
        - "overload_escalation"
    output_artifacts:
      lightweight:
        - "codex_development_document"
        - "codex_task_packages"
        - "human_supervision_plan"
      full_supervised:
        - "capability_enablement_plan"
        - "skill_mcp_routing_plan"
        - "development_operating_system_plan"
        - "codex_task_package_blueprint"
        - "agentic_delivery_plan"
        - "codex_task_packages"
        - "human_supervision_plan"
        - "development_governance_report"
    must_not_write_to:
      - "development_log_only"
      - "unapproved_skill_update"
  task_types:
    - "capability_enablement"
    - "skill_creation"
    - "mcp_integration"
    - "registry_harness"
    - "product_development"
    - "qa_review"
    - "learning"
  capability_enablement_tasks:
    mode: "full_supervised_package_only"
    tasks:
      - task_id: ""
        goal: ""
        allowed_write_paths:
          - ""
        forbidden_write_paths:
          - ""
        validation_commands:
          - ""
        human_confirmation_points:
          - ""
        minimal_fix_strategy: ""
  skill_creation_tasks:
    mode: "proposal_only_and_full_supervised_package_only"
    tasks:
      - task_id: ""
        proposal_only: true
        human_approval_required: true
  mcp_integration_tasks:
    mode: "explicit_request_or_approved_plan_only"
    tasks:
      - task_id: ""
        source_trace_required: true
        human_verification_required: true
  registry_harness_tasks:
    mode: "explicit_request_or_approved_plan_only"
    tasks:
      - task_id: ""
        validation_commands:
          - ""
  product_development_tasks:
    - task_id: ""
      allowed_write_paths:
        - ""
      forbidden_write_paths:
        - ""
  branch_startup_packages:
    mode: "multi_branch_execution_only"
    packages:
      - branch_name: ""
        task_goal: ""
        context_summary: ""
        allowed_write_paths:
          - ""
        forbidden_write_paths:
          - ""
        dependency_branches:
          - ""
        related_files:
          - ""
        execution_steps:
          - ""
        validation_commands:
          - ""
        acceptance_criteria:
          - ""
        failure_handling: ""
        evidence_required:
          - ""
        ready_standard:
          - "goal_clear"
          - "scope_clear"
          - "forbidden_scope_clear"
          - "dependencies_clear"
          - "acceptance_clear"
          - "validation_clear"
          - "rollback_clear"
        done_standard:
          - "work_completed"
          - "self_check_completed"
          - "tests_completed"
          - "required_harness_completed"
          - "review_completed"
          - "evidence_complete"
          - "rollback_clear"
          - "closeout_generated"
  human_confirmation_points:
    - ""
  minimal_fix_strategy:
    - ""
  learning_route:
    project_cache: ""
    skill_update_proposal: ""
```
