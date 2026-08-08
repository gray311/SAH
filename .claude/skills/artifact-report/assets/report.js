/* artifact-report — inline this whole file into the report's <script> block.
   No dependencies, no CDN: the report has to open from a file:// URL on a
   cluster login node with no network.

   Provides: tip(), dotPlot(), divergingBars(), decomposition(), initTheme().
   All three chart helpers read colors from the CSS custom properties in
   report.css, so they follow the light/dark toggle for free.

   The report body supplies the data as a literal array read out of the
   artifacts. Never fetch() — a fetch breaks under file:// and, worse, lets a
   number reach the page without a human having read it out of the artifact. */

const NS = "http://www.w3.org/2000/svg";
const el = (n, a = {}) => { const e = document.createElementNS(NS, n); for (const k in a) e.setAttribute(k, a[k]); return e; };

/* ---------- hover tooltip (shared by every chart) ----------
   Requires <div class="tt" id="tt"><div class="tth"></div><div class="ttr"></div></div>
   as the last element in <body>. `rows` is an HTML string; use <br> between lines. */
function tip(node, head, rows) {
  const tt = document.getElementById("tt");
  node.addEventListener("mousemove", e => {
    tt.querySelector(".tth").textContent = head;
    tt.querySelector(".ttr").innerHTML = rows;
    tt.style.opacity = 1;
    const r = tt.getBoundingClientRect();
    let x = e.clientX + 14, y = e.clientY + 14;
    if (x + r.width  > innerWidth  - 8) x = e.clientX - r.width  - 14;
    if (y + r.height > innerHeight - 8) y = e.clientY - r.height - 14;
    tt.style.left = x + "px"; tt.style.top = y + "px";
  });
  node.addEventListener("mouseleave", () => tt.style.opacity = 0);
}

/* ---------- dot plot ----------
   For a magnitude that lives in a narrow band far from zero (scores near 1.0).
   A bar chart would need a truncated baseline, which is a lie; a dot plot is
   allowed a non-zero axis because the mark encodes position, not length.

   opts = {
     rows:   [{label, value, tipHead, tipRows, flag?}],  // flag appends "✦" to the label
     lo, hi,                                             // axis domain
     ticks:  [numbers],
     refs:   [{value, text, side:-1|1}],                 // dashed reference lines
     origin: number,                                     // stems drawn from here
     fmt:    v => string,                                // data-label format
     tickFmt: v => string,                               // axis-tick format (defaults to fmt)
     axis:   "label under the axis"
   } */
function dotPlot(svg, o) {
  const W = 700, H = +(svg.getAttribute("viewBox").split(" ")[3]);
  const L = 72, R = 62, T = 16, B = 44, iw = W - L - R, ih = H - T - B;
  const x = v => L + (v - o.lo) / (o.hi - o.lo) * iw;
  const step = ih / o.rows.length;

  o.ticks.forEach(t => {
    svg.appendChild(el("line", { x1: x(t), x2: x(t), y1: T, y2: T + ih, class: "grid-line" }));
    const lab = el("text", { x: x(t), y: T + ih + 18, class: "tick", "text-anchor": "middle" });
    lab.textContent = (o.tickFmt || o.fmt || String)(t); svg.appendChild(lab);
  });
  (o.refs || []).forEach(r => {
    svg.appendChild(el("line", { x1: x(r.value), x2: x(r.value), y1: T - 6, y2: T + ih + 4, class: "refline" }));
    const t2 = el("text", { x: x(r.value) + r.side * 5, y: T + ih + 34, class: "reftext",
                            "text-anchor": r.side < 0 ? "start" : "end" });
    t2.textContent = r.text; svg.appendChild(t2);
  });

  o.rows.forEach((d, i) => {
    const yy = T + step * i + step / 2;
    svg.appendChild(el("line", { x1: x(o.origin), x2: x(d.value), y1: yy, y2: yy,
      stroke: "var(--border-strong)", "stroke-width": 2, "stroke-linecap": "round" }));
    svg.appendChild(el("circle", { cx: x(d.value), cy: yy, r: 6, fill: "var(--series-1)",
      stroke: "var(--surface-1)", "stroke-width": 2 }));
    const cat = el("text", { x: L - 14, y: yy + 4, class: "cat", "text-anchor": "end" });
    cat.textContent = d.label + (d.flag ? " ✦" : ""); svg.appendChild(cat);
    const val = el("text", { x: x(d.value) + 11, y: yy + 4, class: "dlabel" });
    val.textContent = o.fmt ? o.fmt(d.value) : d.value; svg.appendChild(val);
    const hb = el("rect", { x: L, y: yy - step / 2, width: iw, height: step, class: "hitbox" });
    svg.appendChild(hb); tip(hb, d.tipHead, d.tipRows);
  });

  svg.appendChild(el("line", { x1: L, x2: L + iw, y1: T + ih, y2: T + ih, class: "axis-line" }));
  const ax = el("text", { x: L + iw / 2, y: T + ih + 34, class: "reftext", "text-anchor": "middle" });
  ax.textContent = o.axis; svg.appendChild(ax);
}

