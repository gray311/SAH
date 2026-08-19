---
name: discrete-search-playbook
description: Playbook for discrete structure enumeration in Erdős optimization. When continuous optimization stalls, switch to generating sparse step functions and evaluating them directly.
---

# Discrete Structure Search Playbook

## When to Use
After trying continuous optimization with gradient descent and getting no improvement (scores stuck at ~0.9996), switch to discrete search.

## Method

### 1. Generate Discrete Candidates
Call probe_discrete_structures() to get 10-15 sparse step functions.
- These have 3-6 clean transitions
- Each satisfies ∫h = 1 exactly
- No optimization needed - just evaluate

### 2. Quick Screening with probe
Use probe_solution on each candidate (fast, subsampled).
- Track the best c5_bound seen
- Look for candidates with bound < 0.38

### 3. Full Evaluation
Evaluate top 2-3 promising candidates with evaluate_solution.
- A score > 1.0 means you beat the current bound!

### 4. Optional Refinement
If a discrete candidate is close but not quite there:
- Edit to add a short gradient refinement (500-1000 steps max)
- Often the discrete structure is already optimal - no need to refine

## Key Principle
Erdős problems have COMBINATORIAL optima. The best bound likely comes from
a simple 3-5 step function, not a complex gradient descent curve. Enumerate,
then evaluate - don't optimize.
