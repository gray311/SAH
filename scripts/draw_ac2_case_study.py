#!/usr/bin/env python3
"""AC2 case-study figure: three reward routes with audited event nodes.

Data: papers/figures/reward_route_requested5_latest_data.json
(displayed_common_budget_series, eft__math__second_autocorr_ineq).
y = gap to human best in percent.  Layout: chart left, numbered node
panel right; markers on the curves carry the numbers.
"""
import json
import textwrap
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
     dict(color="#084594", ls="-",  lw=2.4, marker="o", ms=4.5, zorder=9)),
    ("context", "Analyzer context (weights frozen)",
     dict(color="#8a8a8a", ls="-.", lw=1.9, marker="^", ms=4.5, zorder=7)),
    ("executor", "Update executor weights (fixed H2)",
     dict(color="#e07b28", ls="--", lw=1.9, marker="s", ms=4.5, zorder=8)),
]
STYLE = {k: st for k, _, st in ROUTES}

NODES = [
    ("1", 6, "proposer_full",
     "Multi-start initialization: the proposer edits system prompt + "
     "skill, widening the search space."),
    ("2", 8, "context",
     "A brief is evidence read through a frozen policy: it can shift what "
     "the proposer believes, not how it decides.  RL moves the policy "
     "itself (node 1); here the frozen policy rebuilds the weak 0.955 "
     "seed -- 20/20 evals, below the shared start."),
    ("3", 13, "proposer_full",
     "Machinery only this route can add: inherited skills force "
     "diversity -- cycle 8-12 step-function families, reinitializing "
     "every 100-300 steps instead of riding one basin; this jump's seed "
     "traces to them by hash.  The proposer even writes the rule as "
     "code: an enforce_diversification middleware forces a family switch "
     "after 5 stalled iterations, and a new function class after 3 "
     "stalled families.  Executor updates keep the harness fixed and "
     "cannot author any of this."),
]

def render(active, outputs):
    fig = plt.figure(figsize=(11.8, 4.9))
    gs = fig.add_gridspec(1, 2, width_ratios=[0.60, 0.40],
                          left=0.06, right=0.985, top=0.955, bottom=0.115,
                          wspace=0.06)
    ax = fig.add_subplot(gs[0])
    for key, label, st in ROUTES:
        pts = S[key]
        ax.step([p["x"] for p in pts], [gap(p["score"]) for p in pts],
                where="post", label=label, **st)
    ax.axhline(0.0, color="#555555", lw=1.0, ls=":", zorder=2)
    ax.text(1.2, 0.06, "human best", fontsize=8.5, color="#555555",
            va="bottom")
    ax.axvline(B, color="#bbbbbb", lw=1.0, ls="--", zorder=1)
    ax.text(B - 0.7, -2.55, f"common budget $B{{=}}{B}$", fontsize=8,
            color="#888888", rotation=90, ha="right", va="bottom")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Gap to human best (%)")
    ax.set_xlim(0.5, B + 1.5)
    ax.grid(color="#e8e8e8", lw=0.7)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(loc="lower right", bbox_to_anchor=(0.995, 0.03), fontsize=8.6,
              frameon=False, handlelength=2.2)

    shown = [n for n in NODES if n[0] in active]
    for num, x, route, _ in shown:
        pts = S[route]
        exact = [p for p in pts if p["x"] == x]
        y = gap(exact[0]["score"]) if exact else \
            gap(max(p["score"] for p in pts if p["x"] <= x))
        c = STYLE[route]["color"]
        ax.plot(x, y, marker="o", ms=12.5, mfc="white", mec=c, mew=1.8,
                zorder=11)
        ax.text(x, y, num, ha="center", va="center", fontsize=8, color=c,
                weight="bold", zorder=12)

    # ---- right panel: numbered node texts ----
    px = fig.add_subplot(gs[1]); px.axis("off")
    px.set_xlim(0, 1); px.set_ylim(0, 1)
    y = 0.985
    for num, _, route, text in shown:
        c = STYLE[route]["color"]
        lines = textwrap.wrap(text, width=54)
        h = 0.052 * len(lines) + 0.035
        px.add_patch(plt.Rectangle((0.015, y - h), 0.97, h, fill=True,
                     fc="white", ec=c, lw=1.0, zorder=2,
                     transform=px.transAxes, clip_on=False))
        px.add_patch(plt.Circle((0.055, y - 0.033), 0.021, fc="white",
                     ec=c, lw=1.6, zorder=3, transform=px.transAxes,
                     clip_on=False))
        px.text(0.055, y - 0.033, num, ha="center", va="center", fontsize=8,
                color=c, weight="bold", zorder=4, transform=px.transAxes)
        px.text(0.10, y - 0.018, "\n".join(lines), ha="left", va="top",
                fontsize=8.3, color="#333333", zorder=3, linespacing=1.25,
                transform=px.transAxes)
        y -= h + 0.028
    for out in outputs:
        fig.savefig(out, dpi=200)
    plt.close(fig)
    print("wrote", outputs[0].rsplit("/", 1)[-1])

render({"1"}, ("papers/figures/ac2_case_study_node1.pdf",
               "papers/figures/ac2_case_study_node1.png"))
render({"1", "2"}, ("papers/figures/ac2_case_study_node2.pdf",
                    "papers/figures/ac2_case_study_node2.png"))
render({"1", "2", "3"}, ("papers/figures/ac2_case_study.pdf",
                         "papers/figures/ac2_case_study.png"))
