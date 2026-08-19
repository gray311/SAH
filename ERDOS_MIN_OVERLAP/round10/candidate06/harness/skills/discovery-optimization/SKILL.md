---
name: discovery-optimization
description: "Generate mathematically principled step function initializations for Erdos problem using probe_construction tool."
---

# Erdos Minimum Overlap - Construction-Based Strategy

## Problem
Find step function h: [0,2] -> [0,1] minimizing max_k integral h(x)(1-h(x+k)) dx

## Why Construction-Based Search
The seed uses sigmoid of random latents, but optimal h may be a sharp step function.
Mathematically principled constructions are more likely to yield low C5 bounds.

## Strategy

### Phase 1: Systematic Construction Exploration (Use all 30 evals)
1. Use probe_construction tool to get 3-4 different construction types:
   - bimodal_tight: Two narrow peaks at 0.25 and 0.75
   - periodic_step: Alternating step function
   - golomb_ruler: Peaks at optimal spacing [0, 0.25, 0.625, 0.9375, 1.0]
   - triangular_wave: Piecewise linear with 3 levels

2. For EACH construction type, EDIT the _get_best_initialization to:
   - Replace the pattern loop with a single construction
   - Ensure integral(h) ≈ 1 (adjust peak widths)

3. CALL evaluate_solution ONCE per construction type
   - Track which gives best combined_score
   - Stop when score > 1.0

### Phase 2: Refinement
If a construction type yields score > 1.0:
- Make small edits to adjust peak positions/widths
- Fine-tune the constraint penalty
- Try to push score further above 1.0

## Success Criteria
- combined_score > 1.0 (new C5 upper bound)
- Document which construction type worked best

## Tool Usage
- probe_construction: Generate candidate latent vectors (NO EVAL used)
- evaluate_solution: Test a construction (costs 1 eval)
- edit_solution: Modify _get_best_initialization to use a specific construction
