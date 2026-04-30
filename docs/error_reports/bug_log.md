# Bug Log

长期记录项目执行过程中的错误、失败检查、治理漂移和修复状态。

| ID | Date | Severity | Area | Status | Evidence | Suspected cause | Solution recommendation | Next action | User approval |
|---|---|---|---|---|---|---|---|---|---|
| BUG-2026-04-28-001 | 2026-04-28 | P2 | production pipeline governance | fixed | `run_pipeline.py` now enforces workflow approval gates by default, keeps `--governed` only as a compatibility flag, and requires explicit `--fast-draft` for draft exploration. Governance trace records `governance_mode`, `approval_gate_enforced`, `required_approvals`, and `stage_actions`; regression verifies default governed blocking, explicit `--governed` blocking, and `--fast-draft` allowance in a temp fixture; 2026-04-29 and 2026-04-30 overnight checks reran regression and harness check-only successfully, confirmed `pipeline-latest` is governed, and found no production bypass. | Previous fast draft pipeline did not enforce `workflow/prd_workflow.yaml` approvals by default and harness did not inspect pipeline governance declarations. Follow-up fixes scoped demo-only overrides to `pipeline_assumption_overrides`, centralized stage action mapping through manifest `stage_actions`, made shared JSON writes atomic, and made fast draft explicit. | Use the governed default path for production runs. Use `--fast-draft` only for labeled draft exploration. Keep demo-only overrides in `pipeline_assumption_overrides` and never treat them as product approvals. | Continue scheduled monitoring for any pipeline command that relies on implicit fast draft, omits required approvals, or produces a production manifest without governed approval fields. | No for the completed fix and monitoring evidence updates; yes for future stable governance or formal delivery policy changes. |
| BUG-2026-04-30-001 | 2026-04-30 | P1 | harness dependency closure | fixed | `run_harness.py` imported conditional checkers before all referenced checker files were committed. Commits `dfff924` and `e6837d0` added the remaining conditional harness checkers and UI style selector assets. Regression and harness check-only pass after both fixes. | Candidate / detachable capabilities were wired into stable entrypoints before their source files were fully submitted, creating a clean-checkout risk. | When a stable entrypoint imports a candidate component, either commit the component with explicit candidate boundaries or remove the import until the candidate is approved. | During future candidate work, run a clean dependency scan before committing stable entrypoints. | No for the completed fix; yes before promoting any candidate to stable. |
| BUG-2026-04-30-002 | 2026-04-30 | P1 | preference cache governance | fixed | Commit `9816c87` requires `--approved-by-user` for `clear` / `archive-clear`, records `user_approval_required` and `user_approval_confirmed`, and adds regression coverage. Harness preference cache check passes. | The preference cache tool allowed clear/archive-clear operations without a command-level explicit approval marker, which conflicted with the supervised long-term memory rule. | Keep project preference caches project-local. Require explicit approval for clearing, archive clearing, or long-term memory promotion. | Revisit only during project closeout or archive disposition. | Yes for actual project cache clearing or long-term memory promotion. |
| BUG-2026-04-30-003 | 2026-04-30 | P2 | internal delivery packaging | fixed | Commit `22ad7ff` generalized `package_internal_delivery.py`, adds `MANIFEST.json`, excludes runs/cache/zip by default, and validates demo / fitness / jiaxiaoqian packages in `/private/tmp`. Regression now checks internal package output. | The script was tied to an older project layout and required `交付包目录说明.md`, so generic projects such as demo and fitness failed. | Keep internal package as trusted-team tooling, separate from external B packages and redaction workflow. | Run real-output checks before using it for a new project delivery. | Yes before sharing any generated package externally; no for trusted internal package generation after project approval. |

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
