# Skill 文件夹上传与源码加密方案

- 文档状态: 产品方案 Ready / 一期开发范围待确认 / 上线前业务参数待补齐
- 生成日期: 2026-05-08
- 适用读者: 产品经理、研发负责人、后端、平台工程师、安全负责人、Skill 管理员
- 文档用途: 单独说明“Skill 是一个一个文件夹”时，如何上传、版本化、加密存储、授权调用和防源码泄露
- 关联文档:
  - PRD: [01_product_document.md](/Users/liujun/Desktop/产品经理skill/projects/ai-collaboration-efficiency-platform/01_product_document.md)
  - 开发文档: [02_development_document.md](/Users/liujun/Desktop/产品经理skill/projects/ai-collaboration-efficiency-platform/02_development_document.md)
  - 原型图: [06_prototype_wireframes.md](/Users/liujun/Desktop/产品经理skill/projects/ai-collaboration-efficiency-platform/06_prototype_wireframes.md)

---

## 1. 核心结论

本平台的 Skill 不是单条配置，而是一个文件夹形式的能力资产。本方案的核心不是复杂加密，而是“简单加密 + 严格权限 + 版本不可覆盖 + 审计追溯”:

```text
Skill 文件夹
-> 打包
-> 校验
-> 生成 manifest
-> 加密成 SkillSourcePackage
-> 存储密文包
-> SkillVersion 绑定密文包
-> 授权用户只能调用
-> 运行时临时解密执行
-> 执行后清理临时源码
-> 全程审计
```

调用方可以拿到运行结果，但不能拿到 Skill 源码。这里的源码包括:

- Prompt 源文件。
- Workflow / DAG 编排文件。
- Tool adapter / 工具适配代码。
- 执行脚本。
- 私有规则配置。
- 测试集答案、评分规则、Few-shot 样例。
- 内部依赖说明和私有知识引用。

`call` 授权只代表“可以运行这个 Skill”，不代表“可以查看、下载、复制这个 Skill 文件夹”。源码查看和源码导出必须使用独立授权: `source_read`、`source_export`。

已确认落地口径:

- 加密只做简单包级防护，推荐服务端 AES-GCM；密钥从环境变量或部署 Secret 注入。
- 开发重点是权限管理和版本管理: `call` 不等于源码查看，`manage` 不等于源码导出，源码包版本不可覆盖，SkillVersion 必须绑定明确的 SourcePackage 版本。
- 一期必须实现 Skill 源码包加密上传、加密存储、运行时解密执行和执行后清理。
- 一期后端采用 FastAPI + Celery Worker；企业 KMS / 云 KMS / Vault 不作为本阶段重点，只作为后续可替换增强。
- 一期 Skill 执行模式固定为 `single`，不做并发执行；`parallel` / `dag`、ExecutionPlan、SkillSubCall 和 Reducer 放到二期。
- 一期不开放源码导出；`source_read` 只允许 `skill_admin` / `system_admin` 查看脱敏结构摘要，`source_export` 二期再做二次审批。

## 2. Skill 文件夹建议结构

建议每个 Skill 以一个文件夹为最小上传单位:

```text
skill-folder/
  SKILL.md
  manifest.json
  prompts/
    system.md
    task.md
    examples.json
  workflow/
    dag.json
    reducer.json
  tools/
    adapter.ts
    schema.json
  tests/
    dataset.jsonl
    expected.jsonl
  assets/
    template.docx
    reference.md
  README.md
```

最低要求:

- 必须有 `manifest.json` 或由平台上传时自动生成 manifest。
- 必须有入口声明，例如 `entrypoint`、`runtime`、`allowed_tools`。
- 必须声明 Skill 名称、版本、负责人、适用任务类型、风险等级、输入输出 Schema。
- 源码包中不得包含 `.git/`、本地密钥、个人凭据、临时文件、明文生产 API Key。

建议排除:

```text
.git/
.DS_Store
node_modules/
__pycache__/
.env
.env.*
*.pem
*.key
*.log
tmp/
dist/
build/
```

## 3. 上传方式

### 3.1 管理端 Web 上传

适合 Skill 管理员手工发布。

Web 端可以支持两种入口:

