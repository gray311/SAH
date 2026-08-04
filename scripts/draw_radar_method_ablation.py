#!/usr/bin/env python3
"""Method-ablation radar over the 11 tasks.

Values are transcribed from papers/tables/proposer_update.tex (campaign-best
protocol). Normalization gives every axis the same semantic anchors:
    0 (center)  = Initial Program (the seed)
    1 (ring)    = Previous <=10B SOTA  -> drawn as the red dashed unit circle
so a series outside the ring sets a new state of the art on that axis.
Minimization tasks (Erdos, AC1) are handled by measuring progress seed->SOTA.
Scores below the seed clip at the center.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TASKS = ["Erdős", "AC1", "AC2", "CP", "Hadamard",
         "ahc039", "ahc058", "EPLB", "PRISM", "LLM-SQL", "Txn"]

INITIAL = [0.495056, 1.5186, 0.8558, 0.959764, 0.143275, 534850, 0,
           0.1265, 21.89, 0.6856, 2824.86]
SOTA    = [0.380932, 1.5031, 0.9472, 2.635983, 0.576400, 557168, 525286896,
           0.1270, 24.70, 0.7341, 4761.90]

SERIES = {
 "Best Human":
   ([0.380927, 1.5097, 0.9015, 2.634000, 0.935673, 566997, 847674723,
     0.1265, 21.89, 0.6920, 2724.80],
    dict(color="#222222", ls="-.", lw=1.5, zorder=4)),
 "Qwen3.5-9B + OpenEvolve":
   ([0.385512, 1.5186, 0.8801, 1.172702, 0.397184, 553582, 134486700,
     0.1269, 22.36, 0.6858, 3584.23],
    dict(color="#8a8a8a", ls="-",  lw=1.7, zorder=5)),
 "Finch-9B + OpenEvolve":
   ([0.381100, 1.5141, 0.9122, 1.936000, 0.480585, 553759, 525286896,
     0.1265, 23.93, 0.7024, 3636.36],
    dict(color="#e07b28", ls="-",  lw=2.0, zorder=6)),
 "HarnessRL (weight)":
   ([0.380919, 1.5098, 0.9339, 2.502000, 0.573283, 559534, 713552303,
     0.1272, 26.26, 0.7415, 4255.32],
    dict(color="#084594", ls="-",  lw=2.6, zorder=8, fill=True)),
}

def norm(vals):
    out = []
    for v, s0, s1 in zip(vals, INITIAL, SOTA):
        out.append(max((v - s0) / (s1 - s0), 0.0))   # sign flips fall out
    return np.array(out)

N = len(TASKS)
ang = np.linspace(0, 2 * np.pi, N, endpoint=False)
ang_c = np.concatenate([ang, ang[:1]])
RMAX = 1.9

fig, ax = plt.subplots(figsize=(9.2, 6.6), subplot_kw=dict(polar=True))
ax.set_theta_offset(np.pi / 2); ax.set_theta_direction(-1)
ax.set_ylim(0, RMAX)
ax.set_yticks([0.5, 1.5]); ax.set_yticklabels([])
ax.grid(color="#e0e0e0", lw=0.7)
ax.spines["polar"].set_color("#bbbbbb")
ax.set_xticks(ang); ax.set_xticklabels(TASKS, fontsize=11)
ax.tick_params(pad=12)

# the SOTA ring and the seed center
th = np.linspace(0, 2 * np.pi, 361)
ax.plot(th, np.ones_like(th), color="#c0392b", ls="--", lw=2.0, zorder=7,
        label="Previous SOTA ($\\leq$10B)  (unit ring)")
ax.plot(0, 0, marker="o", ms=4, color="#9a9a9a", zorder=3)

for name, (v, st) in SERIES.items():
    r = norm(v); r = np.concatenate([r, r[:1]])
    ax.plot(ang_c, r, color=st["color"], ls=st["ls"], lw=st["lw"],
            zorder=st["zorder"], label=name,
            marker="o" if st.get("fill") else None, ms=4)
    if st.get("fill"):
        ax.fill(ang_c, r, color=st["color"], alpha=0.10, zorder=st["zorder"]-1)

fig.legend(*ax.get_legend_handles_labels(), loc="center left",
           bbox_to_anchor=(0.015, 0.5), fontsize=10, frameon=False,
           handlelength=2.2)
fig.subplots_adjust(left=0.36, right=0.94, top=0.92, bottom=0.08)
for out in ("papers/figures/radar_method_ablation.pdf",
            "papers/figures/radar_method_ablation.png"):
    fig.savefig(out, dpi=200)
print("wrote radar_method_ablation.{pdf,png}")
