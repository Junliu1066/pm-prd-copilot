# 合并审核清单

- 文档状态：Draft / SDD 合并门禁
- 适用对象：集成负责人、Codex 主线程、PR 审核者
- 最后更新时间：2026-05-10

---

## 1. 合并前必查

每个 Codex 分线程进入合并前，必须逐项检查：

```text
Branch:
Task ID:
Thread ID:
Reviewer:
Review Date:
```

| 检查项 | 结果 | 备注 |
|---|---|---|
| 已读取 `AGENTS.md` | pass / fail |  |
| 已填写 Task Brief | pass / fail |  |
| Task Brief allowed paths 与实际 diff 一致 | pass / fail |  |
| 未修改 forbidden paths | pass / fail |  |
| locked paths 已获 owner 授权 | pass / fail / n/a |  |
| 契约变更已走 CCR | pass / fail / n/a |  |
| API 文档与实现一致 | pass / fail / n/a |  |
| 数据库 schema 与 migration 一致 | pass / fail / n/a |  |
| 权限、幂等、审计、错误码完整 | pass / fail / n/a |  |
| 积分流水不可重复、不可提现、不可收益化表达 | pass / fail / n/a |  |
| 量化能力只保留 `research_only` / `simulation_only` | pass / fail / n/a |  |
| AI 输出有风险提示、来源、置信度和 fallback | pass / fail / n/a |  |
| 未新增 C 端高风险能力 | pass / fail |  |
| `make check-all` 通过 | pass / fail |  |
| `THREAD=<branch> make check-boundary` 通过 | pass / fail |  |
| 后端 / 前端 / 原型专项命令通过 | pass / fail / n/a |  |
| 交付摘要完整 | pass / fail |  |
| `automation/thread_registry.md` 状态已更新或有更新请求 | pass / fail |  |

---

## 2. 必跑命令

项目级：

```bash
make check-all
THREAD=<branch> make check-boundary
```

后端工程存在时：

```bash
cd backend
./mvnw test
```

Web 工程存在时：

```bash
cd web
npm run lint
npm run build
```

后台工程存在时：

```bash
cd admin
npm run lint
npm run build
```

---

## 3. 退回条件

命中以下任一条件，不能合并：

- 修改范围超出 Task Brief。
- 修改 forbidden paths。
- 未经授权修改 locked paths。
- API、数据库、积分、量化模式或合规边界发生隐性漂移。
- 为了通过检查删除或放宽门禁。
- `make check-all` 失败。
- 当前线程无法说明测试失败原因、替代检查和残余风险。

---

## 4. 合并摘要模板

```text
合并结论: approved / changes_requested / rejected

主要变更:

验证结果:
- make check-all:
- THREAD=<branch> make check-boundary:
- 其他:

契约变更:

文件边界:

残余风险:

后续线程:
```
