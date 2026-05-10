# A股 AI 量化策略研究平台 API 规格

- 文档状态：Draft / 工程实现版
- 适用读者：后端、前端、小程序、测试、Codex 执行线程
- 默认后端：Spring Boot 3.x
- 默认基础路径：`/api/v1`
- 最后更新时间：2026-05-08

---

## 1. API 基线

### 1.1 通用约定

- 所有接口使用 JSON。
- 时间统一使用 ISO-8601 字符串，服务端按 `Asia/Shanghai` 处理展示。
- 金额字段使用 decimal 字符串或 `BigDecimal`，积分字段使用 int。
- 分页从 `page=1` 开始，默认 `pageSize=20`，最大 `pageSize=100`。
- C 端不得返回持仓、买卖点、实时信号、策略代码、券商账户或自动下单字段。
- P0 充值接口只做测试通道和积分流水，真实微信支付后置。

### 1.2 认证

| 场景 | Header |
|---|---|
| 游客接口 | 无 |
| 登录接口 | 无 |
| 用户接口 | `Authorization: Bearer <token>` |
| 后台接口 | `Authorization: Bearer <admin_token>` |
| 幂等写接口 | `Idempotency-Key: <uuid>` |

### 1.3 通用响应

成功：

```json
{
  "code": "OK",
  "message": "success",
  "data": {},
  "traceId": "018f-req-id"
}
```

失败：

```json
{
  "code": "POINTS_NOT_ENOUGH",
  "message": "积分余额不足",
  "details": {
    "requiredPoints": 10,
    "balance": 3
  },
  "traceId": "018f-req-id"
}
```

分页：

```json
{
  "code": "OK",
  "message": "success",
  "data": {
    "items": [],
    "page": 1,
    "pageSize": 20,
    "total": 0
  },
  "traceId": "018f-req-id"
}
```

### 1.4 通用错误码

| code | HTTP | 说明 |
|---|---:|---|
| `OK` | 200 | 成功 |
| `BAD_REQUEST` | 400 | 参数错误 |
| `UNAUTHORIZED` | 401 | 未登录或 token 失效 |
| `FORBIDDEN` | 403 | 权限不足 |
| `NOT_FOUND` | 404 | 资源不存在 |
| `CONFLICT` | 409 | 状态冲突或重复提交 |
| `IDEMPOTENCY_REPLAY` | 409 | 幂等键重复且请求体不一致 |
| `POINTS_NOT_ENOUGH` | 402 | 积分余额不足 |
| `RISK_CONFIRM_REQUIRED` | 428 | 需要确认风险提示 |
| `CONTENT_LOCKED` | 403 | 内容需要积分解锁 |
| `AUDIT_REQUIRED` | 403 | 内容未审核通过 |
| `RATE_LIMITED` | 429 | 请求过于频繁 |
| `INTERNAL_ERROR` | 500 | 服务异常 |

---

## 2. C 端接口

### 2.1 市场温度

| 方法 | 路径 | 登录 | 说明 |
|---|---|---|---|
| GET | `/market/temperature/latest` | 否 | 获取最新市场温度 |

Query：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| market | string | 否 | 默认 `A_SHARE`，可选 `CSI300`、`ETF` |

Response `data`：

```json
{
  "market": "A_SHARE",
  "score": 62,
  "conclusion": "中性",
  "scores": {
    "sentiment": 58,
    "trend": 64,
    "profitEffect": 61,
    "volatilityRisk": 40,
    "rotation": 55
  },
  "explanation": "市场处于中性偏热区间。",
  "dataSource": "internal_mock",
  "snapshotAt": "2026-05-08T15:30:00+08:00"
}
```

错误码：`BAD_REQUEST`。

### 2.2 策略

| 方法 | 路径 | 登录 | 说明 |
|---|---|---|---|
| GET | `/strategies` | 否 | 策略列表 |
| GET | `/strategies/{id}` | 否 | 策略详情，按权限返回可见内容 |
| POST | `/user/favorites` | 是 | 关注策略 |

`GET /strategies` Query：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| type | string | 否 | `trend` / `rotation` / `defense` / `multi_factor` |
| riskLevel | string | 否 | `low` / `medium` / `high` |
| keyword | string | 否 | 策略名或摘要 |
| page | int | 否 | 默认 1 |
| pageSize | int | 否 | 默认 20 |

列表 item：

