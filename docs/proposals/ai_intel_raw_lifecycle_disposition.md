# AI Intel Raw 生命周期处置清单

- 日期：2026-05-02
- 状态：审查清单，不批准联网抓取、删除、归档、staging、commit、push、PR、decision docs 更新、模型变更或长期规则写入。
- 范围：`ai-intel/raw/2026-04-30/`，并说明它和 `daily / events / logs / decisions` 的边界。
- 主线任务：明确 AI 情报 raw 证据如何保留、复核、归档候选或 30 天后删除候选，防止 raw 网页快照污染稳定仓库。

## 结论

`ai-intel/raw/2026-04-30/` 是本地 raw 证据，不建议提交。

推荐处理：

1. raw 保持本地复核证据，暂不提交。
2. 已结构化的 `daily / events / logs` 才是默认可审计证据。
3. `decisions/*` 不由脚本自动更新，必须人工确认后再进入决策面。
4. raw 在本轮 AI 情报验收完成后，可列入 `archive_candidate` 或 `delete_after_30_days_candidate`，但不能现在删除。

## 当前 raw 文件

| Vendor | Source | 文件 | 类型 | 大小 | 推荐状态 |
|---|---|---|---|---:|---|
| OpenAI | model release notes | `ai-intel/raw/2026-04-30/openai/openai-model-release-notes.html` | HTML snapshot | 134K | `raw_local_evidence` |
| OpenAI | model release notes | `ai-intel/raw/2026-04-30/openai/openai-model-release-notes.json` | fetch metadata | 320B | `raw_local_evidence` |
| OpenAI | ChatGPT release notes | `ai-intel/raw/2026-04-30/openai/openai-chatgpt-release-notes.html` | HTML snapshot | 468K | `raw_local_evidence` |
| OpenAI | ChatGPT release notes | `ai-intel/raw/2026-04-30/openai/openai-chatgpt-release-notes.json` | fetch metadata | 324B | `raw_local_evidence` |
| Anthropic | model deprecations | `ai-intel/raw/2026-04-30/anthropic/anthropic-model-deprecations.html` | HTML snapshot | 608K | `raw_local_evidence` |
| Anthropic | model deprecations | `ai-intel/raw/2026-04-30/anthropic/anthropic-model-deprecations.json` | fetch metadata | 328B | `raw_local_evidence` |
| Anthropic | news | `ai-intel/raw/2026-04-30/anthropic/anthropic-news.html` | HTML snapshot | 352K | `raw_local_evidence` |
| Anthropic | news | `ai-intel/raw/2026-04-30/anthropic/anthropic-news.json` | fetch metadata | 278B | `raw_local_evidence` |
| Google | Gemini changelog | `ai-intel/raw/2026-04-30/google/gemini-api-changelog.html` | HTML snapshot | 135K | `raw_local_evidence` |
| Google | Gemini changelog | `ai-intel/raw/2026-04-30/google/gemini-api-changelog.json` | fetch metadata | 298B | `raw_local_evidence` |
| Google | Gemini deprecations | `ai-intel/raw/2026-04-30/google/gemini-api-deprecations.html` | HTML snapshot | 102K | `raw_local_evidence` |
| Google | Gemini deprecations | `ai-intel/raw/2026-04-30/google/gemini-api-deprecations.json` | fetch metadata | 304B | `raw_local_evidence` |

## 生命周期状态

| 区域 | 生命周期状态 | 默认动作 | 原因 |
|---|---|---|---|
| `ai-intel/raw/2026-04-30/*/*.html` | `raw_local_evidence` | 本地保留，暂不提交 | HTML 快照体积大、噪音高，只适合复核来源。 |
| `ai-intel/raw/2026-04-30/*/*.json` | `raw_local_evidence` | 本地保留，暂不提交 | 记录 fetch 元数据，但已由 `logs` 汇总。 |
| `ai-intel/events/2026-04-30.json` | `normalized_event` | 已作为结构化证据处理 | 可追踪事件摘要，但仍需人工核验原始来源。 |
| `ai-intel/daily/2026-04-30.md` | `reviewed_daily_signal_candidate` | 可作为人工汇报证据 | 只能提供信号，不能自动改变架构。 |
| `ai-intel/logs/2026-04-30.json` | `reviewed_run_log` | 可作为运行证据 | 记录抓取状态、HTTP 状态、来源和字节数。 |
| `ai-intel/decisions/*` | `decision_doc_candidate` | 不自动更新 | 任何架构影响都必须人工确认。 |

## 为什么 raw 不提交

| 原因 | 说明 |
|---|---|
| 体积和噪音高 | 6 个 HTML 快照约 1.8MB，网页细节变化会产生大量 diff。 |
| 容易误认为事实结论 | raw 是抓取快照，不代表已经核验、采纳或适合改变架构。 |
| 可由结构化证据替代 | `daily / events / logs` 足够解释本次 AI 情报运行事实。 |
| 不利于长期瘦身 | raw 默认提交会让每次 AI 情报运行都污染仓库。 |
| 合规和敏感边界更复杂 | 虽然当前来源是公开 AI 站点，但 raw HTML 仍不适合默认长期保存。 |

## 可选处理方案

| 选项 | 效果 | 优势 | 劣势 / 风险 | 我的建议 |
|---|---|---|---|---|
| A. 本地保留 raw，暂不提交 | 保留复核能力，不污染仓库 | 最稳，成本低，可回溯 | 工作区继续有未跟踪目录 | 当前选择 |
| B. 提交 raw | raw 完整进入仓库 | 复现能力强 | 噪音大，长期膨胀，容易被误用 | 不选 |
| C. 归档 raw | raw 进入 archive 候选 | 保留证据且离开 active 区 | 需要先确认 archive 策略 | 后续可评估 |
| D. 30 天后删除候选 | 验收后清理 raw | 仓库和工作区更轻 | 删除前必须确认不再需要复核原网页 | 后续推荐 |

## 推荐执行边界

当前阶段：

- 不提交 `ai-intel/raw/2026-04-30/`。
- 不删除 raw。
- 不移动 raw 到 archive。
- 不更新 `ai-intel/decisions/*`。
- 不因 AI 情报改变模型、供应商、成本、workflow、skill、harness、registry 或长期规则。

后续阶段：

1. 用户确认 `daily / events / logs` 足以作为本轮 AI 情报证据。
2. raw 保留 30 天作为本地复核证据。
3. 30 天后输出精确删除候选清单。
4. 用户批准后才删除 raw。

## 需要用户拍板

| 拍板项 | 我的建议 | 不同选择的效果 |
|---|---|---|
| raw 是否提交 | 不提交 | 不提交能保持仓库轻量；提交会产生大量网页快照噪音。 |
| raw 是否现在删除 | 不删除 | 不删除保留复核能力；现在删除会丢失本轮抓取证据。 |
| raw 是否进入 archive | 暂缓 | 等 archive 策略明确后再决定；现在归档会扩大 archive 范围。 |
| raw 是否 30 天后删除候选 | 是，后续单独批准 | 能长期瘦身，但不会立即删除。 |
| decision docs 是否更新 | 暂不更新 | 避免未经核验的信息进入架构决策面。 |
| AI 情报是否自动影响治理架构 | 不允许 | 保持 AI 情报为信号，不自动改规则。 |

## 本轮不做

- 不联网抓取。
- 不删除 raw。
- 不移动 raw。
- 不 staging / commit raw。
- 不提交 `ai-intel/decisions/*`。
- 不修改 AI 情报脚本。
- 不修改 skill、harness、workflow、registry、pipeline、automation。
- 不写长期记忆。
