"use strict";

const $ = (s) => document.querySelector(s);
const CATS = ["productive", "neutral", "distracting"];
const CAT_LABEL = { productive: "Productive", neutral: "Neutral", distracting: "Distracting", idle: "Away" };
const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

const state = { date: null, today: null, rangeDays: 7, filter: "all", logAll: false, day: null, range: [], habits: null, demo: false };

/* ---------- helpers ---------- */
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
function fmt(sec, short = false) {
  sec = Math.round(sec || 0);
  if (sec < 60) return sec + "s";
  const h = Math.floor(sec / 3600), m = Math.round((sec % 3600) / 60);
  if (h === 0) return m + "m";
  if (m === 60) return h + 1 + "h";
  return short || m === 0 ? (m ? `${h}h ${m}m` : `${h}h`) : `${h}h ${m}m`;
}
const clock = (ts) => new Date(ts * 1000).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
const hh = (h) => String(h).padStart(2, "0") + ":00";
const pct = (a, b) => (b ? Math.round((100 * a) / b) : 0);
const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const iso = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
function shiftDate(s, n) { const d = new Date(s + "T12:00:00"); d.setDate(d.getDate() + n); return iso(d); }
async function api(path, body) {
  const r = await fetch(path, body ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } : {});
  return r.json();
}

/* ---------- tooltip ---------- */
const tip = $("#tip");
function showTip(e, html) {
  tip.innerHTML = html;
  tip.classList.add("show");
  const pad = 14, w = tip.offsetWidth, h = tip.offsetHeight;
  let x = e.clientX + pad, y = e.clientY + pad;
  if (x + w > innerWidth - 8) x = e.clientX - w - pad;
  if (y + h > innerHeight - 8) y = e.clientY - h - pad;
  tip.style.left = Math.max(8, x) + "px";
  tip.style.top = Math.max(8, y) + "px";
}
const hideTip = () => tip.classList.remove("show");
const ttRow = (cat, label, val) => `<div class="tt-row"><i class="sw ${cat}"></i>${esc(label)}<b>${val}</b></div>`;

/* ---------- loading ---------- */
async function load() {
  const [day, range, habits] = await Promise.all([
    api(`/api/day?date=${state.date}`),
    api(`/api/range?date=${state.date}&days=${Math.max(state.rangeDays, 8)}`),
    api(`/api/habits?date=${state.date}&days=28`),
  ]);
  Object.assign(state, { day, range, habits });
  render();
}

function render() {
  renderHeader();
  renderKpis();
  renderTimeline();
  renderHourly();
  renderActivities();
  renderTrend();
  renderHabits();
  renderInsights();
  renderLog();
}

function renderHeader() {
  const d = new Date(state.date + "T12:00:00");
  const isToday = state.date === state.today;
  const hr = new Date().getHours();
  $("#greeting").textContent = isToday ? (hr < 12 ? "Good morning" : hr < 18 ? "Good afternoon" : "Good evening") : "Day in review";
  $("#dateLabel").textContent = d.toLocaleDateString([], { weekday: "long", month: "long", day: "numeric", year: "numeric" });
  $("#datePick").value = state.date;
  $("#datePick").max = state.today;
  $("#nextDay").disabled = isToday;
  $("#todayBtn").hidden = isToday;
}

/* ---------- KPIs ---------- */
function weekAvg(key) {
  const past = state.range.slice(0, -1).slice(-7).filter((d) => d.active > 600);
  return past.length ? past.reduce((a, d) => a + d[key], 0) / past.length : null;
}
function delta(cur, avg, goodWhenUp) {
  if (avg == null || avg === 0) return "";
  const p = Math.round(((cur - avg) / avg) * 100);
  if (Math.abs(p) < 3) return `<span>≈ your 7-day average</span>`;
  const good = goodWhenUp ? p > 0 : p < 0;
  return `<span class="${good ? "up" : "down"}">${p > 0 ? "▲" : "▼"} ${Math.abs(p)}%</span> vs 7-day avg`;
}

