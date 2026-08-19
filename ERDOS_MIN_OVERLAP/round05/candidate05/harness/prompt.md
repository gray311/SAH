You are an expert in mathematical optimization for step functions. Your goal is to find a function h: [0,2] -> [0,1] that minimizes max_k integral h(x)(1-h(x+k))dx.

Current best upper bound: C5 <= 0.38092303510845016
Goal: Find a step function with combined_score > 1 (i.e., C5_bound < 0.38092303510845016)

STRATEGY: This is a DISCRETE optimization problem. The seed uses gradient descent on a sigmoid parameterization, but step functions may be better found through:
1. Coarse-to-fine approach: Start with few intervals (e.g., 16, 32, 64), optimize, then refine
2. Pattern-based constructions: Try explicit piecewise-constant patterns, not just random initializations
3. Structural simplification: Assume h takes values from a small discrete set (e.g., {0.1, 0.5, 0.9}) then optimize the boundaries
4. Alternative parameterizations: Use hard thresholding or quantized representations

Be decisive: Each evaluation is expensive (30 total budget). Make each edit substantive - change the search paradigm, not just hyperparameters.

Remember: The EVOLVE-BLOCK can completely replace the optimizer. Write entirely new code that implements a different strategy.
