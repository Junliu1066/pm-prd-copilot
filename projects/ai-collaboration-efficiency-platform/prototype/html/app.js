const screenMeta = {
  dashboard: {
    title: "Dashboard 工作台",
    breadcrumb: "首页 / Dashboard 工作台",
  },
  "task-center": {
    title: "任务中心 / 新建任务",
    breadcrumb: "首页 / 任务中心",
  },
  "skill-run": {
    title: "Skill 调用 / 结果预览",
    breadcrumb: "首页 / 任务中心 / Skill 调用",
  },
  "review-center": {
    title: "Review 多人评审中心",
    breadcrumb: "首页 / Review 评审",
  },
  efficiency: {
    title: "员工效率看板",
    breadcrumb: "首页 / 效率看板",
  },
  "skill-admin": {
    title: "Skill 管理与权重配置",
    breadcrumb: "首页 / Skill 管理",
  },
  calculation: {
    title: "权重计算引擎",
    breadcrumb: "首页 / 权重计算",
  },
  knowledge: {
    title: "知识沉淀 / 组织资产库",
    breadcrumb: "首页 / 知识库",
  },
  reports: {
    title: "报表导出中心",
    breadcrumb: "首页 / 报表导出",
  },
  "risk-admin": {
    title: "权限与风控",
    breadcrumb: "首页 / 权限与风控",
  },
};

const contextMessages = {
  "dashboard-create": "来自 Dashboard 的新建任务",
  "pending-review": "筛选条件已设置为待 Review",
  "new-task": "已携带任务：生成月度经营分析报告",
  "submit-review": "已提交候选结果到 Review 队列",
  "from-top-create": "从顶部快捷入口发起任务",
  "report-agent": "已选择智能分析报告生成 Skill",
  "meeting-agent": "已选择会议纪要结构化 Skill",
  "contract-agent": "已选择合同风险初筛 Skill",
  "weight-guide": "已打开权重计算引擎口径",
};

const drawers = {
  evidence: {
    title: "贡献分证据链",
    body: "每条贡献分都保留任务 ID、Skill 版本、模型和 Prompt 版本、Review 记录、公式快照、权重来源、封顶结果和知识复用记录。",
  },
  knowledge: {
    title: "知识沉淀规则",
    body: "只有通过 Review 或满足低风险自动通过规则的结果可以沉淀。P0 拦截和未通过 Review 的高风险内容不得进入知识库。",
  },
};

function showToast(message) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(showToast.timer);
  showToast.timer = setTimeout(() => toast.classList.remove("show"), 2200);
}

function showScreen(screenId, context) {
  const target = document.querySelector(`[data-screen="${screenId}"]`);
  if (!target) return;

  document.querySelectorAll("[data-screen]").forEach((screen) => {
    screen.classList.toggle("active", screen === target);
  });

  document.querySelectorAll(".nav-item").forEach((item) => {
    item.classList.toggle("active", item.dataset.navTarget === screenId);
  });

  const meta = screenMeta[screenId];
  if (meta) {
    document.getElementById("pageTitle").textContent = meta.title;
    document.getElementById("breadcrumb").textContent = meta.breadcrumb;
  }

  if (context && contextMessages[context]) {
    showToast(contextMessages[context]);
  }
}

function openDrawer(type) {
  const content = drawers[type] || drawers.evidence;
  document.getElementById("drawerTitle").textContent = content.title;
  document.getElementById("drawerBody").textContent = content.body;
  document.getElementById("contextDrawer").classList.add("open");
  document.getElementById("contextDrawer").setAttribute("aria-hidden", "false");
}

function closeDrawer() {
  document.getElementById("contextDrawer").classList.remove("open");
  document.getElementById("contextDrawer").setAttribute("aria-hidden", "true");
}

function openModal(id) {
  const modal = document.getElementById(id);
  if (!modal) return;
  modal.classList.add("open");
  modal.setAttribute("aria-hidden", "false");
}

function closeModal() {
  document.querySelectorAll(".modal.open").forEach((modal) => {
    modal.classList.remove("open");
    modal.setAttribute("aria-hidden", "true");
  });
}

