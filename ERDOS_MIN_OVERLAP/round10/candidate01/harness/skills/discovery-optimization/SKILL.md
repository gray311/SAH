---
name: discovery-optimization
description: "Structural initialization exploration for Erdos optimizer. Generate and test diverse mathematical constructions systematically using probes."
---

# Erdos Minimum Overlap - Structural Search Strategy

## Core Insight
The seed optimizer uses sigmoid(latent) as a generic initialization. We need to bypass this by directly constructing diverse step function shapes.

## Phase 1: Structural Analysis (Use First 5 Evals)
1. Call `structural_analysis` on seed to see its structure
2. Identify key features: peak locations, widths, asymmetry

## Phase 2: Diverse Construction (Main Strategy - 20 Evals)
For each of 4 construction types:
- `construct_structured_init` generates: bimodal_tight, triangular_3step, periodic_2, golomb_5
- For each construction:
  1. Use `probe_solution` to quickly check constraint satisfaction (10 sec)
  2. If integral close to 1 and c5_reasonable, call `evaluate_solution` (full score)
  3. Track best combined_score

## Phase 3: Targeted Improvements (If stuck)
If best score < 1.0:
- Call structural_analysis again on current best
- Generate constructions with MODIFIED parameters (narrower peaks, different spacing)
- Focus on constructions that reduce overlap at the problematic lags

## Important Notes
- Use probe_solution extensively - it's CHEAP (~10s vs minutes for full eval)
- A combined_score > 1.0 means c5_bound < 0.38092303510845016
- Document which construction type worked best
