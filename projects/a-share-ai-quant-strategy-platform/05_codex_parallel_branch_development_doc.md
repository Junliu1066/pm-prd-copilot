# Codex 分线程 / 分支并行开发文档

- 文档状态：Draft / 内部研发并行协作文档
- 适用项目：A股 AI 量化策略研究平台
- 适用读者：产品负责人、研发负责人、Codex 操作者、代码集成人
- 关联文档：[04_codex_development_doc.md](/Users/liujun/Desktop/产品经理skill/projects/a-share-ai-quant-strategy-platform/04_codex_development_doc.md)
- 关联治理文档：[12_codex_thread_governance.md](/Users/liujun/Desktop/产品经理skill/projects/a-share-ai-quant-strategy-platform/12_codex_thread_governance.md)
- 最后更新时间：2026-05-09

---

## 1. 为什么要用分线程 / 分支

本项目天然适合 Codex 并行开发，因为产品链路被拆成了多个相对独立的工作域：

- 产品文档。
- HTML / UI 原型。
- 小程序前端。
- Web 前端。
- Spring Boot 后端。
- 量化研究 / 回测 / 仿真引擎。
- 积分账户与充值接口。
- 策略竞技场。
- AI 风控与合规。
- QA 与质量门禁。

分线程 / 分支能提升速度的前提是：每条线程有清晰所有权，避免多个 Codex 同时修改同一批核心文件。

---

## 2. 推荐分支模型

主分支只保留稳定产物：

```text
main
```

Codex 功能分支统一使用 `codex/` 前缀：

```text
codex/p0-docs
codex/p0-web-prototype
codex/p0-miniapp-frontend
codex/p0-web-frontend
codex/p0-spring-api
codex/p0-quant-engine
codex/p0-points
codex/p0-admin
codex/p1-arena
codex/ai-compliance
codex/qa-gates
```

---

## 3. 分支职责

| 分支 | 目标 | 主要文件范围 | 禁止改动 |
|---|---|---|---|
| `codex/p0-docs` | PRD、开发文档、接口草案、数据模型草案、分线程治理文档 | `*.md`、`automation/thread_registry.md`、`tasks/*.brief.md` | 业务代码、原型代码 |
| `codex/p0-web-prototype` | HTML 原型高保真迭代 | `prototype/html/` | 后端代码、数据库迁移 |
| `codex/p0-miniapp-frontend` | 微信小程序页面和组件 | `miniapp/` | Web 原型、后端核心逻辑 |
| `codex/p0-web-frontend` | Web C 端页面 | `web/` | 小程序、后端核心逻辑 |
| `codex/p0-spring-api` | Spring Boot 基础 API | `backend/common/`、`backend/auth/`、`backend/user/`、`api/`、`tests/backend/` | HTML 原型、PRD 大范围改写、未授权 migration |
| `codex/p0-quant-engine` | 量化执行逻辑、指标、回测、仿真、风控计算；参考 QuantDinger 的闭环但不接实盘 | `backend/marketdata/`、`backend/indicator/`、`backend/strategyengine/`、`backend/backtest/`、`backend/risk/` | 积分账务、C 端买卖信号、券商账户、自动下单 |
| `codex/p0-points` | 积分账户、充值接口占位、每日登录赠送 | `backend/points/`、`tests/points/` | 前端页面、竞技场核心榜单、未授权 migration |
| `codex/p0-admin` | 运营后台和内容审核 | `admin/`、`backend/admin/`、`backend/audit/` | C 端主路径 |
| `codex/p1-arena` | 策略竞技场、排行榜、1v1、选手报名 | `arena/`、`backend/arena/` | P0 登录、积分核心账务 |
| `codex/ai-compliance` | AI 输出结构、风险词、合规拦截 | `backend/ai/`、`backend/audit/`、prompt 文档 | UI 大范围重构 |
| `codex/qa-gates` | 自动化检查、测试、截图验收 | `tests/`、`scripts/`、`Makefile`、`10_test_plan.md`、`19_merge_review_checklist.md` | 产品功能实现 |

---

## 4. 并行开发原则

### 4.1 文件所有权

每条线程开始前必须声明：

- 本线程目标。
- 可改文件。
- 不可改文件。
- 依赖输入。
- 必跑检查。
- 合并条件。

优先使用 `tasks/` 目录中的预填 Task Brief；新任务必须按 `13_task_brief_template.md` 补齐。

示例：

```text
线程：codex/p0-points
目标：实现积分账户、充值订单、每日登录赠送和积分消耗接口
可改：backend/points/**, tests/points/**
不可改：prototype/html/**, arena/**, PRD 主范围, db/migration/**
必跑：make check-all, THREAD=codex/p0-points make check-boundary, Spring Boot Test, points API tests
合并条件：积分流水不可为负，重复登录不重复赠送，充值回调幂等
```

### 4.2 不同线程不能抢同一文件

高冲突文件：

- `01_prd.md`
- `02_prototype_layer.md`
- `03_internal_development_doc.md`
- `prototype/html/app.js`
- `prototype/html/styles.css`
- 后端全局配置文件
- 数据库 migration 汇总文件

