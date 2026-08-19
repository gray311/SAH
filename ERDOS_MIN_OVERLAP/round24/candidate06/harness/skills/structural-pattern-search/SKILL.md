---
name: structural-pattern-search
description: Use generate_variants to create 5 completely new initialization patterns. Check integral constraint and probe c5_bound for each. Evaluate only if probe c5_bound < 0.375. If no success, try structural hyperparameter changes (num_intervals=400, penalty_strength=100).
---

# Structural Pattern Search for Erdos C5

## Why Structural Variants Work

The seed has 15 fixed patterns but they may all be in the same basin of attraction.
We need structurally different initializations.

## Workflow

1. CALL generate_variants() ONCE at start

2. For each of 5 candidates:
   - Check integral ≈ 1.0 (skip if not close)
   - CALL probe_solution to get actual c5_bound
   - Keep if probe c5_bound < 0.375 (safety margin)

3. CALL evaluate_solution on the BEST 1-2 candidates (lowest probe scores)

4. If no improvement after 3 evals:
   - Try num_intervals=400 (coarser grid)
   - Try num_restarts=5 (more diversity)
   - Try penalty_strength=100 (stricter integral=1)

## Pattern Types Explained

- golomb_7: 7 equally-spaced marks minimize pairwise overlap
- tri_modal_3: 3 narrow peaks distribute mass at [0.3, 1.0, 1.7]
- bipartite_var: step function with a=0.45
- multi_peak_4: 4 peaks at [0.25, 0.65, 1.05, 1.45]
- golomb_5_shifted: 5 marks shifted to [0.1, 0.5, 0.9, 1.3, 1.7]

## Budget Discipline

- 1 generate_variants call
- Up to 5 probe_solution calls
- Max 3 evaluate_solution calls
- Total evals: ≤ 9 (well under 30 budget)

## Success Criteria

- c5_bound < 0.375 from probe → likely to beat seed on full eval
- combined_score > 1.0 on full eval
- If stuck after all patterns, try structural hyperparameter changes
