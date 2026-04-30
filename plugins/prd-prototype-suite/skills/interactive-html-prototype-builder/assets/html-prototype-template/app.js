const screens = Array.from(document.querySelectorAll("[data-screen]"));
const toast = document.querySelector("[data-toast]");
const modalBackdrop = document.querySelector("[data-modal-backdrop]");

function showScreen(screenId) {
  screens.forEach((screen) => {
    screen.classList.toggle("is-active", screen.dataset.screen === screenId);
  });
}

function showToast(message) {
  if (!toast) return;
  toast.textContent = message;
  toast.hidden = false;
  window.clearTimeout(showToast.timeout);
  showToast.timeout = window.setTimeout(() => {
    toast.hidden = true;
  }, 1800);
}

function openModal() {
  if (modalBackdrop) modalBackdrop.hidden = false;
}

function closeModal() {
  if (modalBackdrop) modalBackdrop.hidden = true;
}

function activateTab(tabId) {
  document.querySelectorAll("[data-action='tab']").forEach((tab) => {
    tab.classList.toggle("is-active", tab.dataset.tab === tabId);
  });
  document.querySelectorAll("[data-tab-panel]").forEach((panel) => {
    panel.classList.toggle("is-active", panel.dataset.tabPanel === tabId);
  });
}

document.addEventListener("click", (event) => {
  const navButton = event.target.closest("[data-nav-target]");
  if (navButton) {
    showScreen(navButton.dataset.navTarget);
    return;
  }

  const actionButton = event.target.closest("[data-action]");
  if (!actionButton) return;

  const { action, message, tab } = actionButton.dataset;
  if (action === "open-modal") openModal();
  if (action === "close-modal") closeModal();
  if (action === "toast") showToast(message || "操作已完成");
  if (action === "tab") activateTab(tab);
});

if (modalBackdrop) {
  modalBackdrop.addEventListener("click", (event) => {
    if (event.target === modalBackdrop) closeModal();
  });
}
