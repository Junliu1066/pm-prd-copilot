# C10 Jiaxiaoqian AI 投研项目 High-value Closeout 审查

- 日期：2026-05-02
- 状态：项目 closeout 审查材料，不批准归档、删除、移动、staging、commit、push、PR、长期记忆写入或项目产物提交。
- 范围：`projects/jiaxiaoqian-ai-invest-research/` 与 `projects/_archives/delivery-packages/` 中的 Jiaxiaoqian 交付包。
- 主线任务：判断该高价值项目的生命周期状态、项目产物边界、B 包 / 内部包分发边界、金融合规反哺价值，以及后续是否需要进入正式 closeout。

## 结论

`jiaxiaoqian-ai-invest-research` 应保持为 `closeout_candidate_high_value_reviewed`，暂不提交项目、暂不归档、暂不删除。

它是本轮治理修复中最有价值的复杂项目证据之一，原因是：

- 覆盖了 PRD、开发文档、AI 模型选型、原型图、HTML prototype、B 包、内部完整包、外部脱敏包。
- 场景是金融投研，能检验来源引用、风险提示、权限边界、审计日志、AI fallback 和合规审核。
- closeout architecture feedback 已明确提到模板、prompt、workflow、回归测试和数据模型优化候选。

但它不能直接进入稳定核心：

- 体量约 26MB，包含多个 zip 和 prototype 截图。
- closeout 显示 harness / efficiency 没有跑，最近运行 ID 为空。
- 25 个文件被标记为 `manual_review`，说明项目 artifact 注册和归档边界还不够清楚。
- 项目内存在历史旧口径和多版本材料，不能作为稳定模板直接复用。

## 处理后的效果

按本方案处理后，可以达到这些效果：

| 目标 | 效果 |
|---|---|
| 保住高价值经验 | 把金融 AI 项目暴露的问题沉淀为候选，不丢掉。 |
| 不污染稳定核心 | 不提交 26MB 项目产物、不提交 zip、不提交 prototype、不提交项目 PRD。 |
| 保护内外部分发边界 | 内部完整包、外部 B 包、外部脱敏包分开审，不把内部治理暴露给外部。 |
| 防止旧口径回潮 | 历史“原型图 / 线框图”“一句话摘要”等旧口径只作为历史项目证据，不反向改稳定规则。 |
| 为后续瘦身准备 | 明确哪些 zip、截图、HTML、项目 docs 后续可归档候选或 30 天后删除候选。 |

## 当前证据

| 证据 | 结论 |
|---|---|
| `closeout/closeout-report.md` | dry run，未执行清理；扫描 34 个文件，约 26.9MB；harness / efficiency 为 `not_run`。 |
| `closeout/cleanup-plan.md` | 9 个 prototype 文件建议沉淀后归档，25 个文件需要人工审核。 |
| `closeout/architecture-feedback.md` | 有明确架构反哺：权限边界、审计日志、fallback 污染、非导出类项目回归、敏感操作回归。 |
| `closeout/preference-memory-disposition.md` | 未发现项目偏好缓存，不写长期记忆。 |
| `01_prd.md` | 已把图表放入对应章节，AI 模型选型合理存在；但历史标题仍有“一句话摘要”“原型图 / 线框图”。 |
| `10_开发文档.md` | 明确内部版边界，包含内部治理框架，只适合可信内部使用。 |
| `10_B.md` | 外部 B 包使用英文、短文件名和受众边界，适合作为外部分发候选。 |
| `README_B.md` | B 包只暴露执行要求、质量门禁、验收和责任边界。 |
| `交付包目录说明.md` | 已明确内部完整版、B 包、外部分发的差异，但仍包含内部治理启动要求。 |
| `projects/_archives/delivery-packages/*B*` | 已有独立 B 包 zip，文件名短、体量小、内容更适合外部分发。 |
| `projects/_archives/delivery-packages/*external-redacted*` | 有外部脱敏包证据，但仍需确认 redaction 是否完全合格。 |

## 发现的问题

### 1. 项目产物注册不足，导致 25 个文件进入人工审核

closeout 将 PRD、开发文档、B 包、AI 模型选型、MVP 排期、埋点验收、zip 等都标成 `manual_review`。

判断：

- 这不是要马上新增 artifact registry 的理由。
- 但说明真实项目里会产生大量稳定结构的项目产物，而当前 closeout 对这些产物的识别还不够细。

建议：

- 先记录为架构候选，不新增 harness / skill。
- 后续至少再看 2-3 个项目后，再决定是否补 artifact 类型或 closeout 分类规则。

### 2. 内部完整包、B 包、外部脱敏包边界清楚但未形成最终提交策略

当前项目有：

- 项目内完整包：`价小前投研_完整开发交付包.zip`、`jiaxiaoqian_ai_invest_complete_dev_package.zip`。
- 项目内 B 文档：`10_B.md`、`README_B.md`。
- 归档区 B 包：`projects/_archives/delivery-packages/jiaxiaoqian-ai-invest-research-B-20260428.zip`。
- 归档区外部脱敏包：`projects/_archives/delivery-packages/jiaxiaoqian-ai-invest-research-external-redacted-20260428.zip`。

判断：

- B 包策略有价值，但当前不提交 zip。
- 外部包必须先确认不泄露内部治理、私有路径、原始 PDF、source assets、内部多管家命名。
- 中文文件名 zip 在 `unzip -l` 下出现乱码，长期外部分发应优先使用 ASCII / 短文件名包。

建议：

- 后续做“项目交付包归档策略”时，优先保留 B 包和外部脱敏包作为候选，不保留重复完整包。
- 当前不移动、不删除、不提交。

### 3. 金融合规边界是高价值反哺，但不能自动进入 stable

