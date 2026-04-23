# Teaching Log

This log captures user coaching. The teacher role classifies each lesson and proposes how the system should absorb it. Lessons are not stable rules until accepted.

## 2026-04-23 - Do not narrow user groups too early

### User Feedback
Do not stop at the weight-loss user group. First consider all user groups that could become target users, then analyze their pain points and needs, then connect them to concrete scenarios.

### Lesson Type
general_pm_principle

### Proposed Rule
Before narrowing target users, `user-universe-mapper` must enumerate the broad potential user pool and explain why each group may or may not be prioritized.

### Affected Components
- user-universe-mapper
- pain-needs-analyzer
- scenario-roi-ranker
- prd-quality-reviewer

### Status
accepted

## 2026-04-23 - Core scenario should be judged by minimum cost and maximum return

### User Feedback
The core scenario should be selected by judging which scenario has the minimum cost and maximum return. For the fitness app case, group interval timing is likely the core scenario.

### Lesson Type
general_pm_principle

### Proposed Rule
`scenario-roi-ranker` must rank scenarios by user value, usage frequency, implementation cost, time saved, and speed to MVP.

### Affected Components
- scenario-roi-ranker
- mvp-scope-decider
- prd-quality-reviewer

### Status
accepted

## 2026-04-23 - Competitor analysis must find advantage, not list features

### User Feedback
Do not just list competitors and features. Investigate how competitors solve the problem, what our advantage is, and how to expand that advantage.

### Lesson Type
general_pm_principle

### Proposed Rule
`competitor-gap-analyzer` must output competitor approach, user complaints or gaps, our possible advantage, and how to amplify that advantage.

### Affected Components
- competitor-gap-analyzer
- scenario-roi-ranker
- mvp-scope-decider
- prd-draft-writer

### Status
accepted
