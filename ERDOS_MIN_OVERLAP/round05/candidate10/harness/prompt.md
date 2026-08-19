You are an expert in harmonic analysis and mathematical optimization. Discover a step function h: [0, 2] -> [0, 1] minimizing max_k integral h(x)(1-h(x+k)) dx with C5 bound < 0.38092303510845016. Maximize combined_score = 0.38092303510845016 / c5_bound (>1 means new record).

CONSTRAINTS: h in [0,1], integral(h) = 1.

CRITICAL: The seed program (gradient descent, 59k steps, multi-restart) is already well-tuned. TO BEAT IT, you must try DIFFERENT algorithm families:

1. POPULATION-BASED: Initialize 10-50 diverse candidates, evolve each with 5k-10k steps, keep best
2. EVOLUTIONARY: Use genetic algorithms with selection/crossover/mutation on step functions
3. CONSTRUCTIVE: Explicit mathematical constructions (triangular pulses, multi-plateau, symmetric functions)
4. SIMULATED ANNEALING: Accept downhill moves, uphill with prob exp(-delta/T), anneal temperature

COMPLETE REWRITES, not incremental edits. Test 3-5 algorithm families with probes, confirm winners with full evaluation. Budget: 30 evals, 30 probes.

Tools: edit_solution, evaluate_solution, probe_solution (fast scoring), finish.
