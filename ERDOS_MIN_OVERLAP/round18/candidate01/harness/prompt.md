Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016 (combined_score > 1.0 needed).

SEED PROGRAM HAS num_intervals=800 (EXPENSIVE FFT). ONLY GET 1-2 EVALUATIONS.

NEW STRATEGY: DIVERSIFIED MUTATION + PROBE RANKING

1. Use mutation_diversity_probe to generate 5 diverse, VALID candidates
   - Mutate hyperparameters: num_intervals (try 200, 400), base_learning_rate, num_steps
   - Mutate optimizer structure: try fewer restarts, different seeds
   - Mutate objective: try alternative patterns in _get_best_initialization
   - Keep integral constraint in mind
2. EXAMINE probe scores from mutation_diversity_probe (returns c5 estimates)
3. CALL evaluate_solution ON THE SINGLE BEST PROBE (lowest c5 estimate)
4. If no improvement, call mutation_diversity_probe again with DIFFERENT mutation types
5. NEVER waste evals on candidates with c5 > 0.378

KEY: 30 evals budget is tight. Use probes to filter, only 1-2 full evals total.
