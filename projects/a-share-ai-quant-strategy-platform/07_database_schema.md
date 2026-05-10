# A股 AI 量化策略研究平台数据库设计

- 文档状态：Draft / 建表实现版
- 默认数据库：MySQL 8.x
- 默认字符集：`utf8mb4`
- 默认存储引擎：InnoDB
- 最后更新时间：2026-05-08

---

## 1. 建模约定

- 主键统一 `BIGINT UNSIGNED AUTO_INCREMENT`。
- 时间字段统一 `DATETIME(3)`。
- 金额字段统一 `DECIMAL(18,2)`。
- 比率和指标字段统一 `DECIMAL(18,6)`，展示时前端格式化。
- JSON 字段使用 MySQL `JSON`。
- 状态枚举落库使用 `VARCHAR(32)`，业务层用 Java enum。
- 表必须包含必要索引，后台审计表只追加不物理删除。
- P0 不保存券商账户、实盘订单、公开持仓、买卖点和实时信号。

---

## 2. Migration 顺序

| 顺序 | migration | 内容 |
|---:|---|---|
| 1 | `V001__create_users_and_auth.sql` | 用户、风险确认 |
| 2 | `V002__create_points.sql` | 积分账户、流水、充值订单、幂等记录 |
| 3 | `V003__create_strategy_report.sql` | 策略、指标、报告 |
| 4 | `V004__create_quant_engine.sql` | 数据批次、指标快照、回测任务、净值点、风控检查 |
| 5 | `V005__create_market_temperature.sql` | 市场温度 |
| 6 | `V006__create_arena.sql` | 赛季、选手、榜单、对决、投票、观察权益 |
| 7 | `V007__create_audit_logs.sql` | 审核任务、操作日志、AI 输出日志 |

---

## 3. 用户与权限

### 3.1 `users`

