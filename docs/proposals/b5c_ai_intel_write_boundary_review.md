# B5c AI 情报写入边界审查

- 日期：2026-04-30
- 状态：决策记录，只记录边界审查；不批准 staging、commit、push、PR、联网自动化、模型/供应商变更、稳定规则变更、归档、删除或长期记忆写入。
- 范围：`ai-intel/*`
- 原则：AI 情报只能提供信号，不能自动改变治理架构。

## 结论

AI 情报区有价值，但必须保持候选区和人工监督。它适合收集 OpenAI、Anthropic、Google 等 AI 相关变化，辅助判断是否需要优化治理架构；但它不适合作为无人值守的稳定治理更新器。

当前建议：

1. 保留 AI 情报作为 candidate 能力。
2. 不把它并入主 harness 或主 workflow。
3. 不让它自动修改 decision docs、长期规则、registry、skill、harness 或模型选择。
4. 只提交经人工复核后的 `daily / events / logs` 证据；raw 默认不提交。
5. 后续如要定时运行，必须先做 dry-run 或 output-dir，避免直接写稳定仓库。

## 当前组件边界

| 路径 | 作用 | 是否写文件 | 当前状态 |
|---|---|---:|---|
| `ai-intel/README.md` | AI 情报目录说明和规则 | 否 | 候选说明 |
| `ai-intel/sources/registry.yaml` | 人工维护的信息源列表 | 否 | 候选源清单 |
| `ai-intel/scripts/fetch_sources.py` | 抓取网页原始内容 | 是，写 `raw/` 和 `logs/` | 需要人工监督 |
| `ai-intel/scripts/normalize_events.py` | 把 raw 归一化为事件 JSON | 是，写 `events/` | 需要复核 |
| `ai-intel/scripts/summarize_daily.py` | 生成每日摘要 | 是，写 `daily/` | 可作为人工报告 |
| `ai-intel/scripts/update_decision_matrix.py` | 更新决策面板 | 是，写 `decisions/` | 高风险，不能自动采用 |
| `ai-intel/raw/` | 原始网页证据 | 是 | 默认不提交 |
| `ai-intel/events/`、`daily/`、`logs/` | 结构化证据和报告 | 是 | 人工复核后可提交 |

## 主要风险

| 风险 | 影响 | 建议 |
|---|---|---|
| 联网抓取会产生噪音 | 网页变动、失败抓取、大量 raw diff 会污染仓库 | raw 只作本地证据，不默认提交 |
| daily 看起来像结论 | 用户可能误以为情报已经被采纳 | daily 必须保留“信号，不是决策”的口径 |
| decision docs 被脚本直接改 | 容易把候选信号误写成架构规则 | decision docs 更新必须人工复核 |
| 缺少 dry-run / output-dir | 定时任务会直接写 repo | 稳定自动化前必须补输出隔离方案 |
| `__pycache__` 等运行产物 | 增加无意义 diff | 禁止 staging |

## 用户已确认的处理方向

- 可以启动联网抓取，但必须在人工监督下。
- AI 情报汇报需要带解决方案建议。
- 生成物中只提交经复核的 `daily / events / logs`。
- `raw/` 不提交，后续再判断归档或 30 天后删除候选。
- decision docs 暂不提交，避免未经核验的信息进入决策面。

## 不允许混入的内容

```text
ai-intel/raw/*
ai-intel/scripts/__pycache__/*
ai-intel/decisions/*
projects/*
memory-cache/*
docs/archive/*
root 删除项
```

## 后续建议

AI 情报如果继续推进，建议按以下顺序：

1. 保持候选区，不转 stable。
2. 先用人工复核 daily / events / logs。
3. 补 dry-run / output-dir 后，再讨论定时任务。
4. decision docs 只允许人工确认后更新。
5. 任何 AI 情报带来的架构优化，都先进 proposal / architecture inbox，再由用户拍板。