/* ---------- diverging bars ----------
   For a signed quantity around a TRUE zero (advantages, deltas, effects). Bars
   are correct here precisely because zero is meaningful. Sign carries the
   meaning, so the two hues must be the diverging pair, never two categoricals.

   opts = { rows: [{label, value, tipHead, tipRows}], max, ticks, fmt, tickFmt, axis } */
function divergingBars(svg, o) {
  const W = 700, H = +(svg.getAttribute("viewBox").split(" ")[3]);
  const L = 72, R = 24, T = 16, B = 44, iw = W - L - R, ih = H - T - B;
  const x = v => L + (v + o.max) / (2 * o.max) * iw;
  const step = ih / o.rows.length, bh = Math.min(20, step * 0.56);

  o.ticks.forEach(t => {
    svg.appendChild(el("line", { x1: x(t), x2: x(t), y1: T, y2: T + ih,
      class: t === 0 ? "axis-line" : "grid-line" }));
    const lab = el("text", { x: x(t), y: T + ih + 18, class: "tick", "text-anchor": "middle" });
    lab.textContent = (o.tickFmt || o.fmt || String)(t); svg.appendChild(lab);
  });

  o.rows.forEach((d, i) => {
    const yy = T + step * i + step / 2, pos = d.value >= 0;
    const x0 = pos ? x(0) + 1 : x(d.value);
    const w = Math.max(2, Math.abs(x(d.value) - x(0)) - 1);
    svg.appendChild(el("rect", { x: x0, y: yy - bh / 2, width: w, height: bh, rx: 4,
      fill: pos ? "var(--series-1)" : "var(--series-2)" }));
    const cat = el("text", { x: L - 14, y: yy + 4, class: "cat", "text-anchor": "end" });
    cat.textContent = d.label; svg.appendChild(cat);
    const val = el("text", { x: pos ? x(d.value) + 9 : x(d.value) - 9, y: yy + 4,
      class: "dlabel", "text-anchor": pos ? "start" : "end" });
    val.textContent = (pos ? "+" : "") + (o.fmt ? o.fmt(d.value) : d.value); svg.appendChild(val);
    const hb = el("rect", { x: L, y: yy - step / 2, width: iw, height: step, class: "hitbox" });
    svg.appendChild(hb); tip(hb, d.tipHead, d.tipRows);
  });

  const ax = el("text", { x: L + iw / 2, y: T + ih + 34, class: "reftext", "text-anchor": "middle" });
  ax.textContent = o.axis; svg.appendChild(ax);
}

/* ---------- decomposition bar ----------
   One quantity split into parts that sum to it — "how much of this gain is
   actually attributable to X". Stacks from a true zero, so segment widths are
   directly comparable. Reserve R for the outside label of the small segment;
   a narrow segment cannot hold a label inside it.

   opts = {
     segments: [{value, fill, tipHead, tipRows, inLabel?, outLabel?}],
     caption:  "text above the bar",
     endLabel: "right-hand axis label",
     R:        right margin in viewBox units (default 168)
   } */
function decomposition(svg, o) {
  const W = 700, H = +(svg.getAttribute("viewBox").split(" ")[3]);
  const L = 4, R = o.R ?? 168, T = 26, B = 30, iw = W - L - R;
  const bh = 44, yy = T + 6;
  const total = o.segments.reduce((s, d) => s + d.value, 0);

  let cx = L;
  o.segments.forEach(s => {
    const w = iw * s.value / total;
    const r = el("rect", { x: cx, y: yy, width: Math.max(3, w - 1), height: bh, rx: 4, fill: s.fill });
    svg.appendChild(r); tip(r, s.tipHead, s.tipRows);
    if (s.inLabel) {
      const t = el("text", { x: cx + w / 2, y: yy + bh / 2 + 5, class: "dlabel",
        "text-anchor": "middle", "font-weight": "600" });
      t.textContent = s.inLabel; svg.appendChild(t);
    }
    cx += w + 1;
  });
  const last = o.segments[o.segments.length - 1];
  if (last.outLabel) {
    const t = el("text", { x: cx + 11, y: yy + bh / 2 + 5, class: "dlabel", "font-weight": "600" });
    t.textContent = last.outLabel; svg.appendChild(t);
  }
  const cap = el("text", { x: L, y: T - 8, class: "reftext" });
  cap.textContent = o.caption; svg.appendChild(cap);

  svg.appendChild(el("line", { x1: L, x2: L + iw, y1: yy + bh + 10, y2: yy + bh + 10, class: "axis-line" }));
  [[L, "0", "start"], [L + iw, o.endLabel, "end"]].forEach(([xx, t, anchor]) => {
    const l2 = el("text", { x: xx, y: yy + bh + 26, class: "tick", "text-anchor": anchor });
    l2.textContent = t; svg.appendChild(l2);
  });
}

/* ---------- theme ----------
   Defaults to the OS setting, then a button toggles it. Dark is a selected set
   of steps (see report.css), not an automatic inversion. */
function initTheme(btnId = "themeBtn") {
  const root = document.documentElement, btn = document.getElementById(btnId);
  if (matchMedia("(prefers-color-scheme: dark)").matches) root.setAttribute("data-theme", "dark");
  btn.addEventListener("click", () =>
    root.setAttribute("data-theme", root.getAttribute("data-theme") === "dark" ? "light" : "dark"));
}
