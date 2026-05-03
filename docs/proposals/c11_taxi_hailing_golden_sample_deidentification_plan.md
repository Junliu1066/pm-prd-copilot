# C11 打车 PRD Golden Sample 候选脱敏方案

- 日期：2026-05-03
- 状态：proposal，C11a / C11b / C11c 已按用户批准执行；仍不是 stable policy。
- 范围：`projects/taxi-hailing-prd-test` 的 golden sample candidate 处置方案。
- 主线任务：把具体测试项目抽象成可复用的 0-1 普通业务 PRD 结构样例候选，同时避免项目产物、测试目的、绝对路径和单项目经验污染稳定架构。

## 1. 结论

`projects/taxi-hailing-prd-test/02_prd.final.md` 有较高结构价值，但不能直接作为稳定 golden sample。

推荐做法：

1. 先保留它作为项目证据和候选样例来源。
2. 生成一份通用脱敏版样例，放入 `pm-prd-copilot/evals/golden_cases/` 的候选目录或后续样例组合中。
3. 更新 regression，使它检查脱敏样例或候选样例组合，而不是直接依赖 `projects/taxi-hailing-prd-test/`。
4. 本轮不提交 `projects/taxi-hailing-prd-test/`，不把单个项目升级为 stable golden sample。

这样做能解决两个问题：

- 保留这份 PRD 暴露出来的结构价值。
- 避免稳定检查依赖未跟踪项目目录，导致干净 checkout 下 regression 不可靠。

## 1.1 本轮执行结果

已完成：

| 批次 | 结果 |
|---|---|
| C11a 脱敏样例草案 | 已生成通用 `0-1 本地服务履约平台 MVP` 样例。 |
| C11b 样例入候选库 | 已新增 `pm-prd-copilot/evals/golden_cases/zero_to_one_service_prd/`。 |
| C11c Regression 依赖修复 | 已把 `run_regression.py` 从未跟踪项目目录依赖切到脱敏样例路径。 |

未完成：

| 批次 | 当前状态 |
|---|---|
| C11d Golden sample portfolio | 未做。仍需后续收集更多 PRD 样例，不能用单个样例代表所有 0-1 PRD。 |

## 2. 当前证据

| 文件 | 当前价值 | 风险 |
|---|---|---|
| `projects/taxi-hailing-prd-test/00_raw_input.md` | 原始输入证据，能追溯测试来源。 | 项目特定，不应进入稳定样例。 |
| `projects/taxi-hailing-prd-test/00_test_review_notes.md` | 记录旧生成链路暴露的问题。 | 是测试过程材料，不应直接变规则。 |
| `projects/taxi-hailing-prd-test/02_prd.generated.md` | 旧问题样本，可用于对比退化。 | 含测试目的误入产品目标、泛化图表、非 AI 项目 AI 选型等问题。 |
| `projects/taxi-hailing-prd-test/02_prd.final.md` | 人工修正后的高价值结构候选。 | 含具体项目名、绝对路径、测试项目上下文，不能直接稳定入库。 |
| `projects/taxi-hailing-prd-test/closeout/architecture-feedback.md` | 架构反哺候选。 | 未经逐条批准，不应直接改 prompt / template / regression。 |

## 3. 已验证的结构价值

这份 final PRD 值得提炼的不是“打车业务本身”，而是 0-1 普通业务 PRD 的结构底线：

| 结构能力 | 价值 |
|---|---|
| 摘要后放产品总览图 | 让读者快速理解产品全貌。 |
| 用户 / JTBD 和使用场景分开 | 避免只堆功能，不说明用户任务。 |
| 范围定义后放 MVP 范围地图 | 把 MVP、V1、Later 和不做事项压清楚。 |
| 方案章节内放泳道图、流程图、状态流转图 | 图表贴近对应内容，不再集中堆“PRD 可视化层”。 |
| 页面说明 + 页面跳转关系 + 原型图层 | 支撑后续 UI、原型确认和 Codex 开发文档。 |
| 非 AI 项目不写 AI 模型选型 | 避免普通业务 PRD 被 AI 章节污染。 |
| 目标 / 非目标和成功指标后置 | 先讲清用户、范围、方案，再收束目标和指标。 |
| 风险控制闭环和开放问题显式化 | 把上线风险、权限边界和未决问题暴露出来。 |

## 4. 不能直接入库的原因

| 问题 | 影响 |
|---|---|
| 项目目录未跟踪 | 当前 regression 如果直接依赖 `projects/taxi-hailing-prd-test/02_prd.final.md`，干净 checkout 可能缺文件。 |
| 项目名称和路径暴露 | 文档内有具体项目路径和测试项目上下文，不适合作为通用样例。 |
| 单项目过拟合 | 打车是出行履约场景，不能代表所有 0-1 普通业务 PRD。 |
| 没有样例组合 | 稳定 golden sample 应至少覆盖普通业务、AI-heavy、复杂 B2B / 后台类等不同项目。 |
| 仍需用户批准 | 样例进入 `golden_cases` 后会影响 regression，属于稳定检查口径变化。 |

