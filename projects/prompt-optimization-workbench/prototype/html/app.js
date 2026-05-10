const routeTitles = {
  dashboard: "Dashboard 页面",
  prompts: "Prompts 页面",
  "prompt-create": "创建 Prompt 页面",
  "dataset-detail": "Dataset 详情",
  "dataset-edit": "编辑 Dataset",
  datasets: "Datasets 页面",
  models: "Models 页面",
  runs: "Runs 页面",
  review: "人工评审",
  evaluations: "Evaluations 页面",
  optimize: "Optimize 页面",
  compare: "Compare 页面",
  knowledge: "Knowledge 页面",
  "knowledge-detail": "知识条目详情",
  settings: "Settings 页面"
};

const editKey = "prompt-workbench-v2-inline-edits";
const toast = document.querySelector("#toast");
const pageTitle = document.querySelector("#pageTitle");
let activeDataset = "trademark";
let activeKnowledge = "instruction";

const datasetStore = {
  trademark: {
    id: "DST-0001",
    name: "商标侵权覆盖测试集",
    type: "商标侵权判断",
    owner: "张三",
    status: "已启用",
    cases: "2,048",
    risk: "345",
    riskRate: "12.8%",
    updated: "2024-05-24 10:30",
    tags: "商标、近似、法务",
    description: "用于评估商标侵权判断助手在近似商标、商品类别、混淆可能性与法律依据方面的表现。",
    casesRows: [
      ["CASE-0001", "文字与图形近似判断", "高风险", "高风险", "38 / 100"],
      ["CASE-0002", "商品类别与服务冲突", "中风险", "中风险", "68 / 100"]
    ],
    history: ["商标侵权新增样本_20240524.xlsx", "近似商标 Case 补充_20240520.csv", "高风险样本修订_20240518.xlsx"]
  },
  contract: {
    id: "DST-0002",
    name: "合同风险评测样本",
    type: "合同审核",
    owner: "李四",
    status: "已启用",
    cases: "1,890",
    risk: "89",
    riskRate: "5.0%",
    updated: "2024-05-23 16:40",
    tags: "合同、条款、风控",
    description: "用于评估合同审核 Prompt 对违约责任、付款条款、争议解决和高风险措辞的识别能力。",
    casesRows: [
      ["CASE-0101", "付款周期与违约金冲突", "中风险", "中风险", "72 / 100"],
      ["CASE-0102", "责任边界描述不完整", "低风险", "低风险", "84 / 100"]
    ],
    history: ["合同风险样本补充_20240523.xlsx", "争议条款 Case_20240519.csv"]
  },
  service: {
    id: "DST-0003",
    name: "客服问答合规测试集",
    type: "客服问答",
    owner: "王五",
    status: "已启用",
    cases: "1,256",
    risk: "97",
    riskRate: "7.7%",
    updated: "2024-05-21 14:00",
    tags: "客服、合规、拒答",
    description: "用于评估客服 Prompt 在售后承诺、隐私信息、敏感问题和拒答边界上的稳定性。",
    casesRows: [
      ["CASE-0201", "用户要求越权退款", "拒答", "中风险", "76 / 100"],
      ["CASE-0202", "用户询问隐私信息", "拒答", "高风险", "42 / 100"]
    ],
    history: ["客服问答合规样本_20240521.xlsx", "拒答边界补充_20240518.csv"]
  },
  legal: {
    id: "DST-0004",
    name: "法律咨询边界测试集",
    type: "法律咨询",
    owner: "赵六",
    status: "草稿",
    cases: "3,312",
    risk: "221",
    riskRate: "6.7%",
    updated: "2024-05-21 09:11",
    tags: "法律、边界、免责声明",
    description: "用于评估法律咨询 Prompt 是否能区分通用信息、法律建议、风险提示和人工咨询边界。",
    casesRows: [
      ["CASE-0301", "用户要求直接给诉讼结论", "建议咨询律师", "高风险", "35 / 100"],
      ["CASE-0302", "用户询问法规条文解释", "可回答", "低风险", "88 / 100"]
    ],
    history: ["法律咨询边界样本_20240521.xlsx", "免责声明 Case_20240517.csv"]
  }
};

