# A4 真实输出复核报告

- 日期：2026-04-29
- 状态：真实输出复核报告，不批准 staging / commit / push
- 范围：B 包、closeout、Codex 开发文档模板、项目偏好缓存边界
- 结论：`ready_for_staging_list_for_selected_subset`
- 原则：长期稳定可靠优先；如无必要，不增 skill / harness

## 1. 总结结论

A4 原始复核发现两个问题：B 包在中文源场景下会退化成通用内容，外部保护版开发文档模板带有金融场景专用 wording。用户已批准按建议修复，本轮已完成修正并重新验证。

当前结论：

- B 包脚本可以进入下一步 staging 清单候选，但必须保留“无确认英文源则失败”和“prototype 需要显式 `--include-prototype`”。
- closeout 工具可以进入下一步 staging 清单候选，但必须继续只生成审核材料。
- Codex 内部开发文档模板和外部保护模板可以进入下一步 staging 清单候选。
- 项目偏好缓存仍保持项目内 candidate，不进入稳定主链路。

| A4 子项 | 复核结论 | 推荐动作 |
|---|---|---|
| B 包脚本与 redaction | 修复后通过；无英文源会失败，有英文源可生成 | `ready_for_staging_list` |
| closeout 工具 | 临时输出验证通过，只生成审核材料 | `ready_for_staging_list` |
| Codex 内部开发文档模板 | 内部/外部边界清楚 | `ready_for_staging_list` |
| 外部保护开发文档模板 | 金融专用 wording 已改为通用安全门禁 | `ready_for_staging_list` |
| 项目偏好缓存 | 临时流程验证通过，但应保持项目内候选能力 | `keep_candidate` |

整体建议：下一步可以生成 A4 最终 staging 清单，但只纳入通过复核的稳定子集；不要把 `memory-cache/*`、项目 closeout 产物、B 包 zip 或偏好缓存工具默认稳定化混进去。

## 2. 执行过的真实输出验证

所有真实输出都写入 `/private/tmp`，没有写入 `projects/*`。

### 2.1 编译检查

命令：

```bash
PYTHONPYCACHEPREFIX=/tmp/pycache python3 -m py_compile pm-prd-copilot/scripts/package_b_delivery.py pm-prd-copilot/scripts/closeout_project.py pm-prd-copilot/scripts/manage_preference_cache.py
```

结果：通过。

### 2.2 B 包输出验证

命令：

```bash
python3 pm-prd-copilot/scripts/package_b_delivery.py --base-dir . --project-dir projects/demo-project --output /private/tmp/a4-review-demo/B-after-fix.zip
python3 pm-prd-copilot/scripts/package_b_delivery.py --base-dir . --project-dir projects/fitness-app-mvp --output /private/tmp/a4-review-fitness/B-after-fix.zip
python3 pm-prd-copilot/scripts/package_b_delivery.py --base-dir . --project-dir projects/demo-project --source-file /private/tmp/a4-review-demo/b-source.md --output /private/tmp/a4-review-demo/B-after-fix.zip
python3 pm-prd-copilot/scripts/package_b_delivery.py --base-dir . --project-dir projects/demo-project --source-file /private/tmp/a4-review-demo/b-source.md --include-prototype --output /private/tmp/a4-review-demo/B-after-fix-with-prototype.zip
python3 pm-prd-copilot/scripts/package_b_delivery.py --base-dir . --project-dir projects/fitness-app-mvp --source-file /private/tmp/a4-review-fitness/b-source.md --output /private/tmp/a4-review-fitness/B-after-fix.zip
```

结果：

- `demo-project` 无 `--source-file`：按预期失败，提示需要 confirmed English source。
- `fitness-app-mvp` 无 `--source-file`：按预期失败，提示需要 confirmed English source。
- `demo-project` 带 `--source-file`：生成成功，redaction check passed。
- `fitness-app-mvp` 带 `--source-file`：生成成功，redaction check passed。
- zip 都只写在 `/private/tmp`。

结构观察：

- 默认 B 包只包含 `README.md` 和 `docs/*.md`，不复制 `prototype/*`。
- 显式 `--include-prototype` 后才复制 `prototype/*`。
- `docs/A.md` 使用确认过的英文源，不再退化为 `Project: Product Delivery.`。

仍需注意：

- redaction 主要扫描文本内容，不能识别图片像素里的潜在敏感文字。
- 因此 `--include-prototype` 只能在人工确认图片可外发后使用。

修复结果：

