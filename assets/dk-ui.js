/* DegenKit app UI layer: network promo cards (all pages) + Solana market pulse. No dependencies. */
(function () {
  "use strict";
  var m = location.pathname.match(/\/launch\/([a-z]+)\/?/);
  var CHAIN = m ? m[1] : "";
  var ASSETS = "../../assets/";

  /* ---------------- promo cards ---------------- */
  var PROMOS = [
    { key: "solana", name: "Solana", tag: "Live", line: "SPL tokens in one signature — mint & freeze revoked.", logo: "solana-logo.png", p1: "#3B1D6B", p2: "#0E8F73" },
    { key: "ethereum", name: "Ethereum", tag: "Live", line: "Fixed-supply ERC-20s and custom-tax tokens.", logo: "ethereum-logo.png", p1: "#2C3A7A", p2: "#171A33" },
    { key: "bnb", name: "BNB Chain", tag: "New", line: "Low-fee tokens and tax tokens on BNB Smart Chain.", logo: "bnb-logo.png", p1: "#7A5B00", p2: "#1E1700" },
    { key: "base", name: "Base", tag: "New", line: "Launch on Coinbase's low-fee Layer 2.", logo: "base-logo.png", p1: "#1946B8", p2: "#0A1230" },
    { key: "robinhood", name: "Robinhood Chain", tag: "New", line: "Fixed-supply and tax tokens, same simple flow.", logo: "robinhood-logo.png", p1: "#0B6B1E", p2: "#06160A" }
  ];

  function buildPromos() {
    var items = PROMOS.filter(function (p) { return p.key !== CHAIN; });
    var wrap = document.createElement("div");
    wrap.className = "promo-wrap";
    var html = '<div class="promo-title">Launch on another network</div><div class="promo-row">';
    items.forEach(function (p) {
      html += '<a class="promo-card" style="--p1:' + p.p1 + ';--p2:' + p.p2 + '" href="/launch/' + p.key + '/">' +
        '<img class="promo-img" alt="" loading="lazy" data-k="' + p.key + '" src="' + ASSETS + 'promo/' + p.key + '.webp">' +
        '<img class="promo-logo" alt="" src="' + ASSETS + p.logo + '">' +
        '<div class="promo-body"><span class="promo-tag">' + p.tag + '</span><h4>Launch on ' + p.name + '</h4><p>' + p.line + '</p>' +
        '<span class="promo-cta">Launch on ' + p.name + ' →</span></div></a>';
    });
    wrap.innerHTML = html + "</div>";
    wrap.querySelectorAll(".promo-img").forEach(function (img) {
      img.addEventListener("load", function () { img.parentNode.classList.add("has-img"); });
      img.addEventListener("error", function () {
        if (!img.dataset.png) { img.dataset.png = "1"; img.src = ASSETS + "promo/" + img.dataset.k + ".png"; }
        else img.remove();
      });
    });
    return wrap;
  }
  function addPromos() {
    document.querySelectorAll(".tool-view").forEach(function (v) {
      if (!v.querySelector(".promo-wrap")) v.appendChild(buildPromos());
    });
  }

  /* ---------------- helpers ---------------- */
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function usd(n) {
    if (n == null || !isFinite(n)) return "—";
    var a = Math.abs(n);
    if (a >= 1e12) return "$" + (n / 1e12).toFixed(2) + "T";
    if (a >= 1e9) return "$" + (n / 1e9).toFixed(2) + "B";
    if (a >= 1e6) return "$" + (n / 1e6).toFixed(1) + "M";
    if (a >= 1e3) return "$" + (n / 1e3).toFixed(1) + "K";
    return "$" + n.toFixed(2);
  }
  function price(n) {
    if (n == null || !isFinite(n)) return "—";
    if (n >= 1) return "$" + n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    if (n >= 0.01) return "$" + n.toFixed(4);
    return "$" + Number(n.toPrecision(3)).toString();
  }
  function pct(n, d) { return (n >= 0 ? "+" : "") + n.toFixed(d == null ? 1 : d) + "%"; }
  function chgPill(n) {
    if (n == null || !isFinite(n)) return "";
    var c = Math.abs(n) < 0.3 ? "flat" : n > 0 ? "up" : "down";
    return '<span class="chg ' + c + '">' + (n > 0 ? "▲ " : n < 0 ? "▼ " : "") + pct(Math.abs(n)).replace("+", "") + "</span>";
  }
  function fetchJson(url, ms) {
    var ctl = new AbortController();
    var t = setTimeout(function () { ctl.abort(); }, ms || 9000);
    return fetch(url, { signal: ctl.signal, headers: { accept: "application/json" } }).then(function (r) {
      clearTimeout(t);
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    });
  }

  /* ---------------- market data ---------------- */
  var CACHE_KEY = "dk-mkt-v1", TTL = 5 * 60 * 1000;
  var STABLES = { SOL: 1, WSOL: 1, USDC: 1, USDT: 1, USDS: 1, PYUSD: 1, JUP: 0 };

  function pickTrending(boosts, pairs) {
    var best = null;
    var bySym = {};
    pairs.forEach(function (p) {
      if (!p || !p.baseToken || p.chainId !== "solana") return;
      var a = p.baseToken.address;
      var liq = (p.liquidity && p.liquidity.usd) || 0;
      if (!bySym[a] || liq > ((bySym[a].liquidity && bySym[a].liquidity.usd) || 0)) bySym[a] = p;
    });
    Object.keys(bySym).forEach(function (a) {
      var p = bySym[a];
      var sym = (p.baseToken.symbol || "").toUpperCase();
      if (STABLES[sym]) return;
      var liq = (p.liquidity && p.liquidity.usd) || 0;
      var vol = (p.volume && p.volume.h24) || 0;
      if (liq < 30000 || vol < 100000) return;
      var ch = (p.priceChange && p.priceChange.h24) || 0;
      var boost = 0;
      boosts.forEach(function (b) { if (b.tokenAddress === a) boost = b.totalAmount || b.amount || 1; });
      var score = Math.log10(vol + 1) * 2 + Math.log10(liq + 1) + Math.max(-30, Math.min(ch, 300)) / 60 + (boost ? 1 : 0);
      if (!best || score > best.score) best = { score: score, pair: p, boosted: !!boost };
    });
    return best;
  }

  function loadMarket(force) {
    if (!force) {
      try {
        var c = JSON.parse(localStorage.getItem(CACHE_KEY) || "null");
        if (c && Date.now() - c.t < TTL) return Promise.resolve(c);
      } catch (e) {}
    }
    var out = { t: Date.now(), sol: null, global: null, fng: null, dex: null, meme: null, trend: null };
    var jobs = [
      fetchJson("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=solana&price_change_percentage=24h").then(function (r) { out.sol = r && r[0]; }),
      fetchJson("https://api.coingecko.com/api/v3/global").then(function (r) { out.global = r && r.data; }),
      fetchJson("https://api.alternative.me/fng/?limit=2").then(function (r) { out.fng = r && r.data; }),
      fetchJson("https://api.llama.fi/overview/dexs/Solana?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true").then(function (r) { out.dex = r; }),
      fetchJson("https://api.coingecko.com/api/v3/coins/categories").then(function (r) {
        out.meme = (r || []).filter(function (x) { return x.id === "solana-meme-coins"; })[0] || null;
      }),
      fetchJson("https://api.dexscreener.com/token-boosts/top/v1").then(function (boosts) {
        var sol = (boosts || []).filter(function (b) { return b.chainId === "solana"; }).slice(0, 12);
        if (!sol.length) return;
        var addrs = sol.map(function (b) { return b.tokenAddress; }).join(",");
        return fetchJson("https://api.dexscreener.com/tokens/v1/solana/" + addrs).then(function (pairs) {
          out.trend = pickTrending(sol, pairs || []);
        });
      })
    ];
    return Promise.allSettled(jobs).then(function () {
      var any = out.sol || out.global || out.fng || out.dex || out.meme || out.trend;
      if (any) { try { localStorage.setItem(CACHE_KEY, JSON.stringify(out)); } catch (e) {} return out; }
      try { var old = JSON.parse(localStorage.getItem(CACHE_KEY) || "null"); if (old) return old; } catch (e) {}
      return out;
    });
  }

  /* ---------------- plain-language text ---------------- */
  function priceWords(ch) {
    if (ch == null) return "";
    if (ch >= 6) return "Strong rally.";
    if (ch >= 2) return "Climbing.";
    if (ch > -2) return "Calm, no big move.";
    if (ch > -6) return "Pulling back.";
    return "Sharp drop.";
  }
  function moodWords(v) {
    if (v <= 24) return "Most people are scared.";
    if (v <= 44) return "Traders are cautious.";
    if (v <= 55) return "Market can't decide.";
    if (v <= 74) return "Traders are optimistic.";
    return "Very hot, can flip fast.";
  }
  function moodLabel(v) { return v <= 24 ? "Extreme fear" : v <= 44 ? "Fear" : v <= 55 ? "Neutral" : v <= 74 ? "Greed" : "Extreme greed"; }
  function volWords(vol, mcap) {
    if (!vol || !mcap) return "";
    var r = vol / mcap * 100;
    if (r >= 9) return "Very busy.";
    if (r >= 5) return "Busier than usual.";
    if (r >= 2.5) return "Normal day.";
    return "Quiet.";
  }
  function domWords(d) {
    if (d == null) return "";
    return "<b>$" + d.toFixed(1) + "</b> of every $100 in crypto.";
  }

  function buildInsights(d) {
    var items = [];
    var ds = new Date().toLocaleDateString("en-US", { weekday: "long", day: "numeric", month: "long", year: "numeric" });
    if (d.sol) {
      var ch = d.sol.price_change_percentage_24h;
      items.push({ ic: ch >= 0 ? "📈" : "📉", t: ch >= 2 ? "Solana is climbing" : ch <= -2 ? "Solana is under pressure" : "Solana is moving sideways",
        d: price(d.sol.current_price) + " (" + pct(ch) + " in 24h)." });
    }
    if (d.fng && d.fng[0]) {
      var v = +d.fng[0].value, y = d.fng[1] ? +d.fng[1].value : null;
      var trend = y == null ? "" : v > y + 2 ? " Mood improved since yesterday." : v < y - 2 ? " Mood got worse since yesterday." : " About the same as yesterday.";
      items.push({ ic: v <= 44 ? "😨" : v <= 55 ? "😐" : "🤑", t: "Crypto mood: " + moodLabel(v), d: moodWords(v) });
    }
    if (d.dex && d.dex.total24h) {
      var c1 = d.dex.change_1d;
      items.push({ ic: "🔄", t: "Solana DEX trading " + (c1 > 10 ? "is heating up" : c1 < -10 ? "is cooling down" : "is steady"),
        d: usd(d.dex.total24h) + " in 24h" + (c1 != null ? ", " + pct(c1, 0) + " vs yesterday." : ".") });
    }
    if (d.meme) {
      var mc = d.meme.market_cap_change_24h;
      items.push({ ic: "🐸", t: "Solana memecoins " + (mc > 3 ? "are hot" : mc < -3 ? "are slipping" : "are flat"),
        d: usd(d.meme.volume_24h) + " traded in 24h (" + pct(mc || 0) + ")." });
    }
    return items;
  }

  /* ---------------- rendering ---------------- */
  function statCards(d) {
    var s = d.sol, g = d.global, f = d.fng && d.fng[0];
    var h = "";
    h += '<div class="mkt-card"><div class="mkt-k"><img class="mkt-ico" src="' + ASSETS + 'solana-logo.png" alt="">Solana price</div><div class="mkt-v">' + (s ? price(s.current_price) + chgPill(s.price_change_percentage_24h) : "—") +
      '</div><div class="mkt-s">' + (s ? priceWords(s.price_change_percentage_24h) : "Unavailable right now.") + "</div></div>";
    h += '<div class="mkt-card"><div class="mkt-k">🌡 Market mood</div><div class="mkt-v">' + (f ? esc(moodLabel(+f.value)) + ' <small style="font-size:15px;color:var(--muted)">' + f.value + "/100</small>" : "—") + "</div>" +
      (f ? '<div class="gauge"><i style="left:' + Math.max(2, Math.min(98, +f.value)) + '%"></i></div>' : "") +
      '<div class="mkt-s">' + (f ? moodWords(+f.value) : "Unavailable right now.") + "</div></div>";
    var dom = (s && g && g.total_market_cap && g.total_market_cap.usd) ? s.market_cap / g.total_market_cap.usd * 100 : null;
    h += '<div class="mkt-card"><div class="mkt-k">🥧 Solana\'s share</div><div class="mkt-v">' + (dom != null ? dom.toFixed(1) + "%" : "—") + '</div><div class="mkt-s">' +
      (dom != null ? domWords(dom) : "Unavailable right now.") + "</div></div>";
    h += '<div class="mkt-card"><div class="mkt-k">💸 Traded today</div><div class="mkt-v">' + (s ? usd(s.total_volume) : "—") + '</div><div class="mkt-s">' +
      (s ? volWords(s.total_volume, s.market_cap) : "Unavailable right now.") + "</div></div>";
    return '<div class="mkt-grid">' + h + "</div>";
  }
  function dexCards(d) {
    var x = d.dex, me = d.meme, h = "";
    h += '<div class="mkt-card"><div class="mkt-k">🔄 Solana DEX volume</div><div class="mkt-v">' + (x && x.total24h ? usd(x.total24h) + chgPill(x.change_1d) : "—") + '</div><div class="mkt-s">' +
      (x && x.total24h ? "Swapped on Solana DEXs in 24h" + (x.change_1d != null ? (x.change_1d > 10 ? " — picking up." : x.change_1d < -10 ? " — slowing down." : " — steady.") : ".") : "Unavailable right now.") + "</div></div>";
    h += '<div class="mkt-card"><div class="mkt-k">🐸 Memecoin volume</div><div class="mkt-v">' + (me ? usd(me.volume_24h) + chgPill(me.market_cap_change_24h) : "—") + '</div><div class="mkt-s">' +
      (me ? "Traded in 24h. All memecoins together: <b>" + usd(me.market_cap) + "</b>." : "Unavailable right now.") + "</div></div>";
    var ratio = (x && x.total24h && d.sol) ? (x.total24h / d.sol.total_volume) : null;
    h += '<div class="mkt-card"><div class="mkt-k">🧭 How to read this</div><div class="mkt-s" style="margin-top:2px">Green ▲ = up in 24h, red ▼ = down. Refreshes every few minutes.</div></div>';
    return '<div class="mkt-grid g3">' + h + "</div>";
  }
  function insightsCard(d) {
    var items = buildInsights(d);
    if (!items.length) return '<div class="mkt-card"><div class="mkt-k">Market insights</div><div class="mkt-err">Insights will appear when market data loads.</div></div>';
    var h = '<div class="mkt-card"><div class="mkt-k">📰 Market insights</div>';
    items.forEach(function (i) {
      h += '<div class="ins-item"><div class="ins-ic">' + i.ic + '</div><div><div class="ins-t">' + esc(i.t) + '</div><div class="ins-d">' + esc(i.d) + "</div></div></div>";
    });
    return h + "</div>";
  }
  function trendCard(d) {
    var t = d.trend;
    if (!t) return '<div class="mkt-card trend"><div class="trend-badge">🔥 Trending on Solana</div><div class="mkt-err">No trending token found right now. Check back in a few minutes.</div></div>';
    var p = t.pair, b = p.baseToken || {};
    var vol = (p.volume && p.volume.h24) || 0, liq = (p.liquidity && p.liquidity.usd) || 0;
    var ch = (p.priceChange && p.priceChange.h24) || 0;
    var buys = p.txns && p.txns.h24 ? p.txns.h24.buys : 0, sells = p.txns && p.txns.h24 ? p.txns.h24.sells : 0;
    var ageH = p.pairCreatedAt ? (Date.now() - p.pairCreatedAt) / 36e5 : null;
    var why = [];
    why.push("<b>" + usd(vol) + "</b> traded in 24h, price " + (ch >= 0 ? "up " : "down ") + "<b>" + Math.abs(ch).toFixed(0) + "%</b>.");
    if (buys + sells > 50) why.push(buys > sells * 1.1 ? "Buyers leading." : sells > buys * 1.1 ? "Sellers leading." : "Balanced.");
    if (t.boosted) why.push("Promoted on DexScreener.");
    var chips = "";
    if (ageH != null) chips += '<span class="chip ' + (ageH < 24 ? "warn" : "") + '">' + (ageH < 24 ? "Brand new (" + Math.max(1, Math.round(ageH)) + "h old)" : ageH < 24 * 7 ? Math.round(ageH / 24) + " days old" : Math.round(ageH / 24) + " days old") + "</span>";
    chips += '<span class="chip ' + (liq < 100000 ? "warn" : "good") + '">' + (liq < 100000 ? "Low liquidity — hard to sell" : "Decent liquidity") + "</span>";
    if (ch > 150) chips += '<span class="chip warn">Already pumped a lot</span>';
    var img = (p.info && p.info.imageUrl) ? '<img class="trend-img" alt="" src="' + esc(p.info.imageUrl) + '" referrerpolicy="no-referrer" onerror="this.replaceWith(Object.assign(document.createElement(\'div\'),{className:\'trend-img\',textContent:\'' + esc((b.symbol || "?").charAt(0).toUpperCase()) + '\'}))">'
      : '<div class="trend-img">' + esc((b.symbol || "?").charAt(0).toUpperCase()) + "</div>";
    var url = p.url ? esc(p.url) : "https://dexscreener.com/solana/" + esc(b.address || "");
    return '<div class="mkt-card trend"><div class="trend-badge">🔥 Trending on Solana today</div>' +
      '<div class="trend-top">' + img + '<div><div class="trend-name">' + esc(b.name || "Unknown") + '</div><div class="trend-sym">$' + esc(b.symbol || "") + " · " + price(+p.priceUsd) + " " + chgPill(ch) + "</div></div></div>" +
      '<div class="mkt-s" style="margin-bottom:6px">' + why.join(" ") + "</div>" +
      '<div class="trend-stats"><div><small>24h volume</small><b>' + usd(vol) + "</b></div><div><small>Liquidity</small><b>" + usd(liq) + "</b></div><div><small>Buys / sells</small><b>" + (buys || 0) + " / " + (sells || 0) + "</b></div></div>" +
      '<div class="chips">' + chips + "</div>" +
      '<div class="trend-actions"><a class="a1" href="' + url + '" target="_blank" rel="noopener">See chart on DexScreener →</a></div>' +
      '<div class="disc">Auto-ranked by volume and liquidity. <b>Not financial advice</b> — memecoins can go to zero.</div></div>';
  }

  function render(el, d, full) {
    var upd = new Date(d.t).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    var head = '<div class="mkt-head"><div><h2>' + (full ? "Solana market today" : "Market pulse") + "</h2><p>" +
      (full ? "What's happening on Solana right now, in plain words." : "A quick read on Solana today.") +
      '</p></div><div class="mkt-upd">Updated ' + upd + ' <button type="button" data-dk-refresh>↻ Refresh</button>' +
      (full ? "" : ' <button type="button" data-dk-more>See full market →</button>') + "</div></div>";
    var body = statCards(d);
    if (full) body += dexCards(d) + '<div class="mkt-two">' + insightsCard(d) + trendCard(d) + "</div>";
    else body += '<div class="mkt-two">' + trendCard(d) + insightsCard(d) + "</div>";
    el.innerHTML = head + body;
  }
  function skeleton(el) {
    el.innerHTML = '<div class="mkt-grid"><div class="mkt-skel"></div><div class="mkt-skel"></div><div class="mkt-skel"></div><div class="mkt-skel"></div></div><div class="mkt-skel" style="height:240px"></div>';
  }

  function initMarket() {
    var side = document.querySelector('.sidebar-item[data-view="scanner"]');
    var group = side && side.parentNode;
    if (group && !document.querySelector('.sidebar-item[data-view="market"]')) {
      var item = document.createElement("div");
      item.className = "sidebar-item"; item.setAttribute("data-view", "market");
      item.innerHTML = '<span class="ic">📊</span> Market';
      group.insertBefore(item, side);
      item.addEventListener("click", function () { if (window.switchView) window.switchView("market"); });
    }
    var main = document.querySelector(".main-inner");
    if (main && !document.getElementById("view-market")) {
      var sec = document.createElement("section");
      sec.id = "view-market"; sec.className = "tool-view";
      sec.innerHTML = '<div class="tool-header"><h1>Market</h1><p>Live Solana numbers explained simply — price, mood, trading activity and what\'s trending.</p></div><div class="mkt-wrap" id="marketFull" style="margin-top:22px"></div>';
      var create = document.getElementById("view-create");
      main.insertBefore(sec, create ? create.nextSibling : null);
    }
    var create = document.getElementById("view-create");
    if (create && !document.getElementById("marketMini")) {
      var mini = document.createElement("div");
      mini.className = "mkt-mini-sec"; mini.innerHTML = '<div class="mkt-wrap" id="marketMini"></div>';
      create.appendChild(mini);
    }
    var full = document.getElementById("marketFull"), mini2 = document.getElementById("marketMini");
    function paint(force, quiet) {
      if (!quiet) [mini2, full].forEach(function (el) { if (el) skeleton(el); });
      loadMarket(force).then(function (d) {
        if (mini2) render(mini2, d, false);
        if (full) render(full, d, true);
      });
    }
    document.addEventListener("click", function (e) {
      if (e.target.closest("[data-dk-refresh]")) paint(true);
      if (e.target.closest("[data-dk-more]") && window.switchView) window.switchView("market");
    });
    paint(false);
    setInterval(function () { if (!document.hidden) paint(false, true); }, TTL + 5000);
  }


  /* ---------------- announcement rail (square 1080x1080 images) ---------------- */
  var NEWS = [
    { img: "news/1.webp", t: "Tax tokens are live", s: "Ethereum · BNB · Base · Robinhood", href: "../ethereum/", g: "linear-gradient(135deg,#FF7A1A,#E8505B)" },
    { img: "news/2.webp", t: "Robinhood Chain is live", s: "Fixed-supply and tax tokens", href: "../robinhood/", g: "linear-gradient(135deg,#0B6B1E,#7BC500)" },
    { img: "news/3.webp", t: "Launch on BNB Chain", s: "Low-fee tokens in one click", href: "../bnb/", g: "linear-gradient(135deg,#8A6500,#F0B90B)" },
    { img: "news/4.webp", t: "Launch on Base", s: "Coinbase's low-fee Layer 2", href: "../base/", g: "linear-gradient(135deg,#0A2A8A,#0052FF)" }
  ].filter(function (n) { return n.href.indexOf("/" + CHAIN + "/") < 0; });

  function addNews() {
    var v = document.getElementById("view-create");
    var ws = v && v.querySelector(".workshop");
    if (!ws || v.querySelector(".news-row") || !NEWS.length) return;
    var row = document.createElement("div"); row.className = "workshop news-row"; row.setAttribute("aria-label", "Announcements");
    NEWS.slice(0, 2).forEach(function (n) {
      var a = document.createElement("a"); a.className = "news-card"; a.href = n.href; a.style.background = n.g;
      a.innerHTML = '<img class="news-img" alt="" src="' + ASSETS + n.img + '"><div class="news-txt"><b>' + esc(n.t) + "</b><span>" + esc(n.s) + "</span></div>";
      var im = a.querySelector("img");
      im.addEventListener("load", function () { a.classList.add("has-img"); });
      im.addEventListener("error", function () { im.remove(); });
      row.appendChild(a);
    });
    ws.after(row);
  }

  /* ---------------- popup card ---------------- */
  function addPopup() {
    try { if (+localStorage.getItem("dk-pop-v1") > Date.now()) return; } catch (e) {}
    var P = PROMOS.filter(function (p) { return p.key === (CHAIN === "robinhood" ? "base" : "robinhood"); })[0];
    var el = document.createElement("div"); el.className = "dk-pop"; el.setAttribute("role", "complementary");
    el.innerHTML = '<button type="button" class="dk-pop-x" aria-label="Close">×</button>' +
      '<div class="dk-pop-top"><img src="' + ASSETS + P.logo + '" alt=""><div><b>' + esc(P.name) + ' is live</b><span>' + esc(P.line) + "</span></div></div>" +
      '<a class="dk-pop-cta" href="../' + P.key + '/">Launch on ' + esc(P.name) + " →</a>";
    function close() {
      el.classList.remove("show"); setTimeout(function () { el.remove(); }, 300);
      try { localStorage.setItem("dk-pop-v1", String(Date.now() + 864e5)); } catch (e) {}
    }
    el.querySelector(".dk-pop-x").addEventListener("click", close);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && el.parentNode) close(); });
    setTimeout(function () { document.body.appendChild(el); requestAnimationFrame(function () { el.classList.add("show"); }); }, 3500);
  }

  /* ---------------- Solana: coming-soon pages ---------------- */
  var SOON = {
    "soon-create": { name: "Create Liquidity", ic: "💧", line: "Open a trading pool for your token so people can buy and sell it.", pts: ["Pick the starting price", "Add SOL and your tokens", "Get tradable on Solana DEXs"] },
    "soon-remove": { name: "Remove Liquidity", ic: "🧯", line: "Take your tokens and SOL back out of a pool you created.", pts: ["See your pool positions", "Pull out all or part", "One transaction, you sign it"] }
  };
  function initSoon() {
    var host = document.querySelector(".main-inner"); if (!host) return;
    document.querySelectorAll(".sidebar-item.disabled").forEach(function (it) {
      var key = /Create/i.test(it.textContent) ? "soon-create" : /Remove/i.test(it.textContent) ? "soon-remove" : null;
      if (!key) return;
      var c = SOON[key];
      it.classList.remove("disabled"); it.classList.add("soon-open"); it.dataset.view = key;
      var sec = document.createElement("section"); sec.id = "view-" + key; sec.className = "tool-view";
      sec.innerHTML = '<div class="soon-box"><div class="soon-ic">' + c.ic + '</div><span class="promo-tag">Coming soon</span><h2>' + c.name + "</h2><p>" + c.line + "</p><ul>" +
        c.pts.map(function (x) { return "<li>" + x + "</li>"; }).join("") + '</ul><a class="promo-cta" href="../../support/">Get notified →</a></div>';
      host.appendChild(sec);
      it.addEventListener("click", function () { if (window.switchView) window.switchView(key); });
    });
  }

  function boot() {
    addNews();
    if (CHAIN === "solana") { initMarket(); initSoon(); }
    addPromos();
    addPopup();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
