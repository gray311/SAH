Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

STRATEGY (CRITICAL - THIS IS HOW YOU WIN):

1. ANALYZE THE SEED: The seed program already uses 800 intervals and many restart patterns.
   It's NOT the intervals that need changing - it's the MUTATION STRATEGY.

2. RANDOM TUNING FAILS: Hyperparameter sweeps (learning rate, steps, penalty) are useless
   because the optimization landscape is NOT smooth. The solver must make STRUCTURAL changes.

3. THE WINNING MOVE: Force the solver to think about the mathematical structure of h.
   - Try BIPARTITE functions: h(x) = sigmoid(a*x + b) thresholded - this creates a single jump
   - Try MULTI-MODAL functions: 3-4 narrow peaks with specific spacing
   - Try GOLOMB-RULER patterns: marks at specific positions [0, 0.4, 0.8, 1.2, 1.6]

4. HOW TO EDIT:
   - Change num_intervals from 800 to 400 or 1600 (coarser or finer)
   - Change the initialization pattern COMPLETELY - not "add small noise" but REPLACE with:
     * "h = sigmoid(10*(x - 0.5))" for a single jump at 0.5
     * "h = 0.5 + 0.5*sin(10*pi*x)" for oscillating pattern
     * "h = piecewise: 0 for x<0.4, 1 for 0.4<=x<0.6, 0 for x>=0.6"

5. DO NOT: Tune learning_rate, penalty_strength, num_steps. These won't work.

6. DO: Completely replace the latent initialization with a new analytic pattern.
