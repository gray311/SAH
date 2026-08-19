You are solving the Erdos minimum overlap problem: minimize max_k integral h(x)(1-h(x+k)) dx
for a step function h: [0,2] -> [0,1] with integral(h)=1.

Current best bound: C5 <= 0.38092303510845016
Goal: Find combined_score > 1.0 (c5_bound < 0.380923)

CRITICAL WORKFLOW:
1. START with the seed program and CALL evaluate_solution ONCE to establish baseline (expected ~0.999855)
2. For EVERY edit, FIRST call probe_solution to check constraint satisfaction:
   - Compute integral(h) from the probe output
   - If |integral(h) - 1| >= 0.05, DISCARD that variant immediately
   - If constraint passes, get approximate c5_bound from probe
3. Primary search: INCREASE num_intervals to 1600, 3200, 4000, 6400
   - Finer discretization enables more complex step functions
   - For each new resolution, test 2-3 LR values (0.001, 0.003, 0.007)
4. Secondary: Adjust penalty_strength to 30, 100, 200, 500
5. Use probe to RANK variants by approximate c5_bound BEFORE any full eval
6. Call evaluate_solution ONLY on top 1-2 probe-ranked variants per resolution
7. Keep only the best full-eval result
Expected usage pattern: ~6 full evals total (1 baseline + 5 on promising probe variants)
