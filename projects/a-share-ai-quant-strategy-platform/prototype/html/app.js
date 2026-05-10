const routes = [
  { id: "home", label: "首页", icon: "首", title: "首页", subtitle: "A股 AI 量化策略研究平台" },
  { id: "market", label: "市场温度", icon: "温", title: "市场温度计", subtitle: "2026-05-04 16:20 更新" },
  { id: "strategy", label: "策略", icon: "策", title: "策略列表", subtitle: "筛选、排序、回测入口" },
  { id: "arena", label: "竞技场", icon: "竞", title: "策略竞技场 S1", subtitle: "匿名仿真对决" },
  { id: "member", label: "积分", icon: "积", title: "积分中心", subtitle: "充值、赠送、消耗规则" },
  { id: "profile", label: "我的", icon: "我", title: "我的账户", subtitle: "积分、报告、关注策略" },
  { id: "strategyDetail", label: "策略详情", icon: "详", title: "策略详情", subtitle: "逻辑、曲线、适用行情" },
  { id: "backtest", label: "回测报告", icon: "测", title: "回测报告", subtitle: "完整指标与风险解释" },
  { id: "ai", label: "AI助手", icon: "AI", title: "AI策略助手", subtitle: "只解释研究信息" },
  { id: "weekly", label: "策略周报", icon: "周", title: "每周策略报告", subtitle: "市场回顾与风险提醒" },
  { id: "risk", label: "风险提示", icon: "险", title: "风险提示", subtitle: "合规边界与确认" },
  { id: "login", label: "登录注册", icon: "登", title: "登录 / 注册", subtitle: "微信授权与手机绑定" },
  { id: "ranking", label: "排行榜", icon: "榜", title: "竞技场排行榜", subtitle: "综合指标每日更新" },
  { id: "battle", label: "1v1对决", icon: "VS", title: "1v1 策略对决", subtitle: "同场景收益比较" },
  { id: "audience", label: "观察解锁", icon: "票", title: "观察内容解锁", subtitle: "用积分查看匿名表现" },
  { id: "arenaRules", label: "赛季规则", icon: "规", title: "S1 赛季规则", subtitle: "统一规则与风控口径" },
  { id: "signup", label: "选手报名", icon: "报", title: "选手报名", subtitle: "昵称、皮肤、积分报名" },
  { id: "player", label: "选手档案", icon: "档", title: "选手档案", subtitle: "匿名策略表现档案" },
  { id: "admin", label: "运营后台", icon: "审", title: "运营后台 / 内容审核", subtitle: "策略、报告、合规词命中" }
];

const primaryRouteIds = ["home", "market", "strategy", "arena", "member"];
const routeMap = new Map(routes.map((route) => [route.id, route]));

const strategies = [
  {
    name: "沪深300趋势增强",
    code: "沪",
    type: "趋势策略",
    market: "指数 / 趋势增强",
    annual: "18.42%",
    drawdown: "-12.37%",
    sharpe: "1.36",
    risk: "中",
    access: "积分解锁",
    status: "已验证",
    desc: "用趋势确认和回撤控制过滤弱行情，适合中高温市场观察。"
  },
  {
    name: "ETF行业轮动",
    code: "E",
    type: "轮动策略",
    market: "ETF / 行业轮动",
    annual: "15.76%",
    drawdown: "-10.21%",
    sharpe: "1.21",
    risk: "中",
    access: "积分解锁",
    status: "周更",
    desc: "跟踪行业强弱切换，重点观察轮动持续性和拥挤度。"
  },
  {
    name: "红利低波防守",
    code: "红",
    type: "防守策略",
    market: "股票 / 低波红利",
    annual: "12.03%",
    drawdown: "-6.48%",
    sharpe: "1.44",
    risk: "低",
    access: "免费试看",
    status: "稳健",
    desc: "偏防守配置，适合低温或震荡行情下的策略研究。"
  },
  {
    name: "中证500强弱轮动",
    code: "500",
    type: "轮动策略",
    market: "指数 / 强弱轮动",
    annual: "17.31%",
    drawdown: "-13.95%",
    sharpe: "1.09",
    risk: "中",
    access: "积分解锁",
    status: "观察",
    desc: "用强弱相对排名切换持仓方向，波动较沪深300更高。"
  }
];

const arenaRows = [
  { rank: 1, id: "A7", title: "稳健平衡派", value: "21.37%", dd: "-8.41%", sharpe: "1.68", stability: "0.62", level: "王者 I", sub: "已解锁", badge: "gold" },
  { rank: 2, id: "K3", title: "趋势追随者", value: "17.84%", dd: "-10.27%", sharpe: "1.42", stability: "0.71", level: "钻石 II", sub: "积分解锁", badge: "silver" },
  { rank: 3, id: "M9", title: "量化猎手", value: "16.25%", dd: "-9.16%", sharpe: "1.36", stability: "0.68", level: "钻石 III", sub: "积分解锁", badge: "bronze" },
  { rank: 4, id: "Q5", title: "价值发现者", value: "14.38%", dd: "-7.93%", sharpe: "1.21", stability: "0.60", level: "铂金 I", sub: "积分解锁", badge: "blue" },
  { rank: 5, id: "T2", title: "多因子驱动", value: "13.02%", dd: "-11.12%", sharpe: "1.09", stability: "0.77", level: "铂金 II", sub: "积分解锁", badge: "blue" },
  { rank: 6, id: "L8", title: "红利守护者", value: "12.11%", dd: "-6.88%", sharpe: "1.08", stability: "0.58", level: "黄金 I", sub: "积分解锁", badge: "green" },
  { rank: 7, id: "J6", title: "波段捕手", value: "11.07%", dd: "-9.45%", sharpe: "1.01", stability: "0.73", level: "黄金 II", sub: "积分解锁", badge: "green" },
  { rank: 8, id: "P1", title: "事件驱动派", value: "9.64%", dd: "-13.67%", sharpe: "0.82", stability: "0.88", level: "黄金 III", sub: "积分解锁", badge: "green" }
];

