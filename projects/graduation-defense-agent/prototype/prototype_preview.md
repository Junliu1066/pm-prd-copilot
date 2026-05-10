# 毕业答辩辅导智能体低保真原型预览说明

状态：`draft`  
模式：`prototype_preview`  
来源：`projects/graduation-defense-agent/02_prd.generated.md` v0.5 产品包  
范围：MVP 核心训练路径。全量原型已扩展到 `full_prototype.md`，本文保留为一期 MVP 子集预览。

## 预览图

![毕业答辩辅导智能体原型预览](/Users/liujun/Desktop/产品经理skill/projects/graduation-defense-agent/prototype/prototype_preview.png)

如果图片没有显示，可直接打开：

- `/Users/liujun/Desktop/产品经理skill/projects/graduation-defense-agent/prototype/prototype_preview.png`
- `/Users/liujun/Desktop/产品经理skill/projects/graduation-defense-agent/prototype/prototype_preview.svg`

全量原型：

- `/Users/liujun/Desktop/产品经理skill/projects/graduation-defense-agent/prototype/full_prototype.md`
- `/Users/liujun/Desktop/产品经理skill/projects/graduation-defense-agent/prototype/full_prototype.png`

## 页面清单

| 页面 | 目标 | 主按钮 | 下一步 |
| --- | --- | --- | --- |
| P1 新建训练 | 收集论文资料、判断资料完整度、选择训练模式 | 开始生成问题 | 进入模拟答辩 |
| P2 模拟答辩 | 展示老师问题、学生作答、触发追问和五维评分 | 提交回答 | 进入单题复盘或下一轮追问 |
| P3 单题复盘 | 展示扣分原因、示范改写和待补充依据 | 下一题 | 继续答题或完成训练 |
| P4 训练报告 | 汇总五维表现、薄弱模块、复练计划和诚信提醒 | 开始复练 | 创建复练 session |

## 页面 1：新建训练

- 关键区域：论文题目、专业/论文类型、摘要/目录/方法/结论输入。
- 系统反馈：资料完整度分为低、中、高。
- 训练模式：基础核验、理解深挖、方法证据、压力反驳、全流程模拟。
- 异常状态：资料不足时提示“将使用通用问题库训练，无法做论文事实追问”。

## 页面 2：模拟答辩

- 关键区域：老师问题、考察点、回答输入框、追问原因、五维评分。
- 系统行为：根据回答质量判断是否追问，单题最多 2 轮。
- 风险提示：不鼓励编造数据，不替学生生成虚假研究过程。

## 页面 3：单题复盘

- 关键区域：原回答、扣分原因、示范改写、待补充依据。
- 输出规则：示范改写只重组表达，不新增用户未提供的论文事实。
- 下一步：用户可进入下一题，或回到论文资料补充证据。

## 页面 4：训练报告

- 关键区域：五维均分、薄弱模块、典型问题、复练题单。
- 输出：熟悉度、逻辑性、证据意识、反思能力、表达能力。
- 下一步：开始复练，或导出训练摘要。
