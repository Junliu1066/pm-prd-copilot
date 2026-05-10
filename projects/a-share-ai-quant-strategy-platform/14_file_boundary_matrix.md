# 文件修改边界矩阵

- 文档状态：Draft / SDD 执行边界
- 适用对象：Codex 分线程、工程师、集成负责人
- 最后更新时间：2026-05-10

---

## 1. 权限标记

| 标记 | 含义 |
|---|---|
| `write` | 当前线程可以直接修改 |
| `read` | 当前线程只能读取，不能修改 |
| `locked` | 高冲突路径，必须获得 owner 授权 |
| `forbidden` | 当前线程禁止修改 |
| `request` | 只能提交变更请求，由 owner 修改 |

---

## 2. 契约与文档边界

| 路径 | Owner | `p0-docs` | `p0-spring-api` | `p0-quant-engine` | `p0-points` | 前端线程 | `qa-gates` |
|---|---|---|---|---|---|---|---|
| `AGENTS.md` | 集成负责人 | write | read | read | read | read | request |
| `01_prd.md` | 产品负责人 | locked | read | read | read | read | read |
| `02_prototype_layer.md` | 原型 owner | write | read | read | read | read | read |
| `03_internal_development_doc.md` | `p0-docs` | write | request | request | request | request | request |
| `04_codex_development_doc.md` | `p0-docs` | write | request | request | request | request | request |
| `05_codex_parallel_branch_development_doc.md` | `p0-docs` | write | request | request | request | request | request |
| `06_api_spec.md` | 集成负责人 | write | request | request | request | read | read |
| `07_database_schema.md` | 集成负责人 | write | request | request | request | read | read |
| `08_backend_engineering_spec.md` | `p0-spring-api` | request | write | request | request | read | read |
| `09_task_breakdown.md` | `p0-docs` | write | request | request | request | read | request |
| `10_test_plan.md` | QA owner | request | read | read | read | read | write |
| `11_local_dev_runbook.md` | 集成负责人 | write | request | request | request | read | request |
| `12_codex_thread_governance.md` | 集成负责人 | write | read | read | read | read | request |
| `13_task_brief_template.md` | 集成负责人 | write | read | read | read | read | request |
| `14_file_boundary_matrix.md` | 集成负责人 | write | read | read | read | read | request |
| `15_failure_handling_protocol.md` | 集成负责人 | write | read | read | read | read | request |
| `16_codex_execution_runbook.md` | 集成负责人 | write | read | read | read | read | request |
| `17_sdd_engineering_lessons.md` | 集成负责人 | write | read | read | read | read | request |
| `18_contract_change_request_template.md` | 集成负责人 | write | read | read | read | read | request |
| `19_merge_review_checklist.md` | QA owner | request | read | read | read | read | write |
| `automation/thread_registry.md` | 集成负责人 | write | read | read | read | read | request |
| `tasks/*.brief.md` | 集成负责人 | write | read | read | read | read | request |

---

## 3. 工程路径边界

| 路径 | Owner | `p0-spring-api` | `p0-quant-engine` | `p0-points` | `p0-admin` | `ai-compliance` | `qa-gates` |
|---|---|---|---|---|---|---|---|
| `backend/common/**`, `backend/src/main/java/com/aquant/common/**` | `p0-spring-api` | write | request | request | request | request | read |
| `backend/auth/**`, `backend/src/main/java/com/aquant/auth/**` | `p0-spring-api` | write | read | request | request | read | read |
| `backend/user/**`, `backend/src/main/java/com/aquant/user/**` | `p0-spring-api` | write | read | request | read | read | read |
| `backend/points/**`, `backend/src/main/java/com/aquant/points/**` | `p0-points` | request | forbidden | write | read | read | read |
| `backend/marketdata/**`, `backend/src/main/java/com/aquant/marketdata/**` | `p0-quant-engine` | request | write | forbidden | read | read | read |
| `backend/indicator/**`, `backend/src/main/java/com/aquant/indicator/**` | `p0-quant-engine` | request | write | forbidden | read | read | read |
| `backend/strategyengine/**`, `backend/src/main/java/com/aquant/strategyengine/**` | `p0-quant-engine` | request | write | forbidden | read | read | read |
| `backend/backtest/**`, `backend/src/main/java/com/aquant/backtest/**` | `p0-quant-engine` | request | write | forbidden | read | read | read |
| `backend/risk/**`, `backend/src/main/java/com/aquant/risk/**` | `p0-quant-engine` / `ai-compliance` | request | write | read | read | write | read |
| `backend/arena/**`, `backend/src/main/java/com/aquant/arena/**` | `p1-arena` | read | read | forbidden | read | read | read |
| `backend/ai/**`, `backend/src/main/java/com/aquant/ai/**` | `ai-compliance` | request | read | read | read | write | read |
| `backend/admin/**`, `backend/src/main/java/com/aquant/admin/**` | `p0-admin` | request | read | read | write | read | read |
| `db/migration/**` | 集成负责人 | locked | locked | locked | locked | locked | read |
| `tests/**` | QA owner | read | read | read | read | read | write |
| `scripts/**` | QA owner | read | read | read | read | read | write |

---

## 4. 前端与原型边界

| 路径 | Owner | `p0-web-prototype` | `p0-miniapp-frontend` | `p0-web-frontend` | `p0-admin` | 后端线程 |
|---|---|---|---|---|---|---|
| `prototype/html/**` | `p0-web-prototype` | write | read | read | read | forbidden |
| `miniapp/**` | `p0-miniapp-frontend` | read | write | forbidden | forbidden | read |
| `web/**` | `p0-web-frontend` | read | forbidden | write | forbidden | read |
| `admin/**` | `p0-admin` | read | forbidden | forbidden | write | read |

---

## 5. 冲突处理

- `locked` 路径必须先向 owner 提交变更请求。
- `request` 路径不得直接改，必须在交付摘要中写建议更新。
- `forbidden` 路径发现问题时只能记录，不得修改。
- 任何线程修改超出矩阵授权的文件，按 `15_failure_handling_protocol.md` 的文件越界处理。
