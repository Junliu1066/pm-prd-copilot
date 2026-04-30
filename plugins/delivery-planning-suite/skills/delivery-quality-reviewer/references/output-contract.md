# Delivery Quality Reviewer Output Contract

```yaml
delivery_quality_report:
  review_id: ""
  review_status: pass|warn|fail
  readiness_score: 0
  findings:
    - severity: pass|warn|fail
      area: phase_boundary|estimate|effect|risk|scope_backflow|testing|governance
      issue: ""
      evidence: ""
      required_fix: ""
  required_fixes:
    - ""
  pm_backflow_questions:
    - ""
  approved_for_development_planning: true
```
