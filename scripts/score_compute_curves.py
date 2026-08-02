#!/usr/bin/env python3
r"""Score-vs-compute curves, one panel per task.

Tests the hypothesis that updating the PROPOSER internalizes reward faster per
executor rollout than (a) leaving the proposer fixed and evolving only external
context, and (b) adapting the executor's own weights (test-time RL).

Everything plotted from our side is measured, not schematic:
  x = cumulative EXECUTOR ROLLOUTS actually spent on the task (one rollout = one
      candidate harness rolled out once by the frozen executor)
  y = best VALID score so far, direction-corrected and normalized so that 0 is
      the task's seed program and 1.0 is the published <=10B best

Series:
  "Update proposer (ours)"  rounds driven by a trained phi (mphi_*)
  "Fixed proposer"          rounds driven by the untrained base phi -- the
                            OpenEvolve-like condition: the harness/context still
                            evolves, the policy proposing it does not
  "TTT-Discover"            published endpoint only. Their repo ships final
                            scores, not per-compute traces, and reproducing the
                            trace needs their training API, so we plot the single
                            (budget, score) point they report and say so.
"""
import json, glob, os, re, sys, collections

RUN = os.environ.get("RUN_ROOT") or "/lustre/fsw/portfolios/av/users/yingzim/runs"
R = f"{RUN}/self_adapt_harness"
BASE_PHI = "c202236235762e1c871ad0ccb60c8ee5ba337b9a"

TASKS = [
    ("eft__math__erdos_min_overlap",    "Erdős min-overlap",       False),
    ("eft__math__circle_packing",       "Circle packing (n=26)",   False),
    ("eft__math__hadamard_maximal_det", "Hadamard max-det",        False),
    ("eft__math__first_autocorr_ineq",  "Autocorrelation I",       False),
    ("eft__math__second_autocorr_ineq", "Autocorrelation II",      False),
    ("eft__ahc_simpletes__ahc039",      "AHC039",                  False),
]

# seed (0.0 on the y axis) and published <=10B best (1.0), in COMBINED units
ANCHOR = {   # (initial program, published <=10B best) in combined units
    "eft__math__erdos_min_overlap":    (0.769452, 0.999974),
    "eft__math__circle_packing":       (0.364237, 1.000373),
    "eft__math__hadamard_maximal_det": (0.143275, 0.576400),
    "eft__math__first_autocorr_ineq":  (0.991237, 1.001437),
    "eft__math__second_autocorr_ineq": (0.954836, 1.056813),
    "eft__ahc_simpletes__ahc039":      (2.377111, 2.476302),
}

# TTT arm: we reproduce the setting ourselves (update the EXECUTOR on its own
# high-scoring rollouts, fixed harness, no proposer). Each task's point sits at
# the number of executor rollouts whose programs went into its training set,
# plus the K rollouts spent evaluating it.
TTT_DIR = f"{R}/ttt_arm"
# TTT-Discover's own Qwen3-8B run (arXiv:2601.16175, Table 2) -- the like-for-like
# ~10B comparison -- at their reported budget of 512 rollouts/step x 50 steps.
TTT_BUDGET = 25600
TTT_PUBLISHED = {
    "eft__math__erdos_min_overlap":    0.380922 / 0.380932,   # 0.380932 raw
    "eft__math__first_autocorr_ineq":  1.505293 / 1.50525,    # 1.50525 raw
    "eft__math__second_autocorr_ineq": 0.9472 / 0.896280,     # 0.9472 raw
}
TTT_FINAL = {
    "eft__math__erdos_min_overlap":    0.999974,   # holds the <=10B best
    "eft__math__second_autocorr_ineq": 1.056813,   # holds the <=10B best
    "eft__math__first_autocorr_ineq":  None,
    "eft__math__circle_packing":       None,
    "eft__math__hadamard_maximal_det": None,
    "eft__ahc_simpletes__ahc039":      None,
}


def round_phi_map():
    m = {}
    for lg in glob.glob(f"{R}/*/*/driver*.log") + glob.glob(f"{R}/*/driver*.log"):
        try: txt = open(lg, errors="ignore").read()
        except OSError: continue
        for mm in re.finditer(r"round(\d+) propose \(phi=([^)]+)\)", txt):
            m[int(mm.group(1))] = mm.group(2)
    return m


