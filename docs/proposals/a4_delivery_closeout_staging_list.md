# A4 交付边界最终 Staging 清单

- 日期：2026-04-29
- 状态：最终 staging 清单，不批准 staging / commit / push
- 输入材料：`docs/proposals/a4_delivery_closeout_real_output_review.md`
- 审查结论：`ready_for_staging_list_for_selected_subset`
- 执行边界：本文件只用于用户拍板；真正 staging 必须再次获得明确批准

## 1. A4 提交意图

A4 的目标是稳定交付边界，而不是把所有交付相关能力一次性转 stable。

本批次只覆盖已经通过真实输出复核的稳定子集：

- B 执行包打包器和 redaction 边界。
- closeout 报告生成器。
- Codex 内部开发文档模板和 B 执行口径模板。
- 分发、redaction、开发文档和内部治理保护规则。
- A4 相关 regression 覆盖。

本批次不稳定项目偏好缓存，不提交项目产物，不提交 B 包 zip。

## 2. 允许进入 A4 Staging 的精确文件

未来如果用户批准 A4 staging，只允许暂存以下 12 个文件。

| 序号 | 文件 | 归属 | 纳入原因 |
|---:|---|---|---|
| 1 | `pm-prd-copilot/scripts/package_b_delivery.py` | B package | 通用 B 执行包生成；无确认英文源则失败；prototype 必须显式 `--include-prototype`。 |
| 2 | `pm-prd-copilot/scripts/closeout_project.py` | Closeout | 只生成归档前审核材料，不执行归档、删除或清空缓存。 |
| 3 | `pm-prd-copilot/scripts/run_regression.py` | Regression | 锁住 B 包英文源门禁和 prototype 显式复制行为。 |
| 4 | `pm-prd-copilot/rules/distribution_policy.yaml` | Rules | 机器可读分发策略。 |
| 5 | `pm-prd-copilot/rules/distribution_policy.md` | Rules | 分发策略说明。 |
| 6 | `pm-prd-copilot/rules/redaction_terms.yaml` | Rules | B 包保护词表。 |
| 7 | `pm-prd-copilot/rules/external_redaction_policy.md` | Rules | B 包保护规则。 |
| 8 | `pm-prd-copilot/rules/development_document_policy.md` | Rules | PRD / Codex 开发文档输出边界。 |
| 9 | `pm-prd-copilot/rules/agent_embedding_policy.md` | Rules | `agent.md` 中性嵌入边界。 |
| 10 | `pm-prd-copilot/rules/codex_internal_governance_policy.md` | Rules | 内部版 Codex 开发文档治理嵌入边界。 |
| 11 | `pm-prd-copilot/templates/codex_development_document_template.md` | Template | 内部 Codex 开发文档模板。 |
| 12 | `pm-prd-copilot/templates/external_protected_development_document_template.md` | Template | B 执行口径外部保护模板，已去除金融专用门禁。 |

## 3. 明确不进入 A4 Staging 的文件

以下文件或目录不得混入 A4 staging：

| 路径 / 范围 | 处理 |
|---|---|
| `pm-prd-copilot/scripts/manage_preference_cache.py` | 保持项目内 candidate，不进入稳定主链路。 |
| `memory-cache/*` | 真实项目偏好缓存，不提交。 |
| `pm-prd-copilot/memory/user_preferences.md` | 长期偏好文件，后续走治理文档 / 长期记忆批次，不混入 A4。 |
| `projects/*/closeout/*` | 项目 closeout 产物，属于项目证据批次。 |
| `projects/**/*.zip`、`projects/_archives/**/*.zip` | B 包、内部包、历史 zip，属于项目/归档候选，不进稳定核心。 |
| `pm-prd-copilot/scripts/package_internal_delivery.py` | 内部打包器候选，未进入本轮复核。 |
| `pm-prd-copilot/scripts/select_ui_style.py`、`pm-prd-copilot/ui-design/*` | UI 风格候选能力，非 A4 稳定子集。 |
| `docs/proposals/*` | 审核材料，不混入 stable core commit。 |
| `plugins/*` | candidate plugin，不转 stable。 |

## 4. 未来精确 Staging 命令

如果用户明确批准 A4 staging，只能使用下面这个精确命令：

```bash
git add pm-prd-copilot/scripts/package_b_delivery.py pm-prd-copilot/scripts/closeout_project.py pm-prd-copilot/scripts/run_regression.py pm-prd-copilot/rules/distribution_policy.yaml pm-prd-copilot/rules/distribution_policy.md pm-prd-copilot/rules/redaction_terms.yaml pm-prd-copilot/rules/external_redaction_policy.md pm-prd-copilot/rules/development_document_policy.md pm-prd-copilot/rules/agent_embedding_policy.md pm-prd-copilot/rules/codex_internal_governance_policy.md pm-prd-copilot/templates/codex_development_document_template.md pm-prd-copilot/templates/external_protected_development_document_template.md
```

禁止使用：

```bash
git add .
git add pm-prd-copilot/scripts
git add pm-prd-copilot/rules
git add pm-prd-copilot/templates
git add docs/proposals
git add projects
git add memory-cache
```

原因：这些宽泛命令会把 candidate 工具、项目产物、B 包 zip、项目偏好缓存或 proposal 文档带进暂存区。

## 5. Staging 后必须核对的结果

A4 staging 后必须立即运行：

```bash
git diff --cached --name-only
```

结果必须严格等于以下 12 个文件：

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

如果多出任何文件，必须停止，不 commit，并只撤销 A4 staged 状态：

```bash
git restore --staged pm-prd-copilot/scripts/package_b_delivery.py pm-prd-copilot/scripts/closeout_project.py pm-prd-copilot/scripts/run_regression.py pm-prd-copilot/rules/distribution_policy.yaml pm-prd-copilot/rules/distribution_policy.md pm-prd-copilot/rules/redaction_terms.yaml pm-prd-copilot/rules/external_redaction_policy.md pm-prd-copilot/rules/development_document_policy.md pm-prd-copilot/rules/agent_embedding_policy.md pm-prd-copilot/rules/codex_internal_governance_policy.md pm-prd-copilot/templates/codex_development_document_template.md pm-prd-copilot/templates/external_protected_development_document_template.md
```

不得使用 `git restore` 恢复工作区内容，除非用户另行批准。

## 6. Staging 前检查命令

真正 staging 前必须先跑：

```bash
PYTHONPYCACHEPREFIX=/tmp/pycache python3 -m py_compile pm-prd-copilot/scripts/package_b_delivery.py pm-prd-copilot/scripts/closeout_project.py pm-prd-copilot/scripts/run_regression.py
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

如果任一检查失败，不进入 staging。

## 7. 本轮未批准事项

本清单不批准：

- `git add`
- commit / push / PR
- 删除、恢复、移动、归档
- 暂存 `docs/proposals/*`
- 暂存项目 closeout 产物
- 暂存 B 包 zip
- 暂存真实 `memory-cache/*`
- 把项目偏好缓存工具转 stable
- 把 candidate plugin 转 stable

## 8. 下一步建议

如果用户认可本清单，下一步再单独申请：

```text
A4 精确 Staging 执行方案
```

该下一步只会按第 4 节命令暂存 12 个 A4 文件，并立即核对暂存区范围；仍不 commit。
