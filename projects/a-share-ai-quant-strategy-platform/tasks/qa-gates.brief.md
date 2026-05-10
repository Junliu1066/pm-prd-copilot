# Task Brief: QA Gates

Task ID: `qa-gates-001`
Branch: `codex/qa-gates`
Owner: Codex worker / QA owner
Status: `proposed`

## Goal

维护项目级质量门禁、测试清单和静态检查脚本，让文档、原型、合规、契约和线程边界可以被命令验证。

## Why

SDD 工程包只有在检查可执行时才适合并行开发。QA 线程需要把“应该遵守”变成“失败会非 0 退出”的门禁。

## Input Docs

- `AGENTS.md`
- `06_api_spec.md`
- `07_database_schema.md`
- `08_backend_engineering_spec.md`
- `09_task_breakdown.md`
- `10_test_plan.md`
- `12_codex_thread_governance.md`
- `13_task_brief_template.md`
- `14_file_boundary_matrix.md`
- `15_failure_handling_protocol.md`
- `16_codex_execution_runbook.md`

## Allowed Paths

- `scripts/**`
- `tests/**`
- `Makefile`
- `10_test_plan.md`
- `19_merge_review_checklist.md`

## Forbidden Paths

- `01_prd.md`
- `02_prototype_layer.md`
- `prototype/html/**`
- `backend/**`
- `db/migration/**`
- `miniapp/**`
- `web/**`
- `admin/**`

## Locked Paths

- `06_api_spec.md`: integration owner
- `07_database_schema.md`: integration owner
- `08_backend_engineering_spec.md`: `codex/p0-spring-api`
- `AGENTS.md`: integration owner

## Contract Touched

- API: no
- Database: no
- Permissions: no
- Points: no
- Quant run mode: no
- AI output: no
- Compliance wording: yes, only for gate rules and forbidden contexts

## Implementation Scope

- 维护 `make check-all`。
- 维护 docs、compliance、contracts、prototype、thread boundary 检查。
- 增加测试清单和合并清单中的可执行命令。
- 后端、前端工程创建后，把专项 test / lint / build 接入门禁。

## Out Of Scope

- 不实现产品功能。
- 不修改 API 或数据库契约。
- 不放宽合规红线。
- 不为通过检查删除已有门禁。

## Dependencies

- Upstream threads: `codex/p0-docs`
- Downstream affected threads: all implementation branches
- Required decisions: 新增重型依赖或外部扫描工具前需要集成负责人确认

## Exact Commands

- Required before work: `make check-all`
- Required before handoff: `THREAD=codex/qa-gates make check-boundary`
- Required after work: `make check-all`

## Exit Criteria

- 所有脚本失败时非 0 退出。
- `make check-all` 可以作为主入口。
- 线程边界检查可以按 `THREAD=<branch>` 执行。
- 文档说明和脚本行为一致。

## Failure Action

- 如果门禁误报，先增加最小白名单或上下文判断，不直接删除检查。
- 如果门禁漏报，增加复现样例并补检查。
- 如果需要改契约文件，提交 CCR 或请求 owner 修改。

## Delivery Summary Required

交付摘要必须包含完成内容、修改文件、验证结果、未完成事项、风险、需要主线集成处理、契约变更和文件边界结果。
