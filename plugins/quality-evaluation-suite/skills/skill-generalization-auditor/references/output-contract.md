# Skill Generalization Auditor Output Contract

Use this compact structure when writing a formal generalization audit artifact.

```yaml
audit_scope:
  changed_skills:
    - skill_id: ""
      path: ""
  checked_proposals:
    - proposal_id: ""
  evaluation_cases_used:
    - case_id: ""
findings:
  - finding_id: ""
    severity: pass|warn|fail
    leakage_type: project_preference|user_preference|domain_default|style_default|market_default|platform_default|unclear_scope
    evidence: ""
    affected_file: ""
    recommended_route: project_cache|user_preference|generic_skill|open_lesson|reject
routing_decisions:
  - item: ""
    route: project_cache|user_preference|generic_skill|open_lesson|reject
    reason: ""
generic_rules_allowed:
  - rule: ""
    abstraction_level: ""
project_specific_items:
  - item: ""
    project_scope: ""
recommended_fixes:
  - fix: ""
    target: ""
    minimum_change: true
validation_plan:
  - check: ""
```
