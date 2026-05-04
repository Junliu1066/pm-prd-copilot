# Projects 生命周期盘点报告

- 日期：2026-05-04
- 状态：项目产物生命周期台账，不是 stable policy。
- 主线任务：把 `projects/*` 剩余未跟踪产物分区，防止项目材料污染稳定治理核心。
- 本报告不批准：删除、移动、归档、提交项目目录、清空缓存、写长期记忆、push / PR。

## 总结论

项目产物已经和稳定治理核心分开。当前 tracked 修改已清空，剩余主要是未跟踪项目目录、原型、closeout、raw、memory-cache 和临时 proposal。

当前策略：

1. `demo-project` 继续作为治理测试 fixture。
2. `fitness-app-mvp` 继续 active；已提交 8 个分析证据文件，但 `memory-cache`、prototype、closeout 暂不提交。
3. `taxi-hailing-prd-test` 继续 golden sample candidate，不直接 stable。
4. 高价值项目先保留，不整包提交。
5. 低证据或 temporary 项目进入 archive / 30 天候选，但不立即删除。

## 当前项目分层

| 项目 / 范围 | 当前状态 | 推荐动作 | 不同选择的效果 |
|---|---|---|---|
| `demo-project` | `fixture_active` | 保留为治理测试 fixture | 保留能保证 regression / harness 有稳定现场；归档会削弱测试覆盖。 |
| `fitness-app-mvp` | `active_project` | 项目内保留，后续归档前再处理缓存 | 保持 active 能继续项目；现在归档会打断偏好缓存和原型链路。 |
| `taxi-hailing-prd-test` | `golden_sample_candidate` | 候选保留，后续脱敏组合成样例集 | 直接 stable 容易过拟合；候选保留更稳。 |
| `graduation-defense-agent` | `closeout_candidate_reviewed` | 保留，后续单独 closeout 拍板 | 该项目有 AI、delivery、Codex 开发和原型链路价值，但整包提交会污染仓库。 |
| `jiaxiaoqian-ai-invest-research` | `high_value_closeout_candidate` | 保留，后续处理 package / zip / B 包 | 价值高但体量大，必须单独审，不混入当前批次。 |
| `ai-collaboration-efficiency-platform` | `closeout_candidate_refreshed` | 项目内保留，不提交项目产物 | 可作为复杂 AI / Skill 治理产品证据，暂不稳定化。 |
| `prompt-optimization-workbench` | `prototype_artifact_closeout_candidate` | 保留为低证据原型候选 | 不作为 PRD 样例，不提炼 stable。 |
| `santoip-ai-brand-video` | `prototype_artifact_closeout_candidate` | 保留为业务原型候选 | 可后续对比 UI / UX 原型链路，但暂不提交。 |
| `temp-generated-project` | `temporary_project_evidence` | 放入 30 天删除候选 | 临时项目不适合长期堆积，但删除仍需到期二次确认。 |
| `projects/_archives` | `archive_area_candidate` | 保留，不扩大提交 | 当前是交付包归档区，需和项目 zip 生命周期一起处理。 |

## 已收口进度

| 范围 | 当前结果 |
|---|---|
| `demo-project` fixture | 已提交治理 fixture、run evidence、closeout evidence 和剩余 artifact disposition。 |
| `fitness-app-mvp` tracked 8 文件 | 已提交为项目分析证据，不再是 tracked 噪音。 |
| C12-C16 项目汇总 | 已完成 L1/L2 判断，结论是不提交项目目录、不提交 zip/HTML/PNG/raw 项目产物。 |
| 项目 zip / package | 已完成生命周期候选判断，后续单独处理 canonical / duplicate / archive evidence。 |

## 当前剩余项目产物

| 剩余范围 | 处理建议 | 原因 |
|---|---|---|
| `projects/demo-project/prototype/` | 暂不提交 | 原型过程产物，不影响治理 fixture。 |
| `projects/fitness-app-mvp/closeout/` | 暂缓 | closeout 是归档前审核材料，不等于项目已归档。 |
| `projects/fitness-app-mvp/prototype/` | 暂缓 | 原型仍可本地参考，等待项目是否继续推进。 |
| `projects/fitness-app-mvp/runs/plan-execution-preview-20260425/` | 暂缓 | 项目运行证据，和原型/缓存一起归档前再审。 |
| `projects/fitness-app-mvp/runs/prototype-preview-20260424/` | 暂缓 | 项目运行证据，暂不混入仓库。 |
| `projects/a-share-ai-quant-strategy-platform/` | 暂缓 | 小体量项目，但尚未完成独立生命周期判断。 |
| `projects/ai-collaboration-efficiency-platform/` | 保留候选 | 复杂 AI / Skill 治理产品证据，不能直接归档或提交。 |
| `projects/graduation-defense-agent/` | 保留候选 | 高价值端到端交付证据，后续单独 closeout。 |
| `projects/jiaxiaoqian-ai-invest-research/` | 保留候选 | 金融合规、B 包、zip 生命周期价值高，单独审。 |
| `projects/prompt-optimization-workbench/` | archive candidate | 低证据原型项目，后续可进入 30 天候选。 |
| `projects/santoip-ai-brand-video/` | archive candidate | 业务原型候选，暂不 stable。 |
| `projects/taxi-hailing-prd-test/` | golden sample candidate | 不直接 stable，后续脱敏组合样例集。 |
| `projects/temp-generated-project/` | 30 天删除候选 | temporary 项目，保留到到期复核。 |
| `projects/_archives/` | archive evidence candidate | 不提交 zip，不删除，等待 package 生命周期批次。 |

## 需要你后续拍板的功能项

| 拍板项 | 我的建议 | 选择后的效果 |
|---|---|---|
| 是否继续提交 `projects/*` 目录 | 暂不提交 | 工作区继续保留项目上下文，但稳定治理核心不被污染。 |
| 是否把 `fitness-app-mvp` closeout 提交 | 暂缓 | 避免被误认为项目已归档；等项目暂停或归档前再提交。 |
| 是否把 `taxi-hailing-prd-test` 转 golden sample | 暂不转 | 保持候选，等多样例组合后更稳。 |
| 是否清理 `temp-generated-project` | 放入 30 天候选 | 能瘦身，但不会马上删除，保留复核窗口。 |
| 是否提交原型 / zip / HTML | 暂不提交 | 避免项目体积膨胀和旧口径污染。 |
| 是否把项目经验写入长期记忆 | 不自动写 | 项目经验先入 architecture inbox 或 closeout，长期记忆必须逐条批准。 |

## 后续最快收口顺序

1. 缓存和 raw 批：确认 `memory-cache/`、`ai-intel/raw/` 只保留生命周期记录，不提交本体。
2. 临时 proposal 批：已记录 30 天候选，本体继续不提交。
3. 项目目录批：只在项目进入 closeout 或 archive 前逐个处理。
4. zip / package 批：统一判断 canonical、duplicate、archive evidence 和 30 天删除候选。

## 当前禁止动作

- 不提交整个 `projects/*`。
- 不删除项目目录。
- 不移动到 `_archives`。
- 不清空 `memory-cache/`。
- 不提交项目 raw / zip / HTML / PNG。
- 不把项目偏好写入长期记忆。
- 不把单个项目经验直接升级为 stable policy。

## 结论

项目产物批已经完成生命周期分区。当前最稳的做法不是继续提交项目文件，而是把剩余未跟踪项目目录作为候选区保留；下一步处理 `memory-cache/` 和 `ai-intel/raw/` 的生命周期记录，继续压低仓库噪音。
