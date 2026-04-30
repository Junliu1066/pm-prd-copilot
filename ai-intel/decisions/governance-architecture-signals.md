# Governance Architecture Signals

请自行核验原始链接、发布日期、模型名、API 功能开关、区域可用性、价格、合规要求和迁移成本后，再决定是否改动治理架构。

## Signal categories

| Category | What to watch | Possible architecture impact | Requires user decision |
|---|---|---|---|
| Model capability | coding, reasoning, long context, multimodal, realtime, tool use | Update model-selection criteria, task routing, fallback policy, eval cases | Yes |
| API or SDK change | structured output, tools, file search, browser/computer use, batch, streaming | Update implementation templates, harness checks, development task packages | Yes |
| Pricing or quota | token price, rate limits, batch discount, cache pricing | Update cost gates, efficiency audit thresholds, recommended model tier | Yes |
| Deprecation | model retirement, endpoint migration, SDK breaking change | Create migration checklist, compatibility tests, rollout plan | Yes |
| Safety or policy | data retention, privacy controls, restricted use, audit logs | Update approval points, source policy, redaction and supervision rules | Yes |
| Agent workflow | new planning, coding, browser, sandbox, or tool orchestration capability | Evaluate whether to add a skill, MCP/tool route, or harness gate | Yes |

## Latest observed changes

<!-- LATEST_UPDATES_START -->
- No updates yet.
<!-- LATEST_UPDATES_END -->

## Daily report use

Every daily report should translate AI updates into one of four outcomes:

- No architecture action.
- Watchlist only.
- Proposal needed.
- User approval needed before adoption.

## Adoption rule

AI intel can recommend architecture changes, but it cannot directly change stable workflow, registry, steward ownership, skill prompts, model provider, data source, retention policy, deletion policy, or publishing behavior without explicit user approval.
