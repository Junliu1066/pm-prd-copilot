# Bug Log

长期记录项目执行过程中的错误、失败检查、治理漂移和修复状态。

| ID | Date | Severity | Area | Status | Evidence | Suspected cause | Solution recommendation | Next action | User approval |
|---|---|---|---|---|---|---|---|---|---|
| BUG-2026-04-28-001 | 2026-04-28 | P2 | production pipeline governance | fixed | `run_pipeline.py` now enforces workflow approval gates by default, keeps `--governed` only as a compatibility flag, and requires explicit `--fast-draft` for draft exploration. Governance trace records `governance_mode`, `approval_gate_enforced`, `required_approvals`, and `stage_actions`; regression verifies default governed blocking, explicit `--governed` blocking, and `--fast-draft` allowance in a temp fixture; 2026-04-29 overnight check reran regression and harness check-only successfully, confirmed `pipeline-latest` is governed, and found no production bypass. | Previous fast draft pipeline did not enforce `workflow/prd_workflow.yaml` approvals by default and harness did not inspect pipeline governance declarations. Follow-up fixes scoped demo-only overrides to `pipeline_assumption_overrides`, centralized stage action mapping through manifest `stage_actions`, made shared JSON writes atomic, and made fast draft explicit. | Use the governed default path for production runs. Use `--fast-draft` only for labeled draft exploration. Keep demo-only overrides in `pipeline_assumption_overrides` and never treat them as product approvals. | Continue scheduled monitoring for any pipeline command that relies on implicit fast draft, omits required approvals, or produces a production manifest without governed approval fields. | No for the completed fix and monitoring evidence updates; yes for future stable governance or formal delivery policy changes. |

## Status Rules

- `open`: 已确认存在，尚未修复。
- `watch`: 未复现或风险较低，需要继续观察。
- `fixed`: 已修复并通过复测。
- `blocked`: 需要用户决策、外部凭证、环境或上游信息。

## Severity Rules

- `P0`: 阻塞主流程或可能造成数据/文件损失。
- `P1`: 治理合同、开发文档、外部版或核心交付链路明显失效。
- `P2`: 局部功能、文档同步、测试覆盖或效率问题。
- `P3`: 低风险清理、说明、命名或观察项。
