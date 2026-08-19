---
name: discovery-optimization
description: "Discretization-first strategy for Erdos problem with structured initialization backup."
---

# Erdos Minimum Overlap - Discretization-First Strategy

## Problem Understanding
We need to find h: [0,2] → [0,1] with ∫h=1 minimizing max_k ∫h(x)(1-h(x+k))dx.
The seed uses 800 intervals - but the optimal solution may need different resolution.

## Why Discretization Matters
The FFT-based correlation computation is sensitive to grid alignment. 
- Too coarse (e.g., 200): Cannot represent fine features
- Too fine (e.g., 8000): Numerical precision issues, optimization harder
- Optimal may be 1200-4800 with careful feature placement

## Strategy: Discretization Sweep (Primary Attack)

### Round 1: Coarse-to-Fine Sweep
Test: num_intervals ∈ {200, 400, 600, 800, 1200, 1600, 2400, 3200, 4800, 6400}
For each:
- Test learning_rates ∈ {0.001, 0.005, 0.01, 0.02, 0.05, 0.1}
- Use probe_solution to quickly reject variants with poor constraint satisfaction
- Evaluate top 1-2 per discretization

### Round 2: Analyze Winners
For the best-performing discretization:
- If constraint not satisfied: increase penalty_strength (100→500→2000→10000)
- If objective doesn't improve: try construct_structured_init

### Round 3: Structured Initialization (If Needed)
Use construct_structured_init to generate principled initializations:
- bimodal_tight: Peaks at 0.25, 0.75 (theoretical for C5)
- golomb_5: Marks at optimal spacing [0, 0.5, 1.25, 1.625, 2] scaled
- periodic_2: Simple alternating pattern

Then sweep hyperparameters on each structured init.

## Tool Usage
1. probe_solution: Screen constraint satisfaction (integral ≈ 1) - CRITICAL
2. construct_structured_init: Get mathematically principled starts
3. evaluate_solution: Only call after probe passes or structured init is good

## Success Criteria
- combined_score > 1.0 (c5_bound < 0.380923)
- Best combined_score > seed score

## Common Pitfalls
- Don't waste evaluations on trivial hyperparameter changes without discretization sweep
- Always verify constraint satisfaction
- If stuck at seed score, try MUCH finer discretization (4800-8000)