function renderKpis() {
  const { summary: s, goal_hours } = state.day;
  const score = s.active ? s.focus_score : 0;
  $("#scoreValue").textContent = s.active ? score : "–";
  $("#scoreRing").style.strokeDashoffset = 314.16 * (1 - score / 100);
  const [title, desc] = !s.active ? ["No activity yet", "Use your PC normally — FocusLens records in the background."]
    : score >= 75 ? ["Deep focus day", "Most of your screen time went into real work. Keep this rhythm."]
    : score >= 55 ? ["Solid focus", "Good work time, with a few leaks worth closing."]
    : score >= 35 ? ["Scattered attention", "Work and distraction are mixed. Try longer single-task blocks."]
    : ["Distracted day", "Distractions dominated. Start tomorrow with one protected focus block."];
  $("#scoreTitle").textContent = title;
  $("#scoreDesc").textContent = desc;
  $("#splitBar").innerHTML = CATS.map((c) => `<span style="flex-grow:${s[c]};background:var(--${c})"></span>`).join("");
  $("#splitLegend").innerHTML = CATS.map((c) => `<li><i class="sw ${c}"></i>${CAT_LABEL[c]} <b>${pct(s[c], s.active)}%</b></li>`).join("");

  $("#kActive").textContent = fmt(s.active);
  const d = state.day;
  $("#kActiveFoot").innerHTML = d.first_seen ? `${clock(d.first_seen)} – ${clock(d.last_seen)} · ${fmt(s.idle)} away` : "Nothing recorded";

  $("#kProd").textContent = fmt(s.productive);
  const goal = goal_hours * 3600, gp = Math.min(100, pct(s.productive, goal));
  $("#goalFill").style.width = gp + "%";
  $("#goalText").innerHTML = s.productive >= goal ? `<span class="up">Goal reached</span> · ${fmt(goal)} target` : `${gp}% of ${fmt(goal)} goal · ${delta(s.productive, weekAvg("productive"), true)}`;

  $("#kLost").textContent = fmt(s.distracting);
  $("#kLostFoot").innerHTML = `${pct(s.distracting, s.active)}% of screen time ${weekAvg("distracting") ? "· " + delta(s.distracting, weekAvg("distracting"), false) : ""}`;

  $("#kStreak").textContent = fmt(d.longest_focus);
  const n = d.deep_sessions.length;
  $("#kStreakFoot").textContent = n ? `${n} deep-work block${n > 1 ? "s" : ""} of 25m+` : "No 25m+ deep-work block yet";

  $("#kSwitch").textContent = d.switches;
  $("#kSwitchFoot").textContent = d.switches_per_hour ? `${d.switches_per_hour} per hour · every ~${Math.max(1, Math.round(60 / d.switches_per_hour))} min` : "—";
}

/* ---------- timeline ---------- */
function visibleHours() {
  const d = state.day;
  if (!d.first_seen) return [8, 20];
  const dayStart = new Date(state.date + "T00:00:00").getTime() / 1000;
  let a = Math.floor((d.first_seen - dayStart) / 3600);
  let b = Math.min(24, Math.ceil((d.last_seen - dayStart) / 3600));
  while (b - a < 8) { if (a > 0) a--; if (b - a < 8 && b < 24) b++; if (a === 0 && b === 24) break; }
  return [a, Math.min(24, b)];
}

function renderTimeline() {
  const el = $("#timelineChart");
  const [h0, h1] = visibleHours();
  const t0 = new Date(state.date + "T00:00:00").getTime() / 1000 + h0 * 3600;
  const span = (h1 - h0) * 3600;
  const x = (t) => Math.max(0, Math.min(100, ((t - t0) / span) * 100));
  const segs = state.day.timeline.map((b, i) => {
    const l = x(b.start), w = Math.max(x(b.end) - l, 0.08);
    return `<div class="tl-seg" data-i="${i}" style="left:${l}%;width:${w}%;background:var(--${b.category})"></div>`;
  }).join("");
  const step = h1 - h0 > 14 ? 3 : h1 - h0 > 8 ? 2 : 1;
  let ticks = "";
  for (let h = h0; h <= h1; h += step) ticks += `<span style="left:${((h - h0) / (h1 - h0)) * 100}%">${hh(h % 24)}</span>`;
  const deep = state.day.deep_sessions.map((s) => `<span style="left:${x(s.start)}%;width:${x(s.end) - x(s.start)}%"></span>`).join("");
  el.innerHTML = `<div class="tl-band">${segs}</div><div class="tl-deep">${deep}</div><div class="tl-axis">${ticks}</div>`;
  el.querySelector(".tl-band").onmousemove = (e) => {
    const i = e.target.dataset.i;
    if (i == null) return hideTip();
    const b = state.day.timeline[i];
    showTip(e, `<div class="tt-title">${esc(b.activity)}</div>${ttRow(b.category, CAT_LABEL[b.category], fmt(b.seconds))}<div class="tt-sub">${clock(b.start)} – ${clock(b.end)}${b.app && b.app !== b.activity ? " · " + esc(b.app) : ""}</div>`);
  };
  el.querySelector(".tl-band").onmouseleave = hideTip;
  $("#deepList").innerHTML = state.day.deep_sessions.length
    ? `<span>Deep work:</span>` + state.day.deep_sessions.map((s) => `<span class="chip">${clock(s.start)}–${clock(s.end)} · ${fmt(s.seconds)}</span>`).join("")
    : `<span>Purple marks under the timeline show deep-work blocks (25+ minutes of focused work).</span>`;
}