const ranks = {
  comprehensive: arenaRows.slice(0, 3).map(({ rank, id, value, dd, sharpe, level }) => ({ rank, id, value: `+${value}`, dd, sharpe, level })),
  day: [
    { rank: 1, id: "A7", value: "+3.24%", dd: "-0.72%", sharpe: "1.10", level: "王者 I" },
    { rank: 2, id: "Q5", value: "+2.91%", dd: "-1.03%", sharpe: "0.98", level: "铂金 I" },
    { rank: 3, id: "L8", value: "+2.44%", dd: "-0.88%", sharpe: "1.02", level: "黄金 I" }
  ],
  horse: [
    { rank: 1, id: "K3", value: "+8.76%", dd: "-2.47%", sharpe: "1.21", level: "钻石 II" },
    { rank: 2, id: "T2", value: "+7.20%", dd: "-3.11%", sharpe: "0.92", level: "铂金 II" },
    { rank: 3, id: "J6", value: "+6.48%", dd: "-1.96%", sharpe: "1.04", level: "黄金 II" }
  ],
  risk: [
    { rank: 1, id: "L8", value: "+12.11%", dd: "-6.88%", sharpe: "1.08", level: "黄金 I" },
    { rank: 2, id: "Q5", value: "+14.38%", dd: "-7.93%", sharpe: "1.21", level: "铂金 I" },
    { rank: 3, id: "A7", value: "+21.37%", dd: "-8.41%", sharpe: "1.68", level: "王者 I" }
  ],
  sharpe: [
    { rank: 1, id: "A7", value: "+21.37%", dd: "-8.41%", sharpe: "1.68", level: "王者 I" },
    { rank: 2, id: "K3", value: "+17.84%", dd: "-10.27%", sharpe: "1.42", level: "钻石 II" },
    { rank: 3, id: "M9", value: "+16.25%", dd: "-9.16%", sharpe: "1.36", level: "钻石 III" }
  ]
};

const featureItems = [
  { title: "市场温度计", desc: "把握市场节奏", icon: "thermo", route: "market" },
  { title: "回测报告", desc: "多维回测分析", icon: "chart", route: "backtest" },
  { title: "AI解读", desc: "智能策略解释", icon: "ai", route: "ai" },
  { title: "风险评分", desc: "量化风险评估", icon: "shield", route: "risk" }
];

const app = document.querySelector("#app");
const tabbar = document.querySelector("#tabbar");
const sideNav = document.querySelector("#sideNav");
const pageTitle = document.querySelector("#pageTitle");
const pageSubtitle = document.querySelector("#pageSubtitle");
const searchbar = document.querySelector("#searchbar");
const backButton = document.querySelector("#backButton");
const modal = document.querySelector("#modal");
const modalContent = document.querySelector("#modalContent");
const modalClose = document.querySelector("#modalClose");

let currentRoute = "home";
let currentRank = "comprehensive";

function navigate(route) {
  currentRoute = routeMap.has(route) ? route : "home";
  const meta = routeMap.get(currentRoute) || routes[0];
  pageTitle.textContent = meta.title;
  pageSubtitle.textContent = meta.subtitle;
  searchbar.style.display = currentRoute === "home" || currentRoute === "strategy" ? "flex" : "none";
  backButton.style.visibility = currentRoute === "home" ? "hidden" : "visible";
  renderNav();
  render();
  app.scrollTop = 0;
}

function renderNav() {
  tabbar.innerHTML = primaryRouteIds.map((id) => {
    const route = routeMap.get(id);
    return `
      <button class="${currentRoute === route.id ? "active" : ""}" data-route="${route.id}">
        <span class="tab-icon">${route.icon}</span>
        <span>${route.label}</span>
      </button>
    `;
  }).join("");

  sideNav.innerHTML = routes.map((route) => `
    <button class="${currentRoute === route.id ? "active" : ""}" data-route="${route.id}">
      <span>${route.label}</span>
      <span>${route.id === "arena" ? "P1" : route.id === "admin" ? "Web" : ""}</span>
    </button>
  `).join("");
}

function chartSvg(kind = "up", label) {
  const red = kind === "drawdown"
    ? "M0 34 C44 80, 88 30, 134 66 C190 108, 232 48, 286 88 C336 126, 382 72, 440 110"
    : "M0 132 C48 112, 72 134, 112 94 C160 48, 196 76, 246 42 C310 4, 346 58, 440 18";
  const grey = kind === "drawdown"
    ? "M0 54 C55 118, 102 74, 160 120 C212 150, 256 82, 320 136 C362 164, 404 132, 440 146"
    : "M0 142 C72 128, 106 150, 166 108 C210 76, 248 106, 302 74 C350 48, 386 86, 440 60";
  return `
    <div class="chart">
      <span class="chart-label">${label || (kind === "drawdown" ? "最大回撤曲线" : "策略 vs 基准收益曲线")}</span>
      <svg viewBox="0 0 440 180" preserveAspectRatio="none" aria-hidden="true">
        <path d="${grey}" fill="none" stroke="#9aa3b3" stroke-width="4" opacity=".75" />
        <path d="${red}" fill="none" stroke="${kind === "blue" ? "#2563eb" : "#e60012"}" stroke-width="4" />
      </svg>
    </div>
  `;
}

function featureIcon(type) {
  const icons = {
    thermo: `
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <path d="M21 8a5 5 0 0 1 10 0v18.8a12 12 0 1 1-10 0V8Z" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
        <path d="M26 30V14" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
        <circle cx="26" cy="36" r="5" fill="currentColor"/>
        <path d="M34 10h7M34 17h5M34 24h7" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
      </svg>
    `,
    chart: `
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <rect x="8" y="8" width="32" height="32" rx="6" fill="currentColor"/>
        <path d="M14 31l7-7 5 5 8-12" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    `,
    ai: `
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <rect x="8" y="8" width="32" height="28" rx="7" fill="currentColor"/>
        <path d="M17 36l-5 6v-8" fill="currentColor"/>
        <path d="M16 28l5-12h3l5 12M18 24h9M33 16v12" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    `,
    shield: `
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <path d="M24 6l16 6v11c0 10-6.5 16.5-16 20C14.5 39.5 8 33 8 23V12l16-6Z" fill="currentColor"/>
        <path d="M17 24l5 5 10-12" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    `,
    ticket: `
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <path d="M9 15a5 5 0 0 1 5-5h20a5 5 0 0 1 5 5v4a5 5 0 0 0 0 10v4a5 5 0 0 1-5 5H14a5 5 0 0 1-5-5v-4a5 5 0 0 0 0-10v-4Z" fill="currentColor"/>
        <path d="M23 16v4M23 28v4" stroke="#fff" stroke-width="3" stroke-linecap="round"/>
      </svg>
    `,
    trophy: `
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <path d="M15 8h18v7h6c0 8-4 12-10 13a10 10 0 0 1-3 2v5h7v5H15v-5h7v-5a10 10 0 0 1-3-2C13 27 9 23 9 15h6V8Z" fill="currentColor"/>
        <path d="M18 14h12" stroke="#fff" stroke-width="3" stroke-linecap="round"/>
      </svg>
    `
  };
  return icons[type] || icons.chart;
}

function renderFeatureStrip() {
  return `
    <section class="section feature-strip" aria-label="核心功能入口">
      ${featureItems.map((item) => `
        <article class="feature" data-route="${item.route}">
          <span class="feature-icon">${featureIcon(item.icon)}</span>
          <span class="feature-copy">
            <strong>${item.title}</strong>
            <small>${item.desc}</small>
          </span>
        </article>
      `).join("")}
    </section>
  `;
}

