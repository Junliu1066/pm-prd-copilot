# AI 模型选型方案

- 文档状态：Draft
- 最后更新：2026-04-26
- 适用范围：价小前投研 MVP 与 V1 AI 能力
- 重要提醒：模型能力、价格、上下文长度、可用地区和合规要求变化很快，上线前必须按官方页面二次复核。

---

## 1. 结论先行

MVP 不建议“一个模型打天下”，建议采用模型路由：

| 任务 | 默认策略 | 备选策略 | 原因 |
|---|---|---|---|
| 新闻/公告清洗、分类、实体抽取 | 低成本快速模型 | 本地规则 + 小模型 | 高频、低复杂度、成本敏感 |
| 事件摘要、概念解释 | 中等能力模型 + RAG | 高能力模型复核高风险内容 | 需要中文表达、结构化输出、引用来源 |
| 个股深度分析、长文本研报/公告理解 | 高能力长上下文模型 | 分块检索 + 多轮汇总 | 复杂推理和跨来源综合 |
| 内容安全与合规拦截 | 规则引擎 + 分类模型 | 人工审核 | 买卖建议、收益承诺、传闻包装必须稳定拦截 |
| 向量检索 | 独立 embedding 模型 | 本地 embedding | 与生成模型解耦，便于替换 |
| 低风险批量任务 | Batch / 异步低价通道 | 夜间任务 | 成本优先，允许延迟 |

推荐架构：

```text
Model Router
├── fast_extract_model：实体抽取、分类、摘要草稿
├── reasoning_model：事件推理、个股深度分析、复杂问答
├── long_context_model：研报/公告/多文档长上下文
├── safety_model：内容安全分类
├── embedding_model：向量召回
└── fallback_model：主模型失败时降级
```

---

## 2. 选型原则

### 2.1 必须满足

- 支持中文金融语境。
- 支持结构化 JSON 输出。
- 支持函数调用或工具调用，便于接入数据查询。
- 支持长上下文或可与 RAG 稳定配合。
- 可记录模型名、Prompt 版本、输入来源、输出和审核状态。
- 可满足数据合规、隐私、备案/登记、跨境传输和供应商合同要求。

### 2.2 不能只看模型榜单

本产品的 AI 质量由四件事共同决定：

- 数据源是否真实、授权、及时。
- 检索是否召回正确来源。
- Prompt 是否强制区分事实、推断和风险。
- 安全规则是否拦截违规投资表达。

模型本身只是一环。即使使用最强模型，也不能让它无来源生成投研结论。

---

## 3. 官方资料观察

### 3.1 OpenAI

OpenAI 官方模型页建议复杂推理和编码从 `gpt-5.5` 开始，若优化成本和延迟，可选更小的 `gpt-5.4-mini` 或 `gpt-5.4-nano`；最新 OpenAI 模型支持文本和图像输入、文本输出、多语言和视觉能力，并通过 Responses API 与 SDK 使用。

可用于本项目：

- `gpt-5.5`：复杂个股深度分析、跨来源综合、Prompt/评测生成。
- `gpt-5.4-mini`：事件摘要、概念解释、后台管理辅助。
- `gpt-5.4-nano`：分类、标签、低风险结构化抽取。

官方价格页显示 `gpt-5.5` 标准短上下文价格为 input $5 / MTok、output $30 / MTok；`gpt-5.4-mini` 为 input $0.75 / MTok、output $4.50 / MTok；`gpt-5.4-nano` 为 input $0.20 / MTok、output $1.25 / MTok。

### 3.2 DeepSeek

DeepSeek 官方文档显示 API 兼容 OpenAI/Anthropic 格式，当前可用模型包括 `deepseek-v4-flash`、`deepseek-v4-pro`，并标注旧的 `deepseek-chat`、`deepseek-reasoner` 将来废弃。价格页显示 DeepSeek V4 系列支持 thinking / non-thinking、1M 上下文、JSON Output、Tool Calls。

