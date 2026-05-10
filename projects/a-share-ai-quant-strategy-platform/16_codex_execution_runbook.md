# Codex 执行手册

- 文档状态：Draft / SDD 执行手册
- 适用对象：Codex 主线程、Codex 子线程、代码集成人
- 最后更新时间：2026-05-10

---

## 1. 执行前检查

进入项目后先运行：

```bash
pwd
ls
make check-all
```

然后读取：

```text
AGENTS.md
13_task_brief_template.md
14_file_boundary_matrix.md
15_failure_handling_protocol.md
12_codex_thread_governance.md
automation/thread_registry.md
18_contract_change_request_template.md
19_merge_review_checklist.md
对应的 tasks/*.brief.md
```

如果 `make check-all` 在开工前失败，先修门禁或报告阻塞，不要开始功能实现。

---

## 2. 开线程 Prompt 模板

```text
你是本项目的 Codex 分线程，分支为 <branch>。

必须先读取：
- AGENTS.md
- 13_task_brief_template.md
- 14_file_boundary_matrix.md
- 15_failure_handling_protocol.md
- 12_codex_thread_governance.md
- 与任务相关的工程文档

任务目标：
<goal>

允许修改：
<allowed paths>

禁止修改：
<forbidden paths>

锁定文件：
<locked paths>

必须运行：
<commands>

交付时必须包含：
完成内容、修改文件、验证结果、未完成事项、风险、需要主线集成处理。
```

---

## 3. 推荐启动顺序

第一批：

```text
codex/p0-docs
codex/p0-spring-api
codex/p0-quant-engine
codex/p0-points
codex/qa-gates
```

第二批：

```text
codex/p0-web-prototype
codex/p0-miniapp-frontend
codex/p0-web-frontend
codex/p0-admin
codex/ai-compliance
```

第三批：

```text
codex/p1-arena
```

前端线程必须等 `06_api_spec.md` 对应接口稳定后再进入正式联调。

---

## 4. 常用命令

项目级静态门禁：

```bash
make check-docs
make check-compliance
make check-contracts
make check-prototype
make check-boundary
make check-all
```

分线程边界检查：

```bash
THREAD=codex/p0-spring-api make check-boundary
THREAD=codex/p0-quant-engine make check-boundary
THREAD=codex/p0-points make check-boundary
THREAD=codex/qa-gates make check-boundary
```

`check-boundary` 需要干净或可比较的 git 基线。启动第一批实现线程前，先确认当前工程包已进入基线提交；否则未跟踪文件会被视为本线程改动。

后端工程创建后：

```bash
cd backend
./mvnw test
./mvnw spring-boot:run -Dspring-boot.run.profiles=local
```

Web 工程创建后：

```bash
cd web
npm install
npm run lint
npm run build
npm run dev
```

后台工程创建后：

```bash
cd admin
npm install
npm run lint
npm run build
npm run dev
```

原型检查：

```bash
node --check prototype/html/app.js
```

---

## 5. 契约变更流程

任何线程需要修改 API、数据库、权限、积分、量化模式、AI 输出或合规话术时，必须先提交：

```text
Contract Change Request

变更类型：
影响文件：
变更原因：
旧契约：
新契约：
影响线程：
测试影响：
是否需要合规确认：
```

集成负责人确认后，先更新契约文档，再进入实现。

---

## 6. 交付摘要模板

```text
分支：
Task ID：

完成内容：

修改文件：

验证结果：
- make check-all:
- 其他命令：

未完成事项：

风险：

需要主线集成处理：

契约变更：

文件边界：
- 是否越界：
- 如越界，处理方式：
```

---

## 7. 不允许的执行方式

- 不读 `AGENTS.md` 就开始改文件。
- 不写 Task Brief 就开始实现。
- 把 raw source notes 当成当前事实。
- 为了通过测试删除检查。
- 未经审批修改 API 或数据库。
- 在前端临时发明字段。
- 在量化模块引入 `live_trade`。
- 不得在 C 端展示持仓、买卖点、实时信号、跟单入口。
