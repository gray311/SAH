You are solving the Erdos minimum overlap problem: minimize max_k integral h(x)(1-h(x+k)) dx

for a step function h: [0,2] -> [0,1] with integral(h)=1.

Current best bound: C5 <= 0.38092303510845016

CRITICAL INSIGHT: The seed's 12 initialization patterns all use sigmoid(latent) but none guarantee integral(h)=1. This means they start from INFEASIBLE points and waste optimizer steps fixing constraints.

STRATEGY: Create INITIALIZATIONS that already satisfy integral(h)=1, then optimize from feasible points.

Steps:
1. CALL constraint_satisfying_init to get latents where sigmoid(latent) integrates to exactly 1
2. For each initialization, EDIT the seed to use ONLY that pattern (num_restarts=1, seed_start=pattern_index)
3. Call probe_solution to verify c5_bound < 0.37 (no need to check integral - it's already 1)
4. Call evaluate_solution on top 1-2 candidates with c5_bound < 0.37
5. If none work, EDIT _get_best_initialization to add a pattern using piecewise constant values (not sigmoid) that can be scaled to integral=1

Key insight: Start FEASIBLE. The FFT evaluator is fast enough that you can afford 3-5 full evaluations if your initializations are good.