- 已支持显式 `--source-file`。
- 已改为无确认英文源则失败。
- 已改为 prototype 默认不复制，必须显式 `--include-prototype`。
- 已在 regression 中补充上述行为检查。

## 3. Closeout 输出验证

命令：

```bash
python3 pm-prd-copilot/scripts/closeout_project.py --base-dir . --project demo-project --output-dir /private/tmp/a4-review-demo/closeout
python3 pm-prd-copilot/scripts/closeout_project.py --base-dir . --project fitness-app-mvp --output-dir /private/tmp/a4-review-fitness/closeout
```

结果：

- 两个项目都生成了：
  - `manifest.json`
  - `closeout-report.md`
  - `architecture-feedback.md`
  - `cleanup-plan.md`
  - `preference-memory-disposition.md`
- 输出路径均在 `/private/tmp`。
- manifest 显示：
  - `mode: dry_run_report_only`
  - `destructive_actions_enabled: false`
  - `approval_required: true`
  - `archive_before_delete: true`
  - `hard_delete_eligible_after_days: 30`

结论：closeout 工具可以进入下一步 staging 清单候选，但必须继续保持“只生成审核材料，不执行归档、不删除、不清空缓存”。

## 4. Codex 开发文档模板复核

内部版模板：

- 能明确区分产品能力和开发内部机制。
- 明确外部分发时必须改用外部保护模板。
- 包含 PRD、页面说明、页面跳转关系、PRD 原型图层和 AI 条件输入。
- 可作为内部 Codex 开发文档模板候选。

外部保护模板：

- 使用 B 包口径，隐藏内部治理机制。
- 使用英文，适合外部执行包。
- 金融专用门禁已改为通用表达：domain-specific safety, compliance, privacy, and risk-expression limits.

建议：

- 内部版模板可进入 staging 候选。
- 外部保护模板可进入 staging 候选；金融项目再由项目 PRD/开发文档补充专用约束。

## 5. 项目偏好缓存复核

临时验证命令：

```bash
python3 pm-prd-copilot/scripts/manage_preference_cache.py --base-dir /private/tmp/a4-review-cache --project sandbox-project --reason a4-review init
python3 pm-prd-copilot/scripts/manage_preference_cache.py --base-dir /private/tmp/a4-review-cache --project sandbox-project --reason a4-review-archive-alignment archive-clear
```

结果：

- 临时 cache 初始化成功。
- `archive-clear` 先生成 `/private/tmp/a4-review-cache/projects/sandbox-project/closeout/preference-memory-disposition.json`。
- 随后 `current.json` 标记为 `status: cleared`。
- policy 中包含：
  - `cross_project_reuse_allowed: false`
  - `long_term_memory_requires_user_approval: true`
  - `archive_alignment_required: true`
  - `clear_after_project_archive_alignment: true`

结论：

- 偏好缓存机制符合项目内隔离和归档对齐原则。
- 但它会真实写 `memory-cache/` 并改变项目 cache 指针，不能作为默认稳定主链路。
- 推荐保持 `keep_candidate`，仅在具体项目需要偏好连续性时启用。

## 6. 需要你拍板

用户已批准按以下建议执行：

| 决策项 | 已采用方案 | 后续效果 |
|---|---|---|
| B 包中文源被过滤时怎么办 | 失败并要求确认英文源 | 防止自动生成泛化 B 包。 |
| B 包是否默认复制 prototype 图片 | 需要显式 `--include-prototype` | 防止未经确认的图片资产外发。 |
| 外部保护模板是否先修通用 wording | 已修通用 wording | 防止通用模板被金融场景污染。 |
| closeout 工具是否进入下一步 staging 候选 | 进入 | 但仍只能生成审核材料。 |
| 偏好缓存是否进入稳定核心 | 保持项目内 candidate | 防止跨项目偏好污染和长期记忆污染。 |

## 7. 下一步建议

下一步可以做：

```text
A4 最终 Staging 清单
```

清单必须把稳定子集和 candidate 子集分开：B 包脚本、closeout、分发规则、开发文档模板可以列入候选；`memory-cache/*`、项目 closeout 产物、B 包 zip、项目偏好缓存真实数据不得纳入。

## 8. 本轮未执行事项

- 未 staging。
- 未 commit / push / PR。
- 未删除、恢复、移动、归档。
- 未写入 `projects/*`。
- 未生成 repo 内 zip。
- 未清空或迁移真实 `memory-cache/*`。
- 未把 A4 转 stable。
- 未新增 skill / harness。
