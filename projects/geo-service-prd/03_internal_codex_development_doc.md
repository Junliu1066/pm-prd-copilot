# GEO 服务商业化内部 Codex 开发文档

- 文档目标：把 GEO 服务商业化 PRD 转化为可交给 Codex 执行的内部开发计划，并测试“Codex 多分支工程执行操作系统”是否能真实落地。
- 配套 PRD：[01_prd.md](/Users/liujun/Desktop/产品经理skill/projects/geo-service-prd/01_prd.md)
- 配套原型图层：[02_prototype_layer.md](/Users/liujun/Desktop/产品经理skill/projects/geo-service-prd/02_prototype_layer.md)
- 前置简报：[00_source_brief.md](/Users/liujun/Desktop/产品经理skill/projects/geo-service-prd/00_source_brief.md)
- 外部分发参考：[B.md](/Users/liujun/Desktop/产品经理skill/projects/geo-service-prd/B.md)
- 文档状态：Draft / internal test output
- 分发等级：内部执行版，禁止直接外发。
- 最后更新：2026-05-05

---

## 0. 使用模式与边界

### 0.1 模式判断

本项目不适合只输出普通轻量开发文档。原因是它同时涉及 Web 引流、线索提交、私域承接、客户信息采集、客户可溯源数据看板、报告交付、升级报价、内部交付工作台和 AI 辅助交付边界。

因此本内部版启用 `Codex 多分支工程执行操作系统`，但仍遵守最小化原则：

- 不新增长期 skill。
- 不新增长期 harness。
- 不修改 workflow / registry / stable policy。
- 不创建真实 git 分支。
- 不 push / PR。
- 所有分支成果默认是项目候选产物，不自动 stable。

### 0.2 本轮开发目标

把 PRD 的 MVP 转化为可开发的工程执行计划，目标效果是：

- Codex 能看清应该先做哪些模块、哪些可以并行、哪些必须等 contract 冻结。
- 每个分支都有明确允许修改范围、禁止修改范围、验证命令和人工拍板条件。
- 内部 AI 辅助只作为交付效率工具，不直接生成客户可见结论。
- 客户可见数据必须可追溯到问题样本、平台、原始答案、来源、更新时间和人工复核状态。

### 0.3 本轮不解决

- 不做完整 SaaS 平台。
- 不做代理商后台。
- 不做合同、支付、发票系统。
- 不做自动化大规模 AI 抓取。
- 不做自动内容发布或外链建设。
- 不承诺 AI 一定推荐、排名或带来线索。
- 不生成 HTML、PNG、高保真 UI。

---

## 1. 输入材料

### 1.1 已确认事实

| 编号 | 事实 |
|---|---|
| F1 | 业务目标是把 GEO 包装成可销售、可交付、可复购的服务产品。 |
| F2 | MVP 重点不是完整 SaaS，而是 Web 引流、私域承接、免费检测、体检报告、数据看板和升级转化。 |
| F3 | 客户核心关心 AI 是否推荐自己、是否推荐竞品、是否正确描述品牌。 |
| F4 | 客户看板必须可溯源，展示检测样本、原始答案、来源、指标、优化动作和更新时间。 |
| F5 | 内部 Agent 只用于问题库、标注、内容缺口、报告初稿和风险检查提效，客户交付必须人工复核。 |
| F6 | 外部分发版 `B.md` 已存在，本文件是内部执行版，不外发。 |

### 1.2 当前假设

| 假设 | 影响范围 | 验证方式 | 失效时处理 |
|---|---|---|---|
| MVP 使用轻量 Web 应用承载落地页、表单、客户看板和报告视图。 | 技术架构、前后端分支 | 开发前技术选型确认 | 若不用 Web 应用，重做分支矩阵。 |
| 客户看板使用项目 token 或签名链接访问，不做完整账号系统。 | 权限、数据模型 | P0 决策确认 | 若必须登录，权限分支升级为 P0。 |
| 报告先支持 Markdown / HTML 视图，PDF 后置。 | 报告导出 | 交付确认 | 若首期必须 PDF，新增导出分支。 |
| AI 平台样本先人工 / 半自动录入，不做自动抓取。 | AI 辅助、合规 | 风险复核 | 若要自动抓取，进入后续审批。 |
| 私域承接先用可配置企微 / 微信链接。 | 线索转化 | 业务确认 | 若接 CRM，需要新接口分支。 |

### 1.3 待决策问题

