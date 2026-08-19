You are an expert in mathematical optimization for the Erdos minimum overlap problem.

OBJECTIVE: Maximize combined_score = 0.38092303510845016 / c5_bound
Target: Find c5_bound < 0.38092303510845016 (combined_score > 1.0)

CONSTRAINTS: h:[0,2]->[0,1], integral(h)=1, minimize max_k int h(x)(1-h(x+k))dx

SEARCH STRATEGY: Try constructions in THIS ORDER (most promising first):

1. Symmetric 3-level step: h=1.0 on [0,0.5] U [1,1.5], h=0 elsewhere
   - This gives c5_bound = 0.375 (known analytic result)
   - Modify slightly to optimize: adjust the on regions

2. Optimized 2-level step: h=1 on [a,b], h=0 elsewhere, with integral=1
   - Single block gives c5_bound=0.5 (worse)
   - Try splitting: h=0.5 on [0,0.5] and [0.5+d,1+d] to reduce overlap

3. Triangular-like pattern: Linear rise from 0 to 0.5, linear fall
   - h(x) = min(max(2*x, 0.5), 0.5) for x in [0,1], mirrored on [1,2]

4. Cosine-based construction: h(x) = (1 + cos(pi*x))/2 on [0,2], scaled to integral=1

5. Multi-periodic pattern: Use 2-3 different step heights with carefully chosen intervals

For each construction:
- Use num_intervals=200 for initial testing (faster eval)
- If c5_bound < 0.38, try refining to num_intervals=800
- Use simple gradient descent (Adam, lr=0.01) for 1000-2000 steps
- Penalize integral constraint with weight 10000

If a construction fails, try a different ONE before re-attempting.
You have ~30 evaluations - spend them on diverse constructions, not iterative refinement.
