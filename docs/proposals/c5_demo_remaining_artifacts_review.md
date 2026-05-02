# C5 Demo 剩余项目产物审查

## 结论

本轮只审查 `demo-project` 剩余项目产物，不提交项目文件、不删除、不恢复、不归档。

当前判断：

- `projects/demo-project` 的已跟踪生成稿改动不适合提交，因为当前改动让用户故事、风险检查和埋点计划从具体业务判断退化成通用占位内容。
- `runs/pipeline-latest` 新增的 eval / real-output / skill-generalization 报告有治理证据价值，但不能和退化的生成稿混在同一批提交。
- `closeout/` 是项目收口证据，可以作为 C 批项目证据候选，仍需你确认是否提交。
- `prototype/` 里的 PNG 和 UI 风格方向是项目原型过程产物，暂不进入治理稳定提交。

## 当前文件状态

| 区域 | 状态 | 判断 |
|---|---|---|
| `01_requirement_brief.md` 和 meta | 已跟踪修改 | 增加了待确认问题分级，有一定价值，但不应单独提交，需和完整 fixture 质量一起处理。 |
| `03_user_stories.generated.md` | 已跟踪修改 | 明显退化：原本具体的客服、商家、内部财务、权限管理员故事被压缩成通用故事。 |
| `04_risk_check.generated.*` | 已跟踪修改 | 明显退化：原本权限、字段口径、敏感字段、性能、审计等高价值风险被压缩成通用风险。 |
| `05_tracking_plan.generated.md` | 已跟踪修改 | 明显退化：原本细粒度事件和 QA 口径被压缩成通用埋点。 |
| `runs/pipeline-latest/harness_report.json` | 已跟踪修改 | 增加了更多治理检查结果，有价值，但应和 run evidence 单独处理。 |
| `runs/pipeline-latest/efficiency_report.json` | 已跟踪修改 | 跟随退化生成稿变化，不能单独作为质量提升证据。 |
| `runs/pipeline-latest/eval_suite_report.json` | 未跟踪 | 治理检查证据，可后续单独提交。 |
| `runs/pipeline-latest/real_output_eval_status.json` | 未跟踪 | 治理检查证据，可后续单独提交。 |
| `runs/pipeline-latest/skill_generalization_audit.json` | 未跟踪 | 治理检查证据，可后续单独提交。 |
| `closeout/` | 未跟踪 | 项目 closeout 证据，先保留候选，不混入稳定治理。 |
| `prototype/` | 未跟踪 | 项目原型和 UI 过程产物，暂不提交。 |

## 功能 / 架构影响

如果直接提交当前 demo 修改：

- 好处：工作区会更干净，pipeline-latest 的新检查结果能被记录。
- 坏处：demo fixture 的业务质量会下降，后续 real-output eval 可能把更差的生成稿当成基准。
- 风险：这会和我们前面修复的 PRD 退化问题冲突。

如果本轮只提交审查报告：

- 好处：保留判断依据，不污染 demo fixture。
- 坏处：项目文件仍然留在工作区，需要后续再处理。
- 风险：如果后续没有继续收口，工作区仍会有项目产物噪音。

我的建议：本轮只提交本审查报告；下一步单独做 `demo-project` 最小 fixture 修复方案。

## 后续推荐路线

### 路线 A：保护 demo fixture 质量

推荐。

处理方式：

- 不提交当前退化的 generated PRD / stories / risk / tracking 改动。
- 后续单独决定是恢复到已跟踪版本，还是重新用稳定后的 pipeline 生成一版更好的 fixture。
- run evidence 只有在和高质量 fixture 对齐后再提交。

效果：

- demo fixture 继续作为治理测试样例，不被低质量输出污染。
- 工作区会多保留一段时间的项目改动，需要后续清理。

### 路线 B：提交当前项目现场

不推荐。

处理方式：

- 提交当前所有 demo 修改、closeout、prototype 和 run evidence。

效果：

- 工作区最干净。
- 但会把退化产物、项目原型、closeout 证据混在一起，长期治理风险高。

### 路线 C：只提交 run evidence

暂缓。

处理方式：

- 只提交新增的 3 个 run evidence 和更新后的 harness report。

效果：

- 能保留检查证据。
- 但如果核心 generated 文件仍是退化状态，run evidence 的解释会不完整。

## 需要你后续拍板

| 拍板项 | 我的建议 | 原因 |
|---|---|---|
| 是否提交当前 demo generated 改动 | 不提交 | 当前内容退化，不适合作为 fixture。 |
| 是否提交 demo closeout | 暂缓 | closeout 是项目证据，不应和 fixture 修复混在一起。 |
| 是否提交 demo prototype PNG | 暂缓 | PNG 是项目过程产物，体积较大，且不属于稳定治理最小集。 |
| 是否提交 run evidence | 暂缓到 fixture 修复后 | 避免检查证据和退化产物绑定。 |
| 是否恢复或重生成 demo fixture | 后续单独处理 | 需要明确最小高质量 fixture 范围。 |

## 本轮不做

- 不提交 `projects/demo-project/*`。
- 不删除或恢复项目文件。
- 不归档项目。
- 不提交 `memory-cache/`。
- 不提交 `ai-intel/raw/`。
- 不修改 skill、harness、workflow、registry。