```json
{
  "id": 1001,
  "name": "沪深300趋势增强",
  "code": "ST-HS300-001",
  "strategyType": "trend",
  "riskLevel": "medium",
  "accessLevel": "preview",
  "summary": "趋势跟随与回撤控制结合。",
  "metrics": {
    "annualReturn": "18.42",
    "maxDrawdown": "-12.37",
    "sharpe": "1.36",
    "dataType": "backtest",
    "calculatedAt": "2026-05-08T15:30:00+08:00"
  }
}
```

`GET /strategies/{id}` Response `data`：

```json
{
  "id": 1001,
  "name": "沪深300趋势增强",
  "accessLevel": "points_locked",
  "summary": "趋势跟随与回撤控制结合。",
  "logicSummary": "试看版逻辑摘要。",
  "applicableMarket": "趋势延续行情",
  "failureScenarios": "高频震荡或极端流动性冲击",
  "complianceNote": "仅供研究，不构成投资建议。",
  "locked": true,
  "unlockScene": "report",
  "requiredPoints": 10
}
```

`POST /user/favorites` Request：

```json
{
  "strategyId": 1001,
  "action": "add"
}
```

错误码：`UNAUTHORIZED`、`NOT_FOUND`、`BAD_REQUEST`。

### 2.3 报告

| 方法 | 路径 | 登录 | 说明 |
|---|---|---|---|
| GET | `/reports/{id}` | 否 | 报告详情，按权限返回试看或完整内容 |

Response `data`：

```json
{
  "id": 2001,
  "strategyId": 1001,
  "title": "沪深300趋势增强回测报告",
  "version": "2026-W18",
  "visibility": "points_locked",
  "locked": true,
  "requiredPoints": 10,
  "contentBlocks": [
    {
      "type": "summary",
      "title": "报告摘要",
      "content": "试看内容。"
    }
  ],
  "backtestParams": {
    "initialCapital": "1000000",
    "feeRate": "0.0003",
    "slippageRate": "0.0005",
    "benchmark": "CSI300"
  },
  "riskNote": "回测不代表未来收益。"
}
```

错误码：`NOT_FOUND`、`CONTENT_LOCKED`、`RISK_CONFIRM_REQUIRED`。

### 2.4 登录与账户

| 方法 | 路径 | 登录 | 说明 |
|---|---|---|---|
| POST | `/auth/wechat-login` | 否 | 小程序微信登录 |
| POST | `/auth/sms-login` | 否 | 手机号验证码登录 |
| GET | `/profile` | 是 | 我的账户 |

`POST /auth/wechat-login` Request：

```json
{
  "code": "wx_login_code",
  "encryptedData": "optional",
  "iv": "optional"
}
```

Response `data`：

```json
{
  "token": "jwt-token",
  "expiresIn": 7200,
  "user": {
    "id": 1,
    "nickname": "用户123",
    "avatarUrl": "",
    "phoneBound": false
  }
}
```

`POST /auth/sms-login` Request：

```json
{
  "phone": "13800000000",
  "code": "123456"
}
```

`GET /profile` Response `data`：

```json
{
  "id": 1,
  "nickname": "用户123",
  "avatarUrl": "",
  "phone": "138****0000",
  "pointBalance": 18,
  "riskConfirmedVersions": ["report-v1"]
}
```

错误码：`BAD_REQUEST`、`UNAUTHORIZED`、`RATE_LIMITED`。

### 2.5 积分

| 方法 | 路径 | 登录 | 幂等 | 说明 |
|---|---|---|---|---|
| GET | `/points/account` | 是 | 否 | 积分账户 |
| GET | `/points/transactions` | 是 | 否 | 积分明细 |
| POST | `/points/recharge-orders` | 是 | 是 | 创建测试充值订单 |
| POST | `/points/daily-checkin` | 是 | 是 | 每日登录赠送 1 积分 |
| POST | `/points/consume` | 是 | 是 | 消耗积分解锁内容 |

`GET /points/account` Response `data`：

```json
{
  "balance": 18,
  "totalRecharged": 100,
  "totalGranted": 5,
  "totalConsumed": 87,
  "rules": {
    "rechargeRate": "1 CNY = 1 point",
    "dailyGrant": 1,
    "withdrawable": false
  }
}
```

`GET /points/transactions` Query：`scene`、`page`、`pageSize`。

`POST /points/recharge-orders` Request：

```json
{
  "amountCny": "30.00",
  "paymentChannel": "test"
}
```

Response `data`：

```json
{
  "orderId": 3001,
  "amountCny": "30.00",
  "points": 30,
  "status": "paid",
  "testMode": true
}
```

`POST /points/daily-checkin` Response `data`：

