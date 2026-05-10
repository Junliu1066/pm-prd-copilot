# Prompt 优化工作台 HTML 原型说明

## 来源

- 新上传的 8 张页面截图：Datasets、Settings、Knowledge、Compare、Optimize、Evaluations、Runs、Models。
- 本次按这些截图重新生成 HTML 结构，不沿用旧版固定高度布局。

## 已实现范围

- 统一的左侧导航、顶部搜索、顶部操作区。
- Datasets 页面：测试集概览卡片、测试集列表、测试集详情、Cases、评分规则、导入导出与历史。
- Settings 页面：用户信息、默认参数、模型默认配置、评测配置、导出与日志设置、系统状态侧栏。
- Knowledge 页面：知识沉淀统计、规则/样例/失败模式等页签、分类筛选、规则列表、知识详情。
- Compare 页面：版本对比配置、核心指标变化、旧版/新版对比、发布建议、Case 对比。
- Optimize 页面：优化构建器、目标数据、候选版本、回归测试结果、最佳候选详情。
- Evaluations 页面：评测指标、筛选、Summary、分项得分、通过失败分布、失败/风险 Case、Case 详情。
- Runs 页面：Run Builder、运行队列、Run List、Run Detail。
- Review 页面：人工评审任务、版本指标对比、规则检查、Case 变更示例、评分、决策、评论和提交记录。
- Models 页面：Provider 概览、凭证列表、连接日志、默认模型设置。
- Dashboard、Prompts 与创建 Prompt：作为可点击入口与创建流程保留，方便后续补图扩展。

## 可点击交互

- 点击左侧导航：切换到对应页面，并同步高亮与标题。
- 点击页面内页签：切换高亮并显示反馈。
- 点击 Knowledge 页的“规则库 / 样例库 / 失败模式库 / 最佳实践 / Skill 候选池”：跳转到对应模块内容。
- 点击表格中的“查看”：选中当前行并显示操作反馈。
- 点击 Datasets 表格“查看 / 编辑 / 更多”：进入 Dataset 详情或编辑页，展示对应测试集内容。
- 点击 Knowledge 表格“查看”：进入知识条目详情页，展示规则说明、推荐写法、适用条件、收益和关联资源。
- 点击普通按钮：显示明确反馈，避免死点击。
- 点击顶部“新建 Run”：进入 Runs 页面。
- 点击左侧 Review 或 Runs 里的“提交人工评审”：进入人工评审模块。
- 在 Review 页面可调整评分、选择通过/有条件通过/不通过、保存草稿或提交评审。
- 点击顶部“创建 Prompt”：进入创建 Prompt 页面，而不是只弹提示。
- 点击 Dashboard 快捷入口：进入 Datasets、Optimize、Compare、Models。
- 双击普通文本：原位编辑；Enter 保存，Esc 取消，失焦自动保存。
- 文本修改保存在当前浏览器本地存储，不会写回源码。

## 跨平台打开方式

- 推荐交付：发送 `prompt-optimization-workbench-html-prototype.zip`，对方解压后双击 `html/index.html`。
- 单文件版本：双击 `standalone.html`，适合只发一个文件的场景。
- macOS：双击 `index.html`，或双击 `open-mac.command`。
- Windows：双击 `index.html`，或双击 `open-windows.bat`。
- 不需要安装依赖，不需要启动服务。
- 如果发送源码结构，请发送整个 `html` 文件夹，不要只发送单独的 `index.html`。

## 本次修正重点

- 移除旧版固定高度容器，页面改为自然纵向滚动，避免底部内容缺失。
- 表格区域增加横向滚动和固定列宽，避免与右侧模块重叠。
- 所有核心页面统一进入一个 HTML 原型，适合产品经理连续点击走查。
- 所有资源使用相对路径，支持 Windows 和 macOS 解压后直接打开。
- Settings 页移除顶部重复页签，仅保留实际配置模块标题。
- Knowledge 页顶部模块入口改为真实模块跳转，并补齐样例库、失败模式库、最佳实践、Skill 候选池内容。

## 后续待补

- 本次新图没有提供 Prompts 详情页，当前补了 Prompt 列表入口和创建 Prompt 页面骨架。
- 如果后续提供更高清图片，可以继续细化字段、表格行数和图表比例。
