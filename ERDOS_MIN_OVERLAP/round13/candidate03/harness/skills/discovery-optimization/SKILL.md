---
name: discovery-optimization
description: "Generate functions with EXACT integral=1, then optimize overlap. Use probes to screen normalized candidates."
---

# Constraint-First Strategy for Erdos Optimizer

## Problem
The seed's 12 initialization patterns produce latent values that, after sigmoid, have integral ≠ 1. The constraint penalty (61.0×) dominates the loss, so the optimizer wastes iterations fixing constraints instead of minimizing overlap.

## Solution
Generate functions with EXACT integral=1 BEFORE optimization. This removes the constraint penalty and lets the optimizer focus purely on minimizing overlap.

## Workflow

1. **Generate normalized initializations**: Use the new tool normalize_to_integral_one to get h with ∫h=1 exactly.

2. **Edit seed to use normalized h**: Replace the initial latent in the optimizer with the normalized h (no sigmoid needed - h is already in [0,1]).

3. **Probe immediately**: Call probe_solution on the normalized h to get c5_bound estimate. No training needed.

4. **Evaluate promising candidates**: Call evaluate_solution on candidates with c5_bound < 0.37.

5. **If stuck**: EDIT to make small adjustments to normalized h (e.g., shift one interval, change one amplitude) to create new valid candidates.

## Why This Works
- Removing constraint penalty lets optimizer focus on overlap
- Probes screen VALID candidates quickly
- 30 probes can find multiple normalized candidates
- Only 2-3 full evaluations needed
