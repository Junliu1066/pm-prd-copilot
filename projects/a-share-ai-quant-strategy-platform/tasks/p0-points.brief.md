# Task Brief: P0 Points

Task ID: `p0-points-001`
Branch: `codex/p0-points`
Owner: Codex worker / points owner
Status: `proposed`

## Goal

实现积分账户、每日登录赠送、充值占位、积分流水、报告解锁扣减和幂等防重复。

## Why

项目已将 C 端商业化表达收敛为积分制度。P0 必须先把积分账户和流水做成可审计、可回放、不可提现、不可收益化表达的基础能力。

## Input Docs

- `AGENTS.md`
- `03_internal_development_doc.md`
- `06_api_spec.md`
- `07_database_schema.md`
- `08_backend_engineering_spec.md`
- `09_task_breakdown.md`
- `10_test_plan.md`
- `12_codex_thread_governance.md`
- `14_file_boundary_matrix.md`

## Allowed Paths

- `backend/points/**`
- `backend/src/main/java/com/aquant/points/**`
- `backend/src/test/java/com/aquant/points/**`
- `tests/points/**`

## Forbidden Paths

- `01_prd.md`
- `02_prototype_layer.md`
- `prototype/html/**`
- `backend/marketdata/**`
- `backend/indicator/**`
- `backend/strategyengine/**`
- `backend/backtest/**`
- `backend/arena/**`
- `miniapp/**`
- `web/**`
- `admin/**`

## Locked Paths

- `06_api_spec.md`: integration owner
- `07_database_schema.md`: integration owner
- `08_backend_engineering_spec.md`: `codex/p0-spring-api`
- `db/migration/**`: integration owner
- `backend/common/**`: `codex/p0-spring-api`
- `backend/user/**`: `codex/p0-spring-api`

## Contract Touched

- API: no, unless CCR approved
- Database: no, unless CCR approved
- Permissions: yes
- Points: yes
- Quant run mode: no
- AI output: no
- Compliance wording: yes, only for points labels within allowed files

## Implementation Scope

- 创建或查询用户积分账户。
- 实现每日登录赠送 1 积分的幂等流水。
- 实现充值订单测试模式和积分入账占位。
- 实现报告解锁扣减和余额不足错误。
- 实现积分流水审计查询。

## Out Of Scope

- 不接真实微信支付。
- 不实现提现、返利、收益或投资回报。
- 不实现竞技场观察内容分成。
- 不修改用户模块公共登录逻辑，除非 owner 授权。

## Dependencies

- Upstream threads: `codex/p0-docs`, `codex/p0-spring-api`
- Downstream affected threads: `codex/p0-web-frontend`, `codex/p0-miniapp-frontend`, `codex/p0-admin`
- Required decisions: 真实支付后置为 P0.5/P1 审批项

## Exact Commands

- Required before work: `make check-all`
- Required before handoff: `THREAD=codex/p0-points make check-boundary`
- Required after backend exists: `cd backend && ./mvnw test`

## Exit Criteria

- 重复登录不重复赠送积分。
- 重复充值回调或重复请求不会重复入账。
- 积分不足返回 `POINTS_NOT_ENOUGH`。
- 所有流水有来源、业务单号、方向、数量、余额快照和审计时间。
- 不出现积分收益化、提现化表达。

## Failure Action

- 如果需要新增或调整表结构，停止并提交 CCR。
- 如果出现重复入账风险，优先修复幂等和唯一约束。
- 如果合规门禁失败，先修文案再继续实现。

## Delivery Summary Required

交付摘要必须包含完成内容、修改文件、验证结果、未完成事项、风险、需要主线集成处理、契约变更和文件边界结果。
