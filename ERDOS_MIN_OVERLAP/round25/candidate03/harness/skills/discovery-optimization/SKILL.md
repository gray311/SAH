---
name: discovery-optimization
description: "Combinatorial step function search for Erdos C5 minimization. Direct construction of piecewise constant functions with integral=1 constraint. Bypass gradient training - step functions give exact analytical C5 bounds immediately."
---

# Step Function Optimization for Erdos C5 Problem

## CORE STRATEGY: Direct Step Function Construction

The key insight is that this is a COMBINATORIAL problem about discrete step function structures, NOT a training problem. Gradient-based optimization (seed optimizer) is the WRONG approach.

## Method 1: Step Functions (PRIMARY APPROACH)

1. CALL enumerate_step_functions with pattern_type="auto" to generate valid step functions
2. Each returned candidate has:
   - Exact integral=1 (constraint satisfied by construction)
   - Precomputed c5_bound via FFT
   - Discrete step structure (natural for this problem)
3. CALL evaluate_solution on candidates with c5_bound < 0.375
4. Step functions require NO training - they are ready candidates!

## Step Function Patterns to Explore:

**2-segment (Bipartite):**
- a on [0,a), b on [a,2]
- Integral: a*a + b*(2-a) = 1
- Try a=0.5: then a*0.5 + b*1.5 = 1 => 0.25 + 1.5b = 1 => b = 0.5/1.5 = 0.333

**3-segment:**
- Pieces at [0,1/3), [1/3,2/3), [2/3,2]
- Symmetric around x=1

**Symmetric patterns:**
- h(x) = h(2-x) for some segmentations
- Reduces search space, often optimal

**Asymmetric patterns:**
- All mass in [0,a)
- All mass in [a,2]

## Method 2: Seed Optimizer (Fallback)

ONLY use the seed optimizer if step functions fail:
1. Set num_restarts=3, num_steps=59000 (seed defaults)
2. Tune penalty_strength: 20, 40, 60, 80 (stronger integral constraint)
3. Tune base_learning_rate: 0.001, 0.005, 0.01
4. Use probe_solution sparingly (it's approximate anyway)

## Evaluation Budget

- Step functions: 1 call to enumerate_step_functions, then 2-3 evaluate_solution calls
- Seed optimizer: Can consume 10+ evals if no progress after step functions fail

## Expected Outcome

Step functions naturally satisfy the problem structure. With 3-5 well-designed step functions,
you should find c5_bound < 0.375, potentially < 0.36, giving combined_score > 1.0.
