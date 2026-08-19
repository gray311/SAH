You are optimizing functions to maximize C2 = ||f★f||₂² / ((∫f)² ||f★f||_∞). Current best: 0.8962799441554086 (step function, combined_score 1.03896).

STRATEGY: The step-function record is achieved by multi-level step patterns. To beat it, you MUST refine step patterns systematically, not abandon them for smooth functions.

EXPLORATION PLAN:
1. At iteration 1, call analyze_step_pattern to understand the current step pattern structure
2. Generate mutations using step_mutator with small, targeted changes (height perturbation ±0.02-0.08, width expansion 3-8%, spacing adjustments)
3. Use probe_solution to rapidly rank 10-15 mutations, then evaluate top 3-5
4. If no improvement after 8 iterations of step refinement, try hybrid patterns (combine two seed patterns)
5. Only as last resort (iteration >20), call generate_candidates for non-step families
6. Never spend 3+ evals on a single mutation type without probe filtering

CRITICAL: f(x)≥0, use softplus/exponential for constraints. Leverage FFT convolution. Start with 600 intervals, refine to 800-1000 if needed.

Tools: edit_solution (implement mutations), evaluate_solution (full score, 30 budget), probe_solution (approx score, 30 budget, FAST - USE THIS TO FILTER), analyze_step_pattern (structural analysis of current best), step_mutator (guided mutation generation).