function renderHero({ title, red = "", desc, badges = [], cta = [], icon = "chart", dark = false }) {
  return `
    <section class="${dark ? "arena-hero hero-visual dark" : "hero hero-visual"}">
      <div class="hero-copy">
        <h1>${title}${red ? ` <span>${red}</span>` : ""}</h1>
        <p>${desc}</p>
        ${badges.length ? `<div class="pill-row">${badges.map((badge) => `<span class="pill ${badge[1] || "red"}">${badge[0]}</span>`).join("")}</div>` : ""}
        ${cta.length ? `<div class="button-row">${cta.map((item) => `<button class="${item[2] || "button"}" data-route="${item[1]}">${item[0]}</button>`).join("")}</div>` : ""}
      </div>
      <div class="hero-object">
        <span>${featureIcon(icon)}</span>
      </div>
    </section>
  `;
}

function metricStrip(items) {
  return `
    <section class="section metric-strip">
      ${items.map((item) => `
        <article>
          <span>${item[0]}</span>
          <b class="${item[2] || ""}">${item[1]}</b>
          ${item[3] ? `<small>${item[3]}</small>` : ""}
        </article>
      `).join("")}
    </section>
  `;
}

function renderStrategyCards(items, mode = "grid") {
  return `<div class="${mode === "list" ? "strategy-list" : "strategy-grid"}">${items.map((item) => `
    <article class="${mode === "list" ? "strategy-list-card" : "strategy-card"}">
      <div class="card-head">
        <span class="mini-icon">${item.code}</span>
        <div>
          <span class="pill red">${item.type}</span>
          <h3>${item.name}</h3>
          <p class="caption">${item.market}</p>
        </div>
        <span class="status-dot">${item.status}</span>
      </div>
      <p class="caption">${item.desc}</p>
      <div class="stat-line">
        <span class="stat"><small>历史年化收益</small><b>${item.annual}</b></span>
        <span class="stat negative"><small>最大回撤</small><b>${item.drawdown}</b></span>
      </div>
      <div class="meta-line">
        <span>夏普 ${item.sharpe}</span>
        <span>风险 ${item.risk}</span>
        <span>${item.access}</span>
      </div>
      <div class="button-row compact">
        <button class="button button-light" data-route="strategyDetail">查看详情</button>
        <button class="button button-ghost" data-route="backtest">回测报告</button>
      </div>
    </article>
  `).join("")}</div>`;
}

function renderRankList(type) {
  return ranks[type].map((item) => `
    <article class="rank-row">
      <span class="rank-medal">${item.rank}</span>
      <div>
        <strong>${item.id}</strong>
        <div class="rank-meta">最大回撤 ${item.dd}｜夏普 ${item.sharpe}｜${item.level}</div>
      </div>
      <span class="rank-value">${item.value}</span>
    </article>
  `).join("");
}

function renderRankingRows() {
  return `
    <section class="section rank-table">
      <div class="rank-table-head">
        <span>排名</span><span>参赛者</span><span>收益</span><span>最大回撤</span><span>夏普</span><span>段位</span><span>解锁</span>
      </div>
      ${arenaRows.map((row) => `
        <article class="rank-table-row">
          <span class="medal ${row.badge}">${row.rank <= 3 ? row.rank : row.rank}</span>
          <span class="competitor">
            <b>${row.id}</b>
            <small>${row.title}</small>
          </span>
          <span class="red-value">${row.value}</span>
          <span>${row.dd}</span>
          <span>${row.sharpe}</span>
          <span><i class="tier ${row.badge}"></i>${row.level}</span>
          <button class="button button-light small-button" data-route="audience">${row.sub}</button>
        </article>
      `).join("")}
    </section>
  `;
}

function renderHome() {
  return `
    ${renderHero({
      title: "A股",
      red: "AI 量化策略研究平台",
      desc: "用回测、风险指标和 AI 解读看懂策略，先理解市场，再研究策略。",
      icon: "chart",
      cta: [["免费查看市场温度", "market"], ["查看策略列表", "strategy", "button button-outline"]]
    })}

    ${renderFeatureStrip()}

    <section class="section">
      <div class="section-title">
        <h2>策略样例 <span class="info-dot">i</span></h2>
        <button data-route="strategy">更多策略 ›</button>
      </div>
      ${renderStrategyCards(strategies.slice(0, 2))}
    </section>

    <section class="section arena-banner">
      <h2>策略竞技场 S1</h2>
      <p>匿名仿真对决、赛季榜单、积分解锁观察、1v1 观战，不展示持仓和买卖信号。</p>
      <div class="button-row">
        <button class="button" data-route="arena">进入竞技场</button>
        <button class="button button-outline" data-route="ranking">查看排行榜</button>
      </div>
    </section>

    <section class="section trust-row">
      <div><strong>区分回测/模拟/实盘</strong><span class="caption">清晰标注，避免混淆</span></div>
      <div><strong>不承诺收益</strong><span class="caption">历史不代表未来</span></div>
      <div><strong>不喊单</strong><span class="caption">不做具体投资建议</span></div>
    </section>

    <section class="section">
      <div class="section-title"><h2>设计稿页面入口</h2><button data-route="admin">后台稿 ›</button></div>
      <div class="function-grid">
        ${[
          ["策略详情", "strategyDetail", "chart"],
          ["AI助手", "ai", "ai"],
          ["策略周报", "weekly", "ticket"],
          ["风险提示", "risk", "shield"],
          ["观察解锁", "audience", "ticket"],
          ["选手报名", "signup", "trophy"]
        ].map(([title, route, icon]) => `
          <button class="function-card" data-route="${route}">
            <span>${featureIcon(icon)}</span>
            <b>${title}</b>
          </button>
        `).join("")}
      </div>
    </section>
  `;
}

function renderMarket() {
  return `
    <section class="thermo-panel">
      <div class="gauge"><span>58</span></div>
      <div>
        <p class="eyebrow">今日结论</p>
        <h1 class="screen-title red-value">中性偏热</h1>
        <p class="caption">适合观察趋势与轮动策略。综合得分较昨日 +6，数据样本为全市场。</p>
        <div class="pill-row">
          <span class="pill red">综合 58/100</span>
          <span class="pill amber">较昨日 +6</span>
          <span class="pill blue">全市场</span>
        </div>
      </div>
    </section>

    <section class="section metric-grid">
      ${[
        ["市场情绪", "中性偏热", "情绪活跃度上升", "red"],
        ["趋势强度", "中性", "趋势动能一般", "amber"],
        ["赚钱效应", "偏热", "赚钱效应偏强", "red"],
        ["波动风险", "中性", "波动率处于中等", "blue"],
        ["行业轮动", "偏热", "轮动活跃度较高", "purple"],
        ["适合策略", "趋势/轮动", "更适合趋势与轮动", "green"]
      ].map(([title, value, desc, color]) => `<article class="metric"><span class="pill ${color}">${title}</span><b>${value}</b><small>${desc}</small></article>`).join("")}
    </section>

    <section class="section notice">
      <h3>为什么是这个状态 / 需要注意什么风险</h3>
      <p>市场情绪与赚钱效应偏强，资金活跃度提升；趋势动能一般，需要关注关键支撑位有效性；波动风险中等，突发事件可能带来短期扰动。</p>
    </section>

    <section class="section">
      <div class="section-title"><h2>适合关注的策略</h2><button data-route="strategy">查看全部策略 ›</button></div>
      ${renderStrategyCards(strategies.slice(0, 2))}
      <div class="button-row section">
        <button class="button" data-route="strategy">查看适合策略</button>
        <button class="button button-outline" data-route="weekly">查看每周策略周报</button>
      </div>
    </section>

    <p class="fineprint">本页内容仅供策略研究参考，不构成任何投资建议。历史业绩不代表未来表现，市场有风险。</p>
  `;
}

