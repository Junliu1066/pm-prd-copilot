# 商家财务流水批量导出 - Tracking Plan

请自行核验事件命名、属性定义、采集位置和统计口径后再用于正式开发。

## Metrics
- export_usage (input)
  - 定义：导出请求次数
  - 公式：count(export_submit)
  - 观察窗口：daily
- export_success_rate (input)
  - 定义：导出成功次数 / 导出请求次数
  - 公式：count(export_success) / count(export_submit)
  - 观察窗口：daily
- manual_support_tickets (guardrail)
  - 定义：相关人工支持工单量
  - 公式：count(tickets tagged export)
  - 观察窗口：weekly
- export_failure_rate (guardrail)
  - 定义：导出失败次数 / 导出请求次数
  - 公式：count(export_failure) / count(export_submit)
  - 观察窗口：daily

## Events
- export_click
  - 触发时机：用户点击导出入口
  - 属性：role、module、date_range
  - 关联指标：export_usage
  - QA：前端事件校验 + 日志抽样核对
- export_submit
  - 触发时机：用户提交导出请求
  - 属性：role、row_estimate、filters
  - 关联指标：export_usage
  - QA：请求链路日志比对
- export_success
  - 触发时机：导出任务成功完成
  - 属性：duration_ms、row_count、file_size
  - 关联指标：export_success_rate
  - QA：服务端日志与埋点对账
- export_failure
  - 触发时机：导出任务失败
  - 属性：error_code、duration_ms、role
  - 关联指标：export_failure_rate
  - QA：错误码分布核对

## Open Questions
- 导出的核心目标用户是谁：商家自助导出，还是客服后台代导出，或两者都要？
- “财务流水”具体包含哪些业务单据/资金变动类型？
- 导出字段清单、字段定义、排序方式、筛选条件分别是什么？
- 数据权限如何定义：按商家、门店、账号、时间范围还是资金账户隔离？
- 是否允许导出全部历史数据？单次最大时间跨度和最大数据量是多少？
- 导出形式是同步下载还是异步任务？是否需要邮件/站内通知？
- 支持哪些文件格式（CSV、Excel）？是否有模板要求？
- 是否需要脱敏字段（如账户信息、联系人信息）？
- 是否需要操作审计、审批流或水印？
- 成功指标如何定义：客服工单下降、导出使用率、对账耗时下降、成交支持数等？
- 期望上线时间和客户承诺时间是什么？