| 优先级 | 问题 | 影响 | 当前处理 |
|---|---|---|---|
| P0 | 看板访问方式：项目 token / 签名链接 / 登录？ | 权限模型和数据隔离 | 默认项目 token / 签名链接，生产前确认。 |
| P0 | 首批私域承接工具是微信还是企微？ | 表单字段和跟进状态 | 默认可配置外链和二维码。 |
| P1 | 报告首期是否必须 PDF？ | 导出链路 | 默认 HTML / Markdown，PDF 后置。 |
| P1 | 首期 AI 平台列表是否固定？ | 样本数据结构 | 默认配置化平台名称，不写死。 |
| P2 | 是否需要运营月报趋势图？ | V2 范围 | MVP 只预留数据结构。 |

### 1.4 必备产品输入覆盖

| 输入项 | 当前状态 |
|---|---|
| PRD | 已有 `01_prd.md`。 |
| 页面说明 | 已有 `02_prototype_layer.md` 第 2 / 4 节。 |
| 页面跳转关系 | 已有 `02_prototype_layer.md` 第 3 节。 |
| PRD 原型图层 | 已有低保真触点与页面草图。 |
| 核心流程 | PRD 和原型层均已覆盖 Web -> 私域 -> 报告 -> 看板 -> 复购。 |
| 用户故事与验收标准 | PRD 有验收方向，但开发级 API / 数据验收仍需补充。 |
| In Scope / Out of Scope | PRD 第 7 节已覆盖。 |
| AI 模型选型 | 项目涉及内部 AI 辅助，但不涉及客户可见模型承诺；模型选择需按内部辅助任务后续确认。 |

---

## 2. 开发范围

### 2.1 本轮 MVP 开发范围

| 模块 / 页面 / 能力 | 目标 | 主要变更 | 验收标准 |
|---|---|---|---|
| Web 引流与免费检测 | 获取线索并制造初步冲击 | 内容页、检测落地页、提交表单、简版结果页 | 线索可提交，字段校验可用，结果页不承诺效果。 |
| 私域承接 | 引导顾问沟通和付费体检 | 顾问入口、二维码 / 链接、跟进状态 | 每条线索可记录承接状态。 |
| 客户信息采集 | 支持付费体检输入 | 品牌、官网、行业、竞品、目标客户、资料链接 | 信息完整性可校验，缺关键字段不能进入正式检测。 |
| 内部检测工作台 | 存储问题、平台、竞品、原始答案和来源 | 项目、问题、样本、标注、来源、复核状态 | 至少支持 30 问题、3 平台、3 竞品的数据结构。 |
| 客户可溯源数据看板 | 向客户展示服务过程和证据 | 项目状态、指标卡、样本表、来源表、优化动作 | 每个指标可追溯到样本和更新时间。 |
| GEO 体检报告 | 输出低价成交交付物 | 报告视图、竞品对比、内容缺口、建议、报价入口 | 未复核高风险结论不能交付。 |
| 升级报价 | 推动深度诊断和代运营 | 方案档位、范围、周期、价格区间、边界 | 报价不扩大已确认服务范围。 |
| 内部 AI 辅助 | 提高问题库、标注、报告初稿效率 | AI draft 标识、人工复核、风险检查 | AI 输出默认 draft，复核后才能客户可见。 |

### 2.2 本轮不做

- 完整 SaaS 多租户后台。
- 代理商后台。
- 自动抓取 AI 平台答案。
- 自动发布客户内容。
- 自动外链 / 第三方信号建设。
- 合同、支付、发票。
- 客户可见 AI 自动结论。

### 2.3 影响面

| 类型 | 是否涉及 | 说明 |
|---|---|---|
| 前端页面 / 交互 | 是 | Web、表单、结果页、看板、报告、报价页、内部工作台。 |
| 后端接口 / 服务 | 是 | 线索、项目、样本、指标、报告、发布状态、访问 token。 |
| 数据库 / 数据模型 | 是 | 多实体和可追溯证据链。 |
| 权限 / 账号 | 是 | MVP 至少需要内部角色和客户 token / 签名链接边界。 |
| AI / Prompt / 模型 | 是 | 仅内部辅助，不直接客户可见。 |
| 第三方 API / MCP | 暂不涉及 | MVP 不接自动检测和 CRM。 |
| 发布 / 部署 | 是 | 至少需要 Web 应用部署、回滚和监控。 |

---

## 3. 工程任务包

