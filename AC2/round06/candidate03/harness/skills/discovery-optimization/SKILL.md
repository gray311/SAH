---
name: discovery-optimization
description: "Edit _create_step_initializer to create better step functions. Probe 3-5 variants, evaluate top 2. Max 4 evals."
---

# Step Function C2 Optimization

## Objective: C2 > 1.02665

## Edit _create_step_initializer with these patterns:

Pattern 1 (tall narrow): 0.25n-0.5n, h=1.4
Pattern 2 (bimodal): 0.1n-0.2n h=1.2, 0.5n-0.6n h=1.3
Pattern 3 (asymmetric): 0.1n-0.4n, h=1.3
Pattern 4 (3 peaks): 0.15n-0.25n h=1.2, 0.35n-0.45n h=1.3, 0.6n-0.7n h=1.2
Pattern 5 (wide flat): 0.1n-0.7n, h=0.9

## Workflow:
1. Edit for Pattern 1
2. probe_solution
3. Edit for Pattern 2
4. probe_solution
5. Edit for Pattern 3
6. probe_solution
7. Rank and eval top 2

## Rules:
- Edit concretely in _create_step_initializer
- Probe before eval
- Max 4 evals
- STEP FUNCTIONS ONLY