这些文件只能由一个线程拥有。其他线程需要变更时，先在自己的文档里提变更建议，由集成线程统一改。

### 4.3 P0 优先

合并优先级：

1. 文档与接口冻结。
2. Spring Boot 基础 API。
3. 量化研究、指标、回测、仿真和风控计算。
4. 积分账户和充值接口。
5. 小程序 / Web 主路径。
6. 后台审核。
7. AI 风控。
8. 策略竞技场 P1。
9. QA 门禁。

P1 竞技场不能阻塞 P0 主路径上线。

---

## 5. 推荐并行批次

### 第一批：基础闭环

```text
codex/p0-docs
codex/p0-web-prototype
codex/p0-spring-api
codex/p0-quant-engine
codex/p0-points
codex/ai-compliance
codex/qa-gates
```

目标：

- 冻结 PRD、开发文档、API 草案和数据模型。
- 稳定 HTML 原型。
- 建立 Spring Boot 基础工程。
- 建立 research_only / simulation_only 量化研究和回测链路。
- 实现积分账户、充值接口占位、每日登录赠送。
- 建立 AI 风控规则。
- 建立基础检查脚本。

### 第二批：端侧落地

```text
codex/p0-miniapp-frontend
codex/p0-web-frontend
codex/p0-admin
```

目标：

- 小程序主路径可用。
- Web C 端主路径可用。
- 后台支持策略、报告、审核、积分记录。

### 第三批：竞技场实验

```text
codex/p1-arena
codex/ai-compliance
codex/qa-gates
```

目标：

- 策略竞技场 S1 可内测。
- 排行榜、1v1、选手报名、观察内容解锁可用。
- 合规和异常处理闭环。

---

## 6. Codex 分线程任务模板

每条线程启动时复制以下模板：

```text
线程名称：
分支名称：
负责人：

目标：

输入：
- PRD：
- 原型：
- 开发文档：
- 接口草案：

可修改文件：

不可修改文件：

实现范围：

不做范围：

数据 / 接口依赖：

合规边界：

必跑检查：

交付物：

合并前检查：
```

---

## 7. 合并门禁

每个分支合并前必须满足：

- `make check-all` 通过。
- `THREAD=<branch> make check-boundary` 通过。
- 没有语法错误。
- 没有明显未处理冲突。
- 没有越权修改不属于本线程的文件。
- 关键路径可跑通。
- 文档和接口变更同步。
- 不引入买卖建议、收益承诺、跟单、持仓、实时信号。
- 如果涉及积分，必须保证积分流水可追溯、不可提现、不可返利、不可被描述为收益。
- 如果涉及 Spring Boot 后端，必须跑对应测试。
- 如果涉及量化执行，必须默认 `research_only` / `simulation_only`，不得新增实盘、券商账户、自动下单或 C 端实时买卖信号。

---

## 8. 冲突处理

### 8.1 文档冲突

处理原则：

- 以最新产品范围为准。
- 保留事实 / 假设 / 待确认问题。
- 不把未确认假设写成已确认事实。
- 合规边界从严。

### 8.2 原型冲突

处理原则：

- 以当前 HTML 原型为视觉基线。
- 用户明确否定的组件不能回归，例如手机状态栏。
- 积分制度替代会员、月票、观众票。
- 页面必须保留风险提示。

### 8.3 后端冲突

处理原则：

- Spring Boot 工程结构优先稳定。
- 数据库迁移必须线性可追溯。
- `p0-quant-engine` 只负责研究 / 仿真 / 回测能力，不能把实盘执行字段带入主数据模型。
- 积分账务相关冲突优先人工复核。
- 认证、权限、审计日志不可绕过。

---

## 9. 本项目推荐合并顺序

```text
codex/p0-docs
-> codex/p0-spring-api
-> codex/p0-quant-engine
-> codex/p0-points
-> codex/p0-web-prototype
-> codex/p0-miniapp-frontend
-> codex/p0-web-frontend
-> codex/p0-admin
-> codex/ai-compliance
-> codex/p1-arena
-> codex/qa-gates
```

说明：

- `p0-docs` 先合并，避免后续实现没有依据。
- `p0-spring-api` 和 `p0-points` 优先，前端需要接口约束。
- `p0-quant-engine` 在基础 API 后进入，先输出研究 / 仿真 / 回测能力，再给市场温度、报告和竞技场复用。
- `p1-arena` 后置，避免拖慢 P0。
- `qa-gates` 可以持续并行，但最终合并时要覆盖所有主路径。

---

## 10. 分支交付摘要格式

每个分支结束时输出：

```text
分支：
完成内容：
修改文件：
验证结果：
未完成事项：
风险：
需要主线集成处理：
契约变更：
文件边界：
```

示例：

```text
分支：codex/p0-points
完成内容：积分账户、充值订单、每日登录赠送、积分消耗接口
修改文件：backend/points/**, tests/points/**
验证结果：make check-all 通过，THREAD=codex/p0-points make check-boundary 通过，JUnit 通过，重复登录不重复赠送
未完成事项：真实微信支付回调待接入
风险：积分退款规则需财务确认
需要主线集成处理：前端积分中心接入接口
契约变更：无
文件边界：未越界
```
