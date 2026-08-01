#!/usr/bin/env python3
"""Build the cross-task transfer matrix from the rows submitted by
cross_task_transfer.sh.

Cell (i,j) = direction-normalized improvement of source adapter phi_i on target
task tau_j over the BASE proposer phi_0 on the same task, so a positive number
means "this adapter proposes better harnesses for that task than the untrained
proposer does".  Minimized tasks are sign-flipped so >0 is always better.
"""
import json, os, sys, glob

OUT = os.path.expandvars("$RUN_ROOT/self_adapt_harness/outer")
WS  = os.path.expandvars("$RUN_ROOT/self_adapt_harness/cross_task")
LOWER = {"eft__math__erdos_min_overlap", "eft__math__first_autocorr_ineq"}
SHORT = {"eft__math__erdos_min_overlap":"Erd","eft__math__first_autocorr_ineq":"AC1",
 "eft__math__second_autocorr_ineq":"AC2","eft__math__circle_packing":"CP",
 "eft__math__hadamard_maximal_det":"Had","eft__ahc_simpletes__ahc039":"a039",
 "eft__ahc_simpletes__ahc058":"a058","adrs__eplb":"EPLB","adrs__prism":"PRI",
 "adrs__llm_sql":"SQL","adrs__txn_scheduling":"Txn"}

rows = []
for line in open(os.path.join(WS, "rows.txt")):
    src, rnd, job = line.split()
    f = os.path.join(OUT, f"round{int(rnd):03d}", "round_summary.json")
    if not os.path.exists(f):
        print(f"  (round{rnd} for {src} not collected yet)", file=sys.stderr); continue
    g = json.load(open(f))["groups"]
    rows.append((src, {t: v.get("best_score") for t, v in g.items()}))

if not rows:
    sys.exit("no collected rows yet")
base = dict(rows[0][1]) if rows[0][0] == "BASE" else {}
tasks = [t for t in SHORT if any(t in r[1] for r in rows)]

print("source".ljust(22) + "".join(SHORT[t].rjust(8) for t in tasks) + "    mean")
for src, sc in rows:
    cells, out = [], []
    for t in tasks:
        v, b = sc.get(t), base.get(t)
        if v is None or b is None or b == 0:
            out.append("   --"); continue
        d = (b - v) / abs(b) if t in LOWER else (v - b) / abs(b)   # direction-normalized
        cells.append(d); out.append(f"{100*d:+7.1f}")
    m = f"{100*sum(cells)/len(cells):+7.1f}" if cells else "     --"
    print(src.replace("mphi_f_", "").ljust(22) + "".join(out) + m)
print("\ncells are % improvement over the BASE proposer on the same task; >0 = better.")
