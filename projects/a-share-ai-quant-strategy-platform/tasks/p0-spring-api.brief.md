# Task Brief: P0 Spring API

Task ID: `p0-spring-api-001`
Branch: `codex/p0-spring-api`
Owner: Codex worker / backend owner
Status: `proposed`

## Goal

创建 Spring Boot 3.x 后端基础工程和公共 API 能力，让后续积分、量化、后台线程可以复用统一响应体、认证、权限、异常、审计、OpenAPI 和测试框架。

## Why

后端公共层是 P0 其他工程线程的前置依赖。如果公共响应、错误码、权限、审计和幂等规则不先冻结，后续模块会各自发明接口形态，导致联调和合并成本失控。

## Input Docs

- `AGENTS.md`
- `03_internal_development_doc.md`
- `06_api_spec.md`
- `07_database_schema.md`
- `08_backend_engineering_spec.md`
- `09_task_breakdown.md`
- `10_test_plan.md`
- `11_local_dev_runbook.md`
- `12_codex_thread_governance.md`
- `14_file_boundary_matrix.md`

## Allowed Paths

- `backend/pom.xml`
- `backend/mvnw`
- `backend/mvnw.cmd`
- `backend/.mvn/**`
- `backend/common/**`
- `backend/auth/**`
- `backend/user/**`
- `backend/config/**`
- `backend/src/main/java/com/aquant/AQuantApplication.java`
- `backend/src/main/java/com/aquant/common/**`
- `backend/src/main/java/com/aquant/auth/**`
- `backend/src/main/java/com/aquant/user/**`
- `backend/src/main/resources/application*.yml`
- `backend/src/test/java/com/aquant/common/**`
- `backend/src/test/java/com/aquant/auth/**`
- `backend/src/test/java/com/aquant/user/**`
- `api/**`
- `tests/backend/**`
- `08_backend_engineering_spec.md`

## Forbidden Paths

- `01_prd.md`
- `02_prototype_layer.md`
- `prototype/html/**`
- `miniapp/**`
- `web/**`
- `admin/**`
- `backend/points/**`
- `backend/marketdata/**`
- `backend/indicator/**`
- `backend/strategyengine/**`
- `backend/backtest/**`
- `backend/arena/**`

## Locked Paths

- `06_api_spec.md`: integration owner
- `07_database_schema.md`: integration owner
- `db/migration/**`: integration owner
- `10_test_plan.md`: QA owner

## Contract Touched

- API: no, unless CCR approved
- Database: no, unless CCR approved
- Permissions: yes
- Points: no
- Quant run mode: no
- AI output: no
- Compliance wording: no

## Implementation Scope

- 建立 Spring Boot 3.x 工程骨架。
- 建立统一响应体、错误码、异常处理、请求追踪 ID。
- 建立 Spring Security 基础配置和 mock/local 登录能力。
- 建立审计 AOP、幂等拦截器占位、OpenAPI 配置。
- 建立健康检查和基础集成测试。

## Out Of Scope

- 不实现积分业务。
- 不实现量化引擎。
- 不实现竞技场。
- 不接真实微信支付。
- 不接外部行情源。
- 不新增 C 端高风险能力。

## Dependencies

- Upstream threads: `codex/p0-docs`
- Downstream affected threads: `codex/p0-points`, `codex/p0-quant-engine`, `codex/p0-admin`, `codex/p0-web-frontend`, `codex/p0-miniapp-frontend`
- Required decisions: Java 版本、构建工具、数据访问框架按 `08_backend_engineering_spec.md` 执行

## Exact Commands

- Required before work: `make check-all`
- Required before handoff: `THREAD=codex/p0-spring-api make check-boundary`
- Required after backend exists: `cd backend && ./mvnw test`

## Exit Criteria

- 后端工程可以本地启动。
- `./mvnw test` 通过。
- OpenAPI 页面可访问。
- 统一错误码和响应结构符合 `06_api_spec.md`。
- 未直接修改 API / DB 契约文件。

## Failure Action

- 如果需要改 API 或 DB 契约，停止实现并提交 `18_contract_change_request_template.md`。
- 如果 boundary gate 失败，撤出越界文件或请求 owner 授权。
- 如果后端测试失败，只修本线程授权路径内的问题。

## Delivery Summary Required

交付摘要必须包含完成内容、修改文件、验证结果、未完成事项、风险、需要主线集成处理、契约变更和文件边界结果。
