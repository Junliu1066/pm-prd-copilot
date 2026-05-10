# Prompt Architecture：毕业答辩辅导智能体

prompt_architecture_id: `prompt-architecture-20260425`

## prompt_assets

| prompt_id | 用途 | 输入 | 输出格式 | 关键约束 |
| --- | --- | --- | --- | --- |
| P-01 `question_generation` | 生成训练问题组 | 论文资料、训练模式、题库模块 | JSON question_set | 不编造论文事实；资料不足要提示 |
| P-02 `follow_up_generation` | 生成追问 | 主问题、学生回答、评分线索 | JSON follow_up | 最多 2 个追问；不能羞辱或过度压迫 |
| P-03 `five_dimension_scoring` | 五维评分 | 问题、回答、rubric | JSON score_card | 每个维度必须有证据句和扣分原因 |
| P-04 `answer_rewrite` | 示范改写 | 回答、缺失点、论文资料 | Markdown 示例 | 未提供事实用“待补充”占位 |
| P-05 `retry_plan_generation` | 生成复练计划 | 本轮评分、薄弱标签 | JSON retry_plan | 解释复练原因，给下一轮题目 |
| P-06 `integrity_guardrail` | 学术诚信拦截 | 用户输入、候选输出 | JSON moderation_result | 禁止代写、编造、规避检测 |

## versioning

- Prompt 版本格式：`{prompt_id}@v{major}.{minor}`。
- 任何 Prompt 变更必须记录：变更原因、影响任务、预期提升、风险、回归样例。
- 重大变更必须走人工确认，并运行 test_cases。
- Prompt 与模型绑定关系由 model_gateway 配置，不在业务代码里硬编码。

## test_cases

| case_id | 覆盖问题 | 预期行为 |
| --- | --- | --- |
| TC-01 | 论文资料缺失 | 问题生成提示补充资料，不编造 |
| TC-02 | 回答只有一句空话 | 评分低，触发依据追问 |
| TC-03 | 回答承认研究不足 | 评分应奖励反思能力，不简单扣满分 |
| TC-04 | 用户要求伪造数据 | integrity_guardrail 拦截并给安全替代 |
| TC-05 | 用户要求示范表达 | answer_rewrite 给结构，不新增事实 |

## safety_controls

- 所有 Prompt 都要包含“不得把示范内容当成用户论文事实”的约束。
- 对高风险请求先执行 integrity_guardrail，再进入生成链路。
- 对评分结果加入非承诺说明：这是训练反馈，不代表真实答辩结果。
- 对输出结构进行 JSON schema 校验，失败时重试一次，再走 fallback。

## tool_boundaries

- Prompt 不直接读写数据库，只接收服务层提供的净化输入。
- Prompt 不决定产品范围、版本路线或商业策略。
- Prompt 不直接更新用户能力画像，只输出 evidence，画像由确定性规则汇总。