function runSkill() {
  const runState = document.getElementById("runState");
  runState.innerHTML = "<strong>处理中...</strong><p>正在读取输入材料、调用 Skill，并生成候选结果。</p>";
  showToast("Skill 已开始处理");
  setTimeout(() => {
    runState.innerHTML = "<strong>候选结果已生成</strong><p>系统识别 3 个经营异常、2 个预算偏差和 4 条后续行动项。输出结果尚未计分，需提交 Review。</p>";
    showToast("候选结果已生成，等待提交 Review");
  }, 900);
}

function approveReview() {
  const history = document.getElementById("reviewHistory");
  const row = document.createElement("tr");
  row.innerHTML = "<td>当前评审人</td><td>已通过</td><td>88</td><td>刚刚</td><td>通过并建议沉淀为知识资产</td>";
  history.prepend(row);
  showToast("Review 已通过，贡献分进入待入账队列");
  setTimeout(() => showScreen("efficiency", "review-approved"), 700);
}

function returnReview() {
  const comment = document.getElementById("reviewComment").value.trim();
  if (!comment) {
    showToast("退回必须填写评审意见");
    return;
  }
  showToast("已退回给提交人，任务状态变为被退回");
}

function recheckReview() {
  showToast("已发起复审，追加一名评审人");
}

function exportReport() {
  showToast("导出任务已创建，报表导出动作已写入审计日志");
  setTimeout(() => showScreen("risk-admin", "audit-export"), 900);
}

function confirmRisk() {
  closeModal();
  showToast("高风险配置已二次确认并写入审计日志");
}

function saveDraft() {
  showToast("草稿已保存，未进入贡献统计");
}

function enableInlineEditing() {
  document.querySelectorAll("[data-inline-editable]").forEach((node) => {
    node.title = "双击可编辑，Enter 保存，Esc 取消";
    node.addEventListener("dblclick", () => {
      const original = node.textContent;
      node.contentEditable = "true";
      node.classList.add("editing");
      node.focus();

      function finish(save) {
        node.contentEditable = "false";
        node.classList.remove("editing");
        if (!save) node.textContent = original;
        node.removeEventListener("keydown", onKeydown);
        node.removeEventListener("blur", onBlur);
      }

      function onKeydown(event) {
        if (event.key === "Enter") {
          event.preventDefault();
          finish(true);
          showToast("文案已更新");
        }
        if (event.key === "Escape") {
          finish(false);
        }
      }

      function onBlur() {
        finish(true);
      }

      node.addEventListener("keydown", onKeydown);
      node.addEventListener("blur", onBlur);
    });
  });
}

document.addEventListener("click", (event) => {
  const navTarget = event.target.closest("[data-nav-target]");
  if (navTarget) {
    showScreen(navTarget.dataset.navTarget, navTarget.dataset.context);
    return;
  }

  const rowTarget = event.target.closest("[data-row-target]");
  if (rowTarget) {
    showScreen(rowTarget.dataset.rowTarget);
    return;
  }

  const actionTarget = event.target.closest("[data-action]");
  if (!actionTarget) return;

  const action = actionTarget.dataset.action;
  if (action === "toast") showToast(actionTarget.dataset.message || "操作已记录");
  if (action === "save-draft") saveDraft();
  if (action === "run-skill") runSkill();
  if (action === "review-approve") approveReview();
  if (action === "review-return") returnReview();
  if (action === "review-recheck") recheckReview();
  if (action === "export-report") exportReport();
  if (action === "open-drawer") openDrawer(actionTarget.dataset.drawer);
  if (action === "close-drawer") closeDrawer();
  if (action === "open-modal") openModal(actionTarget.dataset.modal);
  if (action === "close-modal") closeModal();
  if (action === "confirm-risk") confirmRisk();
  if (action === "select-review") showToast("已切换评审任务：" + actionTarget.dataset.review);
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeDrawer();
    closeModal();
  }
});

document.getElementById("globalSearch").addEventListener("input", (event) => {
  const value = event.target.value.trim();
  if (value.length >= 2) showToast(`正在筛选：${value}`);
});

enableInlineEditing();
