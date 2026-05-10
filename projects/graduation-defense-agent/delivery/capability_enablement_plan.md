# Capability Enablement Plan：毕业答辩辅导智能体

plan_id: `capability-enablement-20260425`

## capability_gaps

| gap | impact_on_development | severity |
| --- | --- | --- |
| AI 模型真实评测缺口 | 不能直接确定生产模型，只能先用文档初筛和 fallback | high |
| Prompt 回归样例缺口 | 无法判断评分、追问、改写是否稳定 | high |
| MCP 外部情报接入缺口 | 后续模型动态、竞品信息、价格变化无法自动收集 | medium |
| Skill/MCP 路由缺口 | Codex 开发任务容易只写代码，忽略先扩展 Skill、MCP、harness | high |
| 项目偏好和通用经验分流缺口 | 容易把项目反馈误写进通用 Skill | medium |

## skill_reuse_decision

| need | decision | target_skill | reason | human_approval_required |
| --- | --- | --- | --- | --- |
| 技术开发路径 | reuse_existing | `technical-scope-planner`, `release-roadmap-planner`, `effort-estimator` | 已能输出模块、版本和工期 | false |
| 半自动开发编排 | update_existing | `agentic-delivery-orchestrator` | 需要吸收 Skill/MCP/harness/管家系统 | true |
| 判断是否需要建 Skill/MCP | create_new | `capability-enablement-planner` | 原有 delivery 只管开发，不管能力启用 | true |
| Skill/MCP 分工路由 | create_new | `skill-mcp-routing-planner` | 多 Skill 和 MCP 需要准确调用边界 | true |
| 管家系统落到开发流程 | create_new | `development-governance-orchestrator` | 需要大管家、小管家、随机检查、效率、教师机制统一接入 | true |
| Codex 任务包蓝图 | create_new | `codex-task-package-writer` | 需要把能力启用、MCP、harness、产品代码任务统一打包 | true |

## new_skill_candidates

| skill | purpose | owner_steward | detachable | approval_status |
| --- | --- | --- | --- | --- |
| `capability-enablement-planner` | 判断复用、更新、创建 Skill 和接入 MCP | capability-enablement-steward | true | proposal_approved_for_this_run |
| `skill-mcp-routing-planner` | 给每阶段分配 Skill、MCP、source_trace、fallback | capability-enablement-steward | true | proposal_approved_for_this_run |
| `development-governance-orchestrator` | 把管家、随机检查官、效率部、教师、记忆、harness 接入开发 | development-governance-steward | true | proposal_approved_for_this_run |
| `codex-task-package-writer` | 生成 Codex 可执行任务包蓝图 | development-governance-steward | true | proposal_approved_for_this_run |

## mcp_candidates

| mcp | purpose | allowed_outputs | forbidden_outputs | source_trace_required | human_verification_required |
| --- | --- | --- | --- | --- | --- |
| fetch/firecrawl 类网页抓取 | 收集模型官方文档、价格页、竞品页面 | external_signal, source_trace | prd_scope, mvp_scope, model_final_decision, skill_update | true | true |
| GitHub connector | 读取/推送仓库、创建 PR、检查 CI | repo_signal, pr_status | destructive_reset, unapproved_push | true | true |
| browser-use | 本地预览前端、截图检查 | local_preview_signal | product_scope_decision | false | true |
| future app-store/review MCP | 收集应用商店、评论、榜单 | app_review_signal | mvp_final_decision | true | true |

## harness_requirements

| check_name | guards | failure_mode |
| --- | --- | --- |
| registry | Skill、MCP、steward、artifact 是否注册一致 | fail |
| plugin_boundary | 插件是否可拔插、是否引用宿主私有路径 | fail |
| source_trace | MCP 外部数据是否有来源和人工核验标记 | fail |
| skill_generalization | 通用 Skill 是否吸收项目特有偏好 | fail |
| ai_solution | AI 方案是否包含模型候选池、benchmark、Prompt、RAG、记忆和评审 | fail |
| agentic_delivery | 半自动开发是否包含能力启用、Skill/MCP 路由、治理系统和任务包 | fail |
| random_audit | 随机抽查 Skill/MCP 是否越界 | advisory/pass |
| efficiency | 检查无效 token、重复产物、过多调用 | advisory/pass |

## memory_learning_route

- project_preferences: 只进入本项目偏好缓存，不写入通用 Skill。
- generic_lessons: 进入 teaching lesson，再生成 Skill 更新提案。
- rejected_or_unclear_items: 进入 open lesson，等待用户确认。
- human_approval_required: 所有 Skill 更新、MCP 接入、harness 规则变更都需要用户确认。