| 任务 ID | 目标 | 输入材料 | 允许修改范围 | 禁止修改范围 | 预期输出 | 验证命令 | 人工确认点 |
|---|---|---|---|---|---|---|---|
| T1 | 冻结数据模型和 API contract | PRD / 原型层 | `src/server/**`, `src/shared/**`, `db/**`, `docs/api/**` | UI 样式、AI prompt、部署配置 | schema、API 草案、权限字段 | typecheck、schema test、API contract test | 看板访问方式、报告导出格式 |
| T2 | 构建 Web 获客与线索表单 | 原型 T01-T04 | `src/app/marketing/**`, `src/app/leads/**` | 内部工作台、AI、报告导出 | 落地页、表单、结果页、私域入口 | lint、component tests、form validation tests | 私域工具和字段 |
| T3 | 构建内部检测工作台 | 原型 T05-T06 | `src/app/internal/**`, `src/server/projects/**` | 公共落地页、AI 自动化 | 项目、问题、样本、来源、复核状态 | integration tests、permission tests | 内部角色范围 |
| T4 | 构建客户看板 | 原型 T06 | `src/app/dashboard/**`, `src/server/dashboard/**` | 原始未复核结论直接展示 | 指标、样本、来源、动作、更新时间 | dashboard tests、traceability tests | 客户访问方式 |
| T5 | 构建报告和升级报价 | 原型 T07-T08 | `src/app/reports/**`, `src/server/reports/**` | 支付、发票、自动承诺效果 | 报告视图、报价模块、风险边界 | report tests、risk copy tests | 报告导出格式 |
| T6 | 内部 AI 辅助草稿 | PRD AI 边界 | `src/server/ai-assist/**`, `prompts/**` | 客户可见自动发布、模型供应商变更 | draft 生成、复核状态、风险检查 | prompt regression、fallback tests | 模型选择和成本上限 |
| T7 | 验收、监控和发布 | 全部输入 | `tests/**`, `docs/release/**`, deployment config | 产品范围扩张 | 回归、监控、回滚说明 | full test suite、smoke test | 上线窗口和回滚责任人 |

### 3.1 最小修复策略

- 先冻结 contract，再并行页面和工作台。
- 不因内部 AI 辅助新增长期 skill / harness。
- 不把本项目的 GEO 业务规则写成通用 stable policy。
- 不把外部分发版 `B.md` 中的保护口径反向污染内部执行文档。

---

## 4. Codex 多分支工程执行操作系统

### 4.1 启用判断

| 判断项 | 结论 | 证据 |
|---|---|---|
| 是否需要多分支 | 是 | 涉及前端多触点、后端数据模型、内部工作台、客户看板、报告、AI 辅助和部署。 |
| 是否可降级为单分支 | 不建议 | 单分支会让 API、UI、AI、权限互相覆盖，integration 风险高。 |
| 是否存在 blocked 分支 | 是 | 看板访问方式、报告导出格式、私域承接工具是 P0 / P1 待决策。 |
| 是否需要完整内部模式 | 是，但只展开项目级机制 | 用户明确要求内部版 Codex 开发文档，并希望测试分支治理机制。 |

### 4.2 输入门禁

| 检查项 | 结论 | 缺失 / 风险 | 处理建议 |
|---|---|---|---|
| 需求是否完整 | 部分通过 | 商业和页面清楚，技术栈未指定 | 可继续做开发计划，技术栈作为实现前确认。 |
| 验收标准是否清楚 | 部分通过 | PRD 有产品验收，缺 API / DB 级验收 | T1 补 contract test。 |
| API contract 是否明确 | 不通过 | 尚无 API 字段定义 | T1 P0 先做。 |
| 数据库 / 数据字段是否明确 | 部分通过 | PRD 描述实体，但无 schema | T1 P0 先做。 |
| 页面状态是否明确 | 通过 | 原型层覆盖主要状态和异常 | UI 分支可基于原型推进。 |
| AI 输出格式是否明确 | 部分通过 | AI 辅助方向明确，输出 schema 未定 | T6 后置到 T1 contract 后。 |
| 依赖关系是否明确 | 通过 | Web -> 私域 -> 项目 -> 看板 -> 报告链路明确 | 可拆分分支。 |
| 风险点是否说明 | 通过 | 不承诺排名、不做黑帽、人工复核明确 | 写入风险门禁。 |

输入门禁结论：允许拆分支，但 P0 contract 分支必须先行；AI 辅助和报告导出不能早于核心数据模型冻结。

