---
name: discovery-optimization
description: "Maximize C2 constant using systematic step-function exploration. Step functions are the record holders (0.8963); start there immediately with concrete patterns. Use probes to rank variants, evals sparingly for top candidates. Diversify to Gaussian/B-spline if stuck."
---

# C2 Optimization: Step Function Focus

## Critical Insight
Step functions (piecewise-constant) achieved 0.8963 - the current record. The seed uses piecewise-linear. Your FIRST task: implement a step function variant.

## Step 1: Immediate Switch to Step Functions

Implement one of these patterns in the EVOLVE-BLOCK:
- Single wide step: 0.25n to 0.75n, height=1.0
- Multi-level: 3 segments with heights 1.0, 2.0, 1.5
- Asymmetric: 0.15n to 0.55n, height=1.15 (wider left)
- Two-step with gap: 0.1n-0.35n at 1.4, gap, 0.55n-0.9n at 0.85

Make SEARCH/REPLACE edits targeting the _create_initializer method. Change ONE pattern.

## Step 2: Probe Variants

Create 3-5 step function variants with different parameters:
- Vary support: 0.1n-0.9n, 0.2n-0.8n, 0.3n-0.7n
- Vary heights: 0.9, 1.0, 1.1, 1.2, 1.5, 2.0
- Vary number of steps: 2 segments, 3 segments, 4 segments

For each variant:
1. Edit the initializer to implement this pattern
2. Call probe_solution to get quick score
3. Note the probe score
4. Do NOT eval yet - test more variants

After probing, compare scores and select top 2.

## Step 3: Full Evaluation

For each top 2 candidate:
1. Run 2-3 different random seeds (change pattern_idx or key)
2. Call evaluate_solution for each seed
3. Track which seed performed best

Max 5 evals total. If all <1.027, try different function family.

## Step 4: If Stuck - Switch Families

If step functions don't beat 1.027 after 3 evals:
- Try Gaussian mixtures: sum of 3-5 Gaussians with softplus for positivity
- Try B-splines: smooth piecewise polynomials with optimized knots

NEVER tune the same pattern for 3+ evals without trying something new.

## Tool Priority
1. edit_solution - implement step function pattern
2. probe_solution - test 3-5 variants quickly
3. evaluate_solution - confirm top 2 only
4. finish - when done or no progress