function renderStrategy() {
  return `
    <section class="section filter-card">
      <div class="section-title"><h2>策略筛选</h2><button data-route="risk">查看风险规则 ›</button></div>
      <div class="chip-grid">
        ${["全部市场", "沪深300", "ETF", "低回撤", "趋势", "轮动", "防守", "积分可看"].map((chip, index) => `<button class="${index === 0 ? "active" : ""}">${chip}</button>`).join("")}
      </div>
    </section>

    <section class="section">
      <div class="rank-tabs">
        ${["综合评分", "趋势", "轮动", "防守", "低回撤"].map((tab, index) => `<button class="${index === 0 ? "active" : ""}">${tab}</button>`).join("")}
      </div>
      ${renderStrategyCards(strategies, "list")}
    </section>

    <section class="section report-card">
      <div class="section-title"><h2>回测报告样例</h2><button data-route="backtest">完整报告 ›</button></div>
      <div class="rule-grid metric-grid">
        <div><span class="caption">回测区间</span><strong>2015-01-01 至 2025-04-30</strong></div>
        <div><span class="caption">初始资金</span><strong>虚拟资金 100 万</strong></div>
        <div><span class="caption">手续费</span><strong>万分之三</strong></div>
        <div><span class="caption">滑点</span><strong>万分之二</strong></div>
      </div>
      <div class="section dual-grid">${chartSvg("up")}${chartSvg("drawdown")}</div>
    </section>
  `;
}

function renderStrategyDetail() {
  const item = strategies[0];
  return `
    <section class="detail-header">
      <div class="card-head">
        <span class="mini-icon big">${item.code}</span>
        <div>
          <div class="pill-row">
            <span class="pill red">${item.type}</span>
            <span class="pill blue">指数增强</span>
            <span class="pill green">已验证</span>
          </div>
          <h1>${item.name}</h1>
          <p class="caption">历史回测 / 风险评分 / 适用行情 / AI 解读</p>
        </div>
      </div>
    </section>

    ${metricStrip([
      ["历史年化", item.annual, "red-value"],
      ["最大回撤", item.drawdown, "green"],
      ["夏普比率", item.sharpe],
      ["风险等级", "中"]
    ])}

    <section class="section chart-card">
      <div class="section-title">
        <h2>净值走势</h2>
        <div class="mini-tabs"><button class="active">1年</button><button>3年</button><button>全部</button></div>
      </div>
      ${chartSvg("up", "策略收益 / 沪深300基准")}
    </section>

    <section class="section info-stack">
      ${[
        ["策略逻辑", "趋势确认 + 波动过滤 + 回撤控制，避免在弱趋势阶段持续暴露。"],
        ["适用行情", "中性偏热、趋势延续、行业轮动活跃时更适合观察。"],
        ["失效场景", "震荡反复、单日极端波动、流动性收缩时可能发生连续回撤。"],
        ["回测口径", "统一手续费、滑点和数据切片，报告中区分回测、模拟与实盘。"]
      ].map(([title, desc]) => `<article class="info-card"><h3>${title}</h3><p>${desc}</p></article>`).join("")}
    </section>

    <section class="section bottom-cta">
      <button class="button" data-route="backtest">查看完整回测报告</button>
      <button class="button button-outline" data-route="member">积分解锁</button>
    </section>
    <p class="fineprint">仅供策略研究参考，不构成任何投资建议，不展示持仓、买卖点或实时交易信号。</p>
  `;
}

function renderBacktest() {
  return `
    ${renderHero({
      title: "沪深300趋势增强",
      red: "回测报告",
      desc: "展示参数口径、净值曲线、回撤曲线、年度/月度表现和极端行情表现。",
      icon: "chart",
      badges: [["简版报告", "red"], ["更新时间 2025-05-12", "blue"]]
    })}

    <section class="section parameter-grid">
      ${[
        ["回测区间", "2015-01-01 至 2025-04-30"],
        ["初始资金", "虚拟资金 100 万"],
        ["手续费", "万分之三"],
        ["滑点", "万分之二"],
        ["标的池", "沪深300成分股 + ETF"],
        ["调仓频率", "每周一次"]
      ].map(([k, v]) => `<article><span>${k}</span><b>${v}</b></article>`).join("")}
    </section>

    <section class="section dual-grid">${chartSvg("up")}${chartSvg("drawdown")}</section>

    <section class="section table-card compact-table">
      <table>
        <thead><tr><th>年份</th><th>策略</th><th>基准</th><th>最大回撤</th></tr></thead>
        <tbody>
          <tr><td>2024</td><td class="red-value">18.42%</td><td>12.03%</td><td>-8.42%</td></tr>
          <tr><td>2023</td><td>-6.21%</td><td>-11.38%</td><td>-10.37%</td></tr>
          <tr><td>2022</td><td>-9.84%</td><td>-21.63%</td><td>-12.37%</td></tr>
        </tbody>
      </table>
    </section>

    <section class="section report-grid">
      <article class="info-card"><h3>AI 解读</h3><p>策略收益主要来自趋势延续阶段，弱市中通过仓位控制降低回撤，但无法规避所有极端波动。</p></article>
      <article class="info-card"><h3>风险评分</h3><p>综合风险为中，最大风险来自趋势反复与轮动失效。</p></article>
      <article class="info-card"><h3>失效提醒</h3><p>连续缩量、风格急切换和黑天鹅事件可能使策略短期失效。</p></article>
    </section>

    <section class="section locked-banner">
      <div><strong>完整报告已锁定</strong><p class="caption">解锁月度收益表、极端行情回放和完整风险解释。</p></div>
      <button class="button" data-route="member">用 20 积分解锁</button>
    </section>
  `;
}

