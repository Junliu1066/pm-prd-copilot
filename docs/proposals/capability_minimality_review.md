# 新增能力最小化审计报告

- Date: 2026-04-29
- Scope: plugin suites, skill candidates, harness/eval expansion, helper scripts, package templates, UI design support, and marketplace exposure.
- Rule: this report is advisory only. It does not approve cleanup, deletion, archive, staging, commit, push, plugin promotion, skill promotion, or harness promotion.
- Governance principle: 如无必要，不增 skill，不增 harness。

## Executive Summary

当前新增能力不是同一种风险；用户已确认 7 点落地策略，本报告同步为执行状态：

- 6 个 plugin suite 继续可见，但必须显式标记 `candidate` / `requires review` / `non-stable capability`，不能被当成 stable 自动使用。
- `eval_suite`、`real_output_eval`、`skill_generalization`、`prototype_preview_gate`、`external_redaction` 是已批准的最小稳定检查层。
- `delivery_plan`、`ai_solution`、`agentic_delivery`、`preference_cache` 继续按需触发，不扩大成每个项目默认必经主流程。
- B 包脚本已从项目硬编码方向转为通用外部分发打包器方向，并通过回归检查保护。
- 项目偏好机制启动，但限定为项目内缓存、closeout/归档对齐、默认不跨项目复用，长期记忆必须经用户明确批准。
- 2026-04-29 用户进一步确认：candidate plugin 暂不转 stable；5 个必要检查稳定保留；golden sample 先候选，后续收集多篇 PRD 后再迭代；0-1 PRD 收件箱逐条批准；项目偏好缓存归档前对齐；root 删除接受候选但保留 canonical / archive；历史 PRD 回扫延后；工作区分区提交。

## Confirmed Governance Direction

| Area | Confirmed direction | Operational boundary |
|---|---|---|
| Candidate plugins | Do not promote to stable now. | Keep candidate / detachable; project-specific use only. |
| Necessary checks | Keep stable. | `eval_suite`, `real_output_eval`, `skill_generalization`, `prototype_preview_gate`, and `external_redaction` are the minimum protection layer. |
| Golden sample | Keep as candidate. | Collect multiple PRDs before creating a stable golden sample portfolio. |
| Architecture inbox | Approve item by item. | Inbox evidence cannot automatically become prompt, template, regression, or long-term memory. |
| Project preference cache | Keep until archive alignment. | Do not cross project boundaries; long-term memory still requires explicit approval. |
| Root deletion state | Accept as deletion candidate with canonical/archive retained. | No hard delete until the retention window and exact approval. |
| Historical PRD sweep | Defer. | Stabilize the architecture first, then choose active projects for review. |
| Workspace submission | Split by partition. | Stable architecture, project artifacts, archive candidates, and experimental capabilities must not be mixed. |

This direction follows two standing principles:

- 如无必要，不增 skill，不增 harness。
- 长期稳定可靠优先；能用一行清晰代码解决，就不扩展成多行、额外抽象或新增组件。

## Decision Scale

| Action | Meaning |
|---|---|
| `keep_in_architecture` | 建议进入稳定架构资产，但仍需你确认后才能作为稳定变更提交。 |
| `keep_detachable_candidate` | 保留为可拆卸候选能力，只在项目明确需要时使用，不进入默认主链路。 |
| `defer_not_stable` | 暂缓稳定化；保留现场证据或草案，但不要把它当成可复用能力。 |
| `archive_candidate` | 后续可归档，归档前需提取有用信息并经你确认。 |
| `delete_after_30_days_candidate` | 仅适用于低价值生成物；先归档或记录，30 天后经你精确批准再硬删除。 |

## Plugin Suite Review

