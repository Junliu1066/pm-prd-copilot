# Codex 分线程治理文档

- 文档状态：Draft / 内部研发治理版
- 适用项目：A股 AI 量化策略研究平台
- 适用读者：产品负责人、研发负责人、Codex 操作者、代码集成人、QA、合规审核
- 关联文档：[05_codex_parallel_branch_development_doc.md](/Users/liujun/Desktop/产品经理skill/projects/a-share-ai-quant-strategy-platform/05_codex_parallel_branch_development_doc.md)
- 最后更新时间：2026-05-09

---

## 1. 治理目标

本文件解决“多个 Codex 线程并行开发时，如何不互相踩、如何同步接口、如何合并、如何止损”的问题。

`05_codex_parallel_branch_development_doc.md` 定义分支模型和任务拆分，本文件定义治理规则。

治理目标：

- 每条线程有唯一目标、唯一 owner、明确文件边界。
- 高冲突文件必须先锁定，再修改。
- API、数据库、权限、积分、合规边界不能被单线程私自改。
- 线程之间通过契约同步，不靠口头记忆。
- 合并前可检查、可追溯、可回滚。
- 失控线程可以暂停、隔离或废弃，不污染主线。

---

## 2. 角色与职责

| 角色 | 职责 | 可由谁承担 |
|---|---|---|
| 产品负责人 | 决定范围、优先级、合规风险接受度 | 项目 owner |
| 集成负责人 | 控制主线、接口、数据库、跨线程冲突和合并顺序 | 技术负责人 / 主 Codex 线程 |
| 线程负责人 | 执行单一分支任务，维护本线程上下文和交付摘要 | Codex 子线程 / 工程师 |
| QA 负责人 | 定义和执行质量门禁 | QA / Codex QA 线程 |
| 合规负责人 | 审核风险话术、AI 输出、积分和量化边界 | 合规 / 项目 owner |

单人项目中可以一个人承担多个角色，但决策权要分开看：产品范围、接口契约、数据库结构、合规边界都不能由实现线程临时决定。

---

## 3. 线程生命周期

```text
申请线程
-> 分配 owner
-> 生成线程卡
-> 锁定文件范围
-> 执行开发
-> 同步契约变更
-> 自测通过
-> 提交交付摘要
-> 集成审核
-> 合并或退回
-> 关闭线程
```

每条线程必须处于以下状态之一：

| 状态 | 含义 | 允许动作 |
|---|---|---|
| `proposed` | 已提出，未开工 | 补充范围、依赖、风险 |
| `active` | 正在执行 | 修改已授权文件，定期同步 |
| `blocked` | 被外部决策阻塞 | 记录阻塞点，不扩大范围 |
| `ready_for_review` | 自测完成，等待审核 | 不再追加功能，只修审核问题 |
| `changes_requested` | 被退回 | 只修指定问题 |
| `merged` | 已合并 | 关闭线程 |
| `abandoned` | 废弃 | 不再合并，必要时手动摘取可用变更 |

---

## 4. 线程卡模板

每条线程开工前必须创建线程卡。线程卡记录在本地 `automation/thread_registry.md` 中，详细执行范围写入对应的 `tasks/*.brief.md`。

```text
线程 ID：
分支：
状态：
owner：
创建时间：
预计关闭时间：

目标：

输入文档：
- PRD：
- 原型：
- API：
- 数据库：
- 后端规范：
- 测试计划：

允许改动：

禁止改动：

文件锁：

依赖线程：

对外契约：
- API：
- 数据表：
- 事件 / 任务：
- 配置：

合规边界：

必跑检查：

交付物：

最新同步记录：
```

---

## 5. 文件锁规则

### 5.1 独占锁

以下文件或目录同一时间只能由一个线程修改：

| 文件 / 目录 | 默认 owner |
|---|---|
| `01_prd.md` | `codex/p0-docs` |
| `02_prototype_layer.md` | `codex/p0-web-prototype` |
| `03_internal_development_doc.md` | `codex/p0-docs` |
| `04_codex_development_doc.md` | `codex/p0-docs` |
| `05_codex_parallel_branch_development_doc.md` | `codex/p0-docs` |
| `06_api_spec.md` | `codex/p0-docs` / 集成负责人 |
| `07_database_schema.md` | `codex/p0-docs` / 集成负责人 |
| `08_backend_engineering_spec.md` | `codex/p0-spring-api` / 集成负责人 |
| `prototype/html/app.js` | `codex/p0-web-prototype` |
| `prototype/html/styles.css` | `codex/p0-web-prototype` |
| `backend/common/**` | `codex/p0-spring-api` |
| `db/migration/**` | 集成负责人 |

其他线程需要修改独占锁文件时，必须提交“变更请求”，由 owner 统一改。

### 5.2 共享读锁

以下文档所有线程可读，但默认不可直接改：

- `01_prd.md`
- `03_internal_development_doc.md`
- `06_api_spec.md`
- `07_database_schema.md`
- `10_test_plan.md`

线程发现不一致时，优先填写 `18_contract_change_request_template.md`，或在交付摘要中写：

```text
建议更新：
文件：
位置：
原因：
建议内容：
影响线程：
```

---

## 6. 契约变更治理

契约包括 API、数据库、权限、积分规则、量化执行模式、AI 输出结构、合规红线。

### 6.1 需要审批的变更

以下变更必须先停手审批：

