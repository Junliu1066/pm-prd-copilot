# Conversation Memory Plan：毕业答辩辅导智能体

conversation_memory_id: `conversation-memory-20260425`

## memory_layers

| layer | 内容 | 生命周期 | 用途 | 用户控制 |
| --- | --- | --- | --- | --- |
| session_memory | 当前训练问题、回答、追问、临时评分 | 单次训练 | 保持上下文连贯 | 结束训练后可清除 |
| thesis_profile | 论文题目、摘要、目录、方法、核心结论 | 用户主动保存期间 | 个性化问题和追问 | 可编辑、可删除 |
| training_history | 历史训练报告、薄弱标签、复练记录 | 默认保留，用户可删除 | 趋势和复练 | 可按训练删除 |
| learner_profile | 能力维度、置信度、近期变化 | 从训练历史汇总 | 自适应教练 | 可重置 |
| preference_memory | 用户偏好，如训练强度、输出风格 | 用户批准后保存 | 个性化体验 | 可清除 |

## retention

- session_memory 默认只保留当前训练需要的最小上下文。
- thesis_profile 和 training_history 必须提供删除入口。
- learner_profile 应支持重置，不得跨账号或跨项目泄露。
- 长期记忆只保存结构化摘要，不保存不必要原文。

## clear_control

- 用户可以清除单次训练记录。
- 用户可以清除全部论文资料。
- 用户可以重置学习画像。
- 清除后 RAG 索引、缓存摘要和推荐计划必须失效。

## sensitive_data

- 论文题目、摘要、研究方法、数据描述、训练回答都视为敏感学习资料。
- 不把用户论文资料用于通用 Skill 更新。
- 不把用户训练内容共享给导师、机构或外部系统，除非未来版本明确授权。

## write_policy

- AI 只能提出 memory update suggestion。
- 服务层根据规则写入 session_memory、training_history 和 learner_profile。
- 用户偏好类记忆必须经过用户同意后保存。