| Capability | Current use | Existing alternative | Writes files | Cost / risk | Recommendation | Reason |
|---|---|---|---|---|---|---|
| `prd-analysis-suite` | 拆分需求收集、用户、竞品、场景、MVP 判断 | 主 pipeline 和 PRD prompt 也能完成基础 PRD | Plugin skills may write analysis artifacts | 6 个 skills，维护成本中等 | `keep_detachable_candidate` | 有助于 0-1 PRD 前置分析，但不应替代默认 pipeline；适合复杂项目时按需调用。 |
| `prd-prototype-suite` | 原型参考、业务流、中保真/低保真预览、HTML 原型 | PRD 默认只需要页面说明和页面跳转关系 | Writes prototype artifacts when used | 容易重新引入“PRD 默认线框图”问题 | `keep_detachable_candidate` | 与用户确认的原型链路匹配，但必须继续受“先预览、后 HTML/UI”的监督门禁约束。 |
| `preference-memory-suite` | 项目级偏好缓存 | teaching docs + memory proposal 可以记录候选学习 | Writes `memory-cache/` | 隐私、误学习、跨项目污染风险高 | `keep_detachable_candidate` | 已启动项目内偏好机制，但只能项目内读取；归档前进入 closeout 对齐，长期记忆仍需用户批准。 |
| `quality-evaluation-suite` | 审计 Skill 泛化与项目偏好泄漏 | regression 能查 PRD 输出，但不专门查 Skill 过拟合 | Read-oriented plugin; reports may be written by harness | 维护成本低，治理收益高 | `keep_detachable_candidate` | 能补上“用户教过的东西被错误泛化”的风险，但作为 plugin 仍保持 candidate；对应 eval/harness 可稳定。 |
| `delivery-planning-suite` | Codex 开发文档、技术拆分、交付计划、能力启用、路由、开发治理 | 普通开发文档模板可覆盖基础交付 | Writes delivery and Codex planning artifacts when used | 11 个 skills，范围最大，最容易膨胀 | `keep_detachable_candidate` | 用户已确认“开发文档=Codex 开发文档”，但这套能力只能在进入开发文档阶段时调用。 |
| `ai-solution-planning-suite` | AI 能力、模型、prompt、RAG、记忆、profile、coaching、AI 架构 | PRD 中只在涉及 AI 时写产品级 AI 约束 | Writes AI solution artifacts when used | 模型/成本/隐私/外部事实时效性风险高 | `keep_detachable_candidate` | 只适合 AI 项目或用户明确要求 AI 架构时进入；不得默认注入非 AI PRD。 |

## Harness / Eval Review

| Capability | Trigger | Writes files | Recommendation | Reason |
|---|---|---|---|---|
| `evals/skill_quality_cases.yaml` | regression / real-output eval | No | `keep_in_architecture` | 用户已确认 5 个必要检查稳定保留；本套样例覆盖 PRD 视觉图表放置、页面说明、页面跳转、非 AI 不默认模型选型，是防止这轮退化复发的核心样例集。 |
| `evals/run_real_output_eval.py` | 手动或定时真实输出评估 | Writes eval report when run | `keep_in_architecture` | 用户已确认 5 个必要检查稳定保留；真实输出 eval 比单纯 schema 更能发现“输出越来越差”的问题。 |
| `evals/generalization_audit.yaml` | Skill 泛化泄漏扫描 | No | `keep_in_architecture` | 用户已确认 5 个必要检查稳定保留；直接服务“用户教的内容不能乱变成通用规则”。 |
| `harness/eval_suite_checker.py` | default harness | Writes only when `--write-report` | `keep_in_architecture` | 用户已确认 5 个必要检查稳定保留；复用现有 harness，不新增入口。 |
| `harness/real_output_eval_checker.py` | default harness | Writes only when `--write-report` | `keep_in_architecture` | 用户已确认 5 个必要检查稳定保留；防止“评估跑了但真实输出没过”的错位。 |
| `harness/skill_generalization_checker.py` | default harness | Writes only when `--write-report` | `keep_in_architecture` | 用户已确认 5 个必要检查稳定保留；防止 Skill 或 skill-update proposal 吸收项目特定偏好。 |
| `harness/external_redaction_checker.py` | optional `--external-package` | No | `keep_in_architecture` | 用户已确认 5 个必要检查稳定保留；内部版 / 外部 B 包边界需要红线扫描。 |
| `harness/prototype_preview_gate_checker.py` | default harness, project trace based | No | `keep_in_architecture` | 用户已确认 5 个必要检查稳定保留；保护“先页面说明/跳转关系，再经你确认进入 PNG/HTML/UI”的原型链路。 |
| `harness/delivery_plan_checker.py` | only when delivery planning requested | No | `keep_detachable_candidate` | 交付规划不是每个 PRD 必备，适合保留为按需检查。 |
| `harness/ai_solution_checker.py` | only when AI solution requested | No | `keep_detachable_candidate` | AI solution 是 detachable workflow，不应进入默认 PRD 主流程。 |
| `harness/agentic_delivery_checker.py` | only when Codex development planning requested | No | `keep_detachable_candidate` | 对 Codex 开发文档有价值，但只在开发文档阶段触发。 |
| `harness/preference_cache_checker.py` | when project caches exist | No | `keep_detachable_candidate` | 检查项目缓存的项目内隔离、归档对齐和长期记忆审批边界；不作为无缓存项目的新增负担。 |
| `evals/__pycache__/` | Python cache | No architecture value | `delete_after_30_days_candidate` | 纯运行缓存；本轮不删除，只列入后续清理候选。 |