- 新增、删除或重命名 API。
- 修改 request / response 字段。
- 修改错误码。
- 新增或修改数据库表、索引、状态枚举。
- 修改积分充值、消耗、退款、赠送规则。
- 修改 `research_only` / `simulation_only` 量化边界。
- 新增外部数据源或真实支付通道。
- 修改 AI 禁止输出规则。
- 任何涉及荐股、跟单、实盘、自动下单、券商账户、买卖点、实时信号的能力。

### 6.2 变更流程

```text
线程提出变更请求
-> 集成负责人判断影响范围
-> 产品 / 技术 / 合规确认
-> 更新 06/07/08/10 对应文档
-> 通知依赖线程
-> 线程按新契约继续实现
```

实现线程不得先写代码再回填契约文档。

---

## 7. 上下文包治理

每条线程只接收完成任务所需的最小上下文，避免上下文污染。

### 7.1 P0 后端上下文包

必须包含：

- `03_internal_development_doc.md`
- `06_api_spec.md`
- `07_database_schema.md`
- `08_backend_engineering_spec.md`
- `10_test_plan.md`

不得包含：

- 与当前模块无关的 UI 细节。
- 未确认的商业化假设。
- 外部分享版材料。

### 7.2 前端上下文包

必须包含：

- `01_prd.md`
- `02_prototype_layer.md`
- `06_api_spec.md`
- HTML 原型相关文件。

前端线程只能消费 API 契约，不得临时发明后端字段。

### 7.3 QA 上下文包

必须包含：

- `06_api_spec.md`
- `07_database_schema.md`
- `08_backend_engineering_spec.md`
- `09_task_breakdown.md`
- `10_test_plan.md`

QA 线程可以提出缺陷和门禁，不直接实现产品功能。

---

## 8. 日常同步机制

并行开发时，每条 active 线程每天或每个大步骤后输出一次同步记录：

```text
线程：
日期：
已完成：
正在做：
阻塞：
新增契约变更：
影响其他线程：
下一步：
```

必须同步的情况：

- 修改 API。
- 修改数据库。
- 修改 shared common 代码。
- 修改积分或权限逻辑。
- 修改合规边界。
- 发现原型和 API 不一致。
- 测试门禁失败且影响其他线程。

---

## 9. 合并治理

### 9.1 合并前检查

每条线程合并前必须满足：

- 只修改授权范围内文件。
- 自测命令已执行并记录结果。
- API 和数据库变更已同步文档。
- 没有引入废弃收费话术。
- 没有引入荐股、跟单、持仓、买卖点、实时信号、自动下单、券商账户。
- 后台敏感操作有审计日志。
- 积分相关逻辑可追溯、不可提现、不可返利。
- 量化相关逻辑只允许 `research_only` / `simulation_only`。

### 9.2 合并顺序

默认顺序：

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

如果后续线程依赖前置线程接口，必须等待前置线程至少达到 `ready_for_review` 并冻结契约。

---

## 10. 冲突处理

### 10.1 文档冲突

优先级：

```text
用户最新明确指令
-> 01_prd.md
-> 03_internal_development_doc.md
-> 06_api_spec.md / 07_database_schema.md / 08_backend_engineering_spec.md
-> 线程局部说明
```

如果 PRD 与工程文档冲突，先暂停实现，由 `codex/p0-docs` 更新后再继续。

### 10.2 代码冲突

处理规则：

- 不允许用覆盖方式解决冲突。
- 先判断 owner，再由 owner 合并。
- 共享基础设施冲突归 `codex/p0-spring-api` 或集成负责人处理。
- 数据库 migration 冲突必须线性重排，不允许两个线程生成同一个版本号。

### 10.3 合规冲突

合规从严：

- 不确定是否可写时，先按不可写处理。
- 不确定是否可展示时，先不展示。
- 不确定是否收费合规时，先按积分测试模式处理，不上线真实支付。

---

## 11. 失控线程处理

以下情况视为失控线程：

- 修改大量未授权文件。
- 未经审批修改产品范围、数据库、API 或合规边界。
- 引入实盘、券商账户、自动下单、跟单、持仓、买卖点或实时信号。
- 重构范围明显超过任务目标。
- 多次测试失败且影响其他线程。

处理方式：

```text
暂停线程
-> 标记 blocked 或 abandoned
-> 提取可用 diff
-> 集成负责人判断是否保留
-> 重新开小线程修复
```

禁止为了保留失控线程的工作量而降低合并门禁。

---

## 12. 治理台账

已创建 `automation/thread_registry.md`，记录所有线程状态。

台账字段：

| 字段 | 说明 |
|---|---|
| thread_id | 线程 ID |
| branch | 分支名 |
| owner | 负责人 |
| status | 线程状态 |
| locked_paths | 文件锁 |
| depends_on | 依赖线程 |
| contract_changes | 契约变更 |
| last_sync | 最近同步时间 |
| merge_status | 合并状态 |

MVP 阶段以 `automation/thread_registry.md` 作为唯一轻量真实来源；外部任务系统可以引用它，但不能与其冲突。

---

## 13. 启动第一批线程建议

第一批只启动以下线程：

| 顺序 | 线程 | 目的 |
|---:|---|---|
| 1 | `codex/p0-docs` | 冻结文档、API、数据库、工程规范 |
| 2 | `codex/p0-spring-api` | 建 Spring Boot 基础工程和公共能力 |
| 3 | `codex/p0-quant-engine` | 建 research_only / simulation_only 量化链路 |
| 4 | `codex/p0-points` | 建积分账户、充值占位、每日赠送、消耗和权益 |
| 5 | `codex/qa-gates` | 建基础质量门禁 |

小程序、Web、后台线程等 API 契约稳定后再进入。
