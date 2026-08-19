---
name: discovery-optimization
description: "Generate structural initialization variants for Erdos C5. Use generate_variants to create 5 new patterns (Golomb-7, tri-modal, bipartite, multi-peak, Golomb-5-shifted). Check integral constraint and probe c5_bound for each. Evaluate only if probe c5_bound < 0.375. Budget: 1 generate call + up to 5 probes + 3 evals max."
---

# Structured Search for Erdos C5

## Core Strategy

Seed optimizer uses 15 fixed patterns. To beat C5 ≤ 0.381, need NEW patterns, not hyperparameter tuning.

## Step 1: Generate Structural Variants

CALL generate_variants() once. Returns 5 candidates with pattern_type, integral check, c5_bound (approximate).
Patterns: Golomb-7 (7 marks), Golomb-5-shifted, tri-modal (3 peaks), bipartite (variant), multi-peak (4 peaks).

## Step 2: Filter by Probe

For each candidate:
- Check integral ≈ 1.0 (skip if not close)
- Call probe_solution to get actual c5_bound
- Keep if probe c5_bound < 0.375

## Step 3: Evaluate Top Candidates

Call evaluate_solution on best 1-2 candidates with lowest probe scores.

## Step 4: If Stuck

Try num_intervals=400, penalty_strength=100, num_steps=80000.

## Why This Works

- Structural variants explore different regions of initialization space
- Golomb patterns: equally-spaced marks minimize pairwise overlap
- Probe solution: cheap screening saves evaluation budget

## Key Metrics

- c5_bound target: < 0.375
- combined_score target: > 1.0
- Evals used: ≤ 20 out of 30
