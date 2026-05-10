# 一期 Codex 执行文档：MVP 文字版训练闭环

## 1. 阶段目标

一期目标是打通毕业答辩辅导智能体的 MVP 文字训练闭环。用户可见效果是：学生录入论文资料后，完成模拟答辩、获得追问和五维评分、查看单题复盘、生成训练报告，并从报告进入复练。

## 2. 本期输入

- PRD 产品包：`projects/graduation-defense-agent/02_prd.generated.md`，包含产品判断、功能矩阵、流程图和原型图说明。
- 产品包同步拆分文件：
  - 功能矩阵：`projects/graduation-defense-agent/feature_matrix.md`
  - 流程图：`projects/graduation-defense-agent/prototype/product_flow.md`
  - MVP 原型图：`projects/graduation-defense-agent/prototype/prototype_preview.md`
  - 全量原型图：`projects/graduation-defense-agent/prototype/full_prototype.md`，一期只实现 P1-P6
- AI 方案：`projects/graduation-defense-agent/ai/ai_capability_map.md`
- 本期只实现 MVP P0 能力。

## 3. 本期范围

包含：

- 论文资料录入和资料完整度判断。
- 训练模式选择。
- 问题库结构化和抽题。
- 文字作答。
- 动态追问。
- 五维评分。
- 单题复盘和示范改写。
- 训练报告和复练计划。
- 学术诚信拦截。
- 删除论文资料和训练记录。

不包含：

- 语音、视频、导师端、机构后台。
- 上传完整论文并自动解析。
- 学校规范库。
- 支付和商业化。

## 4. 总体框架

| 层 | 一期内容 |
| --- | --- |
| 前端 | 新建训练页、模拟答辩页、单题复盘页、训练报告页 |
| 后端 | 资料、训练、问题、回答评价、报告、复练、风控 |
| 数据 | ThesisProfile、QuestionItem、TrainingSession、AnswerEvaluation、TrainingReport、RetryPlan |
| AI / Prompt / RAG / Memory | 问题生成、追问、评分、改写、复练计划、诚信拦截；一期不做复杂 RAG |
| Skill / MCP | 复用现有 PM/Delivery/AI/Agentic skills；一期不接外部 MCP |
| Harness | agentic_delivery、ai_solution、efficiency、random_audit |
| GitHub / PR | 完成一期后按任务包提交 PR，不直接推送未评审实现 |
| 教学 / 记忆 | 用户对文档分层和 Codex 开发规则的反馈进入通用 Skill 提案 |

## 5. 页面与交互

| 页面 | 用户动作 | 系统反馈 | 异常状态 |
| --- | --- | --- | --- |
| 新建训练 | 填论文资料、选训练模式 | 显示资料完整度并生成题组 | 资料不足进入通用训练 |
| 模拟答辩 | 输入并提交回答 | 返回评分、追问或进入复盘 | 空回答提示重答 |
| 单题复盘 | 查看扣分原因和示范改写 | 标出待补充论文依据 | 缺事实只显示占位 |
| 训练报告 | 查看薄弱模块并开始复练 | 生成复练题单 | 删除前二次确认 |

## 6. 服务与数据

| 服务 | 数据对象 | 说明 |
| --- | --- | --- |
| 论文资料服务 | ThesisProfile | 保存资料、计算完整度、删除资料 |
| 训练会话服务 | TrainingSession | 创建训练、维护题目序列 |
| 问题服务 | QuestionItem | 题库读取、按模式抽题 |
| 评价服务 | AnswerEvaluation | 评分、追问、示范改写 |
| 报告服务 | TrainingReport、RetryPlan | 训练总结和复练题单 |
| 风控服务 | moderation result | 代写、编造、规避检测拦截 |

## 7. AI / Prompt / RAG / Memory

