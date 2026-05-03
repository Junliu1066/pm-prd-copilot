# Projects 生命周期盘点报告

- 日期：2026-05-02
- 状态：项目生命周期审查清单，不批准删除、移动、归档、staging、commit、push、PR、长期记忆写入或项目产物提交。
- 范围：`projects/*` 当前可见项目目录。
- 主线任务：判断每个项目的生命周期状态，防止项目产物继续污染稳定治理核心，并为后续 closeout / archive / 30 天删除候选提供监督清单。

## 结论

当前不建议提交任何项目产物，也不建议归档或删除任何项目目录。

推荐分类：

| 项目 | 推荐状态 | 当前动作 | 原因 |
|---|---|---|---|
| `demo-project` | `fixture_active` | 保留为治理测试 fixture | 已承担 regression / harness 测试现场；prototype 暂不提交。 |
| `fitness-app-mvp` | `active_project` | 项目内保留 | 项目偏好缓存仍 active，final 产物未完成。 |
| `taxi-hailing-prd-test` | `golden_sample_candidate` | 保留候选，不转 stable | final PRD 结构价值高，但需脱敏和多样例组合后再稳定化。 |
| `graduation-defense-agent` | `closeout_candidate_reviewed` | 保留，等待后续 closeout 拍板 | C9 已完成 closeout 审查，确认 `答辩.md` 是项目原始输入证据候选，但还不能自动归档。 |
| `jiaxiaoqian-ai-invest-research` | `closeout_candidate_high_value_reviewed` | 保留，等待后续 package / zip 处置拍板 | C10 已完成 high-value closeout 审查，确认其适合沉淀架构候选，但不能直接提交项目或升级 golden sample。 |
| `ai-collaboration-efficiency-platform` | `closeout_candidate_needs_refresh` | 保留，需刷新 closeout 证据后再判断 | 目录有完整文档和 prototype，但 closeout 扫描数异常偏低。 |
| `prompt-optimization-workbench` | `archive_candidate_needs_review` | 暂不归档，后续确认是否仍有价值 | 主要是 prototype zip 和 closeout，证据较薄。 |
| `santoip-ai-brand-video` | `archive_candidate_needs_review` | 暂不归档，后续确认是否仍有价值 | 主要是 prototype zip 和 closeout，证据较薄。 |
| `temp-generated-project` | `temporary_project` | 暂不删除，后续可进 30 天候选 | 明确 temporary，仍有 blocked questions。 |
| `projects/_archives` | `archive_area_candidate` | 保留，不扩大提交 | 包含 Jiaxiaoqian 交付包归档，需和正式 archive 策略对齐。 |

## 当前证据摘要

| 项目 | 文件数 | 大小 | closeout | project_state | 关键证据 |
|---|---:|---:|---|---|---|
| `demo-project` | 29 | 已跟踪为主 | 已提交 closeout | 有 | governed fixture，last run `pipeline-latest`。 |
| `fitness-app-mvp` | 38 | 项目中等 | 有 closeout 草案 | 有 | `preference_cache.status=active`，final PRD / stories 只有标题。 |
| `taxi-hailing-prd-test` | 14 | 112K | 有 closeout 草案 | 无 | closeout 标记 final PRD 是黄金样例候选。 |
| `graduation-defense-agent` | 54 | 13M | 有 closeout 草案 | 有 | 已有 AI 方案、delivery、Codex 开发文档、完整 prototype。 |
| `jiaxiaoqian-ai-invest-research` | 31 | 26M | 有 closeout 草案 | 无 | 含多个 PRD / 开发文档 / zip / prototype / B 包，架构反馈价值高。 |
| `ai-collaboration-efficiency-platform` | 17 | 15M | 有 closeout 草案 | 无 | 有产品文档、开发文档、图表、HTML prototype zip；closeout 扫描文件数显示 1，需刷新。 |
| `prompt-optimization-workbench` | 8 | 288K | 有 closeout 草案 | 无 | 主要是 prototype zip 和 closeout。 |
| `santoip-ai-brand-video` | 8 | 236K | 有 closeout 草案 | 无 | 主要是 prototype zip 和 closeout。 |
| `temp-generated-project` | 9 | 64K | 只有 architecture-feedback | 有 | 明确 `temporary: true`，blocked questions 未解决。 |
| `projects/_archives` | 5 | 296K | 无 | 无 | 全是 Jiaxiaoqian delivery package zip。 |