/* ---------- stacked bar chart (shared by hourly + trend) ---------- */
function topRounded(x, y, w, h, r) {
  r = Math.min(r, w / 2, h);
  return `M${x},${y + h}V${y + r}Q${x},${y} ${x + r},${y}H${x + w - r}Q${x + w},${y} ${x + w},${y + r}V${y + h}Z`;
}
function stackedBars(el, items, { maxY, ticks, tickFmt, topLabel, height = 220 }) {
  const W = Math.max(el.clientWidth, 280), H = height, padL = 40, padB = 24, padT = topLabel ? 18 : 6;
  const plotH = H - padB - padT, n = items.length, slot = (W - padL) / n, bw = Math.max(4, Math.min(36, slot * 0.62));
  const y = (v) => padT + plotH - (v / maxY) * plotH;
  let svg = "";
  ticks.forEach((t) => {
    svg += `<line class="${t === 0 ? "baseline" : "gridline"}" x1="${padL}" x2="${W}" y1="${y(t)}" y2="${y(t)}"/>`;
    svg += `<text x="${padL - 8}" y="${y(t) + 4}" text-anchor="end">${tickFmt(t)}</text>`;
  });
  const labelEvery = Math.ceil(n / Math.floor((W - padL) / 44));
  items.forEach((it, i) => {
    const cx = padL + slot * i + slot / 2, x0 = cx - bw / 2;
    let acc = 0, g = "";
    const parts = CATS.map((c) => [c, it.values[c]]).filter(([, v]) => v > 0);
    parts.forEach(([c, v], j) => {
      const yTop = y(acc + v), hgt = y(acc) - yTop - (j > 0 ? 2 : 0);
      if (hgt > 0.5) {
        g += j === parts.length - 1
          ? `<path class="bar" d="${topRounded(x0, yTop, bw, hgt, 4)}" fill="var(--${c})"/>`
          : `<rect class="bar" x="${x0}" y="${yTop}" width="${bw}" height="${hgt}" fill="var(--${c})"/>`;
      }
      acc += v;
    });
    if (topLabel && it.top) g += `<text class="score-lbl" x="${cx}" y="${y(acc) - 6}" text-anchor="middle">${it.top}</text>`;
    if (i % labelEvery === 0) g += `<text x="${cx}" y="${H - 6}" text-anchor="middle">${esc(it.label)}</text>`;
    svg += `<g class="col" data-i="${i}"><rect class="hit" x="${padL + slot * i}" y="0" width="${slot}" height="${H - padB}"/>${g}</g>`;
  });
  el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" height="${H}" role="img">${svg}</svg>`;
  const s = el.querySelector("svg");
  s.onmousemove = (e) => {
    const col = e.target.closest(".col");
    s.querySelectorAll(".col").forEach((c) => c.classList.toggle("dim", !!col && c !== col));
    if (!col) return hideTip();
    showTip(e, items[col.dataset.i].tip);
  };
  s.onmouseleave = () => { hideTip(); s.querySelectorAll(".col").forEach((c) => c.classList.remove("dim")); };
}

function renderHourly() {
  const [h0, h1] = visibleHours();
  const items = state.day.hourly.slice(h0, h1).map((h) => {
    const tot = h.productive + h.neutral + h.distracting;
    return {
      label: hh(h.hour).slice(0, 2), values: { productive: h.productive / 60, neutral: h.neutral / 60, distracting: h.distracting / 60 },
      tip: `<div class="tt-title">${hh(h.hour)} – ${hh((h.hour + 1) % 24)}</div>` + CATS.map((c) => ttRow(c, CAT_LABEL[c], fmt(h[c]))).join("") + `<div class="tt-sub">${fmt(tot)} active</div>`,
    };
  });
  stackedBars($("#hourlyChart"), items, { maxY: 60, ticks: [0, 15, 30, 45, 60], tickFmt: (t) => t + "m", height: 200 });
}