function renderArena() {
  const tabs = [
    ["comprehensive", "综合榜"],
    ["day", "今日涨幅 TOP"],
    ["horse", "本周黑马"],
    ["risk", "回撤警示"],
    ["sharpe", "夏普榜"]
  ];

  return `
    <section class="arena-hero hero-visual dark">
      <div class="hero-copy">
        <h1>策略竞技场 S1</h1>
        <p>匿名仿真对决 / 榜单排行 / 1v1 对决 / 积分观察</p>
        <div class="pill-row">
          <span class="pill red">第 2 周</span>
          <span class="pill amber">火热进行中</span>
          <span class="pill blue">统一虚拟资金 100 万</span>
        </div>
      </div>
      <div class="hero-object trophy-object"><span>${featureIcon("trophy")}</span></div>
    </section>

    <section class="section rule-grid metric-grid">
      ${["公平竞技|统一规则", "统一成本|佣金滑点透明", "匿名对决|策略ID隐藏", "风控限制|回撤熔断"].map((item) => {
        const [title, desc] = item.split("|");
        return `<article class="metric"><span class="pill red">${title}</span><b>${desc}</b></article>`;
      }).join("")}
    </section>

    <section class="section">
      <div class="rank-tabs">
        ${tabs.map(([id, label]) => `<button class="${currentRank === id ? "active" : ""}" data-rank="${id}">${label}</button>`).join("")}
      </div>
      <div id="rankList">${renderRankList(currentRank)}</div>
    </section>

    <section class="section podium">
      <article><span>2</span><b>K3</b><small>+17.84%</small></article>
      <article class="first"><span>1</span><b>A7</b><small>+21.37%</small></article>
      <article><span>3</span><b>M9</b><small>+16.25%</small></article>
    </section>

    <section class="section">
      <div class="section-title"><h2>今日看点</h2><button data-route="arenaRules">更多规则 ›</button></div>
      <div class="quick-grid">
        <article class="simple-card"><span class="pill red">今日涨幅 TOP</span><h3>A7 +3.24%</h3><p class="caption">今日收益领先，最大回撤 -0.72%</p></article>
        <article class="simple-card"><span class="pill amber">本周黑马</span><h3>K3 +8.76%</h3><p class="caption">本周收益跃升，波动需观察</p></article>
        <article class="simple-card"><span class="pill blue">稳健防守</span><h3>L8 -6.88%</h3><p class="caption">当前最大回撤最小</p></article>
        <article class="simple-card"><span class="pill green">路演摘要</span><h3>前五策略复盘</h3><p class="caption">讲逻辑，不透露代码和信号</p></article>
      </div>
    </section>

    <section class="section battle-panel">
      <div class="section-title"><h2>1v1 策略对决</h2><button data-route="battle">进入对决 ›</button></div>
      <p class="caption">同一市场环境、同一标的池、同一交易成本、同一时间窗。</p>
      <div class="battle-grid">
        <div><span class="pill red">A7</span><h3>收益 +3.2%</h3><p class="caption">最大回撤 -1.1%，夏普 1.4</p><div class="progress"><span style="width:56%"></span></div></div>
        <div><span class="pill blue">K3</span><h3>收益 +2.5%</h3><p class="caption">最大回撤 -0.6%，夏普 1.7</p><div class="progress blue"><span style="width:44%"></span></div></div>
      </div>
    </section>

    <section class="section bottom-cta">
      <button class="button" data-route="signup">申请参赛</button>
      <button class="button button-outline" data-route="audience">积分解锁观察</button>
    </section>
    <section class="section risk-box">策略竞技场为虚拟仿真环境，仅用于量化策略研究与展示，不构成任何投资建议。</section>
  `;
}

function renderRanking() {
  return `
    ${renderHero({
      title: "策略竞技场 S1",
      red: "排行榜",
      desc: "匿名仿真对决，排名每日更新。综合榜同时考虑收益、回撤、夏普和稳定性。",
      icon: "trophy",
      dark: true,
      badges: [["火热进行中", "red"], ["2024-06-01 至 2024-08-31", "blue"]]
    })}

    <section class="section sticky-tabs">
      <button class="active">综合榜</button><button>今日涨幅TOP</button><button>本周黑马</button><button>回撤警示</button><button>夏普榜</button>
    </section>

    <section class="section split-actions">
      <div class="segmented"><button class="active">总榜</button><button>分榜</button></div>
      <button class="button button-light" data-route="arenaRules">查看赛季规则 ›</button>
    </section>

    <section class="section alert-line">排名综合考虑收益、回撤、夏普、稳定性等多维指标，而非仅收益。</section>
    ${renderRankingRows()}
    <p class="fineprint">风险提示：本排行榜为模拟研究展示，不构成任何投资建议，投资有风险，入市需谨慎。</p>
  `;
}

function renderBattle() {
  return `
    ${renderHero({
      title: "A7 vs K3",
      red: "策略对决",
      desc: "两个匿名策略在同一市场环境、同一交易成本和同一时间窗内进行模拟表现比较。",
      icon: "trophy",
      badges: [["本周焦点战", "red"], ["观众可投票", "blue"]]
    })}

    <section class="section versus-card">
      <article class="battle-side red-side"><span>A7</span><h2>+3.24%</h2><p>稳健平衡派</p></article>
      <strong class="vs-mark">VS</strong>
      <article class="battle-side blue-side"><span>K3</span><h2>+2.58%</h2><p>趋势追随者</p></article>
    </section>

    <section class="section dual-grid">${chartSvg("up", "A7 净值曲线")}${chartSvg("blue", "K3 净值曲线")}</section>

    <section class="section comparison-strip">
      ${[
        ["收益", "+3.24%", "+2.58%"],
        ["最大回撤", "-1.10%", "-0.62%"],
        ["夏普", "1.40", "1.70"],
        ["投票", "56%", "44%"]
      ].map(([k, a, b]) => `<article><span>${k}</span><b>${a}</b><small>${b}</small></article>`).join("")}
    </section>

    <section class="section vote-row">
      <button class="button" data-action="voteBattle">投 A7</button>
      <button class="button button-outline" data-action="voteBattle">投 K3</button>
    </section>

    <section class="section comment-card">
      <h3>观众讨论</h3>
      <p>“A7 回撤控制更稳，但 K3 在趋势延续时爆发力更强。”</p>
      <p class="caption">讨论区不展示策略代码、持仓、买卖点或实时信号。</p>
    </section>
  `;
}

