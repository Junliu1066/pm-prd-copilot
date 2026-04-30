# Codex Development Plan Review Output Contract

```yaml
codex_development_review:
  artifact: "codex_development_review.md"
  required_sections:
    - "审核结论"
    - "审核对象"
    - "最优性评估"
    - "执行阻碍检查"
    - "任务包可执行性"
    - "依赖与权限检查"
    - "AI / Prompt / RAG / Memory 检查"
    - "Skill / MCP / Harness 检查"
    - "风险与回滚检查"
    - "发送前修改建议"
    - "人工确认清单"
    - "最终建议"
  decision_levels:
    - pass
    - warn
    - fail
  issue_schema:
    severity: "P0 | P1 | P2"
    issue: ""
    impact: ""
    required_action: ""
    owner: ""
  score_schema:
    readiness_score: "0-100"
    optimality_score: "0-100"
    blocker_count: 0
```
