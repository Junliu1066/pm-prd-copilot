# Agentic Delivery Orchestrator Output Contract

```yaml
mode_selection:
  lightweight_codex_delivery:
    use_when:
      - "ordinary development-ready PRD"
      - "single-phase implementation plan"
      - "user asks for a Codex development document"
    required_artifacts:
      - "codex_development_document.md or codex_development_plan.md"
      - "codex_task_packages.md"
      - "human_supervision_plan.md"
      - "codex_development_review.md"
    forbidden_by_default:
      - "phase_1_codex_plan.md"
      - "phase_2_codex_plan.md"
      - "phase_3_codex_plan.md"
      - "final_codex_plan.md"
      - "development_governance_report.json"
      - "full Skill/MCP/Harness operating-system exposition"
  full_agentic_delivery:
    use_when:
      - "user explicitly asks for semi-automated agent delivery"
      - "user explicitly asks for phase 1 / 2 / 3 / final Codex plans"
      - "the project has approved development governance, capability enablement, or agent orchestration scope"
    required_artifacts:
      - "codex_development_plan.md"
      - "phase_1_codex_plan.md"
      - "phase_2_codex_plan.md"
      - "phase_3_codex_plan.md"
      - "final_codex_plan.md"
      - "codex_development_review.md"
      - "agentic_delivery_plan.md"
      - "codex_task_packages.md"
      - "human_supervision_plan.md"
      - "development_governance_report.json"
lightweight_codex_development_document:
  artifact: "codex_development_document.md or codex_development_plan.md"
  required_sections:
    - "文档目标"
    - "输入材料"
    - "开发范围"
    - "任务包"
    - "允许修改范围"
    - "禁止修改范围"
    - "人工确认点"
    - "验证命令"
    - "回滚方案"
    - "待决策项"
    - "审核结论"
codex_development_plan:
  mode: "full_agentic_delivery or explicitly requested multi-phase plan"
  artifact: "codex_development_plan.md"
  required_sections:
    - "文档目标"
    - "当前状态"
    - "总体结构"
    - "主开发流程"
    - "阶段总览"
    - "通用 Codex 执行框架"
    - "Codex 多分支工程执行操作系统"
    - "Skill / MCP / Harness 框架"
    - "AI / Prompt / RAG / Memory 框架"
    - "教学与记忆沉淀"
    - "人工确认点"
    - "验收与回归"
    - "阶段文档索引"
phase_codex_plans:
  mode: "full_agentic_delivery only, unless user explicitly asks for phase plans"
  phase_1_codex_plan:
    artifact: "phase_1_codex_plan.md"
    phase_name: "一期"
  phase_2_codex_plan:
    artifact: "phase_2_codex_plan.md"
    phase_name: "二期"
  phase_3_codex_plan:
    artifact: "phase_3_codex_plan.md"
    phase_name: "三期"
  final_codex_plan:
    artifact: "final_codex_plan.md"
    phase_name: "最终"
  each_phase_requires:
    - "阶段目标"
    - "本期输入"
    - "本期范围"
    - "总体框架"
    - "页面与交互"
    - "服务与数据"
    - "AI / Prompt / RAG / Memory"
    - "Skill / MCP 接入"
    - "Codex 任务包"
    - "人工确认点"
    - "GitHub / 发布流程"
    - "Harness / 审计 / 回归"
    - "教学与记忆沉淀"
    - "风险与回滚"
    - "验收标准"
    - "下一期衔接"
codex_development_review:
  artifact: "codex_development_review.md"
  required_before_send: true
  required_sections:
    - "审核结论"
    - "执行阻碍检查"
    - "最优性评估"
    - "任务包可执行性"
    - "人工确认清单"
    - "最终建议"
agentic_delivery_plan:
  mode: "full_agentic_delivery"
  plan_id: ""
  document_layering:
    product_package_may_include:
      - "feature_matrix"
      - "product_flow"
      - "prototype_preview"
    codex_development_must_be_separate: true
    forbidden_in_product_package:
      - "database_schema"
      - "api_contract"
      - "prompt_asset"
      - "model_route"
      - "github_process"
      - "codex_task_package"
  absorbed_inputs:
    prd: true
    feature_matrix: true
    product_flow: true
    prototype_preview: true
    capability_enablement_plan: true
    skill_mcp_routing_plan: true
    development_operating_system_plan: true
    codex_task_package_blueprint: true
  departments:
    - name: ""
      responsibility: ""
      reads:
        - ""
      writes:
        - ""
      forbidden:
        - ""
  development_order:
    - phase: ""
      goal: ""
      tasks:
        - ""
  multi_branch_execution:
    activation_reason: ""
    input_gate:
      status: "pass | partial | fail"
      missing_items:
        - ""
      blocked_branches:
        - ""
    branch_matrix:
      - branch_name: ""
        task_nodes:
          - ""
        version_scope: "v0.1 | v0.2 | later | out-of-scope"
        priority: "P0 | P1 | P2 | P3 | P4"
        impact_surface:
          - ""
        dependencies:
          - ""
        can_parallelize: false
        conflict_prediction: ""
        risk_level: "low | medium | high"
        in_current_version: false
    branch_governance_cards:
      - branch_name: ""
        goal: ""
        allowed_write_paths:
          - ""
        forbidden_write_paths:
          - ""
        responsible_stewards:
          - ""
        action_contract: ""
        artifact_contract: ""
        harness_gates:
          - ""
        review_gate: ""
        efficiency_check: ""
        evidence_required:
          - ""
        bug_route: ""
        failure_return_route: ""
        closeout_route: ""
        user_approval_conditions:
          - ""
    branch_startup_packages:
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
    contract_freeze:
      - contract: "api | database | ai_output | page_state | permission | config"
        status: "draft | frozen | changed | deprecated"
        dependent_branches:
          - ""
        change_policy: ""
    scope_change_control:
      request_format: "scope_change_request"
      allowed_decisions:
        - "expand_current_branch"
        - "create_new_branch"
        - "defer_to_next_version"
        - "user_decision_required"
    decision_log:
      - decision: ""
        reason: ""
        impact: ""
        alternatives:
          - ""
        final_choice: ""
        user_approval_required: false
    branch_state_machine:
      states:
        - "planned"
        - "ready"
        - "running"
        - "self_checked"
        - "reviewed"
        - "gate_passed"
        - "integration_pending"
        - "integration_passed"
        - "integration_failed"
        - "fix_required"
        - "closed"
        - "blocked"
    permission_boundaries:
      cannot_auto:
        - "merge_main"
        - "push_or_pr"
        - "delete_or_migrate_important_data"
        - "modify_stable_rules"
        - "create_long_lived_skill"
        - "create_long_lived_harness"
        - "publish_external_package"
        - "accept_high_risk_unresolved_issue"
        - "expand_version_scope"
        - "promote_candidate_to_stable"
        - "write_long_term_memory"
  capability_enablement:
    skill_reuse_decision: ""
    new_skill_route: ""
    mcp_route: ""
    harness_route: ""
  skill_mcp_routing:
    stage_routing: ""
    source_trace: ""
    fallback: ""
  governance_operating_system:
    chief_steward: ""
    sub_stewards: ""
    random_audit: ""
    efficiency_audit: ""
    teacher: ""
    preference_cache: ""
    skill_update_proposal: ""
codex_task_packages:
  - task_id: ""
    task_type: ""
    owner_department: ""
    goal: ""
    input_files:
      - ""
    allowed_write_paths:
      - ""
    forbidden_write_paths:
      - ""
    expected_outputs:
      - ""
    validation_commands:
      - ""
    human_confirmation_points:
      - ""
    minimal_fix_strategy: ""
human_supervision_plan:
  required_confirmations:
    - ""
development_governance_report:
  mode: "full_agentic_delivery"
  checks:
    - ""
  absorbed_operating_system:
    capability_enablement: true
    skill_mcp_routing: true
    governance: true
    codex_blueprint: true
  conflict_policy: ""
  feedback_learning_loop: ""
```
