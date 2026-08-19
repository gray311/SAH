You are an expert in harmonic analysis and mathematical optimization. Your task is to find a step function h: [0,2]→[0,1] that minimizes max_k ∫ h(x)(1-h(x+k)) dx.

**OBJECTIVE**: Maximize combined_score = 0.38092303510845016 / c5_bound

**CONSTRAINTS**: h must integrate to exactly 1 over [0,2] and stay in [0,1].

**STRATEGY**: Do NOT rely solely on gradient descent from random initializations. Instead:

1. Use the new_construct_candidates tool to generate provably valid step functions with integral=1
2. Try explicit piecewise constant constructions (few intervals, clear structure)
3. For each candidate, check that integral(h)=1 before evaluating
4. Use coarse discretization (100-200 intervals) first, then refine

**IMPORTANT**: The seed program's optimizer gets trapped in local optima. You must generate fundamentally different candidate functions, not just tweak hyperparameters. Use new_construct_candidates to create valid h functions with known integral.
