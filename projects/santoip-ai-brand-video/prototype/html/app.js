(function () {
  const storagePrefix = "santoip-prototype-edit:";
  const screens = Array.from(document.querySelectorAll(".screen[data-screen]"));
  const modal = document.getElementById("claimModal");
  const toast = document.getElementById("toast");
  const progress = document.getElementById("generateProgress");
  const percent = document.getElementById("generatePercent");
  const historyStack = [];

  const screenMeta = {
    "lead-detail": { mode: "customer", back: "返回线索列表", backTarget: "admin-leads" },
    "brand-create": { mode: "customer", back: "返回", backTarget: "case-gallery" },
    generating: { mode: "customer", back: "返回填写", backTarget: "brand-create" },
    result: { mode: "customer", back: "返回填写", backTarget: "brand-create" },
    "case-gallery": { mode: "customer", back: "返回", backTarget: "brand-create" },
    "admin-leads": { mode: "admin", back: "返回前台", backTarget: "lead-detail" }
  };

  function currentScreenId() {
    const active = document.querySelector(".screen.active");
    return active ? active.dataset.screen : "lead-detail";
  }

  function showToast(message) {
    toast.textContent = message || "操作已完成";
    toast.classList.add("show");
    clearTimeout(showToast.timer);
    showToast.timer = setTimeout(() => toast.classList.remove("show"), 1800);
  }

  function updateNav(target) {
    document.querySelectorAll(".nav-item").forEach((item) => {
      item.classList.toggle("active", item.dataset.navTarget === target);
    });
  }

  function updateTopbar(target) {
    const meta = screenMeta[target] || screenMeta["lead-detail"];
    document.body.dataset.mode = meta.mode;
    const back = document.querySelector(".back-control");
    if (back) {
      back.textContent = "← " + meta.back;
      back.dataset.backTarget = meta.backTarget;
    }
    const role = document.querySelector(".role-copy");
    if (role) role.textContent = meta.mode === "admin" ? "超级管理员" : "创业者";
  }

  function navigate(target, options = {}) {
    const next = document.querySelector(`.screen[data-screen="${target}"]`);
    if (!next) {
      showToast("目标页面尚未纳入原型");
      return;
    }
    const current = currentScreenId();
    if (!options.replace && current !== target) historyStack.push(current);
    screens.forEach((screen) => screen.classList.toggle("active", screen === next));
    updateTopbar(target);
    updateNav(target);
    document.querySelector(".workspace").scrollTo({ top: 0, behavior: "smooth" });
    if (target === "generating") startProgress();
  }

  function goBack() {
    const active = currentScreenId();
    const meta = screenMeta[active];
    const target = historyStack.pop() || (meta && meta.backTarget) || "lead-detail";
    navigate(target, { replace: true });
  }

  function startProgress() {
    let value = 38;
    progress.style.width = value + "%";
    percent.textContent = value + "%";
    clearInterval(startProgress.timer);
    startProgress.timer = setInterval(() => {
      value = Math.min(65, value + 3);
      progress.style.width = value + "%";
      percent.textContent = value + "%";
      if (value >= 65) clearInterval(startProgress.timer);
    }, 180);
  }

  function openModal() {
    modal.classList.add("open");
    modal.setAttribute("aria-hidden", "false");
  }

  function closeModal() {
    modal.classList.remove("open");
    modal.setAttribute("aria-hidden", "true");
  }

  function startGenerate() {
    const brandName = document.getElementById("brandName");
    const industry = document.getElementById("industry");
    const desc = document.getElementById("brandDesc");
    if (brandName && !brandName.value.trim()) brandName.value = "星屿茶研";
    if (industry && industry.selectedIndex === 0) industry.selectedIndex = 1;
    if (desc && !desc.value.trim()) {
      desc.value = "以原叶鲜奶茶为主，搭配新中式茶点，注重健康与东方美学体验。";
    }
    showToast("品牌信息已进入生成流程");
    navigate("generating");
  }

  function saveFollow() {
    const note = document.getElementById("followNote");
    const status = document.getElementById("followStatus");
    const timeline = document.querySelector(".timeline");
    const text = note && note.value.trim() ? note.value.trim() : "已电话沟通，客户希望先查看完整风险报告后再决定。";
    const item = document.createElement("div");
    item.className = "timeline-card";
    item.innerHTML = `<strong class="editable">人工跟进记录</strong><span class="editable">${new Date().toLocaleString("zh-CN")}</span><small class="editable">${status.value}：${text}</small>`;
    timeline.appendChild(item);
    note.value = "";
    makeEditable(item.querySelectorAll(".editable"));
    showToast("跟进记录已保存");
  }

  function assignAdvisor() {
    const status = document.getElementById("followStatus");
    if (status) status.value = "跟进中";
    showToast("已分配知识产权顾问，线索状态更新为跟进中");
  }

  function makeEditable(nodes) {
    Array.from(nodes).forEach((node, index) => {
      if (!node.dataset.editId) {
        const base = node.textContent.trim().slice(0, 16).replace(/\s+/g, "-") || "copy";
        node.dataset.editId = base + "-" + index + "-" + Array.from(document.querySelectorAll(".editable")).indexOf(node);
      }
      const key = storagePrefix + node.dataset.editId;
      const saved = localStorage.getItem(key);
      if (saved !== null) node.textContent = saved;

      node.addEventListener("dblclick", (event) => {
        event.stopPropagation();
        if (node.closest("button") || node.closest("input") || node.closest("textarea") || node.closest("select")) return;
        const original = node.textContent;
        node.contentEditable = "true";
        node.classList.add("editing");
        node.focus();
        document.execCommand("selectAll", false, null);

        function save() {
          node.contentEditable = "false";
          node.classList.remove("editing");
          localStorage.setItem(key, node.textContent.trim());
          cleanup();
        }

        function cancel() {
          node.textContent = original;
          node.contentEditable = "false";
          node.classList.remove("editing");
          cleanup();
        }

        function onKeydown(keyEvent) {
          if (keyEvent.key === "Enter") {
            keyEvent.preventDefault();
            save();
          }
          if (keyEvent.key === "Escape") {
            keyEvent.preventDefault();
            cancel();
          }
        }

        function cleanup() {
          node.removeEventListener("blur", save);
          node.removeEventListener("keydown", onKeydown);
        }

        node.addEventListener("blur", save);
        node.addEventListener("keydown", onKeydown);
      });
    });
  }

  document.addEventListener("click", (event) => {
    const nav = event.target.closest("[data-nav-target]");
    if (nav) {
      navigate(nav.dataset.navTarget);
      return;
    }

    const actionNode = event.target.closest("[data-action]");
    if (!actionNode) return;
    const action = actionNode.dataset.action;

    if (action === "back") goBack();
    if (action === "toast") showToast(actionNode.dataset.message);
    if (action === "open-modal") openModal();
    if (action === "close-modal") closeModal();
    if (action === "claim-submit") {
      closeModal();
      showToast("已提交，完整报告与顾问服务已解锁");
    }
    if (action === "start-generate") startGenerate();
    if (action === "save-follow") saveFollow();
    if (action === "assign-advisor") assignAdvisor();
    if (action === "toggle-admin") {
      navigate(document.body.dataset.mode === "admin" ? "lead-detail" : "admin-leads");
    }
  });

  document.addEventListener("click", (event) => {
    const chip = event.target.closest("[data-chip-group] .chip");
    if (!chip) return;
    chip.classList.toggle("selected");
  });

  document.addEventListener("click", (event) => {
    const segment = event.target.closest(".segmented button");
    if (!segment) return;
    segment.parentElement.querySelectorAll("button").forEach((button) => button.classList.remove("selected"));
    segment.classList.add("selected");
  });

  document.addEventListener("click", (event) => {
    const tab = event.target.closest(".tab-row button");
    if (!tab) return;
    tab.parentElement.querySelectorAll("button").forEach((button) => button.classList.remove("selected"));
    tab.classList.add("selected");
    showToast("已切换模块视图");
  });

  document.addEventListener("input", (event) => {
    const field = event.target;
    if (!(field instanceof HTMLTextAreaElement)) return;
    const counter = field.parentElement && field.parentElement.querySelector(".counter");
    if (counter) counter.textContent = `${field.value.length} / ${field.maxLength || 300}`;
  });

  modal.addEventListener("click", (event) => {
    if (event.target === modal) closeModal();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && modal.classList.contains("open")) closeModal();
  });

  makeEditable(document.querySelectorAll(".editable"));
  updateTopbar("lead-detail");
  updateNav("lead-detail");
})();