## 5. 推荐脱敏口径

### 5.1 保留

- PRD 章节结构。
- 图表放对应章节的布局方式。
- 页面说明、页面跳转关系、原型图层。
- 非 AI 项目不写 AI 模型选型的判断。
- MVP 范围地图、用户故事地图、权限矩阵、风险闭环等结构。
- PNG / HTML 后置的边界说明。

### 5.2 替换

| 原内容 | 替换方式 |
|---|---|
| `城市即时打车平台 MVP` | `0-1 本地服务履约平台 MVP 样例` 或 `0-1 普通业务 MVP 样例` |
| `乘客 / 司机` | `消费者 / 服务提供者`，必要时保留为出行领域示例但标明只是领域样例。 |
| 具体项目路径 | 删除或改成相对样例路径。 |
| 测试输入、测试目的、修复记录 | 放到样例说明，不进入 PRD 正文。 |
| 具体城市、价格、运营假设 | 改成通用占位或说明为示例假设。 |

### 5.3 删除

- 绝对路径。
- 项目 ID。
- 测试目的和本轮治理修复说明。
- 未经确认的项目偏好。
- closeout 过程材料。
- 任何可能让模型把单个测试项目当长期规则的措辞。

## 6. 推荐文件结构

后续如果你批准，可新增：

```text
pm-prd-copilot/evals/golden_cases/zero_to_one_service_prd/
  README.md
  input.md
  expected_prd.md
  acceptance.md
```

含义：

| 文件 | 作用 |
|---|---|
| `README.md` | 说明样例来源、为什么重要、适用范围和不适用范围。 |
| `input.md` | 脱敏后的 0-1 普通业务输入，不包含测试目的。 |
| `expected_prd.md` | 脱敏后的结构样例，不直接复用项目原文。 |
| `acceptance.md` | 写清必须检查的结构点：页面说明、页面跳转关系、原型图层、非 AI 不写 AI 选型等。 |

## 7. Regression 修复建议

当前 `run_regression.py` 已经检查 `projects/taxi-hailing-prd-test/02_prd.final.md`。这会带来干净 checkout 风险。

建议后续改成：

1. 如果 `pm-prd-copilot/evals/golden_cases/zero_to_one_service_prd/expected_prd.md` 存在，检查该脱敏样例。
2. 不再把未跟踪项目目录作为稳定 regression 的硬依赖。
3. 项目原文只作为项目证据，不作为稳定检查输入。

这样做的效果：

- 稳定检查可复现。
- 项目产物不需要混入 stable commit。
- 后续可以逐步扩展成 golden sample portfolio。

## 8. 执行批次状态

### C11a：脱敏样例生成方案

状态：已完成。

- 已输出脱敏样例草案。
- 未提交项目产物。
- 等你检查样例是否过拟合、是否可读、是否适合作为候选样例。

### C11b：样例入候选库

状态：已完成。

- 已新增 `pm-prd-copilot/evals/golden_cases/zero_to_one_service_prd/`。
- 未提交 `projects/taxi-hailing-prd-test/`。
- 仍标记为 candidate，不等于 stable portfolio。

### C11c：Regression 依赖修复

状态：已完成，待验证结果随本轮汇报同步。

- 已修改 `run_regression.py`，检查脱敏样例路径。
- 已移除对未跟踪项目目录的硬依赖。
- 已增加防污染断言：不得出现项目 ID、测试项目名称和绝对路径。

### C11d：Golden sample portfolio

- 等后续至少再有 2-3 个不同类型 PRD 后，再决定是否形成正式 portfolio。
- 单个打车样例不直接代表所有 0-1 PRD。

## 9. 需要你后续拍板

| 决策 | 我的建议 | 效果 |
|---|---|---|
| 是否接受本轮脱敏样例候选 | 建议先接受为 candidate | 能让 regression 有可复现结构基线，但不把它升级为完整 portfolio。 |
| 是否后续继续扩展更多 PRD 样例 | 建议继续 | 多项目样例组合更稳，避免单个本地服务样例过拟合。 |
| 是否提交 `projects/taxi-hailing-prd-test/` | 不提交 | 保持项目产物和稳定样例分离。 |
| 是否把打车样例转 stable golden sample | 暂不转 | 先作为 portfolio 候选，等多项目证据。 |

## 10. 当前不做

- 不提交 `projects/taxi-hailing-prd-test/`。
- 不新增 stable policy。
- 不删除、归档项目文件。
- 不写长期记忆。
- 不新增 skill、harness、workflow、plugin 或 automation。
- 不把单个样例升级为完整 golden sample portfolio。
