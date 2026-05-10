# A股 AI 量化策略研究平台 Spring Boot 后端工程规范

- 文档状态：Draft / 工程实现版
- 默认框架：Spring Boot 3.x
- 默认 Java：17
- 默认数据库：MySQL 8.x
- 默认缓存：Redis
- 最后更新时间：2026-05-08

---

## 1. 工程目标

P0 后端目标是支撑微信小程序 + Web C 端 + Web 管理后台的基础闭环：

- 登录、用户、权限、风险确认。
- 策略、报告、市场温度、积分解锁。
- 量化研究、指标、回测、仿真和风控计算。
- 后台内容、审核、操作日志。
- AI 解读的结构化输出和合规拦截。

P0 不实现真实支付、券商账户、实盘交易、自动下单、跟单、公开持仓、买卖点和实时信号。

---

## 2. 推荐工程结构

MVP 可以单体部署，代码按模块分包：

```text
backend/
  src/main/java/com/aquant/
    AQuantApplication.java
    common/
      api/
      error/
      security/
      audit/
      idempotency/
      pagination/
    auth/
    user/
    strategy/
    report/
    marketdata/
    indicator/
    strategyengine/
    backtest/
    risk/
    points/
    arena/
    ai/
    admin/
  src/main/resources/
    application.yml
    application-local.yml
    db/migration/
```

包命名使用 Java 小写包名，文件夹可以映射为：

| 逻辑模块 | Java package | 职责 |
|---|---|---|
| `auth` | `auth` | 微信登录、短信登录、token |
| `user` | `user` | 用户资料、关注、风险确认 |
| `strategy` | `strategy` | 策略列表、详情、状态 |
| `report` | `report` | 报告、试看、积分解锁权限 |
| `market-data` | `marketdata` | 数据批次、交易日历、数据源状态 |
| `indicator-engine` | `indicator` | 市场温度和指标计算 |
| `strategy-engine` | `strategyengine` | 内部策略信号和参数版本 |
| `backtest-engine` | `backtest` | 回测任务、净值曲线、绩效摘要 |
| `risk-engine` | `risk` | 风控检查、风险词、合规边界 |
| `points` | `points` | 积分账户、充值订单、每日赠送、消耗 |
| `arena` | `arena` | 赛季、选手、榜单、对决、投票 |
| `ai` | `ai` | AI 解读、输出日志、拦截 |
| `admin` | `admin` | 后台聚合接口 |

---

## 3. 分层规范

每个业务模块默认包含：

```text
module/
  controller/
  service/
  repository/
  entity/
  dto/
  mapper/
```

| 层 | 规则 |
|---|---|
| Controller | 只处理 HTTP、鉴权注解、参数校验、响应包装 |
| Service | 写业务规则、事务、权限二次校验、幂等处理 |
| Repository | 只做数据访问，不写业务判断 |
| Entity | 对应数据库表，不直接暴露给前端 |
| DTO | request / response 分开命名 |
| Mapper | Entity 与 DTO 转换，禁止在 Controller 手写大量转换 |

事务规则：

- 积分扣减、权益写入、流水写入必须同一事务。
- 后台发布、审核、下线和取消成绩必须同一事务内写操作日志。
- 回测任务创建和执行可拆分事务，创建任务后异步计算。

---

## 4. 统一响应与异常

### 4.1 统一响应体

```java
public record ApiResponse<T>(
    String code,
    String message,
    T data,
    String traceId
) {}
```

分页响应：

```java
public record PageResponse<T>(
    List<T> items,
    int page,
    int pageSize,
    long total
) {}
```

### 4.2 异常码

后端统一定义 `ErrorCode` enum：

| code | HTTP |
|---|---:|
| `BAD_REQUEST` | 400 |
| `UNAUTHORIZED` | 401 |
| `FORBIDDEN` | 403 |
| `POINTS_NOT_ENOUGH` | 402 |
| `CONTENT_LOCKED` | 403 |
| `RISK_CONFIRM_REQUIRED` | 428 |
| `AUDIT_REQUIRED` | 403 |
| `NOT_FOUND` | 404 |
| `CONFLICT` | 409 |
| `IDEMPOTENCY_REPLAY` | 409 |
| `RATE_LIMITED` | 429 |
| `INTERNAL_ERROR` | 500 |

