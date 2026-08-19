You are solving the Erdos minimum overlap problem: minimize max_k integral h(x)(1-h(x+k)) dx for a step function h: [0,2] -> [0,1] with integral(h)=1.

Current best bound: C5 <= 0.38092303510845016

STRATEGY: The seed program uses gradient descent which gets stuck in local minima. Instead, use COMBINATORIAL SEARCH:
1. Generate structured step function candidates directly (not via latent optimization)
2. Use probe_solution to quickly rank candidates (approximate evaluation)
3. Evaluate promising candidates fully with evaluate_solution
4. Refine successful patterns combinatorially (merge/split/shift regions)
5. Track best c5_bound found; aim for combined_score > 1.0 (c5_bound < 0.3809)

Focus: Generate diverse step function structures, evaluate them, and evolve the best pattern structurally.