```json
{
  "granted": true,
  "points": 1,
  "balance": 19,
  "checkedInDate": "2026-05-08"
}
```

`POST /points/consume` Request：

```json
{
  "scene": "report",
  "objectType": "report",
  "objectId": 2001,
  "points": 10
}
```

Response `data`：

```json
{
  "transactionId": 4001,
  "balance": 8,
  "entitlement": {
    "scene": "report",
    "objectType": "report",
    "objectId": 2001,
    "expiresAt": null
  }
}
```

错误码：`UNAUTHORIZED`、`BAD_REQUEST`、`POINTS_NOT_ENOUGH`、`RISK_CONFIRM_REQUIRED`、`IDEMPOTENCY_REPLAY`。

### 2.6 风险确认与 AI 解读

| 方法 | 路径 | 登录 | 幂等 | 说明 |
|---|---|---|---|---|
| POST | `/risk/confirmations` | 是 | 是 | 风险提示确认 |
| POST | `/ai/strategy-explain` | 是 | 是 | AI 策略解释 |

`POST /risk/confirmations` Request：

```json
{
  "scene": "report",
  "version": "report-v1"
}
```

`POST /ai/strategy-explain` Request：

```json
{
  "strategyId": 1001,
  "question": "这个策略为什么回撤较低？"
}
```

Response `data`：

```json
{
  "answer": "该策略通过趋势过滤和回撤控制降低波动。",
  "confidence": "medium",
  "sources": ["backtest_run:5001", "strategy:1001"],
  "riskNotes": ["仅解释研究报告，不构成投资建议。"],
  "blocked": false
}
```

错误码：`UNAUTHORIZED`、`AUDIT_REQUIRED`、`BAD_REQUEST`、`RATE_LIMITED`。

---

## 3. 竞技场接口

| 方法 | 路径 | 登录 | 幂等 | 说明 |
|---|---|---|---|---|
| GET | `/arena/seasons/current` | 否 | 否 | 当前赛季 |
| GET | `/arena/rankings` | 否 | 否 | 排行榜 |
| GET | `/arena/players/{id}` | 否 | 否 | 选手档案 |
| POST | `/arena/players/apply` | 是 | 是 | 选手报名 |
| GET | `/arena/battles/{id}` | 否 | 否 | 1v1 对决详情 |
| POST | `/arena/battles/{id}/votes` | 是 | 是 | 投票 |
| GET | `/arena/audience/entitlements` | 是 | 否 | 观察内容可解锁范围 |
| POST | `/arena/audience/unlock` | 是 | 是 | 消耗积分解锁观察内容 |

`GET /arena/rankings` Query：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| seasonId | bigint | 否 | 默认当前赛季 |
| rankType | string | 否 | `comprehensive` / `day` / `horse` / `drawdown` / `sharpe` |
| page | int | 否 | 默认 1 |
| pageSize | int | 否 | 默认 20 |

Ranking item：

```json
{
  "rankNo": 1,
  "playerId": 501,
  "nickname": "Alpha-07",
  "tier": "Gold",
  "returnRate": "12.35",
  "maxDrawdown": "-5.20",
  "sharpe": "1.48",
  "stability": "82.00",
  "score": "88.50",
  "locked": false
}
```

`POST /arena/players/apply` Request：

```json
{
  "seasonId": 1,
  "nickname": "Alpha-07",
  "signature": "趋势研究者",
  "skinCode": "red-basic",
  "platformAccountId": "sim-account-001"
}
```

说明：报名消耗积分时由服务端按赛季规则读取 `applyCostPoints`，客户端不得决定费用。

`POST /arena/battles/{id}/votes` Request：

```json
{
  "votedPlayerId": 501
}
```

`POST /arena/audience/unlock` Request：

```json
{
  "seasonId": 1,
  "objectType": "player",
  "objectId": 501
}
```

Response `data`：

```json
{
  "transactionId": 4101,
  "balance": 6,
  "visibleFields": [
    "equityCurve",
    "maxDrawdown",
    "sharpe",
    "stability",
    "roadshowSummary"
  ],
  "excludedFields": [
    "positions",
    "buySellSignals",
    "strategyCode",
    "brokerAccount"
  ]
}
```

错误码：`UNAUTHORIZED`、`POINTS_NOT_ENOUGH`、`CONFLICT`、`RISK_CONFIRM_REQUIRED`、`AUDIT_REQUIRED`。

---

## 4. 管理后台接口

后台接口全部要求管理员 token，并记录 `operation_logs`。

### 4.1 内容与审核

