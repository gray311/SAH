Erdos minimum overlap: find step function h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016.

The seed optimizer already has 15 initialization patterns and 3 restarts. 

Your job: GENERATE MORE DIVERSE RESTART POINTS using generate_extra_restarts.

Strategy:

1. Call generate_extra_restarts(temperature=0.8) to get 10 NEW diverse patterns
2. Merge with seed's patterns (keep the best 15 initializations total)
3. Run optimizer with num_restarts=5 on the merged set
4. Evaluate the BEST 1 candidate (lowest analytical c5_bound < 0.365)
5. If no improvement, regenerate with temperature=1.0

Why this works:
- Seed patterns: sine/cosine, Golomb, bipartite, tri-modal, Gaussian bumps
- Extra patterns: piecewise constant, piecewise linear, random block patterns, 
  delta-like constructions - patterns the seed's optimizer might miss
- More restarts = better exploration of high-dimensional search space
- Analytical screening still saves evals, but MORE lenient threshold
