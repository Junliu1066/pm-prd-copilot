# PRD 页面级原型图必要性测试报告

- 文档状态：Test Output，待用户检查
- 测试对象：[01_prd.md](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/01_prd.md)
- 可打开 HTML 原型：[prototype/index.html](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/prototype/index.html)
- 页面级 PNG 目录：[prototype/screenshots/](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/prototype/screenshots)
- 重要边界：本报告只是项目级测试产出，不是长期规则，不写入长期记忆。

---

## 1. 测试结论

这份 PRD 需要页面级 PNG 原型图。

原因：

- PRD 后续要进入 UI 设计阶段，单纯 Mermaid / ASCII 线框不足以表达页面长什么样。
- 产品包含多个核心页面：首页 / 高频跟踪、事件详情、概念中心、行情复盘、个股详情、AI 助手、管理后台。
- 页面之间存在跳转关系，研发需要看到信息布局、主次区域和入口位置。
- 金融投研产品需要在页面上明确展示来源、置信度、更新时间和风险提示。
- 后续要转 Codex 开发文档，页面级 PNG 能降低页面拆解和验收误差。

---

## 2. 页面清单判断

| 页面 | 是否需要 PNG | 触发原因 | 覆盖 PRD 模块 |
|---|---|---|---|
| 高频跟踪 / 首页工作台 | 需要 | MVP 主入口，承载事件发现和指标概览 | 高频跟踪、事件中心、财经日历、事件排行 |
| 事件详情 | 需要 | 主路径详情页，连接事件、概念、股票、AI 风险提示 | 事件详情、相关股票、相关概念、AI 摘要 |
| 概念中心 | 需要 | 核心研究入口，关系到搜索、筛选、概念卡片 | 概念列表、概念详情、历史时间轴 |
| 行情复盘 | 需要 | 图表密集页面，需要提前验证信息布局 | 市场全景、板块热力、概念异动 |
| 个股详情 | 需要 | 信息密度最高，需要验证六类标签和研究卡片 | 个股头部、股票行情、财务、公司档案、AI 深度分析 |
| AI 投研助手 | 需要 | AI 能力独立承载页，需要展示输入、模型路由、生成结果和反馈 | AI 生成、模型路由、用户反馈 |
| Admin 审核后台 | 需要 | 高风险后台页面，需要明确审核动作和权限 | 内容审核、规则命中、人工处理、日志 |

---

## 3. 本次页面级 PNG 输出

| 页面 | PNG |
|---|---|
| 高频跟踪 / 首页工作台 | [01_home_tracking.png](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/prototype/screenshots/01_home_tracking.png) |
| 事件详情 | [02_event_detail.png](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/prototype/screenshots/02_event_detail.png) |
| 概念中心 | [03_concept_center.png](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/prototype/screenshots/03_concept_center.png) |
| 行情复盘 | [04_market_review.png](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/prototype/screenshots/04_market_review.png) |
| 个股详情 | [05_stock_detail.png](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/prototype/screenshots/05_stock_detail.png) |
| AI 投研助手 | [06_ai_assistant.png](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/prototype/screenshots/06_ai_assistant.png) |
| Admin 审核后台 | [07_admin_review.png](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/prototype/screenshots/07_admin_review.png) |

---

## 4. 产出方式

- 在现有 HTML 原型中补齐缺失的独立页面：事件详情、AI 投研助手。
- 使用 Playwright 打开 HTML 原型并按页面锚点截图。
- 所有截图使用英文文件名。
- 截图放在项目目录下，便于 Codex、UI 设计和研发直接打开。
- 正式 PRD 和原型展开文档都已引用这些 PNG。

---

## 5. 是否建议长期沉淀

如果用户检查通过，建议长期沉淀为“页面级原型图必要性判断机制”，而不是所有 PRD 都强制生成 PNG。

建议规则：

1. 软件 / 产品 PRD 先从 MVP 模块反推页面清单。
2. 如果后续要进入 UI 设计、Codex 开发文档、外部研发交付，默认需要页面级 PNG 或 HTML 原型截图。
3. 页面级原型图必须是完整页面，不是局部组件截图，也不是 Mermaid 流程图。
4. 文件名使用英文，放在项目可打开目录。
5. PRD 正文必须引用原型图，原型展开文档必须提供清单。
6. 简单单页工具可以只生成 1-3 张关键页面；复杂平台型产品应覆盖主入口、核心详情、管理/审核、关键 AI 或风险页面。

---

## 6. 用户检查点

请重点检查：

- 页面清单是否覆盖了 MVP 核心模块。
- 是否还需要补充“通知中心 / 关注列表 / Pro 权限页”这类页面。
- PNG 是否达到了“完整页面级原型图”的要求。
- 这些图是否足够进入 UI 设计阶段。
- 是否认可后续把“页面级原型图必要性判断机制”加入长期规则。