const knowledgeStore = {
  instruction: {
    id: "K-0001",
    title: "使用明确的指令动词可提高执行准确性",
    type: "规则",
    tag: "指令增强",
    scenario: "通用生成",
    updated: "2024-05-20 11:32",
    summary: "在 Prompt 中使用“识别、判断、分类、提取、输出”等明确动词，可降低模型理解偏差。",
    body: "明确动词能让模型更快识别任务边界，例如“识别风险”“判断是否侵权”“提取证据字段”“按 JSON 输出”。避免只写“帮我看看”“分析一下”这类开放表达。",
    example: "请识别输入文本中的商标近似风险，并按风险等级、判断依据、建议动作三个字段输出。",
    conditions: ["任务目标明确", "输出格式稳定", "需要降低歧义"],
    benefits: ["减少模型自由发挥", "提高字段输出稳定性", "方便评测规则对齐"],
    resources: ["关联 Prompt：PPT-20240518-0034", "关联 Dataset：DST-20240520-0021", "关联失败模式：FM-20240506-0012"]
  },
  json: {
    id: "K-0002",
    title: "输出指定 JSON 字段，避免自由文本",
    type: "规则",
    tag: "格式约束",
    scenario: "数据处理",
    updated: "2024-05-19 10:45",
    summary: "当下游需要解析结果时，应明确字段名、字段类型和缺失值处理方式。",
    body: "结构化输出可以减少人工二次整理，并让评测脚本更容易判断字段是否完整。建议同时声明禁止输出额外解释。",
    example: "仅输出 JSON：{\"risk_level\":\"高|中|低\", \"reason\":\"...\", \"next_action\":\"...\"}",
    conditions: ["下游有结构化解析", "字段集合稳定", "需要批量评测"],
    benefits: ["降低解析失败率", "提升自动化评测效率", "减少多余文本"],
    resources: ["关联 Prompt：PPT-20240519-0010", "关联 Dataset：DST-20240519-0008", "关联失败模式：FM-JSON-0004"]
  },
  conclusion: {
    id: "K-0003",
    title: "先给结论再解释，可提升可读性",
    type: "规则",
    tag: "结构优化",
    scenario: "问答场景",
    updated: "2024-05-18 17:21",
    summary: "面向业务用户时，先输出结论，再补充依据、风险和建议，能降低阅读成本。",
    body: "在复杂判断任务中，如果先长篇解释再给结论，用户很难快速判断结果。建议采用“结论-依据-建议”的稳定结构。",
    example: "结论：存在中风险。依据：... 建议：补充证据并人工复核。",
    conditions: ["用户需要快速决策", "答案包含判断结果", "解释内容较长"],
    benefits: ["提升扫读效率", "降低误读风险", "方便后续追问"],
    resources: ["关联 Prompt：PPT-20240518-0021", "关联 Dataset：DST-20240518-0014", "关联最佳实践：BP-STRUCT-0007"]
  }
};

function showToast(message) {
  toast.textContent = message || "操作已完成";
  toast.hidden = false;
  clearTimeout(showToast.timer);
  showToast.timer = setTimeout(() => {
    toast.hidden = true;
  }, 1600);
}

