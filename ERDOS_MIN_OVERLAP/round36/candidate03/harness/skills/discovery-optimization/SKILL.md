---
name: discovery-optimization
description: "Use generate_bipartite_step or generate_multimodal_step to create valid step functions\nfrom scratch, then refine them. Always start with analytically valid candidates rather than\nmutating complex existing programs.\n\nBipartite functions (single threshold at t=1.0) are mathematically guaranteed to satisfy\nintegral(h)=1. Multimodal functions with separated peaks can reduce overlap at specific k values.\n\nStrategy: Generate diverse step function templates -> evaluate -> pick best -> refine."
---

# Erdos C5 - Step Function Generation Strategy

## Phase 1: Generate Valid Step Functions

1. CALL generate_bipartite_step with different styles:
   - style="single_peak": Creates h(x)=1 for x in [0,1], 0 otherwise
   - style="two_peaks": Two symmetric peaks at [0.5, 1.0]
   - style="plateau": Flat top in the middle
   - style="step_down": Decreasing steps from 1 to 0

2. CALL generate_multimodal_step with peak_positions=[0.4, 1.0, 1.6]
   - Three peaks spread across [0,2] to reduce overlap
   - This can be better than single/bipartite for C5 minimization

3. Examine the generated h arrays and their integral checks

## Phase 2: Evaluate and Refine

1. CALL evaluate_solution on the best generated candidate
2. If combined_score <= 1.0, generate new variants:
   - Modify peak positions (try [0.25, 1.0, 1.75] instead of [0.4, 1.0, 1.6])
   - Adjust peak heights (try [0.8, 1.0, 0.8] instead of [1.0, 1.0, 1.0])
   - Add/remove peaks

3. Use probe_solution to screen new variants before full evaluation

## Phase 3: Targeted Improvements

If the seed optimizer already has a program:
1. Analyze its structure
2. Generate step functions that are structurally different
3. Compare and keep the best

## Key Rules
- ALWAYS start with step function GENERATION, not mutation
- Ensure integral(h) = 1 before evaluation
- Keep h values in [0,1]
- Multi-peak functions often beat single-peak for C5
- Try peak positions that are NOT symmetric if single peak fails
