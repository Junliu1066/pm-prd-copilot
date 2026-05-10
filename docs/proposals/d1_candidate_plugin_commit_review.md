# D1 候选插件 Registry / Source Commit 审查

- 日期：2026-04-30
- 状态：commit 审查材料，不批准 commit
- 范围：candidate plugin marketplace、plugin registry、skill registry、candidate plugin source
- 规则：本文档不批准 commit、push、PR、candidate 转 stable、删除、归档、长期记忆写入或自动化启用。

## 结论

D1 当前暂存范围是正确的，可以进入 commit 前最终审核。

建议 commit，但必须保留这次提交的性质：

- 这是 candidate-only 提交。
- 不是稳定能力转正。
- 不是新增稳定 skill。
- 不是新增稳定 harness。
- 不是允许自动使用 candidate plugin。
- 不是批准 B5c AI 情报区。
- 不是批准 E root/archive 清理。

推荐 commit message：

```text
Add candidate plugin registry and source alignment
```

## 当前暂存范围

当前暂存区包含 97 个文件：

- `.agents/plugins/marketplace.json`
- `registry/plugins.yaml`
- `registry/skills.yaml`
- 5 个新 candidate plugin 源码：
  - `plugins/prd-prototype-suite/`
  - `plugins/preference-memory-suite/`
  - `plugins/quality-evaluation-suite/`
  - `plugins/delivery-planning-suite/`
  - `plugins/ai-solution-planning-suite/`

暂存统计：

```text
97 files changed, 4504 insertions(+), 1 deletion(-)
```

暂存区未包含：

- `plugins/**/__pycache__/*`
- `docs/proposals/*`
- `harness/*`
- `ai-intel/*`
- `projects/*`
- `docs/archive/*`
- `memory-cache/*`
- root 删除项

## 这次提交解决什么问题

之前的问题是：marketplace 已经让 6 个 candidate plugin 可见，但 registry 和源码没有一起对齐，容易形成三类漂移：

| 漂移类型 | 风险 |
|---|---|
| marketplace 可见，但源码未提交 | 稳定仓库显示了不存在的插件目录。 |
| plugin registry 有条目，但 skill registry 未对齐 | 治理层知道插件，但不知道插件拥有的 skill 合同。 |
| skill registry 有合同，但源码未对齐 | 检查能通过表面合同，但实际 skill 不存在。 |

D1 把这三层一起暂存，目标是让 candidate 能力“可见、可追踪、可拆卸、不可被误认为 stable”。

## Candidate 边界

这次提交必须保持以下边界：

- 所有 plugin 都是 `candidate`。
- 所有 plugin 都是 `stable: false` 或 `stable_use_allowed: false`。
- 所有 plugin 都是 `detachable: true`。
- 所有 plugin 都需要用户审核后才能 stable use。
- 所有新增 skill 合同都是 candidate skill。
- candidate plugin 源码可以作为候选能力存在，但不能自动进入主 PRD workflow。

## 包含的能力

| Candidate suite | 作用 | 当前建议 |
|---|---|---|
| `prd-prototype-suite` | 原型参考分析、业务流、低保真原型、HTML 原型候选能力 | 保持 candidate，用户确认后使用。 |
| `preference-memory-suite` | 项目级偏好缓存候选能力 | 保持项目内隔离，不自动进入长期记忆。 |
| `quality-evaluation-suite` | skill 泛化和偏好泄漏审查候选能力 | 可用于候选审查，不等于新增稳定 harness。 |
| `delivery-planning-suite` | 技术范围、路线图、Codex 开发文档、交付治理候选能力 | 保持 detachable，不能自动改产品范围。 |
| `ai-solution-planning-suite` | AI 能力、模型、Prompt、RAG、记忆、AI 架构候选能力 | 仅 AI 项目按需使用，不进入普通 PRD 默认输出。 |

## 不包含的内容

本次 D1 commit 不包含：

- B5c AI 情报区。
- E root/archive 清理。
- 项目 closeout。
- 项目产物。
- 新 harness checker。
- `memory-cache/*`。
- root 删除状态。
- proposal 审查文档。

## Commit 前检查要求

commit 前必须重新运行：

```bash
git diff --cached --name-only
git diff --cached --check
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

额外核对：

```bash
git diff --cached --name-only | rg "__pycache__|docs/proposals|harness/|ai-intel/|projects/|docs/archive|memory-cache|^prd_|skill_suite_overview"
```

预期：无输出。

## 当前已通过检查

- `git diff --cached --check` 通过。
- `git diff --check` 通过。
- D1 marketplace / registry / skill / plugin source 对齐检查通过。
- AI intel / prototype 相关脚本编译通过。
- regression 通过。
- harness check-only 通过，且未写项目文件。
- 非 D1 暂存项搜索无命中。

## 回滚方式

如果只是不想提交 D1：

```bash
git restore --staged .agents/plugins/marketplace.json registry/plugins.yaml registry/skills.yaml plugins/prd-prototype-suite plugins/preference-memory-suite plugins/quality-evaluation-suite plugins/delivery-planning-suite plugins/ai-solution-planning-suite
```

如果 commit 后需要撤销：

```bash
git revert <D1_commit_hash>
```

不要使用 destructive reset。

## 需要你最终批准

| 决策 | 我的建议 | 说明 |
|---|---|---|
| 是否允许 D1 commit | 建议允许 | 当前暂存范围已对齐，能消除 marketplace / registry / source 漂移。 |
| 是否允许 candidate 转 stable | 不允许 | 这不是 D1 目标，仍需单独审批。 |
| 是否把 B5c 一起提交 | 不允许 | AI 情报区写入边界不同，后续单独处理。 |
| 是否把 E root/archive 一起提交 | 不允许 | 删除/归档必须逐项审批。 |

## 建议下一步

明早如果你认可 D1 commit 审查，再单独批准：

```text
批准 D1 commit
```

我再执行 commit，并在 commit 后核对最新提交只包含 D1 范围。

