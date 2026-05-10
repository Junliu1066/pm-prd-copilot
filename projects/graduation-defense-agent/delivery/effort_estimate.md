# Effort Estimate：毕业答辩辅导智能体

estimate_id: `effort-estimate-20260425`

## Team Assumptions / 团队假设

- frontend: 1 名前端工程师，负责 Web/H5 页面。
- backend: 1 名后端工程师，负责 API、会话、数据模型。
- ai_model: 1 名 AI/全栈工程师，负责 Prompt、模型调用、回退规则。
- qa: 1 名测试兼职投入。
- pm_design_review: 1 名 PM/设计兼职评审交互和验收。

> 估算是规划指导，不是交付承诺。真实工期会受团队熟练度、模型供应商、设计稿质量和测试标准影响。

## Module Estimates

| module_id | 模块 | frontend_days | backend_days | ai_model_days | qa_days | integration_days | uncertainty |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| FE-01 | 新建训练页 | 2 | 0 | 0 | 0.5 | 0.5 | low |
| FE-02 | 模拟答辩页 | 3 | 0 | 0 | 1 | 1 | medium |
| FE-03 | 训练报告页 | 2 | 0 | 0 | 0.5 | 0.5 | low |
| API-01 | 训练会话服务 | 0 | 2 | 0 | 0.5 | 0.5 | low |
| API-02 | 问题生成与追问服务 | 0 | 2 | 2 | 1 | 1 | medium |
| API-03 | 回答评价服务 | 0 | 2 | 2 | 1 | 1 | medium |
| API-04 | 报告与复练服务 | 0 | 2 | 1 | 0.5 | 0.5 | medium |
| DB-01/02 | 数据模型 | 0 | 2 | 0 | 0.5 | 0.5 | low |
| SEC-01 | 隐私与拦截 | 0.5 | 1 | 1 | 1 | 0.5 | medium |
| ANA-01 | 埋点 | 0.5 | 0.5 | 0 | 0.5 | 0.5 | low |

## Phase Estimates

| phase_id | duration_range | critical_path | buffer |
| --- | --- | --- | --- |
| MVP | 3.5 - 5 周 | 模型调用与评分质量、训练会话、报告生成 | 20%，用于 Prompt 调试、联调和回归 |
| V1 | 3 - 4 周 | PPT 大纲输入、历史趋势、题库扩展 | 20%，用于题库质量和体验打磨 |
| V1.5 | 4 - 6 周 | 导师授权、班级管理、批量报告 | 25%，用于多角色权限和数据隔离 |
| Future | 按专题拆分 | 语音/视频、组织级质量看板、知识图谱 | 需单独技术方案 |

## Buffer Policy / 风险预留

- MVP 默认增加 20% buffer，因为 AI 评分、追问质量和学术诚信边界需要多轮调试。
- V1.5 增加 25% buffer，因为权限、组织和批量报告有更高测试成本。
- QA、联调、验收评审必须纳入工期，不允许只估开发编码时间。

## Estimate Risks

- 模型输出不稳定：需要 Prompt 回归样例和兜底规则。
- 学术诚信边界难控：需要违规请求样例库。
- 用户输入论文材料质量差：需要资料不足模式和占位提示。
- 如果 MVP 加语音输入，工期至少增加 1.5 - 2.5 周。
