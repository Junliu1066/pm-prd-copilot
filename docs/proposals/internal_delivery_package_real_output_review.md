# 内部完整包真实输出复核报告

- 日期：2026-04-30
- 状态：真实输出复核 + 最小修复报告
- 范围：`pm-prd-copilot/scripts/package_internal_delivery.py`
- 原则：内部包服务可信团队；外部分发继续走 B 包；不写项目目录，不提交生成 zip。

## 结论

内部完整包能力值得保留为候选工具，但原脚本是旧项目专用，不能直接进入稳定使用。

本轮已做最小修复：

- 不再依赖 `交付包目录说明.md`。
- 自动生成内部 `README.md` 和 `MANIFEST.json`。
- 支持当前通用项目结构：PRD、用户故事、风险、埋点、analysis、prototype、delivery、ai、governance、closeout。
- 默认排除 `runs/`、`memory-cache/`、隐藏文件、`__pycache__` 和已有 zip。
- 输出只写到用户指定 zip 路径，本轮复核全部写入 `/private/tmp`。

## 修复前问题

| 问题 | 影响 |
|---|---|
| 强依赖 `交付包目录说明.md` | `demo-project` 和 `fitness-app-mvp` 都无法生成内部包。 |
| 文件名硬编码为旧项目结构 | 当前 0-1 PRD 项目和通用项目目录无法复用。 |
| 默认复制 `prototype` 和 `governance`，但没有 manifest | 包内容不可审计。 |
| 未声明和 B 包外部分发的边界 | 容易把内部包误用于外部交付。 |

## 当前输出效果

| 项目 | 临时输出 | 结果 | 文件数 | 观察 |
|---|---|---:|---:|---|
| `demo-project` | `/private/tmp/internal-delivery-demo.zip` | 通过 | 35 | 包含 PRD、用户故事、风险、埋点、closeout、prototype；不含 runs/cache/zip。 |
| `fitness-app-mvp` | `/private/tmp/internal-delivery-fitness.zip` | 通过 | 38 | 包含 analysis、PRD、prototype、closeout；不含 runs/cache/zip。 |
| `jiaxiaoqian-ai-invest-research` | `/private/tmp/internal-delivery-jiaxiaoqian.zip` | 通过 | 35 | 包含历史完整开发资料和 prototype；不复制项目内已有 zip。 |

## 功能边界

内部包和 B 包分工如下：

| 包类型 | 受众 | 内容 | 语言 | 风险控制 |
|---|---|---|---|---|
| 内部完整包 | 用户自己、可信团队 | 可包含中文 PRD、Codex 开发文档、原型、closeout、内部说明 | 中文或项目原文 | 不能外发；外发前必须重走 redaction。 |
| B 执行包 | 外部执行方 | 英文短文件名、执行要求、验收边界 | 英文 | 隐藏内部治理机制，经过 redaction。 |

本轮修复不会改变 B 包逻辑，也不会把内部包变成默认外部分发包。

## 回归保护

已在 `run_regression.py` 增加内部包检查：

- 能用 `demo-project` 生成临时内部包。
- zip 必须包含 `README.md`、`MANIFEST.json` 和 PRD 文件。
- 默认不能包含 `runs/`、`memory-cache/` 或已有 zip。
- manifest 必须声明 `package_type: trusted_internal`。
- 默认 `include_runs` 必须为 `false`。

## 仍需你拍板

| 拍板项 | 我的建议 | 原因 |
|---|---|---|
| 是否提交内部包脚本和复核报告 | 建议提交 | 已通过三项目真实输出，边界清楚，回归已覆盖。 |
| 是否把内部包能力转 stable | 暂不 | 先作为候选工具，跑更多真实项目后再决定。 |
| 是否允许默认包含 `runs/` | 不允许 | run 输出噪音大，可能含临时报告；需要时用显式 `--include-runs`。 |
| 是否允许内部包外发 | 不允许 | 外发必须走 B 包和 redaction。 |

## 本轮未做

- 未提交任何生成 zip。
- 未写入 `projects/*`。
- 未提交 `memory-cache/`。
- 未修改 B 包脚本。
- 未改变 PRD 主链路。
- 未把内部包能力转 stable。
