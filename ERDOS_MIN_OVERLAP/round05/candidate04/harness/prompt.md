You are an expert in optimization and harmonic analysis. Your task: evolve a JAX-based optimizer to find a step function h:[0,2]->[0,1] that MINIMIZES max_k ∫h(x)(1-h(x+k))dx, maximizing combined_score = 0.38092303510845016 / c5_bound.

KEY CONSTRAINTS: ∫h(x)dx must equal exactly 1.0 (use sigmoid for numerical stability, then penalize deviation).

SEARCH STRATEGY:
1. The seed optimizer uses Adam with 12 initialization patterns. Start by preserving this structure.
2. Focus on: (a) better initializations (more patterns, smarter patterns), (b) hyperparameter tuning (learning rate, penalty strength, num_intervals, num_steps), (c) different optimizers (adamw, rmsprop, adagrad), (d) structural improvements to the constraint handling.
3. Use quick_eval to cheaply test different configurations (100 iterations, fewer patterns) before full evaluation.
4. If a config satisfies constraints well (score close to 1.0), run full optimization to completion.
5. Prioritize changes that maintain validity while reducing c5_bound.

TOOL USAGE:
- edit_solution: Make targeted changes to _get_best_initialization, Hyperparameters, or _objective_fn. Use SEARCH/REPLACE for small edits.
- evaluate_solution: Full evaluation. Use sparingly (budget=30). Only evaluate configs that look promising from quick_eval.
- quick_eval: Test a config cheaply (100 steps, reduced num_intervals=200). Use this to quickly screen hyperparameters.
- finish: When no improvements after 2 failed quick_evals OR budget exhausted.

MAKE CHANGES that work as complete programs. Don't break the optimization loop or constraint handling.
