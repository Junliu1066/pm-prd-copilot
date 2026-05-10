# Technical Scope：毕业答辩辅导智能体

scope_id: `technical-scope-20260425`

## Source Artifacts

- `projects/graduation-defense-agent/02_prd.generated.md`
- `projects/graduation-defense-agent/prototype/product_flow.md`
- `projects/graduation-defense-agent/prototype/prototype_preview.md`

## Technical Modules

| module_id | 模块 | layer | included_work | excluded_work | dependencies |
| --- | --- | --- | --- | --- | --- |
| FE-01 | 新建训练页 | frontend | 论文信息录入、训练模式选择、资料不足提示 | 文件上传解析 | PRD 输入字段 |
| FE-02 | 模拟答辩页 | frontend | 问题卡、回答输入、追问展示、评分反馈 | 语音输入、视频模拟 | API-02 |
| FE-03 | 训练报告页 | frontend | 五维评分、薄弱模块、示范改写、复练入口 | 雷达图高级动效 | API-04 |
| API-01 | 训练会话服务 | backend | 创建训练、保存训练状态、管理题目序列 | 多人班级训练 | DB-01 |
| API-02 | 问题生成与追问服务 | backend | 按模式抽题、生成追问、控制追问轮数 | 专业知识图谱 | AI-01 |
| API-03 | 回答评价服务 | backend | 五维评分、低分原因、薄弱标签 | 真实答辩结果预测 | AI-02 |
| API-04 | 报告与复练服务 | backend | 训练报告、复练题单、历史记录 | 导师端统计 | DB-02 |
| AI-01 | 问题与追问 Prompt | ai_model | 问题库结构化、追问规则、学术诚信边界 | 自动验证论文事实 | 问题库数据 |
| AI-02 | 评分与改写 Prompt | ai_model | 五维评分、示范改写、缺失事实占位 | 编造数据/文献 | 用户输入 |
| DB-01 | 训练数据模型 | data | thesis_profile、training_session、question、answer | 学校组织架构 | API 服务 |
| DB-02 | 复练与报告模型 | data | evaluation、weakness_tag、retry_plan | 班级聚合报表 | API-04 |
| SEC-01 | 隐私与学术诚信 | security | 删除数据、敏感提示、违规请求拦截 | 学校统一认证 | 合规文案 |
| ANA-01 | 埋点与指标 | analytics | 创建训练、提交回答、追问触发、报告完成、复练开始 | 商业化漏斗 | tracking plan |
| QA-01 | 测试与验收 | qa | 主路径、异常输入、Prompt 回归、隐私边界 | 压测 | 测试样例 |

## Data and API Scope

- entities: `ThesisProfile`, `TrainingSession`, `QuestionItem`, `AnswerEvaluation`, `TrainingReport`, `RetryPlan`
- api_groups: `/training`, `/questions`, `/answers/evaluate`, `/reports`, `/retry-plans`

## AI / Model Scope

- calls:
  - generate_question_set
  - generate_follow_up
  - evaluate_answer
  - rewrite_answer
  - generate_retry_plan
- prompt_assets:
  - defense_question_bank_prompt
  - follow_up_rule_prompt
  - five_dimension_scoring_prompt
  - academic_integrity_guardrail_prompt
- fallback_rules:
  - 模型失败时返回通用问题和手动评分提示。
  - 事实缺失时输出“待学生补充”，不能编造论文内容。

## Privacy Security Scope

- 用户可删除论文资料和训练记录。
- 不向导师或第三方展示个人训练内容，除非后续版本增加授权机制。
- 所有外部模型输出均标记为辅助建议，不作为论文事实。

## Analytics Scope

- training_create
- question_generate
- answer_submit
- follow_up_trigger
- evaluation_view
- rewrite_view
- report_complete
- retry_start
- integrity_block

## Testing Scope

- 正常路径：新建训练、生成题目、提交回答、触发评分、生成报告、进入复练。
- 异常路径：资料不足、空回答、极短回答、要求编造数据、模型调用失败。
- Prompt 回归：固定样例回答的评分维度和追问原因应稳定。

## PM Backflow Questions

- MVP 是否需要账号登录，还是允许游客本地试用？
- MVP 是否允许上传完整论文文件，还是只支持结构化文本输入？
- 是否需要把“语音输入”提前到 MVP？