function renderArenaRules() {
  return `
    ${renderHero({
      title: "策略竞技场",
      red: "S1 赛季规则",
      desc: "统一资金、统一标的池、统一交易成本和统一风控口径，让排名可比较。",
      icon: "shield",
      badges: [["匿名制", "red"], ["综合评分", "blue"], ["月赛/赛季", "green"]]
    })}

    <section class="section rule-section">
      <h2>基础规则</h2>
      <div class="metric-grid">
        ${[
          ["初始资金", "统一虚拟资金 100 万"],
          ["标的池", "沪深300成分股 + ETF"],
          ["交易成本", "统一佣金与滑点"],
          ["操作要求", "每周至少一次有效操作"]
        ].map(([k, v]) => `<article class="metric"><span>${k}</span><b>${v}</b></article>`).join("")}
      </div>
    </section>

    <section class="section rule-section">
      <h2>风控规则</h2>
      <div class="warning-list">
        <p><b>单标的上限 20%</b><span>避免单一品种过度集中。</span></p>
        <p><b>单日最大回撤 7%</b><span>触发后进入熔断观察。</span></p>
        <p><b>异常交易复核</b><span>极小仓位刷曲线、尾盘异常拉升等直接取消成绩。</span></p>
      </div>
    </section>

    <section class="section weights-grid">
      <article><b>收益</b><span>40%</span></article>
      <article><b>最大回撤</b><span>25%</span></article>
      <article><b>夏普</b><span>20%</span></article>
      <article><b>稳定性</b><span>15%</span></article>
    </section>

    <section class="section split-card">
      <article><h3>奖励与路演</h3><p>前五名参与 10 分钟策略逻辑路演，不透露代码和买卖细节。</p></article>
      <article><h3>合规边界</h3><p>不接入实盘资金，不提供跟单、持仓、买卖点和收益承诺。</p></article>
    </section>

    <section class="section bottom-cta">
      <button class="button" data-route="signup">我要报名</button>
      <button class="button button-outline" data-route="audience">查看积分规则</button>
    </section>
  `;
}

function renderSignup() {
  return `
    ${renderHero({
      title: "成为 S1",
      red: "匿名选手",
      desc: "创建昵称、选择角色皮肤、绑定平台模拟账号后即可报名参赛。",
      icon: "trophy",
      badges: [["报名消耗 30 积分", "red"], ["每日登录送 1 积分", "amber"]]
    })}

    <section class="section form-stack">
      <label class="field"><span>自定义昵称</span><input placeholder="例如 A7 / 稳健平衡派" /></label>
      <label class="field"><span>个性签名</span><input placeholder="一句话说明你的策略风格" /></label>
      <div class="skin-grid">
        ${["红色先锋", "银色防守", "蓝色量化"].map((skin, index) => `<button class="skin-card ${index === 0 ? "active" : ""}"><i></i><b>${skin}</b><small>${index === 0 ? "推荐" : "可选"}</small></button>`).join("")}
      </div>
      <div class="segmented wide"><button class="active">月赛</button><button>S1 赛季</button><button>1v1 表演赛</button></div>
      <label class="field"><span>平台模拟账号 ID</span><input placeholder="填写聚宽/掘金/MT5 等模拟账号" /></label>
      <div class="checkbox-list">
        <label><input type="checkbox" checked /> 我同意匿名展示收益曲线、回撤、夏普和榜单表现</label>
        <label><input type="checkbox" checked /> 我确认不提交实盘资金、不展示持仓和买卖信号</label>
      </div>
      <button class="button full-button" data-action="applyArena">提交报名</button>
    </section>
  `;
}

function renderPlayer() {
  return `
    <section class="player-hero">
      <div class="player-avatar">A7</div>
      <div>
        <span class="pill red">王者 I</span>
        <h1>A7 稳健平衡派</h1>
        <p class="caption">签名：收益不是唯一目标，控制回撤才是长期游戏。</p>
      </div>
    </section>

    ${metricStrip([
      ["S1收益", "+21.37%", "red-value"],
      ["最大回撤", "-8.41%", "green"],
      ["夏普", "1.68"],
      ["解锁人数", "128"]
    ])}

    <section class="section dual-grid">${chartSvg("up", "净值曲线")}${chartSvg("drawdown", "回撤曲线")}</section>

    <section class="section info-stack">
      ${[
        ["策略风格", "稳健平衡，趋势确认后提高暴露，弱趋势阶段降低仓位。"],
        ["赛季记录", "连续 3 周进入综合榜前三，未触发风控熔断。"],
        ["积分解锁可见", "匿名动态收益曲线、最大回撤、夏普、路演摘要。"],
        ["不可见", "持仓、买卖点、实时信号、策略代码。"]
      ].map(([title, desc]) => `<article class="info-card"><h3>${title}</h3><p>${desc}</p></article>`).join("")}
    </section>

    <section class="section risk-box">过往收益不代表未来表现，积分解锁仅获得研究信息，不构成投资建议。</section>
    <section class="section bottom-cta">
      <button class="button" data-route="audience">积分解锁观察</button>
      <button class="button button-outline" data-route="battle">发起对决</button>
    </section>
  `;
}

function renderAudience() {
  return `
    ${renderHero({
      title: "积分解锁",
      red: "观察内容",
      desc: "使用积分查看匿名策略表现。积分只用于平台研究内容和功能消耗，不开放持仓、买卖点和实时信号。",
      icon: "ticket",
      badges: [["1 元 = 1 积分", "red"], ["每日登录 +1", "blue"], ["内容消耗", "green"]]
    })}

    <section class="section split-card">
      <article>
        <h3>您将获得</h3>
        ${["查看匿名策略动态收益曲线", "查看最大回撤 / 夏普 / 稳定性评分", "查看赛季榜单与 1v1 对决", "查看路演摘要"].map((item) => `<p class="check-line">${item}</p>`).join("")}
      </article>
      <article>
        <h3>不包含以下内容</h3>
        ${["持仓", "买卖点", "实时信号", "跟单服务"].map((item) => `<p class="cross-line">${item}</p>`).join("")}
      </article>
    </section>

    <section class="section ticket-grid">
      <article class="ticket-card active"><span>推荐</span><h3>积分充值</h3><p>充值接口占位</p><b>1 元 = 1 积分</b><small>积分可用于解锁研究内容</small></article>
      <article class="ticket-card"><h3>每日赠送</h3><p>登录奖励</p><b>+1 积分 / 天</b><small>每日登录自动入账，不可提现</small></article>
    </section>

    <section class="section bottom-cta">
      <button class="button" data-action="pay">充值积分</button>
      <button class="button button-outline" data-route="ranking">查看免费榜单</button>
    </section>

    <section class="section creator-card">
      <span>${featureIcon("ticket")}</span>
      <div><h3>积分消耗说明</h3><p>积分用于解锁报告、AI 解读次数、匿名观察内容和报名资格；不代表投资收益或分成。</p></div>
      <button data-route="arenaRules">了解更多 ›</button>
    </section>

    <section class="section risk-box">策略竞技场展示的所有策略及历史数据仅供参考，不构成任何投资建议。市场有风险，过往收益不代表未来表现。</section>
  `;
}

