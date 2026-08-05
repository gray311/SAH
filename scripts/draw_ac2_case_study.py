#!/usr/bin/env python3
"""AC2 case-study figure, rebuilt step by step.

Data: papers/figures/reward_route_requested5_latest_data.json
(displayed_common_budget_series for eft__math__second_autocorr_ineq).
y = gap to human best in percent: (score/human_best - 1) * 100.
Step 1: the clean base chart -- three routes, human-best baseline,
shared-H2 start, common-budget cutoff.
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = json.load(open("papers/figures/reward_route_requested5_latest_data.json"))
T = D["tasks"]["eft__math__second_autocorr_ineq"]
HB = T["human_best_combined_score"]
B  = T["common_trajectory_budget"]
S  = T["displayed_common_budget_series"]

def gap(s): return (s / HB - 1.0) * 100.0

ROUTES = [
    ("proposer_full", "Update proposer weights (ours)",
     dict(color="#084594", ls="-",  lw=2.6, marker="o", ms=5, zorder=9)),
    ("context", "Analyzer context (weights frozen)",
     dict(color="#8a8a8a", ls="-.", lw=2.0, marker="^", ms=5, zorder=7)),
    ("executor", "Update executor weights (fixed H2)",
     dict(color="#e07b28", ls="--", lw=2.0, marker="s", ms=5, zorder=8)),
]

fig, ax = plt.subplots(figsize=(7.6, 4.4))
for key, label, st in ROUTES:
    pts = S[key]
    xs = [p["x"] for p in pts]
    ys = [gap(p["score"]) for p in pts]
    ax.step(xs, ys, where="post", label=label, **st)

ax.axhline(0.0, color="#555555", lw=1.0, ls=":", zorder=2)
ax.text(1.2, 0.06, "human best", fontsize=9, color="#555555", va="bottom")
ax.axvline(B, color="#bbbbbb", lw=1.0, ls="--", zorder=1)
ax.text(B - 0.6, ax.get_ylim()[0] + 0.1, f"common budget $B{{=}}{B}$",
        fontsize=8.5, color="#888888", rotation=90, ha="right", va="bottom")

# ---- audited event nodes (added step by step) ------------------------------
# Each: (x, route_key, circled number, short mechanism text, text_xy)
NODES = [
    (6, "proposer_full", "1",
     "Multi-start initialization:\nproposer edits system prompt + skill,\n"
     "widening the search space",
     (2.0, 1.05)),
    (8, "context", "2",
     "Context carries information, not behavior:\nboth arms see the same incumbent, but a\n"
     "brief cannot reshape what the frozen\nproposer tends to propose -- its H2 stays\n"
     "near the base prior, rebuilding the weak\n0.955 seed (20/20 evals, below the start)",
     (8.2, -1.62)),
]
ROUTE_STYLE = {k: st for k, _, st in ROUTES}
for x, route, num, text, txy in NODES:
    pts = S[route]
    exact = [p for p in pts if p["x"] == x]
    y = gap(exact[0]["score"]) if exact else gap(max(p["score"] for p in pts if p["x"] <= x))
    c = ROUTE_STYLE[route]["color"]
    ax.plot(x, y, marker="o", ms=13, mfc="white", mec=c, mew=1.8, zorder=11)
    ax.text(x, y, num, ha="center", va="center", fontsize=8.5, color=c,
            weight="bold", zorder=12)
    ax.annotate(text, xy=(x, y), xytext=txy, fontsize=8.2, color="#333333",
                ha="left", va="center", zorder=10,
                arrowprops=dict(arrowstyle="-", color=c, lw=1.0,
                                shrinkA=2, shrinkB=8,
                                connectionstyle="arc3,rad=0.15"),
                bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=c,
                          lw=0.9, alpha=0.95))

ax.set_xlabel("Executor trajectories (incl. shared fixed-harness start)")
ax.set_ylabel("Gap to human best (%)")
ax.set_xlim(0.5, B + 1.5)
ax.grid(color="#e8e8e8", lw=0.7)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.legend(loc="lower right", bbox_to_anchor=(0.99, 0.06), fontsize=9.5, frameon=False)
fig.tight_layout()
for out in ("papers/figures/ac2_case_study.pdf", "papers/figures/ac2_case_study.png"):
    fig.savefig(out, dpi=200)
print("wrote ac2_case_study.{pdf,png}")
