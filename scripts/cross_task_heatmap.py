#!/usr/bin/env python3
r"""Cross-task proposer transfer as a heatmap.

Cell (i,j): percentage change in Best@6 on target task j when the harness is
proposed by the adapter trained on source task i, relative to the untrained base
proposer on the same task. Rows are zero-shot -- the adapter is used as-is, from
the same fixed initial harness and seed program, with no inheritance, history, or
analyst pass -- so a cell isolates what the adapter itself carries.
"""
import json, os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

RUN = os.environ.get("RUN_ROOT") or "/lustre/fsw/portfolios/av/users/yingzim/runs"
OUT = f"{RUN}/self_adapt_harness/outer"; WS = f"{RUN}/self_adapt_harness/cross_task"
SHORT = {"eft__math__erdos_min_overlap":"Erd","eft__math__first_autocorr_ineq":"AC1",
 "eft__math__second_autocorr_ineq":"AC2","eft__math__circle_packing":"CP",
 "eft__math__hadamard_maximal_det":"Had","eft__ahc_simpletes__ahc039":"a039",
 "eft__ahc_simpletes__ahc058":"a058","adrs__eplb":"EPLB","adrs__prism":"PRI",
 "adrs__llm_sql":"SQL","adrs__txn_scheduling":"Txn"}
SRC2TASK = {"erdosmin":"Erd","firstaut":"AC1","secondau":"AC2","circlepa":"CP",
 "hadamard":"Had","ahc039":"a039","ahc058":"a058","eplb":"EPLB","prism":"PRI",
 "llmsql":"SQL","txnsched":"Txn"}

merged, order = {}, []
for fn in ("rows.txt", "rows2.txt"):
    p = os.path.join(WS, fn)
    if not os.path.exists(p): continue
    for line in open(p):
        pr = line.split()
        if len(pr) < 3: continue
        src, rnd = pr[0], pr[1]
        f = os.path.join(OUT, f"round{int(rnd):03d}", "round_summary.json")
        if not os.path.exists(f): continue
        for t, v in json.load(open(f))["groups"].items():
            s = v.get("best_score")
            if s is None: continue
            merged.setdefault(src, {}); 
            if src not in order: order.append(src)
            merged[src][t] = s if t not in merged[src] else max(merged[src][t], s)

base = merged.get("BASE", {})
tasks = [t for t in SHORT if any(t in merged[s] for s in merged)]
srcs = [s for s in order if s != "BASE"]

M = np.full((len(srcs), len(tasks)), np.nan)
for i, s in enumerate(srcs):
    for j, t in enumerate(tasks):
        v, b = merged[s].get(t), base.get(t)
        if v is None or b in (None, 0) or v == 0: continue
        M[i, j] = 100.0 * (v - b) / abs(b)

# ahc058's base is ~0, so its ratios explode and would wash out the colour scale
a058 = tasks.index("eft__ahc_simpletes__ahc058") if "eft__ahc_simpletes__ahc058" in tasks else None
Mc = M.copy()
if a058 is not None: Mc[:, a058] = np.nan
lim = float(np.nanpercentile(np.abs(Mc), 95)) if np.isfinite(Mc).any() else 10.0
lim = max(lim, 2.0)

fig, ax = plt.subplots(figsize=(10.5, 7.2), constrained_layout=True)
im = ax.imshow(Mc, cmap="RdBu_r", norm=TwoSlopeNorm(vmin=-lim, vcenter=0, vmax=lim), aspect="auto")
ax.set_xticks(range(len(tasks))); ax.set_xticklabels([SHORT[t] for t in tasks], fontsize=10)
ax.set_yticks(range(len(srcs)))
ax.set_yticklabels([s.replace("mphi_f_", "").replace("_", " ") for s in srcs], fontsize=9)
ax.set_xlabel("target task  $\\tau_j$", fontsize=11)
ax.set_ylabel("source adapter  $\\phi_i$", fontsize=11)
ax.set_title("Cross-task proposer transfer: % change in Best@6 vs. the untrained proposer\n"
             "(zero-shot; blank = rollout failed; ahc058 greyed out, its base score is ~0)",
             fontsize=12)
for i in range(len(srcs)):
    for j in range(len(tasks)):
        if np.isnan(M[i, j]):
            ax.text(j, i, "--", ha="center", va="center", fontsize=8, color="0.5"); continue
        grey = (a058 is not None and j == a058)
        ax.text(j, i, f"{M[i,j]:+.1f}", ha="center", va="center", fontsize=7.5,
                color="0.45" if grey else ("white" if abs(Mc[i,j] if not grey else 0) > .7*lim else "black"))
        if grey: ax.add_patch(plt.Rectangle((j-.5, i-.5), 1, 1, color="0.92", zorder=0))
# mark the diagonal (in-task) cells
for i, s in enumerate(srcs):
    tag = s.replace("mphi_f_", "").rsplit("_", 1)[0]
    lab = SRC2TASK.get(tag)
    if lab and lab in [SHORT[t] for t in tasks]:
        j = [SHORT[t] for t in tasks].index(lab)
        ax.add_patch(plt.Rectangle((j-.5, i-.5), 1, 1, fill=False, ec="black", lw=2.0, zorder=3))
fig.colorbar(im, ax=ax, label="% change vs. untrained proposer")
out = "/lustre/fsw/portfolios/av/users/yingzim/code/self_adapt_harness/papers/figures/cross_task_transfer.png"
fig.savefig(out, dpi=180); fig.savefig(out.replace(".png", ".pdf"))
print("wrote", out)
row = np.nanmean(Mc, axis=1)
print("  row means (ahc058 excluded):")
for s, m in zip(srcs, row):
    print(f"    {s.replace('mphi_f_',''):16s} {m:+.2f}%")
