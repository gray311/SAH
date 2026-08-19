---
name: discovery-optimization
description: "Multi-phase Erdos optimization: generate diverse structured initializations, refine via systematic peak mutations, rank with probes, optimize top candidates with adaptive hyperparameters."
---

# Erdos C5 Minimization - Multi-Phase Strategy

## Phase 1: Generate Diverse Constructions
Generate 5-7 initial step function candidates:
- bimodal_asymmetric: Two peaks at x=0.25 and x=1.75, LEFT peak narrower (width=0.12) than RIGHT (width=0.18)
- bimodal_symmetric: Equal width peaks at 0.25 and 1.75 (width=0.15 each)
- triangular_4level: 4-level piecewise linear from x=0 to x=2
- periodic_folded: Period 1 pattern folded onto [0,2]
- golomb_7: Optimal Golomb ruler for 7 marks scaled to domain

Each should satisfy ∫h ≈ 1 (sigmoid output normalized).

## Phase 2: Refine Each Construction
For each initial candidate, apply TARGETED MUTATIONS:

Mutation types:
- Peak_shift: Move each peak by ±0.02, ±0.04, ±0.06 (3 variants per peak)
- Width_tune: Adjust peak widths by ±0.015, ±0.030 (2 variants per peak)
- Mass_rebalance: Shift 5-10% mass between peaks (2 variants)
- Add_noise: Add small Gaussian noise (σ=0.02, 0.05) (2 variants)

Call refine_constructions(initial_h, mutation_type) to get 3 refined candidates.

## Phase 3: Rank with Probes
Use probe_solution on all refined candidates to rank by c5_bound.
Keep top 3 by lowest c5_bound (highest probe score).

## Phase 4: Optimize Top Candidates
For each top candidate, run optimization with:
- num_intervals: 1600 (start), increase to 3200 if progress stalls
- num_steps: 15000
- base_learning_rate: 0.01 (for Phase 1), 0.003 (for Phase 2 if needed)
- penalty_strength: 2000 (Phase 1), 8000 (Phase 2, tighter constraint)
- num_restarts: 1 per initial

## Success Criteria
combined_score > 1.0 means c5_bound < 0.38092303510845016
Save best program with lowest c5_bound.
