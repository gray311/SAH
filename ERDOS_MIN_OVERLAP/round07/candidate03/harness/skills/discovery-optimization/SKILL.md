---
name: discovery-optimization
description: "C\u2085 optimization via constructive search. Generate piecewise constant candidates, rank with probes, refine. Target combined_score > 1.0 by beating c5_bound 0.380923."
---

# Constructive Approach for C₅ Bound

## Why Gradient Descent Fails

The seed's 12-pattern initialization + Adam on 800 intervals = trapped in poor local optima.

## Success Strategy: Construct, Don't Optimize from Random

### Step 1: Generate Candidate Step Functions

Use construct_step_functions to create diverse piecewise constant functions:
- 2-10 intervals only (start simple!)
- Enforce integral=1 exactly
- Try many different patterns (single block, double block, uniform, etc.)

### Step 2: Probe and Rank

For each candidate, call probe_solution to get approximate score.
Filter out anything with c5_bound >= 0.380923.

### Step 3: Refine Only the Promising Ones

If you find c5_bound < 0.380923, THEN use gradient descent to fine-tune THAT specific construction.
Do NOT try 800 intervals on random seeds.

### Concrete Construction Patterns

Try these as STARTING POINTS:

1. **Uniform**: h(x) = 0.5 for all x in [0,2] (∫h = 1 ✓)

2. **Two-block**: h=1 on [0,0.5] and [1.5,2]

3. **Centered Mass**: h concentrated around x=1

### Execution Flow

1. Call construct_step_functions with n_candidates=20, max_intervals=10
2. For each candidate: call probe_solution
3. Keep top 3-5 by approximate score
4. Call evaluate_solution on those 3-5
5. If any score > 1.0, DONE. Otherwise, try different constructions.