可用于本项目：

- `deepseek-v4-flash`：中文高频抽取、分类、事件摘要草稿、低成本批量任务。
- `deepseek-v4-pro`：复杂推理、重点事件复核、个股深度分析备选。

注意：DeepSeek 价格页显示 `deepseek-v4-pro` 当前有截至 2026-05-05 15:59 UTC 的限时折扣，因此成本估算必须按上线时官方价格复核。

### 3.3 Google Gemini

Google Gemini 3 文档显示 Gemini 3.1 Pro 适合复杂任务和跨模态推理，Gemini 3 Flash 偏速度与价格，Gemini 3.1 Flash-Lite 偏高吞吐和成本效率。Gemini 3 系列当前为 preview，支持 1M 输入上下文、64k 输出，支持结构化输出、函数调用、搜索 grounding、URL context 等能力。

可用于本项目：

- `gemini-3.1-pro-preview`：PDF、研报、公告等长上下文理解备选。
- `gemini-3-flash-preview` 或 `gemini-3.1-flash-lite-preview`：低成本摘要和分类备选。

注意：Preview 模型适合评估，不建议作为唯一生产依赖。

### 3.4 Anthropic Claude

Anthropic 官方价格页显示 Claude Opus 4.7、4.6、4.5 等模型价格，并说明 Opus 4.7、Opus 4.6、Sonnet 4.6 等包含 1M token context window。Claude 适合作为长文档综合、严谨写作和安全表达的备选。

可用于本项目：

- Claude Opus / Sonnet 系列：长文档分析、复杂总结、投研表达质量对比。
- 不建议 MVP 首期强依赖单一 Claude 路线，除非数据合规、成本和调用稳定性已确认。

---

## 4. MVP 推荐组合

### 4.1 若优先控制成本

| 层级 | 推荐 |
|---|---|
| 快速抽取 | `deepseek-v4-flash` 或同等级国内低成本模型 |
| 深度分析 | `gpt-5.4-mini` / `deepseek-v4-pro` 二选一评测 |
| 高风险复核 | `gpt-5.5` 或人工审核 |
| 长文档备选 | `gemini-3.1-pro-preview` 仅用于评测 |
| 内容安全 | 规则引擎 + 分类模型 + 人工审核 |

适用：内测期、调用量大、预算敏感。

### 4.2 若优先保证质量

| 层级 | 推荐 |
|---|---|
| 快速抽取 | `gpt-5.4-nano` / `deepseek-v4-flash` |
| 事件摘要 | `gpt-5.4-mini` |
| 个股深度分析 | `gpt-5.5` |
| 长文档理解 | `gpt-5.5` / `gemini-3.1-pro-preview` 对比 |
| 内容安全 | 规则引擎 + 模型分类 + 人工审核 |

适用：首批付费用户、机构内测、需要高可信输出。

### 4.3 推荐落地方案

MVP 默认采用“成本优先 + 高风险升级”：

```text
普通任务：deepseek-v4-flash / gpt-5.4-nano
中等任务：gpt-5.4-mini
复杂任务：gpt-5.5
高风险内容：规则拦截 + gpt-5.5 复核 + 人工审核
长文档评测：gemini-3.1-pro-preview / Claude Sonnet 备选
```

这样可以把高频成本压下来，同时把重点分析和合规风险交给更强模型或人工。

---

## 5. 任务到模型映射