/* ---------- activities ---------- */
const AVATAR = { productive: "var(--productive)", neutral: "var(--neutral)", distracting: "var(--distracting)" };
function renderActivities() {
  const list = state.day.activities.filter((a) => state.filter === "all" || a.category === state.filter);
  const el = $("#actList");
  if (!list.length) { el.innerHTML = `<div class="empty">No activities here yet.</div>`; return; }
  const max = list[0].seconds, active = state.day.summary.active;
  el.innerHTML = list.slice(0, 40).map((a, i) => `
    <div class="act" data-i="${i}">
      <div class="avatar" style="background:${AVATAR[a.category]}">${esc(a.name.trim()[0] || "?").toUpperCase()}</div>
      <div class="act-name"><strong title="${esc(a.name)}">${esc(a.name)}</strong><span>${esc(a.app)} · ${a.sessions} session${a.sessions === 1 ? "" : "s"}</span></div>
      <div class="act-bar"><span style="width:${Math.max(2, (a.seconds / max) * 100)}%;background:var(--${a.category})"></span></div>
      <div class="act-time"><strong>${fmt(a.seconds)}</strong><span>${pct(a.seconds, active)}%</span></div>
      <div class="cat-wrap"><select class="cat-select" data-name="${esc(a.name)}" aria-label="Category for ${esc(a.name)}">
        ${CATS.map((c) => `<option value="${c}" ${c === a.category ? "selected" : ""}>${CAT_LABEL[c]}</option>`).join("")}
      </select></div>
      <button class="expand" aria-label="Show window titles"><svg viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg></button>
      <div class="titles">${a.titles.length ? a.titles.map((t) => `<div><span title="${esc(t.title)}">${esc(t.title)}</span><span>${fmt(t.seconds)}</span></div>`).join("") : "<div>No window titles</div>"}</div>
    </div>`).join("");
  el.querySelectorAll(".expand").forEach((b) => (b.onclick = () => b.closest(".act").classList.toggle("open")));
  el.querySelectorAll(".cat-select").forEach((s) => (s.onchange = async () => {
    await api("/api/override", { activity: s.dataset.name, category: s.value });
    load();
  }));
}

/* ---------- trend ---------- */
function renderTrend() {
  const days = state.range.slice(-state.rangeDays);
  const maxH = Math.max(1, ...days.map((d) => d.active / 3600));
  const top = Math.ceil(maxH / 2) * 2, step = top > 8 ? 4 : 2;
  const ticks = []; for (let t = 0; t <= top; t += step) ticks.push(t);
  const items = days.map((d) => {
    const dt = new Date(d.date + "T12:00:00");
    return {
      label: state.rangeDays <= 7 ? DAYS[(dt.getDay() + 6) % 7] : `${dt.getDate()}/${dt.getMonth() + 1}`,
      values: { productive: d.productive / 3600, neutral: d.neutral / 3600, distracting: d.distracting / 3600 },
      top: state.rangeDays <= 14 && d.active ? d.focus_score : "",
      tip: `<div class="tt-title">${dt.toLocaleDateString([], { weekday: "short", month: "short", day: "numeric" })}</div>` +
        CATS.map((c) => ttRow(c, CAT_LABEL[c], fmt(d[c]))).join("") + `<div class="tt-sub">Focus score ${d.active ? d.focus_score : "–"}</div>`,
    };
  });
  stackedBars($("#trendChart"), items, { maxY: Math.max(top, ticks[ticks.length - 1]), ticks, tickFmt: (t) => t + "h", topLabel: true, height: 240 });
  const tracked = days.filter((d) => d.active > 600);
  const avg = (k) => (tracked.length ? tracked.reduce((a, d) => a + d[k], 0) / tracked.length : 0);
  const best = tracked.reduce((b, d) => (!b || d.focus_score > b.focus_score ? d : b), null);
  $("#trendStats").innerHTML = `
    <div><span>Avg productive / day</span><strong>${fmt(avg("productive"))}</strong></div>
    <div><span>Avg lost / day</span><strong>${fmt(avg("distracting"))}</strong></div>
    <div><span>Avg focus score</span><strong>${Math.round(avg("focus_score"))}</strong></div>
    <div><span>Best day</span><strong>${best ? new Date(best.date + "T12:00:00").toLocaleDateString([], { weekday: "short", day: "numeric" }) + " · " + best.focus_score : "–"}</strong></div>`;
}

