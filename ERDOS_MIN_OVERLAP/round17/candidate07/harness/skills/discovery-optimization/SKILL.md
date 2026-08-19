---
name: discovery-optimization
description: "Golomb ruler optimization: use optimize_golomb_marks to find optimal 5-mark placements, then edit the code to use those marks. Only 1 eval needed per candidate."
---

# Analytical Screening Strategy

## Problem
The seed optimizer trains for 59000 steps per candidate. We need to screen MANY candidates cheaply.

## Solution: generate_ready_candidates Tool

This tool generates 3 structurally diverse, VALID initializations:
- Golomb ruler pattern (optimal spacing)
- Bipartite pattern (separated support)
- Tri-modal pattern (3 narrow peaks)

Each candidate has:
- h: pre-sigmoided latent (values in [0,1])
- integral: precomputed sum(h)*dx (should be 1.0)
- c5_bound: precomputed max correlation (analytical, no training)

## Workflow

1. CALL generate_ready_candidates(temperature=0.5)

2. Analyze the 3 candidates:
   - Skip if integral != 1.0 (constraint violation)
   - Skip if c5_bound >= 0.375 (too bad)
   - Keep if c5_bound < 0.37

3. CALL evaluate_solution on ALL candidates with c5_bound < 0.37

4. If none pass, CALL generate_ready_candidates again with temperature=0.8 for more diversity

5. Total probes used: 1-2. Total evaluations: 2-3 max.

## Why This Works

- 3 structural diversity: Golomb (optimal spacing), Bipartite (separated), Tri-modal (distributed)
- Precomputed integral: no constraint violation waste
- Precomputed c5: fast analytical screening
- Only 2-3 full evaluations needed

## Example Expected Output

Candidate 0 (Golomb): integral=0.998, c5=0.365 -> EVALUATE
Candidate 1 (Bipartite): integral=1.001, c5=0.372 -> EVALUATE
Candidate 2 (Tri-modal): integral=0.995, c5=0.385 -> SKIP (too high)