| 入口 | 说明 | 推荐程度 |
|---|---|---|
| 上传 zip / skillpkg | 管理员先把 Skill 文件夹打包，再上传单个文件 | 推荐，最稳定 |
| 选择文件夹 | 页面用目录选择能力读取整个文件夹，再由前端或后端打包 | 可选，体验更好但要处理浏览器兼容 |

无论入口是哪一种，平台内部都统一转成标准源码包:

```text
folder tree
-> normalize path
-> remove excluded files
-> build zip / skillpkg
-> calculate hash
-> validate manifest
-> encrypt SkillSourcePackage
```

流程:

```text
选择 Skill
-> 上传 skill-folder.zip 或选择 skill-folder/
-> 平台解压到临时隔离区
-> 校验结构和敏感文件
-> 生成 manifest 和 hash
-> 管理员确认版本说明
-> 平台加密源码包
-> 生成 SkillSourcePackage
-> 创建 SkillVersion candidate
-> 进入测试 / 评审 / 发布
```

页面字段:

| 字段 | 说明 |
|---|---|
| Skill | 绑定已有 Skill 或新建 Skill |
| 版本号 | 例如 `v2.3.1` |
| 源码包 | 上传 zip |
| 变更说明 | 本次修改了什么 |
| 风险等级 | P0 / P1 / P2 / Low |
| 执行模式 | 一期固定 single；二期支持 parallel / dag |
| 最大并发 | 二期并发 Skill 才需要 |
| 失败策略 | 二期并发 Skill 才需要: fail_fast / best_effort / require_all / quorum |
| 是否允许源码查看 | 默认否 |
| 是否允许源码导出 | 默认否，需审批 |

### 3.2 CLI / CI 上传

适合工程团队从 Git 或内部制品流水线上传。

推荐命令形态:

```bash
skillctl package ./skills/monthly-report \
  --skill-id sk_001 \
  --version v2.3.1 \
  --out ./dist/monthly-report-v2.3.1.skillpkg

skillctl upload ./dist/monthly-report-v2.3.1.skillpkg \
  --env prod \
  --change-note "优化月度经营分析结构和 reducer"
```

CLI 必须做:

- 本地结构校验。
- 敏感文件扫描。
- manifest 生成或校验。
- 包 hash 计算。
- 上传到平台临时区。
- 平台侧二次校验和加密。

不建议 CLI 在本地完成最终加密。最终加密应由平台服务端或受控 CI 完成，避免密钥散落在开发者机器上；是否接入企业 KMS 属于后续增强，不影响本阶段方案。

### 3.3 API 上传

一期可先实现单接口 `POST /api/admin/skill-source-packages`，接收 zip / skillpkg 或上传会话引用并完成校验、加密、入库。大文件和 CI 场景推荐二期拆成三步，避免大文件和审批混在一个接口里:

```text
POST /api/admin/skill-source-packages/upload-session
PUT  /upload/{session_id}
POST /api/admin/skill-source-packages/finalize
```

`POST /api/admin/skill-source-packages/upload-session`:

```json
{
  "skill_id": "sk_001",
  "version_code": "v2.3.1",
  "package_name": "monthly-report-v2.3.1.zip",
  "package_size": 248000,
  "package_sha256": "sha256:...",
  "change_note": "优化月度经营分析结构和 reducer"
}
```

`POST /api/admin/skill-source-packages/finalize`:

```json
{
  "session_id": "ups_001",
  "skill_id": "sk_001",
  "version_code": "v2.3.1",
  "manifest": {
    "entrypoint": "main.run",
    "runtime": "python3.11",
    "execution_mode": "single",
    "input_schema": {
      "required": ["business_scenario", "input_material", "expected_output"]
    },
    "output_schema": {
      "required": ["summary", "findings", "recommendations"]
    }
  },
  "reason": "发布月度经营分析 Skill v2.3.1"
}
```

响应:

```json
{
  "data": {
    "source_package_id": "spkg_001",
    "skill_id": "sk_001",
    "version_code": "v2.3.1",
    "package_hash": "sha256:...",
    "encrypted": true,
    "status": "active",
    "source_visibility": "runtime_only"
  },
  "error": null
}
```

