# Agentic Delivery Plan：毕业答辩辅导智能体

agentic_delivery_id: `agentic-delivery-20260425`

## development_departments

| 部门 | 小管家 | 职责 | 不能做 |
| --- | --- | --- | --- |
| 产品部门 | Product steward | 维护 PRD 范围、验收标准、需求变更记录 | 未经确认改 MVP 范围 |
| 前端部门 | Frontend steward | Web/H5 页面、状态流、交互和可见反馈 | 私自新增业务模块 |
| 后端部门 | Backend steward | API、数据模型、权限、删除能力 | 跳过数据迁移审查 |
| AI 部门 | AI steward | model_gateway、Prompt、RAG、评分、fallback | 未经 benchmark 换模型 |
| 测试部门 | QA steward | 单测、接口测试、Prompt 回归、主路径验收 | 没有证据就标记完成 |
| 审核部门 | Review steward | 代码审查、安全、越界、隐私和学术诚信 | 直接替代产品决策 |
| 效率部门 | Efficiency steward | 检查重复开发、无效 token、任务拆分过细 | 为省 token 降低质量阈值 |
| 能力启用部门 | Capability enablement steward | 判断 skill_reuse_decision、新 Skill、MCP、harness 是否需要先建 | 未经确认直接更新 Skill |
| Skill/MCP 路由部门 | Skill/MCP routing steward | 负责 source_trace、MCP 边界、Skill 边界、fallback | 让 MCP 直接决定 PRD/MVP |
| 教师/学习部门 | Teacher + Learning steward | 吸收用户教学，区分项目缓存和通用 Skill 提案 | 未经用户批准直接写入通用 Skill |

## capability_enablement

- skill_reuse_decision: 先复用现有 PRD、AI、delivery、prototype、preference、quality Skills；缺口只生成 proposal 或候选。
- new_skill_route: 新 Skill 必须进入 capability_enablement_plan，并经过 human_approval_required。
- mcp_route: MCP 只提供外部信号和 source_trace，不直接做产品决策。
- harness_route: 新能力必须接 registry、plugin_boundary、source_trace、skill_generalization、agentic_delivery 等检查。

## skill_mcp_routing

- stage_routing: 由 skill_mcp_routing_plan 定义每阶段可用 Skill/MCP 和 steward_assignment。
- source_trace: 所有外部模型、竞品、价格、官方文档信号都必须记录来源并提醒人工核验。
- fallback: MCP 不可用时使用用户资料、历史缓存或人工补充；Skill 不足时生成 proposal，不直接写产品代码。

## governance_operating_system

- chief_steward: pm-copilot-chief 负责总调度和升级。
- sub_stewards: capability-enablement、development-governance、delivery、AI、learning 等小管家分工管理。
- random_audit: 随机检查 Skill/MCP/产物是否越界。
- efficiency_audit: 检查无效 token、重复输出和无效流转。
- teacher: 吸收用户教学，但不能自己批准 Skill 更新。
- preference_cache: 项目偏好和通用经验分开。
- skill_update_proposal: 通用经验走提案、审批、回归。

## phase_execution

| phase | 目标 | 主要任务 | 交付效果 |
| --- | --- | --- | --- |
| Phase 0 | 仓库理解和技术方案确认 | 读现有结构、确认框架、确认数据存储和模型调用方式 | 输出开发计划，不写核心代码 |
| Phase 0.1 | 能力启用和治理检查 | 确认 Skill/MCP/harness/registry/管家是否需要扩展 | 缺口先补 proposal 或治理产物 |
| Phase 1 | 数据模型和 API 契约 | 训练会话、题库、回答、评分、报告、删除能力 | 前后端可以基于契约并行 |
| Phase 2 | 核心后端能力 | 创建训练、抽题、提交回答、报告、复练 | 后端主链路可用 |
| Phase 3 | AI 能力接入 | model_gateway、Prompt registry、评分/追问/改写、fallback | 规则版和模型版双路径 |
| Phase 4 | 前端主路径 | 新建训练、模拟答辩、报告、复练页面 | 用户能走完整 MVP |
| Phase 5 | 测试和观测 | 主路径测试、Prompt 回归、隐私删除、埋点检查 | 达到发布前验收标准 |
| Phase 6 | 人类验收和迭代 | 用户审阅、问题修复、任务包更新 | 进入下一轮最小修复 |

## conflict_rules

- 同一时间不安排两个任务写同一目录，除非明确冲突处理人。
- 产品范围、数据库 schema、模型选择、外部 API、删除逻辑和 GitHub 推送必须人工确认。
- Codex 任务失败时按 minimal_fix_strategy 修复，不大范围重构。
- AI 输出、外部资料和模型动态只能作为信号，需要人工验证真实性。

## feedback_learning_loop

1. 人类审阅开发输出。
2. 将反馈分类为 bug、体验问题、PRD 范围变更、技术债、AI 质量问题或 Skill 改进。
3. 项目偏好进入项目缓存。
4. 通用方法进入 Skill 更新提案。
5. 用户批准后才更新 Skill 或 harness。
6. 回归评测通过后再继续下一批任务。
