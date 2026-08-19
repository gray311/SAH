You are an expert in harmonic analysis and numerical optimization. Your task: improve a Python script that finds a step function h: [0,2]→[0,1] minimizing max_k ∫ h(x)(1-h(x+k))dx.

Target: Beat C5 ≤ 0.38092303510845016 (your score = 0.38092303510845016 / c5_bound; >1 means new record).

Key insight: The seed uses 800 intervals and gradient descent. To find better constructions, try:
1. Vary the discretization (100-2000 intervals) to find better representations
2. Use structured step functions: uniform blocks, triangular patterns, sine-based initializations
3. Try multi-restart optimization with diverse seeds
4. Always ensure ∫h(x)dx=1 exactly (otherwise invalid)

STRATEGY: Use probe_solution to cheaply rank candidate designs (many fast tests, few full evals). When probe scores are similar, use full evaluation. Focus on structural changes: number of intervals, function shape patterns, initialization diversity.

Use edit_solution for targeted changes: modify interval counts, restructure _get_best_initialization, adjust penalty_strength. Then probe_solution, evaluate_solution only on promising candidates.

Call finish when you beat the seed (score > 0.999641) or exhaust budget.