## 项目逐项判断

### 1. `demo-project`

状态：`fixture_active`

判断：

- 已提交治理 fixture、run evidence 和 closeout evidence。
- 当前仍有 `prototype/` 未跟踪，但已判定为项目原型过程产物。
- 不应把 prototype PNG 混入稳定核心。

建议：

- 继续作为 regression / harness fixture。
- 不提交 prototype，除非后续作为 C 批项目证据单独提交。

### 2. `fitness-app-mvp`

状态：`active_project`

判断：

- `project_state.json` 显示项目偏好缓存 active。
- `memory-cache` 仍属于项目内上下文。
- `02_prd.final.md` 和 `03_user_stories.final.md` 只有标题，不能作为完成交付物。

建议：

- 不归档、不清空缓存、不提交项目产物。
- 后续如果继续项目，应另开项目线程。
- 如果暂停，应先做 closeout review 和偏好缓存逐条处置。

### 3. `taxi-hailing-prd-test`

状态：`golden_sample_candidate`

判断：

- closeout 明确 `02_prd.final.md` 是结构黄金样例候选。
- 它暴露并修复了 0-1 PRD 的关键问题：测试目的误入产品目标、非 AI 项目 AI 选型、图表位置、页面说明和原型图层。
- 但单个样例不能直接变稳定 golden sample。

建议：

- 保留为候选。
- 后续做脱敏通用版，再和 2-3 个 PRD 组成 golden sample portfolio。
- 不直接提交为 stable baseline。

### 4. `graduation-defense-agent`

状态：`closeout_candidate_reviewed`

判断：

- 有 PRD、AI 方案、delivery plan、Codex 开发文档、完整 prototype。
- `project_state.json` 标记完成 delivery planning、AI solution planning、agentic delivery planning、codex blueprint 等。
- 它可能是“PRD -> AI 方案 -> Codex 开发文档 -> prototype”的高价值样例。
- C9 closeout 审查已确认 `docs/archive/notes/答辩.md` 与该项目原始输入高度相关，应作为项目原始输入证据候选。
- 但 closeout 不等于已归档，项目产物和 `答辩.md` 都不能自动提交、移动或删除。

建议：

- 暂不提交、暂不归档。
- 后续如进入正式归档，先由你拍板 `答辩.md`、`00_complete_delivery_package.md`、`.DS_Store` 和 prototype 的处置。
- 不在当前治理线程展开答辩产品功能。

### 5. `jiaxiaoqian-ai-invest-research`

状态：`closeout_candidate_high_value_reviewed`

判断：

- 体量最大，包含 PRD、开发文档、多管家开发文档、B 包、prototype、多个 zip。
- closeout architecture feedback 提到权限边界、审计日志、fallback 污染、非导出类项目回归等高价值反哺。
- 历史旧口径可能仍存在，不能直接作为稳定样例。
- C10 已确认内部完整包、外部 B 包、外部脱敏包、金融合规专项规则和 zip 生命周期都有治理价值，但不能混入稳定核心。

建议：

- 暂不提交全部项目。
- 后续单独做 package / zip 处置清单。
- 金融合规、B 包边界、fallback 污染和敏感操作审计先进入架构候选，不直接 stable。

### 6. `ai-collaboration-efficiency-platform`

状态：`closeout_candidate_needs_refresh`

判断：

- 目录有产品文档、开发文档、思维导图、流程图、prototype wireframes、HTML prototype zip。
- closeout 报告显示扫描文件数为 1，与实际目录文件明显不一致。
- 说明 closeout 证据可能过期或生成时上下文不完整。

