#!/usr/bin/env python3
"""Method-ablation radar over the 11 tasks.

Series and values are transcribed from papers/tables/proposer_update.tex
(the campaign-best protocol). Each axis is independently min-max scaled over
the plotted series, with minimization tasks (Erdos, AC1) flipped so outward
is always better; a small floor keeps the per-axis minimum visible.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TASKS = ["Erdős", "AC1", "AC2", "CP", "Hadamard",
         "ahc039", "ahc058", "EPLB", "PRISM", "LLM-SQL", "Txn"]
LOWER_BETTER = {"Erdős", "AC1"}

SERIES = {  # name -> (values, style)
 "Initial Program":
   ([0.495056, 1.5186, 0.8558, 0.959764, 0.143275, 534850, 0,
     0.1265, 21.89, 0.6856, 2824.86],
    dict(color="#9a9a9a", ls=":",  lw=1.4, zorder=2)),
 "Best Human":
   ([0.380927, 1.5097, 0.9015, 2.634000, 0.935673, 566997, 847674723,
     0.1265, 21.89, 0.6920, 2724.80],
    dict(color="#222222", ls="-.", lw=1.4, zorder=3)),
 "Qwen3.5-9B + OpenEvolve":
   ([0.385512, 1.5186, 0.8801, 1.172702, 0.397184, 553582, 134486700,
     0.1269, 22.36, 0.6858, 3584.23],
    dict(color="#7f7f7f", ls="-",  lw=1.6, zorder=4)),
 "Finch-9B + OpenEvolve":
   ([0.381100, 1.5141, 0.9122, 1.936000, 0.480585, 553759, 525286896,
     0.1265, 23.93, 0.7024, 3636.36],
    dict(color="#e07b28", ls="-",  lw=1.9, zorder=5)),
 "HarnessRL (initial)":
   ([0.456591, 1.5182, 0.8961, 1.477767, 0.360961, 557225, 134487000,
     0.1265, 24.02, 0.0934, 3610.11],
    dict(color="#9ecae1", ls="-",  lw=1.7, zorder=6)),
 "HarnessRL (context)":
   ([0.395849, 1.5098, 0.9263, 2.370463, 0.517212, 559534, 562824208,
     0.1278, 23.04, 0.7267, 3906.25],
    dict(color="#4292c6", ls="-",  lw=2.0, zorder=7)),
 "HarnessRL (weight)":
   ([0.380919, 1.5098, 0.9339, 2.502000, 0.573283, 559534, 713552303,
     0.1272, 26.26, 0.7415, 4255.32],
    dict(color="#084594", ls="-",  lw=2.6, zorder=9, fill=True)),
 "Previous SOTA ($\\leq$10B)":
   ([0.380932, 1.5031, 0.9472, 2.635983, 0.576400, 557168, 525286896,
     0.1270, 24.70, 0.7341, 4761.90],
    dict(color="#c0392b", ls="--", lw=1.9, zorder=8)),
}

FLOOR = 0.06
vals = np.array([v for v, _ in SERIES.values()], dtype=float)  # (8, 11)
norm = np.zeros_like(vals)
for j, task in enumerate(TASKS):
    col = vals[:, j].copy()
    if task in LOWER_BETTER:
        col = -col
    lo, hi = col.min(), col.max()
    norm[:, j] = FLOOR + (1 - FLOOR) * (col - lo) / (hi - lo)

N = len(TASKS)
ang = np.linspace(0, 2 * np.pi, N, endpoint=False)
ang_c = np.concatenate([ang, ang[:1]])

fig, ax = plt.subplots(figsize=(7.2, 7.6), subplot_kw=dict(polar=True))
ax.set_theta_offset(np.pi / 2); ax.set_theta_direction(-1)
ax.set_ylim(0, 1.02)
ax.set_yticks([0.25, 0.5, 0.75, 1.0]); ax.set_yticklabels([])
ax.grid(color="#d5d5d5", lw=0.7)
ax.spines["polar"].set_color("#bbbbbb")
ax.set_xticks(ang)
ax.set_xticklabels(TASKS, fontsize=10.5)
ax.tick_params(pad=14)

for (name, (v, st)), row in zip(SERIES.items(), norm):
    r = np.concatenate([row, row[:1]])
    ax.plot(ang_c, r, color=st["color"], ls=st["ls"], lw=st["lw"],
            zorder=st["zorder"], label=name)
    if st.get("fill"):
        ax.fill(ang_c, r, color=st["color"], alpha=0.10, zorder=st["zorder"] - 1)

ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.06), fontsize=9.3,
          frameon=False, handlelength=2.2, ncols=3, columnspacing=1.2)
fig.subplots_adjust(left=0.09, right=0.91, top=0.93, bottom=0.15)
for out in ("papers/figures/radar_method_ablation.pdf",
            "papers/figures/radar_method_ablation.png"):
    fig.savefig(out, dpi=200)
print("wrote radar_method_ablation.{pdf,png}")
