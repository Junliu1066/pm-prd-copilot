# 稳定核心审查包

- 日期：2026-04-29
- 状态：proposal / 审查包，尚未 staging、commit、push、归档或删除
- 输入依据：`docs/proposals/precise_submission_plan.md`
- 当前工作区基线：`git status --short` 仍为 148 项，包含 `67 M`、`4 D`、`77 ??`
- 最高原则：长期稳定可靠优先；如无必要，不增 skill，不增 harness

## 审查结论

| Unit | Recommendation | Reason |
|---|---|---|
| A1 PRD 主链路与输出口径 | 进入 Stable Core 候选 | 直接压住 PRD 退化、图表错位、非 AI 项目强行模型选型、原型图层缺失。 |
| A2 Pipeline / Workflow / Harness 合同 | 进入 Stable Core 候选 | 直接压住 governed workflow 被 pipeline 绕过、action/artifact 漂移、harness 默认写文件。 |
| A3 5 个必要检查与 eval 基线 | 进入 Stable Core 候选 | 这 5 个检查已被确认必要，覆盖 PRD 质量、真实输出、偏好泛化、原型监督、外部分发泄漏。 |
| A4 B 包 / closeout / Codex 开发文档 / 偏好边界 | 暂缓稳定化 | 价值高，但脚本和模板仍需要真实输出复核；不能把项目缓存、B 包 zip、closeout 产物混进 Stable Core。 |

本审查包只冻结 A1-A3 的候选范围，不批准提交。A4 只记录复核清单。

## A1. PRD 主链路与输出口径

### 文件清单

| Path | Current status | Stable-core role |
|---|---|---|
| `pm-prd-copilot/SKILL.md` | modified | 稳定 skill 入口，约束 PRD 默认输出。 |
| `pm-prd-copilot/references/output_style_guide.md` | modified | 输出风格说明，防止旧口径回潮。 |
| `pm-prd-copilot/references/prd_pm_2026_playbook.md` | modified | PRD playbook canonical copy。 |
| `pm-prd-copilot/templates/prd_template_2026.md` | modified | PRD 模板主入口。 |
| `shared/schemas/prd_document.schema.json` | modified | PRD 结构合同。 |
| `pm-prd-copilot/scripts/pipeline_common.py` | modified | PRD 组装、章节和条件输出逻辑。 |
| `pm-prd-copilot/scripts/prompt_builders.py` | modified | prompt 构建入口。 |
| `pm-prd-copilot/scripts/router.py` | modified | 项目/输出路由。 |

### 当前 diff 摘要

- 8 个 tracked 文件变更。
- 当前 stat：`837 insertions(+), 123 deletions(-)`。
- 主要变化：PRD 图表从集中层改为放在对应章节；PRD 阶段保留页面说明、页面跳转关系和原型图层；非 AI 项目不默认输出 AI 模型选型；模板、schema、prompt、pipeline 逻辑对齐。

### 是否可进入稳定核心

可以，建议作为第一个稳定核心候选单元冻结。原因是 A1 直接决定所有后续 PRD 质量，且当前 regression 已覆盖相关退化风险。

### 风险点

- 模板、schema、prompt、pipeline 如果不同步，会再次出现“文档写对了、输出跑偏了”。
- wording 如果过宽，可能把项目测试经验误写成通用规则。
- 历史项目 PRD 旧口径不能在本单元批量回扫。

### 不能混入

- `projects/*` 生成结果、final PRD、原型、run outputs。
- `plugins/*` candidate suite。
- `harness/*_checker.py` 新增候选检查。
- root 删除项和 `docs/archive/*`。

### 回滚方式

只回滚 A1 文件，不动项目产物、candidate plugin、root 删除项。若回滚后 regression 失败，再单独检查 schema/template/pipeline 的兼容关系。

### 提交前检查