### 4.3 分支矩阵

| 分支名 | 任务节点 | 版本归属 | 优先级 | 影响面 | 依赖 | 可并行 | 冲突预测 | 风险等级 | 是否进入当前版本 |
|---|---|---|---|---|---|---|---|---|---|
| `codex/geo-contract-core` | 数据模型 / API / 权限 contract | v0.1 | P0 | DB、API、权限、指标口径 | 无 | 否 | 与所有分支共享字段，高风险 | 高 | 是 |
| `codex/geo-lead-funnel` | Web 引流、免费检测、私域承接 | v0.1 | P1 | 前端、线索 API | contract-core | 是 | 与 customer-dashboard 共享 lead/project 字段 | 中 | 是 |
| `codex/geo-internal-workspace` | 内部项目、问题、样本、来源、复核 | v0.1 | P1 | 内部页面、API、权限 | contract-core | 是 | 与 report 分支共享样本和复核状态 | 高 | 是 |
| `codex/geo-customer-dashboard` | 客户可溯源数据看板 | v0.1 | P1 | 前端、客户访问、指标展示 | contract-core、internal-workspace | 部分 | 权限和指标口径冲突 | 高 | 是 |
| `codex/geo-report-quote` | 体检报告和升级报价 | v0.1 | P1 | 报告视图、报价、风险边界 | contract-core、internal-workspace | 部分 | 与 dashboard 共享指标和来源 | 中 | 是 |
| `codex/geo-ai-assist` | 内部 AI draft 辅助 | v0.2 | P2 | Prompt、AI 服务、复核状态 | contract-core、internal-workspace | 是 | 若越权客户可见风险高 | 高 | 是，降级可选 |
| `codex/geo-release-quality` | 测试、监控、部署、回滚 | v0.1 | P1 | 测试、发布、监控 | 所有 v0.1 分支 | 否 | integration 后发现跨分支问题 | 中 | 是 |
| `codex/geo-monthly-ops` | 月度趋势看板 / 复盘 | v0.2 | P3 | 趋势、月报、代运营 | dashboard、report | 是 | 指标历史口径未冻结 | 中 | 暂缓 |
| `codex/geo-saas-platform` | 完整 SaaS、多租户、代理商后台 | later | P4 | 多租户、权限、计费 | MVP 成立后 | 否 | 范围膨胀 | 高 | 否 |

### 4.4 冲突预测与预算

| 分支 A | 分支 B | 冲突类型 | 风险 | 处理方式 |
|---|---|---|---|---|
| contract-core | 所有分支 | API / DB / 权限字段 | 高 | contract-core 先冻结，其他分支只基于 frozen contract 开发。 |
| internal-workspace | customer-dashboard | 样本、复核状态、来源字段 | 高 | internal-workspace 先定义 review_status 和 evidence model。 |
| customer-dashboard | report-quote | 指标口径和风险文案 | 中 | 共用 metrics service，不各自计算。 |
| lead-funnel | customer-dashboard | lead -> project 转换字段 | 中 | contract-core 定义 lead/project 映射。 |
| ai-assist | report-quote | AI draft 进入客户报告 | 高 | AI 输出必须 draft，report 只读取 reviewed 内容。 |

| 预算项 | 建议值 | 当前值 | 处理动作 |
|---|---:|---:|---|
| 建议分支数 | 5-7 | 7 个当前版本候选 | 可接受。 |
| 最大分支数 | 8 | 9 个总候选 | later 分支不执行。 |
| 最大并行数 | 3 | 3 | contract 后并行。 |
| 最大高风险分支数 | 2 | 3 | AI-assist 可降级到 v0.2，降低首期风险。 |
| 最大待人工拍板点 | 5 | 5 | 可接受。 |

### 4.5 分支治理卡