def series(task, lower, phi_map):
    """(cumulative rollouts, best-so-far) for trained-phi and fixed-phi rounds."""
    out = {"trained": [], "fixed": []}
    per = {"trained": [], "fixed": []}
    for f in glob.glob(f"{R}/outer/round*/round_summary.json"):
        rd = int(re.search(r"round(\d+)", f).group(1))
        if rd not in phi_map:
            continue
        try: g = json.load(open(f))["groups"].get(task)
        except Exception: continue
        if not g: continue
        kind = "fixed" if phi_map[rd].startswith(BASE_PHI[:12]) else "trained"
        rows = g.get("rows") or []
        scores = [r["score"] for r in rows if r.get("valid") and r.get("score") is not None]
        per[kind].append((rd, len(rows), scores))
    for kind, items in per.items():
        items.sort()
        cum, best = 0, None
        for rd, n, scores in items:
            cum += n
            for s in scores:
                if s <= 0: continue
                best = s if best is None else (min(best, s) if lower else max(best, s))
            if best is not None:
                out[kind].append((cum, best))
    return out


TAGS = {"eft__math__erdos_min_overlap": "erdos_min", "eft__math__circle_packing": "circle_pa",
        "eft__math__hadamard_maximal_det": "hadamard_", "eft__math__first_autocorr_ineq": "first_aut",
        "eft__math__second_autocorr_ineq": "second_au", "eft__ahc_simpletes__ahc039": "ahc039"}


def ttt_curve(task):
    """[(cumulative rollouts, best-so-far)] from the iterative TTT run."""
    f = f"{TTT_DIR}/iter_{TAGS.get(task,'')}/curve.jsonl"
    if not os.path.exists(f):
        return []
    pts = []
    for line in open(f):
        try: d = json.loads(line)
        except Exception: continue
        if d.get("best") is not None:
            pts.append((int(d["cum_rollouts"]), float(d["best"])))
    return sorted(pts)


def normalize(task, v, lower):
    seed, ref = ANCHOR[task]
    if lower:                      # smaller is better -> flip
        return (seed - v) / (seed - ref) if seed != ref else 0.0
    return (v - seed) / (ref - seed) if ref != seed else 0.0


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    phi_map = round_phi_map()
    fig, axes = plt.subplots(2, 3, figsize=(16.5, 9.0), constrained_layout=True)
    fig.suptitle("Where should the reward go?  Updating the proposer vs. the executor vs. context alone",
                 fontsize=15)

    for ax, (task, title, lower) in zip(axes.ravel(), TASKS):
        s = series(task, lower, phi_map)
        for kind, color, style, marker, label in [
            ("trained", "#1f4e79", "-",  "o", "Update proposer (ours)"),
            ("fixed",   "#7f7f7f", "-.", "^", "Fixed proposer (context only)"),
        ]:
            pts = s[kind]
            if not pts: continue
            xs = [p[0] for p in pts]
            ys = [normalize(task, p[1], lower) for p in pts]
            ax.plot(xs, ys, style, color=color, marker=marker, ms=4.5, lw=2.2,
                    mfc="white" if kind == "fixed" else color, label=label)

        tc = ttt_curve(task)
        if tc:
            ax.plot([p[0] for p in tc], [normalize(task, p[1], lower) for p in tc],
                    "--", color="#d67c1c", marker="s", ms=5.5, lw=2.2, mfc="white",
                    label="Update executor (TTT, reproduced)")

        pub = TTT_PUBLISHED.get(task)
        if pub is not None:
            ax.plot([TTT_BUDGET], [normalize(task, pub, lower)], marker="*", ms=16,
                    color="#b03a2e", ls="none",
                    label="TTT-Discover Qwen3-8B (published, 25.6k rollouts)")

        ax.axhline(1.0, color="black", ls=":", lw=1.2, alpha=.7)
        ax.text(0.015, 1.005, "published ≤10B best", transform=ax.get_yaxis_transform(),
                fontsize=7.5, color="black", va="bottom")
        ax.set_title(title, fontsize=12)
        ax.set_xscale("log")
        ax.grid(alpha=.25, ls="--")
        ax.set_xlabel("cumulative executor rollouts (log)", fontsize=9.5)
        ax.set_ylim(-0.05, 1.25)
        if ax in (axes[0][0], axes[1][0]):
            ax.set_ylabel("normalized best validated score", fontsize=10)
        ax.legend(fontsize=7.5, loc="lower right", framealpha=.9)

    out = "/lustre/fsw/portfolios/av/users/yingzim/code/self_adapt_harness/papers/figures/score_compute_curves.png"
    fig.savefig(out, dpi=180)
    fig.savefig(out.replace(".png", ".pdf"))
    print("wrote", out)

    for task, title, lower in TASKS:
        s = series(task, lower, phi_map)
        t = s["trained"][-1] if s["trained"] else None
        f = s["fixed"][-1] if s["fixed"] else None
        print(f"  {title:24s} trained: {('%d rollouts -> %.3f' % (t[0], normalize(task,t[1],lower))) if t else 'n/a':32s}"
              f" fixed: {('%d rollouts -> %.3f' % (f[0], normalize(task,f[1],lower))) if f else 'n/a'}")


if __name__ == "__main__":
    main()
