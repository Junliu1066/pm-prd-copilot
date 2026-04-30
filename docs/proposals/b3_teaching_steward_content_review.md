# B3 Teaching / Steward 内容边界审查

- 日期：2026-04-29
- 状态：决策记录，只记录审查结论；不批准 staging、commit、push、PR、归档、删除、长期记忆写入、skill / harness / steward 转 stable。
- 范围：`teaching/*` 和 `stewards/*.md`
- 原则：长期稳定优先；不能把项目经验、阶段性偏好或 steward 权限过度长期化。

## 结论

B3 不能按原始状态直接进入稳定治理文档。原因是它涉及用户教学记录、长期偏好和 steward 操作权限，如果 wording 过宽，会影响后续所有 PRD、开发文档、原型和项目偏好处理。

推荐处理：

1. 保留 B3 作为治理决策记录。
2. teaching 里的长期偏好必须经过用户显式确认。
3. steward 文档必须写清职责、输入、输出、禁止事项和需要用户批准的动作。
4. 不新增 steward，不新增 skill，不新增 harness。

## 文件审查结论

| 文件 | 结论 | 原因 | 建议动作 |
|---|---|---|---|
| `teaching/accepted_lessons.md` | 需要收窄后再稳定 | 原有“每个 PRD 固定五图”“每个产品文档配开发文档”等表达过宽 | 改成 PRD 视觉底线 + 按项目必要性选择图表 |
| `teaching/open_lessons.md` | 可保留候选 | 已明确是待确认经验，不自动生效 | 只作为候选记录 |
| `teaching/teaching_log.md` | 可保留证据 | 有助追溯用户教学过程，但不能覆盖已批准规则 | 作为证据，不作为自动规则 |
| `teaching/user_preferences.md` | 需要用户显式确认 | 会直接影响未来行为 | 逐条确认后再稳定 |
| `stewards/ai_architecture_steward.md` | 可作为候选协议 | 能限制 AI 方案只在 AI 项目或用户明确要求时触发 | 后续可单独提交 |
| `stewards/ai_coaching_steward.md` | 可作为候选协议 | 记忆、隐私、审批边界较清楚 | 后续可单独提交 |
| `stewards/capability_enablement_steward.md` | 可作为候选协议 | 符合“如无必要，不增 skill / harness” | 后续可单独提交 |
| `stewards/delivery_planning_steward.md` | 可作为候选协议 | 保留范围、外部服务、push/PR、破坏性操作审批边界 | 后续可单独提交 |
| `stewards/development_governance_steward.md` | 可作为候选协议 | 覆盖合同对齐和读写边界 | 后续可单独提交 |
| `stewards/learning_steward.md` | 原始状态需修正 | 需要补充项目偏好缓存写入、清除、归档前处置审批边界 | 修正后再进入后续批次 |
| `stewards/prototype_design_steward.md` | 原始状态需修正 | 需要补充完整原型、HTML、UI 风格长期化的审批边界 | 修正后再进入后续批次 |

## 需要避免的问题

| 风险 | 影响 | 处理方式 |
|---|---|---|
| 把项目经验写成永久规则 | 后续不同项目会被错误套用 | 项目经验先入收件箱或 closeout，长期化需用户批准 |
| PRD 图表规则固定过死 | 简单项目被迫输出无意义图表 | 稳定底线是页面说明、页面跳转关系、原型图层；其它图表按必要性选择 |
| Codex 开发文档默认泛化 | 非开发就绪文档会变重 | 仅在开发就绪 PRD、Codex 开发规划或用户要求时输出 |
| 开发包包含“所有资产” | 包过重，且可能泄露内部治理信息 | 按受众、阶段、脱敏策略和执行需要打包 |
| steward 权限过宽 | 后续可能越权修改长期规则或缓存 | 必须写清审批项和禁止事项 |

## 已形成的稳定口径

- PRD 必须有页面说明、页面跳转关系、原型图层。
- 思维导图、泳道图、MVP 范围图、风险闭环图等按项目必要性放在对应章节。
- 非 AI 项目不写 AI 模型选型。
- 项目偏好不能自动跨项目复用。
- 长期记忆必须逐条经用户批准。
- 完整原型、HTML、UI 风格长期默认、项目产物包生成都需要用户确认。

## 后续建议

B3 后续可以作为单独批次处理，但必须满足：

```text
只提交已收窄的 teaching / steward 文档
不提交 memory-cache
不把 open lessons 当 stable
不新增 skill / harness / workflow / plugin
不自动写长期记忆
```