function renderAi() {
  return `
    ${renderHero({
      title: "AI",
      red: "策略助手",
      desc: "解释策略逻辑、指标含义、回测差异和风险来源，不给出具体买卖建议。",
      icon: "ai",
      badges: [["不荐股", "red"], ["不喊单", "blue"], ["有风险提示", "green"]]
    })}

    <section class="section ability-strip">
      ${[
        ["解释策略", "读懂因子与风控"],
        ["解读回测", "收益、回撤、夏普"],
        ["提示风险", "识别失效场景"]
      ].map(([title, desc]) => `<article><span>${featureIcon("ai")}</span><b>${title}</b><small>${desc}</small></article>`).join("")}
    </section>

    <section class="section risk-box">AI 输出仅用于辅助理解研究材料，不构成投资建议。关键信息需以报告和数据来源为准。</section>

    <section class="section ai-question-grid">
      ${["这个策略为什么适合中性偏热行情？", "最大回撤和夏普应该怎么看？", "什么情况下策略可能失效？", "回测和模拟表现有什么区别？"].map((question) => `<button>${question}</button>`).join("")}
    </section>

    <section class="section chat-card">
      <article class="message-card user">沪深300趋势增强策略适合现在吗？</article>
      <article class="message-card bot">
        <b>AI 解读</b>
        <p>当前市场温度为 58，处于中性偏热。该策略依赖趋势确认和回撤控制，可以纳入观察，但不代表一定获得正收益。</p>
        <div class="source-line">来源：市场温度计、策略回测报告、风险评分</div>
      </article>
    </section>

    <section class="section input-dock">
      <button>+</button>
      <input placeholder="输入你想理解的策略问题" />
      <button class="send">发送</button>
    </section>
  `;
}

function renderWeekly() {
  return `
    ${renderHero({
      title: "每周",
      red: "策略报告",
      desc: "汇总关注策略、市场温度变化、风险提醒和下周观察重点。",
      icon: "ticket",
      badges: [["周一更新", "red"], ["积分解锁", "blue"]]
    })}

    <section class="section">
      <div class="section-title"><h2>本周关注策略</h2><button data-route="strategy">管理关注 ›</button></div>
      ${renderStrategyCards(strategies.slice(0, 2))}
    </section>

    <section class="section market-review">
      <article><span>市场温度</span><b>58</b><small>较上周 +6</small></article>
      <article><span>赚钱效应</span><b>偏热</b><small>活跃度提升</small></article>
      <article><span>波动风险</span><b>中性</b><small>事件扰动需关注</small></article>
    </section>

    <section class="section info-stack">
      <article class="info-card"><h3>市场回顾</h3><p>行业轮动活跃，趋势策略表现优于防守策略，但回撤波动略有增加。</p></article>
      <article class="info-card"><h3>风险提醒</h3><p>需关注成交量收缩和风格快速切换，避免把短期排名视为确定性机会。</p></article>
    </section>

    <section class="section locked-banner">
      <div><strong>完整周报已锁定</strong><p class="caption">包含策略对比、异常波动解释和下周观察清单。</p></div>
      <button class="button" data-route="member">用积分解锁</button>
    </section>
  `;
}

function renderRisk() {
  return `
    ${renderHero({
      title: "风险提示与",
      red: "服务边界",
      desc: "平台提供策略研究、数据分析和投资者教育，不提供任何证券投资建议或交易执行服务。",
      icon: "shield",
      badges: [["必须阅读", "red"], ["合规边界", "blue"]]
    })}

    <section class="section numbered-list">
      ${[
        ["历史不代表未来", "回测、模拟和过往表现均不能保证未来收益。"],
        ["不提供投资建议", "平台不推荐具体股票、不提供买卖点、不承诺收益。"],
        ["不接入实盘资金", "平台不代客理财、不托管资金、不提供跟单服务。"],
        ["AI 仅做解释", "AI 解释用于辅助理解报告，不作为交易依据。"]
      ].map(([title, desc], index) => `<article><span>${index + 1}</span><div><h3>${title}</h3><p>${desc}</p></div></article>`).join("")}
    </section>

    <section class="section no-service-grid">
      ${["持仓", "买卖点", "实时信号", "跟单服务"].map((item) => `<article><b>不提供</b><span>${item}</span></article>`).join("")}
    </section>

    <section class="section checkbox-list risk-confirm">
      <label><input type="checkbox" checked /> 我已理解平台仅提供信息服务</label>
      <label><input type="checkbox" checked /> 我已理解所有投资决策需自行判断并承担风险</label>
    </section>
    <button class="button full-button" data-route="home">确认并继续</button>
  `;
}

function renderPricing(compact = false) {
  const plans = [
    ["免费内容", "基础体验", "0 积分", "市场温度计、部分榜单、简版周报", "当前可用"],
    ["积分充值", "统一充值比例", "1 元 = 1 积分", "充值积分用于解锁研究内容和功能次数", "充值积分"],
    ["每日登录", "活跃奖励", "+1 积分 / 天", "每日登录自动发放，积分不可提现", "领取记录"],
    ["报告解锁", "深度报告阅读", "10-30 积分 / 份", "完整回测、指标解释、风险说明", "积分解锁"],
    ["AI 解读次数", "策略解释", "1 积分 / 次", "解释指标、回测差异和风险来源", "使用积分"],
    ["机构服务", "企业级服务", "人工咨询", "API、团队权限、私有化、定制报告", "咨询机构版"]
  ];
  const list = compact ? plans.slice(0, 3) : plans;
  return `<div class="pricing-list">${list.map(([name, sub, price, desc, action], index) => `
    <article class="pricing-card ${index === 1 ? "highlight" : ""}">
      <span class="feature-badge">${name.slice(0, 1)}</span>
      <div>
        <h3>${name}</h3>
        <p class="caption">${sub}</p>
        <p>${desc}</p>
      </div>
      <div>
        <div class="price">${price}</div>
        <button class="button ${name === "免费内容" ? "button-light" : ""}" data-action="pay">${action}</button>
      </div>
    </article>
  `).join("")}</div>`;
}

function renderMember() {
  return `
    ${renderHero({
      title: "积分中心",
      red: "充值与消耗",
      desc: "统一使用积分解锁研究内容和功能次数。积分不绑定收益，不提供股票推荐、收益保证、跟单或代客交易服务。",
      icon: "ticket",
      badges: [["1 元 = 1 积分", "red"], ["每日登录 +1", "blue"], ["不可提现", "green"]]
    })}
    <section class="section">${renderPricing()}</section>
    <section class="section faq-list">
      <article><b>是否包含买卖建议？</b><span>不包含，平台只提供研究信息和风险解释。</span></article>
      <article><b>积分能否提现吗？</b><span>不能，积分只用于平台内研究内容和功能消耗。</span></article>
      <article><b>能否查看持仓？</b><span>不能，竞技场观察内容只展示匿名表现指标。</span></article>
      <article><b>后续 APP 怎么处理？</b><span>一期先做小程序和 Web，APP 留作后续版本。</span></article>
    </section>
    <section class="section risk-box">本平台积分仅用于策略研究、数据分析和投资者教育内容消耗，不构成任何证券投资建议。充值接口上线前需完成法务、财务、税务和平台规则确认。</section>
  `;
}

