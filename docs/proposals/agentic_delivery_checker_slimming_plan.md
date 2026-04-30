# Agentic Delivery Checker 瘦身方案

- 日期：2026-04-30
- 状态：方案，不批准代码修改 / staging / commit / stable 化
- 范围：`harness/agentic_delivery_checker.py`
- 原则：长期稳定可靠优先；如无必要，不增 harness；能放模板或人工审查清单的内容，不放进强 checker。

## 结论

`agentic_delivery_checker.py` 有价值，但当前检查面过宽。它把 Codex 开发文档、任务包、阶段计划、能力启用、Skill/MCP 路由、治理系统、学习机制、回滚和人工监督都压进一个 checker，长期维护成本偏高。

推荐做法：不删除、不 stable，先瘦身为“底线安全检查”。它只负责防止半自动开发阶段出现高风险缺口，其他细项移到模板、人工审查清单或 proposal。

## 当前问题

| 问题 | 影响 | 建议 |
|---|---|---|
| 检查文件太多 | 每次 Codex 开发文档结构调整都可能导致误报 | 只保留核心交付文档和审查文档的底线检查。 |
| 关键词过细 | 文档写法变化会造成 false positive | 用少量稳定概念检查替代大量细节关键词。 |
| 把治理机制细节放得太重 | 容易把候选治理能力误认为每个项目都必须完整具备 | 治理细项放到模板和人工审查清单。 |
| 阶段计划检查过满 | `一期 / 二期 / 三期 / 最终` 可能因项目规模变化而调整 | checker 只检查是否有阶段边界和验收，不强制每份阶段文档都有全部关键词。 |

## 建议保留的底线检查

瘦身后 checker 只检查 6 类底线：

| 底线 | 目的 |
|---|---|
| 允许修改范围 | 防止 agent 改出授权目录。 |
| 禁止修改范围 | 防止误改用户资产、稳定架构、生产配置或无关项目。 |
| 验证命令 | 防止任务包不可验收。 |
| 人工确认点 | 防止绕过 PRD 范围、数据库、外部服务、模型、发布、删除等高风险审批。 |
| 回滚方案 | 防止半自动开发失败后无法恢复。 |
| 任务包可执行性 | 确认每个任务有输入、输出、边界和验收方式。 |

## 建议弱化或移出 harness 的内容

| 内容 | 处理建议 | 原因 |
|---|---|---|
| 大量 Skill/MCP/Harness 细项 | 移到 Codex 开发文档模板 | 属于文档质量要求，不应都变成强 checker。 |
| 多管家、教师、学习机制等完整治理描述 | 移到内部版开发文档模板 | 外部版或轻量项目不一定需要完整展开。 |
| 每个阶段文档的完整关键词列表 | 改成人工审查清单 | 阶段结构会随项目变化。 |
| 能力启用、MCP 接入、新 Skill 创建的细粒度检查 | 保留为人工确认项 | 符合“如无必要，不增 skill / harness”。 |
| 发送前最优性报告的大量检查维度 | 保留为推荐审查模板 | 不应阻塞每个 agentic delivery 项目。 |

## 建议代码修改方向

后续如果你批准代码修改，建议这样改：

1. 保留触发条件：
   - `requires_agentic_delivery`
   - `agentic_delivery_planning`
   - manifest required outputs / enabled skills
   - 已存在 agentic delivery 文件
2. 缩小必需文件集合：
   - `codex_task_packages.md`
   - `human_supervision_plan.md`
   - `codex_development_document.md` 或 `codex_development_plan.md`
   - `codex_development_review.md`
   - `development_governance_report.json`
3. 其他文件不再作为 hard required：
   - `capability_enablement_plan.md`
   - `skill_mcp_routing_plan.md`
   - `development_operating_system_plan.md`
   - `codex_task_package_blueprint.md`
   - `phase_1/2/3/final_codex_plan.md`
4. 对非必需文件的处理：
   - 如果存在，只做轻量建议检查。
   - 如果不存在，不报错。
5. 把错误分成两类：
   - `fail`：缺少写入边界、人工确认、验证命令、回滚、任务可执行性。
   - `warn`：缺少增强治理说明、阶段细节、Skill/MCP 路由细节。

## 预期效果

| 维度 | 瘦身前 | 瘦身后 |
|---|---|---|
| 长期维护成本 | 高 | 中低 |
| 对真实项目适配性 | 容易过拟合完整治理文档 | 更适合不同规模项目 |
| 防事故能力 | 强但重 | 保留关键安全边界 |
| 误报风险 | 高 | 降低 |
| 是否新增 harness | 否 | 否 |

## 不建议的做法

- 不建议删除这个 checker：它仍能保护 Codex 半自动开发阶段。
- 不建议直接 stable：真实项目验证还不够。
- 不建议继续扩大检查项：会违背“如无必要，不增 harness”。
- 不建议把所有开发文档质量要求都写进 checker：模板和人工审查更合适。

## 需要你后续拍板

| 决策 | 我的建议 | 结果 |
|---|---|---|
| 是否按本方案瘦身代码 | 建议做 | 可以降低维护成本，并保留关键安全边界。 |
| 是否提交瘦身后的 checker | 瘦身并验证后再单独提交 | 不和项目产物或其他候选混提交。 |
| 是否保留完整细项为模板/审查清单 | 建议保留 | 不丢治理经验，但不压进强 checker。 |
| 是否转 stable | 暂不 | 真实项目跑 2-3 次后再决定。 |

## 验证方案

如果后续执行代码修改，需要运行：

```bash
PYTHONPYCACHEPREFIX=/tmp/pycache python3 -m py_compile harness/agentic_delivery_checker.py harness/run_harness.py
git diff --check
python3 pm-prd-copilot/scripts/run_regression.py --base-dir . --strict
python3 harness/run_harness.py --base-dir . --project demo-project --mode advisory --check-only --audit --efficiency
```

人工验收重点：

- 未请求 agentic delivery 的项目不被阻塞。
- 缺少写入边界、人工确认、验证命令、回滚方案时必须报错。
- 缺少增强型治理细节时不直接 fail。
- 不新增 harness。
- 不写项目文件。