所有异常由 `GlobalExceptionHandler` 转成 `ApiResponse`。

---

## 5. 安全与权限

### 5.1 Spring Security

- C 端登录使用 JWT。
- 小程序登录通过微信 `code` 换取 openid，P0 可用 mock provider。
- 后台管理员使用单独角色：`ADMIN`、`OPERATOR`、`COMPLIANCE`。
- 所有 `/admin/**` 必须要求后台角色。
- 所有积分写接口必须登录。

### 5.2 权限底线

- 游客只能看首页、市场温度、策略简版、报告试看、竞技场免费榜单。
- 未登录用户不能充值、消耗积分、投票、报名、保存关注。
- 未消耗积分用户不能查看完整报告或需解锁观察内容。
- 积分解锁不能解锁持仓、买卖点、实时信号或策略代码。
- 后台所有敏感操作必须写 `operation_logs`。

---

## 6. 幂等与并发

### 6.1 幂等拦截

对以下接口启用 `Idempotency-Key`：

- 创建充值订单。
- 每日登录赠送。
- 消耗积分。
- 风险确认。
- AI 解读提交。
- 竞技场报名、投票、观察解锁。
- 后台发布、审核、下线、取消成绩。

实现规则：

- 保存 `userId + path + key + requestHash`。
- 请求体相同返回首次结果。
- 请求体不同返回 `IDEMPOTENCY_REPLAY`。
- Redis 可做短期缓存，MySQL 保存最终记录。

### 6.2 积分并发

- 扣减积分时使用数据库行锁：`SELECT ... FOR UPDATE`。
- 禁止余额为负。
- 流水记录必须包含 `balance_after`。
- 每日登录赠送按 `userId + date` 防重复。

---

## 7. 量化研究执行

### 7.1 默认模式

量化模块只允许：

- `research_only`
- `simulation_only`

业务层必须拒绝：

- `live_trade`
- broker account
- real order
- copy trading
- buy/sell signal for C端

### 7.2 执行链路

```text
data_batches
-> indicator_snapshots
-> backtest_runs
-> backtest_equity_points
-> risk_checks
-> reports / market_temperature / arena_rankings
```

### 7.3 任务调度

P0 使用 Spring Scheduler 即可：

- 每日市场温度刷新。
- 回测任务队列扫描。
- 竞技场榜单重算。
- 每日登录积分补偿任务。

后续并发压力上来后再切换 XXL-Job 或队列。

---

## 8. AI 风控

AI 输出必须结构化：

```json
{
  "answer": "",
  "confidence": "low|medium|high",
  "sources": [],
  "riskNotes": [],
  "blocked": false
}
```

服务端必须做：

- prompt 模板版本记录。
- 输出风险词扫描。
- 命中高风险词写 `audit_tasks`。
- 所有输出写 `ai_output_logs`。
- 禁止输出直接买入、卖出、持有、仓位、价格、跟单等操作建议。

---

## 9. OpenAPI 与文档

- 使用 `springdoc-openapi`。
- 本地地址默认 `/swagger-ui/index.html`。
- Controller 必须写 operation summary。
- Request DTO 必须使用 Bean Validation。
- 错误码以 `06_api_spec.md` 为准。

---

## 10. 配置

`application-local.yml` 默认包含：

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/aquant?useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai
    username: aquant
    password: aquant
  data:
    redis:
      host: localhost
      port: 6379

app:
  security:
    jwt-secret: local-dev-secret
  payment:
    mode: test
  quant:
    allowed-run-modes:
      - research_only
      - simulation_only
```

禁止把生产密钥提交到仓库。

---

## 11. 测试约定

| 类型 | 工具 | 必测 |
|---|---|---|
| 单元测试 | JUnit 5 | 积分、幂等、风控、评分 |
| Web 测试 | MockMvc | Controller 参数、鉴权、错误码 |
| 数据层 | Spring Boot Test | migration、Repository |
| 集成测试 | Spring Boot Test | 积分扣减、报告解锁、后台审核 |

最低门禁：

- `./mvnw test` 通过。
- 积分余额不可为负。
- 重复每日登录不重复赠送。
- 回测模式不能写入 `live_trade`。
- C 端响应不包含持仓、买卖点、实时信号、策略代码字段。

