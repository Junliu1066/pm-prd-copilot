# Contract Change Request 模板

- 文档状态：Draft / SDD 契约变更模板
- 适用对象：Codex 分线程、工程师、集成负责人、产品负责人、合规审核
- 最后更新时间：2026-05-10

---

## 1. 使用规则

任何线程需要改变 API、数据库、权限、积分、量化执行模式、AI 输出结构或合规边界时，必须先提交本模板。未经确认，不得先写实现代码再回填契约文档。

适用变更类型：

- `api`
- `database`
- `permission`
- `points`
- `quant_run_mode`
- `ai_output`
- `compliance_wording`
- `external_dependency`
- `payment`

---

## 2. 标准模板

```text
CCR ID:
Requester Branch:
Requester Owner:
Status: proposed / approved / rejected / superseded
Created At:

Change Type:

Background:

Current Contract:
- File:
- Section:
- Current Rule:

Proposed Contract:
- File:
- Section:
- New Rule:

Reason:

Affected Threads:
- Upstream:
- Downstream:

Affected Files:

Risk Assessment:
- Product:
- Engineering:
- Data:
- Compliance:
- Test:

Required Document Updates:
- 06_api_spec.md:
- 07_database_schema.md:
- 08_backend_engineering_spec.md:
- 09_task_breakdown.md:
- 10_test_plan.md:
- 11_local_dev_runbook.md:
- 12_codex_thread_governance.md:

Required Checks:
- make check-all
- THREAD=<branch> make check-boundary
- backend / frontend specific commands:

Rollback Plan:

Approval:
- Product:
- Engineering:
- Compliance:
```

---

## 3. 审批规则

| 变更类型 | 最低审批 |
|---|---|
| API path / method / request / response / error code | engineering |
| 数据表、索引、枚举、migration 顺序 | engineering |
| 权限、角色、后台审核流程 | product + engineering |
| 积分充值、赠送、消耗、退款、冻结 | product + engineering + compliance |
| `research_only` / `simulation_only` 边界 | product + engineering + compliance |
| AI 输出结构、风险提示、拦截规则 | product + compliance |
| 外部数据源、真实支付、短信、模型供应商 | product + engineering + compliance |

---

## 4. 拒绝条件

以下变更直接拒绝，除非项目负责人重新定义产品范围并取得合规确认：

- 禁止新增 C 端实盘交易能力。
- 禁止新增券商账户绑定能力。
- 禁止新增自动下单能力。
- 禁止新增跟单、带单或代客操作能力。
- 向 C 端输出个性化买卖建议。
- 禁止展示持仓、买卖点、实时交易信号或策略代码。
- 把积分描述成可提现资产、收益、返利或投资回报。

---

## 5. 最小合并要求

CCR 被批准后，合并前必须满足：

- 契约文档已先更新。
- 受影响 Task Brief 已同步。
- 测试计划已覆盖新增或变更行为。
- `make check-all` 通过。
- 涉及线程运行 `THREAD=<branch> make check-boundary`。
- 交付摘要中列出 CCR ID。
