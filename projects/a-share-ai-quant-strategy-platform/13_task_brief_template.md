# Task Brief 硬模板

- 文档状态：Draft / SDD 执行模板
- 适用对象：所有 Codex 分线程和工程实现任务
- 最后更新时间：2026-05-10

---

## 1. 使用规则

每个实现任务开工前必须复制本模板并填写完整。没有 Task Brief，不得修改代码、接口、数据库、原型或工程文档。

Task Brief 的作用是把“我要做什么、能改哪里、不能改哪里、怎么检查、失败怎么办”一次性说清楚。

---

## 2. 标准模板

```text
Task ID:
Branch:
Owner:
Status: proposed / active / blocked / ready_for_review / changes_requested / merged / abandoned

Goal:

Why:

Input Docs:
- AGENTS.md:
- PRD:
- Internal Dev Doc:
- API Spec:
- Database Schema:
- Backend Spec:
- Test Plan:
- Thread Governance:
- Prototype / UI:

Allowed Paths:

Forbidden Paths:

Locked Paths:

Contract Touched:
- API: yes / no
- Database: yes / no
- Permissions: yes / no
- Points: yes / no
- Quant run mode: yes / no
- AI output: yes / no
- Compliance wording: yes / no

Implementation Scope:

Out Of Scope:

Dependencies:
- Upstream threads:
- Downstream affected threads:
- Required decisions:

Exact Commands:
- Required before work:
- Required after work:
- Optional checks:

Exit Criteria:

Failure Action:

Delivery Summary Required:
```

---

## 3. 必填约束

### 3.1 Allowed Paths

必须写具体路径，不能写“相关文件”。

正确示例：

```text
Allowed Paths:
- backend/points/**
- db/migration/V002__create_points.sql
- tests/points/**
```

错误示例：

```text
Allowed Paths:
- 后端相关文件
```

### 3.2 Forbidden Paths

必须列出容易误改的边界。

示例：

```text
Forbidden Paths:
- 01_prd.md
- prototype/html/**
- backend/arena/**
- backend/backtest/**
```

### 3.3 Locked Paths

如果任务涉及高冲突文件，必须写 owner。

示例：

```text
Locked Paths:
- db/migration/**: locked by integration owner
- 06_api_spec.md: locked by codex/p0-docs
```

### 3.4 Contract Touched

只要改 API、数据库、权限、积分、量化模式、AI 输出或合规话术，就必须先确认契约文件更新策略。

默认规则：

- 实现线程不能先改代码再回填契约。
- 非契约 owner 线程只能提出变更请求。

### 3.5 Exact Commands

必须写可复制执行的命令。

示例：

```text
Exact Commands:
- make check-all
- cd backend && ./mvnw test
```

### 3.6 Failure Action

必须写失败后的处理方式。

示例：

```text
Failure Action:
- If make check-all fails, stop and fix only the failing gate.
- If migration conflicts, stop and ask integration owner to re-sequence migration numbers.
- If compliance gate fails, remove or rewrite the offending wording before continuing.
```

---

## 4. P0 后端任务示例

```text
Task ID: p0-points-001
Branch: codex/p0-points
Owner: Codex worker
Status: proposed

Goal:
Implement point account creation and query API.

Why:
P0 report unlock and daily check-in depend on point account availability.

Input Docs:
- AGENTS.md: required
- API Spec: 06_api_spec.md
- Database Schema: 07_database_schema.md
- Backend Spec: 08_backend_engineering_spec.md
- Test Plan: 10_test_plan.md
- Thread Governance: 12_codex_thread_governance.md

Allowed Paths:
- backend/points/**
- backend/user/**
- tests/points/**

Forbidden Paths:
- prototype/html/**
- backend/arena/**
- backend/backtest/**
- 01_prd.md

Locked Paths:
- db/migration/**: integration owner
- 06_api_spec.md: codex/p0-docs

Contract Touched:
- API: no
- Database: no
- Permissions: yes
- Points: yes
- Quant run mode: no
- AI output: no
- Compliance wording: no

Implementation Scope:
- Create point account on first login.
- Implement GET /api/v1/points/account.
- Return balance and accumulated counters.

Out Of Scope:
- Real payment.
- Arena observe unlock.
- Refund.

Exact Commands:
- make check-all
- cd backend && ./mvnw test

Exit Criteria:
- New user gets a point account.
- Existing user does not get duplicate account.
- API response follows 06_api_spec.md.

Failure Action:
- If point account duplication occurs, stop and fix unique constraint handling.
- If API spec mismatch appears, stop and raise contract change request.
```

