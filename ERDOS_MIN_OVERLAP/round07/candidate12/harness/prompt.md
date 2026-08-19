You are an expert mathematician specializing in harmonic analysis and optimization. Your task is to find a step function h: [0, 2] → [0, 1] that minimizes max_k ∫ h(x)(1-h(x+k)) dx.

**OBJECTIVE**: Maximize combined_score = 0.38092303510845016 / c5_bound. You must achieve combined_score > 1.0.

**CONSTRAINTS**: h must be in [0, 1] and integrate to exactly 1 over [0, 2].

**CRITICAL**: The seed program's multi-restart Adam optimizer is trapped at the seed score. DO NOT make minor hyperparameter tweaks. COMPLETELY REWRITE the EVOLVE-BLOCK to use a fundamentally different approach.

**STRATEGY**: Construct piecewise-constant step functions directly with controlled support sets. Start with 2-3 breakpoints, optimize their positions and heights, then optionally refine. Avoid relying on gradient descent from random initializations.

**BUDGET**: ~30 evaluations total. Use probe_solution to rapidly rank candidates before full evaluation. Stop as soon as combined_score > 1.0.

**PROCESS**:
1. Call probe_solution first to check constraint satisfaction and get approximate score
2. Use probe results to iteratively refine your construction
3. When probe confirms constraints, call evaluate_solution for final scoring
4. If score improves, keep the edit; if not, try a completely different construction

**COMPLETE REWRITES ONLY**: Edit the entire ErdosOptimizer class with new initialization logic, optimization approach, or architecture. Do not edit single lines.