| 任务 | 输入 | 输出 | 推荐模型等级 | 是否异步 | 是否人工审核 |
|---|---|---|---|---|---|
| 文档去重 | 标题、正文 hash | 去重结果 | 规则 / 小模型 | 是 | 否 |
| 实体识别 | 新闻/公告文本 | 股票、概念、行业、机构 | 快速抽取模型 | 是 | 抽样 |
| 事件分类 | 文档 + 实体 | 事件类型、情绪、置信度 | 快速抽取模型 | 是 | 低置信度 |
| 事件摘要 | 多来源事件 | 摘要、背景、风险 | 中等模型 | 是 | 高影响事件 |
| 概念解释 | 概念、事件、股票 | 定义、驱动、上下游 | 中等模型 | 是 | 抽样 |
| 个股深度分析 | 财务、公告、新闻、研报摘要 | 结构化分析 | 高能力模型 | 是 | Pro/高风险 |
| 市场复盘 | 指数、涨停、事件、概念热度 | 主线、风险、待观察 | 中高模型 | 是 | 发布前抽样 |
| 用户问答 | 用户问题 + RAG | 有引用回答 | 中高模型 | 否 | 高风险拦截 |
| 内容安全 | AI 输出 | 通过/拦截/待审 | 规则 + 分类模型 | 否 | 命中规则 |

---

## 6. 评测方案

上线前必须用项目自己的数据做 A/B 评测，不能只看官方介绍。

### 6.1 评测集

- 100 条新闻事件。
- 50 条公告事件。
- 30 条研报摘要。
- 50 个概念解释。
- 30 个个股深度分析样例。
- 100 条违规/边界样例。

### 6.2 评分维度

| 维度 | 权重 | 说明 |
|---|---:|---|
| 事实准确性 | 30% | 是否被来源支持 |
| 引用完整性 | 20% | 关键结论是否有来源 |
| 金融表达质量 | 15% | 是否符合中文投研表达 |
| 合规安全 | 20% | 是否避免买卖建议和收益承诺 |
| 延迟 | 5% | 是否满足页面体验 |
| 成本 | 10% | 单次任务平均成本 |

### 6.3 通过门槛

- P0 违规内容拦截率 100%。
- 关键事实引用覆盖率 >= 98%。
- 事件摘要人工可用率 >= 85%。
- 个股深度分析人工可用率 >= 80%。
- AI 任务成功率 >= 95%。
- 平均成本低于预算上限。

---

## 7. 工程接入设计

### 7.1 模型路由配置

```yaml
model_router:
  fast_extract:
    primary: deepseek-v4-flash
    fallback: gpt-5.4-nano
  event_summary:
    primary: gpt-5.4-mini
    fallback: deepseek-v4-pro
  stock_deep_analysis:
    primary: gpt-5.5
    fallback: gpt-5.4-mini
  long_context_review:
    primary: gpt-5.5
    fallback: gemini-3.1-pro-preview
  safety_review:
    primary: rules
    fallback: gpt-5.4-mini
```

### 7.2 每次调用必须记录

- `provider`
- `model`
- `model_version`
- `prompt_version`
- `input_doc_ids`
- `output_insight_id`
- `latency_ms`
- `input_tokens`
- `output_tokens`
- `estimated_cost`
- `safety_status`
- `fallback_used`

---

## 8. 合规注意事项

- 金融数据和用户行为数据是否允许出境，需要法务确认。
- 面向中国境内公众提供生成式 AI 能力，需关注生成式 AI 服务备案/登记、公示和内容安全要求。
- 若使用境外模型处理未公开数据、用户数据、付费研报内容，必须先确认合同、授权和跨境数据边界。
- AI 输出不得替代持牌投资顾问，不得输出确定性买卖建议。

---

## 9. 官方来源

- OpenAI Models：[https://developers.openai.com/api/docs/models](https://developers.openai.com/api/docs/models)
- OpenAI Pricing：[https://developers.openai.com/api/docs/pricing](https://developers.openai.com/api/docs/pricing)
- DeepSeek API Quick Start：[https://api-docs.deepseek.com/](https://api-docs.deepseek.com/)
- DeepSeek Models & Pricing：[https://api-docs.deepseek.com/quick_start/pricing](https://api-docs.deepseek.com/quick_start/pricing)
- Google Gemini 3 Developer Guide：[https://ai.google.dev/gemini-api/docs/gemini-3](https://ai.google.dev/gemini-api/docs/gemini-3)
- Anthropic Claude Pricing：[https://platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing)

