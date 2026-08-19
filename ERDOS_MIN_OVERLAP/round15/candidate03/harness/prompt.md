You are solving the Erdos minimum overlap problem: minimize max_k integral h(x)(1-h(x+k)) dx

Current best bound: C5 <= 0.38092303510845016

KEY INSIGHT: The seed uses sigmoid-smoothed latents which produce similar Gaussian-like shapes. This is a local optimum.

BETTER STRATEGY: Use HARD STEP FUNCTIONS with different support patterns, not smooth latents.

Steps:

1. Create hard step-function initializations (no sigmoid):
   - 3-block patterns: high on [0,a], medium on [a,b], low on [b,2]
   - 4-block patterns with different breakpoint ratios
   - Support-split: h=0 on [0,x), h=1 on [x,2]

2. For each step-function initialization, EDIT the seed to:
   - Replace sigmoid(latent) with step-function directly
   - Set num_restarts=1, use that one pattern
   - Use higher learning rate (0.01-0.02)

3. Use probe_solution to check c5_bound (use probe_budget aggressively)

4. Call evaluate_solution on top 2-3 candidates with c5_bound < 0.375

5. If no success, try COARSE-TO-FINE: start with num_intervals=100, optimize, then increase to 800

6. Focus on piecewise CONSTANT functions, not sigmoid-smoothed latents

Success: combined_score > 1.0 (c5_bound < 0.380923)
