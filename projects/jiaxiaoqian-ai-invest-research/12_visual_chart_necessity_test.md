# PRD 辅助理解图表必要性测试报告

- 文档状态：Test Output，待用户检查
- 测试对象：[01_prd.md](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/01_prd.md)
- 图表包：[11_visual_prd_preview.md](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/11_visual_prd_preview.md)
- 测试目标：验证“先判断必要性，再决定辅助理解图表组合”的方法是否适合长期沉淀。
- 重要边界：本报告只是项目级测试产出，不是长期规则，不写入长期记忆。

---

## 1. 测试结论

这份 PRD 建议启用完整 10 图模式。

原因：

- 产品属于 AI + 金融投研场景，存在事实、来源、合规和高风险表达问题。
- 用户角色多，包括高频事件用户、概念研究用户、个股研究用户、合规管理员。
- 页面结构多，包括首页 / 高频跟踪、概念中心、个股详情、AI 助手、管理后台。
- 流程跨用户、系统、AI、数据源、合规审核、管理员。
- 状态复杂，涉及采集、清洗、AI 解读、审核、发布、过期、撤回。
- 有明确权限差异和后台审核动作。
- MVP 范围偏大，需要用图压清边界。
- 后续要进入 UI 设计和 Codex 开发文档，图表能减少理解成本。

---

## 2. 必要性判断表

| 图表 | 是否需要 | 触发条件 | 本 PRD 证据 | 放置位置 | 判断 |
|---|---|---|---|---|---|
| 产品总览思维导图 | 需要 | 产品模块多、读者需要快速理解全貌 | 目标用户、核心场景、核心模块、AI 能力、合规边界、成功指标都较多 | 摘要后 | 必须做 |
| 用户场景 / JTBD 思维导图 | 需要 | 用户角色差异明显，任务目标不同 | 高频事件、概念研究、个股研究、合规管理员的任务不同 | 目标用户 / JTBD 后 | 必须做 |
| 核心业务泳道图 | 需要 | 多角色、多系统、多审核点 | 用户、系统、AI、数据源、合规审核、管理员都有动作 | 用户主流程前 | 必须做 |
| 页面信息架构图 / 页面跳转图 | 需要 | 多页面、多入口、后续要做 UI | 首页、高频跟踪、概念中心、个股详情、AI 助手、管理后台互相跳转 | 核心页面跳转后 | 必须做 |
| 事件状态流转图 | 需要 | 有复杂对象状态和异常状态 | 事件从采集到发布、撤回、过期，AI 内容有审核和拦截 | 状态流转表后 | 必须做 |
| MVP 范围地图 / 分阶段路线图 | 需要 | PRD 范围大，需要压边界 | MVP、V1、暂不做需要清晰分层 | 范围定义后 | 必须做 |
| AI 模型路由决策树 | 需要 | 有 AI 任务类型、模型路由和人工复核 | 任务类型、实时性、长上下文、高风险、来源充分性影响模型选择 | AI 模型选型内 | 必须做 |
| 权限矩阵 | 需要 | 有登录、Pro、Admin、合规审核权限 | 查看、生成、编辑、审核、发布、撤回、配置动作权限不同 | 账号与权限内 | 必须做 |
| 风险控制闭环图 | 需要 | 金融投研和 AI 输出均有合规风险 | 风险来源、识别、AI 标记、人工审核、发布限制、日志、复盘需要闭环 | 合规与风险控制开头 | 必须做 |
| 用户故事地图 | 需要 | 多用户旅程和开发优先级需要对齐 | 用户故事需要和 MVP / V1 / Later 对齐 | 用户故事前 | 必须做 |

---

## 3. 本次测试输出清单

正式 PRD 已放入以下图表：

| 图表 | 正式 PRD 位置 |
|---|---|
| 产品总览思维导图 | [01_prd.md](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/01_prd.md:28) |
| 用户场景 / JTBD 思维导图 | [01_prd.md](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/01_prd.md:189) |
| MVP 范围地图 / 分阶段路线图 | [01_prd.md](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/01_prd.md:295) |
| 核心业务泳道图 | [01_prd.md](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/01_prd.md:342) |
| 事件状态流转图 | [01_prd.md](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/01_prd.md:441) |
| 页面信息架构图 / 页面跳转图 | [01_prd.md](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/01_prd.md:557) |
| AI 模型路由决策树 | [01_prd.md](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/01_prd.md:686) |
| 权限矩阵 | [01_prd.md](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/01_prd.md:803) |
| 用户故事地图 | [01_prd.md](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/01_prd.md:1026) |
| 风险控制闭环图 | [01_prd.md](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/01_prd.md:1112) |

图表包同步位置：

- [11_visual_prd_preview.md](/Users/liujun/Desktop/产品经理skill/projects/jiaxiaoqian-ai-invest-research/11_visual_prd_preview.md)

---

## 4. 如果不是复杂项目，应该怎么减少

这轮测试也验证了一个边界：长期规则不应要求所有 PRD 都强制 10 张图。

| 项目类型 | 建议图表 |
|---|---|
| 简单工具 / 单页面功能 | 产品总览、页面信息架构、MVP 范围 |
| 普通 SaaS / 多页面产品 | 产品总览、核心业务泳道、页面信息架构、MVP 范围、用户故事地图 |
| 多角色 / 审批流产品 | 增加权限矩阵、状态流转图 |
| AI 产品 | 增加 AI 模型路由决策树、风险控制闭环图 |
| 金融 / 医疗 / 教育等高风险产品 | 增加风险控制闭环图，并强化审核和日志 |
| 复杂 B 端后台 / 平台型产品 | 完整 10 图模式 |

---

## 5. 建议沉淀为长期机制的版本

如果用户检查通过，建议长期沉淀为：

1. PRD 生成前先做“辅助理解图表必要性判断”。
2. 不机械要求所有 PRD 都有 10 张图。
3. 默认至少判断以下触发条件：
   - 是否多角色
   - 是否多页面
   - 是否多流程 / 审批
   - 是否复杂状态
   - 是否 AI / 模型 / Skill 路由
   - 是否权限复杂
   - 是否高风险合规
   - 是否需要 UI 设计或 Codex 开发文档
4. 输出中说明本次选择了哪些图、为什么选择、哪些图不做。
5. 简单项目允许减少图表，复杂项目启用完整 10 图模式。

---

## 6. 用户检查点

请重点检查：

- 这 10 张图是否确实对这份 PRD 有必要。
- 有没有图是重复、过重、可以删掉的。
- 有没有图还缺关键业务信息。
- “必要性判断表”是否足够清晰。
- 是否认可把这个机制沉淀到长期规则，但仍保持“按必要性选择”，而不是所有 PRD 强制 10 张。

