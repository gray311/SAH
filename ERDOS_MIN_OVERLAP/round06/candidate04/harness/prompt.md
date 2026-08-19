You are an expert in mathematical optimization for the Erdős minimum overlap problem.

**OBJECTIVE**: Find a step function h: [0,2]→[0,1] with ∫h=1 that minimizes max_k ∫h(x)(1-h(x+k))dx.
Target: combined_score = 0.38092303510845016 / c5_bound > 1.0

**KEY INSIGHT**: The seed's gradient-based optimizer is trapped in local optima. 
Instead of gradient descent, you should use DIRECT CONSTRUCTION: generate candidate
piecewise constant functions systematically and evaluate them.

**STRATEGY**: 
1. Use construct_candidates to generate structured step functions (1-2 evaluations)
2. Pick the best candidate and refine with targeted edits
3. Try coarse discretization (num_intervals=100-200) then refine

**CONSTRAINTS**: h∈[0,1], ∫h=1 over [0,2]

**AGENCY**: Complete rewrites of the EVOLVE-BLOCK are encouraged. Generate complete
working programs that directly construct candidate solutions.
