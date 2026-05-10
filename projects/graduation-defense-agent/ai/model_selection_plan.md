# Model Selection Plan：毕业答辩辅导智能体

model_selection_id: `model-selection-20260425-market-screening`

## docs_verification_required

本版是“官方文档与价格页初筛”，不是 API 实测结论。最终上线前必须重新核验官方文档、价格、可用地区、上下文长度、数据保留政策、结构化输出能力、速率限制，并用本文件的 `benchmark_plan` 做真实 API 评测。

## market_scope

- default_market: 中国市场优先。
- included_provider_types: 国内可接入模型、OpenAI-compatible 模型、国际高质量模型。
- evaluation_goal: 找出适合“毕业答辩训练”的模型组合，而不是只选单一模型。
- product_tasks: 个性化问题生成、动态追问、五维评分、示范改写、学术诚信拦截、报告/复练计划、后续长文档或多模态输入。

## official_source_snapshot

collected_at: `2026-04-25`

| provider | 官方来源 | 本次使用的信息 | human_verification_required |
| --- | --- | --- | --- |
| OpenAI | [Models](https://platform.openai.com/docs/models)、[Pricing](https://openai.com/api/pricing/) | GPT 系列模型、价格、能力定位 | true |
| Anthropic | [Claude models overview](https://docs.anthropic.com/en/docs/about-claude/models/overview)、[API pricing](https://www.anthropic.com/api) | Claude 4.x 系列、价格、上下文与适用任务 | true |
| Google | [Gemini models](https://ai.google.dev/gemini-api/docs/models)、[Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) | Gemini 3.x / 2.5 系列、价格、上下文、多模态能力 | true |
| DeepSeek | [DeepSeek API pricing](https://api-docs.deepseek.com/quick_start/pricing) | DeepSeek-V4-Pro / Flash、上下文、价格页 | true |
| Alibaba Cloud 百炼 / Qwen | [模型列表](https://help.aliyun.com/zh/model-studio/getting-started/models) | Qwen3.6 Max/Plus/Flash、上下文、价格 | true |
| Moonshot / Kimi | [Kimi API pricing](https://platform.moonshot.cn/docs/pricing/chat) | Kimi K 系列长上下文模型与价格页 | true |

## candidate_model_pool

| provider | candidate_model | role_fit | 文档初筛优势 | 主要风险 | pricing_or_cost_note |
| --- | --- | --- | --- | --- | --- |
| Qwen / 阿里云百炼 | `qwen3.6-plus` | MVP 主模型候选：问题生成、追问、评分、改写 | 中文能力、本地云接入、1M 上下文、成本相对可控 | 评分稳定性需实测 | 官方页显示输入约 ¥2/1M tokens，输出约 ¥12/1M tokens，需上线前复核 |
| Qwen / 阿里云百炼 | `qwen3.6-flash` | 低成本 fallback：诚信初筛、资料完整性判断、简单改写 | 成本低、延迟友好、适合批量轻任务 | 复杂追问和评分质量可能不足 | 官方页显示输入约 ¥0.05/1M tokens，输出约 ¥0.5/1M tokens，需复核 |
| DeepSeek | `deepseek-v4-flash` | 低成本推理候选：追问、评分辅助、报告草稿 | OpenAI-compatible 接入、长上下文、成本优势 | 模型版本和价格变化快，需锁定模型 id | 以官方 pricing 页为准，需复核 |
| DeepSeek | `deepseek-v4-pro` | 质量候选：复杂追问、评分解释、复练计划 | 更适合复杂推理任务 | 成本和延迟高于 flash，真实评分一致性待测 | 以官方 pricing 页为准，需复核 |
| Moonshot / Kimi | `kimi-k2.6` 或当前 Kimi 主力模型 | 长上下文候选：完整论文/PPT 输入、长报告总结 | 中文长文本场景友好，适合后续上传完整论文 | 当前 MVP 不一定需要完整长上下文；价格需复核 | 以 Kimi 官方 pricing 页为准 |
| OpenAI | `gpt-5.4` / 当前稳定 GPT 主力模型 | 国际质量候选：评分、追问、结构化输出 | 推理、结构化输出、工具生态成熟 | 中国市场接入、成本、合规和网络稳定性需评估 | 以 OpenAI 官方 pricing 页为准 |
| OpenAI | `gpt-5.4-mini` / 当前轻量 GPT 模型 | 国际低成本候选：轻量评分、改写、分类 | 成本低于主力 GPT，适合轻任务 | 中文教育场景需实测 | 以 OpenAI 官方 pricing 页为准 |
| Anthropic | `claude-sonnet-4.6` 或当前 Sonnet 主力模型 | 质量候选：长答案反馈、教练式解释 | 长文本理解和反馈质量可能适合辅导场景 | 国内接入、成本、中文评分一致性需实测 | 以 Anthropic 官方 pricing 页为准 |
| Google | `gemini-3.1-pro` / 当前 Pro 模型 | 多模态/长上下文未来候选：PPT、图片、视频扩展 | 多模态和长上下文能力适合 Future 阶段 | MVP 文字训练未必需要，国内接入需评估 | 以 Gemini 官方 pricing 页为准 |
| Google | `gemini-3.0-flash` / 当前 Flash 模型 | 低延迟候选：简单改写、摘要、轻量问答 | 速度和成本可能适合轻任务 | 中文答辩评分需实测 | 以 Gemini 官方 pricing 页为准 |

## model_comparison_matrix

> measured_score 当前均为 `not_measured`，因为本轮未调用各家 API。以下是文档初筛，不是最终质量排名。

| task | 候选模型 | doc_screening_score | measured_score | reason | benchmark_required |
| --- | --- | --- | --- | --- | --- |
| 个性化问题生成 | `qwen3.6-plus` | A | not_measured | 中文场景、成本、上下文和国内可接入性平衡 | true |
| 个性化问题生成 | `deepseek-v4-flash` | B+ | not_measured | 成本优势明显，适合生成题组草稿 | true |
| 个性化问题生成 | `gpt-5.4` | A | not_measured | 国际质量候选，但成本和接入需评估 | true |
| 动态追问 | `qwen3.6-plus` | A- | not_measured | 中文教育追问和成本平衡 | true |
| 动态追问 | `deepseek-v4-pro` | A- | not_measured | 复杂追问推理候选 | true |
| 动态追问 | `claude-sonnet-4.6` | A- | not_measured | 教练式反馈候选 | true |
| 五维评分 | `qwen3.6-plus` | A- | not_measured | 可作为中国市场 MVP 主评分模型候选 | true |
| 五维评分 | `deepseek-v4-pro` | A- | not_measured | 推理评分候选，需测稳定性 | true |
| 五维评分 | `gpt-5.4` | A | not_measured | 质量候选，适合对照评测 | true |
| 示范改写 | `qwen3.6-plus` | A | not_measured | 中文表达与成本平衡 | true |
| 示范改写 | `qwen3.6-flash` | B+ | not_measured | 可做低成本改写 fallback | true |
| 学术诚信拦截 | `qwen3.6-flash` + 规则 | A- | not_measured | 轻模型 + 规则更经济 | true |
| 学术诚信拦截 | `deepseek-v4-flash` + 规则 | A- | not_measured | 低成本分类候选 | true |
| 长文档/PPT 扩展 | `kimi-k2.6` | A- | not_measured | 长上下文候选，适合后续完整论文输入 | true |
| 多模态扩展 | `gemini-3.1-pro` | A- | not_measured | Future 阶段图片/PPT/视频候选 | true |

## benchmark_plan

| benchmark_id | 任务 | 样例数量 | pass_criteria | measured | human_review_required |
| --- | --- | ---: | --- | --- | --- |
| BM-01 | 根据论文摘要生成问题组 | 30 | 问题相关率 >= 85%，虚构事实为 0 | false | true |
| BM-02 | 对空泛回答触发追问 | 30 | 应追问命中率 >= 80%，不应追问误触发 <= 20% | false | true |
| BM-03 | 五维评分一致性 | 50 | 同类回答分差可解释，评分理由与 rubric 匹配 | false | true |
| BM-04 | 示范改写安全性 | 30 | 不新增用户未提供事实，缺失事实用“待补充” | false | true |
| BM-05 | 学术诚信拦截 | 40 | 高风险请求拦截率 >= 95%，安全替代建议清晰 | false | true |
| BM-06 | latency/cost 压测 | 100 | 单题反馈延迟和单轮成本在 MVP 预算内 | false | true |

## benchmark_status

- status: `not_run`
- reason: 当前没有使用各家 API key 做真实调用；本文件只完成官方文档与价格页初筛。
- next_step: 准备 180 条测试样例，对 `qwen3.6-plus`、`qwen3.6-flash`、`deepseek-v4-flash`、`deepseek-v4-pro`、`gpt-5.4`、`claude-sonnet-4.6` 做同题评测。

## shortlist_recommendations

### Recommendation A：首发中国市场 MVP 组合

- primary: `qwen3.6-plus`
- low_cost_fallback: `qwen3.6-flash`
- secondary_candidate: `deepseek-v4-flash`
- use_for:
  - `qwen3.6-plus`：问题生成、动态追问、五维评分、示范改写、报告总结。
  - `qwen3.6-flash`：学术诚信初筛、资料完整性判断、低风险改写 fallback。
  - `deepseek-v4-flash`：成本对照和低成本 fallback。
- why: 更贴近中国市场接入、中文教育场景和成本控制；适合 MVP 先跑通训练闭环。
- conditions: 必须完成 BM-01 到 BM-06；如果评分一致性不达标，切换到质量优先组合或只保留人工/规则评分 fallback。

### Recommendation B：质量优先对照组合

- primary_candidates:
  - `gpt-5.4`
  - `claude-sonnet-4.6`
  - `deepseek-v4-pro`
- use_for:
  - 五维评分对照评测。
  - 动态追问质量评测。
  - 示范改写安全性对照。
- why: 用高质量候选模型做 benchmark 对照，可以判断国内主模型的质量差距。
- conditions: 只有在 API 接入、成本、合规和网络稳定性可接受时进入生产候选。

### Recommendation C：后续长上下文/多模态扩展组合

- long_context_candidate: `kimi-k2.6` 或当前 Kimi 主力模型。
- multimodal_candidate: `gemini-3.1-pro` 或当前 Gemini Pro 模型。
- use_for:
  - 上传完整论文、PPT 页绑定问题。
  - 后续图片/PPT/视频输入。
- why: 这类能力不应该卡住 MVP，但应提前留接口。
- conditions: V1/Future 阶段重新评估价格、上下文、文件处理和隐私策略。

## routing_rules

- MVP 默认先采用 Recommendation A，并保留 Recommendation B 的同题 benchmark 对照。
- 高风险学术诚信请求先走规则，再走低成本分类模型，不直接进入生成模型。
- 评分任务必须记录模型 id、Prompt 版本、rubric 版本、输入摘要和输出摘要。
- 模型输出失败、超时或结构化校验失败时，降级到规则题库、固定 rubric 和手动评分模板。
- 任一模型更新必须重新跑 BM-01 到 BM-06，且需要人工确认。

## fallback_strategy

| trigger | fallback |
| --- | --- |
| 主模型超时 | 切换到低成本/低延迟模型，提示“反馈可能较简化” |
| 模型输出格式错误 | 重试一次，仍失败则返回固定 rubric 模板 |
| 评分一致性不达标 | 暂停自动评分，只展示建议和人工评分入口 |
| 生成内容疑似编造论文事实 | 输出“待学生补充”，不继续生成事实 |
| 成本超预算 | 降低题量、限制追问轮次、切换 flash/fallback 模型 |

## open_decisions

- 是否优先选择阿里云百炼作为国内主 provider？
- 是否需要接入 DeepSeek 作为成本对照？
- 是否允许国际 API 进入生产，还是只作为离线 benchmark 对照？
- BM-01 到 BM-06 的样例由谁标注为金标准？

## human_verification_note

AI 情报、官方文档和价格页都只能作为决策信号。正式选型前需要你自己核验真实性、可用性、价格、合规、延迟和实际输出质量。
