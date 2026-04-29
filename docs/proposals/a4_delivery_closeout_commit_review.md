# A4 交付边界 Commit 审查

- 日期：2026-04-29
- 状态：commit 前审查材料，不批准 commit / push / PR
- 当前 staged 范围：A4 12 个交付边界稳定子集文件
- 前提：真正 commit 仍需用户明确批准

## 1. 当前 Staged 范围

当前暂存区严格包含以下 12 个文件：

```text
pm-prd-copilot/rules/agent_embedding_policy.md
pm-prd-copilot/rules/codex_internal_governance_policy.md
pm-prd-copilot/rules/development_document_policy.md
pm-prd-copilot/rules/distribution_policy.md
pm-prd-copilot/rules/distribution_policy.yaml
pm-prd-copilot/rules/external_redaction_policy.md
pm-prd-copilot/rules/redaction_terms.yaml
pm-prd-copilot/scripts/closeout_project.py
pm-prd-copilot/scripts/package_b_delivery.py
pm-prd-copilot/scripts/run_regression.py
pm-prd-copilot/templates/codex_development_document_template.md
pm-prd-copilot/templates/external_protected_development_document_template.md
```

当前 staged stat：

```text
12 files changed, 2148 insertions(+)
```

未包含：

- `docs/proposals/*`
- `projects/*`
- `memory-cache/*`
- `pm-prd-copilot/scripts/manage_preference_cache.py`
- `pm-prd-copilot/memory/user_preferences.md`
- `pm-prd-copilot/scripts/package_internal_delivery.py`
- UI 风格候选能力
- `plugins/*`
- B 包 zip / 项目 zip

## 2. 推荐 Commit Message

```text
Stabilize delivery packaging and closeout boundaries
```

推荐 commit body：

```text
- Add supervised B execution package generation with confirmed English source requirements.
- Require explicit prototype inclusion for B packages.
- Add closeout report generation as a supervised, non-destructive pre-archive step.
- Add distribution, redaction, and development-document boundary rules.
- Add internal and protected external Codex development document templates.
- Extend regression coverage for B package source and prototype boundaries.
```

## 3. Commit 前必须再次验证

真正 commit 前必须运行：

```bash
git diff --cached --name-only
git diff --cached --check
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

`git diff --cached --name-only` 必须严格等于第 1 节的 12 个文件。

如果任一检查失败：

- 不 commit。
- 保留 staged 状态，先汇报失败项。
- 只有用户要求撤销 staged 时，才执行 A4 范围的 `git restore --staged`。

## 4. Commit 后核对

如果用户后续明确批准 commit，commit 后必须运行：

```bash
git show --stat --oneline --name-only HEAD
git status --short
```

`git show` 必须显示最新 commit 只包含 A4 12 个交付边界文件。

## 5. 回滚策略

如果 commit 前需要撤销暂存：

```bash
git restore --staged pm-prd-copilot/scripts/package_b_delivery.py pm-prd-copilot/scripts/closeout_project.py pm-prd-copilot/scripts/run_regression.py pm-prd-copilot/rules/distribution_policy.yaml pm-prd-copilot/rules/distribution_policy.md pm-prd-copilot/rules/redaction_terms.yaml pm-prd-copilot/rules/external_redaction_policy.md pm-prd-copilot/rules/development_document_policy.md pm-prd-copilot/rules/agent_embedding_policy.md pm-prd-copilot/rules/codex_internal_governance_policy.md pm-prd-copilot/templates/codex_development_document_template.md pm-prd-copilot/templates/external_protected_development_document_template.md
```

如果 commit 后需要撤销：

```bash
git revert <commit>
```

不使用 `git reset --hard`，不恢复或覆盖用户未批准的其他工作区变更。

## 6. 本轮未批准事项

本审查材料不批准：

- commit
- push / PR
- 删除、恢复、移动、归档
- 暂存 `docs/proposals/*`
- 暂存项目 closeout 产物
- 暂存 B 包 zip
- 暂存真实 `memory-cache/*`
- 把项目偏好缓存工具转 stable
- 把 candidate plugin 转 stable

## 7. 下一步建议

如果用户认可本审查材料，下一步再单独申请：

```text
A4 Commit 执行方案
```

该下一步只会在检查通过后创建一个 A4 独立 commit，仍不 push。
