# 临时生成项目 - 原始输入

- Project ID: temp-generated-project
- 项目性质: 临时生成使用
- 创建日期: 2026-04-30
- 工作区: `/Users/liujun/Desktop/产品经理skill`
- 写入边界: 仅写入 `projects/temp-generated-project/`

## 1. 用户原始要求

用户要求基于当前产品经理 skill 工作区做一个新项目，但不要改动治理架构。

明确边界:

- 先创建独立项目目录 `projects/<项目英文名>/`
- 所有 PRD、原型说明、开发文档、运行产物只写入该项目目录
- 不修改 `pm-prd-copilot/`、`workflow/`、`registry/`、`harness/`、`governance/`、`docs/proposals/`、`memory-cache/` 或根目录文件
- 如果发现需要优化 skill / harness / workflow / 长期偏好，只记录到项目 closeout 或 architecture-feedback
- 输出中文报告

补充说明:

- 用户说明“这只是临时生成使用”

## 2. 本次执行假设

由于用户未指定具体业务主题，本项目采用临时可丢弃主题:

> 临时需求交付包生成器：面向产品经理和小团队，把一段业务输入快速整理成需求澄清、PRD、低保真原型说明和开发交付包。

该主题只用于生成临时项目样例，不代表对稳定 skill、harness、workflow 或长期偏好的修改。

## 3. 已确认事实

- 必须隔离在独立项目目录内。
- 必须避免改动治理架构和稳定目录。
- 项目产物需要覆盖 PRD、原型说明、开发文档、运行产物。
- 本项目是临时生成，不要求进入稳定流程或长期复用。

## 4. 工作假设

- 项目英文名使用 `temp-generated-project`。
- 目标读者为核心团队和后续开发执行者，因此文档保留必要执行细节。
- 原型以静态 HTML 低保真方式交付，可直接用浏览器打开，不启动开发服务器。
- MVP 重点验证“输入需求 -> 澄清问题 -> 生成交付包 -> 检查完整性”的主路径。

## 5. 不改动范围

本项目不触碰以下路径:

- `pm-prd-copilot/`
- `workflow/`
- `registry/`
- `harness/`
- `governance/`
- `docs/proposals/`
- `memory-cache/`
- 根目录文件

如后续发现流程优化建议，只能写入:

- `projects/temp-generated-project/closeout/architecture-feedback.md`