建议：

- 暂不归档。
- 后续如要处理，先刷新 closeout 或重新生成项目盘点。
- 不直接把当前 closeout 当作可靠归档依据。

### 7. `prompt-optimization-workbench`

状态：`archive_candidate_needs_review`

判断：

- 主要文件是 prototype zip 和 closeout 五件套。
- 没有明显 final PRD / project_state。
- 证据较薄，可能是历史原型输出或临时项目。

建议：

- 暂不提交、不删除。
- 后续确认是否仍有项目价值；若无，进入 archive candidate，再 30 天后删除候选。

### 8. `santoip-ai-brand-video`

状态：`archive_candidate_needs_review`

判断：

- 主要文件是 prototype zip 和 closeout 五件套。
- 没有明显 final PRD / project_state。
- 证据较薄，可能是历史原型输出或临时项目。

建议：

- 暂不提交、不删除。
- 后续确认是否仍有项目价值；若无，进入 archive candidate，再 30 天后删除候选。

### 9. `temp-generated-project`

状态：`temporary_project`

判断：

- `project_state.json` 明确 `temporary: true`。
- 记录了 blocked questions：真实业务主题未指定、是否产品化未确认、是否接入 AI 自动生成未确认。
- 属于临时生成项目，不应稳定化。

建议：

- 暂不删除。
- 后续如果确认无复用价值，可列入 archive candidate 或 30 天后删除候选。
- 不把它沉淀为稳定模板或 skill。

### 10. `projects/_archives`

状态：`archive_area_candidate`

判断：

- 当前包含 Jiaxiaoqian 交付包 zip。
- 是项目交付包归档区，不是 active project。
- 需要和 archive / deletion 生命周期对齐。

建议：

- 保留，不扩大提交。
- 后续随 Jiaxiaoqian 项目 closeout 一起判断是否正式归档或 30 天后删除候选。

## 需要用户后续拍板

| 拍板项 | 我的建议 | 不同选择的效果 |
|---|---|---|
| `graduation-defense-agent` 是否进入正式 closeout | 暂缓，保持 `closeout_candidate_reviewed` | 已完成 C9 审查；继续暂缓最稳，避免项目产物过早归档或提交。 |
| `jiaxiaoqian-ai-invest-research` 后续怎么处理 | 暂缓项目提交，后续做 package / zip 处置清单 | C10 已完成审查；继续暂缓最稳，避免 26MB 项目产物污染仓库。 |
| `taxi-hailing-prd-test` 是否升级 golden sample | 暂不升级 | 先脱敏通用化和多样例组合更稳。 |
| `temp-generated-project` 是否进入 30 天删除候选 | 后续可进入 | 它明确 temporary，但仍需你确认不再复用。 |
| `prompt-optimization-workbench` / `santoip-ai-brand-video` 是否归档候选 | 后续可进入 | 证据较薄，适合先确认是否仍有项目价值。 |
| `ai-collaboration-efficiency-platform` 是否刷新 closeout | 建议刷新后再判断 | 当前 closeout 扫描数异常，直接归档风险高。 |
| `_archives` 是否提交 | 暂不提交 | 避免项目交付包归档策略未定就固化。 |

## 推荐后续顺序

1. `taxi-hailing-prd-test` golden sample candidate 脱敏方案。
2. `ai-collaboration-efficiency-platform` 刷新 closeout 或重新盘点。
3. `prompt-optimization-workbench`、`santoip-ai-brand-video`、`temp-generated-project` 归档 / 30 天删除候选审查。
4. `projects/_archives` 和项目 zip 统一归档策略。

## 本轮不做

- 不 staging / commit 任何 `projects/*`。
- 不删除项目。
- 不移动项目。
- 不归档项目。
- 不清空项目缓存。
- 不把项目经验写入长期记忆。
- 不把任何项目升级为 golden sample。
- 不修改 skill、harness、workflow、registry、pipeline 或 automation。
