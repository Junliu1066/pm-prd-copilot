# C16 项目 Package / Zip 生命周期审查

- 日期：2026-05-03
- 状态：proposal / package lifecycle review，不是 stable policy。
- 授权等级：L1 审查与台账更新；不执行 L2 staging / commit，不执行 L3 删除 / 归档。
- 主线任务：把项目里的 zip、HTML 原型包、交付包和 archive 包分层管理，防止包类产物继续污染稳定治理提交。

## 1. 结论

当前仓库里有 12 个压缩包，其中 11 个在 `projects/` 下，1 个在 `docs/archive/root-files/` 下。它们不应统一提交，也不应统一删除。

推荐总原则：

1. 项目内 zip 默认是项目产物，不进入 stable core。
2. 已进入 `projects/_archives/delivery-packages/` 的 zip 默认是 archive evidence，不再回流到项目根目录。
3. 同一项目出现多个完整交付包时，只保留一个 canonical package，其它列为 duplicate candidate。
4. HTML 原型 zip 是原型阶段产物，只在项目 closeout / 归档时处理。
5. 所有删除必须先归档、列精确清单、满 30 天后再二次批准。

## 2. 当前发现的包

| 路径 | 大小 | 类型判断 | 当前建议 |
|---|---:|---|---|
| `projects/_archives/delivery-packages/jiaxiaoqian-ai-invest-research-external-redacted-20260428.zip` | 47K | 外部脱敏交付包 archive evidence | 保留在 archive，不回流。 |
| `projects/_archives/delivery-packages/jiaxiaoqian-ai-invest-research-B-20260428.zip` | 11K | B 包 archive evidence | 保留在 archive，不回流。 |
| `projects/_archives/delivery-packages/jiaxiaoqian-ai-invest-research-internal-full-20260428.zip` | 78K | 内部完整包 archive evidence | 保留在 archive，不回流。 |
| `projects/_archives/delivery-packages/jiaxiaoqian-ai-invest-research-A-internal-20260428.zip` | 76K | A 内部包 archive evidence | 保留在 archive，不回流。 |
| `projects/_archives/delivery-packages/jiaxiaoqian-ai-invest-research-devdoc-regenerated-20260428.zip` | 73K | 开发文档再生成包 archive evidence | 保留在 archive，不回流。 |
| `projects/santoip-ai-brand-video/prototype/santoip-ai-brand-video-html-prototype.zip` | 35K | HTML 原型项目产物 | 项目内保留，归档前再审。 |
| `projects/prompt-optimization-workbench/prototype/evaluation-report-detail-html-prototype.zip` | 46K | HTML 原型项目产物 | 项目内保留，C13 审查时一起判断。 |
| `projects/ai-collaboration-efficiency-platform/prototype/ai-collaboration-efficiency-html-prototype.zip` | 2.9M | HTML 原型项目产物 | 项目内保留，C12 已标记归档前再审。 |
| `projects/jiaxiaoqian-ai-invest-research/价小前投研_完整开发交付包.zip` | 12M | 完整交付包，含原始 PDF / 截图 / 文档 | duplicate / sensitive candidate，暂不提交。 |
| `projects/jiaxiaoqian-ai-invest-research/jiaxiaoqian_ai_invest_complete_dev_package.zip` | 12M | 英文命名完整交付包，含 source_request.pdf / 截图 / 文档 | 暂定 canonical project package，归档前再审。 |
| `projects/jiaxiaoqian-ai-invest-research/价小前投研_多管家平台_PRD和开发文档.zip` | 17K | 小型 PRD + 开发文档包 | duplicate candidate，暂不提交。 |
| `docs/archive/root-files/prd_skill_kit_2026.zip` | 53K | root cleanup archive evidence | 已属 E 批 archive evidence，不处理。 |

## 3. 关键发现

### 3.1 Jiaxiaoqian 有重复完整交付包

两个 12M 完整包内容高度接近：

- `价小前投研_完整开发交付包.zip`
- `jiaxiaoqian_ai_invest_complete_dev_package.zip`

差异主要是包内目录和部分文件命名。中文包存在 zip 编码乱码风险；英文包命名更稳定，且文件名更适合后续脚本或外部分发审查。

建议：

- 暂定英文包为 canonical project package。
- 中文 12M 包列为 duplicate candidate。
- 不现在删除；进入归档后 30 天删除候选前，需要用户再次批准。

### 3.2 HTML 原型包不等于 stable UI 资产

以下包都是项目原型产物：

- `santoip-ai-brand-video-html-prototype.zip`
- `evaluation-report-detail-html-prototype.zip`
- `ai-collaboration-efficiency-html-prototype.zip`

它们可以帮助项目验收和回看，但不能进入稳定架构、PRD 主链路或 UI 默认产物。

建议：

- 项目内保留。
- 项目 closeout 时记录是否有 HTML 原型。
- 归档前再判断是否保留 zip，或只保留解压后的 canonical HTML / manifest。

### 3.3 Archive delivery packages 只能当证据

`projects/_archives/delivery-packages/` 下的 5 个 Jiaxiaoqian 包已经是 archive evidence。它们的用途是证明过去生成过不同分发版本，不是当前项目的活跃交付源。

建议：

- 不回流到项目根目录。
- 不和 stable core 一起提交。
- 后续 archive 策略确认后，作为 archive evidence 小批次处理。

## 4. 生命周期规则候选

以下只是候选规则，不直接 stable：

| 规则候选 | 建议 |
|---|---|
| package manifest | 每个保留的 zip 都应有来源、受众、生成时间、是否脱敏、是否 canonical、是否可替代。 |
| canonical package | 每个项目同一交付类型最多保留一个 canonical zip。 |
| duplicate package | 同内容、不同命名、旧版本或乱码风险包列为 duplicate candidate。 |
| prototype zip | 原型 zip 默认是项目阶段产物，closeout 前不提交到治理核心。 |
| archive evidence | archive 包只能证明历史，不作为当前执行源。 |
| delete after 30 days | duplicate / 临时 zip 满足归档后 30 天且用户二次批准后才硬删除。 |

## 5. 后续建议

### L1 可自动做

- 维护包清单。
- 在 closeout 审查中标记项目是否有 zip / HTML 原型包。
- 对 zip 做只读目录检查。
- 更新台账。

### L2 需要批量审批

| 批量审批项 | 我的建议 | 效果 |
|---|---|---|
| 是否提交本 C16 审查报告 | 后续和 C12 / C13 / C14 项目审查记录一起提交 | 保留 package 生命周期判断，但不增加碎提交。 |
| 是否把英文 Jiaxiaoqian 完整包标为 canonical | 暂定 canonical，后续归档前确认 | 减少重复包判断成本，但现在不删除中文包。 |
| 是否后续为 zip 建统一 manifest 模板 | 暂缓 | 当前先用审查表即可，避免新增工具或模板。 |

### L3 必须单独审批

- 删除任何 zip。
- 移动任何 zip 到 archive。
- 对外发布任何 zip。
- 把 package 生命周期规则写入 stable policy。
- 新增 package 管理脚本或 harness。

## 6. 本轮不做

- 不删除 zip。
- 不移动 zip。
- 不解压 zip 到仓库。
- 不提交项目 zip。
- 不提交 `projects/*`。
- 不改 package 脚本、workflow、harness 或 registry。
- 不把本方案写入 stable policy。

## 7. 推荐状态

建议在台账中增加：

```text
C16 package_zip_lifecycle_review_done
```

下一步可继续 C13 `prompt-optimization-workbench` 和 C14 `santoip-ai-brand-video` 低证据项目审查。
