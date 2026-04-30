# 用户长期偏好

状态：已批准的长期偏好

本文件只记录已经得到用户明确批准的长期偏好。

## 当前已批准偏好

- 默认输出语言：中文。
- 决策风格：直接、结构化、务实。
- 工程简洁规则：长期稳定可靠优先；如果一行清晰代码能正确、可读地解决问题，就不要扩展成多行代码、额外抽象或新增组件。
- 升级审批规则：具体建议方案和 PR 级改动必须经过用户明确批准。
- 长期规则评审格式：任何长期规则、稳定偏好、Skill 行为、harness 检查、workflow 规则、steward 规则、plugin 规则、automation 规则或其他治理变更写入前，必须先提供具体建议方案，包含问题背景、推荐方案、优势、劣势与风险、替代方案、推荐结论、执行范围、验证方式和需要审批的点。只有用户明确批准后，才能写入变更。
- PRD 交付底线：软件或产品开发类 PRD 必须包含页面说明、页面跳转关系和 PRD 原型图层，原型图层可以是页面级低保真原型说明或页面原型说明。产品总览思维导图、泳道图、页面信息架构图、MVP 范围图、风险控制闭环图、状态流转图、决策树、用户故事地图等辅助图表，按项目必要性选择，并放在对应 PRD 章节里，不集中堆成通用“可视化层”。AI 模型选型只在项目涉及 AI 能力时出现。
- PRD 原型图层批准记录：2026-04-29，用户已明确批准把 PRD 原型图层加入长期规则。PRD 输出必须包含页面级低保真原型说明或页面原型说明；PNG、HTML、完整原型和 UI 设计仍需要后续用户确认后再进入。
- 原型交付链路：原型工作遵循受监督链路：`PRD / 需求 -> 产品流程 / 页面信息架构 / PRD 原型图层 -> 低保真原型预览 -> 人工审核 -> 完整线框图或原型 -> 必要时转 HTML -> 视觉 / 交互 / 跳转 QA -> 人工批准 -> UI 设计或 Codex 开发文档`。不得跳过预览审批；如果原型反馈改变产品行为，必须同步更新 PRD 或产品流程。
- 项目偏好缓存规则：项目级偏好只能在当前项目内使用，只能记录本项目内讨论并批准的偏好，并且必须在归档前保存进 closeout / 归档材料。归档时需要和用户对齐哪些清除、哪些作为项目证据保留、哪些可以提炼为长期偏好。默认禁止跨项目复用；长期记忆更新必须经过用户明确批准。
- 术语偏好：当用户说“开发文档”时，默认理解为 Codex 开发文档，而不是泛泛的技术文档，除非用户明确说明其他含义。
- 文档边界规则：产品归产品，开发归开发。PRD 描述面向用户的产品价值、用户流程、产品范围、验收标准和产品约束；开发文档描述实现、架构、任务拆分、工具、内部 agent、Skill/MCP、harness 和工程治理。除非用户明确要求产品化，否则不得把开发机制写成用户侧产品能力。
- Codex 开发文档底线：Codex 开发文档必须包含任务包、允许修改路径、禁止修改路径、验证命令、人工确认点、回滚或最小修复策略，以及评审或复盘路径。完整内部治理细节，例如 Skill/MCP 路由、harness、审计、学习吸收、多管家运行结构，应放在内部版 / 完整版，或在项目确实需要时出现，不作为每份文档的强制堆叠内容。
- 框架保护规则：默认输出 B execution-pack 版本，除非用户明确说“内部版”、“我自己用”、“自己项目”、“我的项目”或“可信团队”。只有明确的内部 / 自用语义，才可以输出带完整命名的治理框架。语义不清时，输出 B execution-pack 版本，使用字母化文件名和包名，保留执行门禁与验收要求，同时隐藏框架名称和内部机制。
- 框架暴露条件：只有用户明确要求把框架产品化、集成、暴露，或明确说不需要隐藏时，才可以把多管家、Skill/MCP、harness、审计、学习机制等作为产品能力或可见运行层表达。否则一律按内部治理机制保护。
- 开发分期规则：Codex 开发文档和 B execution-pack 文档应使用 `一期 / 二期 / 三期 / 最终` 作为顶层交付路线。更细的 Phase 0-9 或任务拆分只能放在该路线之下。
- B execution-pack 语言规则：所有 B 版本文件和 B 包 README 必须只使用英文。内部版 / 完整版文档可保持中文，除非用户另有要求。
- 开发归属语义规则：当用户说“我自己开发”或“自己开发”时，理解为“用户会主导或参与开发”，不能理解为“产品只给个人使用”。产品受众需要根据上下文判断，或单独向用户确认。
- 文档受众分层规则：按受众拆分文档。PRD 服务产品 / 业务 / 用户评审；开发文档服务工程实现；Codex 内部开发文档服务 agent 执行、任务边界、验证和人工门禁。可以互相引用，但不能合并成一份泛化文档。
- Codex 内部可执行性规则：Codex 内部开发文档如果缺少任务包、负责人、输入、输出、允许修改路径、禁止修改路径、验证命令、人工确认点、依赖关系和最小修复策略，就视为不完整。
- 开发包完整性规则：当用户要求开发就绪包时，按受众和项目阶段包含执行所需资产，并遵守脱敏和分发策略。典型资产包括 PRD、开发文档、必要时的 Codex 内部文档、流程图、PRD 原型图层、已确认的原型材料、仅限 AI 项目的 AI / 模型说明、相关来源材料和包清单。跨平台分发时优先使用英文路径 zip。
- 禁止改动指令规则：当用户说“先别改动”或同等意思时，只能报告分析或建议；在得到明确批准前，不得编辑文件、memory、skills、proposals、packages 或项目产物。

