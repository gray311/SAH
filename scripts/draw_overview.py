#!/usr/bin/env python3
"""Overview of HarnessRL, drawn to a vector PDF (and a PNG for quick viewing).

Two rows: the outer loop synthesizes a harness, the inner loop runs it on the
frozen executor. Both feedback boxes sit directly under the node they feed, so
the return paths are short verticals: advantage -> phi (the only gradient) and
ratchet -> the next round's context. Grey = frozen, blue = the only trained part.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

BLUE, GREY, ORANGE = "#1f4e79", "#6b6b6b", "#c9700a"
FILL = {"trained": "#dce9f6", "frozen": "#e8e8e8", "proc": "#ffffff", "sig": "#fdebd6"}
EDGE = {"trained": BLUE, "frozen": "#7a7a7a", "proc": "#8a8a8a", "sig": ORANGE}

W, H = 2.05, 0.78                      # box size in data units
TOP, BOT = 2.0, 0.0                    # row centres
XS = [0.0, 2.55, 5.10, 7.65]           # column centres

fig, ax = plt.subplots(figsize=(11.6, 3.5))
ax.set_xlim(-1.35, 9.0); ax.set_ylim(-1.25, 3.15); ax.axis("off")

def box(x, y, title, sub, kind):
    ax.add_patch(FancyBboxPatch((x - W/2, y - H/2), W, H,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        fc=FILL[kind], ec=EDGE[kind], lw=1.1, zorder=3))
    ax.text(x, y + 0.16, title, ha="center", va="center", fontsize=10.5,
            zorder=4, color="black")
    ax.text(x, y - 0.16, sub, ha="center", va="center", fontsize=7.8,
            zorder=4, color="#444444", linespacing=1.25)
    return x, y

# outer loop (top row)
ctx  = box(XS[0], TOP, r"task context $c_\tau$", "spec · incumbent\n· experience digest", "proc")
phi  = box(XS[1], TOP, r"proposer $\pi_\phi$",   "frozen base + LoRA\n(the only trained part)", "trained")
spec = box(XS[2], TOP, r"$K$ harness specs",     "prompt · skills · tools\n· control params", "proc")
rev  = box(XS[3], TOP, "review chain",           "static gates · sandbox\n· parity repair", "proc")
# inner loop (bottom row)
rat  = box(XS[0], BOT, "ratchet",         "best program\n+ best harness", "sig")
adv  = box(XS[1], BOT, "advantage",       "gap-normalized\nreward, RLOO", "sig")
sco  = box(XS[2], BOT, r"scores $s_k$",   "best valid score\nper rollout", "proc")
exe  = box(XS[3], BOT, r"executor $M_0$", "FROZEN · edit→evaluate\nunder budget $B$", "frozen")

def arrow(a, b, color="#555555", dashed=False, rad=0.0, label=None,
          lx=0, ly=0, ha="center"):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=11,
        lw=1.15, color=color, zorder=2,
        linestyle=(0, (4, 2.4)) if dashed else "solid",
        connectionstyle=f"arc3,rad={rad}",
        shrinkA=0, shrinkB=0))
    if label:
        ax.text((a[0]+b[0])/2 + lx, (a[1]+b[1])/2 + ly, label, fontsize=7.6,
                ha=ha, va="center", color=color, zorder=5,
                bbox=dict(fc="white", ec="none", pad=0.9))

def R(p): return (p[0] + W/2, p[1])
def L(p): return (p[0] - W/2, p[1])
def U(p): return (p[0], p[1] + H/2)
def D(p): return (p[0], p[1] - H/2)

# forward flow: left to right on top, right to left on the bottom
for a, b in [(ctx, phi), (phi, spec), (spec, rev)]:
    arrow(R(a), L(b))
arrow(D(rev), U(exe), label="materialize\n" + r"$H_k$", lx=0.42, ha="left")
for a, b in [(exe, sco), (sco, adv)]:
    arrow(L(a), R(b))

# feedback: two short verticals, nothing crosses a box
arrow(U(adv), D(phi), color=ORANGE, dashed=True,
      label=r"update $\phi$ only", lx=0.60, ha="left")
arrow(U(rat), D(ctx), color=ORANGE, dashed=True,
      label="next round", lx=-0.55, ha="right")
# scores -> ratchet, routed below the row so it clears the advantage box
y = BOT - H/2 - 0.34
ax.plot([sco[0], sco[0], rat[0], rat[0]], [BOT - H/2, y, y, BOT - H/2],
        color=ORANGE, lw=1.15, ls=(0, (4, 2.4)), zorder=1)
ax.add_patch(FancyArrowPatch((rat[0], y + 0.02), (rat[0], BOT - H/2),
    arrowstyle="-|>", mutation_scale=11, lw=1.15, color=ORANGE, zorder=2,
    shrinkA=0, shrinkB=0))

# loop labels
ax.text(XS[0] - W/2, TOP + H/2 + 0.30, "OUTER LOOP — synthesize a harness",
        fontsize=8.6, color="#666666", weight="bold", va="center")
ax.text(XS[0] - W/2, y - 0.30,
        "INNER LOOP — run it on the frozen executor; no gradient reaches $M_0$",
        fontsize=8.6, color="#666666", weight="bold", va="center")

out = "papers/figures/overview"
fig.savefig(out + ".pdf", bbox_inches="tight")
fig.savefig(out + ".png", dpi=200, bbox_inches="tight")
print("wrote", out + ".pdf/.png")
