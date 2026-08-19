Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

CRITICAL STRATEGY: The seed optimizer TRAINS from latent patterns for 59000 steps. 
You must:

1. START WITH SEED HYPERPARAMETERS (baseline):
   - num_intervals=800
   - base_learning_rate=0.006
   - num_steps=59000
   - penalty_strength=60.0
   - num_restarts=3
   Run this FIRST to establish baseline.

2. THEN SYSTEMATICALLY VARY ONE HYPERPARAMETER AT A TIME:
   - Vary base_learning_rate: try 0.001, 0.005, 0.01, 0.02 (affects convergence speed)
   - Vary penalty_strength: try 20, 40, 80, 120 (strengthens integral=1 constraint)
   - Vary num_steps: try 10000, 30000, 100000 (training duration)
   - Vary num_intervals: try 400, 1600, 3200 (grid resolution)
   - Vary num_restarts: try 1, 5, 10 (initialization diversity)

3. FOR QUICK SCREENING, USE SHORT TRAINING RUNS (num_steps=5000-10000) with ONE restart:
   This lets you test many hyperparameter combinations cheaply before full training.

4. USE probe_solution TO SCREEN CANDIDATES BEFORE FULL EVALUATION:
   - probe_solution is fast (500 intervals) but approximate
   - evaluate_solution is slow (59000 steps) and exact
   - Only call evaluate_solution if probe suggests c5_bound < 0.382

5. PATTERN-TUNING INSIGHTS (modify latent initialization, not hyperparams):
   - Golomb marks [0.0, 0.4, 0.8, 1.2, 1.6]: well-spaced, minimizes overlap
   - Bipartite: threshold at x=0.5, high on [0,0.5), low on [0.5,2)
   - Tri-modal: three narrow peaks at [0.4, 1.0, 1.6]

6. EVALUATION RULE:
   - First: run seed hyperparameters for full training (59000 steps, 3 restarts)
   - If no improvement, vary ONE hyperparameter at a time
   - Use probe for quick screening of short training runs
   - Only full evaluate if probe indicates potential improvement