| 分支目标 | 允许修改范围 | 禁止修改范围 | 责任管家 | Action 合同 | Artifact 合同 | Harness / Gate | 审核门禁 | 效率检查 | 执行证据 | Bug 处理 | 失败回流 | Closeout | 用户拍板条件 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `geo-contract-core` 冻结数据/API/权限 | schema、API types、权限枚举、指标口径文档 | UI、AI prompt、部署 | development governance steward | define_contract | api_contract、schema_contract | regression、schema/API tests | P0 contract review | 不重复定义指标 | typecheck、contract tests | contract bug 优先修 | 回到 contract 分支 | contract change log | 访问方式、核心字段 |
| `geo-lead-funnel` 完成获客链路 | marketing / leads 页面和接口 | dashboard、report、AI | delivery planning steward | build_lead_funnel | lead_flow_artifact | form tests、copy risk check | 私域承接 review | 复用表单组件 | UI tests、validation tests | 回本分支修 | integration retry | lead closeout | 私域工具 |
| `geo-internal-workspace` 完成内部检测 | internal workspace、project/sample/evidence API | customer publish、AI 自动发布 | development governance steward | build_internal_workspace | workspace_artifact | permission tests | 内部角色 review | 复用 project model | integration tests | 回本分支修 | dashboard/report 依赖更新 | workspace closeout | 角色范围 |
| `geo-customer-dashboard` 完成客户看板 | dashboard UI、metrics、token access | 未复核结论、跨客户数据 | prototype/design steward + governance steward | build_dashboard | dashboard_artifact | source trace、permission gate | 客户可见 review | 复用 metrics service | traceability tests | 回本分支修 | report 联调 | dashboard closeout | 访问方式 |
| `geo-report-quote` 完成报告报价 | report view、quote section、risk copy | 支付、发票、效果承诺 | delivery planning steward | build_report_quote | report_artifact | external redaction、risk copy gate | 报告交付 review | 复用 dashboard metrics | report tests | 回本分支修 | dashboard/report 联调 | report closeout | PDF 是否首期 |
| `geo-ai-assist` 完成内部 AI 辅助 | ai-assist service、prompts、draft schema | 客户自动发布、模型供应商变更 | AI architecture steward 按需 | build_ai_draft | ai_draft_artifact | ai_solution 按需、prompt regression | AI 输出人工复核 | 不做全自动检测 | prompt tests、fallback tests | 回本分支修 | draft schema 更新 | AI closeout | 模型/成本/供应商 |
| `geo-release-quality` 完成验收发布 | tests、release docs、monitoring config | 业务范围扩张 | QA / governance steward | verify_release | release_evidence | harness check-only、regression | main 合入拍板 | 不重复建工具 | full test report | 定位责任分支 | integration fix loop | release closeout | 上线窗口、回滚责任 |

### 4.6 分支启动包

#### `codex/geo-contract-core`

| 字段 | 内容 |
|---|---|
| 分支名 | `codex/geo-contract-core` |
| 任务目标 | 定义 lead、customer project、question、sample、source evidence、metric、report、quote、review status 和 access token 的最小 contract。 |
| 上下文摘要 | MVP 依赖可追溯样本和客户看板，所有后续分支必须基于 frozen contract。 |
| 允许修改范围 | `src/shared/**`, `src/server/**`, `db/**`, `docs/api/**`, `tests/contract/**` |
| 禁止修改范围 | UI 高保真、AI prompt、部署、项目 PRD、stable governance |
| 依赖分支 | 无 |
| 相关文件 | `01_prd.md`, `02_prototype_layer.md` |
| 执行步骤 | 定义实体 -> 定义 API -> 定义权限 -> 定义 metric calculation -> 写 contract tests |
| 检查命令 | `npm run typecheck`, `npm test -- contract`, `npm run lint` |
| 验收标准 | contract 能支持 30 问题、3 平台、3 竞品、样本来源、复核状态和客户看板追溯。 |
| 失败处理方式 | 停止其他依赖分支，回 contract 分支修复。 |
| 输出证据要求 | schema diff、API contract、contract test output、人工确认点清单。 |

#### `codex/geo-lead-funnel`

| 字段 | 内容 |
|---|---|
| 分支名 | `codex/geo-lead-funnel` |
| 任务目标 | 实现 Web 引流页、免费检测表单、简版结果页和私域承接入口。 |
| 上下文摘要 | 这是获客入口，不能承诺效果，必须把线索转成后续项目输入。 |
| 允许修改范围 | `src/app/marketing/**`, `src/app/leads/**`, `src/server/leads/**`, `tests/leads/**` |
| 禁止修改范围 | dashboard、report、AI 自动化、stable governance |
| 依赖分支 | `codex/geo-contract-core` |
| 相关文件 | 原型 T01-T04 |
| 执行步骤 | 页面 -> 表单 -> 校验 -> duplicate state -> 私域 CTA -> 简版结果 |
| 检查命令 | `npm run lint`, `npm test -- leads`, `npm run test:e2e -- lead-funnel` |
| 验收标准 | 线索可提交、可校验、可进入私域承接；文案不承诺 AI 推荐。 |
| 失败处理方式 | 回本分支修复，不改 contract，除非提交 scope change request。 |
| 输出证据要求 | 表单测试、页面截图、风险文案检查、线索流转记录。 |