## 4. 加密存储方案

### 4.1 包级加密

Skill 文件夹上传后，平台不直接存明文 zip。平台应生成 `SkillSourcePackage`:

| 字段 | 说明 |
|---|---|
| `id` | 源码包 ID |
| `skill_id` | 所属 Skill |
| `version_code` | 源码包版本 |
| `encrypted_package_ref` | 对象存储中的密文包地址 |
| `package_hash` | 明文包 hash，用于完整性校验 |
| `encrypted_hash` | 密文包 hash，用于存储校验 |
| `key_ref_id` | EncryptedSecret / key_version 引用 |
| `manifest` | 脱敏 manifest |
| `status` | draft / active / revoked / archived |

简单加密建议:

```text
服务端读取部署 Secret 或环境变量中的主密钥
使用 AES-GCM 加密源码包
每个包使用随机 nonce / iv
数据库保存 key_version、nonce / iv、密文包引用和 hash
对象存储只保存密文包
```

本阶段不要求 envelope encryption。可落地流程:

```text
source.zip
-> read package encryption key from deployment secret
-> encrypted_source_blob = AES-GCM.encrypt(source.zip, key, nonce)
-> store encrypted_source_blob in object storage
-> store key_version / nonce / hash / encrypted_package_ref in metadata
```

### 4.2 运行时解密

调用 Skill 时不把源码包发给调用方，而是在服务端运行时解密:

```text
SkillCall 创建
-> 校验 call 授权和风险
-> Worker 获取 SkillVersion.source_package_id
-> Worker 读取部署 Secret 对应 key_version
-> Worker 拉取 encrypted_source_blob
-> Worker 在隔离临时目录解密
-> 执行 entrypoint
-> 生成 TaskResult / UsageMeterRecord
-> 清理临时目录和内存引用
-> 写审计
```

运行时要求:

- 解密只能发生在 Worker / 沙箱 / 容器中。
- 临时目录必须有生命周期，执行后清理。
- 重点校验调用者权限、SkillVersion 绑定的 source_package_id、源码包状态和版本号。
- 日志不得打印源码文件内容。
- TaskResult 不保存 Prompt 源、Workflow DAG 或工具代码。
- 报表、看板、计量接口不返回源码。
- 运行失败也要清理临时目录。

### 4.3 权限边界

权限必须拆开:

| 权限 | 能做什么 | 不能做什么 |
|---|---|---|
| `call` | 调用 Skill，得到运行结果 | 看源码、下载源码、复制源码 |
| `read` | 看 Skill 说明、版本摘要、指标 | 看源码 |
| `source_read` | 查看脱敏源码摘要或受控源码预览 | 下载源码包 |
| `source_export` | 导出源码包 | 绕过审批、长期链接下载 |
| `manage` | 管理 Skill 配置和版本 | 自动拥有源码导出 |
| `system_admin` | 系统级管理 | 仍需审计和二次确认 |

关键规则:

- `call` 不等于 `source_read`。
- `manage` 不等于 `source_export`。
- 源码导出必须二次审批、短期链接、单次下载、全量审计。
- 外部客户最多拿到 license 和调用结果，不拿源码包。

### 4.4 版本管理边界

版本管理是本方案的开发重点:

| 规则 | 说明 |
|---|---|
| 源码包不可覆盖 | 已绑定 SkillVersion 或状态为 active 的 SkillSourcePackage 不能原地替换 |
| 新源码新版本 | 任意源码变化都必须创建新的 `version_code` 和新的 `package_hash` |
| 调用绑定快照 | SkillCall 必须保存 `skill_id`、`skill_version_id`、`source_package_id`、`source_package_version` 和 `package_hash` |
| 撤销不删历史 | SourcePackage revoked 后不允许新调用，但历史 SkillCall 仍可解释 |
| 权限按版本判断 | `call` 授权应校验 Skill / SkillVersion / SourcePackage 状态，不能只看 Skill 名称 |
| 审计按版本记录 | 上传、绑定、撤销、运行时解密、查看摘要、导出申请都要写版本号和 hash |

## 5. 二期并发 Skill 的上传差异

一期不启用并发执行。如果二期 Skill 支持多线程 / 多 Worker 并发，文件夹里需要额外声明:

