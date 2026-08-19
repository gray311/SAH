You are solving the Erdos minimum overlap problem: minimize max_k integral h(x)(1-h(x+k)) dx
for a step function h: [0,2] -> [0,1] with integral(h)=1.

Current best bound: C5 <= 0.38092303510845016

CRITICAL INSIGHT: The seed program's optimizer gets STUCK at its initial local optimum.
The multi-restart initialization with 12 patterns is GOOD but NOT GOOD ENOUGH.
The optimizer is trying to find a BETTER local optimum but fails to escape the seed's basin.

STRATEGY: Do NOT just tune hyperparameters. You MUST fundamentally CHANGE the search strategy.

PHASE 1 - CONSTRUCTION-FIRST APPROACH (Use 15 evals):
Instead of optimizing a continuous latent space, construct EXACT step functions by specifying:
- A set of interval boundaries in [0, 2] (e.g., [0, 0.5, 1.0, 1.5, 2.0])
- A value in [0,1] for each interval

This gives YOU control over the DISCRETE structure. Try constructions like:
- Uniform distribution: 2 intervals, each with h=0.5
- Concentrated mass: Many tiny intervals at one location
- Alternating: k intervals alternating between a and b (where a*b=1 for integral=1)
- Golomb-like spacing: intervals spaced to minimize overlaps

Edit the EVOLVE-BLOCK to IMPLEMENT this construction approach. Replace the entire optimizer
with a constructor that takes specified boundaries/values and computes the C5 bound directly.

PHASE 2 - SYSTEMATIC CONSTRUCTION SPACE SEARCH (Use 15 evals):
Once you have working constructions, systematically explore:
- Number of intervals: 2, 3, 4, 5, 6, 8, 10
- For each n, try different value combinations where all values are in [0,1] and sum to 1
- Use probe_solution to quickly score constructions before full evaluation

PHASE 3 - GRADUAL COMPLEXITY (Use 10 evals):
Start with simple constructions (2-3 intervals), then gradually increase complexity.
For each complexity level, do a systematic grid search over the parameter space.

IMPORTANT: Each edit must COMPLETELY REPLACE the EVOLVE-BLOCK with a working implementation
of your proposed construction strategy. Do NOT try to "tune" the existing optimizer.

SUCCESS CRITERIA: combined_score > 1.0 (meaning c5_bound < 0.38092303510845016)
