---
name: c2-systematic-exploration
description: A method playbook for C2 optimization using variant-based exploration. Generate variants, rank by approx_c2, then evaluate top candidates.
---

# C2 Systematic Exploration

## Objective
Maximize C2 > 1.026 by systematically exploring function families.

## Core Strategy
1. Call variant_generator to get 10-20 variants per family
2. Examine approx_c2 scores and pick top 3
3. Use edit_solution to implement the best variant
4. Call probe_solution to verify
5. Call evaluate_solution on top 2 candidates
6. If no improvement: try a NEW family

## Function Families
1. Step functions (record holders at 0.8963) - vary width, height, pieces
2. Gaussian mixtures - vary K, sigma, means
3. B-splines - vary num_knots, spacing
4. Exponential - vary rate, terms

## Workflow
- Generate variants for a family
- Rank by approx_c2
- Edit top variant, probe, then evaluate
- Max 4 evals per family, then diversify
