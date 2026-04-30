# D1 Candidate Plugin Registry / Source 对齐审查

- 日期：2026-04-30
- 状态：决策记录，只记录 candidate plugin 对齐结论；不批准 push、PR、candidate 转 stable、删除、归档、长期记忆写入或自动化启用。
- 范围：`.agents/plugins/marketplace.json`、`registry/plugins.yaml`、`registry/skills.yaml`、candidate plugin 源码目录。
- 原则：candidate 能力可以可见，但必须明确是候选能力，不能被误当作稳定能力。

## 结论

D1 的核心问题不是“要不要新增稳定插件”，而是“已经可见的 candidate plugin 必须与 registry 和源码保持一致”。如果 marketplace 单独提交，而对应 registry / source 不提交，干净环境会看到候选插件入口，但找不到完整来源和技能合同。

推荐处理：

1. candidate plugin 保持可见。
2. marketplace、registry、skills、source 必须同批对齐。
3. 所有 candidate 必须保留 `candidate / non-stable / requires review` 标记。
4. 不把 candidate plugin 转 stable。
5. 不新增 harness，不新增 skill，只收口已存在的候选能力边界。

## 候选能力审查表

| Suite | Marketplace | Registry | Source | 建议 |
|---|---|---|---|---|
| `prd-analysis-suite` | candidate 可见 | candidate | 已存在 | 只保持 registry 对齐 |
| `prd-prototype-suite` | candidate 可见 | candidate | 需要纳入源码对齐 | 保持候选，只服务后期原型 / UI 链路 |
| `preference-memory-suite` | candidate 可见 | candidate | 需要纳入源码对齐 | 保持候选，项目偏好不得跨项目复用 |
| `quality-evaluation-suite` | candidate 可见 | candidate | 需要纳入源码对齐 | 保持候选，用于质量评估，不默认扩大主链路 |
| `delivery-planning-suite` | candidate 可见 | candidate | 需要纳入源码对齐 | 保持候选，Codex 开发规划按需触发 |
| `ai-solution-planning-suite` | candidate 可见 | candidate | 需要纳入源码对齐 | 保持候选，AI 方案 detachable，不并入普通 PRD 默认流程 |

## 必须保留的候选边界

- `status` 必须是 candidate。
- `stable` 或 `stable_use_allowed` 必须保持 false。
- 必须标记需要用户审核后才能稳定使用。
- 不允许 candidate 自动进入主 workflow。
- 不允许 candidate 自动写长期记忆。
- 不允许 candidate 被当成稳定 skill / harness。

## 已验证的关键点

| 检查 | 结论 |
|---|---|
| marketplace 与 registry plugin 名称 | 对齐 |
| registry plugin 与 skills 映射 | 对齐 |
| candidate plugin source 与 skill 路径 | 对齐 |
| `plugin.json` 与 marketplace 名称 | 对齐 |
| candidate guardrail | 保留 |
| 项目特定泄漏 | 未发现阻断项 |

一个可接受的特殊情况：

```text
plugins/prd-prototype-suite/skills/interactive-html-prototype-builder/scripts/package_html_prototype.py
```

该文件中出现 `/Users/` 是作为安全扫描的禁止模式，不是项目路径泄漏。

## 不允许混入 D1 的内容

| 范围 | 原因 |
|---|---|
| `plugins/**/__pycache__/*` | 运行缓存，不是源码 |
| `harness/*` | harness 候选另批处理 |
| `ai-intel/*` | AI 情报属于 B5c |
| `projects/*` | 项目产物属于 C 批 |
| `docs/proposals/*` | 审查材料不等于 plugin source |
| `docs/archive/*` | archive 属于 E 批 |
| `memory-cache/*` | 项目偏好需要 closeout / disposition |
| root 删除项 | 删除状态需要 E 批逐条批准 |

## 长期效果

这样处理的效果是：

- 干净环境不会出现 marketplace 可见但源码缺失的问题。
- candidate 能力边界更清楚，降低误用风险。
- 后续可以继续探索 PRD 原型、偏好记忆、质量评估、交付规划和 AI 方案，但不会污染主 PRD 流程。
- 符合“如无必要，不增 skill / harness”：本批只是候选能力对齐，不做稳定能力扩张。

## 后续建议

D1 后续如果再处理，只能按 candidate 批次单独做：

```text
marketplace + registry + skills + candidate source 一起对齐
不混入项目产物
不混入 AI 情报
不混入 harness 候选
不混入 root/archive 清理
```