```sql
CREATE TABLE users (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  openid VARCHAR(128) NULL,
  unionid VARCHAR(128) NULL,
  phone VARCHAR(32) NULL,
  email VARCHAR(128) NULL,
  nickname VARCHAR(64) NOT NULL,
  avatar_url VARCHAR(512) NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'active',
  created_at DATETIME(3) NOT NULL,
  updated_at DATETIME(3) NOT NULL,
  UNIQUE KEY uk_users_openid (openid),
  UNIQUE KEY uk_users_phone (phone),
  KEY idx_users_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

状态：`active`、`disabled`。

### 3.2 `risk_confirmations`

```sql
CREATE TABLE risk_confirmations (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NOT NULL,
  scene VARCHAR(32) NOT NULL,
  version VARCHAR(64) NOT NULL,
  confirmed_at DATETIME(3) NOT NULL,
  UNIQUE KEY uk_risk_user_scene_version (user_id, scene, version),
  KEY idx_risk_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

`scene`：`strategy`、`report`、`arena`、`recharge`、`ai`。

---

## 4. 积分

### 4.1 `point_accounts`

```sql
CREATE TABLE point_accounts (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NOT NULL,
  balance INT NOT NULL DEFAULT 0,
  total_recharged INT NOT NULL DEFAULT 0,
  total_granted INT NOT NULL DEFAULT 0,
  total_consumed INT NOT NULL DEFAULT 0,
  created_at DATETIME(3) NOT NULL,
  updated_at DATETIME(3) NOT NULL,
  UNIQUE KEY uk_point_accounts_user (user_id),
  CONSTRAINT ck_point_balance_non_negative CHECK (balance >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 4.2 `point_transactions`

```sql
CREATE TABLE point_transactions (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NOT NULL,
  account_id BIGINT UNSIGNED NOT NULL,
  tx_type VARCHAR(32) NOT NULL,
  amount INT NOT NULL,
  balance_after INT NOT NULL,
  scene VARCHAR(64) NOT NULL,
  related_object_type VARCHAR(64) NULL,
  related_object_id BIGINT UNSIGNED NULL,
  status VARCHAR(32) NOT NULL,
  idempotency_key VARCHAR(128) NULL,
  created_at DATETIME(3) NOT NULL,
  UNIQUE KEY uk_point_tx_idempotency (user_id, idempotency_key),
  KEY idx_point_tx_user_created (user_id, created_at),
  KEY idx_point_tx_scene (scene, related_object_type, related_object_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

`tx_type`：`recharge`、`daily_grant`、`admin_grant`、`consume`、`refund`。  
`status`：`pending`、`success`、`failed`、`reversed`。

### 4.3 `point_recharge_orders`

```sql
CREATE TABLE point_recharge_orders (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NOT NULL,
  amount_cny DECIMAL(18,2) NOT NULL,
  points INT NOT NULL,
  payment_channel VARCHAR(32) NOT NULL,
  status VARCHAR(32) NOT NULL,
  idempotency_key VARCHAR(128) NULL,
  paid_at DATETIME(3) NULL,
  created_at DATETIME(3) NOT NULL,
  updated_at DATETIME(3) NOT NULL,
  UNIQUE KEY uk_recharge_idempotency (user_id, idempotency_key),
  KEY idx_recharge_user_created (user_id, created_at),
  KEY idx_recharge_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

P0 `payment_channel` 只启用 `test`、`manual`；真实 `wechat` 后置审批。

### 4.4 `idempotency_records`

```sql
CREATE TABLE idempotency_records (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NULL,
  request_path VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(128) NOT NULL,
  request_hash VARCHAR(128) NOT NULL,
  response_body JSON NOT NULL,
  status_code INT NOT NULL,
  expires_at DATETIME(3) NOT NULL,
  created_at DATETIME(3) NOT NULL,
  UNIQUE KEY uk_idempotency_scope (user_id, request_path, idempotency_key),
  KEY idx_idempotency_expires (expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## 5. 策略与报告

### 5.1 `strategies`

```sql
CREATE TABLE strategies (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(128) NOT NULL,
  code VARCHAR(64) NOT NULL,
  strategy_type VARCHAR(32) NOT NULL,
  market_scope VARCHAR(128) NOT NULL,
  risk_level VARCHAR(32) NOT NULL,
  access_level VARCHAR(32) NOT NULL,
  status VARCHAR(32) NOT NULL,
  summary TEXT NOT NULL,
  logic_summary TEXT NOT NULL,
  applicable_market TEXT NULL,
  failure_scenarios TEXT NULL,
  compliance_note TEXT NOT NULL,
  created_by BIGINT UNSIGNED NOT NULL,
  created_at DATETIME(3) NOT NULL,
  updated_at DATETIME(3) NOT NULL,
  UNIQUE KEY uk_strategies_code (code),
  KEY idx_strategies_type_status (strategy_type, status),
  KEY idx_strategies_access (access_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

`access_level`：`free`、`preview`、`points_locked`、`internal_only`。

### 5.2 `strategy_metrics`

```sql
CREATE TABLE strategy_metrics (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  strategy_id BIGINT UNSIGNED NOT NULL,
  period VARCHAR(32) NOT NULL,
  annual_return DECIMAL(18,6) NULL,
  max_drawdown DECIMAL(18,6) NULL,
  sharpe DECIMAL(18,6) NULL,
  volatility DECIMAL(18,6) NULL,
  win_rate DECIMAL(18,6) NULL,
  data_type VARCHAR(32) NOT NULL,
  calculated_at DATETIME(3) NOT NULL,
  UNIQUE KEY uk_strategy_metrics_period (strategy_id, period, data_type),
  KEY idx_strategy_metrics_calc (calculated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

`data_type`：`backtest`、`simulation`、`imported_simulation`。

### 5.3 `reports`

```sql
CREATE TABLE reports (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  strategy_id BIGINT UNSIGNED NOT NULL,
  title VARCHAR(255) NOT NULL,
  version VARCHAR(64) NOT NULL,
  visibility VARCHAR(32) NOT NULL,
  required_points INT NOT NULL DEFAULT 0,
  content_blocks JSON NOT NULL,
  backtest_params JSON NULL,
  status VARCHAR(32) NOT NULL,
  published_at DATETIME(3) NULL,
  created_at DATETIME(3) NOT NULL,
  updated_at DATETIME(3) NOT NULL,
  UNIQUE KEY uk_reports_strategy_version (strategy_id, version),
  KEY idx_reports_status (status),
  KEY idx_reports_visibility (visibility)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

`visibility`：`preview`、`points_locked`、`internal_only`。

### 5.4 `content_entitlements`

```sql
CREATE TABLE content_entitlements (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NOT NULL,
  scene VARCHAR(64) NOT NULL,
  object_type VARCHAR(64) NOT NULL,
  object_id BIGINT UNSIGNED NOT NULL,
  point_transaction_id BIGINT UNSIGNED NOT NULL,
  expires_at DATETIME(3) NULL,
  created_at DATETIME(3) NOT NULL,
  UNIQUE KEY uk_entitlement_object (user_id, scene, object_type, object_id),
  KEY idx_entitlement_user (user_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## 6. 量化研究与回测

### 6.1 `data_batches`

```sql
CREATE TABLE data_batches (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  source VARCHAR(64) NOT NULL,
  market VARCHAR(64) NOT NULL,
  data_type VARCHAR(64) NOT NULL,
  trade_date DATE NOT NULL,
  version VARCHAR(64) NOT NULL,
  status VARCHAR(32) NOT NULL,
  error_message TEXT NULL,
  created_at DATETIME(3) NOT NULL,
  UNIQUE KEY uk_data_batch (source, market, data_type, trade_date, version),
  KEY idx_data_batch_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 6.2 `indicator_snapshots`

```sql
CREATE TABLE indicator_snapshots (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  data_batch_id BIGINT UNSIGNED NOT NULL,
  indicator_code VARCHAR(64) NOT NULL,
  indicator_value DECIMAL(18,6) NOT NULL,
  dimension VARCHAR(64) NOT NULL,
  calculated_at DATETIME(3) NOT NULL,
  KEY idx_indicator_batch (data_batch_id),
  KEY idx_indicator_code_calc (indicator_code, calculated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 6.3 `backtest_runs`

```sql
CREATE TABLE backtest_runs (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  strategy_id BIGINT UNSIGNED NOT NULL,
  run_mode VARCHAR(32) NOT NULL,
  params JSON NOT NULL,
  data_version VARCHAR(64) NOT NULL,
  engine_version VARCHAR(64) NOT NULL,
  status VARCHAR(32) NOT NULL,
  result_summary JSON NULL,
  risk_status VARCHAR(32) NULL,
  created_at DATETIME(3) NOT NULL,
  completed_at DATETIME(3) NULL,
  KEY idx_backtest_strategy (strategy_id, created_at),
  KEY idx_backtest_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

`run_mode` 只允许 `research_only`、`simulation_only`。业务层必须拒绝 `live_trade`。

### 6.4 `backtest_equity_points`

```sql
CREATE TABLE backtest_equity_points (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  run_id BIGINT UNSIGNED NOT NULL,
  trade_date DATE NOT NULL,
  equity DECIMAL(18,6) NOT NULL,
  drawdown DECIMAL(18,6) NOT NULL,
  benchmark_equity DECIMAL(18,6) NULL,
  UNIQUE KEY uk_backtest_equity_day (run_id, trade_date),
  KEY idx_backtest_equity_run (run_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 6.5 `risk_checks`

```sql
CREATE TABLE risk_checks (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  object_type VARCHAR(64) NOT NULL,
  object_id BIGINT UNSIGNED NOT NULL,
  check_type VARCHAR(64) NOT NULL,
  result VARCHAR(32) NOT NULL,
  detail JSON NULL,
  checked_at DATETIME(3) NOT NULL,
  KEY idx_risk_object (object_type, object_id),
  KEY idx_risk_result (result, checked_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## 7. 市场温度

```sql
CREATE TABLE market_temperature_snapshots (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  market VARCHAR(64) NOT NULL,
  score INT NOT NULL,
  conclusion VARCHAR(32) NOT NULL,
  sentiment_score INT NOT NULL,
  trend_score INT NOT NULL,
  profit_effect_score INT NOT NULL,
  volatility_risk_score INT NOT NULL,
  rotation_score INT NOT NULL,
  explanation TEXT NOT NULL,
  data_source VARCHAR(128) NOT NULL,
  snapshot_at DATETIME(3) NOT NULL,
  created_at DATETIME(3) NOT NULL,
  KEY idx_market_temp_latest (market, snapshot_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## 8. 竞技场

### 8.1 `arena_seasons`

```sql
CREATE TABLE arena_seasons (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(64) NOT NULL,
  starts_at DATE NOT NULL,
  ends_at DATE NOT NULL,
  initial_capital DECIMAL(18,2) NOT NULL,
  target_pool JSON NOT NULL,
  rules JSON NOT NULL,
  status VARCHAR(32) NOT NULL,
  created_at DATETIME(3) NOT NULL,
  updated_at DATETIME(3) NOT NULL,
  UNIQUE KEY uk_arena_season_name (name),
  KEY idx_arena_season_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 8.2 `arena_players`

```sql
CREATE TABLE arena_players (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NOT NULL,
  season_id BIGINT UNSIGNED NOT NULL,
  nickname VARCHAR(64) NOT NULL,
  signature VARCHAR(128) NULL,
  skin_code VARCHAR(64) NULL,
  platform_account_id VARCHAR(128) NULL,
  review_status VARCHAR(32) NOT NULL,
  tier VARCHAR(32) NULL,
  created_at DATETIME(3) NOT NULL,
  updated_at DATETIME(3) NOT NULL,
  UNIQUE KEY uk_arena_player_user_season (user_id, season_id),
  UNIQUE KEY uk_arena_player_nickname_season (season_id, nickname),
  KEY idx_arena_player_review (review_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 8.3 `arena_rankings`

```sql
CREATE TABLE arena_rankings (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  season_id BIGINT UNSIGNED NOT NULL,
  player_id BIGINT UNSIGNED NOT NULL,
  rank_type VARCHAR(32) NOT NULL,
  rank_no INT NOT NULL,
  return_rate DECIMAL(18,6) NOT NULL,
  max_drawdown DECIMAL(18,6) NOT NULL,
  sharpe DECIMAL(18,6) NULL,
  stability DECIMAL(18,6) NULL,
  score DECIMAL(18,6) NOT NULL,
  calculated_at DATETIME(3) NOT NULL,
  UNIQUE KEY uk_arena_ranking_player_type (season_id, player_id, rank_type),
  KEY idx_arena_ranking_list (season_id, rank_type, rank_no)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 8.4 `arena_battles`

```sql
CREATE TABLE arena_battles (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  season_id BIGINT UNSIGNED NOT NULL,
  player_a_id BIGINT UNSIGNED NOT NULL,
  player_b_id BIGINT UNSIGNED NOT NULL,
  starts_at DATETIME(3) NOT NULL,
  ends_at DATETIME(3) NOT NULL,
  result JSON NULL,
  status VARCHAR(32) NOT NULL,
  created_at DATETIME(3) NOT NULL,
  updated_at DATETIME(3) NOT NULL,
  KEY idx_arena_battle_season (season_id, starts_at),
  KEY idx_arena_battle_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 8.5 `arena_votes`

```sql
CREATE TABLE arena_votes (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  battle_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  voted_player_id BIGINT UNSIGNED NOT NULL,
  created_at DATETIME(3) NOT NULL,
  UNIQUE KEY uk_arena_vote_user_battle (battle_id, user_id),
  KEY idx_arena_vote_player (voted_player_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## 9. 审核与日志

### 9.1 `audit_tasks`

```sql
CREATE TABLE audit_tasks (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  object_type VARCHAR(64) NOT NULL,
  object_id BIGINT UNSIGNED NOT NULL,
  risk_level VARCHAR(32) NOT NULL,
  matched_words JSON NULL,
  status VARCHAR(32) NOT NULL,
  reviewer_id BIGINT UNSIGNED NULL,
  reviewed_at DATETIME(3) NULL,
  created_at DATETIME(3) NOT NULL,
  updated_at DATETIME(3) NOT NULL,
  KEY idx_audit_status (status, created_at),
  KEY idx_audit_object (object_type, object_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 9.2 `operation_logs`

```sql
CREATE TABLE operation_logs (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  actor_id BIGINT UNSIGNED NULL,
  action VARCHAR(128) NOT NULL,
  object_type VARCHAR(64) NOT NULL,
  object_id BIGINT UNSIGNED NULL,
  before_data JSON NULL,
  after_data JSON NULL,
  request_id VARCHAR(128) NULL,
  created_at DATETIME(3) NOT NULL,
  KEY idx_operation_actor (actor_id, created_at),
  KEY idx_operation_object (object_type, object_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 9.3 `ai_output_logs`

```sql
CREATE TABLE ai_output_logs (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NULL,
  scene VARCHAR(64) NOT NULL,
  object_type VARCHAR(64) NULL,
  object_id BIGINT UNSIGNED NULL,
  prompt_hash VARCHAR(128) NOT NULL,
  output_text TEXT NOT NULL,
  risk_result VARCHAR(32) NOT NULL,
  matched_words JSON NULL,
  created_at DATETIME(3) NOT NULL,
  KEY idx_ai_log_user (user_id, created_at),
  KEY idx_ai_log_risk (risk_result, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## 10. 数据库验收

- 所有建表 SQL 可在空 MySQL 8 库顺序执行。
- 积分账户余额不能为负。
- 每日登录赠送通过业务唯一键或幂等键避免重复入账。
- 积分消耗和权益写入必须在同一事务内完成。
- 所有后台发布、审核、下线、取消成绩必须写 `operation_logs`。
- `backtest_runs.run_mode` 业务层只能写 `research_only` / `simulation_only`。
- 数据模型不得新增券商账户、实盘订单、公开持仓、买卖点或实时信号表。

