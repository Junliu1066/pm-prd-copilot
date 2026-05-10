# Agent Instructions

本文件是本项目的项目级 Agent 指令。任何 Codex 线程进入本目录后，必须先读本文件，再决定是否可以修改文件。

## 1. 必读顺序

执行任何任务前按顺序读取：

1. `AGENTS.md`
2. `03_internal_development_doc.md`
3. `06_api_spec.md`
4. `07_database_schema.md`
5. `08_backend_engineering_spec.md`
6. `09_task_breakdown.md`
7. `10_test_plan.md`
8. `12_codex_thread_governance.md`
9. 与当前任务直接相关的原型、代码或补充文档

如果任务涉及 Codex 分线程，还必须读取：

- `13_task_brief_template.md`
- `14_file_boundary_matrix.md`
- `15_failure_handling_protocol.md`
- `16_codex_execution_runbook.md`
- `17_sdd_engineering_lessons.md`
- `automation/thread_registry.md`
- `18_contract_change_request_template.md`
- `19_merge_review_checklist.md`
- 对应的 `tasks/*.brief.md`

## 2. 基本边界

- 本项目首期只做微信小程序 + Web，原生 App 后置。
- 后端默认 Spring Boot 3.x、MySQL、Redis、OpenAPI、JUnit 5。
- P0 充值只做测试模式和积分流水，真实支付后置审批。
- 量化能力只允许 `research_only` / `simulation_only`。
- 不得新增荐股、喊单、带单、跟单、代客理财、实盘交易、自动下单、券商账户、买卖点、实时信号、公开持仓或策略代码售卖。
- 不得把积分描述为收益、返利、可提现资产或投资回报。

## 3. 修改规则

- 修改前先确认当前线程的 allowed paths、forbidden paths 和 locked paths。
- 只能修改任务明确允许的文件。
- `06_api_spec.md`、`07_database_schema.md`、`08_backend_engineering_spec.md` 属于契约文件，非 owner 线程不得直接改。
- `db/migration/**`、`backend/common/**`、`backend/src/main/java/com/aquant/common/**`、`prototype/html/app.js`、`prototype/html/styles.css` 属于高冲突路径，必须按文件边界矩阵执行。
- 遇到未授权文件需要变更时，在交付摘要中提出变更请求，不要直接改。

## 4. 质量门禁

交付前必须在项目根目录运行：

```bash
make check-all
```

如果当前任务创建了后端或前端工程，还要额外运行对应命令：

```bash
cd backend && ./mvnw test
cd web && npm run lint && npm run build
cd admin && npm run lint && npm run build
```

如果某个命令无法运行，必须说明原因、替代检查和残余风险。

分线程任务交付前还必须运行：

```bash
THREAD=<branch> make check-boundary
```

## 5. Task Brief

任何开发线程开工前必须使用 `13_task_brief_template.md` 填写 Task Brief。

Task Brief 至少包含：

- branch
- owner
- goal
- allowed paths
- forbidden paths
- locked paths
- input docs
- contract touched
- exact commands
- exit criteria
- failure action

没有 Task Brief，不得开始实现。

首批任务可直接使用 `tasks/` 目录中的预填 Brief；如果实际范围变化，先更新 Brief 或提交 Contract Change Request。

## 6. 失败处理

出现以下情况时停止扩大修改，按 `15_failure_handling_protocol.md` 处理：

- 测试失败。
- 合规检查失败。
- API 和文档不一致。
- migration 冲突。
- 文件越界。
- 线程失控。
- 上下文污染。

禁止为了保留已有工作量而降低门禁。

## 7. 交付摘要

每次交付必须包含：

```text
完成内容：
修改文件：
验证结果：
未完成事项：
风险：
需要主线集成处理：
```

如果涉及代码，还要说明运行过的命令和结果。
