# Task Brief: P0 Quant Engine

Task ID: `p0-quant-engine-001`
Branch: `codex/p0-quant-engine`
Owner: Codex worker / quant owner
Status: `proposed`

## Goal

实现 P0 研究和仿真所需的市场数据、指标、策略、回测和风控模块骨架，默认仅支持 `research_only` / `simulation_only`。

## Why

量化能力是平台的内容可信度来源，但本项目不能接实盘、不能展示 C 端买卖信号、不能引导跟单。该线程必须把 QuantDinger 参考逻辑转成研究和仿真引擎，而不是交易系统。

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

- `backend/marketdata/**`
- `backend/indicator/**`
- `backend/strategyengine/**`
- `backend/backtest/**`
- `backend/risk/**`
- `backend/src/main/java/com/aquant/marketdata/**`
- `backend/src/main/java/com/aquant/indicator/**`
- `backend/src/main/java/com/aquant/strategyengine/**`
- `backend/src/main/java/com/aquant/backtest/**`
- `backend/src/main/java/com/aquant/risk/**`
- `backend/src/test/java/com/aquant/marketdata/**`
- `backend/src/test/java/com/aquant/indicator/**`
- `backend/src/test/java/com/aquant/strategyengine/**`
- `backend/src/test/java/com/aquant/backtest/**`
- `backend/src/test/java/com/aquant/risk/**`
- `tests/quant/**`

## Forbidden Paths

- `01_prd.md`
- `prototype/html/**`
- `backend/points/**`
- `backend/admin/**`
- `backend/arena/**`
- `miniapp/**`
- `web/**`
- `admin/**`

## Locked Paths

- `06_api_spec.md`: integration owner
- `07_database_schema.md`: integration owner
- `08_backend_engineering_spec.md`: `codex/p0-spring-api`
- `db/migration/**`: integration owner

## Contract Touched

- API: no, unless CCR approved
- Database: no, unless CCR approved
- Permissions: no
- Points: no
- Quant run mode: yes
- AI output: no
- Compliance wording: yes, only for risk labels within allowed files

## Implementation Scope

- 建立行情快照、指标计算、回测任务、绩效指标、风险评估的模块骨架。
- 明确交易成本、滑点、数据切片和未来函数防护的接口。
- 支持回测结果落库或内存 mock，具体以已批准 schema 为准。
- 所有执行模式默认标记为 `research_only` 或 `simulation_only`。

## Out Of Scope

- 不接券商账户。
- 不接实盘下单。
- 不输出 C 端实时买卖信号。
- 不展示持仓。
- 不实现跟单、带单或代客操作。
- 不新增数据库结构，除非 CCR 批准。

## Dependencies

- Upstream threads: `codex/p0-docs`, `codex/p0-spring-api`
- Downstream affected threads: `codex/p0-web-frontend`, `codex/p0-miniapp-frontend`, `codex/p1-arena`, `codex/ai-compliance`
- Required decisions: 外部行情源和 QuantDinger 适配范围需要单独确认

## Exact Commands

- Required before work: `make check-all`
- Required before handoff: `THREAD=codex/p0-quant-engine make check-boundary`
- Required after backend exists: `cd backend && ./mvnw test`

## Exit Criteria

- 所有量化入口都有执行模式字段或等价限制。
- 单测覆盖基础指标、回测状态、风险计算和异常数据。
- 不出现实盘、券商账户、自动下单、跟单、C 端买卖信号能力。
- 与 `06_api_spec.md` 和 `07_database_schema.md` 保持一致。

## Failure Action

- 如果发现必须修改 API、DB 或量化边界，停止并提交 CCR。
- 如果出现合规高风险能力，立即移除并运行 `make check-compliance`。
- 如果测试依赖外部数据源，改用 mock 或记录阻塞，不私自接入新数据源。

## Delivery Summary Required

交付摘要必须包含完成内容、修改文件、验证结果、未完成事项、风险、需要主线集成处理、契约变更和文件边界结果。