```json
{
  "execution_mode": "parallel",
  "parallel_policy": {
    "max_parallelism": 6,
    "timeout_ms": 180000,
    "retry": {"max_attempts": 2},
    "failure_policy": "best_effort",
    "budget_limit": {
      "max_total_tokens": 200000,
      "max_tool_calls": 30,
      "max_amount_cny": 20
    }
  },
  "reducer_policy": {
    "reducer_type": "structured_merge",
    "conflict_strategy": "require_evidence",
    "require_final_risk_check": true
  }
}
```

并发执行时:

```text
父级 SkillCall 继承 call 授权
-> ExecutionPlan 读取 encrypted SkillSourcePackage
-> 多个 SkillSubCall 在服务端并发执行
-> Reducer 汇总
-> 最终风险检查
-> TaskResult 输出给用户
```

注意:

- SkillSubCall 不能把源码返回给用户。
- 子任务输出不能绕过 Reducer。
- 并发数不能由员工随意提高。
- 每个子任务要单独计量 token、工具调用、耗时和失败原因。

## 6. 安全检查

上传时必须做:

| 检查 | 处理 |
|---|---|
| 文件结构校验 | 缺 manifest、entrypoint、schema 时拒绝 |
| 敏感文件扫描 | 发现 `.env`、私钥、token 时拒绝或要求删除 |
| 文件大小限制 | 超限拒绝或走大文件审批 |
| 文件类型限制 | 禁止可疑二进制或未声明运行时 |
| 依赖检查 | 未锁版本依赖给出风险提示 |
| 风险等级检查 | P0/P1 Skill 必须发布评审 |
| hash 校验 | 上传前后 hash 不一致则拒绝 |
| 恶意代码扫描 | 高风险脚本进入人工安全复核 |

## 7. 审计日志

必须写审计:

- 创建上传会话。
- 上传完成。
- 校验失败。
- 加密成功或失败。
- SkillSourcePackage 创建。
- SkillVersion 绑定源码包。
- Runtime 解密执行。
- Runtime 解密失败。
- 源码查看。
- 源码导出申请。
- 源码导出审批。
- 源码下载。
- 源码包吊销。

审计字段:

| 字段 | 说明 |
|---|---|
| actor_id | 操作人 |
| action | 操作类型 |
| target_type | skill_source_package / skill_version / skill_call |
| target_id | 目标 ID |
| package_hash | 包 hash |
| key_ref_id | 密钥引用 |
| ip | 操作 IP |
| reason | 操作原因 |
| approval_ticket | 审批单 |
| created_at | 时间 |

审计日志不能写源码明文。

## 8. 推荐落地分期

### 一期

目标: 先保证源码不泄露。

- Web 上传 zip。
- 平台校验结构。
- 平台加密 SkillSourcePackage。
- SkillVersion 绑定源码包。
- call 授权运行。
- 不开放源码导出。
- 执行模式固定为 single。
- 运行时临时解密执行和清理。
- 审计日志。

### 二期

目标: 支持工程化发布和并发 Skill。

- CLI / CI 上传。
- source_read / source_export 权限。
- 源码导出审批。
- ExecutionPlan / SkillSubCall / Reducer。
- 并发计量和成本归集。

### 三期

目标: 强化企业级安全。

- 可选升级企业 KMS / Vault 和多租户密钥隔离。
- 源码包签名。
- 沙箱运行。
- 恶意代码扫描。
- DLP 检测。
- 水印化源码导出。
- 跨环境迁移审批。

## 9. 开发验收标准

- 上传 Skill 文件夹后，平台只保存密文包，不保存长期明文源码。
- 员工和外部调用方可以运行 Skill，但不能查看、下载或复制源码。
- `call`、`source_read`、`source_export` 权限边界清晰。
- 普通 API、看板、报表、计量接口不返回源码明文。
- 运行时解密在隔离目录完成，执行后清理。
- 一期源码查看只返回脱敏摘要并写审计；二期源码导出必须审批、短期链接、单次下载。
- 二期并发 Skill 的子任务也不能泄露源码。
- SkillSourcePackage 可以按版本追溯、吊销和回滚。