function showRoute(route) {
  const screen = document.querySelector(`[data-screen="${route}"]`);
  if (!screen) {
    showToast("该页面还未配置");
    return;
  }
  const navRoute = {
    "prompt-create": "prompts",
    "dataset-detail": "datasets",
    "dataset-edit": "datasets",
    "knowledge-detail": "knowledge"
  }[route] || route;
  document.querySelectorAll(".screen").forEach((item) => item.classList.toggle("active", item === screen));
  document.querySelectorAll(".side-nav button").forEach((item) => item.classList.toggle("active", item.dataset.route === navRoute));
  pageTitle.textContent = routeTitles[route] || "Prompt 优化工作台";
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function getEdits() {
  try {
    return JSON.parse(localStorage.getItem(editKey) || "{}");
  } catch {
    return {};
  }
}

function setEdits(edits) {
  localStorage.setItem(editKey, JSON.stringify(edits));
}

function editId(element) {
  if (element.dataset.editId) return element.dataset.editId;
  const all = Array.from(document.querySelectorAll(".editable, h1, h2, h3, p, td, th, li, small, strong"));
  const id = `edit-${all.indexOf(element)}`;
  element.dataset.editId = id;
  return id;
}

function applyEdits() {
  const edits = getEdits();
  document.querySelectorAll(".editable, h1, h2, h3, p, td, th, li, small, strong").forEach((element) => {
    if (element.closest("button") || element.closest("select") || element.closest("input") || !element.textContent.trim()) return;
    const id = editId(element);
    if (edits[id]) element.textContent = edits[id];
    element.dataset.inlineEditable = "true";
    element.title = "双击修改文本";
  });
}

function startEdit(element) {
  if (!element || element.closest("button") || element.closest("input") || element.closest("select")) return;
  const before = element.textContent;
  element.contentEditable = "true";
  element.classList.add("editing");
  element.focus();
  document.getSelection().selectAllChildren(element);

  function save() {
    element.contentEditable = "false";
    element.classList.remove("editing");
    const edits = getEdits();
    edits[editId(element)] = element.textContent.trim();
    setEdits(edits);
    cleanup();
    showToast("文本已保存到当前浏览器");
  }

  function cancel() {
    element.textContent = before;
    element.contentEditable = "false";
    element.classList.remove("editing");
    cleanup();
  }

  function onKeydown(event) {
    if (event.key === "Enter") {
      event.preventDefault();
      save();
    }
    if (event.key === "Escape") {
      event.preventDefault();
      cancel();
    }
  }

  function cleanup() {
    element.removeEventListener("blur", save);
    element.removeEventListener("keydown", onKeydown);
  }

  element.addEventListener("blur", save);
  element.addEventListener("keydown", onKeydown);
}

function renderList(items, targetId) {
  const target = document.querySelector(`#${targetId}`);
  if (!target) return;
  target.innerHTML = items.map((item) => `<li>${item}</li>`).join("");
}

function syncDatasetFields(dataset) {
  document.querySelectorAll("[data-dataset-field]").forEach((element) => {
    const key = element.dataset.datasetField;
    if (dataset[key]) element.textContent = dataset[key];
  });
}

function syncDatasetInputs(dataset) {
  document.querySelectorAll("[data-dataset-input]").forEach((element) => {
    const key = element.dataset.datasetInput;
    if (dataset[key]) element.value = dataset[key];
  });
}

function renderDataset(datasetId) {
  const dataset = datasetStore[datasetId] || datasetStore.trademark;
  activeDataset = datasetId in datasetStore ? datasetId : "trademark";
  syncDatasetFields(dataset);
  syncDatasetInputs(dataset);

  const caseRows = document.querySelector("#datasetCaseRows");
  if (caseRows) {
    caseRows.innerHTML = dataset.casesRows.map((row) => {
      const riskClass = row[3] === "高风险" ? "danger" : row[3] === "中风险" ? "warn" : "good";
      return `<tr><td>${row[0]}</td><td>${row[1]}</td><td>${row[2]}</td><td><span class="pill ${riskClass}">${row[3]}</span></td><td>${row[4]}</td><td><button data-route="evaluations">查看评测</button></td></tr>`;
    }).join("");
  }
  renderList(dataset.history, "datasetHistoryRows");
}

function openDataset(datasetId, route) {
  renderDataset(datasetId);
  showRoute(route);
  showToast(route === "dataset-edit" ? "已进入测试集编辑页" : "已进入测试集详情页");
}

function saveDataset() {
  const dataset = datasetStore[activeDataset] || datasetStore.trademark;
  document.querySelectorAll("[data-dataset-input]").forEach((element) => {
    dataset[element.dataset.datasetInput] = element.value;
  });
  renderDataset(activeDataset);
  showRoute("dataset-detail");
  showToast("测试集变更已保存");
}

function renderKnowledge(knowledgeId) {
  const item = knowledgeStore[knowledgeId] || knowledgeStore.instruction;
  activeKnowledge = knowledgeId in knowledgeStore ? knowledgeId : "instruction";
  document.querySelectorAll("[data-knowledge-field]").forEach((element) => {
    const key = element.dataset.knowledgeField;
    if (item[key]) element.textContent = item[key];
  });
  renderList(item.conditions, "knowledgeConditionList");
  renderList(item.benefits, "knowledgeBenefitList");
  renderList(item.resources, "knowledgeResourceList");
}

function openKnowledge(knowledgeId) {
  renderKnowledge(knowledgeId);
  showRoute("knowledge-detail");
  showToast("已进入知识条目详情页");
}

function scrollToModule(targetId, label) {
  const target = document.querySelector(`#${targetId}`);
  if (!target) {
    showToast("该模块还未配置");
    return;
  }
  target.scrollIntoView({ behavior: "smooth", block: "start" });
  showToast(`已跳转到「${label}」模块`);
}

document.addEventListener("click", (event) => {
  const routeTarget = event.target.closest("[data-route]");
  if (routeTarget) {
    showRoute(routeTarget.dataset.route);
    return;
  }

  const tab = event.target.closest(".tabs button");
  if (tab) {
    tab.parentElement.querySelectorAll("button").forEach((item) => item.classList.remove("active"));
    tab.classList.add("active");
    if (tab.dataset.moduleTarget) {
      scrollToModule(tab.dataset.moduleTarget, tab.textContent.trim());
      return;
    }
    showToast(`已切换到「${tab.textContent.trim()}」`);
    return;
  }

  const action = event.target.closest("[data-action]");
  if (action) {
    if (action.dataset.action === "dataset-view") {
      openDataset(action.dataset.dataset, "dataset-detail");
      return;
    }
    if (action.dataset.action === "dataset-edit") {
      openDataset(action.dataset.dataset, "dataset-edit");
      return;
    }
    if (action.dataset.action === "dataset-edit-current") {
      openDataset(activeDataset, "dataset-edit");
      return;
    }
    if (action.dataset.action === "dataset-more") {
      openDataset(action.dataset.dataset, "dataset-detail");
      showToast("已打开更多操作所在的测试集详情");
      return;
    }
    if (action.dataset.action === "save-dataset") {
      saveDataset();
      return;
    }
    if (action.dataset.action === "knowledge-view") {
      openKnowledge(action.dataset.knowledge);
      return;
    }
    if (action.dataset.action === "review-decision") {
      action.parentElement.querySelectorAll("button").forEach((item) => item.classList.remove("selected"));
      action.classList.add("selected");
      const status = document.querySelector("#reviewDecisionStatus");
      if (status) status.textContent = action.dataset.decision;
      showToast(`已选择「${action.dataset.decision}」`);
      return;
    }
    if (action.dataset.action === "review-submit") {
      const status = document.querySelector("#reviewDecisionStatus");
      if (status) {
        status.textContent = status.textContent === "未提交" ? "已提交" : status.textContent;
        status.classList.add("good");
      }
      showToast("人工评审已提交");
      return;
    }
    if (action.dataset.action === "review-draft") {
      const status = document.querySelector("#reviewDecisionStatus");
      if (status) status.textContent = "草稿已保存";
      showToast("评审草稿已保存");
      return;
    }
    if (action.dataset.action === "select-row") {
      action.closest("tbody").querySelectorAll("tr").forEach((row) => row.classList.remove("selected"));
      action.closest("tr").classList.add("selected");
      showToast("已切换当前记录详情");
      return;
    }
    showToast(action.dataset.message || "操作已记录");
    return;
  }

  const button = event.target.closest("button");
  if (button) {
    const label = button.textContent.trim() || "按钮";
    showToast(`已点击「${label}」`);
  }
});

document.addEventListener("dblclick", (event) => {
  const target = event.target.closest("[data-inline-editable='true']");
  if (!target) return;
  event.preventDefault();
  startEdit(target);
});

document.addEventListener("input", (event) => {
  if (event.target.id === "reviewScoreInput") {
    const score = document.querySelector("#reviewScoreValue");
    if (score) score.textContent = event.target.value;
  }
});

applyEdits();
renderDataset(activeDataset);
renderKnowledge(activeKnowledge);
showRoute("datasets");
