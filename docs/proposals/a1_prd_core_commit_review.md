# A1 PRD 主链路 Commit 审查

- 日期：2026-04-29
- 状态：commit 前审查材料，不批准 commit / push / PR
- 输入依据：`docs/proposals/a1_prd_core_staging_review.md`、`docs/proposals/a1_prd_core_staging_list.md`
- 当前 staged 范围：严格等于 A1 8 个文件
- 重要边界：本文件不进入本次 A1 commit，除非用户另行批准文档批次

## 1. Commit 目标

本次 A1 commit 的目标是稳定 PRD 主链路输出合同：

- 固定 PRD 页面说明、页面跳转关系、原型图层。
- 图表按章节输出，不集中堆“PRD 可视化层”。
- 非 AI 项目不输出 AI 模型选型。
- PNG / HTML / 完整原型属于用户确认后的项目产物，不进入 PRD 默认交付。
- 模板、schema、prompt、pipeline、skill 指令保持一致。

## 2. 当前 staged 文件范围

当前 staged 文件必须严格等于：

```text
pm-prd-copilot/SKILL.md
pm-prd-copilot/references/output_style_guide.md
pm-prd-copilot/references/prd_pm_2026_playbook.md
pm-prd-copilot/scripts/pipeline_common.py
pm-prd-copilot/scripts/prompt_builders.py
pm-prd-copilot/scripts/router.py
pm-prd-copilot/templates/prd_template_2026.md
shared/schemas/prd_document.schema.json
```

当前 staged stat：

```text
8 files changed, 837 insertions(+), 123 deletions(-)
```

本次 commit 不得包含：

- `projects/*`
- `plugins/*`
- A2 / A3 / A4 文件
- root 删除项
- PNG / HTML / B 包 / closeout / run outputs
- `docs/proposals/*` 审查材料

## 3. 推荐 Commit Message

推荐 subject：

```text
Stabilize PRD core output contract
```

推荐 body：

```text
- Align PRD skill, template, schema, prompt, and pipeline output rules.
- Require page descriptions, page navigation, and prototype layer in PRDs.
- Keep visual diagrams in their relevant sections instead of a centralized visualization layer.
- Limit AI model selection to projects with AI capabilities.
- Keep PNG, HTML, and full prototypes as post-approval project artifacts.
```

## 4. Commit 前必须再次验证

执行 commit 前必须运行：

```bash
git diff --cached --name-only
git diff --cached --check
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

验收条件：

- `git diff --cached --name-only` 严格等于 A1 8 个文件。
- `git diff --cached --check` 通过。
- `git diff --check` 通过。
- regression 通过。
- harness check-only 通过，且显示 `No project files written`。

## 5. Commit 后验证

如果用户后续明确批准并完成 commit，必须立刻检查：

```bash
git status --short
git show --stat --oneline --name-only HEAD
```

验收条件：

- 最新 commit 只包含 A1 8 个文件。
- 工作区仍保留其他未提交批次，不被误删、误还原或误提交。
- 不自动 push，不自动 PR。

## 6. 回滚策略

如果只是撤销 staged 状态，使用：

```bash
git restore --staged pm-prd-copilot/SKILL.md pm-prd-copilot/references/output_style_guide.md pm-prd-copilot/references/prd_pm_2026_playbook.md pm-prd-copilot/templates/prd_template_2026.md shared/schemas/prd_document.schema.json pm-prd-copilot/scripts/pipeline_common.py pm-prd-copilot/scripts/prompt_builders.py pm-prd-copilot/scripts/router.py
```

如果 commit 后需要撤销，优先使用：

```bash
git revert <commit>
```

禁止默认使用：

```bash
git reset --hard
git checkout -- .
```

任何会恢复、删除或覆盖工作区其他变更的动作，都必须重新获得用户明确批准。

## 7. 下一步拍板点

用户需要确认：

- 是否允许按本审查材料执行 A1 commit。
- 是否接受推荐 commit message：`Stabilize PRD core output contract`。
- 是否继续保持 push / PR 暂缓。

未获得确认前，不执行 commit。