/* ---------- habits ---------- */
function renderHabits() {
  const h = state.habits;
  const max = Math.max(1, ...h.heatmap.map((c) => c.distracting));
  let html = `<span></span>`;
  for (let c = 0; c < 24; c++) html += `<span class="cl">${c % 3 === 0 ? c : ""}</span>`;
  for (let wd = 0; wd < 7; wd++) {
    html += `<span class="rl">${DAYS[wd]}</span>`;
    for (let c = 0; c < 24; c++) {
      const cell = h.heatmap[wd * 24 + c], p = Math.round((cell.distracting / max) * 100);
      const bg = cell.distracting > 0 ? `background:color-mix(in oklab, var(--distracting) ${12 + p * 0.88}%, var(--surface-2))` : "";
      html += `<div class="cell" data-i="${wd * 24 + c}" style="${bg}"></div>`;
    }
  }
  const el = $("#heatmap");
  el.innerHTML = html;
  el.onmousemove = (e) => {
    const i = e.target.dataset.i;
    if (i == null) return hideTip();
    const c = h.heatmap[i];
    showTip(e, `<div class="tt-title">${DAYS[c.weekday]} · ${hh(c.hour)}</div>` +
      CATS.map((k) => ttRow(k, CAT_LABEL[k], Math.round(c[k]) + "m")).join("") + `<div class="tt-sub">Average per ${DAYS[c.weekday]}</div>`);
  };
  el.onmouseleave = hideTip;
  $("#triggers").innerHTML = (h.triggers.length
    ? h.triggers.map((t) => `<li><i class="sw productive"></i>${esc(t.from)} <span class="arrow">→</span> <i class="sw distracting"></i>${esc(t.to)}<span class="n">${t.count}×</span></li>`).join("")
    : `<li>No pattern yet — keep tracking for a few days.</li>`) +
    (h.distraction_episodes ? `<li>Once distracted, you stay away for <b>&nbsp;${fmt(h.avg_distraction_episode)}&nbsp;</b> on average<span class="n">${h.distraction_episodes} episodes</span></li>` : "");
}

/* ---------- insights ---------- */
function renderInsights() {
  const d = state.day, s = d.summary, out = [];
  const add = (ic, title, text) => out.push(`<li><span class="ic">${ic}</span><div><strong>${title}</strong><p>${text}</p></div></li>`);
  if (!s.active) {
    add("👋", "Just getting started", "Insights appear after a little activity. Leave FocusLens running in the background.");
  } else {
    const best = d.hourly.reduce((b, h) => (h.productive > b.productive ? h : b));
    if (best.productive > 600) add("⚡", `Peak focus: ${hh(best.hour)}–${hh((best.hour + 1) % 24)}`, `${fmt(best.productive)} of real work in that hour. Schedule your hardest task here.`);
    const sink = d.activities.find((a) => a.category === "distracting");
    if (sink) add("🕳️", `Biggest time sink: ${esc(sink.name)}`, `${fmt(sink.seconds)} today — ${pct(sink.seconds, s.distracting)}% of your lost time. Consider a site blocker during work hours.`);
    const worst = d.hourly.reduce((b, h) => (h.distracting > b.distracting ? h : b));
    if (worst.distracting > 600) add("📉", `Distraction peaks at ${hh(worst.hour)}`, `${fmt(worst.distracting)} lost in that hour. Plan a real break (walk, water) just before it.`);
    if (d.switches_per_hour >= 20) add("🔀", "Fragmented attention", `You switch context about every ${Math.max(1, Math.round(60 / d.switches_per_hour))} minutes. Close chat apps and batch messages twice a day.`);
    else if (d.switches_per_hour > 0) add("🎯", "Steady attention", `Only ${d.switches_per_hour} switches per hour — nice single-tasking.`);
    if (!d.deep_sessions.length && s.active > 3600) add("⏱️", "No deep-work block yet", "Try one 25-minute block on a single task with notifications off.");
    else if (d.deep_sessions.length) add("🧠", `${d.deep_sessions.length} deep-work block${d.deep_sessions.length > 1 ? "s" : ""}`, `Longest uninterrupted focus: ${fmt(d.longest_focus)}.`);
    const avg = weekAvg("productive");
    if (avg) {
      const diff = s.productive - avg;
      add(diff >= 0 ? "📈" : "🔻", diff >= 0 ? "Above your average" : "Below your average", `${fmt(Math.abs(diff))} ${diff >= 0 ? "more" : "less"} productive time than your 7-day average (${fmt(avg)}).`);
    }
  }
  const t = state.habits.triggers[0];
  if (t) add("🔁", "Habit loop detected", `After ${esc(t.from)} you often jump to ${esc(t.to)} (${t.count}× in 4 weeks). Notice the urge and take a 1-minute stretch instead.`);
  $("#insights").innerHTML = out.slice(0, 6).join("");
}

