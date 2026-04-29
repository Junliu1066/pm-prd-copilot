# Contract Responsibility Layer

这层负责把“有人负责”变成“责任被执行并留下证据”。它不新增 steward、不新增 harness，先复用现有角色。

## Scope

触发这层的改动包括：

- interface / artifact / schema / workflow action / registry 字段变化。
- harness、eval、regression、automation 的行为变化。
- PRD 或 Codex 开发文档生成链路变化，包括 template、schema、prompt、renderer、sample output。
- Skill、MCP、plugin、package builder、project closeout、cleanup、memory、teaching 规则变化。

## Owner Matrix

| Area | Primary owner | Required review |
|---|---|---|
| 是否需要新增 Skill / MCP / harness / plugin | `capability-enablement-steward` | 必须先证明复用或扩展现有组件不足 |
| interface、artifact、schema、workflow、registry 合同一致性 | `development-governance-steward` | 必须列出读写边界、owner、输入输出、验证命令 |
| harness / eval 是只读还是会写报告 | `development-governance-steward` | 必须标注写入路径，避免“检查”制造未说明变更 |
| PRD 输出语义质量、图表位置、页面说明、领域污染 | `review-steward` | 必须检查旧口径、跨项目污染、默认 AI/导出误入 |
| 用户教学是否进入长期规则 | `learning-steward` | 必须先形成 proposal 或 recommendation plan，不能直接吸收 |
| 自动化健康、cwd、模型、模板路径、报告位置 | `development-governance-steward` | 每日报告必须列出异常和解决建议 |
| 抽查是否真的留下 owner 证据 | `random-audit-inspector` | 只报告，不直接修改 artifact、memory 或 Skill |

## Required Evidence

每次触发这层时，汇报必须包含：

- affected contract：涉及哪些接口、artifact、schema、workflow、registry、automation 或 generator。
- responsible owner：哪个 steward 负责主审。
- write behavior：检查或脚本是否写文件，写到哪里。
- sync scope：template、schema、prompt、renderer、sample output、regression 是否需要同步。
- validation：至少一条可执行验证命令或替代检查。
- approval point：是否需要用户批准，批准前不得改什么。
- follow-up risk：暂缓处理会留下什么风险。

## Default Decision Rules

- 先复用现有 steward 和 checker，不先新增组件。
- 先用 proposal 或文档规则承接稳定变化，再决定是否需要 harness 化。
- 只读审计和写报告审计必须分开说清楚。
- 生成器相关变更不能只改一个文件；必须检查 template、schema、prompt、renderer、sample output 和 regression。
- 自动化不能因为是定时任务就拥有更高权限；它只能记录、汇报和提出方案，除非用户明确批准执行稳定修改。

## Detachable Workflow Policy

- `ai_solution_planning` 暂不并入主 PRD workflow。只有当项目明确包含 AI 能力，或用户批准进入 AI 方案阶段时，才作为 detachable workflow 启动。
- detachable workflow 可以读取 PRD、页面说明、页面跳转关系、埋点计划和风险报告，但不得反向改写主 PRD 产物，除非形成变更建议并经用户确认。
- `registry/artifacts.yaml` 中属于 detachable workflow 的 AI 产物必须标注 `detachable_workflow: ai_solution_planning`，避免被主流程 gate 误判成主链路必备输出。
