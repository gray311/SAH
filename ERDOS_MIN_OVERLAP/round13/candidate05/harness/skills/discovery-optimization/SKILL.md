---
name: discovery-optimization
description: "Escape the seed's local minimum by generating radically different initialization structures (piecewise constant, binary step, asymmetric) and screening with probes before evaluation."
---

# Breaking the Erdos Local Minimum

## The Problem
The seed uses 12 similar Gaussian/sigmoid initializations. All converge to c5 ≈ 0.3809.

## The Solution
Generate INITIALLY DIFFERENT structures that cannot be reached by tuning.

## Tool: generate_5_init
- Creates 5 fundamentally different step function shapes
- Each has a latent vector that when sigmoided gives h(x) in [0,1]
- Types: binary step, piecewise 3-part, asymmetric trapezoid, bimodal, sparse 3-peak

## Tool: probe_solution
- CHEAP: 500 intervals, ~10s runtime
- Returns estimated c5_bound and constraint satisfaction
- Use all 30 probes to test the 5 initializations BEFORE any full evaluation

## Execution Flow
1. generate_5_init → get 5 latents
2. For each latent: EDIT seed to use ONLY that pattern (num_restarts=1, seed_start=0, use the latent as h)
3. probe_solution all 5 → check c5_bound < 0.37
4. evaluate_solution on max 2 best candidates
5. Repeat with new random seed for generate_5_init
6. If combined_score > 1.0, finish

## Success
- combined_score > 1.0 means c5_bound < 0.380923