## Script / Template Review

| Capability | Current use | Writes files | Recommendation | Reason |
|---|---|---|---|---|
| `pm-prd-copilot/scripts/closeout_project.py` | 项目完成后做总结、学习提取、清理建议 | Yes, writes closeout report/package | `keep_in_architecture` | 直接支撑“清理前先总结反思，反哺架构”，且默认是 dry-run report only。 |
| `pm-prd-copilot/scripts/manage_preference_cache.py` | 初始化、重置、清除、归档对齐清除项目偏好缓存 | Yes, writes `memory-cache/` and closeout disposition | `keep_detachable_candidate` | 已补项目内、归档对齐、禁止跨项目复用和长期记忆审批字段；只在项目需要偏好连续性时启用。 |
| `pm-prd-copilot/scripts/package_b_delivery.py` | 生成 B 执行包并做 protected-term scan | Yes, writes package zip | `keep_in_architecture` | 已去除 Jiaxiaoqian 硬编码，改为基于项目目录生成通用英文短文件名包，并由 redaction 检查保护。 |
| `pm-prd-copilot/scripts/package_internal_delivery.py` | 生成内部完整包 | Yes, writes package zip | `keep_detachable_candidate` | 内部版/外部版分发规则需要它，但应先和真实项目目录结构进一步对齐。 |
| `pm-prd-copilot/scripts/select_ui_style.py` | 根据项目内容生成 UI 风格方向 | Yes, writes project prototype style files | `keep_detachable_candidate` | 支撑 UI 设计方向，但必须保持“人工确认后进入 UI/HTML”的链路。 |
| `pm-prd-copilot/templates/codex_development_document_template.md` | 内部 Codex 开发文档模板 | No by itself | `keep_in_architecture` | 用户已确认“开发文档默认是 Codex 开发文档”，模板是必要资产。 |
| `pm-prd-copilot/templates/external_protected_development_document_template.md` | 外部 B 包受保护模板 | No by itself | `keep_in_architecture` | 解决内部治理机制不能暴露给外部的问题。 |
| `pm-prd-copilot/ui-design/` | UI 风格目录和质量门禁素材 | No by itself | `keep_detachable_candidate` | 可用于 PRD 后的 UI 设计阶段，但不应反向污染 PRD 默认结构。 |

## Marketplace / Registry Risk

