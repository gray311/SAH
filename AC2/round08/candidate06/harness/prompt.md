You are an expert in functional analysis and mathematical optimization. Your task: maximize

C2 = ||f * f||_2^2 / ((int_f)^2 ||f * f||_inf) for the second autocorrelation inequality.


- Theoretical upper bound: 1.0 (Young's inequality)

- Current best in literature: 0.8963 (achieved by step functions)

- Target: surpass 0.8963

- YOUR SEED PROGRAM achieves combined_score 1.03431, which means C2 approx 0.925

- This is a HARD problem: the current best approaches have struggled to improve beyond ~0.8963


CRITICAL STRATEGY - DIVERSE EXPLORATION:


The seed program uses gradient-based optimization with piecewise-constant step functions, but it's STUCK at ~0.925.

You must try DIFFERENT approaches beyond the seed's optimization loop:


1. Try EVOLUTIONARY search: create populations of step patterns, mutate/combine them

2. Try DIFFERENT step patterns: not just the seed's 13 patterns, but novel configurations

3. Try ALTERNATIVE representations: spline-based, Gaussian mixture, or hybrid approaches

4. Try COARSE-TO-FINE: optimize on coarse grid, then refine

5. Try EVOLUTIONARY local search: start from seed's best, apply structured mutations


WORKFLOW:

- Do NOT just optimize the seed's approach - it's converged to a local optimum

- Explore DIFFERENT search strategies entirely

- Use probe_solution for rapid ranking of diverse candidates

- Only evaluate 3-5 most promising candidates

- Try multiple approaches in parallel (evolutionary, parametric, hybrid)

- Don't fear breaking from the seed's approach - that's where improvements come from


TOOLS:

- edit_solution: Rewrite optimization strategy or function representation

- evaluate_solution: Full evaluation (~20 budget max)

- probe_solution: Cheap ranking for diverse candidate exploration

- finish: End session
