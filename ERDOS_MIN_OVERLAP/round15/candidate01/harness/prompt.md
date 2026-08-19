You are solving the Erdos minimum overlap problem: find a step function h: [0,2] -> [0,1] with integral(h)=1 that minimizes C5 = max_k integral h(x)(1-h(x+k))dx.

Current best bound: C5 <= 0.38092303510845016
Goal: Find h achieving C5 < 0.380923 (combined_score > 1.0).

KEY INSIGHT: The seed optimizer uses continuous sigmoid functions and optimizes for many steps. 
BUT the best solutions are likely COARSE step functions with few jumps.

STRATEGY:
1. FIRST: Use step_func_gen to create explicit piecewise constant functions with 3-7 jumps
2. EDIT the seed to directly define h as a step function (replace sigmoid with piecewise constants)
3. Use probe_solution to quickly compute C5 for each candidate (500 intervals, fast)
4. Call evaluate_solution ONLY on candidates with probe C5 < 0.375
5. If no improvement, try BINARY step functions (h only takes values 0 or 1)

Focus on STRUCTURED step functions, not continuous optimizations. The seed's 12 patterns are all similar Gaussian shapes - they need fundamentally different structures.

Step function template: Define h as sum of indicator functions over intervals [a_i, b_i] with heights v_i, ensuring integral = 1.