#### `codex/geo-customer-dashboard`

| 字段 | 内容 |
|---|---|
| 分支名 | `codex/geo-customer-dashboard` |
| 任务目标 | 实现客户可溯源数据看板。 |
| 上下文摘要 | 看板是客户信任和续费核心，所有指标必须可追溯。 |
| 允许修改范围 | `src/app/dashboard/**`, `src/server/dashboard/**`, `tests/dashboard/**` |
| 禁止修改范围 | 未复核 AI 结论客户可见、跨客户数据、自动抓取 |
| 依赖分支 | `codex/geo-contract-core`, `codex/geo-internal-workspace` |
| 相关文件 | 原型 T06，看板数据追溯规则 |
| 执行步骤 | token access -> metric cards -> sample table -> source table -> action tracking -> update time -> risk notes |
| 检查命令 | `npm test -- dashboard`, `npm run test:e2e -- dashboard`, `npm run lint` |
| 验收标准 | 指标可追溯到样本、来源、平台、时间和复核状态；未复核内容不展示。 |
| 失败处理方式 | 回 dashboard 分支；如果 contract 不足，提交 contract change request。 |
| 输出证据要求 | traceability test、permission test、截图、风险提示审查。 |

#### `codex/geo-ai-assist`

| 字段 | 内容 |
|---|---|
| 分支名 | `codex/geo-ai-assist` |
| 任务目标 | 实现内部 AI 辅助 draft，不进入客户自动交付。 |
| 上下文摘要 | AI 只提效，不负责最终客户结论。 |
| 允许修改范围 | `src/server/ai-assist/**`, `prompts/**`, `tests/ai-assist/**` |
| 禁止修改范围 | 自动发布、模型供应商变更、客户可见未复核内容、长期记忆 |
| 依赖分支 | `codex/geo-contract-core`, `codex/geo-internal-workspace` |
| 相关文件 | PRD AI 边界、风险控制章节 |
| 执行步骤 | draft schema -> prompt -> fallback -> review status -> risk flag -> tests |
| 检查命令 | `npm test -- ai-assist`, `npm run prompt:eval`, `npm run lint` |
| 验收标准 | AI 输出均为 draft，必须人工复核后才能被 dashboard/report 读取。 |
| 失败处理方式 | 降级为人工流程，AI 分支延后。 |
| 输出证据要求 | prompt eval、fallback test、人工复核门禁截图或日志。 |

### 4.7 Ready / Done 标准

Ready 标准：

- 分支目标明确。
- 允许 / 禁止修改范围明确。
- 依赖分支明确。
- 验收标准明确。
- 检查命令明确。
- 回滚方式明确。
- 人工拍板点明确。
- contract 分支已冻结或标注为 blocked。

Done 标准：

- 分支代码或文档完成。
- 自检完成。
- 测试完成。
- 必要 gate 完成。
- 管家审核完成。
- 执行证据完整。
- 回滚方式明确。
- closeout 已生成。
- 未解决风险已标注，且高风险未被自动接受。

### 4.8 Contract Freeze

| 契约 | 状态 | 依赖分支 | 变更处理 |
|---|---|---|---|
| API contract | draft | 所有功能分支 | T1 完成后 frozen；变更必须发 contract change request。 |
| 数据库 schema | draft | internal、dashboard、report、AI | T1 完成后 frozen；字段变更触发受影响分支复核。 |
| AI 输出格式 | draft | AI-assist、report | T6 前冻结；默认 draft only。 |
| 页面状态结构 | partial | lead、dashboard、report | 基于原型层先行，开发中补状态枚举。 |
| 权限规则 | draft | dashboard、internal、report | P0 访问方式确认后 frozen。 |
| 配置项 | draft | private-channel、platform names、report export | 默认配置化，不写死。 |

### 4.9 变更控制

| 变更请求 | 原因 | 选项 | 处理结论 |
|---|---|---|---|
| 增加登录账号系统 | token 不满足客户安全要求 | 扩展本分支 / 新建权限分支 / 延后 | 默认新建权限分支，并重新评估 scope。 |
| 增加 PDF 导出 | 客户首期交付要求 | 扩展 report 分支 / 延后 V1 | 默认延后，除非用户确认 P0。 |
| 接入自动 AI 检测 | 人工采样效率不足 | 新建 AI data adapter 分支 / 延后 | 默认延后并要求风险审批。 |
| 接 CRM / 企微 API | 私域跟进需要自动化 | 新建 integration 分支 / 后续版本 | 默认配置外链，不接 API。 |