function renderProfile() {
  return `
    <section class="profile-card member-hero">
      <div class="player-avatar small">研</div>
      <div>
        <h3>研究用户</h3>
        <p class="caption">微信已授权｜积分余额 36｜关注策略 4 个</p>
      </div>
      <button class="button button-light" data-route="login">账号设置</button>
    </section>

    <section class="section function-grid">
      ${[
        ["已解锁报告", "3", "backtest"],
        ["周报解锁", "已开通", "weekly"],
        ["观察内容", "S1", "audience"],
        ["风险确认", "已完成", "risk"],
        ["关注策略", "4", "strategy"],
        ["选手档案", "A7", "player"]
      ].map(([title, value, route]) => `<button class="function-card" data-route="${route}"><b>${title}</b><span>${value}</span></button>`).join("")}
    </section>

    <section class="section benefit-strip">
      <strong>积分余额 36</strong>
      <span>可用于完整回测、AI 解读、观察内容和报名资格</span>
      <button data-route="member">充值 ›</button>
    </section>

    <section class="section list-card">
      ${["我的关注", "积分明细", "充值记录", "隐私与数据授权", "客服与帮助"].map((item) => `<button>${item}<span>›</span></button>`).join("")}
    </section>
  `;
}

function renderLogin() {
  return `
    ${renderHero({
      title: "登录后同步",
      red: "研究资产",
      desc: "使用微信授权登录并绑定手机号，保存关注策略、报告和积分权益。",
      icon: "ai",
      badges: [["微信授权", "green"], ["手机绑定", "blue"]]
    })}

    <section class="section login-card">
      <button class="wechat-button">微信授权登录</button>
      <div class="segmented wide"><button class="active">手机号</button><button>邮箱</button></div>
      <label class="field"><span>手机号</span><input placeholder="请输入手机号" /></label>
      <label class="field code-field"><span>验证码</span><input placeholder="请输入验证码" /><button>获取验证码</button></label>
      <div class="checkbox-list">
        <label><input type="checkbox" checked /> 我同意用户协议、隐私政策和风险提示</label>
      </div>
      <button class="button full-button" data-route="profile">登录 / 注册</button>
      <p class="caption center">未注册用户将自动创建账号，可随时注销。</p>
    </section>
  `;
}

function renderAdmin() {
  return `
    <section class="admin-head">
      <span class="brand-mark">AI</span>
      <div><h1>运营后台 / 内容审核</h1><p class="caption">策略、报告、风险词命中和今日处理量</p></div>
      <button class="icon-button">12</button>
    </section>

    <section class="section admin-grid">
      ${[
        ["待审核策略", "128", "+18"],
        ["待审核报告", "56", "+9"],
        ["风险词命中", "342", "+26"],
        ["今日处理量", "238", "+37"]
      ].map(([title, value, diff]) => `<article><span>${featureIcon("chart")}</span><b>${title}</b><strong>${value}</strong><small>较昨日 ${diff}</small></article>`).join("")}
    </section>

    <section class="section alert-card">
      <span>${featureIcon("shield")}</span>
      <div><h3>合规风险预警 <em>高风险</em></h3><p>近 24 小时内，风险词命中数上升较快，请及时审核相关内容。</p></div>
      <button data-route="risk">查看详情 ›</button>
    </section>

    <section class="section sticky-tabs">
      <button class="active">策略管理</button><button>报告管理</button><button>合规审核 <i>24</i></button><button>日志</button>
    </section>

    <section class="section toolbar">
      <button>全部状态 ▾</button>
      <input placeholder="搜索策略名称 / 关键词" />
      <button>筛选</button>
      <button>导出</button>
    </section>

    <section class="section admin-table">
      <div class="admin-row head"><span>策略名称</span><span>状态</span><span>操作人</span><span>更新时间</span><span>操作</span></div>
      ${[
        ["短线动量增强策略 v2.1", "待审核", "张三", "2024-05-20 15:30", "审核"],
        ["红利低波优选策略 v1.3", "待审核", "李四", "2024-05-20 14:22", "审核"],
        ["AI 趋势轮动策略 v1.0", "已发布", "王五", "2024-05-20 12:10", "下线"],
        ["行业景气度轮动 v2.4", "已发布", "赵六", "2024-05-19 18:45", "下线"],
        ["事件驱动套利策略 v1.2", "待审核", "钱七", "2024-05-19 16:05", "审核"]
      ].map(([name, status, owner, time, action]) => `<div class="admin-row"><span><b>${name}</b><small>股票 / 量化选股</small></span><span class="status-tag ${status === "已发布" ? "ok" : "wait"}">${status}</span><span>${owner}</span><span>${time}</span><button>${action}</button></div>`).join("")}
    </section>

    <section class="section pagination"><span>共 128 条</span><button>‹</button><button class="active">1</button><button>2</button><button>3</button><button>›</button><button>10 条/页 ▾</button></section>
  `;
}

function render() {
  const templates = {
    home: renderHome,
    market: renderMarket,
    strategy: renderStrategy,
    arena: renderArena,
    member: renderMember,
    profile: renderProfile,
    strategyDetail: renderStrategyDetail,
    backtest: renderBacktest,
    ai: renderAi,
    weekly: renderWeekly,
    risk: renderRisk,
    login: renderLogin,
    ranking: renderRanking,
    battle: renderBattle,
    audience: renderAudience,
    arenaRules: renderArenaRules,
    signup: renderSignup,
    player: renderPlayer,
    admin: renderAdmin
  };
  app.innerHTML = (templates[currentRoute] || renderHome)();
}

function openModal(html) {
  modalContent.innerHTML = html;
  modal.classList.add("open");
  modal.setAttribute("aria-hidden", "false");
}

function closeModal() {
  modal.classList.remove("open");
  modal.setAttribute("aria-hidden", "true");
}

function toast(message) {
  openModal(`<h2>${message}</h2><p class="caption">这是 HTML 原型中的交互反馈。</p>`);
}

document.body.addEventListener("click", (event) => {
  const routeButton = event.target.closest("[data-route]");
  if (routeButton) {
    closeModal();
    navigate(routeButton.dataset.route);
    return;
  }

  const rankButton = event.target.closest("[data-rank]");
  if (rankButton) {
    currentRank = rankButton.dataset.rank;
    render();
    return;
  }

  const actionButton = event.target.closest("[data-action]");
  if (!actionButton) return;
  const action = actionButton.dataset.action;
  if (action === "subscribeWeekly") navigate("weekly");
  if (action === "voteBattle") toast("投票已提交");
  if (action === "pay") toast("积分充值接口占位");
  if (action === "applyArena") toast("选手报名流程占位");
});

modalClose.addEventListener("click", closeModal);
modal.addEventListener("click", (event) => {
  if (event.target === modal) closeModal();
});
backButton.addEventListener("click", () => navigate("home"));

renderNav();
navigate("home");