| Item | Finding | Risk | Recommendation |
|---|---|---|---|
| `registry/plugins.yaml` | 6 个 plugin 都是 `status: candidate`、`detachable: true` | 状态表达是正确的 | 保持 candidate，不转 active。 |
| `.agents/plugins/marketplace.json` | 6 个 candidate plugin 都保持 `installation: AVAILABLE`，并新增 candidate governance 标识 | 用户或 agent 仍可能误点，但配置层已标明非稳定能力 | 保持可见，但必须继续由回归检查确认 candidate / non-stable / requires review。 |
| `registry/skills.yaml` | plugin-owned skills 均为 `candidate` | 技能数量已经较多，尤其 delivery 11 个、AI 9 个 | 不新增 skill；优先合并、候选、按需使用。 |
| `workflow/actions.yaml` | delivery/prototype/learning actions 已注册 | 主 workflow 与 detachable workflow 的边界需要持续检查 | 继续依赖 workflow gate checker 防漂移。 |

## Cross-Scope Finding

| Item | Finding | Recommendation |
|---|---|---|
| `pm-prd-copilot/SKILL.md` | 已修复旧口径：不再默认要求集中式 `PRD visualization layer`、默认 wireframes、或非 AI 项目的 AI model selection。 | 已完成并验证。继续保持规则：图表放对应章节，PRD 默认输出页面说明和页面跳转关系，PNG / HTML / 完整原型只在用户确认后进入。 |
| PRD 原型图层 | 用户已于 2026-04-29 明确批准加入长期规则；PRD 需要原型图层，但不等于默认 PNG/HTML/UI。 | 已落地为 PRD 默认页面说明、页面跳转关系、原型图层；其他文档默认引用 PRD 或已确认原型。 |

## Latest Validation Record

| Check | Result | Notes |
|---|---|---|
| 旧口径搜索 | pass | `PRD visualization layer`、`Prototype or wireframe diagrams`、`Do not skip the PRD visualization layer`、`Do not skip PRD flowcharts, wireframes, or AI model selection` 在稳定指令层无残留。 |
| `python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict` | pass | PRD regression passed. |
| `python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency` | pass | Harness check-only passed and printed `No project files written`. |
| `git diff --check` | pass | No whitespace diff issues. |
| 7 点治理落地回归 | pass | 已新增 candidate、B 包、偏好缓存、PRD 原型图层相关断言，并通过 regression / harness check-only。 |

## User Decision List

| Decision needed | Recommended answer | Why |
|---|---|---|
| 是否允许 eval / real-output / skill-generalization 相关检查进入稳定架构？ | Confirmed stable | 这组是防止 PRD 质量退化和错误泛化的最小保护层。 |
| 是否允许 prototype preview gate 进入稳定架构？ | Confirmed stable | 它保护用户确认前不进入 PNG/HTML/UI，符合当前原型链路。 |
| 是否允许 external redaction checker 进入稳定架构？ | Confirmed stable | 内部版 / B 包边界已经是明确需求。 |
| 是否让 6 个 plugin suite 转 stable？ | Confirmed no | 全部继续 candidate / detachable；项目需要时再调用。 |
| 是否启动 preference memory suite？ | Confirmed project-local only | 已补审批、保留、清除、敏感信息和跨项目隔离规则；长期记忆仍需单独批准。 |
| 是否稳定 B 包脚本？ | Confirmed after generic pass | 去掉项目硬编码，改成基于项目输入和模板的通用打包器。 |
| 是否硬删除 `evals/__pycache__/`？ | Confirmed not now | 只列入 30 天后候选，等待清理清单审批。 |
| 是否处理 marketplace candidate 可见性？ | Confirmed visible as candidate | candidate plugin 可见但必须显式标记非稳定、需审核。 |

## Recommended Next Actions

1. 把长期治理生命周期方案保持为 proposal，等待用户后续明确批准是否转 stable policy。
2. 用定时周报做人工监督和判断校准，至少跑 2-4 周后再考虑低风险自动化放权。
3. 后续收集多篇 PRD，建立 golden sample portfolio，再决定是否升级稳定样例。
4. 历史 PRD 回扫延后，只在架构稳定后选择活跃项目处理。

## Validation Notes

本报告只新增审计文档。未执行：

- no cleanup
- no delete
- no archive
- no file move
- no git add
- no commit
- no push
- no plugin promotion
- no skill promotion
- no harness promotion
