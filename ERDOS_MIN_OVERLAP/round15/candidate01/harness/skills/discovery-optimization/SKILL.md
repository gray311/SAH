---
name: discovery-optimization
description: "Generate explicit step functions with few jumps, screen with probes, evaluate only promising candidates."
---

# Step Function Strategy for Erdos Minimum Overlap

## Why Step Functions?
The seed optimizer searches continuous functions. But the optimal C5 bound likely comes from a coarse step function with 3-7 jumps.

## Workflow

### Phase 1: Generate Coarse Step Functions

Use step_func_gen to create 8-12 explicit step functions with different structures:
- Binary: h in {0, 1}, total measure = 1
- Three-part: high on [0,a], medium on [a,b], low on [b,2]
- Symmetric around x=1
- Asymmetric with jumps at "golden" locations

### Phase 2: Edit Seed to Use Step Functions

For each step function:
1. EDIT the seed's _objective_fn to directly compute h as a step function
2. Set num_intervals to a smaller value (20-50) for fast evaluation
3. Call probe_solution to estimate C5

### Phase 3: Probe Screening

Use all 30 probes to screen candidates:
- Check integral constraint (sum(h) * dx ≈ 1)
- Check probe C5 < 0.375

### Phase 4: Full Evaluation

Call evaluate_solution on top 2-3 candidates with probe C5 < 0.37

### Phase 5: Refine Binary Functions

If binary functions work well, try different split points:
- h = 1 on [0, 0.5], h = 0 elsewhere (C5 = 0.5)
- h = 1 on [0.25, 0.75], h = 0 elsewhere
- Weighted splits: h = v on [0,a], h = (1-v*a)/(1-a) on [a,2-a], h = 0 elsewhere

## Success Criteria
- combined_score > 1.0
- c5_bound < 0.38092303510845016