## English Reference

This section is an English reference for tooling and review. The Chinese section above is authoritative.

- Default output language: Chinese.
- Decision style: direct, structured, and practical.
- Engineering simplicity rule: long-term stability and reliability come first. If one clear line of code solves the problem correctly and readably, do not expand it into multi-line code, extra abstraction, or additional components.
- Upgrade approval rule: concrete recommendation plans and PR-level changes require explicit user approval.
- Long-term rule review format: before writing any long-term rule, stable preference, Skill behavior, harness check, workflow rule, steward rule, plugin rule, automation rule, or other governance change, first provide a concrete recommendation plan covering background, recommended plan, advantages, disadvantages and risks, alternatives, recommendation conclusion, execution scope, validation method, and approval points. Do not write the change until the user explicitly approves it.
- PRD delivery baseline: software or product development PRDs must include page descriptions, page navigation relationships, and a PRD prototype layer with page-level low-fidelity prototype notes or page prototype explanations. Other visual aids such as product overview mind maps, swimlanes, page information architecture, MVP scope maps, risk-control loops, state flows, decision trees, and user story maps should be selected by project necessity and placed in the relevant PRD section, not collected into a generic visualization section. AI model selection appears only when the project involves AI capabilities.
- PRD prototype layer approval record: on 2026-04-29, the user explicitly approved adding the PRD prototype layer as a long-term rule. PRD outputs must include page-level low-fidelity prototype notes or page prototype explanations. PNG, HTML, full prototypes, and UI design still require later user confirmation.
- Prototype delivery flow: prototype work follows the supervised chain `PRD / requirements -> product flow / page IA / PRD prototype layer -> low-fi prototype preview -> human review -> full wireframe/prototype -> HTML conversion when useful -> visual/interaction/navigation QA -> human approval -> UI design or Codex development document`. Do not skip preview approval. If prototype feedback changes product behavior, update the PRD or product flow as well.
- Project preference cache rule: project-level preferences may be used only inside the current project, may record only preferences discussed and approved within that project, and must be saved into closeout/archive materials before archive. At archive time, align with the user on what to clear, what to keep as project evidence, and what may become a long-term preference. Cross-project reuse is disabled by default; long-term memory updates require explicit user approval.
- Terminology preference: when the user says “开发文档”, interpret it as a Codex development document by default, not as a generic technical document, unless the user explicitly says otherwise.
- Document boundary rule: product is product and development is development. PRDs describe user-facing product value, user flows, product scope, acceptance criteria, and product constraints. Development documents describe implementation, architecture, task split, tooling, internal agents, Skill/MCP, harness, and engineering governance. Do not move development mechanisms into the user-facing product unless the user explicitly asks to productize them.
- Codex development document baseline: Codex development documents must include task packages, allowed write paths, forbidden write paths, validation commands, human confirmation gates, rollback or minimal-fix strategy, and a review or retrospective path. Full internal governance details such as Skill/MCP routing, harness, audit, learning absorption, and multi-manager operating structure should appear in internal/full versions or when the project requires them, not as mandatory bulk in every document.
- Framework protection rule: default to the B execution-pack version unless the user explicitly says “内部版”, “我自己用”, “自己项目”, “我的项目”, or “可信团队”. Only explicit internal/self-use wording may receive the full named governance framework. If the wording is unclear, generate the B execution-pack version with letter-coded filenames and package names, keeping execution gates and acceptance requirements while hiding framework names and internals.
- Framework exposure condition: when the user explicitly asks for the framework to be productized, integrated, exposed, or says it does not need to be hidden, frameworks such as 多管家, Skill/MCP, harness, audit, and learning mechanisms may be treated as product capabilities or visible operating layers. Otherwise, protect them as internal governance.
- Development phasing rule: Codex development documents and B execution-pack documents should use `一期 / 二期 / 三期 / 最终` as the top-level delivery route. Detailed Phase 0-9 or task breakdowns may appear only beneath that route.
- B execution-pack language rule: all B version files and B package README files must be English-only. Internal/full documents may remain Chinese unless the user asks otherwise.
- Development ownership wording rule: when the user says “我自己开发” or “自己开发”, interpret it as “the user will lead or participate in development”, not as “the product is only for personal use”. Product audience must be inferred from context or confirmed separately.
- Document audience layering rule: separate documents by audience. PRDs serve product/business/user review; development documents serve engineering implementation; Codex internal development documents serve agent execution, task boundaries, validation, and human gates. Cross-reference them, but do not collapse them into one generic document.
- Codex internal executability rule: a Codex internal development document is incomplete unless it includes task packages, owner, inputs, outputs, allowed write paths, forbidden write paths, validation commands, human confirmation points, dependencies, and minimal-fix strategy.
- Development package completeness rule: when asked for a development-ready package, include the execution assets needed for the audience and project stage, subject to redaction and distribution policy. Typical assets include the PRD, development document, Codex internal document when appropriate, flows, PRD prototype layer, confirmed prototype materials, AI/model notes only for AI projects, relevant source materials, and package manifest. Prefer an English-path zip for cross-platform extraction.
- No-write instruction rule: when the user says “先别改动” or equivalent, only report analysis or recommendations. Do not edit files, memory, skills, proposals, packages, or project artifacts until explicit approval is given.