| 方法 | 路径 | 幂等 | 说明 |
|---|---|---|---|
| GET | `/admin/dashboard` | 否 | 后台指标 |
| GET | `/admin/strategies` | 否 | 策略管理列表 |
| POST | `/admin/strategies` | 是 | 新建策略 |
| PATCH | `/admin/strategies/{id}` | 是 | 更新策略 |
| POST | `/admin/strategies/{id}/submit-review` | 是 | 提交审核 |
| POST | `/admin/strategies/{id}/publish` | 是 | 发布策略 |
| POST | `/admin/strategies/{id}/offline` | 是 | 下线策略 |
| GET | `/admin/reports` | 否 | 报告列表 |
| POST | `/admin/reports/{id}/publish` | 是 | 发布报告 |
| GET | `/admin/audit/tasks` | 否 | 审核任务 |
| POST | `/admin/audit/tasks/{id}/approve` | 是 | 审核通过 |
| POST | `/admin/audit/tasks/{id}/reject` | 是 | 审核驳回 |

`POST /admin/strategies` Request：

```json
{
  "name": "沪深300趋势增强",
  "code": "ST-HS300-001",
  "strategyType": "trend",
  "marketScope": "CSI300",
  "riskLevel": "medium",
  "accessLevel": "preview",
  "summary": "趋势跟随与回撤控制结合。",
  "logicSummary": "内部逻辑摘要。",
  "applicableMarket": "趋势延续行情",
  "failureScenarios": "震荡反复",
  "complianceNote": "仅供研究。"
}
```

### 4.2 量化与风控

| 方法 | 路径 | 幂等 | 说明 |
|---|---|---|---|
| GET | `/admin/data-batches` | 否 | 数据批次列表 |
| POST | `/admin/indicators/recalculate` | 是 | 重新计算指标 |
| GET | `/admin/backtest-runs` | 否 | 回测任务列表 |
| POST | `/admin/backtest-runs` | 是 | 创建回测任务 |
| GET | `/admin/risk-checks` | 否 | 风控检查记录 |

`POST /admin/backtest-runs` Request：

```json
{
  "strategyId": 1001,
  "runMode": "research_only",
  "dataVersion": "2026-05-08",
  "engineVersion": "v0.1.0",
  "params": {
    "initialCapital": "1000000",
    "feeRate": "0.0003",
    "slippageRate": "0.0005",
    "rebalanceFrequency": "weekly",
    "benchmark": "CSI300"
  }
}
```

服务端校验：

- `runMode` 只允许 `research_only`、`simulation_only`。
- 不接受 `live_trade`、券商账户、自动下单、持仓公开字段。
- 创建后先写 `backtest_runs`，再由任务调度执行。

### 4.3 竞技场后台

| 方法 | 路径 | 幂等 | 说明 |
|---|---|---|---|
| GET | `/admin/arena/seasons` | 否 | 赛季管理 |
| POST | `/admin/arena/seasons` | 是 | 新建赛季 |
| GET | `/admin/arena/players` | 否 | 选手管理 |
| POST | `/admin/arena/players/{id}/approve` | 是 | 选手审核通过 |
| POST | `/admin/arena/players/{id}/reject` | 是 | 选手审核驳回 |
| POST | `/admin/arena/players/{id}/disqualify` | 是 | 取消选手成绩 |

`POST /admin/arena/seasons` Request：

```json
{
  "name": "S1",
  "startsAt": "2026-06-01",
  "endsAt": "2026-06-30",
  "initialCapital": "1000000",
  "targetPool": ["CSI300", "ETF_POOL"],
  "rules": {
    "applyCostPoints": 30,
    "observeCostPoints": 10,
    "maxSinglePositionRate": "0.20",
    "dailyDrawdownStopRate": "0.07"
  }
}
```

---

## 5. 幂等与权限规则

### 5.1 幂等

- 所有 POST/PATCH 写接口必须支持 `Idempotency-Key`。
- 同一用户、同一接口、同一 key、同一请求体重复提交，返回第一次结果。
- 同一 key 但请求体不同，返回 `IDEMPOTENCY_REPLAY`。
- 幂等记录至少保存 24 小时。

### 5.2 积分扣减

- 积分扣减必须在数据库事务内完成。
- 扣减前锁定 `point_accounts` 用户行。
- 扣减后写 `point_transactions`。
- 任何积分解锁不得返回持仓、买卖点、实时信号、策略代码。

### 5.3 风险确认

- 报告完整解锁、AI 解读、竞技场观察解锁前必须检查风险确认版本。
- 风险确认版本由服务端配置，客户端不能绕过。