### 4.10 决策日志

| 决策项 | 决策原因 | 影响范围 | 替代方案 | 最终选择 | 是否需要用户批准 |
|---|---|---|---|---|---|
| 启用多分支机制 | 项目多模块、多权限、多 AI 边界 | 全部开发计划 | 单分支开发 | 启用 | 已由本测试确认。 |
| 不新增长期 skill / harness | 当前是项目开发文档测试 | 治理架构 | 新增专用 checker | 不新增 | 是，保持现有规则。 |
| AI 只做内部 draft | 防止客户可见风险 | AI、报告、看板 | 客户自动生成报告 | draft + 人工复核 | 生产前需确认模型。 |
| MVP 不做完整 SaaS | 控制范围 | 权限、后台、代理商 | 完整平台 | MVP 轻量 Web + 内部工作台 | PRD 已确认。 |

### 4.11 分支状态机

```text
planned
-> ready
-> running
-> self_checked
-> reviewed
-> gate_passed
-> integration_pending
-> integration_passed / integration_failed
-> fix_required / closed / blocked
```

状态流转要求：

- `planned -> ready`：必须通过输入门禁和 Ready 标准。
- `ready -> running`：必须有分支启动包。
- `running -> self_checked`：必须完成分支内自检。
- `self_checked -> reviewed`：必须有测试证据。
- `reviewed -> gate_passed`：必须通过管家审核和必要 gate。
- `integration_failed -> fix_required`：必须生成失败定位报告并回到责任分支。

### 4.12 执行证据门禁

| 分支 | 自检证据 | 测试证据 | Gate 结果 | 管家审核 | 风险确认 | 回滚说明 |
|---|---|---|---|---|---|---|
| contract-core | schema diff、typecheck | contract tests | workflow / regression | development governance | P0 contract 风险 | revert contract commit |
| lead-funnel | form validation | UI / e2e | risk copy check | delivery planning | 文案承诺风险 | revert lead branch |
| internal-workspace | permission self-check | integration tests | source trace | governance | 内部权限风险 | revert workspace branch |
| customer-dashboard | traceability self-check | dashboard tests | source trace / permission | prototype + governance | 未复核内容外显 | revert dashboard branch |
| report-quote | report self-check | report tests | external redaction | delivery planning | 报告承诺风险 | revert report branch |
| ai-assist | prompt self-check | prompt eval / fallback | ai_solution 按需 | AI architecture 按需 | AI 输出越权 | disable AI feature flag |
| release-quality | release checklist | full regression | harness check-only | governance | 上线回滚风险 | rollback deployment |

没有证据的分支不能进入 integration / test。

### 4.13 Integration / Test 与失败回流

- 所有分支先进入 integration / test，不直接合 main。
- integration 顺序：contract-core -> lead-funnel + internal-workspace -> dashboard + report -> AI-assist -> release-quality。
- 失败时必须定位责任分支，生成失败定位报告。
- contract 变更会触发所有依赖分支复核。
- 高风险未解决问题不能自动接受。

### 4.14 权限边界

系统不能自动：

- 合 main。
- push / PR。
- 删除或迁移重要数据。
- 修改 stable 规则。
- 新增长期 skill。
- 新增长期 harness。
- 外部分发材料。
- 接受高风险未解决问题。
- 扩大版本范围。
- candidate 升 stable。
- 写长期记忆。
- 把 AI draft 直接展示给客户。
- 承诺 AI 推荐、排名或线索结果。

### 4.15 Closeout / 反哺候选

| 分支 | Bug / 问题 | 修复方式 | 是否架构问题 | 是否项目特例 | 反哺候选 | 用户拍板项 |
|---|---|---|---|---|---|---|
| contract-core | contract 字段缺失 | contract change request | 可能 | 否 | Codex 开发文档 contract freeze 模板 | 是否沉淀通用字段 |
| dashboard | 指标不可追溯 | 补 source trace | 可能 | 否 | PRD / 开发文档追溯证据规则 | 是否稳定化 |
| ai-assist | AI 输出越权 | 降级人工复核 | 可能 | 否 | AI draft / review gate 规则 | 是否进入 AI governance |
| report | 风险文案过度承诺 | redaction / risk review | 否 | 项目相关 | GEO 风险词库候选 | 是否项目内保留 |

