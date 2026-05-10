# 毕业答辩辅导智能体全量原型图

prototype_mode: `full`  
visual_variant: `dark_premium`  
approval_status: `approved_as_default`  
来源：`projects/graduation-defense-agent/02_prd.generated.md` v0.5 产品包  
范围：覆盖 MVP、二期个人效率增强、三期导师/机构协作、最终平台化候选能力。MVP 仍是一期开工范围，其余页面是后续阶段原型，不代表当前开发承诺。当前默认视觉风格为 Dark Premium。

## 预览图

![毕业答辩辅导智能体 Dark Premium 全量原型图](/Users/liujun/Desktop/产品经理skill/projects/graduation-defense-agent/prototype/full_prototype.png)

如果图片没有显示，可直接打开：

- `/Users/liujun/Desktop/产品经理skill/projects/graduation-defense-agent/prototype/full_prototype.png`
- `/Users/liujun/Desktop/产品经理skill/projects/graduation-defense-agent/prototype/full_prototype.svg`

浅色结构版已保留为备份：

- `/Users/liujun/Desktop/产品经理skill/projects/graduation-defense-agent/prototype/full_prototype_light.png`
- `/Users/liujun/Desktop/产品经理skill/projects/graduation-defense-agent/prototype/full_prototype_light.svg`

## 页面清单

| 阶段 | 页面 | 页面目标 | 主按钮 | 下一步 |
| --- | --- | --- | --- | --- |
| 一期 MVP | P1 新建训练 | 建立论文资料和训练上下文 | 开始生成问题 | P2 模拟答辩 |
| 一期 MVP | P2 模拟答辩 | 展示老师问题、作答、追问和评分 | 提交回答 | P3 单题复盘 |
| 一期 MVP | P3 单题复盘 | 查看扣分原因、示范改写、待补充依据 | 下一题 | P2 或 P4 |
| 一期 MVP | P4 训练报告 | 汇总五维表现、薄弱模块和复练建议 | 开始复练 | P5 复练训练 |
| 一期 MVP | P5 复练训练 | 围绕低分模块重新训练 | 提交复练 | P4 更新报告 |
| 一期 MVP | P6 资料管理 / 删除 | 管理论文资料和隐私删除 | 删除资料 / 补充资料 | P1 或结束 |
| 二期 | P7 PPT / 章节输入 | 按 PPT 页或论文章节生成问题 | 生成页级问题 | P2 |
| 二期 | P8 历史趋势 | 查看多轮训练五维变化 | 进入专项复练 | P9 |
| 二期 | P9 专项复练 | 指定薄弱模块生成集中题单 | 开始专项复练 | P2 / P5 |
| 二期 | P10 导出复习清单 | 导出低风险训练摘要 | 导出 | 文件下载 / 分享 |
| 二期 | P11 题库标签管理 | 扩展专业题库和抽题标签 | 保存标签规则 | 题库生效 |
| 三期 | P12 学生授权 | 学生授权导师查看训练摘要 | 确认授权 | P14 |
| 三期 | P13 导师任务台 | 导师创建班级训练任务 | 发布训练任务 | 学生收到任务 |
| 三期 | P14 授权学生报告 | 导师查看授权范围内报告 | 写辅导备注 | 学生/导师复盘 |
| 三期 | P15 班级批量报告 | 脱敏汇总班级薄弱点和完成率 | 导出脱敏报告 | 机构辅导 |
| 最终 | P16 语音训练 | 口头回答、转文字和表达反馈 | 提交语音 | 语音复盘 |
| 最终 | P17 视频模拟 | 模拟现场答辩和视频回放 | 开始视频模拟 | 视频复盘 |
| 最终 | P18 学校规范库 / 组织看板 | 来源核验规范库和组织质量管理 | 查看脱敏趋势 | 组织分析 |

## 关键转场

| from_screen | action | to_screen | system_feedback |
| --- | --- | --- | --- |
| P1 | 开始生成问题 | P2 | 根据资料完整度生成通用或个性化题组 |
| P2 | 提交回答 | P3 | 返回评分、追问或单题复盘 |
| P3 | 下一题 | P2 / P4 | 有剩余题回到答题，无剩余题生成报告 |
| P4 | 开始复练 | P5 | 低分模块加权抽题 |
| P4 | 导出摘要 | P10 | 只导出训练摘要，不导出完整论文资料 |
| P7 | 生成页级问题 | P2 | 题目绑定 PPT 页或论文章节 |
| P8 | 进入专项复练 | P9 | 带入历史低分模块 |
| P12 | 确认授权 | P14 | 导师获得授权范围内报告 |
| P13 | 发布训练任务 | P1 / P2 | 学生收到班级任务并开始训练 |
| P16 | 提交语音 | P3 / P4 | 转写后进入评分和复盘 |
| P18 | 查看脱敏趋势 | P15 / 组织看板 | 样本过少时隐藏细分数据 |

## 异常状态覆盖

| 场景 | 原型覆盖方式 |
| --- | --- |
| 资料不足 | P1 提示进入通用训练，P6 可补充资料 |
| 空回答 | P2 提交前校验，阻止空回答 |
| 高风险代写 / 编造 | P1 / P2 触发诚信拦截 |
| 模型失败 | P2 / P4 回退固定题库和通用模板 |
| 待补充事实 | P3 标记待补充依据 |
| 删除资料 | P6 展示删除影响和不可恢复提示 |
| 导出隐私 | P10 默认不导出完整论文资料 |
| 授权撤销 | P12 明确授权范围和有效期 |
| 未授权查看 | P14 不展示未授权学生报告 |
| 样本过少 | P15 / P18 不展示细分模块 |
| 麦克风 / 摄像头拒绝 | P16 / P17 回到文字训练 |
| 规范来源缺失 | P18 不允许使用未核验规范训练 |

## 视觉 QA

| 检查项 | 结果 |
| --- | --- |
| text_overlap_checked | true |
| centered_text_checked | true |
| clipping_checked | true |
| contrast_checked | true |
| png_matches_source_checked | true |

## 评审问题

- P1-P6 是否足够支撑一期 MVP 开发？
- P7-P11 是否覆盖二期个人训练效率增强的主要入口？
- P12-P15 的授权和脱敏边界是否符合你对导师/机构协作的预期？
- P16-P18 是否应该继续拆成更细的最终阶段子原型？