| 能力 | 一期实现 | 兜底 |
| --- | --- | --- |
| 问题组生成 | 题库规则 + 模型辅助个性化 | 固定通用题组 |
| 动态追问 | 模型按回答质量追问 | 固定追问模板 |
| 五维评分 | 模型按 rubric 输出 | 手动评分提示 |
| 示范改写 | 模型重组表达 | 通用回答框架 |
| 诚信拦截 | 规则优先，模型辅助 | 规则拦截 |
| Memory | 当前训练 session 和论文资料 | 无持久画像 |

## 8. Skill / MCP 接入

| 类型 | 一期策略 |
| --- | --- |
| Skill | 复用 `agentic-delivery-orchestrator`、AI planning、delivery planning、prototype skills |
| 新 Skill | 不在一期直接创建，除非题库结构化反复出现高成本操作 |
| MCP | 一期不接外部 MCP |
| Source trace | 外部信号不进入一期核心判断 |

## 9. Codex 任务包

| task_id | goal | allowed_write_paths | forbidden_write_paths | validation | human_confirmation_points |
| --- | --- | --- | --- | --- | --- |
| P1-T1 | 建立题库数据和抽题规则 | `app/data/**`, `app/services/question*` | `projects/**/02_prd.generated.md` | 单场不重复抽题 | 题库结构 |
| P1-T2 | 实现训练会话主链路 | `app/services/training*`, `app/api/training*` | `memory-cache/**` | 创建、开始、完成训练 | 数据模型 |
| P1-T3 | 实现回答评价和追问 | `app/services/evaluation*`, `app/ai/**` | `plugins/**` | 固定样例评分稳定 | 模型调用 |
| P1-T4 | 实现前端四页面 | `web/**`, `app/static/**` | `projects/**/delivery/**` | 页面流程可走通 | UI 评审 |
| P1-T5 | 实现报告、复练、删除 | `app/services/report*`, `app/services/retry*` | `projects/**/02_prd.generated.md` | 报告生成、删除可用 | 隐私文案 |
| P1-T6 | 风控和学术诚信拦截 | `app/services/moderation*`, `app/ai/**` | `pm-prd-copilot/memory/**` | 高风险样例拦截 | 拦截策略 |

最小修复策略：任务失败时只修当前任务允许路径，不扩大到 PRD、Skill、MCP 或记忆。

## 10. 人工确认点

- 一期是否允许游客模式。
- 数据存储方案。
- 是否接外部模型以及模型供应商。
- 学术诚信拦截文案。
- 删除资料的不可恢复提示。

## 11. GitHub / 发布流程

- 分支：`codex/graduation-defense-phase-1`
- PR 内容：一期 MVP 文字训练闭环。
- PR 前检查：单元测试、主路径手测、harness、Prompt 样例回归。
- 回滚：保留旧题库和旧页面入口，AI 调用可关闭。

## 12. Harness / 审计 / 回归

- `harness/run_harness.py --project graduation-defense-agent --mode advisory --audit --efficiency`
- Prompt 回归：空泛回答、完整回答、编造数据、回避不足、答非所问。
- 审计重点：PRD 不被开发任务改写，模型不编造论文事实。

## 13. 教学与记忆沉淀

- 用户对一期页面、流程、报告的修改建议先进入项目候选偏好。
- “文档分层”“每期 Codex 文档”进入通用 Skill 更新提案。
- 评分或追问策略若可跨项目复用，进入 open lesson。
- 任何 stable memory 或 Skill 更新必须人工批准。

## 14. 风险与回滚

| 风险 | 回滚 |
| --- | --- |
| 模型幻觉 | 关闭个性化生成，使用通用题组 |
| 评分不稳定 | 退回模板评分提示 |
| 用户挫败 | 降低追问强度 |
| 隐私问题 | 暂停保存历史，仅本地 session |

## 15. 验收标准

- 主流程完整可用。
- 资料不足时不编造事实。
- 高风险请求可拦截。
- 删除资料和训练记录可用。
- 报告可自然进入复练。
- Harness 无 fail。

## 16. 下一期衔接

一期输出训练历史、薄弱模块和题库标签，为二期的 PPT/章节训练、历史趋势、专项复练提供基础。