---

## 5. 允许修改范围

本开发文档假设实际代码仓库存在类似结构，真实项目启动时必须按实际代码树调整。

| 路径 / 模块 | 允许动作 | 原因 |
|---|---|---|
| `src/app/marketing/**` | 新增 / 修改 | Web 引流内容页。 |
| `src/app/leads/**` | 新增 / 修改 | 免费检测和线索表单。 |
| `src/app/internal/**` | 新增 / 修改 | 内部检测工作台。 |
| `src/app/dashboard/**` | 新增 / 修改 | 客户数据看板。 |
| `src/app/reports/**` | 新增 / 修改 | GEO 体检报告和报价。 |
| `src/server/**` | 新增 / 修改 | API、业务服务、AI assist。 |
| `src/shared/**` | 新增 / 修改 | 共享类型和 contract。 |
| `db/**` | 新增 / 修改 | schema / migration。 |
| `tests/**` | 新增 / 修改 | 单元、集成、e2e 和 contract tests。 |
| `docs/api/**`, `docs/release/**` | 新增 / 修改 | API contract 和发布说明。 |

---

## 6. 禁止修改范围

| 范围 | 禁止原因 |
|---|---|
| PRD / 原型图层范围 | 开发不能擅自改产品范围。 |
| stable governance / skill / harness / workflow / registry | 本项目开发不批准稳定架构变更。 |
| 外部分发材料 | 内部版不能直接改外部包。 |
| 生产配置 / 真实客户数据 | 当前只是开发计划。 |
| 自动发布 / 自动抓取外部 AI 平台 | 涉及成本、合规和稳定性，必须另行批准。 |
| 长期记忆 / memory-cache | 项目经验不能自动长期化。 |

---

## 7. 人工确认点

| 优先级 | 确认点 | 默认建议 | 不确认的处理 |
|---|---|---|---|
| P0 | 客户看板访问方式 | 签名链接 / project token | dashboard 只能做 mock access。 |
| P0 | 私域承接工具 | 可配置微信 / 企微链接 | lead funnel 只留配置字段。 |
| P0 | 核心数据字段和权限 | contract-core 先冻结 | 阻塞正式并行。 |
| P1 | 报告导出格式 | HTML / Markdown 先行 | PDF 延后。 |
| P1 | AI 模型供应商和成本上限 | 暂不指定，先人工流程 fallback | AI 分支降级到 v0.2。 |
| P1 | 上线方式和环境 | 待真实代码仓库确认 | release-quality 只写 checklist。 |

---

## 8. 验证命令

真实代码仓库启动前，需要替换为项目实际命令。默认建议：

```bash
npm run lint
npm run typecheck
npm test
npm run test:e2e
npm run build
```

内部治理校验：

```bash
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

注意：内部治理校验用于本仓库机制验证；如果本文档外发，必须删除这些内部命令和治理细节。

---

## 9. 回滚方案

| 场景 | 回滚方式 |
|---|---|
| 单分支失败 | 回滚该分支 commit，不影响其他分支。 |
| contract 错误 | 停止依赖分支，修 contract 后重新生成影响面报告。 |
| dashboard 暴露未复核内容 | 立即关闭客户可见入口，回滚 dashboard 分支。 |
| AI 输出风险 | 关闭 AI feature flag，降级人工流程。 |
| 发布失败 | 执行部署回滚，保留失败日志和责任分支定位。 |

---

## 10. 审核结论

| 审核项 | 结论 |
|---|---|
| 是否适合内部版 Codex 开发文档 | 是。 |
| 是否适合外部分发 | 否，需使用 `B.md` 或外部保护版。 |
| 是否启用多分支机制 | 是。 |
| 是否新增 skill / harness | 否。 |
| 是否创建真实分支 | 否，本轮只是开发文档输出测试。 |
| 是否提交项目产物 | 暂不提交，先由用户审核。 |
| 是否可进入实现 | 部分可进入，P0 contract 和访问方式需先确认。 |

本次测试结论：该项目能有效触发多分支工程执行机制。模板能输出分支矩阵、分支治理卡、分支启动包、Ready / Done、Contract Freeze、变更控制、执行证据和权限边界；下一步需要用户审核这份真实输出是否符合预期，再决定是否把它作为内部 Codex 开发文档样例候选。