/* ---------- log ---------- */
function renderLog() {
  const rows = state.day.timeline.filter((b) => b.seconds >= 5).slice().reverse();
  const shown = state.logAll ? rows : rows.slice(0, 15);
  $("#logBody").innerHTML = shown.length ? shown.map((b) => `<tr><td>${clock(b.start)}</td><td>${clock(b.end)}</td><td>${fmt(b.seconds)}</td><td>${esc(b.activity)}</td><td>${esc(b.app || "—")}</td><td><i class="sw ${b.category}"></i>${CAT_LABEL[b.category]}</td></tr>`).join("")
    : `<tr><td colspan="6" class="empty">No sessions recorded for this day.</td></tr>`;
  $("#logToggle").hidden = rows.length <= 15;
  $("#logToggle").textContent = state.logAll ? "Show less" : `Show all ${rows.length}`;
}

/* ---------- wiring ---------- */
function setDate(d) { state.date = d > state.today ? state.today : d; load(); }
$("#prevDay").onclick = () => setDate(shiftDate(state.date, -1));
$("#nextDay").onclick = () => setDate(shiftDate(state.date, 1));
$("#todayBtn").onclick = () => setDate(state.today);
$("#datePick").onchange = (e) => e.target.value && setDate(e.target.value);
$("#logToggle").onclick = () => { state.logAll = !state.logAll; renderLog(); };
$("#actFilter").onclick = (e) => {
  const b = e.target.closest("button"); if (!b) return;
  state.filter = b.dataset.f;
  $("#actFilter").querySelectorAll("button").forEach((x) => x.classList.toggle("on", x === b));
  renderActivities();
};
$("#rangeSeg").onclick = (e) => {
  const b = e.target.closest("button"); if (!b) return;
  state.rangeDays = +b.dataset.d;
  $("#rangeSeg").querySelectorAll("button").forEach((x) => x.classList.toggle("on", x === b));
  load();
};
$("#themeBtn").onclick = () => {
  const cur = document.documentElement.dataset.theme || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  const next = cur === "dark" ? "light" : "dark";
  document.documentElement.dataset.theme = next;
  try { localStorage.setItem("fl-theme", next); } catch (e) {}
};
$("#settingsBtn").onclick = async () => {
  const { settings } = await api("/api/config");
  $("#sGoal").value = settings.goal_hours; $("#sIdle").value = settings.idle_minutes; $("#sMedia").value = settings.media_idle_minutes;
  $("#settings").showModal();
};
$("#sSave").onclick = async (e) => {
  e.preventDefault();
  await api("/api/settings", { goal_hours: +$("#sGoal").value, idle_minutes: +$("#sIdle").value, media_idle_minutes: +$("#sMedia").value });
  $("#settings").close();
  load();
};

let resizeT;
addEventListener("resize", () => { clearTimeout(resizeT); resizeT = setTimeout(() => state.day && (renderHourly(), renderTrend()), 150); });

const navLinks = [...document.querySelectorAll("nav a")];
const io = new IntersectionObserver((entries) => entries.forEach((en) => {
  if (en.isIntersecting) navLinks.forEach((a) => a.classList.toggle("active", a.getAttribute("href") === "#" + en.target.id));
}), { rootMargin: "-30% 0px -60% 0px" });
navLinks.forEach((a) => { const t = document.querySelector(a.getAttribute("href")); if (t) io.observe(t); });

(async function init() {
  const cfg = await api("/api/config");
  state.today = state.date = cfg.today;
  state.demo = cfg.demo;
  $("#demoBadge").hidden = !cfg.demo;
  if (cfg.demo) $("#liveText").textContent = "Demo mode — not tracking";
  await load();
  setInterval(() => { if (state.date === state.today && !document.hidden) load(); }, 60000);
})();
