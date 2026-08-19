Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016.

Goal: Beat seed score of 0.999945 (c5_bound < 0.380923).

Strategy:

1. The seed optimizer trains 59000 steps per candidate and uses 15 pattern initializations.

2. FULLY EVALUATE THE SEED: set num_restarts=3, seed_start=0, and run the seed exactly as-is.
   Record its c5_bound. This is your baseline.

3. Single-candidate mutation: set num_restarts=1 and carefully mutate ONE hyperparameter at a time:
   - num_intervals: try [1600, 2000, 2560] (finer discretization for FFT accuracy)
   - base_learning_rate: try [0.001, 0.002, 0.01]
   - num_steps: try [30000, 60000, 80000]
   - penalty_strength: try [30.0, 100.0, 150.0]
   Try ONE mutation per eval.

4. If single mutations fail, try SMALL structural changes:
   - Add 2-3 new pattern initializations (keep total <= 20)
   - Change sigmoid activation to tanh with scaling
   - Use jnp.linspace for better peak placement

5. Use 1-2 evals per iteration. Max 15-20 iterations.

6. STOP when combined_score > 1.0.
