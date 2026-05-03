# C6 Demo Prototype 项目产物审查

- 日期：2026-05-02
- 状态：审查报告，不批准 staging、commit、push、PR、归档、删除、长期规则写入或 candidate 转 stable。
- 范围：`projects/demo-project/prototype/`
- 主线任务：判断 demo 原型产物是否适合进入项目证据，避免项目 PNG / UI 风格材料污染稳定治理核心。

## 结论

`projects/demo-project/prototype/` 属于项目级原型过程产物，不属于稳定治理核心。

当前建议：暂不提交、不删除、不归档，先项目内保留。等 demo fixture 最小保留集和 PRD -> 原型链路稳定后，再决定是否作为 C 批项目证据单独提交。

## 当前文件

| 文件 | 类型 | 当前判断 |
|---|---|---|
| `page_png/01_export_dashboard.png` | 页面 PNG | 可作为“导出中心首页 / 工作台”原型证据。 |
| `page_png/02_create_export_task.png` | 页面 PNG | 可作为“新建导出任务”原型证据。 |
| `page_png/03_export_task_detail.png` | 页面 PNG | 可作为“导出任务详情 / 状态追踪”原型证据。 |
| `page_png/04_field_permission_config.png` | 页面 PNG | 可作为“字段与权限配置”原型证据。 |
| `page_png/05_audit_log.png` | 页面 PNG | 可作为“审计日志”原型证据。 |
| `page_png/prototype_contact_sheet.png` | 汇总图 | 可用于快速审阅，不适合作为稳定模板。 |
| `ui_style_direction.md` | UI 风格建议 | 标记为 draft for human review，适合保留为项目过程材料。 |
| `ui_style_direction.json` | UI 风格结构化输出 | 适合后续验证 UI style selector 输出，不应写成长期默认风格。 |

## 功能效果

如果后续保留这批原型产物，能达到的效果：

- 验证 PRD 阶段“页面说明 + 页面跳转关系 + 原型图层”是否能继续走到页面 PNG。
- 验证 UI 风格选择器能输出可审阅的风格方向，而不是直接生成最终 UI。
- 给后续 Codex 开发文档提供页面级参考，但不把 PNG 当作唯一实现依据。
- 暴露 PRD 与原型之间的不一致，便于继续修复链路。

它不能达到的效果：

- 不能证明 demo PRD 已经是高质量 golden sample。
- 不能证明 UI 风格选择器可以稳定转正。
- 不能作为所有项目默认 UI 风格。
- 不能替代后续 HTML / 高保真 UI / 开发实现审核。

## 架构影响

正向影响：

- 支撑 C 批项目证据，证明原型链路已经能产出页面级视觉材料。
- 有助于检查“PNG 可以单独输出到项目文件夹，PRD 正文只保留示意或引用”这个规则。
- 有助于后续形成原型产物的保留边界：项目目录内保留，稳定核心不引用具体 PNG。

风险：

- PNG 是二进制文件，直接提交会增加仓库体积和 diff 审查成本。
- 当前 demo PRD 本身很短，prototype 比 PRD 更完整，可能让模型误以为“原型可以替代 PRD 结构”。
- 页面主题集中在导出、权限、审计，不能泛化为普通 0-1 PRD 的稳定样例。
- UI 风格为 `swiss_utility`，只适合这类后台工具，不应沉淀为全局默认审美。

## 处理选项

| 选项 | 效果 | 优势 | 劣势 / 风险 | 我的建议 |
|---|---|---|---|---|
| A. 现在提交 prototype 全部文件 | 把 PRD -> 原型过程证据纳入仓库 | 工作区更干净；原型链路有实物证据 | 二进制 PNG 增加噪音；demo PRD 太短，容易过拟合；不利于稳定核心保持轻量 | 暂不选 |
| B. 项目内保留，暂不提交 | 保留现场，后续再按 C 批单独处理 | 最稳；不污染稳定核心；仍可复核原型链路 | 工作区继续有未跟踪目录 | 推荐 |
| C. 移入 archive 候选 | 把原型当作历史证据，不再参与当前链路 | 工作区更清晰 | 会降低后续验证 PRD -> 原型链路的价值 | 暂缓 |
| D. 删除或 30 天后删除候选 | 彻底减少噪音 | 仓库最轻 | 会丢失原型链路真实输出证据 | 不推荐 |

## 需要你后续拍板

| 拍板项 | 我的建议 | 不同选择的结果 |
|---|---|---|
| 是否提交 demo prototype | 暂不提交 | 提交会留下原型证据，但增加二进制噪音；暂不提交更利于先稳定架构。 |
| 是否把 demo prototype 作为原型链路样例 | 只作为观察样例 | 作为稳定样例会过早固化；观察样例能继续暴露问题。 |
| 是否把 `swiss_utility` 设为长期默认风格 | 不设默认 | 设默认会限制未来项目风格；不设默认更符合按项目判断。 |
| 是否允许后续单独提交 contact sheet 而不提交全部 PNG | 可以后续评估 | 只提交汇总图更轻，但会损失页面级细节。 |
| 是否把 prototype 纳入 demo 最小 fixture | 暂不纳入 | 纳入会让 fixture 变重；暂不纳入能保持 regression fixture 轻量。 |

## 本轮不做

- 不 staging / commit `projects/demo-project/prototype/`。
- 不删除或移动 prototype 文件。
- 不把 prototype 写入稳定治理文档。
- 不把 `swiss_utility` 写成长期默认 UI 风格。
- 不生成新的 PNG / HTML / 高保真 UI。
- 不修改 skill、harness、workflow、registry 或长期偏好。
