# Agentic Delivery Orchestrator Output Contract

```yaml
codex_development_plan:
  artifact: "codex_development_plan.md"
  required_sections:
    - "文档目标"
    - "当前状态"
    - "总体结构"
    - "主开发流程"
    - "阶段总览"
    - "通用 Codex 执行框架"
    - "Skill / MCP / Harness 框架"
    - "AI / Prompt / RAG / Memory 框架"
    - "教学与记忆沉淀"
    - "人工确认点"
    - "验收与回归"
    - "阶段文档索引"
phase_codex_plans:
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
