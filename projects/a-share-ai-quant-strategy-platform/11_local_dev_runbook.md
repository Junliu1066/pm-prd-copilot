# A股 AI 量化策略研究平台本地开发 Runbook

- 文档状态：Draft / 本地启动版
- 适用读者：后端、前端、小程序、测试、Codex 执行线程
- 最后更新时间：2026-05-08

---

## 1. 本地依赖

默认版本：

| 依赖 | 版本 |
|---|---|
| Java | 17 |
| Spring Boot | 3.x |
| Maven | 使用项目自带 `mvnw` |
| MySQL | 8.x |
| Redis | 7.x |
| Node.js | 20+ |

P0 不需要真实微信支付、真实行情源、真实 AI 供应商即可本地运行。外部服务全部先用 mock 或测试模式。

---

## 2. 推荐本地目录

```text
projects/a-share-ai-quant-strategy-platform/
  backend/
  miniapp/
  web/
  admin/
  prototype/html/
  db/
```

当前阶段如果还没有代码目录，先按文档创建工程，不要把原型目录当作正式前端工程。

---

## 3. 环境变量

本地 `.env.local` 建议：

```bash
APP_ENV=local
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=aquant
MYSQL_USERNAME=aquant
MYSQL_PASSWORD=aquant
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
JWT_SECRET=local-dev-secret
PAYMENT_MODE=test
AI_PROVIDER=mock
QUANT_RUN_MODES=research_only,simulation_only
```

禁止提交真实密钥。

---

## 4. 启动基础设施

可用 Docker，也可本机安装。

MySQL：

```bash
docker run --name aquant-mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=aquant -e MYSQL_USER=aquant -e MYSQL_PASSWORD=aquant -p 3306:3306 -d mysql:8
```

Redis：

```bash
docker run --name aquant-redis -p 6379:6379 -d redis:7
```

检查：

```bash
docker ps
```

---

## 5. 后端启动

首次启动：

```bash
cd backend
./mvnw clean test
./mvnw spring-boot:run -Dspring-boot.run.profiles=local
```

健康检查：

```bash
curl http://localhost:8080/actuator/health
```

Swagger：

```text
http://localhost:8080/swagger-ui/index.html
```

---

## 6. Mock 数据

P0 最少需要以下数据：

- 1 个游客可见策略。
- 1 个积分解锁策略。
- 1 份试看报告。
- 1 条市场温度快照。
- 1 个测试用户。
- 1 个管理员用户。
- 1 个 `research_only` 回测任务。

Mock 数据不得包含真实客户信息、真实券商账户、真实持仓和真实交易记录。

---

## 7. 前端启动

Web C 端：

```bash
cd web
npm install
npm run dev
```

管理后台：

```bash
cd admin
npm install
npm run dev
```

微信小程序：

- 用微信开发者工具打开 `miniapp/`。
- 本地 API 指向 `http://localhost:8080/api/v1`。
- 微信登录使用 mock code，后端 local profile 返回测试 openid。

HTML 原型：

```text
prototype/html/index.html
```

原型可直接用浏览器打开，不等同正式前端工程。

---

## 8. 常用调试命令

登录后保存 token：

```bash
curl -X POST http://localhost:8080/api/v1/auth/sms-login \
  -H 'Content-Type: application/json' \
  -d '{"phone":"13800000000","code":"123456"}'
```

查询积分：

```bash
curl http://localhost:8080/api/v1/points/account \
  -H 'Authorization: Bearer <token>'
```

测试充值：

```bash
curl -X POST http://localhost:8080/api/v1/points/recharge-orders \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: 00000000-0000-0000-0000-000000000001' \
  -d '{"amountCny":"30.00","paymentChannel":"test"}'
```

创建回测任务：

```bash
curl -X POST http://localhost:8080/api/v1/admin/backtest-runs \
  -H 'Authorization: Bearer <admin_token>' \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: 00000000-0000-0000-0000-000000000101' \
  -d '{"strategyId":1001,"runMode":"research_only","dataVersion":"2026-05-08","engineVersion":"v0.1.0","params":{"initialCapital":"1000000","feeRate":"0.0003","slippageRate":"0.0005","rebalanceFrequency":"weekly","benchmark":"CSI300"}}'
```

---

## 9. 本地检查

项目级门禁：

```bash
make check-all
```

分线程边界门禁：

```bash
THREAD=codex/p0-spring-api make check-boundary
THREAD=codex/p0-quant-engine make check-boundary
THREAD=codex/p0-points make check-boundary
THREAD=codex/qa-gates make check-boundary
```

注意：`check-boundary` 基于 git diff / status 判断改动文件。正式分线程开发前，先把当前工程包作为基线提交，否则整个未跟踪项目都会被视为当前线程改动。

后端：

```bash
cd backend
./mvnw test
```

Web：

```bash
cd web
npm run lint
npm run build
```

后台：

```bash
cd admin
npm run lint
npm run build
```

文档一致性：

```bash
rg -n "会员|月票|观众票|订阅|保证收益|跟单|带单|自动下单|券商账户|买卖点|实时信号" .
```

检查结果需要区分：

- 出现在“禁止使用 / 不做范围 / 合规红线”中可以保留。
- 出现在 C 端功能、接口响应、营销文案中必须删除或改写。

---

## 10. 常见问题

### 积分重复入账

检查：

- `Idempotency-Key` 是否传入。
- `point_transactions` 是否有唯一约束。
- 每日赠送是否按用户和日期去重。

### 报告解锁后仍不可见

检查：

- `content_entitlements` 是否写入。
- `reports.visibility` 是否为 `points_locked`。
- 当前用户是否登录。
- 风险确认版本是否通过。

### 回测任务被拒绝

检查：

- `runMode` 是否只使用 `research_only` 或 `simulation_only`。
- 参数是否包含被禁止字段，如券商账户、实盘订单、买卖信号。

### AI 输出被拦截

检查：

- 是否命中风险词。
- 是否包含直接交易建议。
- `ai_output_logs` 和 `audit_tasks` 是否记录。

---

## 11. 交付前检查

- 后端测试通过。
- 前端构建通过。
- Swagger 可访问。
- migration 可从空库执行。
- 积分充值、每日赠送、消耗、权益主路径可跑通。
- 市场温度、策略列表、报告试看可跑通。
- 后台审核、发布、下线写日志。
- C 端响应不包含持仓、买卖点、实时信号、策略代码。
- P0 文档与实现差异已回写到 `06_api_spec.md`、`07_database_schema.md`、`08_backend_engineering_spec.md`。