```bash
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

### 需要最后拍板

- PRD 稳定保留页面说明、页面跳转关系、原型图层。
- 非 AI 项目不写 AI 模型选型；AI 项目按项目判断。
- 历史项目 PRD 回扫延后，不混进本次稳定核心冻结。

## A2. Pipeline / Workflow / Harness 治理合同

### 文件清单

| Path | Current status | Stable-core role |
|---|---|---|
| `pm-prd-copilot/scripts/run_pipeline.py` | modified | 默认 governed，显式 `--fast-draft` 才允许草稿绕行。 |
| `pm-prd-copilot/scripts/governance_trace.py` | modified | governance mode 和审批 trace。 |
| `pm-prd-copilot/scripts/run_regression.py` | modified | governed / fast draft / PRD 退化回归。 |
| `workflow/actions.yaml` | modified | action 合同。 |
| `workflow/policies.yaml` | modified | workflow 政策。 |
| `workflow/prd_workflow.yaml` | modified | PRD workflow 和审批门禁。 |
| `registry/artifacts.yaml` | modified | artifact 合同和 raw input 边界。 |
| `registry/stewards.yaml` | modified | steward 责任注册。 |
| `governance/steward_operating_rules.yaml` | modified | steward 操作规则。 |
| `governance/teaching_policy.yaml` | modified | teaching / learning / 长期记忆边界。 |
| `harness/README.md` | modified | harness 模式说明。 |
| `harness/common.py` | modified | harness 共用逻辑。 |
| `harness/run_harness.py` | modified | `--check-only` / `--write-report` 主入口。 |
| `harness/workflow_gate_checker.py` | modified | workflow/action/artifact 漂移检查。 |
| `harness/efficiency_auditor.py` | modified | 效率审计。 |
| `harness/random_audit_inspector.py` | modified | 随机审计。 |

### 当前 diff 摘要

- 16 个 tracked 文件变更。
- 当前 stat：`1365 insertions(+), 83 deletions(-)`。
- 主要变化：pipeline 默认 governed；fast draft 必须显式；manifest/trace 标治理模式；workflow/action/artifact 合同对齐；harness 默认 check-only，写报告必须显式；regression 覆盖默认阻断和 fast draft 放行。

### 是否可进入稳定核心

可以，建议作为第二个稳定核心候选单元冻结。原因是 A2 是治理不被绕过的核心合同层。

### 风险点

- 默认 governed 会阻断缺审批项目，这是预期行为，但可能影响旧测试输入。
- harness 如果 future 调用忘记 `--check-only`，仍可能产生报告文件，所以文档和自动化调用必须保持一致。
- workflow/action/artifact 的新增合同必须继续由 harness 检查，不能只靠人工记忆。

### 不能混入

- `.github/workflows/*` 自动化配置，建议单独作为治理文档/自动化批次。
- `projects/*/runs/*` 运行产物。
- D 批 candidate checker 或 plugin suite。
- root 删除项。

### 回滚方式

只回滚 A2 文件。若 governed 默认过严，先回滚 `run_pipeline.py` / `run_regression.py` 的行为变更，再复核 workflow gate，不回滚项目产物。

### 提交前检查

```bash
python3 -m py_compile pm-prd-copilot/scripts/run_pipeline.py pm-prd-copilot/scripts/run_regression.py harness/run_harness.py harness/workflow_gate_checker.py
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

### 需要最后拍板

- 正式 pipeline 默认 governed。
- `--fast-draft` 是唯一草稿绕行路径。
- harness 日常和 CI 默认 `--check-only`，不写项目报告。

## A3. 5 个必要检查与 eval 基线

### 文件清单

| Path | Current status | Stable-core role |
|---|---|---|
| `harness/eval_suite_checker.py` | untracked | 必要检查：PRD/eval 覆盖。 |
| `harness/real_output_eval_checker.py` | untracked | 必要检查：真实输出基线。 |
| `harness/skill_generalization_checker.py` | untracked | 必要检查：防项目偏好错误泛化。 |
| `harness/prototype_preview_gate_checker.py` | untracked | 必要检查：原型监督边界。 |
| `harness/external_redaction_checker.py` | untracked | 必要检查：外部分发 redaction。 |
| `evals/skill_quality_cases.yaml` | untracked | 质量 case 基线。 |
| `evals/generalization_audit.yaml` | untracked | 泛化审计基线。 |
| `evals/run_real_output_eval.py` | untracked | 真实输出 eval 入口。 |
| `evals/real_outputs/20260425T000000Z/summary.md` | untracked | 真实输出摘要。 |
| `evals/real_outputs/20260425T000000Z/real_output_eval_report.json` | untracked | 真实输出报告。 |
| `evals/real_outputs/20260425T000000Z/cases/*/output.md` | untracked | 5 个真实输出样例。 |

### 当前 diff 摘要

- 15 个 untracked 文件。
- 已检查的 checker / eval 主文件合计约 996 行，不含 JSON 报告和 5 个 case 输出全文。
- 范围只包括已确认的 5 个必要检查：`eval_suite`、`real_output_eval`、`skill_generalization`、`prototype_preview_gate`、`external_redaction`。

### 是否可进入稳定核心

可以，但必须严格限定为这 5 个检查和对应 eval 基线。原因是用户已确认稳定保留这一组，它们直接防 PRD 退化、错误泛化、原型越权和外部分发泄漏。

### 风险点

- 这是新增稳定检查文件，维护成本真实存在。
- eval baseline 不能过拟合单个测试项目，后续需要持续收集多项目证据。
- 不能把按需 checker 混入稳定检查层。

### 不能混入

- `harness/delivery_plan_checker.py`
- `harness/ai_solution_checker.py`
- `harness/agentic_delivery_checker.py`
- `harness/preference_cache_checker.py`
- `plugins/*`
- 项目 run outputs 和 closeout 产物。

### 回滚方式

如果检查过严，优先调整 eval case 或阈值；不要直接删除整组检查。若必须回滚，只回滚 A3 文件，不动 A1/A2。

### 提交前检查

```bash
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

### 需要最后拍板

- 这 5 个检查进入稳定核心。
- 第 6 个及之后的检查仍需单独必要性审计。
- 真实输出基线后续可以迭代，但要汇报给用户，不自动扩大长期规则。

## A4. 真实输出复核清单，暂缓稳定化

### 文件和产物范围

| Path / scope | Current status | Review treatment |
|---|---|---|
| `pm-prd-copilot/scripts/package_b_delivery.py` | untracked, 455 lines | 待真实项目 B 包输出复核。 |
| `pm-prd-copilot/scripts/closeout_project.py` | untracked, 993 lines | 待确认只生成审核材料，不执行归档/删除。 |
| `pm-prd-copilot/templates/codex_development_document_template.md` | untracked, 246 lines | 待确认 Codex 开发文档模板不会泄露内部治理细节到外部版。 |
| `pm-prd-copilot/templates/external_protected_development_document_template.md` | untracked, 159 lines | 待确认外部保护版足够清晰且不过度暴露。 |
| `pm-prd-copilot/rules/distribution_policy.yaml` | untracked, 49 lines | 待确认分发策略可通用。 |
| `pm-prd-copilot/rules/redaction_terms.yaml` | untracked, 36 lines | 待确认保护词覆盖但不过度误杀。 |
| `pm-prd-copilot/rules/external_redaction_policy.md` | untracked, 33 lines | 待确认与 B 包脚本一致。 |
| `pm-prd-copilot/memory/user_preferences.md` | modified, `19 insertions(+), 1 deletion(-)` | 只允许包含已明确批准的长期偏好。 |
| `memory-cache/projects/fitness-app-mvp/*` | untracked | 项目偏好缓存，不进 Stable Core。 |
| `projects/_archives/delivery-packages/*.zip` | untracked | 归档/交付包证据，不进 Stable Core。 |

### 复核结论

A4 暂不进入本轮稳定核心冻结。建议下一轮先做真实输出复核，再决定是否拆成稳定单元：

1. `package_b_delivery.py` 用至少 2 个项目做外部分发输出复核。
2. 输出包必须通过 `external_redaction`，且 README / 短文件名 / 英文 B 包要求符合预期。
3. `closeout_project.py` 必须证明只生成报告，不归档、不删除、不清空缓存。
4. Codex 开发文档模板必须分清内部版和外部保护版。
5. `pm-prd-copilot/memory/user_preferences.md` 只保留用户明确批准的长期偏好。
6. `memory-cache/` 必须保持项目内，不跨项目复用，不自动进入长期记忆。

### 不能混入

- 项目偏好缓存。
- B 包 zip / internal zip / redacted zip。
- `projects/*/closeout/` 五件套。
- `pm-prd-copilot/scripts/package_internal_delivery.py` 候选内部打包器。

### 需要最后拍板

- B 包脚本是否达到通用稳定打包器标准。
- closeout 工具是否只作为审核材料生成器。
- 哪些项目偏好可以在归档时清除、保留为项目档案或进入长期记忆候选。

## 稳定冻结顺序建议

| Order | Unit | Action |
|---:|---|---|
| 1 | A1 | 先冻结 PRD 主链路，防止输出继续退化。 |
| 2 | A2 | 冻结 governed pipeline 和 workflow/harness 合同。 |
| 3 | A3 | 冻结已确认的 5 个必要检查和 eval 基线。 |
| 4 | A4 | 暂缓；真实输出复核后再决定。 |

## 本轮禁止动作

- 不 `git add`。
- 不 commit / push / PR。
- 不删除、恢复、移动、归档。
- 不新增 skill、harness、workflow stage、plugin。
- 不把 A4 提前转 stable。
- 不把 project artifacts、candidate plugin、root 删除项混入 A1-A3。

## 本轮验证记录

生成本审查包后需要运行：

```bash
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

第二轮自查重点：

- 确认本轮只新增或更新 `docs/proposals/stable_core_review_packet.md`。
- 确认工作区没有 staging。
- 确认 harness 运行仍显示 check-only，且不写项目文件。
- 确认 A4 仍是“暂缓稳定化 / 待真实项目验证”。