项目已经强调：

- 不输出交易指令、目标价、仓位建议、收益承诺。
- AI 输出必须有来源、置信度、风险提示和 fallback。
- 高风险内容进入审核队列，权限和审计日志要留痕。

判断：

- 这些是 AI 金融投研项目的关键底线。
- 但它们属于行业/项目特定规则，不能直接污染普通 PRD。

建议：

- 后续进入 `architecture-inbox` 候选。
- 如果未来稳定化，应是“金融 / 投研 / 高风险 AI 项目专项规则”，不是所有项目通用规则。

### 4. 历史旧口径只作为项目证据，不回扫修改

项目中仍能看到：

- `## 1. 一句话摘要`
- `### 9.5 原型图 / 线框图`
- 独立图表包 `11_visual_prd_preview.md`

判断：

- 这说明它属于历史项目输出，不是当前 A1 新口径的代表。
- 不能为了美观批量回扫，因为会改动项目历史材料。

建议：

- 当前只记录风险。
- 如果未来要做 golden sample 或外部分发，必须生成脱敏通用版，不直接用这份项目原文。

### 5. AI 模型选型在本项目中是合理存在

这是 AI-heavy 项目，PRD 和独立 `07_ai_model_selection.md` 中出现 AI 模型选型是合理的。

判断：

- 它符合 A1 规则：涉及 AI 的项目才写 AI 模型选型。
- 不是非 AI 项目被 AI 选型污染。

建议：

- 后续作为 AI-heavy 项目模型路由候选样例，但不直接转 stable。

### 6. `projects/_archives` 与项目目录存在重复交付包

`projects/_archives/delivery-packages/` 中已有多个 Jiaxiaoqian zip；项目目录本身也有多个 zip。

判断：

- 这是后续瘦身重点。
- 但 zip 是否可删、哪个是 canonical，需要你后续逐项确认。

建议：

- 当前先标记为“交付包归档策略待定”。
- 后续单独做 zip / package 处置清单，不和 closeout 报告混提交。

## 架构反哺候选

这些只进入候选，不自动改稳定规则：

| 候选 | 价值 | 建议 |
|---|---|---|
| 项目产物 artifact 分类 | 减少 closeout 把 PRD、开发文档、B 包全部打成 manual_review。 | 先收集多项目证据，再决定是否补 registry。 |
| B 包 / 外部脱敏包策略 | 保护内部治理，给外部执行者最小必要信息。 | 后续可稳定化为 package policy，但需真实输出复核。 |
| 金融 AI 合规专项规则 | 防止买卖建议、目标价、仓位建议、收益承诺和无来源结论。 | 作为高风险 AI 项目专项候选，不泛化到所有项目。 |
| fallback 污染回归 | 防止导出 / Excel / 异步任务等旧项目场景污染其它项目。 | 可进入 regression / real-output eval 候选，需你批准。 |
| 权限与审计日志 | 敏感操作必须可追踪。 | 可作为敏感操作 PRD 审查候选，不新增 harness。 |
| zip / package 生命周期 | 防止项目包长期堆积。 | 后续统一归档策略和 30 天删除候选清单。 |

## 需要你后续拍板

| 决策 | 我的建议 | 优势 | 劣势 / 风险 | 选择后的效果 |
|---|---|---|---|---|
| 项目是否进入正式 closeout | 暂缓，保持 `closeout_candidate_high_value_reviewed` | 保留完整上下文，避免过早归档。 | 工作区继续有 26MB 项目产物。 | 最稳，后续可单独处理。 |
| 是否提交项目目录 | 不提交 | 避免项目产物、zip、prototype 污染稳定核心。 | 项目证据暂不进 Git 历史。 | 主仓库更稳。 |
| 是否把它升级为 golden sample | 不直接升级 | 避免金融项目过拟合普通 PRD。 | 暂少一个复杂 AI 样例。 | 后续做脱敏通用版更稳。 |
| 是否提炼金融合规规则 | 后续进入 architecture inbox 候选 | 能沉淀高价值规则。 | 需要人工筛选，不能直接 stable。 | 形成高风险 AI 项目专项候选。 |
| 是否提交 B 包 zip | 暂不提交 | 避免 zip 噪音和未复核泄漏。 | 外部分发证据暂时不入库。 | 后续单独做 package 批次。 |
| 是否保留多个完整 zip | 后续只保留 canonical，重复包进候选清理 | 有利于瘦身。 | 需要逐包比对。 | 最终减少 archive 噪音。 |
| 是否回扫旧 PRD 口径 | 不回扫 | 保留历史证据，避免批量改坏。 | 历史项目里仍能看到旧标题。 | 不影响当前稳定核心。 |
| 是否新增 artifact 类型 | 现在不新增 | 符合“如无必要，不增”。 | closeout 仍会有 manual_review 噪音。 | 等多项目证据后再决定。 |

## 推荐下一步

下一步不建议继续深入 Jiaxiaoqian 业务功能。

建议按治理主线处理：

1. `taxi-hailing-prd-test` golden sample candidate 脱敏方案。
2. 目标是把“0-1 普通业务 PRD 样例”从具体项目中抽象出来，避免再用单个测试项目名称绑定长期规则。
3. Jiaxiaoqian 后续再做 package / zip 处置清单和金融合规专项候选。

## 本轮不做

- 不 staging / commit `projects/jiaxiaoqian-ai-invest-research/*`。
- 不 staging / commit `projects/_archives/*`。
- 不删除 zip。
- 不移动交付包。
- 不归档项目。
- 不写长期记忆。
- 不把项目升级为 golden sample。
- 不修改 skill、harness、workflow、registry、pipeline 或 automation。
