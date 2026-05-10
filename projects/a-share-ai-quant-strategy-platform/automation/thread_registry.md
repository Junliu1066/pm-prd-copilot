# Codex 分线程台账

- 文档状态：Draft / SDD 执行台账
- 适用对象：Codex 主线程、Codex 子线程、集成负责人、QA
- 最后更新时间：2026-05-10

---

## 1. 使用规则

本文件是 Codex 分线程的唯一轻量台账。任何线程开工、阻塞、进入审核、合并或废弃时，都要同步更新本文件或在交付摘要中明确要求集成负责人更新。

台账只记录执行状态，不替代 `13_task_brief_template.md`、`14_file_boundary_matrix.md` 和 `15_failure_handling_protocol.md`。

状态只能使用：

```text
proposed / active / blocked / ready_for_review / changes_requested / merged / abandoned
```

---

## 2. 当前线程

| thread_id | branch | owner | status | locked_paths | depends_on | contract_changes | last_sync | merge_status |
|---|---|---|---|---|---|---|---|---|
| thread-docs-001 | `codex/p0-docs` | integration owner | active | `01_prd.md`, `03_internal_development_doc.md`, `04_codex_development_doc.md`, `05_codex_parallel_branch_development_doc.md`, `06_api_spec.md`, `07_database_schema.md` | none | docs / contracts | 2026-05-10 | not merged |
| thread-spring-api-001 | `codex/p0-spring-api` | unassigned | proposed | `backend/common/**`, `backend/auth/**`, `backend/user/**`, `08_backend_engineering_spec.md` | thread-docs-001 | request only | 2026-05-10 | not started |
| thread-quant-engine-001 | `codex/p0-quant-engine` | unassigned | proposed | `backend/marketdata/**`, `backend/indicator/**`, `backend/strategyengine/**`, `backend/backtest/**`, `backend/risk/**` | thread-docs-001, thread-spring-api-001 | request only | 2026-05-10 | not started |
| thread-points-001 | `codex/p0-points` | unassigned | proposed | `backend/points/**` | thread-docs-001, thread-spring-api-001 | request only | 2026-05-10 | not started |
| thread-qa-gates-001 | `codex/qa-gates` | unassigned | proposed | `scripts/**`, `tests/**`, `Makefile`, `10_test_plan.md` | thread-docs-001 | request only | 2026-05-10 | not started |

---

## 3. 状态更新协议

### 3.1 开工

线程从 `proposed` 进入 `active` 前必须满足：

- 已有 Task Brief。
- 已确认 allowed paths、forbidden paths、locked paths。
- 已运行 `make check-all`。
- 如设置了分支名，已运行 `THREAD=<branch> make check-boundary`。

### 3.2 阻塞

出现以下任一情况时，线程必须进入 `blocked`：

- 需要修改契约文件但当前线程无权限。
- 需要新增或调整数据库 migration 顺序。
- 需要产品、技术或合规确认。
- 质量门禁失败且无法在本线程授权路径内修复。

阻塞记录必须包含：

```text
阻塞原因：
影响文件：
需要谁确认：
建议处理：
可继续的最小范围：
```

### 3.3 审核

线程进入 `ready_for_review` 前必须提供：

- 修改文件清单。
- 运行命令和结果。
- 契约变更记录或“无契约变更”声明。
- 文件边界检查结果。
- 未完成事项和残余风险。

### 3.4 关闭

`merged` 或 `abandoned` 之后不得继续在原线程追加新范围。需要继续开发时，创建新 thread_id 和新 Task Brief。

---

## 4. 文件锁记录

| path | current_owner | status | note |
|---|---|---|---|
| `06_api_spec.md` | integration owner | locked | 所有 API 改动必须走 Contract Change Request |
| `07_database_schema.md` | integration owner | locked | 所有表结构、索引、枚举改动必须走 Contract Change Request |
| `db/migration/**` | integration owner | locked | migration 编号由集成负责人分配 |
| `backend/common/**` | `codex/p0-spring-api` | locked when active | 公共响应体、异常、审计、幂等规则集中维护 |
| `prototype/html/app.js` | `codex/p0-web-prototype` | locked when active | 原型行为由原型线程维护 |
| `prototype/html/styles.css` | `codex/p0-web-prototype` | locked when active | 原型视觉由原型线程维护 |

---

## 5. 台账维护要求

- 每次合并前检查本文件是否需要更新。
- 不允许多个 active 线程同时持有同一 locked path。
- 线程如果只提出变更请求，不得把 contract_changes 写成 approved。
- 台账内容与 Task Brief 冲突时，以 Task Brief 和文件边界矩阵为准，并在合并审核中修正台账。
